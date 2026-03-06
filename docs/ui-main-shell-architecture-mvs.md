# UI Main Shell Architecture (MVS)

## 1) Resumen de decisiones

- Se mantiene estructura MVS con estado observable único en `MainShellState`.
- El runtime sigue siendo declarativo con `page.render(build_app_root, page)`.
- Los formularios de `entry`, notas y sesión continúan inline en el panel central.
- Los mensajes informativos pasan a `SnackBar` flotante.
- Las preguntas de confirmación pasan a `AlertDialog` modal.
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
| `ui/app_root.py` | Root bridge | Observa `toast_state` y `confirmation_state`, y abre/cierra `SnackBar` y `AlertDialog`. |
| `ui/main_shell/model.py` | MODEL | Contratos de render declarativos del panel principal. |
| `ui/main_shell/state/` | STATE | Estado observable, handlers de UI, lecturas y escrituras. |
| `ui/main_shell/view/` | VIEW | Render puro del shell y binding directo a handlers del estado. |

## 4) Flujo declarativo actual

1. El root crea estado con `ft.use_state(MainShellState.create)`.
1. La vista llama `state.build_view_data()` y renderiza solo contenido inline.
1. Los handlers `on_*` mutan `local_state`, `read_state`, `entry_panel_state` y estado transitorio de UI.
1. `toast_state` y `confirmation_state` emiten `event_id` nuevos en cada evento.
1. `app_root.py` detecta esos `event_id` con `ft.use_effect` + `ft.use_ref` y abre el overlay correspondiente.
1. El estado sigue siendo la fuente de verdad; el root solo traduce eventos a overlays de Flet.

## 5) Estado declarativo de UI

### Inline

- `EntryFormViewState`
- `EntryNotesEditorViewState`
- `SessionFormViewState`

### Overlays transitorios

- `ToastState(message, event_id)`
- `ConfirmationState(..., event_id)`

El `event_id` evita que dos emisiones sucesivas con el mismo texto o payload se pierdan.

## 6) Overlays del root

- `SnackBar`
  - `behavior=FLOATING`
  - auto-dismiss
  - icono de cierre
  - margen inferior suficiente para no solapar bottom bar ni FAB
- `AlertDialog`
  - `modal=True`
  - usa `title`, `body` y `confirm_label` ya definidos en estado
  - botón de confirmar con la paleta del FAB
  - botón de cancelar outlined con la misma paleta

## 7) Guardrails de arquitectura

1. Runtime declarativo obligatorio (`page.render` + `@ft.component` en root).
1. Estado observable único de pantalla (`MainShellState`).
1. Ningún mixin de estado conoce `Page` ni abre overlays directamente.
1. Los banners inline se reservan para `warning` y `error`.
1. Las confirmaciones y mensajes informativos transitorios se resuelven en el root.