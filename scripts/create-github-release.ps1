[CmdletBinding()]
param(
    [string]$ReleaseVersion = "",
    [string]$ServiceAccountJsonPath = ".secrets/firestore-mobile-rw.json",
    [string]$OutputDir = "build/apk",
    [switch]$BuildOnly,
    [switch]$DryRun,
    [switch]$SkipTests,
    [switch]$SkipBuild
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-Tool {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [string[]]$Arguments = @(),
        [switch]$AllowFailure
    )

    $hasNativePreference = $null -ne (Get-Variable -Name PSNativeCommandUseErrorActionPreference -ErrorAction SilentlyContinue)
    if ($hasNativePreference) {
        $previousNativePreference = $PSNativeCommandUseErrorActionPreference
        $PSNativeCommandUseErrorActionPreference = $false
    }

    try {
        $output = & $FilePath @Arguments 2>&1
        $exitCode = $LASTEXITCODE
    }
    finally {
        if ($hasNativePreference) {
            $PSNativeCommandUseErrorActionPreference = $previousNativePreference
        }
    }

    if (-not $AllowFailure -and $exitCode -ne 0) {
        $renderedArguments = if ($Arguments.Count -gt 0) {
            " " + ($Arguments -join " ")
        }
        else {
            ""
        }
        $message = ($output | ForEach-Object { "$_" }) -join [Environment]::NewLine
        throw "Fallo al ejecutar: $FilePath$renderedArguments`n$message"
    }

    return [pscustomobject]@{
        ExitCode = $exitCode
        Output   = @($output | ForEach-Object { "$_" })
    }
}

function Get-SingleLineOutput {
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Result
    )

    return ($Result.Output -join [Environment]::NewLine).Trim()
}

function Write-Utf8NoBom {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,
        [Parameter(Mandatory = $true)]
        [string]$Content
    )

    $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
    [System.IO.File]::WriteAllText($Path, $Content, $utf8NoBom)
}

function Resolve-FirestoreProjectId {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot
    )

    if ($env:FIRESTORE_PROJECT_ID -and $env:FIRESTORE_PROJECT_ID.Trim()) {
        return $env:FIRESTORE_PROJECT_ID.Trim()
    }

    $envFilePath = Join-Path $RepoRoot ".env"
    if (-not (Test-Path $envFilePath -PathType Leaf)) {
        return $null
    }

    foreach ($line in Get-Content $envFilePath -Encoding UTF8) {
        if ($line -match "^\s*(#|$)") {
            continue
        }
        if ($line -match "^\s*FIRESTORE_PROJECT_ID\s*=\s*(.+?)\s*$") {
            $candidate = $matches[1].Trim()
            if (
                ($candidate.StartsWith("'") -and $candidate.EndsWith("'")) -or
                ($candidate.StartsWith('"') -and $candidate.EndsWith('"'))
            ) {
                $candidate = $candidate.Substring(1, $candidate.Length - 2).Trim()
            }
            if ($candidate) {
                return $candidate
            }
        }
    }

    return $null
}

function Get-NewLineStyle {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Text
    )

    if ($Text.Contains("`r`n")) {
        return "`r`n"
    }

    return "`n"
}

function Get-LatestReleaseTag {
    $result = Invoke-Tool -FilePath "git" -Arguments @("tag", "--merged", "HEAD", "--list", "v0.*", "--sort=-version:refname")
    $tags = @($result.Output | Where-Object { $_.Trim() })
    if ($tags.Count -eq 0) {
        throw "No se encontró ninguna tag v0.* mergeada en HEAD."
    }

    return $tags[0].Trim()
}

function Get-CommitSubjectsSinceTag {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Tag
    )

    $result = Invoke-Tool -FilePath "git" -Arguments @("log", "--format=%s", "$Tag..HEAD")
    $subjects = @($result.Output | Where-Object { $_.Trim() })
    return ,$subjects
}

function Get-ChangedPathsSinceTag {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Tag
    )

    $result = Invoke-Tool -FilePath "git" -Arguments @("diff", "--name-only", "$Tag..HEAD")
    $paths = @($result.Output | Where-Object { $_.Trim() })
    return ,$paths
}

function Normalize-ReleaseTag {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Version
    )

    $normalized = $Version.Trim()
    if (-not $normalized) {
        throw "La versión indicada está vacía."
    }
    if (-not $normalized.StartsWith("v")) {
        $normalized = "v$normalized"
    }
    if ($normalized -notmatch "^v\d+\.\d+\.\d+$") {
        throw "La versión debe cumplir el formato v0.x.y: $normalized"
    }

    return $normalized
}

function Get-NextReleaseTag {
    param(
        [Parameter(Mandatory = $true)]
        [string]$LatestTag,
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [string[]]$CommitSubjects,
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [string[]]$ChangedPaths
    )

    $version = [System.Version]::Parse($LatestTag.TrimStart("v"))
    $minorBump = $false

    foreach ($subject in $CommitSubjects) {
        if ($subject -match "^feat(\(.+\))?:") {
            $minorBump = $true
            break
        }
    }

    if (-not $minorBump) {
        foreach ($path in $ChangedPaths) {
            if ($path.StartsWith("src/")) {
                $minorBump = $true
                break
            }
        }
    }

    if ($minorBump) {
        return "v{0}.{1}.0" -f $version.Major, ($version.Minor + 1)
    }

    return "v{0}.{1}.{2}" -f $version.Major, $version.Minor, ($version.Build + 1)
}

function Get-ChangeLogInfo {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path
    )

    $raw = Get-Content -Raw -Encoding UTF8 $Path
    $newLine = Get-NewLineStyle -Text $raw
    $pattern = "(?s)## \[Unreleased\]" + [regex]::Escape($newLine) + "(?<section>.*?)(?=" + [regex]::Escape($newLine) + "## \[)"
    $match = [regex]::Match($raw, $pattern)
    if (-not $match.Success) {
        throw "No se pudo localizar la sección [Unreleased] en CHANGELOG.md."
    }

    return [pscustomobject]@{
        Raw      = $raw
        NewLine  = $newLine
        Pattern  = $pattern
        Section  = $match.Groups["section"].Value.Trim("`r", "`n")
    }
}

function Get-ReleaseNotesBody {
    param(
        [Parameter(Mandatory = $true)]
        [string]$UnreleasedSection,
        [Parameter(Mandatory = $true)]
        [AllowEmptyCollection()]
        [string[]]$CommitSubjects,
        [Parameter(Mandatory = $true)]
        [string]$NewLine
    )

    $hasUsefulBullets = ($UnreleasedSection -split "\r?\n" | Where-Object { $_ -match "^\s*-\s+" }).Count -gt 0
    if ($hasUsefulBullets) {
        return $UnreleasedSection.Trim()
    }

    $subjects = @($CommitSubjects | Where-Object { $_.Trim() })
    if ($subjects.Count -eq 0) {
        throw "No hay contenido útil en [Unreleased] ni commits para sintetizar notas."
    }

    $bulletLines = $subjects | ForEach-Object { "- $_" }
    return "### Cambiado$NewLine$NewLine" + ($bulletLines -join $NewLine)
}

function Update-ChangeLogText {
    param(
        [Parameter(Mandatory = $true)]
        [pscustomobject]$Info,
        [Parameter(Mandatory = $true)]
        [string]$Tag,
        [Parameter(Mandatory = $true)]
        [string]$ReleaseNotesBody
    )

    $newLine = $Info.NewLine
    $versionLabel = $Tag.TrimStart("v")
    $releaseHeader = "## [$versionLabel] - $(Get-Date -Format 'yyyy-MM-dd')"
    $replacement = "## [Unreleased]$newLine$newLine$releaseHeader$newLine$newLine$ReleaseNotesBody$newLine$newLine"
    $updated = [regex]::Replace(
        $Info.Raw,
        $Info.Pattern,
        [System.Text.RegularExpressions.MatchEvaluator]{
            param($match)
            $replacement
        },
        1
    )

    $repoUrl = "https://github.com/KikoNet13/frosthaven-campaign-journal"
    $unreleasedBlockPattern = "\[Unreleased\]:(?:\r?\n\s*https://github\.com/KikoNet13/frosthaven-campaign-journal/compare/[^\r\n]+)"
    $unreleasedBlock = "[Unreleased]:$newLine  $repoUrl/compare/$Tag...HEAD"
    $updated = [regex]::Replace($updated, $unreleasedBlockPattern, $unreleasedBlock, 1)

    $releaseLinkLabel = "[$versionLabel]:"
    if ($updated -notmatch [regex]::Escape($releaseLinkLabel)) {
        $releaseBlock = "$releaseLinkLabel$newLine  $repoUrl/releases/tag/$Tag"
        $updated = $updated.Replace($unreleasedBlock, "$unreleasedBlock$newLine$releaseBlock")
    }

    return $updated
}

function Test-GitHubReleaseExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Tag
    )

    $result = Invoke-Tool -FilePath "gh" -Arguments @("release", "list", "--limit", "100") -AllowFailure
    if ($result.ExitCode -ne 0) {
        return $false
    }

    $matches = @($result.Output | Where-Object {
        $columns = @(($_ -split "\s+") | Where-Object { $_ })
        $columns.Count -gt 0 -and $columns[0] -eq $Tag
    })

    return $matches.Count -gt 0
}

function Test-GitTagExists {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Tag
    )

    $result = Invoke-Tool -FilePath "git" -Arguments @("tag", "--list", $Tag)
    $matches = @($result.Output | Where-Object { $_.Trim() -eq $Tag })
    return $matches.Count -gt 0
}

function Build-ApkWithEmbeddedSecrets {
    param(
        [Parameter(Mandatory = $true)]
        [string]$RepoRoot,
        [Parameter(Mandatory = $true)]
        [string]$BuildVersion,
        [Parameter(Mandatory = $true)]
        [int]$BuildNumber,
        [Parameter(Mandatory = $true)]
        [string]$ServiceAccountJsonPath,
        [Parameter(Mandatory = $true)]
        [string]$OutputDir
    )

    $serviceAccountPath = if ([System.IO.Path]::IsPathRooted($ServiceAccountJsonPath)) {
        $ServiceAccountJsonPath
    }
    else {
        Join-Path $RepoRoot $ServiceAccountJsonPath
    }

    if (-not (Test-Path $serviceAccountPath -PathType Leaf)) {
        throw "No existe el JSON de cuenta de servicio: $serviceAccountPath"
    }

    $firestoreProjectId = Resolve-FirestoreProjectId -RepoRoot $RepoRoot
    if (-not $firestoreProjectId) {
        throw "No se pudo resolver FIRESTORE_PROJECT_ID desde entorno ni desde .env."
    }

    $serviceAccountJson = Get-Content $serviceAccountPath -Raw -Encoding UTF8
    try {
        $null = $serviceAccountJson | ConvertFrom-Json
    }
    catch {
        throw "El archivo de cuenta de servicio no es JSON válido: $serviceAccountPath"
    }

    $serviceAccountJsonB64 = [Convert]::ToBase64String([System.Text.Encoding]::UTF8.GetBytes($serviceAccountJson))
    $projectIdLiteral = $firestoreProjectId.Replace("\", "\\").Replace("'", "\\'")
    $jsonB64Literal = $serviceAccountJsonB64.Replace("\", "\\").Replace("'", "\\'")

    $mobileSecretsPath = Join-Path $RepoRoot "src/frosthaven_campaign_journal/config/_mobile_runtime_secrets.py"
    $mobileSecretsDir = Split-Path -Parent $mobileSecretsPath
    if (-not (Test-Path $mobileSecretsDir -PathType Container)) {
        New-Item -ItemType Directory -Path $mobileSecretsDir | Out-Null
    }

    $moduleContent = @"
# Generated by scripts/create-github-release.ps1. Do not commit.
FIRESTORE_PROJECT_ID = '$projectIdLiteral'
GOOGLE_APPLICATION_CREDENTIALS_JSON_B64 = '$jsonB64Literal'
"@

    try {
        Write-Utf8NoBom -Path $mobileSecretsPath -Content $moduleContent

        $env:FLET_CLI_NO_RICH_OUTPUT = "1"
        Invoke-Tool -FilePath "pipenv" -Arguments @(
            "run",
            "flet",
            "build",
            "apk",
            ".",
            "--yes",
            "--no-rich-output",
            "--skip-flutter-doctor",
            "-o",
            $OutputDir,
            "--build-version",
            $BuildVersion,
            "--build-number",
            "$BuildNumber"
        ) | Out-Null

        $outputRoot = if ([System.IO.Path]::IsPathRooted($OutputDir)) {
            $OutputDir
        }
        else {
            Join-Path $RepoRoot $OutputDir
        }

        $canonicalApkPath = Join-Path $outputRoot "frosthaven_campaign_journal.apk"
        if (Test-Path $canonicalApkPath -PathType Leaf) {
            $apkPath = (Resolve-Path $canonicalApkPath).Path
        }
        else {
            $latestApk = Get-ChildItem $outputRoot -File -Filter *.apk | Sort-Object LastWriteTime -Descending | Select-Object -First 1
            if (-not $latestApk) {
                throw "No se encontró ningún .apk en: $outputRoot"
            }
            $apkPath = $latestApk.FullName
        }

        $apkHash = Get-FileHash $apkPath -Algorithm SHA256
        return [pscustomobject]@{
            ApkPath = $apkPath
            Sha256  = $apkHash.Hash
        }
    }
    finally {
        if (Test-Path $mobileSecretsPath -PathType Leaf) {
            Remove-Item $mobileSecretsPath -Force
        }
    }
}

$repoRoot = Get-SingleLineOutput -Result (Invoke-Tool -FilePath "git" -Arguments @("rev-parse", "--show-toplevel"))
Set-Location $repoRoot

$branchName = Get-SingleLineOutput -Result (Invoke-Tool -FilePath "git" -Arguments @("rev-parse", "--abbrev-ref", "HEAD"))
if (-not $BuildOnly -and -not $DryRun -and $branchName -ne "main") {
    throw "La release real solo puede ejecutarse desde main. Rama actual: $branchName"
}

$worktreeStatus = Get-SingleLineOutput -Result (Invoke-Tool -FilePath "git" -Arguments @("status", "--porcelain"))
if (-not $BuildOnly -and $worktreeStatus) {
    throw "El worktree debe estar limpio antes de continuar."
}
if ($BuildOnly -and $worktreeStatus) {
    Write-Warning "BuildOnly continúa con worktree sucio; el artefacto no es trazable para release."
}

$latestTag = Get-LatestReleaseTag
$commitSubjects = Get-CommitSubjectsSinceTag -Tag $latestTag
$changedPaths = Get-ChangedPathsSinceTag -Tag $latestTag

if (-not $ReleaseVersion -and $commitSubjects.Count -eq 0) {
    if (-not $BuildOnly -and -not (Test-GitHubReleaseExists -Tag $latestTag)) {
        throw "No hay commits nuevos desde $latestTag y la GitHub Release asociada no existe."
    }
    Write-Host "SKIP: no hay commits nuevos desde $latestTag."
    exit 0
}

$targetTag = if ($ReleaseVersion) {
    Normalize-ReleaseTag -Version $ReleaseVersion
}
else {
    Get-NextReleaseTag -LatestTag $latestTag -CommitSubjects $commitSubjects -ChangedPaths $changedPaths
}

if ($targetTag -ne $latestTag -and (Test-GitTagExists -Tag $targetTag)) {
    throw "La tag objetivo ya existe: $targetTag"
}

$changeLogPath = Join-Path $repoRoot "CHANGELOG.md"
$changeLogInfo = Get-ChangeLogInfo -Path $changeLogPath
$releaseNotesBody = Get-ReleaseNotesBody -UnreleasedSection $changeLogInfo.Section -CommitSubjects $commitSubjects -NewLine $changeLogInfo.NewLine
$buildNumber = [int](Get-SingleLineOutput -Result (Invoke-Tool -FilePath "git" -Arguments @("rev-list", "--count", "HEAD"))) + 1
$buildVersion = $targetTag.TrimStart("v")

$shouldRunTests = -not $SkipTests -and -not $BuildOnly
if ($shouldRunTests) {
    $env:PYTHONPATH = "src"
    Invoke-Tool -FilePath "pipenv" -Arguments @("run", "python", "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py") | Out-Null
}

$apkInfo = $null
if (-not $SkipBuild) {
    $apkInfo = Build-ApkWithEmbeddedSecrets `
        -RepoRoot $repoRoot `
        -BuildVersion $buildVersion `
        -BuildNumber $buildNumber `
        -ServiceAccountJsonPath $ServiceAccountJsonPath `
        -OutputDir $OutputDir
}

if ($DryRun) {
    Write-Host "DRY RUN"
    Write-Host "Última tag: $latestTag"
    Write-Host "Tag objetivo: $targetTag"
    Write-Host "BuildNumber: $buildNumber"
    if ($apkInfo) {
        Write-Host "APK: $($apkInfo.ApkPath)"
        Write-Host "SHA256: $($apkInfo.Sha256)"
    }
    Write-Host ""
    Write-Host $releaseNotesBody
    exit 0
}

if ($BuildOnly) {
    if (-not $apkInfo) {
        Write-Host "BUILD ONLY: no se solicitó compilación."
        exit 0
    }
    Write-Host "BUILD ONLY"
    Write-Host "Versión objetivo: $targetTag"
    Write-Host "APK: $($apkInfo.ApkPath)"
    Write-Host "SHA256: $($apkInfo.Sha256)"
    exit 0
}

Invoke-Tool -FilePath "gh" -Arguments @("auth", "status") | Out-Null
if (Test-GitHubReleaseExists -Tag $targetTag) {
    throw "La GitHub Release objetivo ya existe: $targetTag"
}

$updatedChangeLog = Update-ChangeLogText -Info $changeLogInfo -Tag $targetTag -ReleaseNotesBody $releaseNotesBody
Write-Utf8NoBom -Path $changeLogPath -Content $updatedChangeLog

$tmpDir = Join-Path $repoRoot ".codex_tmp"
if (-not (Test-Path $tmpDir -PathType Container)) {
    New-Item -ItemType Directory -Path $tmpDir | Out-Null
}

$releaseNotesPath = Join-Path $tmpDir "$($targetTag)-release-notes.md"
$releaseNotesFullBody = $releaseNotesBody + $changeLogInfo.NewLine + $changeLogInfo.NewLine + "Recordatorio operativo: rota la clave de servicio móvil tras publicar una release con credenciales embebidas."
Write-Utf8NoBom -Path $releaseNotesPath -Content $releaseNotesFullBody

Invoke-Tool -FilePath "git" -Arguments @("add", "CHANGELOG.md") | Out-Null
Invoke-Tool -FilePath "git" -Arguments @("commit", "-m", "chore(release): cortar release $targetTag") | Out-Null
Invoke-Tool -FilePath "git" -Arguments @("tag", "-a", $targetTag, "-m", $targetTag) | Out-Null
Invoke-Tool -FilePath "git" -Arguments @("push", "--atomic", "origin", "main", $targetTag) | Out-Null
Invoke-Tool -FilePath "gh" -Arguments @("release", "create", $targetTag, "--title", $targetTag, "--notes-file", $releaseNotesPath, $apkInfo.ApkPath) | Out-Null

Write-Host "RELEASED"
Write-Host "Tag: $targetTag"
Write-Host "APK: $($apkInfo.ApkPath)"
Write-Host "SHA256: $($apkInfo.Sha256)"
