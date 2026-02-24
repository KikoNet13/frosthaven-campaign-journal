# Flujo de Sesión Activa y Reglas de Auto-Stop (MVP)

## Metadatos

- `doc_id`: DOC-ACTIVE-SESSION-FLOW
- `purpose`: Definir el flujo funcional de sesión activa (`start/stop/auto-stop`) del MVP, incluyendo cambio de foco, errores y recuperación esperada del cliente.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar el flujo documental de sesión activa del MVP para que la implementación
pueda aplicar reglas consistentes de `start`, `stop` y `auto-stop` sin romper la
invariante `0..1` sesión activa global y sin confundir `current week`, foco y
estado activo.

## Alcance y no alcance

Incluye:

- flujo normal de `Session.start`, `Session.stop` y `Session.auto_stop`;
- separación entre `current week` (marcador), selección (`Week`/`Entry`) y
  `Entry` activa;
- interacción observable con `Week.close`, `Week.reclose` y `Entry.delete`
  cuando hay sesión activa;
- clasificación de errores (`conflicto`, `transicion_invalida`, `validacion`) y
  recuperación esperada del cliente;
- alineación con `#12`, `#37`, `#18` y el glosario.

No incluye:

- técnica Firestore (transacciones, batch, estrategia de atomicidad técnica);
- consultas/lecturas e índices (`#16`);
- diseño visual final (layout, copy, estilos, toasts vs inline);
- reespecificación del CRUD manual completo de `Session` (`Session.manual_*`);
- código de app.

## Entradas y prerrequisitos

- `docs/domain-glossary.md`
- `docs/conflict-policy.md` (Issue `#8`)
- `docs/campaign-temporal-controls.md` (Issue `#9`)
- `docs/campaign-temporal-initialization.md` (Issue `#13`)
- `docs/firestore-operation-contract.md` (Issue `#12`)
- `docs/editability-policy.md` (Issue `#37`)
- `docs/timestamp-order-policy.md` (Issue `#18`)
- `docs/minimal-read-queries.md` (Issue `#16`)
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`

## Términos de UI/flujo (`current week`, selección, activo)

1. `current week`:
   - marcador visual del estado temporal derivado de `campaign.week_cursor`;
   - no equivale a selección/foco.
1. `selected_week`:
   - `Week` elegida por el usuario para navegar/editar.
1. `selected_entry`:
   - única `Entry` visible/activa en el panel de edición para acciones de
     sesión en el flujo normal del MVP.
1. `active_entry`:
   - `Entry` que posee la sesión activa global (si existe), derivado de una
     `Session` con `ended_at_utc = null`.
1. Los controles `Iniciar/Parar sesión` viven en el bloque de la
   `selected_entry` (junto a total jugado y lista de sesiones desplegable).
1. Cambiar `selected_week` o `selected_entry` no implica por sí mismo cambiar
   `current week` ni cerrar la sesión activa global.

## Modelo de estado del flujo de sesión (cliente)

### Tabla 1 — Estados de flujo (`I14-S1`)

| `flow_state_id` | `descripcion` | `session_active_global` | `selected_week` | `selected_entry` | `current_week_marker` | `acciones_disponibles` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `no_active_selected_entry` | Hay `selected_entry` y no existe sesión activa global | No | Sí | Sí | Sí | `start`, edición de `Entry`, acciones de `Week` | Estado normal sin sesión activa |
| `active_on_selected_entry` | Existe sesión activa global y pertenece a la `selected_entry` | Sí | Sí | Sí | Sí | `stop`, edición, acciones de `Week`/`Entry` | `start` sobre la misma `Entry` sería inválido |
| `active_on_other_entry` | Existe sesión activa global pero la `selected_entry` es otra | Sí | Sí | Sí | Sí | `start` (con `auto-stop`), edición, navegación/foco | La UI debe mostrar diferencia entre foco y activo |
| `pending_session_action` | Acción de sesión en curso (cliente esperando resultado) | 0..1 (pendiente) | Sí | Sí | Sí | bloquear reenvío de la misma acción | Estado transitorio de cliente; no reescribe el contrato de `#12` |
| `error_local` | Error funcional local (`transicion_invalida` / `validacion`) tras acción | 0..1 | Sí | Sí | Sí | corregir acción y reintentar | No requiere `refresh` por defecto |
| `error_conflicto_pending_refresh` | Error de conflicto concurrente detectado | 0..1 desconocido hasta refrescar | Sí | Sí | Sí | `refresh` manual y luego reintento | Alineado con `on-demand refresh` |

## Tabla de transiciones y eventos

### Tabla 2 — Eventos y transiciones (`I14-S1` / `I14-S2`)

| `event_id` | `precondiciones` | `estado_origen_relevante` | `comportamiento_cliente` | `operacion_contractual_relacionada` | `postcondicion_visible` | `errores_posibles` | `recuperacion` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ui.session_start_on_selected_entry` | Existe `selected_entry`; botón `Iniciar` visible en su bloque | `no_active_selected_entry`, `active_on_other_entry` | Ejecuta `start`; si había otra activa, el flujo observable incluye `auto-stop + start`; sin confirmación extra por `auto-stop` | `Session.start` (+ `Session.auto_stop` si aplica) | Sesión activa global pasa a la `selected_entry`; UI muestra estado activo en esa entry | `conflicto`, `validacion`, `transicion_invalida` (si la entry ya era activa por estado obsoleto) | `conflicto`: `refresh` manual + reintentar; otros: error local |
| `ui.session_stop_on_selected_entry` | Existe `selected_entry` con sesión activa global | `active_on_selected_entry` | Ejecuta `stop` desde la `selected_entry` visible | `Session.stop` | Desaparece el estado activo global; la `selected_entry` queda sin sesión activa | `conflicto`, `transicion_invalida` | `conflicto`: `refresh` manual + reintentar; `transicion_invalida`: error local |
| `ui.select_week` | El usuario selecciona una `Week` para navegar/editar | Cualquiera | Cambia `selected_week`; no hace `auto-stop`; puede requerir nueva selección de `Entry` para accionar sesión | No aplica (navegación/foco) | Cambia el foco temporal/edición; la sesión activa global (si existe) sigue corriendo | Ninguno de sesión; potenciales errores de lectura fuera de alcance | No aplica a `#14` |
| `ui.select_entry` | Existe `Entry` seleccionable en la `selected_week` | Cualquiera con `selected_week` | Cambia `selected_entry`; no hace `auto-stop`; habilita/actualiza bloque de sesión para esa entry | No aplica (selección/foco) | La entry visible cambia; el estado activo puede pertenecer a otra entry | Ninguno de sesión; potenciales errores de lectura fuera de alcance | No aplica a `#14` |
| `ui.week_close` | El usuario dispara cierre de `Week`; puede haber sesión activa en esa week | Cualquiera | Ejecuta acción de cierre de week; si hay sesión activa en la week, el `auto-stop` va embebido sin confirmación extra | `Week.close` (+ `Session.auto_stop` si aplica) | Week queda `closed`; si la sesión activa pertenecía a esa week, deja de estar activa; `current week` se actualiza por `week_cursor` derivado | `conflicto`, `validacion`, `transicion_invalida` | `conflicto`: `refresh` manual + reintentar; otros: error local |
| `ui.week_reclose` | El usuario dispara recierre manual `open -> closed` | Cualquiera | Igual patrón observable que `ui.week_close` para sesión activa + cursor | `Week.reclose` (+ `Session.auto_stop` si aplica) | Week `closed`, sesión de esa week cerrada si existía, marcador `current week` actualizado | `conflicto`, `validacion`, `transicion_invalida` | `conflicto`: `refresh` manual + reintentar; otros: error local |
| `ui.entry_delete_selected` | Existe `selected_entry`; puede ser la activa | `active_on_selected_entry`, `no_active_selected_entry` | Ejecuta borrado; si era activa, `auto-stop` ocurre como side-effect de la operación compuesta | `Entry.delete` (+ `Session.auto_stop` si aplica) | Si era activa, el estado activo global queda vacío; la entry desaparece | `conflicto`, `transicion_invalida` | `conflicto`: `refresh` manual + reintentar; `transicion_invalida`: error local |
| `system.auto_stop_due_start_switch` | Existe sesión activa previa y `Session.start` sobre otra `Entry` | `active_on_other_entry` | Side-effect interno del flujo `start` | `Session.auto_stop` dentro de `Session.start` | La sesión previa se cierra y la nueva pasa a activa | `conflicto`, `transicion_invalida` (heredados del padre) | Heredada de `ui.session_start_on_selected_entry` |
| `system.auto_stop_due_week_close` | Cierre/recierre de week afecta a una week con sesión activa | Cualquiera | Side-effect interno del cierre/recierre | `Session.auto_stop` dentro de `Week.close`/`Week.reclose` | La sesión activa de esa week queda cerrada antes de cerrar la week | `conflicto`, `transicion_invalida` (heredados del padre) | Heredada de `ui.week_close` / `ui.week_reclose` |
| `system.auto_stop_due_entry_delete` | Borrado de `Entry` activa | `active_on_selected_entry` | Side-effect interno de borrado | `Session.auto_stop` dentro de `Entry.delete` | La sesión activa asociada deja de estar activa antes del borrado | `conflicto`, `transicion_invalida` (heredados del padre) | Heredada de `ui.entry_delete_selected` |

## Reglas operativas por evento

### `ui.session_start_on_selected_entry`

1. La acción solo existe en el bloque de la `selected_entry` visible.
1. Si no hay `selected_entry`, no hay acción de `start` disponible en el flujo
   normal (no existe `Play` global para suplirla).
1. Si la `selected_entry` ya es la `active_entry`, la acción se trata como
   `transicion_invalida` (error local, sin crear sesión nueva).
1. Si existe otra `active_entry`, el flujo observable es `auto-stop + start`.
1. El `auto-stop` embebido no pide confirmación extra.

### `ui.session_stop_on_selected_entry`

1. La acción solo existe cuando la `selected_entry` es la `active_entry`.
1. Si la sesión ya no está activa al aplicar el `stop`, se clasifica como
   `transicion_invalida`.
1. La recuperación por defecto ante `transicion_invalida` es error local (sin
   `refresh` automático).

### `ui.select_week` y `ui.select_entry`

1. Son eventos de navegación/foco, no operaciones de sesión.
1. No ejecutan `auto-stop`.
1. No requieren confirmación adicional por existir sesión activa global.
1. Deben preservar la visibilidad conceptual de:
   - `current week`;
   - `selected_week` / `selected_entry`;
   - `active_entry` (si existe).

### `ui.week_close` y `ui.week_reclose`

1. `#14` reutiliza el contrato de `#12`:
   - `auto-stop` (si aplica) + cierre/recierre + recálculo de `week_cursor` como
     unidad lógica observable.
1. Si la acción padre ya tiene confirmación, esa confirmación cubre todo el
   flujo (incluido el `auto-stop` embebido).
1. `#14` no redefine validaciones de backend (`0` weeks abiertas, conflicto de
   base, etc.); solo documenta el resultado visible y recuperación del cliente.

### `ui.entry_delete_selected`

1. `#14` no redefine cascada ni atomicidad de borrado (`#12`).
1. Sí documenta el efecto observable cuando la `Entry` borrada era la activa:
   - el estado activo global queda vacío por `auto-stop` embebido.
1. La política exacta de selección/foco posterior al borrado queda fuera de
   alcance de esta issue.

## Cambio de foco y separación foco/activo

1. La UI debe poder mostrar simultáneamente:
   - `current week` (marcador derivado de `week_cursor`);
   - `selected_week` / `selected_entry` (contexto de edición);
   - `active_entry` (estado activo global).
1. Cambiar de `selected_entry` no implica trasladar automáticamente el estado
   activo ni ejecutar `stop`.
1. El usuario puede editar otra `Entry`/`Week` mientras existe una sesión activa
   global en otra `Entry`, sujeto a las reglas de `#37` y `#12`.

## Interacción con cierre/recierre de semana

1. `Week.close` y `Week.reclose` pueden dispararse aunque exista sesión activa
   en la week afectada; el `auto-stop` ocurre como side-effect.
1. Si la sesión activa está en otra week, no debe cerrarse por un cierre/recierre
   de una week distinta.
1. Tras cierre/recierre exitoso, el marcador `current week` debe reflejar el
   `week_cursor` derivado vigente (según `#37`, `#13` y `#9`).
1. La selección (`selected_week` / `selected_entry`) sigue siendo un concepto
   distinto del marcador `current week`.

## Errores y recuperación esperada (UI/cliente)

### Tabla 3 — Errores y recuperación (`I14-S2` / `I14-S3`)

| `error_case_id` | `categoria` | `trigger` | `feedback_esperado` | `accion_usuario_recomendada` | `requiere_refresh` | `notas` |
| --- | --- | --- | --- | --- | --- | --- |
| `session_start_same_active_entry` | `transicion_invalida` | `start` sobre `selected_entry` que ya es activa | Error local breve; no cambia estado | Mantener sesión actual o usar `stop` si quiere cerrarla | No | No crea nueva sesión |
| `session_stop_not_active` | `transicion_invalida` | `stop` sobre sesión ya cerrada/no activa | Error local | Corregir acción; opcionalmente refrescar si sospecha estado obsoleto | No (por defecto) | Sin auto-refresh |
| `session_start_conflict` | `conflicto` | Base obsoleta al aplicar `start` (`auto-stop + start` si aplica) | Error de conflicto concurrente | `refresh` manual y reintentar | Sí | Alineado con `on-demand refresh` |
| `session_stop_conflict` | `conflicto` | Base obsoleta al aplicar `stop` | Error de conflicto concurrente | `refresh` manual y reintentar | Sí | Sin retry automático |
| `week_close_conflict_with_active_session` | `conflicto` | Conflicto durante `Week.close` con `auto-stop` embebido | Error de conflicto de operación compuesta | `refresh` manual y reintentar cierre | Sí | Recuperación heredada de `#12` |
| `week_reclose_invalid_transition` | `transicion_invalida` | `reclose` sobre week ya `closed` o transición no aplicable | Error local | Corregir acción | No | Distinto de conflicto |
| `session_start_validation` | `validacion` | `start` con `selected_entry` inválida/no disponible por payload/estado local | Error local | Corregir selección/entrada | No | `#14` no redefine validación backend |

### Regla de recuperación por categoría

1. `conflicto`:
   - feedback de conflicto;
   - `refresh` manual + reintentar;
   - sin auto-refresh ni retry automático.
1. `transicion_invalida`:
   - error local;
   - no `refresh` por defecto.
1. `validacion`:
   - error local;
   - corregir la acción/selección antes de reintentar.

## Alineación con `#12`, `#37` y `#18`

### `#12` — Contrato por operación

1. `#14` no redefine pre/postcondiciones ni atomicidad de comportamiento.
1. `#14` traduce esas operaciones a flujo observable de cliente/UI:
   - `Session.start`
   - `Session.stop`
   - `Session.auto_stop`
   - `Week.close` / `Week.reclose`
   - `Entry.delete` (solo efecto observable de `auto-stop`)

### `#37` — Editabilidad manual e invariantes

1. `Week.status=closed` no bloquea por sí mismo la edición ni el flujo normal de
   sesión; `Session.start/stop` siguen permitidos en weeks `open|closed` según
   el contrato vigente.
1. `Session.manual_*` puede coexistir con este flujo:
   - puede crear/cerrar una sesión activa global;
   - no sustituye ni reespecifica el flujo normal `start/stop/auto-stop`.
1. Se preserva la invariante `0..1` sesión activa global.

### `#18` — Timestamps y orden estable

1. `#14` no define desempates ni orden estable.
1. Cuando el flujo requiere refrescar listas/estado de sesiones tras acciones o
   conflictos, el orden visible se rige por `docs/timestamp-order-policy.md`.

### `#16` — Consultas mínimas de pantalla principal

1. `#14` define el comportamiento observable del flujo (`start/stop/auto-stop`,
   separación foco/activo y recuperación de errores).
1. `#16` define las lecturas mínimas que soportan ese flujo en pantalla:
   - `Q6 active_session_global`;
   - `Q7 active_entry_doc_if_needed` (condicional);
   - `Q8 sessions_selected_entry_combined`.
1. El arranque sin selección (`selected_week`/`selected_entry` vacíos) y la
   carga diferida de sesiones hasta seleccionar `Entry` se documentan en `#16`.

## Casos de aceptación / verificación documental

1. `Start` sobre `selected_entry` sin sesión activa global crea sesión activa y
   la UI la muestra como activa.
1. `Start` sobre otra `selected_entry` con una sesión activa global previa
   documenta `auto-stop + start` sin confirmación extra.
1. `Start` sobre la `Entry` ya activa se clasifica como `transicion_invalida`
   con error local.
1. `Stop` sobre `selected_entry` activa cierra la sesión activa.
1. `Stop` inválido se clasifica como `transicion_invalida` con error local.
1. Cambiar foco (`select_week` / `select_entry`) no hace `auto-stop`.
1. `Week.close` con sesión activa en esa week documenta el resultado observable
   de auto-stop + cierre + actualización del marcador `current week`.
1. `Week.reclose` replica el patrón de recuperación y clasificación de errores
   del cierre normal.
1. `Entry.delete` activa documenta efecto observable de `auto-stop` sin
   reescribir cascada/atomicidad de `#12`.
1. El documento separa explícitamente `current week`, selección y `active_entry`.

## Riesgos, límites y decisiones diferidas

- El detalle visual exacto de indicadores de foco/activo y mensajes de error
  queda para diseño/UI futura.
- La política de selección/foco posterior a borrar una `Entry` queda fuera de
  alcance de `#14`.
- La técnica de sincronización/atomicidad Firestore permanece en `#12` y código.
- La matriz transversal de edge cases priorizados para concurrencia/sync se
  documenta en `docs/concurrency-sync-edge-case-matrix.md` (Issue `#17`), que
  reutiliza este flujo como fuente de expectativas y recuperación.
- El legado (`tdd.md`) puede seguir reflejando un `Play/Stop` en barra inferior;
  esta decisión oficial prevalece para el MVP actual.

## Referencias

- `AGENTS.md`
- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/firestore-operation-contract.md`
- `docs/editability-policy.md`
- `docs/timestamp-order-policy.md`
- `docs/minimal-read-queries.md`
- `docs/concurrency-sync-edge-case-matrix.md`
- `docs/decision-log.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `tdd.md` (legado temporal; puede divergir en detalles de UI)
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`
