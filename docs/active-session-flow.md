# Flujo de SesiÃ³n Activa y Reglas de Auto-Stop (MVP)

## Metadatos

- `doc_id`: DOC-ACTIVE-SESSION-FLOW
- `purpose`: Definir el flujo funcional de sesiÃ³n activa (`start/stop/auto-stop`) del MVP, incluyendo cambio de foco, errores y recuperaciÃ³n esperada del cliente.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar el flujo documental de sesiÃ³n activa del MVP para que la implementaciÃ³n
pueda aplicar reglas consistentes de `start`, `stop` y `auto-stop` sin romper la
invariante `0..1` sesiÃ³n activa global y sin confundir `current week`, foco y
estado activo.

## Alcance y no alcance

Incluye:

- flujo normal de `Session.start`, `Session.stop` y `Session.auto_stop`;
- separaciÃ³n entre `current week` (marcador), selecciÃ³n (`Week`/`Entry`) y
  `Entry` activa;
- interacciÃ³n observable con `Week.close`, `Week.reclose` y `Entry.delete`
  cuando hay sesiÃ³n activa;
- clasificaciÃ³n de errores (`conflicto`, `transicion_invalida`, `validacion`) y
  recuperaciÃ³n esperada del cliente;
- alineaciÃ³n con `#12`, `#37`, `#18` y el glosario.

No incluye:

- tÃ©cnica Firestore (transacciones, batch, estrategia de atomicidad tÃ©cnica);
- consultas/lecturas e Ã­ndices (`#16`);
- diseÃ±o visual final (layout, copy, estilos, toasts vs inline);
- reespecificaciÃ³n del CRUD manual completo de `Session` (`Session.manual_*`);
- cÃ³digo de app.

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

## TÃ©rminos de UI/flujo (`current week`, selecciÃ³n, activo)

1. `current week`:
   - marcador visual del estado temporal derivado de `campaign.week_cursor`;
   - no equivale a selecciÃ³n/foco.
1. `selected_week`:
   - `Week` elegida por el usuario para navegar/editar.
1. `selected_entry`:
   - Ãºnica `Entry` visible/activa en el panel de ediciÃ³n para acciones de
     sesiÃ³n en el flujo normal del MVP.
   - una implementaciÃ³n puede materializar esto como **entry visible en visor**
     separada de la navegaciÃ³n (`selected_week`) mientras preserve el contrato
     de acciones sobre la entry visible.
1. `active_entry`:
   - `Entry` que posee la sesiÃ³n activa global (si existe), derivado de una
     `Session` con `ended_at_utc = null`.
1. Los controles `Iniciar/Parar sesiÃ³n` viven en el bloque de la
   `selected_entry` (junto a total jugado y lista de sesiones desplegable).
1. Cambiar `selected_week` o `selected_entry` no implica por sÃ­ mismo cambiar
   `current week` ni cerrar la sesiÃ³n activa global.
1. Una implementaciÃ³n puede mantener un **visor sticky** (Ãºltima entry visible)
   al navegar por weeks/aÃ±os; esto no altera la separaciÃ³n de responsabilidades
   entre navegaciÃ³n, visor y estado activo global.

## Modelo de estado del flujo de sesiÃ³n (cliente)

### Tabla 1 â€” Estados de flujo (`I14-S1`)

| `flow_state_id` | `descripcion` | `session_active_global` | `selected_week` | `selected_entry` | `current_week_marker` | `acciones_disponibles` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `no_active_selected_entry` | Hay `selected_entry` y no existe sesiÃ³n activa global | No | SÃ­ | SÃ­ | SÃ­ | `start`, ediciÃ³n de `Entry`, acciones de `Week` | Estado normal sin sesiÃ³n activa |
| `active_on_selected_entry` | Existe sesiÃ³n activa global y pertenece a la `selected_entry` | SÃ­ | SÃ­ | SÃ­ | SÃ­ | `stop`, ediciÃ³n, acciones de `Week`/`Entry` | `start` sobre la misma `Entry` serÃ­a invÃ¡lido |
| `active_on_other_entry` | Existe sesiÃ³n activa global pero la `selected_entry` es otra | SÃ­ | SÃ­ | SÃ­ | SÃ­ | `start` (con `auto-stop`), ediciÃ³n, navegaciÃ³n/foco | La UI debe mostrar diferencia entre foco y activo |
| `pending_session_action` | AcciÃ³n de sesiÃ³n en curso (cliente esperando resultado) | 0..1 (pendiente) | SÃ­ | SÃ­ | SÃ­ | bloquear reenvÃ­o de la misma acciÃ³n | Estado transitorio de cliente; no reescribe el contrato de `#12` |
| `error_local` | Error funcional local (`transicion_invalida` / `validacion`) tras acciÃ³n | 0..1 | SÃ­ | SÃ­ | SÃ­ | corregir acciÃ³n y reintentar | No requiere `refresh` por defecto |
| `error_conflicto_pending_refresh` | Error de conflicto concurrente detectado | 0..1 desconocido hasta refrescar | SÃ­ | SÃ­ | SÃ­ | `refresh` manual y luego reintento | Alineado con `on-demand refresh` |

## Tabla de transiciones y eventos

### Tabla 2 â€” Eventos y transiciones (`I14-S1` / `I14-S2`)

| `event_id` | `precondiciones` | `estado_origen_relevante` | `comportamiento_cliente` | `operacion_contractual_relacionada` | `postcondicion_visible` | `errores_posibles` | `recuperacion` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `ui.session_start_on_selected_entry` | Existe `selected_entry`; botÃ³n `Iniciar` visible en su bloque | `no_active_selected_entry`, `active_on_other_entry` | Ejecuta `start`; si habÃ­a otra activa, el flujo observable incluye `auto-stop + start`; sin confirmaciÃ³n extra por `auto-stop` | `Session.start` (+ `Session.auto_stop` si aplica) | SesiÃ³n activa global pasa a la `selected_entry`; UI muestra estado activo en esa entry | `conflicto`, `validacion`, `transicion_invalida` (si la entry ya era activa por estado obsoleto) | `conflicto`: `refresh` manual + reintentar; otros: error local |
| `ui.session_stop_on_selected_entry` | Existe `selected_entry` con sesiÃ³n activa global | `active_on_selected_entry` | Ejecuta `stop` desde la `selected_entry` visible | `Session.stop` | Desaparece el estado activo global; la `selected_entry` queda sin sesiÃ³n activa | `conflicto`, `transicion_invalida` | `conflicto`: `refresh` manual + reintentar; `transicion_invalida`: error local |
| `ui.select_week` | El usuario selecciona una `Week` para navegar/editar | Cualquiera | Cambia `selected_week`; no hace `auto-stop`; puede requerir nueva selecciÃ³n de `Entry` para accionar sesiÃ³n | No aplica (navegaciÃ³n/foco) | Cambia el foco temporal/ediciÃ³n; la sesiÃ³n activa global (si existe) sigue corriendo | Ninguno de sesiÃ³n; potenciales errores de lectura fuera de alcance | No aplica a `#14` |
| `ui.select_entry` | Existe `Entry` seleccionable en la `selected_week` | Cualquiera con `selected_week` | Cambia `selected_entry`; no hace `auto-stop`; habilita/actualiza bloque de sesiÃ³n para esa entry | No aplica (selecciÃ³n/foco) | La entry visible cambia; el estado activo puede pertenecer a otra entry | Ninguno de sesiÃ³n; potenciales errores de lectura fuera de alcance | No aplica a `#14` |
| `ui.week_close` | El usuario dispara cierre de `Week`; puede haber sesiÃ³n activa en esa week | Cualquiera | Ejecuta acciÃ³n de cierre de week; si hay sesiÃ³n activa en la week, el `auto-stop` va embebido sin confirmaciÃ³n extra | `Week.close` (+ `Session.auto_stop` si aplica) | Week queda `closed`; si la sesiÃ³n activa pertenecÃ­a a esa week, deja de estar activa; `current week` se actualiza por `week_cursor` derivado | `conflicto`, `validacion`, `transicion_invalida` | `conflicto`: `refresh` manual + reintentar; otros: error local |
| `ui.week_reclose` | El usuario dispara recierre manual `open -> closed` | Cualquiera | Igual patrÃ³n observable que `ui.week_close` para sesiÃ³n activa + cursor | `Week.reclose` (+ `Session.auto_stop` si aplica) | Week `closed`, sesiÃ³n de esa week cerrada si existÃ­a, marcador `current week` actualizado | `conflicto`, `validacion`, `transicion_invalida` | `conflicto`: `refresh` manual + reintentar; otros: error local |
| `ui.entry_delete_selected` | Existe `selected_entry`; puede ser la activa | `active_on_selected_entry`, `no_active_selected_entry` | Ejecuta borrado; si era activa, `auto-stop` ocurre como side-effect de la operaciÃ³n compuesta | `Entry.delete` (+ `Session.auto_stop` si aplica) | Si era activa, el estado activo global queda vacÃ­o; la entry desaparece | `conflicto`, `transicion_invalida` | `conflicto`: `refresh` manual + reintentar; `transicion_invalida`: error local |
| `system.auto_stop_due_start_switch` | Existe sesiÃ³n activa previa y `Session.start` sobre otra `Entry` | `active_on_other_entry` | Side-effect interno del flujo `start` | `Session.auto_stop` dentro de `Session.start` | La sesiÃ³n previa se cierra y la nueva pasa a activa | `conflicto`, `transicion_invalida` (heredados del padre) | Heredada de `ui.session_start_on_selected_entry` |
| `system.auto_stop_due_week_close` | Cierre/recierre de week afecta a una week con sesiÃ³n activa | Cualquiera | Side-effect interno del cierre/recierre | `Session.auto_stop` dentro de `Week.close`/`Week.reclose` | La sesiÃ³n activa de esa week queda cerrada antes de cerrar la week | `conflicto`, `transicion_invalida` (heredados del padre) | Heredada de `ui.week_close` / `ui.week_reclose` |
| `system.auto_stop_due_entry_delete` | Borrado de `Entry` activa | `active_on_selected_entry` | Side-effect interno de borrado | `Session.auto_stop` dentro de `Entry.delete` | La sesiÃ³n activa asociada deja de estar activa antes del borrado | `conflicto`, `transicion_invalida` (heredados del padre) | Heredada de `ui.entry_delete_selected` |

## Reglas operativas por evento

### `ui.session_start_on_selected_entry`

1. La acciÃ³n solo existe en el bloque de la `selected_entry` visible.
1. Si no hay `selected_entry`, no hay acciÃ³n de `start` disponible en el flujo
   normal (no existe `Play` global para suplirla).
1. Si la `selected_entry` ya es la `active_entry`, la acciÃ³n se trata como
   `transicion_invalida` (error local, sin crear sesiÃ³n nueva).
1. Si existe otra `active_entry`, el flujo observable es `auto-stop + start`.
1. El `auto-stop` embebido no pide confirmaciÃ³n extra.

### `ui.session_stop_on_selected_entry`

1. La acciÃ³n solo existe cuando la `selected_entry` es la `active_entry`.
1. Si la sesiÃ³n ya no estÃ¡ activa al aplicar el `stop`, se clasifica como
   `transicion_invalida`.
1. La recuperaciÃ³n por defecto ante `transicion_invalida` es error local (sin
   `refresh` automÃ¡tico).

### `ui.select_week` y `ui.select_entry`

1. Son eventos de navegaciÃ³n/foco, no operaciones de sesiÃ³n.
1. No ejecutan `auto-stop`.
1. No requieren confirmaciÃ³n adicional por existir sesiÃ³n activa global.
1. Deben preservar la visibilidad conceptual de:
   - `current week`;
   - `selected_week` / `selected_entry`;
   - `active_entry` (si existe).

### `ui.week_close` y `ui.week_reclose`

1. `#14` reutiliza el contrato de `#12`:
   - `auto-stop` (si aplica) + cierre/recierre + recÃ¡lculo de `week_cursor` como
     unidad lÃ³gica observable.
1. Si la acciÃ³n padre ya tiene confirmaciÃ³n, esa confirmaciÃ³n cubre todo el
   flujo (incluido el `auto-stop` embebido).
1. `#14` no redefine validaciones de backend (`0` weeks abiertas, conflicto de
   base, etc.); solo documenta el resultado visible y recuperaciÃ³n del cliente.

### `ui.entry_delete_selected`

1. `#14` no redefine cascada ni atomicidad de borrado (`#12`).
1. SÃ­ documenta el efecto observable cuando la `Entry` borrada era la activa:
   - el estado activo global queda vacÃ­o por `auto-stop` embebido.
1. La polÃ­tica exacta de selecciÃ³n/foco posterior al borrado queda fuera de
   alcance de esta issue.

## Cambio de foco y separaciÃ³n foco/activo

1. La UI debe poder mostrar simultÃ¡neamente:
   - `current week` (marcador derivado de `week_cursor`);
   - `selected_week` / `selected_entry` (contexto de ediciÃ³n);
   - `active_entry` (estado activo global).
1. La implementaciÃ³n puede distinguir internamente entre:
   - navegaciÃ³n (`selected_week`);
   - entry visible en visor (sticky);
   - `active_entry`;
   siempre que las acciones de sesiÃ³n sigan actuando sobre la entry visible.
1. Cambiar de `selected_entry` no implica trasladar automÃ¡ticamente el estado
   activo ni ejecutar `stop`.
1. El usuario puede editar otra `Entry`/`Week` mientras existe una sesiÃ³n activa
   global en otra `Entry`, sujeto a las reglas de `#37` y `#12`.

## InteracciÃ³n con cierre/recierre de semana

1. `Week.close` y `Week.reclose` pueden dispararse aunque exista sesiÃ³n activa
   en la week afectada; el `auto-stop` ocurre como side-effect.
1. Si la sesiÃ³n activa estÃ¡ en otra week, no debe cerrarse por un cierre/recierre
   de una week distinta.
1. Tras cierre/recierre exitoso, el marcador `current week` debe reflejar el
   `week_cursor` derivado vigente (segÃºn `#37`, `#13` y `#9`).
1. La selecciÃ³n (`selected_week` / `selected_entry`) sigue siendo un concepto
   distinto del marcador `current week`.

## Errores y recuperaciÃ³n esperada (UI/cliente)

### Tabla 3 â€” Errores y recuperaciÃ³n (`I14-S2` / `I14-S3`)

| `error_case_id` | `categoria` | `trigger` | `feedback_esperado` | `accion_usuario_recomendada` | `requiere_refresh` | `notas` |
| --- | --- | --- | --- | --- | --- | --- |
| `session_start_same_active_entry` | `transicion_invalida` | `start` sobre `selected_entry` que ya es activa | Error local breve; no cambia estado | Mantener sesiÃ³n actual o usar `stop` si quiere cerrarla | No | No crea nueva sesiÃ³n |
| `session_stop_not_active` | `transicion_invalida` | `stop` sobre sesiÃ³n ya cerrada/no activa | Error local | Corregir acciÃ³n; opcionalmente refrescar si sospecha estado obsoleto | No (por defecto) | Sin auto-refresh |
| `session_start_conflict` | `conflicto` | Base obsoleta al aplicar `start` (`auto-stop + start` si aplica) | Error de conflicto concurrente | `refresh` manual y reintentar | SÃ­ | Alineado con `on-demand refresh` |
| `session_stop_conflict` | `conflicto` | Base obsoleta al aplicar `stop` | Error de conflicto concurrente | `refresh` manual y reintentar | SÃ­ | Sin retry automÃ¡tico |
| `week_close_conflict_with_active_session` | `conflicto` | Conflicto durante `Week.close` con `auto-stop` embebido | Error de conflicto de operaciÃ³n compuesta | `refresh` manual y reintentar cierre | SÃ­ | RecuperaciÃ³n heredada de `#12` |
| `week_reclose_invalid_transition` | `transicion_invalida` | `reclose` sobre week ya `closed` o transiciÃ³n no aplicable | Error local | Corregir acciÃ³n | No | Distinto de conflicto |
| `session_start_validation` | `validacion` | `start` con `selected_entry` invÃ¡lida/no disponible por payload/estado local | Error local | Corregir selecciÃ³n/entrada | No | `#14` no redefine validaciÃ³n backend |

### Regla de recuperaciÃ³n por categorÃ­a

1. `conflicto`:
   - feedback de conflicto;
   - `refresh` manual + reintentar;
   - sin auto-refresh ni retry automÃ¡tico.
1. `transicion_invalida`:
   - error local;
   - no `refresh` por defecto.
1. `validacion`:
   - error local;
   - corregir la acciÃ³n/selecciÃ³n antes de reintentar.

## AlineaciÃ³n con `#12`, `#37` y `#18`

### `#12` â€” Contrato por operaciÃ³n

1. `#14` no redefine pre/postcondiciones ni atomicidad de comportamiento.
1. `#14` traduce esas operaciones a flujo observable de cliente/UI:
   - `Session.start`
   - `Session.stop`
   - `Session.auto_stop`
   - `Week.close` / `Week.reclose`
   - `Entry.delete` (solo efecto observable de `auto-stop`)

### `#37` â€” Editabilidad manual e invariantes

1. `Week.status=closed` no bloquea por sÃ­ mismo la ediciÃ³n ni el flujo normal de
   sesiÃ³n; `Session.start/stop` siguen permitidos en weeks `open|closed` segÃºn
   el contrato vigente.
1. `Session.manual_*` puede coexistir con este flujo:
   - puede crear/cerrar una sesiÃ³n activa global;
   - no sustituye ni reespecifica el flujo normal `start/stop/auto-stop`.
1. Se preserva la invariante `0..1` sesiÃ³n activa global.

### `#18` â€” Timestamps y orden estable

1. `#14` no define desempates ni orden estable.
1. Cuando el flujo requiere refrescar listas/estado de sesiones tras acciones o
   conflictos, el orden visible se rige por `docs/timestamp-order-policy.md`.

### `#16` â€” Consultas mÃ­nimas de pantalla principal

1. `#14` define el comportamiento observable del flujo (`start/stop/auto-stop`,
   separaciÃ³n foco/activo y recuperaciÃ³n de errores).
1. `#16` define las lecturas mÃ­nimas que soportan ese flujo en pantalla:
   - `Q6 active_session_global`;
   - `Q7 active_entry_doc_if_needed` (condicional);
   - `Q8 sessions_selected_entry_combined`.
1. El arranque sin selecciÃ³n (`selected_week`/`selected_entry` vacÃ­os) y la
   carga diferida de sesiones hasta seleccionar `Entry` se documentan en `#16`.

## Casos de aceptaciÃ³n / verificaciÃ³n documental

1. `Start` sobre `selected_entry` sin sesiÃ³n activa global crea sesiÃ³n activa y
   la UI la muestra como activa.
1. `Start` sobre otra `selected_entry` con una sesiÃ³n activa global previa
   documenta `auto-stop + start` sin confirmaciÃ³n extra.
1. `Start` sobre la `Entry` ya activa se clasifica como `transicion_invalida`
   con error local.
1. `Stop` sobre `selected_entry` activa cierra la sesiÃ³n activa.
1. `Stop` invÃ¡lido se clasifica como `transicion_invalida` con error local.
1. Cambiar foco (`select_week` / `select_entry`) no hace `auto-stop`.
1. `Week.close` con sesiÃ³n activa en esa week documenta el resultado observable
   de auto-stop + cierre + actualizaciÃ³n del marcador `current week`.
1. `Week.reclose` replica el patrÃ³n de recuperaciÃ³n y clasificaciÃ³n de errores
   del cierre normal.
1. `Entry.delete` activa documenta efecto observable de `auto-stop` sin
   reescribir cascada/atomicidad de `#12`.
1. El documento separa explÃ­citamente `current week`, selecciÃ³n y `active_entry`.

## Riesgos, lÃ­mites y decisiones diferidas

- El detalle visual exacto de indicadores de foco/activo y mensajes de error
  queda para diseÃ±o/UI futura.
- La polÃ­tica de selecciÃ³n/foco posterior a borrar una `Entry` queda fuera de
  alcance de `#14`.
- La tÃ©cnica de sincronizaciÃ³n/atomicidad Firestore permanece en `#12` y cÃ³digo.
- La matriz transversal de edge cases priorizados para concurrencia/sync se
  documenta en `docs/concurrency-sync-edge-case-matrix.md` (Issue `#17`), que
  reutiliza este flujo como fuente de expectativas y recuperaciÃ³n.
- El legado (`tdd.md` (retirado el 2026-03-01)) puede seguir reflejando un `Play/Stop` en barra inferior;
  esta decisiÃ³n oficial prevalece para el MVP actual.

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
- `tdd.md` (retirado el 2026-03-01) (legado temporal; puede divergir en detalles de UI)
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`

