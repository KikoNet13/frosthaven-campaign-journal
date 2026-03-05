# Flujo de Release Android (Manual)

## Metadatos

- `doc_id`: DOC-ANDROID-RELEASE-FLOW
- `purpose`: Definir el flujo operativo manual para generar y publicar `.apk` en GitHub Releases.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-19

## Objetivo

Establecer un flujo reproducible para:

1. Generar un `.apk` local con `flet build apk`.
1. Verificar artefacto y hash.
1. Adjuntar el `.apk` en una release de GitHub de forma manual.

## Alcance

Incluye:

- Build Android local para distribución directa por `.apk`.
- Convención de assets para icono y splash.
- Evidencia mínima de build para cierre de issue.

No incluye:

- Publicación en Google Play.
- Automatización CI para adjunto de `.apk`.
- Gestión de secretos de firma en GitHub Actions.

## Prerrequisitos

- Python `3.12` con `pipenv`.
- Dependencias del proyecto instaladas (`pipenv install`).
- Android toolchain operativo en la máquina local.
- Flet CLI con versión compatible de Flutter para el build.

## Convención de assets del build

Ubicación oficial: `src/assets/`

- `icon.png`
- `icon_android.png`
- `splash.png`
- `splash_android.png`

## Prompts para generar assets en ChatGPT

### Prompt 1 — `icon.png`

```text
Genera una imagen PNG de 1024x1024 con fondo transparente para icono de app móvil.
Estilo: fantasy táctico limpio, inspirado en diario de campaña (sin copiar logos existentes).
Elemento central: emblema abstracto tipo escudo/runa de hielo + trazo de pergamino.
Paleta obligatoria: #1D3557, #457B9D, #A8DADC, #E63946, #F1FAEE.
Composición: centrada, alto contraste, legible en tamaño pequeño.
Restricciones: sin texto, sin watermark, sin borde externo, sin mockup.
Entrega: SOLO PNG transparente 1024x1024.
```

### Prompt 2 — `icon_android.png`

```text
Genera una imagen PNG de 1024x1024 con fondo transparente para foreground de icono adaptive Android.
Usa el mismo lenguaje visual del icono principal, pero con zona segura:
el motivo debe ocupar aprox. 62% del ancho/alto y quedar perfectamente centrado.
Paleta: #1D3557, #457B9D, #A8DADC, #E63946, #F1FAEE.
Restricciones: sin texto, sin watermark, sin fondo sólido, sin sombras externas grandes.
Entrega: SOLO PNG transparente 1024x1024.
```

### Prompt 3 — `splash.png`

```text
Genera una imagen PNG de 2048x2048 con fondo transparente para splash screen de app.
Diseño: versión simplificada del emblema del icono, centrado, limpia y elegante.
Uso previsto: se mostrará sobre fondo sólido oscuro #1D3557.
Paleta del emblema: #F1FAEE, #A8DADC, acento mínimo #E63946.
Restricciones: sin texto, sin watermark, sin marco, sin mockup.
Entrega: SOLO PNG transparente 2048x2048.
```

### Prompt 4 — `splash_android.png`

```text
Genera una imagen PNG de 2048x2048 con fondo transparente para splash de Android.
Versión aún más simple que splash.png: emblema compacto y muy legible en tamaños pequeños.
Composición: centrada, motivo ocupando 40-48% del lienzo.
Paleta: #F1FAEE y #A8DADC, acento opcional #E63946 muy sutil.
Restricciones: sin texto, sin watermark, sin efectos complejos, sin fondo.
Entrega: SOLO PNG transparente 2048x2048.
```

## Comando de build APK (manual)

```powershell
$env:FLET_CLI_NO_RICH_OUTPUT="1"
pipenv run flet build apk . --yes --no-rich-output --skip-flutter-doctor -o build/apk --build-version 0.1.1 --build-number 1
```

Nota: ejecutar desde `.` permite aplicar `pyproject.toml` del repo (nombre de
artefacto, metadata y configuración `tool.flet.*`).

## Verificación de artefacto

```powershell
Get-ChildItem build/apk -File
Get-FileHash build/apk/frosthaven_campaign_journal.apk -Algorithm SHA256
```

Si el nombre final cambia por plataforma/ABI, usar el archivo `.apk` realmente generado.

## Adjunto manual en release de GitHub

```powershell
gh release upload <tag> build/apk/frosthaven_campaign_journal.apk --clobber
```

## Evidencia mínima para cierre de issue

- Comando de build usado.
- Resultado de build (`ok` o error trazado).
- Ruta del `.apk` generado.
- Hash SHA256 del artefacto.

## Referencias

- `docs/repo-workflow.md`
- `pyproject.toml`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/105`
