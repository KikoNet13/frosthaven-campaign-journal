# UI Main Shell Architecture (mvs)

## 1) Resumen de decisiones

- Se mantiene la estructura de tres capas: `MODEL`, `STATE`, `VIEW`.
- El runtime de Flet se ejecuta en modo declarativo con `page.render(...)`.
- `STATE` se modela como `@ft.observable` y expone handlers directos para la vista.
- Se elimina el wrapper de acciones (`MainShellViewActions`) para reducir complejidad.
- `VIEW` consume estado observable y mantiene render declarativo sin `update` manual.
- `STATE` no recibe `ft.Page`; el root solo instancia el estado y renderiza la vista.

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
| `model.py` | MODEL | Define contrato de datos para render (`view data`). | `MainShellViewData` | N/A | N/A |
| `state.py` | STATE | Define estado observable del shell y handlers de interacción. | N/A | `MainScreenReadState`, `EntryPanelReadState`, `MainShellState` | N/A |
| `view.py` | VIEW | Render Flet declarativo; consume estado y dispara handlers del estado. | N/A | N/A | `build_main_shell_view` y funciones privadas auxiliares |

## 4) Flujo de eventos

1. Interacción UI en `view.py` (botones, selección de week/entry, recursos).
2. La UI invoca un método handler de `MainShellState`.
3. `MainShellState` muta estado local (`local_state`, `read_state`, `entry_panel_state`).
4. Cuando la mutación es anidada, `MainShellState` ejecuta `notify()` para forzar rerender.
5. `build_app_root(page)` (componente con `use_state(observable)`) instancia el estado una vez y renderiza en modo declarativo.
6. `view.py` reconstruye el render desde `MainShellViewData` generado por el estado.

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
- `MainShellViewActions` (wrapper de callbacks ya no necesario)

## 6) Regla de runtime declarativo en Flet

1. El entrypoint monta la UI con `page.render(build_app_root, page)`.
2. `build_app_root` es un componente con `@ft.component`.
3. El estado de pantalla se construye con `ft.use_state(MainShellState.create(...))`.
4. No se usa `page.update()` ni `control.update()` en la capa `ui/`.

## 7) Convención declarativa ligera (proyecto)

1. `model.py`: `dataclass` de datos de vista o datos de dominio reutilizables.
2. `state.py`: `@ft.observable` + handlers de UI + orquestación de pantalla.
3. `view.py`: render puro y binding directo a handlers del estado (sin lambdas de interacción).
4. Si una mutación no reasigna campos observables (mutación anidada), usar `state.notify()`.
5. Evitar clases intermedias de callbacks salvo necesidad real de desacople.
6. Mantener archivos pequeños: si `state.py` o `view.py` crece demasiado, extraer helpers por sección sin romper API pública del feature.
