# Changelog

Todos los cambios relevantes del proyecto se documentan en este archivo.

El formato sigue
[Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y usa versionado
[SemVer](https://semver.org/lang/es/).

## [Unreleased]

### Añadido

- Tests unitarios de `MainShellState` para `ToastState`, `event_id` de
  confirmación y limpieza de estado tras cancelar/confirmar.

### Cambiado

- `main_shell` mueve los mensajes informativos a `SnackBar` flotante y las
  confirmaciones a `AlertDialog` modal con botones alineados visualmente al FAB.
- `app_root.py` pasa a puentear overlays de Flet desde estado transitorio,
  mientras el panel central mantiene solo banners de error/advertencia y
  formularios inline.

## [0.2.1] - 2026-03-05

### Añadido

- Script operativo `scripts/build-android-with-mobile-secrets.ps1` para
  generar APK Android con secretos móviles embebidos desde `.secrets/`.
- Contrato interno de secretos móviles generados en
  `src/frosthaven_campaign_journal/config/_mobile_runtime_secrets.py`
  (archivo no versionado).
- Registro de decisión `DEC-0051` sobre conectividad Firestore en Android.

### Cambiado

- `load_settings()` ahora mantiene precedencia de entorno/`.env` y aplica
  fallback de secretos embebidos solo cuando faltan
  `FIRESTORE_PROJECT_ID` o `GOOGLE_APPLICATION_CREDENTIALS`.
- `firestore_client.py` actualiza mensajes de error para contemplar también
  secretos móviles embebidos.
- `docs/android-release-flow.md` incorpora build con secretos embebidos,
  advertencia de riesgo y rotación obligatoria de clave tras release pública.

## [0.2.0] - 2026-03-05

### AÃ±adido

- Flujo operativo manual de releases Android en `docs/android-release-flow.md`
  (Issue #105).
- Contrato de empaquetado Flet en `pyproject.toml` para build Android.
- ConvenciÃ³n de assets de app para build en `src/assets/` (`icon*` y
  `splash*`).
- Reglas explÃ­citas de colaboraciÃ³n Kiko-Codex en `AGENTS.md`.
- Estrategia de divisiÃ³n de tareas mÃºltiples en `docs/context-checklists.md`.
- Cierre de alcance MVP v1 documentado en `tdd.md` (Issue #5).
- Regla de aviso para activar `Plan Mode` antes de decisiones interactivas.
- Modelo de dominio unificado `Entry` y glosario oficial en
  `docs/domain-glossary.md` (Issue #6).

### Cambiado

- Estrategia de `.apk` en releases actualizada a flujo manual operativo con
  referencia oficial en `docs/repo-workflow.md`.
- `docs/system-map.md` incorpora `docs/android-release-flow.md` como documento
  oficial de implementaciÃ³n.
- Recuperada la paridad funcional pre-`#94` en `main_shell` manteniendo
  arquitectura declarativa MVS.
- `MainShellState` vuelve a integrar wiring real de Firestore para
  `Q1..Q8` y writes de campaÃ±a/week/session/entry/resources.
- `MainShellViewData` amplÃ­a contrato con estado declarativo de
  confirmaciones, formularios de sesiÃ³n/entry y editor de notas de week.
- `view.py` recupera panel central operativo (modo vacÃ­o/week/entry,
  acciones de entry, sesiones, recursos y ediciÃ³n inline declarativa).
- Actualizada trazabilidad tÃ©cnica con `DEC-0041` y ajustes en
  `docs/ui-main-shell-architecture-mvs.md`, checklist y bloques MVP.
- Shell principal de UI migrado a runtime declarativo de Flet:
  `page.render(build_app_root, page)` en el entrypoint y root con
  `@ft.component`.
- Eliminado el patrÃ³n hÃ­brido imperativo en `src/frosthaven_campaign_journal/ui/`:
  sin `page.update()` ni `control.update()` en la capa UI.
- Corregido el error de render web de `Pagelet` ("height is unbounded")
  ajustando el `Page` raÃ­z para no usar `scroll` global.
- `build_main_shell_view` pasa a helper de vista puro (sin `@ft.component`)
  para evitar errores de composiciÃ³n en `Container.content`.
- Restaurado el diseÃ±o visual del `main_shell` al estilo previo:
  barra temporal superior con bloques de week, tabs de entry centradas y
  panel central limpio en gris.
- Flujo operativo detallado para trabajo con agente en
  `docs/repo-workflow.md`.
- Nota formal sobre estrategia de `.apk` y releases.
- Registro de decisiÃ³n DEC-0011 en `docs/decision-log.md`.
- Reglas de colaboraciÃ³n reforzadas en `AGENTS.md` y
  `docs/repo-workflow.md`.
- `tdd.md` actualiza el bloque de dominio/Firestore de pendiente a cerrado
  segÃºn la Issue #6.
- `docs/system-map.md` incorpora `docs/domain-glossary.md` como fuente
  oficial.

## [0.1.0] - 2026-02-20

### Bootstrap inicial

- Estructura base de contexto (`AGENTS.md`, `docs/`, `learning/`).
- Flujo GitHub Flow minimalista y convenciÃ³n de commits.
- `README.md`, `CONTRIBUTING.md` y plantillas de Issues y PR.
- Base de versionado con `CHANGELOG.md`.
- NormalizaciÃ³n UTF-8 en documentos Markdown.
- Archivo `LICENSE` con licencia MIT.

[Unreleased]:
  https://github.com/KikoNet13/frosthaven-campaign-journal/compare/v0.2.1...HEAD
[0.2.1]:
  https://github.com/KikoNet13/frosthaven-campaign-journal/releases/tag/v0.2.1
[0.2.0]:
  https://github.com/KikoNet13/frosthaven-campaign-journal/releases/tag/v0.2.0
[0.1.0]:
  https://github.com/KikoNet13/frosthaven-campaign-journal/releases/tag/v0.1.0

