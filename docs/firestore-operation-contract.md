# Contrato de Operaciones Firestore por Agregado (MVP)

## Metadatos

- `doc_id`: DOC-FIRESTORE-OPERATION-CONTRACT
- `purpose`: Definir el contrato documental de operaciones de escritura por agregado del MVP (precondiciones, validaciones, rechazos y postcondiciones), alineado con sincronización, conflictos, temporalidad y editabilidad.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar la especificación contractual de operaciones Firestore por agregado para
el MVP, de forma que futuras implementaciones tengan reglas claras de dominio,
rechazo y atomicidad esperada (a nivel de comportamiento) sin adelantar la
técnica concreta de Firestore.

## Alcance y no alcance

Incluye:

- inventario de operaciones de escritura por agregado (`campaign`, `week`,
  `entry`, `session`, `resource_change`);
- precondiciones, validaciones, postcondiciones y rechazos esperados;
- operaciones compuestas y atomicidad esperada de comportamiento;
- alineación explícita con `#13` (temporal) y `#37` (editabilidad);
- diferenciación entre `conflicto`, `transicion_invalida` y `validacion`.

No incluye:

- implementación concreta en Firestore (transacciones, batch, técnica de
  precondiciones);
- consultas/lecturas (`#16`);
- timestamps/desempates de orden estable (`#18`);
- diseño de UI o flujos de pantalla (`#14`, `#16`);
- código de app.

## Entradas y prerrequisitos

- `docs/sync-strategy.md` (Issue `#7`)
- `docs/conflict-policy.md` (Issue `#8`)
- `docs/campaign-temporal-controls.md` (Issue `#9`, con actualización por `#37`)
- `docs/campaign-temporal-initialization.md` (Issue `#13`)
- `docs/editability-policy.md` (Issue `#37`)
- `docs/domain-glossary.md`

## Convenciones del contrato

1. Este documento define **comportamiento esperado**, no técnica Firestore.
1. `respuesta_cliente_recomendada` distingue:
   - `refrescar + reintentar` para conflictos concurrentes;
   - error local (sin refresh por defecto) para transiciones inválidas;
   - corrección de datos/entrada para rechazos de validación.
1. `week_cursor` se expresa como **postcondición derivada** en operaciones que
   cambian estado de `Week` o estructura temporal.
1. `Session` no usa un campo `state`; una sesión activa se define por
   `ended_at_utc = null`.
1. Ownership de `Session` y `ResourceChange` se deriva de la ruta; no se
   redefine por campos.

## Agregados y operaciones cubiertas

- `campaign`
  - `Campaign.provision_initial_years`
  - `Campaign.extend_years_plus_one`
- `week`
  - `Week.close`
  - `Week.reopen`
  - `Week.reclose`
  - `Week.update_notes`
- `entry`
  - `Entry.create`
  - `Entry.update`
  - `Entry.delete`
  - `Entry.reorder_within_week`
- `session`
  - `Session.start`
  - `Session.stop`
  - `Session.auto_stop` (derivada/compuesta)
  - `Session.manual_create`
  - `Session.manual_update`
  - `Session.manual_delete`
- `resource_change`
  - `ResourceChange.create`
  - `ResourceChange.update`
  - `ResourceChange.delete`

## Operaciones excluidas del contrato activo MVP

- `Campaign.set_week_cursor_manual`
  - estado: **excluida**
  - motivo: la semántica previa de ajuste manual fue sustituida por la política
    derivada de `week_cursor` definida en `docs/editability-policy.md` (Issue
    `#37`) y alineada en `docs/campaign-temporal-controls.md`.

## Matriz global de operaciones

| operation_id | agregado_principal | agregados_afectados | tipo | disparador | estado_mvp | dependencias_documentales | notas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Campaign.provision_initial_years` | `campaign` | `campaign`, `year`, `season`, `week` | `compuesta` | creación/provisión inicial de campaña | `activa` | `#9`, `#13`, `#37` | `week_cursor` derivado como postcondición |
| `Campaign.extend_years_plus_one` | `campaign` | `campaign`, `year`, `season`, `week` | `compuesta` | acción `+` de año (UI) | `activa` | `#9`, `#13`, `#37` | crea 1 año completo; cursor derivado |
| `Campaign.set_week_cursor_manual` | `campaign` | `campaign` | `simple` | ajuste manual (semántica histórica) | `excluida` | `#9`, `#37` | semántica sustituida en MVP |
| `Week.close` | `week` | `week`, `campaign`, `session` | `compuesta` | cierre normal de semana | `activa` | `#8`, `#37` | auto-stop si hay sesión activa |
| `Week.reopen` | `week` | `week`, `campaign` | `compuesta` | corrección manual de estado | `activa` | `#8`, `#37` | recálculo de `week_cursor` |
| `Week.reclose` | `week` | `week`, `campaign`, `session` | `compuesta` | corrección manual de estado | `activa` | `#8`, `#37` | auto-stop si hay sesión activa |
| `Week.update_notes` | `week` | `week` | `simple` | edición de notas | `activa` | `#8`, `#37` | permitido en `open|closed` |
| `Entry.create` | `entry` | `entry`, `week` | `compuesta` | creación manual de entry | `activa` | `#37`, glosario | auto-normaliza `order_index` si detecta secuencia inconsistente |
| `Entry.update` | `entry` | `entry` | `simple` | edición manual de entry | `activa` | `#37`, glosario | alcance amplio; sin mover de `Week` |
| `Entry.delete` | `entry` | `entry`, `session`, `resource_change`, `campaign` | `compuesta` | borrado manual de entry | `activa` | glosario, `#37` | hard delete real; cascada; auto-stop si entry activa |
| `Entry.reorder_within_week` | `entry` | `entry`, `week` | `compuesta` | mover una entry en la misma week | `activa` | `#8`, `#37` | resecuencia densa `1..N` |
| `Session.start` | `session` | `campaign`, `entry`, `session` | `compuesta` | iniciar sesión de juego | `activa` | `#8`, glosario | permitido en week `open|closed`; auto-stop si hay activa |
| `Session.stop` | `session` | `campaign`, `entry`, `session` | `simple` | detener sesión activa | `activa` | `#8`, glosario | inválida si la sesión ya no está activa |
| `Session.auto_stop` | `session` | `campaign`, `entry`, `session` | `derivada` | `start`, `Week.close/reclose`, `Entry.delete` | `activa` | glosario, `#37` | no es acción manual principal |
| `Session.manual_create` | `session` | `campaign`, `entry`, `session` | `simple` | corrección manual | `activa` | `#37`, glosario | histórica o activa; permitido en week `open|closed` |
| `Session.manual_update` | `session` | `campaign`, `entry`, `session` | `simple` | corrección manual | `activa` | `#37`, glosario | corrige timestamps; `null <-> valor`; sin reparenting |
| `Session.manual_delete` | `session` | `campaign`, `entry`, `session` | `simple` | corrección manual | `activa` | `#37`, glosario | hard delete; permitido en week `open|closed` |
| `ResourceChange.create` | `resource_change` | `resource_change`, `campaign` | `compuesta` | registro manual de recursos | `activa` | `#8`, glosario | valida no-negatividad final |
| `ResourceChange.update` | `resource_change` | `resource_change`, `campaign` | `compuesta` | corrección manual | `activa` | `#8`, glosario | valida no-negatividad final |
| `ResourceChange.delete` | `resource_change` | `resource_change`, `campaign` | `compuesta` | corrección manual | `activa` | `#8`, glosario | valida consistencia de totales tras eliminación |

## Contrato por operación

| operation_id | precondiciones_dominio | precondiciones_conflicto | validaciones | postcondiciones | rechazos_esperados | categoria_rechazo | atomicidad_esperada_comportamiento | respuesta_cliente_recomendada | notas_de_implementación |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Campaign.provision_initial_years` | campaña existe y está provisionable | base de campaña no obsoleta | crea 4 años; `summer->winter`; 10 semanas/estación; no duplicados (`year/season/week`) | estructura temporal inicial completa; `week_cursor` apunta a primera week abierta | duplicados, base obsoleta | `validacion` / `conflicto` | todo el bloque temporal se crea o falla completo | `refrescar + reintentar` si conflicto; error local si duplicado/estado inválido | no fija técnica Firestore |
| `Campaign.extend_years_plus_one` | campaña ya provisionada; último año identificable | base de campaña/estructura temporal no obsoleta | crea exactamente 1 año; continuidad `year_number` y `week_number`; no duplicados | nuevo año completo añadido; `week_cursor` derivado válido | duplicados; continuidad inválida; base obsoleta | `validacion` / `conflicto` | se añade el año completo o falla completo | `refrescar + reintentar` si conflicto; error local si estructura inválida | disparo UI desde `+` de año |
| `Week.close` | week existe; transición `open -> closed`; week abierta provisionada no quedará en 0 tras operación | base de `week.status` y sesión activa relevante no obsoletas | si hay sesión activa en la week, ejecutar `Session.auto_stop`; validar recálculo de `week_cursor` | week queda `closed`; sesión activa de esa week queda cerrada si existía; `week_cursor` recalculado | transición ya cerrada; dejaría 0 weeks abiertas; base obsoleta | `transicion_invalida` / `validacion` / `conflicto` | auto-stop + cierre + recálculo se consideran una sola operación lógica | error local (transición/validación); `refrescar + reintentar` si conflicto | `closed` no bloquea mutaciones por sí mismo |
| `Week.reopen` | week existe; transición `closed -> open` | base de `week.status` no obsoleta | transición válida; recálculo de `week_cursor` | week queda `open`; `week_cursor` recalculado | transición ya abierta; base obsoleta | `transicion_invalida` / `conflicto` | cambio de estado + recálculo como operación lógica única | error local si transición inválida; `refrescar + reintentar` si conflicto | corrección manual explícita |
| `Week.reclose` | week existe; transición `open -> closed`; no dejar 0 weeks abiertas | base de `week.status` y sesión activa relevante no obsoletas | si hay sesión activa en la week, `auto-stop`; validar recálculo de cursor | week queda `closed`; cursor derivado válido | transición ya cerrada; dejaría 0 weeks abiertas; base obsoleta | `transicion_invalida` / `validacion` / `conflicto` | auto-stop + cambio de estado + recálculo como operación lógica única | error local (transición/validación); `refrescar + reintentar` si conflicto | corrección manual de estado |
| `Week.update_notes` | week existe | base de `updated_at_utc`/versión no obsoleta | edición de texto válida; permitido en `open|closed` | `notes` actualizadas | base obsoleta; payload inválido | `conflicto` / `validacion` | una actualización simple | `refrescar + reingresar cambios` si conflicto; error local si payload inválido | sin LWW |
| `Entry.create` | week existe; ownership por ruta válido | base de orden (`entries` de la week) no obsoleta para inserción | `Entry.type` válido; `scenario_ref` obligatorio si `scenario`; si secuencia `order_index` inconsistente, auto-normalizar denso `1..N` antes/asociado a inserción | nueva entry creada con `order_index` válido y secuencia consistente | payload inválido; week inexistente; base obsoleta no resoluble | `validacion` / `conflicto` | normalización de orden + creación forman operación lógica única | error local si payload inválido; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
| `Entry.update` | entry existe | base de entry no obsoleta | edición amplia de campos funcionales; `scenario_ref` consistente; no cambiar de `Week` | entry actualizada en la misma week | payload inválido; intento de mover de week; base obsoleta | `validacion` / `conflicto` | actualización simple | error local si validación; `refrescar + reintentar` si conflicto | sin reparenting |
| `Entry.delete` | entry existe | base de entry e hijos relevantes no obsoletas | hard delete; si entry activa, `auto-stop`; borrado en cascada de `sessions` y `resource_changes` | entry y descendientes eliminados; no queda sesión activa asociada a esa entry | entry ya borrada; base obsoleta; cascada inválida por conflicto | `transicion_invalida` / `conflicto` | auto-stop + cascada + borrado se tratan como operación lógica única | error local si ya no existe; `refrescar + reintentar` si conflicto | hard delete real (sin soft delete funcional) |
| `Entry.reorder_within_week` | entry existe y pertenece a la week objetivo; misma week | base del orden de la week no obsoleta | posición destino válida; resecuencia densa `1..N`; no mover entre weeks | orden de entries de la week queda consistente | entry inexistente; week inconsistente; base obsoleta | `validacion` / `conflicto` | mover + resecuencia como operación lógica única | error local si validación; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
| `Session.start` | entry existe; sesión activa global puede ser 0..1; week `open|closed` permitida | base de sesión activa global no obsoleta | si ya hay sesión activa, `auto-stop` previo; garantizar unicidad `0..1` activa | nueva sesión activa (o transición equivalente) creada; unicidad preservada | unicidad violada; entry inválida; base obsoleta | `validacion` / `conflicto` | `auto-stop + start` (si aplica) como operación lógica única | error local si validación; `refrescar + reintentar` si conflicto | actividad derivada por `ended_at_utc=null` |
| `Session.stop` | sesión objetivo existe y está activa (`ended_at_utc=null`) | base de sesión no obsoleta | sesión sigue activa al momento de aplicar stop | sesión queda cerrada (`ended_at_utc` definido) | sesión ya cerrada/no activa; base obsoleta | `transicion_invalida` / `conflicto` | actualización simple | error local si transición inválida; `refrescar + reintentar` si conflicto | distingue conflicto de transición inválida |
| `Session.auto_stop` | sesión activa previa existe | base de sesión activa no obsoleta | trigger válido (`start`, `Week.close/reclose`, `Entry.delete`) | sesión activa previa queda cerrada | sesión ya no activa; base obsoleta | `transicion_invalida` / `conflicto` | se evalúa dentro de la operación compuesta disparadora | heredada de la operación padre | no se expone como acción manual principal |
| `Session.manual_create` | entry existe; ownership por ruta válido | base de sesión activa global no obsoleta si crea una activa | timestamps válidos; histórica o activa; unicidad `0..1` activa global | sesión manual creada | timestamps inválidos; unicidad violada; base obsoleta | `validacion` / `conflicto` | creación simple | error local si validación; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
| `Session.manual_update` | sesión existe; ownership por ruta inmutable | base de la sesión y de unicidad global no obsoletas | corrige `started_at_utc`/`ended_at_utc`; permite `null <-> valor`; sin reparenting; unicidad de activa global | sesión corregida; unicidad preservada | timestamps inválidos; reparenting intentado; unicidad violada; base obsoleta | `validacion` / `conflicto` | actualización simple | error local si validación; `refrescar + reintentar` si conflicto | no existe campo `state` separado |
| `Session.manual_delete` | sesión existe | base de sesión no obsoleta | hard delete; preservar `0..1` activa global | sesión eliminada | sesión ya borrada; base obsoleta | `transicion_invalida` / `conflicto` | borrado simple | error local si transición inválida; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
| `ResourceChange.create` | entry existe; ownership por ruta válido | base de `resource_totals` / log relevante no obsoleta | `resource_key` válido; `delta != 0`; totales finales no negativos | cambio creado; totales resultantes válidos | payload inválido; totales negativos; base obsoleta | `validacion` / `conflicto` | cálculo + creación como operación lógica única | error local si validación; `refrescar + reintentar` si conflicto | permitido en week `open|closed` |
| `ResourceChange.update` | change existe | base de change y totales relevantes no obsoletas | payload válido; totales finales no negativos | change actualizado; totales resultantes válidos | change inexistente/alterado; totales negativos; base obsoleta | `transicion_invalida` / `validacion` / `conflicto` | cálculo + actualización como operación lógica única | error local si validación/transición; `refrescar + reintentar` si conflicto | sin LWW |
| `ResourceChange.delete` | change existe | base de change y totales relevantes no obsoletas | recálculo mantiene totales no negativos | change eliminado; totales resultantes válidos | change ya borrado; totales inválidos; base obsoleta | `transicion_invalida` / `validacion` / `conflicto` | cálculo + borrado como operación lógica única | error local si validación/transición; `refrescar + reintentar` si conflicto | hard delete real |

## Operaciones compuestas y atomicidad esperada (comportamiento)

Este documento exige atomicidad a nivel de **resultado observable** (éxito
completo o fallo completo), sin fijar si la implementación usa transacción,
batch o combinación de mecanismos Firestore.

Operaciones compuestas mínimas:

1. `Session.start` con `auto-stop` previo cuando ya existe sesión activa.
1. `Week.close` / `Week.reclose` con `auto-stop` + recálculo de `week_cursor`.
1. `Entry.delete` activa con `auto-stop` + cascada (`sessions`,
   `resource_changes`).
1. `Entry.create` con auto-normalización de `order_index` cuando la secuencia de
   la week llega inconsistente.
1. `Campaign.provision_initial_years` y `Campaign.extend_years_plus_one` con
   estructura temporal completa + cursor derivado válido.

## Alineación temporal con #13

| operacion | insumo_#13 | insumo_#37 | regla_en_#12 | no_definido_en_#12 | riesgo_si_se_viola |
| --- | --- | --- | --- | --- | --- |
| `Campaign.provision_initial_years` | 4 años iniciales, `summer->winter`, 10 semanas/estación, `week_number` correlativo | cursor derivado; no dejar 0 abiertas | creación completa con duplicados rechazados y cursor derivado válido | técnica Firestore | estructura temporal inconsistente / cursor inválido |
| `Campaign.extend_years_plus_one` | +1 año, continuidad `year_number`/`week_number` | cursor derivado | extensión exacta de 1 año; sin reprovisión; sin duplicados | técnica Firestore | numeración rota o duplicados |
| `Week.close/reopen/reclose` | coherencia `week_number`/jerarquía | recálculo de cursor; transición manual | cambio de estado + postcondición de `week_cursor` | timestamp/desempate | cursor incoherente o estado inválido |
| `Entry`/`Session`/`ResourceChange` sobre weeks históricas | weeks siguen existiendo y `week_number` no cambia | editabilidad amplia en `open|closed` | operaciones permitidas en weeks `closed` salvo validación específica | política UI | bloqueos artificiales o contradicción con `#37` |

## Alineación de editabilidad e invariantes con #37

1. `Campaign.set_week_cursor_manual` se documenta como exclusión activa del MVP.
1. `week_cursor` es derivado (postcondición) y nunca selección manual libre.
1. `Week.status=closed` es marcador informativo; no bloquea por sí mismo
   mutaciones de `Entry`, `Session` o `ResourceChange`.
1. `Entry.reorder_within_week` está limitado a la misma `Week` y resecuencia
   densa `1..N`.
1. `Session.manual_update` no cambia ownership por ruta y puede corregir
   `ended_at_utc` en ambos sentidos.
1. Debe preservarse `0..1` sesión activa global.
1. Debe preservarse la existencia de al menos una `Week` abierta provisionada.

## Rechazos por conflicto, validación y transición inválida

### `conflicto`

- La base relevante cambió concurrentemente respecto a la lectura del cliente.
- Respuesta cliente recomendada: `refrescar + reintentar`.

### `validacion`

- La entrada o el resultado violan invariantes (por ejemplo, `scenario_ref`
  ausente, totales negativos, dejar 0 weeks abiertas, posición inválida).
- Respuesta cliente recomendada: error local y corrección de la acción/entrada.

### `transicion_invalida`

- La entidad ya no está en el estado requerido para la transición pedida (por
  ejemplo, `Week.close` sobre `closed`, `Session.stop` sobre sesión no activa).
- Respuesta cliente recomendada: error local (sin refresh por defecto), salvo
  que la UI detecte otros indicios de estado obsoleto.

## Casos de aceptación / verificación documental

1. `Campaign.extend_years_plus_one` crea exactamente 1 año y mantiene
   continuidad temporal de `#13`.
1. `Week.close` con sesión activa define `auto-stop + cerrar` y recálculo de
   `week_cursor` como operación compuesta.
1. `Week.close` sobre week ya `closed` se clasifica como `transicion_invalida`
   con error local.
1. `Week.reclose` rechaza operaciones que dejen `0` weeks abiertas.
1. `Session.start` queda permitido en week `open` o `closed`.
1. `Session.stop` inválido se clasifica como `transicion_invalida`.
1. `Session.manual_update` permite `ended_at_utc: valor -> null` y `null -> valor`
   preservando unicidad de sesión activa global.
1. `Session.manual_update` no permite reparenting.
1. `Entry.create` auto-normaliza `order_index` cuando detecta secuencia
   inconsistente.
1. `Entry.reorder_within_week` funciona también en weeks `closed` y resecuencia
   a `1..N`.
1. `Campaign.set_week_cursor_manual` aparece como exclusión activa del contrato
   MVP.

## Riesgos, límites y decisiones diferidas

- La técnica exacta para garantizar atomicidad en Firestore queda diferida a la
  implementación.
- La política de timestamps y desempate estable sigue diferida a `#18`.
- El contrato no define lecturas ni consultas (`#16`).
- La UX exacta para errores de conflicto vs transición inválida se concreta en
  issues de flujo (`#14`) y UI.

## Referencias

- `docs/domain-glossary.md`
- `docs/sync-strategy.md`
- `docs/conflict-policy.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/editability-policy.md`
- `docs/decision-log.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
