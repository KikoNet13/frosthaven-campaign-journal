# UI Main Shell Architecture (mvs)

## 1) Resumen de decisiones

- Se reemplazó la arquitectura previa por una estructura estricta de tres capas: `MODEL`, `STATE`, `VIEW`.
- `MODEL` concentra contratos de datos y callbacks de interacción para la pantalla.
- `STATE` concentra estado de pantalla, transiciones y handlers invocados por la vista.
- `VIEW` concentra render declarativo de Flet y delega todas las acciones al `STATE`.
- `build_app_root(page)` ahora instancia `MainShellState` y monta `build_main_shell_view`.

## 2) Árbol final de archivos de `ui/features/main_shell`

```text
src/frosthaven_campaign_journal/ui/features/main_shell/
├── __init__.py
├── model.py
├── state.py
└── view.py
```

## 3) Tabla por archivo

| Archivo | Tipo | Responsabilidad | Modelos que define | Estado que define | Vistas que define |
|---|---|---|---|---|---|
| `__init__.py` | Integración | Reexporta API pública del feature. | N/A | N/A | N/A |
| `model.py` | MODEL | Define contratos de datos y callbacks de UI. | `MainShellViewData`, `MainShellViewActions` | N/A | N/A |
| `state.py` | STATE | Define estado de shell, handlers y construcción de data/actions para la vista. | N/A | `MainScreenReadState`, `EntryPanelReadState`, `MainShellState` | N/A |
| `view.py` | VIEW | Render Flet declarativo; consume `MainShellViewData` y dispara acciones. | N/A | N/A | `build_main_shell_view` y funciones privadas auxiliares |

## 4) Flujo de eventos

1. Interacción UI en `view.py` (ejemplo: botón `←`, `→`, selección de week, selección de entry).
2. La UI invoca un callback de `MainShellViewActions`.
3. El callback ejecuta un método handler en `MainShellState`.
4. `MainShellState` actualiza sus subestados (`local_state`, `read_state`, `entry_panel_state`).
5. `MainShellState` reconstruye `MainShellViewData`.
6. `build_main_shell_view(data, actions)` se vuelve a renderizar.

## 5) Elementos eliminados explícitamente

- `contracts.py`
- `dispatcher.py`
- `effects.py`
- `reducer.py`
- `intents.py`
- `selectors.py`
- `dialogs.py`
- `screen.py`
- carpeta `components/` completa (`shared.py`, `temporal.py`, `status.py`, `focus.py`, `__init__.py`)
- `ui/app_root_controller.py`
