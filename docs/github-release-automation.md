# Flujo de Release GitHub Automatizada

## Metadatos

- `doc_id`: DOC-GITHUB-RELEASE-AUTOMATION
- `purpose`: Definir el flujo local automatizado de releases GitHub con tag, changelog y APK desde Codex App.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-08
- `next_review`: 2026-03-20

## Objetivo

Establecer un flujo automatizado y reproducible para:

1. detectar si procede una nueva release diaria;
1. calcular la siguiente versión `v0.x.y`;
1. cortar `CHANGELOG.md`;
1. validar el repo antes de publicar;
1. generar y adjuntar el `.apk`;
1. publicar la GitHub Release con las mismas notas del changelog.

## Alcance

Incluye:

- automatización local en Codex App sobre el worktree del repo;
- sincronización `origin/main` por `fast-forward only`;
- release notes derivadas de `CHANGELOG.md`;
- build Android directo desde la propia automatización;
- publicación en GitHub vía `gh`.

No incluye:

- GitHub Actions o CI remota adicional;
- rollback automático si ya hubo publicación parcial remota;
- subida a Google Play.

## Prerrequisitos

- rama activa `main`;
- worktree limpio;
- `gh auth status` válido;
- `pipenv` operativo;
- Android toolchain operativo;
- `.secrets/firestore-mobile-rw.json`;
- `FIRESTORE_PROJECT_ID` en entorno o `.env`.

## Automatización directa en Codex App

Ruta oficial: `$CODEX_HOME/automations/release-diaria-github/automation.toml`

Contrato operativo:

- la automatización ejecuta el flujo completo de release directamente;
- no invoca `scripts/create-github-release.ps1` en el camino automático;
- el repo versiona `codex/rules/release-diaria-github.rules` como soporte
  operativo de permisos mínimos;
- deja siempre inbox item `released`, `skipped`, `blocked` o `failed`;
- la cadencia se fija a las `20:00` en la zona horaria local del usuario.

## Flujo operativo directo

1. Verificar worktree limpio, rama `main`, secretos y sesión `gh`.
1. Ejecutar `git fetch --tags origin` y `git pull --ff-only origin main`.
1. Resolver la última tag `v0.*` mergeada en `HEAD`.
1. Si no hay commits nuevos desde esa tag:
   - `skip`;
   - si la última tag no tiene GitHub Release asociada, `block`.
1. Calcular la siguiente versión:
   - subir `x` si hay al menos un commit `feat(...)`;
   - también subir `x` si hay cambio de código en `src/` sin tipado convencional claro;
   - en otro caso subir `y`.
1. Tomar el contenido de `[Unreleased]` en `CHANGELOG.md`.
1. Si `[Unreleased]` no tiene bullets útiles, sintetizar notas en castellano a partir de los commits del rango.
1. Ejecutar check bloqueante:

```powershell
$env:PYTHONPATH = "src"
pipenv run python -m unittest discover -s tests -p "test_*.py"
```

1. Calcular `BuildNumber = git rev-list --count HEAD + 1`.
1. Generar el `.apk` directamente desde la automatización:
   - resolver `FIRESTORE_PROJECT_ID`;
   - leer `.secrets/firestore-mobile-rw.json`;
   - crear temporalmente `src/frosthaven_campaign_journal/config/_mobile_runtime_secrets.py`;
   - ejecutar `pipenv run flet build apk . --yes --no-rich-output --skip-flutter-doctor -o build/apk --build-version <version-sin-v> --build-number <build-number>`;
   - localizar el `.apk`;
   - borrar siempre el archivo temporal en cleanup.
1. Si la publicación es viable:
   - actualizar `CHANGELOG.md` con la nueva sección versionada;
   - hacer commit `chore(release): cortar release v0.x.y`;
   - crear tag anotada `v0.x.y`;
   - empujar branch + tag con `git push --atomic`;
   - crear GitHub Release con el cuerpo del changelog y recordatorio post-release de rotación de clave móvil.

## Política de notas y versionado

- `CHANGELOG.md` es la fuente de verdad para el cuerpo de la release.
- La GitHub Release reutiliza la sección recién cortada y añade una nota final de operación post-release.
- La comparativa `[Unreleased]` pasa a apuntar desde la nueva tag hasta `HEAD`.

## Seguridad operativa

- Si el repo está sucio o falta un prerrequisito, la release se omite.
- Si existe estado parcial publicado o la tag/release objetivo ya existe, el flujo se bloquea y no intenta rehacer historia.
- El flujo directo debe limpiar siempre `_mobile_runtime_secrets.py` aunque falle el build.

## Fallback manual documentado

Ruta oficial: `scripts/create-github-release.ps1`

Uso previsto:

- validación manual en `dry_run`;
- build manual `-BuildOnly` cuando se necesita generar el `.apk` con secretos
  embebidos sin publicar release;
- comparación de comportamiento si falla la automatización directa;
- ejecución manual puntual fuera de la automatización programada.

El script permanece como respaldo operativo, pero no es el camino automático principal.

## Referencias

- `docs/repo-workflow.md`
- `docs/android-release-flow.md`
- `codex/rules/release-diaria-github.rules`
- `scripts/create-github-release.ps1`
