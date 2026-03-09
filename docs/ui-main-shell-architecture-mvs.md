# UI Main Shell Architecture (MVS)

## 1) Resumen de decisiones

- Se mantiene estructura MVS con estado observable único en `MainShellState`.
- El runtime sigue siendo declarativo con `page.render(build_app_root, page)`.
- Los formularios de `entry`, notas, sesión y confirmaciones comparten un shell modal declarativo desde el root.
- Los mensajes informativos pasan a `SnackBar` flotante.
- El bridge a overlays vive solo en `ui/app_root.py`; el estado no se acopla a `Page`.
- No se usa `page.update()` ni `control.update()` en la capa `ui`.

## 2) Árbol actual del feature

```text
src/frosthaven_campaign_journal/ui/
├── app_root.py
└── main_shell/
    ├── __init__.py
    ├── model.py
    ├── state/
    └── view/
```

## 3) Tabla por archivo

| Archivo | Tipo | Responsabilidad |
| --- | --- | --- |
| `ui/app_root.py` | Root bridge | Observa `toast_state`, construye `view_data` y monta `SnackBar` + shell modal compartido sobre la shell principal. |
| `ui/main_shell/model.py` | MODEL | Contratos de render declarativos del panel principal. |
| `ui/main_shell/state/` | STATE | Estado observable, handlers de UI, lecturas y escrituras. |
| `ui/main_shell/view/` | VIEW | Render puro del shell y binding directo a handlers del estado. |

## 4) Flujo declarativo actual

1. El root crea estado con `ft.use_state(MainShellState.create)`.
1. El root construye `view_data`, renderiza la shell principal y monta encima el modal activo si existe.
1. Los handlers `on_*` mutan `local_state`, `read_state`, `entry_panel_state` y estado transitorio de UI.
1. `toast_state` y `confirmation_state` emiten `event_id` nuevos en cada evento.
1. `app_root.py` usa `ft.use_effect` solo para `SnackBar`; confirmaciones y formularios se traducen a `view_data` y se renderizan de forma declarativa en el shell modal compartido.
1. El estado sigue siendo la fuente de verdad; el root solo traduce eventos a overlays de Flet cuando el framework lo exige (`SnackBar`).

## 5) Estado declarativo de UI

### Modales declarativos

- `ConfirmationDialogViewState`
- `EntryFormViewState`
- `EntryNotesEditorViewState`
- `SessionFormViewState`

### Overlays transitorios

- `ToastState(message, event_id)`
- `ConfirmationState(..., event_id)` como fuente de verdad para producir `ConfirmationDialogViewState`

El `event_id` evita que dos emisiones sucesivas con el mismo texto o payload se pierdan.

## 6) Overlays del root

- `SnackBar`
  - `behavior=FLOATING`
  - auto-dismiss
  - icono de cierre
  - margen inferior suficiente para no solapar bottom bar ni FAB
- Shell modal compartido
  - scrim + panel centrado renderizados desde `ui/app_root.py`
  - un único diálogo visible a la vez con prioridad: confirmación -> entry -> notas -> sesión
  - sin botón `X`; cierre explícito por acciones
  - botones outlined/filled compartidos y alineados abajo a la derecha
  - título opcional: presente en confirmaciones/entry/sesión y omitido en notas

## 7) Guardrails de arquitectura

1. Runtime declarativo obligatorio (`page.render` + `@ft.component` en root).
1. Estado observable único de pantalla (`MainShellState`).
1. Ningún mixin de estado conoce `Page` ni abre overlays directamente.
1. Los banners inline se reservan para `warning` y `error`.
1. Los formularios persistentes no se renderizan dentro del visor semanal.
1. Las confirmaciones y formularios comparten el mismo shell modal declarativo en el root.
1. Los mensajes informativos transitorios se resuelven en el root mediante `SnackBar`.
