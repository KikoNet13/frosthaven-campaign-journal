# UI Main Shell Architecture (MVS)

## 1) Resumen de decisiones

- Se mantiene estructura de tres capas: `model.py`, `state.py`, `view.py`.
- El runtime sigue siendo declarativo: `page.render(build_app_root, page)`.
- `MainShellState` es `@ft.observable` y concentra orquestaciÃ³n de lecturas,
  escrituras y estado local de UI.
- `build_main_shell_view` es helper puro de render (sin `@ft.component`).
- No se usa `page.update()` ni `control.update()` en `src/.../ui`.
- Se recupera paridad funcional pre-`#94` sin reintroducir capas `MVU+effects`
  eliminadas (`dispatcher/reducer/effects/intents/selectors`).

## 2) Ãrbol actual del feature

```text
src/frosthaven_campaign_journal/ui/features/main_shell/
â”œâ”€â”€ __init__.py
â”œâ”€â”€ model.py
â”œâ”€â”€ state.py
â””â”€â”€ view.py
```

## 3) Tabla por archivo

| Archivo | Tipo | Responsabilidad |
| --- | --- | --- |
| `model.py` | MODEL | Contratos de datos de render (`MainShellViewData` + estados declarativos de confirmaciÃ³n/formularios). |
| `state.py` | STATE | Estado observable y handlers de UI + wiring real Firestore (`Q1..Q8` + writes). |
| `view.py` | VIEW | ComposiciÃ³n visual y binding directo a handlers del estado. |
| `__init__.py` | IntegraciÃ³n | API pÃºblica estable del feature. |

## 4) Flujo declarativo

1. El root crea estado con `ft.use_state(MainShellState.create)`.
1. La vista llama `data = state.build_view_data()`.
1. Controles invocan handlers del estado (`on_*`).
1. El estado muta `local_state`, `read_state`, `entry_panel_state` y UI-state
   declarativo (confirmaciones, formularios, editor de notas).
1. El estado dispara `notify()` y la vista se reconstruye.

## 5) Estado declarativo de UI en `model.py`

- `ConfirmationViewState`
- `EntryFormViewState`
- `SessionFormViewState`

Estos contratos permiten reemplazar modales imperativos por ediciÃ³n/confirmaciÃ³n
declarativa renderizada en el panel central.

## 6) Cobertura funcional recuperada en `state.py`

- Lecturas: `load_main_screen_snapshot`, `read_q5_entries_for_selected_week`,
  `read_entry_by_ref`, `read_q8_sessions_for_entry`.
- Writes:
  - campaÃ±a: `extend_years_plus_one`
  - week: `close_week`, `reopen_week`, `reclose_week`
  - session: `start_session`, `stop_session`, `manual_create_session`,
    `manual_update_session`, `manual_delete_session`
  - entry: `create_entry`, `update_entry`, `delete_entry`,
    `reorder_entry_within_week`
  - resources: `replace_entry_resource_deltas`
- Reglas de consistencia:
  - visor sticky separado de navegaciÃ³n temporal
  - protecciÃ³n de borrador sucio antes de cambios de contexto
  - refresh selectivo Q5/Q8 tras operaciones
  - flags `*_write_pending` + errores por dominio

## 7) Guardrails de arquitectura

1. Runtime declarativo obligatorio (`page.render` + `@ft.component` en root).
1. Estado observable Ãºnico de pantalla (`MainShellState`).
1. Binding directo desde vista a handlers del estado.
1. No usar `page.update()` ni `control.update()` en capa `ui`.



