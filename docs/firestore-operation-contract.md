# Contrato de Operaciones Firestore por Agregado (MVP)

## Metadatos

- `doc_id`: DOC-FIRESTORE-OPERATION-CONTRACT
- `purpose`: Definir el contrato documental de operaciones de escritura por agregado del MVP (precondiciones, validaciones, rechazos y postcondiciones), alineado con sincronizaciÃ³n, conflictos, temporalidad y editabilidad.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-16

## Objetivo

Cerrar la especificaciÃ³n contractual de operaciones Firestore por agregado para
el MVP, de forma que futuras implementaciones tengan reglas claras de dominio,
rechazo y atomicidad esperada (a nivel de comportamiento) sin adelantar la
tÃ©cnica concreta de Firestore.

## Alcance y no alcance

Incluye:

- inventario de operaciones de escritura por agregado (`campaign`, `week`,
  `entry` incluidas mutaciones de `resource_deltas`, `session`);
- precondiciones, validaciones, postcondiciones y rechazos esperados;
- operaciones compuestas y atomicidad esperada de comportamiento;
- alineaciÃ³n explÃ­cita con `#13` (temporal) y `#37` (editabilidad);
- diferenciaciÃ³n entre `conflicto`, `transicion_invalida` y `validacion`.

No incluye:

- implementaciÃ³n concreta en Firestore (transacciones, batch, tÃ©cnica de
  precondiciones);
- consultas/lecturas (`#16`);
- timestamps/desempates de orden estable (se definen en
  `docs/timestamp-order-policy.md`, Issue `#18`);
- diseÃ±o de UI o flujos de pantalla (`#14`, `#16`);
- cÃ³digo de app.

## Entradas y prerrequisitos

- `docs/sync-strategy.md` (Issue `#7`)
- `docs/conflict-policy.md` (Issue `#8`)
- `docs/campaign-temporal-controls.md` (Issue `#9`, con actualizaciÃ³n por `#37`)
- `docs/campaign-temporal-initialization.md` (Issue `#13`)
- `docs/editability-policy.md` (Issue `#37`)
- `docs/resource-delta-model.md` (Issue `#40`, supersesiÃ³n parcial de recursos)
- `docs/resource-validation-recalculation.md` (Issue `#15`, detalle de validaciÃ³n y recÃ¡lculo de recursos)
- `docs/timestamp-order-policy.md` (Issue `#18`)
- `docs/domain-glossary.md`

## Convenciones del contrato

1. Este documento define **comportamiento esperado**, no tÃ©cnica Firestore.
1. `respuesta_cliente_recomendada` distingue:
   - `refrescar + reintentar` para conflictos concurrentes;
   - error local (sin refresh por defecto) para transiciones invÃ¡lidas;
   - correcciÃ³n de datos/entrada para rechazos de validaciÃ³n.
1. La **semana actual derivada** (primera `Week` abierta) se expresa como
   **postcondiciÃ³n derivada** en operaciones que cambian estado de `Week` o
   estructura temporal.
1. **Nota de transiciÃ³n (`#76`)**: la implementaciÃ³n actual todavÃ­a persiste/
   consume `campaign.week_cursor` como mecanismo tÃ©cnico transitorio; este
   documento lo trata como detalle de implementaciÃ³n a retirar en `#81`, no
   como contrato canÃ³nico.
1. `Session` no usa un campo `state`; una sesiÃ³n activa se define por
   `ended_at_utc = null`.
1. Ownership de `Session` se deriva de la ruta; no se redefine por campos.
1. Los cambios de recursos del MVP se modelan como `Entry.resource_deltas`
   (mapa embebido), no como entidad `ResourceChange`.

## Agregados y operaciones cubiertas

- `campaign`
  - `Campaign.provision_initial_years`
  - `Campaign.extend_years_plus_one`
- `week`
  - `Week.close`
  - `Week.reopen`
  - `Week.reclose`
- `entry`
  - `Entry.create`
  - `Entry.update`
  - `Entry.update_notes`
  - `Entry.delete`
  - `Entry.reorder_within_week`
  - `Entry.adjust_resource_delta`
  - `Entry.set_resource_delta`
  - `Entry.clear_resource_delta`
- `session`
  - `Session.start`
  - `Session.stop`
  - `Session.auto_stop` (derivada/compuesta)
  - `Session.manual_create`
  - `Session.manual_update`
  - `Session.manual_delete`
## Operaciones excluidas del contrato activo MVP

- `Campaign.set_week_cursor_manual`
  - estado: **excluida**
  - motivo: la semÃ¡ntica previa de ajuste manual fue sustituida por la polÃ­tica
    derivada de `week_cursor` definida en `docs/editability-policy.md` (Issue
    `#37`) y alineada en `docs/campaign-temporal-controls.md`.

## Matriz global de operaciones

| operation_id | agregado_principal | agregados_afectados | tipo | disparador | estado_mvp | dependencias_documentales | notas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Campaign.provision_initial_years` | `campaign` | `campaign`, `year`, `season`, `week` | `compuesta` | creaciÃ³n/provisiÃ³n inicial de campaÃ±a | `activa` | `#9`, `#13`, `#37` | semana actual derivada como postcondiciÃ³n |
| `Campaign.extend_years_plus_one` | `campaign` | `campaign`, `year`, `season`, `week` | `compuesta` | acciÃ³n `+` de aÃ±o (UI) | `activa` | `#9`, `#13`, `#37` | crea 1 aÃ±o completo; cursor derivado |
| `Campaign.set_week_cursor_manual` | `campaign` | `campaign` | `simple` | ajuste manual (semÃ¡ntica histÃ³rica) | `excluida` | `#9`, `#37` | semÃ¡ntica sustituida en MVP |
| `Week.close` | `week` | `week`, `campaign`, `session` | `compuesta` | cierre normal de semana | `activa` | `#8`, `#37` | auto-stop si hay sesiÃ³n activa |
| `Week.reopen` | `week` | `week`, `campaign` | `compuesta` | correcciÃ³n manual de estado | `activa` | `#8`, `#37` | recÃ¡lculo de semana actual derivada |
| `Week.reclose` | `week` | `week`, `campaign`, `session` | `compuesta` | correcciÃ³n manual de estado | `activa` | `#8`, `#37` | auto-stop si hay sesiÃ³n activa |
| `Entry.create` | `entry` | `entry`, `week` | `compuesta` | creaciÃ³n manual de entry | `activa` | `#37`, glosario | auto-normaliza `order_index` si detecta secuencia inconsistente |
| `Entry.update` | `entry` | `entry` | `simple` | ediciÃ³n manual de entry | `activa` | `#37`, glosario | alcance amplio; sin mover de `Week` |
| `Entry.update_notes` | `entry` | `entry` | `simple` | ediciÃ³n rÃ¡pida de notas de entry | `activa` | `#37`, glosario | permitido en `open|closed`; no cambia tipo/orden |
| `Entry.delete` | `entry` | `entry`, `session`, `campaign` | `compuesta` | borrado manual de entry | `activa` | glosario, `#37`, `#40` | hard delete real; auto-stop si entry activa; elimina `resource_deltas` con la entry |
| `Entry.reorder_within_week` | `entry` | `entry`, `week` | `compuesta` | mover una entry en la misma week | `activa` | `#8`, `#37` | resecuencia densa `1..N` |
| `Entry.adjust_resource_delta` | `entry` | `entry`, `campaign` | `compuesta` | tap `+/-` de recurso en una entry | `activa` | `#8`, `#37`, `#40`, glosario | ajusta delta neto en `Entry.resource_deltas` y valida totales |
| `Entry.set_resource_delta` | `entry` | `entry`, `campaign` | `compuesta` | ediciÃ³n manual de delta neto | `activa` | `#8`, `#37`, `#40`, glosario | reemplaza delta neto; elimina clave si queda en `0` |
| `Entry.clear_resource_delta` | `entry` | `entry`, `campaign` | `compuesta` | limpieza explÃ­cita de recurso en la entry | `activa` | `#8`, `#37`, `#40`, glosario | elimina clave de `resource_deltas`; valida totales |
| `Session.start` | `session` | `campaign`, `entry`, `session` | `compuesta` | iniciar sesiÃ³n de juego | `activa` | `#8`, glosario | permitido en week `open|closed`; auto-stop si hay activa |
| `Session.stop` | `session` | `campaign`, `entry`, `session` | `simple` | detener sesiÃ³n activa | `activa` | `#8`, glosario | invÃ¡lida si la sesiÃ³n ya no estÃ¡ activa |
| `Session.auto_stop` | `session` | `campaign`, `entry`, `session` | `derivada` | `start`, `Week.close/reclose`, `Entry.delete` | `activa` | glosario, `#37` | no es acciÃ³n manual principal |
| `Session.manual_create` | `session` | `campaign`, `entry`, `session` | `simple` | correcciÃ³n manual | `activa` | `#37`, glosario | histÃ³rica o activa; permitido en week `open|closed` |
| `Session.manual_update` | `session` | `campaign`, `entry`, `session` | `simple` | correcciÃ³n manual | `activa` | `#37`, glosario | corrige timestamps; `null <-> valor`; sin reparenting |
| `Session.manual_delete` | `session` | `campaign`, `entry`, `session` | `simple` | correcciÃ³n manual | `activa` | `#37`, glosario | hard delete; permitido en week `open|closed` |

## Contrato por operaciÃ³n

| operation_id | precondiciones_dominio | precondiciones_conflicto | validaciones | postcondiciones | rechazos_esperados | categoria_rechazo | atomicidad_esperada_comportamiento | respuesta_cliente_recomendada | notas_de_implementaciÃ³n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Campaign.provision_initial_years` | campaÃ±a existe y estÃ¡ provisionable | base de campaÃ±a no obsoleta | crea 4 aÃ±os; `summer->winter`; 10 semanas/estaciÃ³n; no duplicados (`year/season/week`) | estructura temporal inicial completa; semana actual derivada apunta a primera week abierta | duplicados, base obsoleta | `validacion` / `conflicto` | todo el bloque temporal se crea o falla completo | `refrescar + reintentar` si conflicto; error local si duplicado/estado invÃ¡lido | no fija tÃ©cnica Firestore |
| `Campaign.extend_years_plus_one` | campaÃ±a ya provisionada; Ãºltimo aÃ±o identificable | base de campaÃ±a/estructura temporal no obsoleta | crea exactamente 1 aÃ±o; continuidad `year_number` y `week_number`; no duplicados | nuevo aÃ±o completo aÃ±adido; semana actual derivada vÃ¡lida | duplicados; continuidad invÃ¡lida; base obsoleta | `validacion` / `conflicto` | se aÃ±ade el aÃ±o completo o falla completo | `refrescar + reintentar` si conflicto; error local si estructura invÃ¡lida | disparo UI desde `+` de aÃ±o |
| `Week.close` | week existe; transiciÃ³n `open -> closed`; week abierta provisionada no quedarÃ¡ en 0 tras operaciÃ³n | base de `week.status` y sesiÃ³n activa relevante no obsoletas | si hay sesiÃ³n activa en la week, ejecutar `Session.auto_stop`; validar recÃ¡lculo de la semana actual derivada | week queda `closed`; sesiÃ³n activa de esa week queda cerrada si existÃ­a; semana actual derivada recalculada | transiciÃ³n ya cerrada; dejarÃ­a 0 weeks abiertas; base obsoleta | `transicion_invalida` / `validacion` / `conflicto` | auto-stop + cierre + recÃ¡lculo se consideran una sola operaciÃ³n lÃ³gica | error local (transiciÃ³n/validaciÃ³n); `refrescar + reintentar` si conflicto | `closed` no bloquea mutaciones por sÃ­ mismo |
| `Week.reopen` | week existe; transiciÃ³n `closed -> open` | base de `week.status` no obsoleta | transiciÃ³n vÃ¡lida; recÃ¡lculo de la semana actual derivada | week queda `open`; semana actual derivada recalculada | transiciÃ³n ya abierta; base obsoleta | `transicion_invalida` / `conflicto` | cambio de estado + recÃ¡lculo como operaciÃ³n lÃ³gica Ãºnica | error local si transiciÃ³n invÃ¡lida; `refrescar + reintentar` si conflicto | correcciÃ³n manual explÃ­cita |
| `Week.reclose` | week existe; transiciÃ³n `open -> closed`; no dejar 0 weeks abiertas | base de `week.status` y sesiÃ³n activa relevante no obsoletas | si hay sesiÃ³n activa en la week, `auto-stop`; validar recÃ¡lculo de cursor | week queda `closed`; cursor derivado vÃ¡lido | transiciÃ³n ya cerrada; dejarÃ­a 0 weeks abiertas; base obsoleta | `transicion_invalida` / `validacion` / `conflicto` | auto-stop + cambio de estado + recÃ¡lculo como operaciÃ³n lÃ³gica Ãºnica | error local (transiciÃ³n/validaciÃ³n); `refrescar + reintentar` si conflicto | correcciÃ³n manual de estado |
| `Entry.create` | week existe; ownership por ruta vÃ¡lido | base de orden (`entries` de la week) no obsoleta para inserciÃ³n | `Entry.type` vÃ¡lido; `scenario_ref` obligatorio si `scenario`; si secuencia `order_index` inconsistente, auto-normalizar denso `1..N` antes/asociado a inserciÃ³n | nueva entry creada con `order_index` vÃ¡lido y secuencia consistente | payload invÃ¡lido; week inexistente; base obsoleta no resoluble | `validacion` / `conflicto` | normalizaciÃ³n de orden + creaciÃ³n forman operaciÃ³n lÃ³gica Ãºnica | error local si payload invÃ¡lido; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
| `Entry.update` | entry existe | base de entry no obsoleta | ediciÃ³n amplia de campos funcionales; `scenario_ref` consistente; no cambiar de `Week` | entry actualizada en la misma week | payload invÃ¡lido; intento de mover de week; base obsoleta | `validacion` / `conflicto` | actualizaciÃ³n simple | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | sin reparenting |
| `Entry.update_notes` | entry existe | base de entry no obsoleta | `notes` es string; permitido en `open|closed` | notas de entry actualizadas sin modificar tipo/orden | payload invÃ¡lido; base obsoleta | `validacion` / `conflicto` | actualizaciÃ³n simple | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | operaciÃ³n enfocada para ediciÃ³n rÃ¡pida en listado semanal |
| `Entry.delete` | entry existe | base de entry e hijos relevantes no obsoletas | hard delete; si entry activa, `auto-stop`; borrado de `sessions`; eliminaciÃ³n implÃ­cita de `resource_deltas` con la `Entry` | entry eliminada con sus `sessions` y `resource_deltas`; no queda sesiÃ³n activa asociada a esa entry | entry ya borrada; base obsoleta; cascada invÃ¡lida por conflicto | `transicion_invalida` / `conflicto` | auto-stop + borrado de hijos + borrado de entry se tratan como operaciÃ³n lÃ³gica Ãºnica | error local si ya no existe; `refrescar + reintentar` si conflicto | hard delete real (sin soft delete funcional) |
| `Entry.reorder_within_week` | entry existe y pertenece a la week objetivo; misma week | base del orden de la week no obsoleta | posiciÃ³n destino vÃ¡lida; resecuencia densa `1..N`; no mover entre weeks | orden de entries de la week queda consistente | entry inexistente; week inconsistente; base obsoleta | `validacion` / `conflicto` | mover + resecuencia como operaciÃ³n lÃ³gica Ãºnica | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
| `Entry.adjust_resource_delta` | entry existe; `resource_key` pertenece al catÃ¡logo MVP | base de entry y `resource_totals` relevantes no obsoletas | ajuste entero firmado; cÃ¡lculo de delta neto; eliminar clave si resultado `0`; totales finales no negativos | `Entry.resource_deltas` actualizado (neto); `campaign.resource_totals` consistente | `resource_key` invÃ¡lida; payload invÃ¡lido; totales negativos; base obsoleta | `validacion` / `conflicto` | recÃ¡lculo de totales + actualizaciÃ³n de `Entry.resource_deltas` como operaciÃ³n lÃ³gica Ãºnica | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | permitido en week `open|closed`; no crea log incremental |
| `Entry.set_resource_delta` | entry existe; `resource_key` vÃ¡lida | base de entry y totales relevantes no obsoletas | delta entero firmado; si delta final `0`, eliminar clave; totales finales no negativos | delta neto fijado (o clave eliminada) y totales consistentes | `resource_key` invÃ¡lida; payload invÃ¡lido; totales negativos; base obsoleta | `validacion` / `conflicto` | recÃ¡lculo de totales + escritura del mapa como operaciÃ³n lÃ³gica Ãºnica | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | ediciÃ³n manual directa del delta neto |
| `Entry.clear_resource_delta` | entry existe | base de entry y totales relevantes no obsoletas | `resource_key` vÃ¡lida; recÃ¡lculo mantiene totales no negativos | clave eliminada de `resource_deltas` (o permanece ausente si se trata como idempotente) y totales consistentes | `resource_key` invÃ¡lida; totales negativos; base obsoleta | `validacion` / `conflicto` | recÃ¡lculo de totales + limpieza de clave como operaciÃ³n lÃ³gica Ãºnica | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | limpiar clave inexistente puede tratarse como idempotente (sin error) |
| `Session.start` | entry existe; sesiÃ³n activa global puede ser 0..1; week `open|closed` permitida | base de sesiÃ³n activa global no obsoleta | si ya hay sesiÃ³n activa, `auto-stop` previo; garantizar unicidad `0..1` activa | nueva sesiÃ³n activa (o transiciÃ³n equivalente) creada; unicidad preservada | unicidad violada; entry invÃ¡lida; base obsoleta | `validacion` / `conflicto` | `auto-stop + start` (si aplica) como operaciÃ³n lÃ³gica Ãºnica | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | actividad derivada por `ended_at_utc=null` |
| `Session.stop` | sesiÃ³n objetivo existe y estÃ¡ activa (`ended_at_utc=null`) | base de sesiÃ³n no obsoleta | sesiÃ³n sigue activa al momento de aplicar stop | sesiÃ³n queda cerrada (`ended_at_utc` definido) | sesiÃ³n ya cerrada/no activa; base obsoleta | `transicion_invalida` / `conflicto` | actualizaciÃ³n simple | error local si transiciÃ³n invÃ¡lida; `refrescar + reintentar` si conflicto | distingue conflicto de transiciÃ³n invÃ¡lida |
| `Session.auto_stop` | sesiÃ³n activa previa existe | base de sesiÃ³n activa no obsoleta | trigger vÃ¡lido (`start`, `Week.close/reclose`, `Entry.delete`) | sesiÃ³n activa previa queda cerrada | sesiÃ³n ya no activa; base obsoleta | `transicion_invalida` / `conflicto` | se evalÃºa dentro de la operaciÃ³n compuesta disparadora | heredada de la operaciÃ³n padre | no se expone como acciÃ³n manual principal |
| `Session.manual_create` | entry existe; ownership por ruta vÃ¡lido | base de sesiÃ³n activa global no obsoleta si crea una activa | timestamps vÃ¡lidos; histÃ³rica o activa; unicidad `0..1` activa global | sesiÃ³n manual creada | timestamps invÃ¡lidos; unicidad violada; base obsoleta | `validacion` / `conflicto` | creaciÃ³n simple | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
| `Session.manual_update` | sesiÃ³n existe; ownership por ruta inmutable | base de la sesiÃ³n y de unicidad global no obsoletas | corrige `started_at_utc`/`ended_at_utc`; permite `null <-> valor`; sin reparenting; unicidad de activa global | sesiÃ³n corregida; unicidad preservada | timestamps invÃ¡lidos; reparenting intentado; unicidad violada; base obsoleta | `validacion` / `conflicto` | actualizaciÃ³n simple | error local si validaciÃ³n; `refrescar + reintentar` si conflicto | no existe campo `state` separado |
| `Session.manual_delete` | sesiÃ³n existe | base de sesiÃ³n no obsoleta | hard delete; preservar `0..1` activa global | sesiÃ³n eliminada | sesiÃ³n ya borrada; base obsoleta | `transicion_invalida` / `conflicto` | borrado simple | error local si transiciÃ³n invÃ¡lida; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
## Operaciones compuestas y atomicidad esperada (comportamiento)

Este documento exige atomicidad a nivel de **resultado observable** (Ã©xito
completo o fallo completo), sin fijar si la implementaciÃ³n usa transacciÃ³n,
batch o combinaciÃ³n de mecanismos Firestore.

Operaciones compuestas mÃ­nimas:

1. `Session.start` con `auto-stop` previo cuando ya existe sesiÃ³n activa.
1. `Week.close` / `Week.reclose` con `auto-stop` + recÃ¡lculo de la semana actual derivada.
1. `Entry.delete` activa con `auto-stop` + borrado de `sessions` (y eliminaciÃ³n
   implÃ­cita de `resource_deltas` al borrar la `Entry`).
1. `Entry.create` con auto-normalizaciÃ³n de `order_index` cuando la secuencia de
   la week llega inconsistente.
1. `Entry.adjust_resource_delta`, `Entry.set_resource_delta` y
   `Entry.clear_resource_delta` con recÃ¡lculo de `campaign.resource_totals`.
1. `Campaign.provision_initial_years` y `Campaign.extend_years_plus_one` con
   estructura temporal completa + semana actual derivada vÃ¡lida.

## AlineaciÃ³n temporal con #13

| operacion | insumo_#13 | insumo_#37 | regla_en_#12 | no_definido_en_#12 | riesgo_si_se_viola |
| --- | --- | --- | --- | --- | --- |
| `Campaign.provision_initial_years` | 4 aÃ±os iniciales, `summer->winter`, 10 semanas/estaciÃ³n, `week_number` correlativo | semana actual derivada; no dejar 0 abiertas | creaciÃ³n completa con duplicados rechazados y semana actual derivada vÃ¡lida | tÃ©cnica Firestore | estructura temporal inconsistente / semana actual invÃ¡lida |
| `Campaign.extend_years_plus_one` | +1 aÃ±o, continuidad `year_number`/`week_number` | semana actual derivada | extensiÃ³n exacta de 1 aÃ±o; sin reprovisiÃ³n; sin duplicados | tÃ©cnica Firestore | numeraciÃ³n rota o duplicados |
| `Week.close/reopen/reclose` | coherencia `week_number`/jerarquÃ­a | recÃ¡lculo de semana actual derivada; transiciÃ³n manual | cambio de estado + postcondiciÃ³n de semana actual derivada | timestamp/desempate | semana actual incoherente o estado invÃ¡lido |
| `Entry`/`Session` (incluyendo `Entry.resource_deltas`) sobre weeks histÃ³ricas | weeks siguen existiendo y `week_number` no cambia | editabilidad amplia en `open|closed` | operaciones permitidas en weeks `closed` salvo validaciÃ³n especÃ­fica | polÃ­tica UI | bloqueos artificiales o contradicciÃ³n con `#37` |

## AlineaciÃ³n de editabilidad e invariantes con #37

1. `Campaign.set_week_cursor_manual` se documenta como exclusiÃ³n activa del MVP.
1. La semana actual derivada (histÃ³ricamente implementada como `week_cursor`) es postcondiciÃ³n y nunca selecciÃ³n manual libre.
1. `Week.status=closed` es marcador informativo; no bloquea por sÃ­ mismo
   mutaciones de `Entry` (incluyendo `resource_deltas`) ni `Session`.
1. `Entry.reorder_within_week` estÃ¡ limitado a la misma `Week` y resecuencia
   densa `1..N`.
1. `Session.manual_update` no cambia ownership por ruta y puede corregir
   `ended_at_utc` en ambos sentidos.
1. Debe preservarse `0..1` sesiÃ³n activa global.
1. Debe preservarse la existencia de al menos una `Week` abierta provisionada.

## Rechazos por conflicto, validaciÃ³n y transiciÃ³n invÃ¡lida

### `conflicto`

- La base relevante cambiÃ³ concurrentemente respecto a la lectura del cliente.
- Respuesta cliente recomendada: `refrescar + reintentar`.

### `validacion`

- La entrada o el resultado violan invariantes (por ejemplo, `scenario_ref`
  ausente, totales negativos, dejar 0 weeks abiertas, posiciÃ³n invÃ¡lida).
- Respuesta cliente recomendada: error local y correcciÃ³n de la acciÃ³n/entrada.

### `transicion_invalida`

- La entidad ya no estÃ¡ en el estado requerido para la transiciÃ³n pedida (por
  ejemplo, `Week.close` sobre `closed`, `Session.stop` sobre sesiÃ³n no activa).
- Respuesta cliente recomendada: error local (sin refresh por defecto), salvo
  que la UI detecte otros indicios de estado obsoleto.

## Casos de aceptaciÃ³n / verificaciÃ³n documental

1. `Campaign.extend_years_plus_one` crea exactamente 1 aÃ±o y mantiene
   continuidad temporal de `#13`.
1. `Week.close` con sesiÃ³n activa define `auto-stop + cerrar` y recÃ¡lculo de la
   semana actual derivada como operaciÃ³n compuesta.
1. `Week.close` sobre week ya `closed` se clasifica como `transicion_invalida`
   con error local.
1. `Week.reclose` rechaza operaciones que dejen `0` weeks abiertas.
1. `Session.start` queda permitido en week `open` o `closed`.
1. `Session.stop` invÃ¡lido se clasifica como `transicion_invalida`.
1. `Session.manual_update` permite `ended_at_utc: valor -> null` y `null -> valor`
   preservando unicidad de sesiÃ³n activa global.
1. `Session.manual_update` no permite reparenting.
1. `Entry.create` auto-normaliza `order_index` cuando detecta secuencia
   inconsistente.
1. `Entry.update_notes` permite editar notas de `Entry` sin cambiar
   `type/scenario_ref/order_index`.
1. `Entry.reorder_within_week` funciona tambiÃ©n en weeks `closed` y resecuencia
   a `1..N`.
1. Las operaciones de recursos del contrato se expresan sobre
   `Entry.resource_deltas` (`adjust/set/clear`) y no sobre `ResourceChange`.
1. `Campaign.set_week_cursor_manual` aparece como exclusiÃ³n activa del contrato
   MVP.

## Riesgos, lÃ­mites y decisiones diferidas

- La tÃ©cnica exacta para garantizar atomicidad en Firestore queda diferida a la
  implementaciÃ³n.
- La polÃ­tica de timestamps y desempate estable se define en
  `docs/timestamp-order-policy.md` (Issue `#18`) y este contrato no la
  reespecifica.
- El contrato no define lecturas ni consultas (`#16`).
- La parte de recursos de este contrato fue parcialmente supersedida por
  `docs/resource-delta-model.md` (Issue `#40`) y parcheada con operaciones
  sobre `Entry.resource_deltas`; el detalle de validaciÃ³n y recÃ¡lculo de
  recursos se especifica en `docs/resource-validation-recalculation.md`
  (Issue `#15`).
- La UX exacta para errores de conflicto vs transiciÃ³n invÃ¡lida se concreta en
  issues de flujo (`#14`) y UI.
- La matriz transversal de edge cases de concurrencia/sincronizaciÃ³n se
  documenta en `docs/concurrency-sync-edge-case-matrix.md` (Issue `#17`) como
  traducciÃ³n verificable de este contrato y otras polÃ­ticas.

## Referencias

- `docs/domain-glossary.md`
- `docs/sync-strategy.md`
- `docs/conflict-policy.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/editability-policy.md`
- `docs/resource-delta-model.md`
- `docs/resource-validation-recalculation.md`
- `docs/timestamp-order-policy.md`
- `docs/concurrency-sync-edge-case-matrix.md`
- `docs/decision-log.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`

