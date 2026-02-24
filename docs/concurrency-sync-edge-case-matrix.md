# Matriz de Edge Cases de Concurrencia y Sincronización (MVP)

## Metadatos

- `doc_id`: DOC-CONCURRENCY-SYNC-EDGE-CASE-MATRIX
- `purpose`: Definir una matriz oficial de edge cases de concurrencia/sincronización del MVP (incluyendo errores locales del mismo flujo operativo) para priorizar verificación y alimentar `#19` / `#20`.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar una matriz documental de edge cases que traduzca los contratos y flujos
oficiales del MVP (`#7`, `#8`, `#12`, `#14`, `#15`, `#16`, `#18`, `#37`, `#40`)
a escenarios verificables con clasificación, recuperación esperada y prioridad.

## Alcance y no alcance

Incluye:

- edge cases de concurrencia y sincronización del MVP;
- `transicion_invalida` / `validacion` cuando forman parte del mismo flujo
  operativo que un caso de concurrencia;
- operaciones compuestas con side-effects (`auto-stop`, recálculo de
  `week_cursor`, recálculo de recursos);
- lecturas críticas ligadas a consistencia visible (`#16` + `#18`);
- severidad, impacto y prioridad de verificación (`P0/P1/P2`);
- subset crítico mínimo para `#19` y `#20`.

No incluye:

- plan de pruebas paso a paso (`#19`);
- scripts, harnesses o fixtures de test;
- implementación de pruebas en código;
- edge cases puramente visuales/UI sin impacto de sincronización/consistencia;
- reapertura de decisiones de dominio ya cerradas.

## Entradas y prerrequisitos

- `docs/sync-strategy.md` (Issue `#7`)
- `docs/conflict-policy.md` (Issue `#8`)
- `docs/firestore-operation-contract.md` (Issue `#12`)
- `docs/active-session-flow.md` (Issue `#14`)
- `docs/resource-validation-recalculation.md` (Issue `#15`)
- `docs/minimal-read-queries.md` (Issue `#16`)
- `docs/timestamp-order-policy.md` (Issue `#18`)
- `docs/editability-policy.md` (Issue `#37`)
- `docs/resource-delta-model.md` (Issue `#40`)
- `docs/domain-glossary.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`

## Marco operativo del MVP (`single writer` / `online-only` / `on-demand refresh`)

1. El MVP opera con `single writer` como modo esperado (`#7`), pero `#17`
   documenta edge cases igualmente porque:
   - pueden ocurrir escrituras desde otro dispositivo;
   - puede existir estado local obsoleto;
   - los side-effects compuestos requieren expectativas explícitas.
1. Las escrituras son `online-only` (`#7`).
1. No hay listeners realtime; la reconciliación visible depende de
   `on-demand refresh` (`#7`, `#16`).
1. La política de conflictos es estricta (`#8`): rechazo + `refrescar` +
   `reintentar`.
1. La matriz no redefine contratos; los traduce a escenarios verificables.

## Taxonomía de edge cases (familias y criterios)

### Criterios de inclusión

1. El caso afecta invariantes, consistencia visible, recuperación de usuario o
   integridad de datos del MVP.
1. El caso tiene expectativa verificable derivable de docs oficiales.
1. Si el caso es solo UI/visual y no afecta sincronización/consistencia, queda
   fuera de `#17` (pasa a `#19` o a diseño/UI).

### Tabla 1 — Taxonomía de casos (`I17-S1`)

| `family_id` | `familia` | `descripcion` | `fuentes_principales` | `incluye_categorias_rechazo` | `notas` |
| --- | --- | --- | --- | --- | --- |
| `session_flow` | Flujo de sesiones y sesión activa global | Casos de `Session.*`, unicidad `0..1` activa global y side-effects `auto-stop` | `#12`, `#14`, `#8` | `conflicto`, `transicion_invalida`, `validacion` | Incluye coexistencia con `Session.manual_*` |
| `week_state_cursor` | Estado de week + `week_cursor` | Transiciones `Week.close/reopen/reclose`, cursor derivado y límite de weeks abiertas | `#12`, `#37`, `#9`, `#13`, `#8` | `conflicto`, `transicion_invalida`, `validacion` | `closed` no bloquea mutaciones por sí mismo |
| `entry_lifecycle_order` | Ciclo de vida y orden de entries | `Entry.create/update/delete/reorder` y consistencia de `order_index` | `#12`, `#14`, `#18` | `conflicto`, `transicion_invalida`, `validacion` | Incluye auto-normalización de orden |
| `resource_totals_deltas` | Recursos por `Entry` + totales campaña | `Entry.adjust/set/clear_resource_delta` y recálculo/validación de totales | `#15`, `#12`, `#40`, `#8` | `conflicto`, `transicion_invalida`, `validacion` | `drift` => `conflicto`; no-ops idempotentes documentados |
| `temporal_provision_extension` | Provisión/extensión temporal | `Campaign.provision_initial_years` y `extend_years_plus_one` con estructura/cursor derivados | `#12`, `#13`, `#37`, `#8` | `conflicto`, `validacion` | Sin reabrir mecánica técnica Firestore |
| `critical_reads_refresh_order` | Lecturas críticas / refresh / orden | Casos de `#16` + `#18` que afectan consistencia visible bajo refresh manual | `#16`, `#18`, `#14`, `#7` | `conflicto`, `validacion` (poco frecuente), `mixta` | Solo lecturas críticas; no UX genérica |

## Matriz principal de escenarios canónicos

### Convenciones

1. `categoria_esperada = mixta` se usa solo cuando el escenario base agrupa
   variantes cuya clasificación final depende de la operación exacta.
1. `recuperacion_esperada` reutiliza la semántica de `#8`, `#12`, `#14`, `#15`.
1. `docs_referencia` enumera las fuentes mínimas para validar el escenario.

### Tabla 2 — Matriz principal (escenarios canónicos) (`I17-S2A`)

| `edge_case_id` | `family_id` | `escenario_canonico` | `precondicion_resumida` | `trigger` | `sintoma_observable` | `resultado_esperado` | `categoria_esperada` | `recuperacion_esperada` | `severidad` | `impacto` | `prioridad_verificacion` | `docs_referencia` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `EC-SESSION-01` | `session_flow` | `start` con base obsoleta y posible `auto-stop + start` en conflicto | Existe sesión activa previa o estado leído obsoleto | `Session.start` | Error al iniciar / activa final distinta de la esperada | Rechazo por conflicto; no doble activa; sin estado parcial confirmado por cliente | `conflicto` | `refresh` manual + reintentar | `critical` | invariante de sesión activa global | `P0` | `#12`, `#14`, `#8` | Operación compuesta |
| `EC-SESSION-02` | `session_flow` | `stop` sobre sesión cambiada concurrentemente | Sesión parecía activa al cliente | `Session.stop` | Stop falla porque la base ya cambió | Rechazo por conflicto; no asumir cierre local como definitivo | `conflicto` | `refresh` manual + reintentar | `high` | flujo principal de sesión | `P1` | `#12`, `#14`, `#8` | Distinguir de sesión ya cerrada |
| `EC-SESSION-03` | `session_flow` | `start` sobre entry ya activa | `selected_entry` coincide con `active_entry` | `ui.session_start_on_selected_entry` / `Session.start` | Usuario pulsa `Iniciar` sobre entry ya activa | Error local; no crea nueva sesión; no `auto-stop` | `transicion_invalida` | error local (sin refresh por defecto) | `medium` | flujo principal de sesión | `P1` | `#14`, `#12` | Caso de UX/flujo crítico |
| `EC-SESSION-04` | `session_flow` | `stop` sobre sesión ya no activa | UI desfasada o acción repetida | `ui.session_stop_on_selected_entry` / `Session.stop` | `Stop` no aplica a la sesión actual | Error local; estado activo no cambia | `transicion_invalida` | error local (refresh opcional si sospecha obsolescencia) | `medium` | flujo principal de sesión | `P2` | `#14`, `#12`, `#8` | Sin auto-refresh |
| `EC-SESSION-05` | `session_flow` | `Session.manual_update` rompe unicidad de activa global | Corrección manual sobre timestamps puede convertir sesión a activa | `Session.manual_update` | Riesgo de >1 sesión activa global | Operación rechazada o conflicto según base; unicidad preservada | `mixta` | error local si validación; `refresh + retry` si conflicto | `high` | invariante de sesión activa global | `P1` | `#12`, `#37`, `#14`, `#8` | Clasificación final por variante |
| `EC-SESSION-06` | `session_flow` | `Entry.delete` activa / `Week.close\|reclose` con `auto-stop` embebido en conflicto compuesto | Sesión activa en la entry/week afectada | `Entry.delete` / `Week.close` / `Week.reclose` | Operación compuesta falla o queda en estado ambiguo al usuario | Rechazo de la operación compuesta; no dejar estado parcial asumido por cliente | `conflicto` | `refresh` manual + reintentar operación padre | `critical` | invariante + flujo principal + recuperación | `P0` | `#12`, `#14`, `#8` | Compuesto con side-effects |
| `EC-WEEK-01` | `week_state_cursor` | Transición inválida de `Week` | Estado real no coincide con transición solicitada | `Week.close` / `Week.reopen` / `Week.reclose` | Acción sobre week ya en ese estado / no aplicable | Error local por transición inválida; no `refresh` por defecto | `transicion_invalida` | error local | `medium` | flujo temporal y estado | `P1` | `#12`, `#8`, `#14` | Distinguir de conflicto |
| `EC-WEEK-02` | `week_state_cursor` | Conflicto en cambio de estado de week con recálculo de `week_cursor` | Week/cursor leídos obsoletos | `Week.close` / `Week.reopen` / `Week.reclose` | Acción de week falla por base obsoleta; marcador `current week` puede quedar viejo | Rechazo por conflicto; `week_cursor` visible se corrige tras refresh | `conflicto` | `refresh` manual + reintentar | `critical` | temporal + consistencia visible | `P0` | `#12`, `#37`, `#9`, `#14`, `#8` | Incluye recálculo derivado de cursor |
| `EC-WEEK-03` | `week_state_cursor` | Cierre/recierre dejaría `0` weeks abiertas | Week objetivo es la última abierta | `Week.close` / `Week.reclose` | Acción rechazada aunque la week exista y transición parezca válida | Validación rechaza; invariante de weeks abiertas preservada | `validacion` | error local; corregir acción | `critical` | invariante temporal | `P0` | `#12`, `#37`, `#13` | Bloquea comportamiento inválido del cursor |
| `EC-ENTRY-01` | `entry_lifecycle_order` | `reorder` con base de orden obsoleta | Orden de entries cambió concurrentemente | `Entry.reorder_within_week` | Reordenación falla / orden visible desfasado | Rechazo por conflicto; orden se restablece tras refresh | `conflicto` | `refresh` manual + reintentar | `high` | consistencia visual + flujo principal | `P1` | `#12`, `#18`, `#8` | Resecuencia densa `1..N` |
| `EC-ENTRY-02` | `entry_lifecycle_order` | `Entry.update/delete` sobre entry obsoleta o ya borrada | Cliente opera sobre entry ya modificada/eliminada | `Entry.update` / `Entry.delete` | Acción falla; tabs/panel pueden quedar desfasados | Conflicto o transición inválida según caso; no estado parcial | `mixta` | error local (`not found`) o `refresh + retry` (conflicto) | `high` | flujo principal + consistencia visible | `P1` | `#12`, `#14`, `#16`, `#8` | Clasificación final por variante |
| `EC-ENTRY-03` | `entry_lifecycle_order` | Secuencia inconsistente de `order_index` y auto-normalización | Secuencia previa con huecos/duplicados | `Entry.create` (y/o inserción con normalización) | Orden previo inconsistente detectado | Se auto-normaliza la secuencia y la operación puede continuar sin error | `validacion` | no aplica; comportamiento controlado | `low` | orden de entries / robustez | `P2` | `#12` | Edge local controlado (no fallo) |
| `EC-RESOURCE-01` | `resource_totals_deltas` | Total final negativo | Delta propuesto haría `campaign_after < 0` | `Entry.adjust/set/clear_resource_delta` | Operación rechazada por total inválido | Validación rechaza; totales no negativos preservados | `validacion` | error local; corregir delta | `high` | integridad de totales de recursos | `P1` | `#15`, `#12` | `clear` puede revelar drift si base mala |
| `EC-RESOURCE-02` | `resource_totals_deltas` | Base obsoleta en deltas/totales | `Entry` o `campaign.resource_totals` cambió | `Entry.adjust/set/clear_resource_delta` | Error al persistir ajuste de recursos | Rechazo por conflicto; no aplicar delta sobre base obsoleta | `conflicto` | `refresh` manual + reintentar | `critical` | integridad de datos/recursos | `P0` | `#15`, `#12`, `#8`, `#40` | Caso central de concurrencia en recursos |
| `EC-RESOURCE-03` | `resource_totals_deltas` | Drift/inconsistencia detectada de totales | Cálculo local detecta preestado imposible | Cualquier operación de recursos (o `Entry.delete` con impacto recursos) | Estado de recursos no cuadra con deltas/totales | Clasificar como conflicto y forzar refresh; escalar si persiste | `conflicto` | `refresh` y reintentar; escalar si persiste | `critical` | integridad de datos/recursos | `P0` | `#15`, `#8`, `#12` | Decisión explícita: drift => conflicto |
| `EC-RESOURCE-04` | `resource_totals_deltas` | No-ops idempotentes sin error | `adjust=0`, `set` mismo valor, `clear` inexistente | `Entry.adjust/set/clear_resource_delta` | Acción no cambia estado pero puede ejecutarse | No error; estado final permanece igual; contrato idempotente | `validacion` | no aplica; seguir flujo normal | `low` | robustez / UX tolerante | `P2` | `#15`, `#12`, `#40` | `clear` inexistente es idempotente |
| `EC-TEMPORAL-01` | `temporal_provision_extension` | `extend_years_plus_one` con base obsoleta/duplicado | Estructura temporal cambió / año ya existe | `Campaign.extend_years_plus_one` | Extensión falla por base obsoleta o duplicados | Rechazo por conflicto o validación; no crear año parcial | `mixta` | error local (duplicado/estructura) o `refresh + retry` (conflicto) | `critical` | temporal + integridad estructural | `P0` | `#12`, `#13`, `#37`, `#8` | Año completo o fallo completo |
| `EC-TEMPORAL-02` | `temporal_provision_extension` | Provisión inicial/reprovisión parcial inválida | Duplicados o continuidad `week_number` rota | `Campaign.provision_initial_years` | Falla la provisión inicial / reprovisión accidental | Rechazo por validación o conflicto; no estructura temporal parcial | `mixta` | error local o `refresh + retry` según base | `high` | temporal + integridad estructural | `P1` | `#12`, `#13`, `#8` | Incluye idempotencia/rechazo de reprovisión |
| `EC-READ-01` | `critical_reads_refresh_order` | `ui.manual_refresh` reconcilia conflicto y normaliza estado visible | Estado visible potencialmente obsoleto tras error | `ui.manual_refresh` | UI desincronizada tras conflicto | Refresco on-demand recarga queries visibles y restablece consistencia | `conflicto` | `refresh` manual (acción del usuario) | `critical` | recuperación MVP | `P0` | `#7`, `#16`, `#14`, `#18` | Sin realtime listeners |
| `EC-READ-02` | `critical_reads_refresh_order` | `Q8` con `serverTimestamp` pendiente produce orden provisional | Sesiones recién escritas con timestamps pendientes | `Q8 sessions_selected_entry_combined` | Orden temporalmente provisional en lista de sesiones | Orden final solo garantizado tras `refresh`; no prometer estabilidad antes | `validacion` | refresh manual cuando se requiera orden final | `medium` | consistencia visual / orden | `P1` | `#18`, `#16` | No es conflicto de escritura |
| `EC-READ-03` | `critical_reads_refresh_order` | Activo global en otra entry (`Q6+Q7`) vs selección/foco | Existe sesión activa global y `selected_entry != active_entry` | `Q6` + `Q7` + estado UI (`#14`) | UI puede mostrar foco y activo distintos | UI distingue foco vs activo; label del activo se resuelve vía Q7 si aplica | `conflicto` | refresh manual si Q6/Q7 quedan obsoletos | `critical` | consistencia visual de foco vs activo | `P0` | `#14`, `#16`, `#18` | Caso crítico de lectura + flujo |
| `EC-READ-04` | `critical_reads_refresh_order` | Arranque sin selección + cargas diferidas correctas | Apertura de pantalla principal sin selección | `open_main_screen` | Carga excesiva o carga prematura de queries de entry | Cargar solo Q1/Q2/Q3/Q4/Q6; no Q5/Q7/Q8 hasta selección | `validacion` | corregir trigger/carga; no requiere refresh | `medium` | coste/latencia y consistencia de arranque | `P1` | `#16`, `#9`, `#14`, `#7` | Caso de lecturas mínimas correctas |
| `EC-READ-05` | `critical_reads_refresh_order` | Cambio de año / merge `Q3+Q4` mantiene orden de weeks | Cambio de año o refresh del año visible | `ui.select_year` / refresh Q3+Q4 | Weeks mezcladas fuera de orden canónico | Merge cliente conserva orden por `week_number ASC` | `validacion` | corregir orden local / refresh si base obsoleta | `medium` | consistencia visual temporal | `P1` | `#16`, `#18`, `#13` | `summer+winter` se ordenan por `week_number` |

## Variantes por familia y operación (capa 2)

### Regla de uso

1. Esta tabla evita multiplicar filas canónicas.
1. Cada operación/evento obligatorio aparece al menos una vez.
1. Si no aporta edge case nuevo, se marca “sin variante crítica adicional” y se
   referencia el escenario canónico más cercano.

### Tabla 3 — Variantes por operación (capa 2) (`I17-S2B`)

| `variant_id` | `operation_or_event` | `edge_case_id_base` | `delta_especifico` | `clasificacion_final_esperada` | `recuperacion_final` | `notas` |
| --- | --- | --- | --- | --- | --- | --- |
| `V-001` | `Campaign.provision_initial_years` | `EC-TEMPORAL-02` | Duplicados/continuidad inválida al reprovisionar o base obsoleta | `validacion` / `conflicto` | error local o `refresh + retry` | Crear 4 años o fallar completo |
| `V-002` | `Campaign.extend_years_plus_one` | `EC-TEMPORAL-01` | Duplicado de año / base obsoleta / continuidad inválida | `validacion` / `conflicto` | error local o `refresh + retry` | Caso P0 |
| `V-003` | `Week.close` | `EC-WEEK-02` | Puede incluir `auto-stop` embebido + recálculo de cursor | `conflicto` / `transicion_invalida` / `validacion` | error local o `refresh + retry` | Ver `EC-WEEK-03` y `EC-SESSION-06` |
| `V-004` | `Week.reopen` | `EC-WEEK-01` | Transición `closed -> open`; cursor derivado | `transicion_invalida` / `conflicto` | error local o `refresh + retry` | Sin caso de `0 weeks abiertas` |
| `V-005` | `Week.reclose` | `EC-WEEK-03` | Puede disparar `auto-stop` y validar `0 weeks abiertas` | `validacion` / `transicion_invalida` / `conflicto` | error local o `refresh + retry` | Compuesto cuando hay activa |
| `V-006` | `Week.update_notes` | `EC-WEEK-02` | No cambia estado/cursor, pero puede fallar por base obsoleta | `conflicto` / `validacion` | error local o `refresh + reingresar cambios` | Sin LWW |
| `V-007` | `Entry.create` | `EC-ENTRY-03` | Auto-normalización de `order_index` y posible conflicto de base | `validacion` / `conflicto` | no-op/normalización o `refresh + retry` | Edge local controlado + conflicto posible |
| `V-008` | `Entry.update` | `EC-ENTRY-02` | Entry obsoleta / intento inválido (ej. mover de week) | `conflicto` / `validacion` | error local o `refresh + retry` | `transicion_invalida` suele aplicar más a delete |
| `V-009` | `Entry.delete` | `EC-SESSION-06` | Si entry activa: `auto-stop` embebido; si ya no existe: not found | `conflicto` / `transicion_invalida` | error local o `refresh + retry` | También impacta recursos (`EC-RESOURCE-03`) |
| `V-010` | `Entry.reorder_within_week` | `EC-ENTRY-01` | Base de orden obsoleta o pertenencia incoherente | `conflicto` / `validacion` | error local o `refresh + retry` | Resecuencia densa `1..N` |
| `V-011` | `Entry.adjust_resource_delta` | `EC-RESOURCE-02` | Base obsoleta; no-op si `adjust=0`; total negativo | `conflicto` / `validacion` | error local o `refresh + retry` | Ver `EC-RESOURCE-04` |
| `V-012` | `Entry.set_resource_delta` | `EC-RESOURCE-02` | Base obsoleta; set mismo valor (no-op); total negativo | `conflicto` / `validacion` | error local o `refresh + retry` | Ver `EC-RESOURCE-04` |
| `V-013` | `Entry.clear_resource_delta` | `EC-RESOURCE-03` | Drift detectado o clave inexistente idempotente | `conflicto` / `validacion` | `refresh + retry` o no-op | `clear` inexistente sin error |
| `V-014` | `Session.start` | `EC-SESSION-01` | Puede derivar a `EC-SESSION-03` si entry ya activa | `conflicto` / `transicion_invalida` / `validacion` | error local o `refresh + retry` | Compuesto si había activa previa |
| `V-015` | `Session.stop` | `EC-SESSION-02` | Si ya no activa -> `EC-SESSION-04` | `conflicto` / `transicion_invalida` | error local o `refresh + retry` | Distinguir conflicto de acción repetida |
| `V-016` | `Session.auto_stop` | `EC-SESSION-06` | Side-effect heredado del padre (`start`, `week close`, `entry delete`) | `conflicto` / `transicion_invalida` | heredada de la operación padre | No acción manual principal |
| `V-017` | `Session.manual_create` | `EC-SESSION-05` | Crear activa manual puede violar unicidad | `validacion` / `conflicto` | error local o `refresh + retry` | Weeks `open\|closed` permitidas |
| `V-018` | `Session.manual_update` | `EC-SESSION-05` | `ended_at_utc null <-> valor`; riesgo unicidad activa | `validacion` / `conflicto` | error local o `refresh + retry` | Sin reparenting |
| `V-019` | `Session.manual_delete` | `EC-ENTRY-02` | Sesión ya borrada vs base obsoleta | `transicion_invalida` / `conflicto` | error local o `refresh + retry` | Puede afectar lectura Q8 |
| `V-020` | `open_main_screen` | `EC-READ-04` | Arranque sin selección; cargas diferidas obligatorias | `validacion` | corregir triggers de carga | No es conflicto, sí edge de sync/coste |
| `V-021` | `ui.manual_refresh` | `EC-READ-01` | Reconciliación de estado visible tras error/conflicto | `conflicto` | `refresh` manual ejecutado por usuario | Núcleo del MVP sin realtime |
| `V-022` | `ui.select_year` | `EC-READ-05` | Merge Q3+Q4 por `week_number`; limpiar selección local | `validacion` / `conflicto` | corregir orden o `refresh` | Q5/Q8 no cargan hasta nueva selección |
| `V-023` | `ui.select_week` | `EC-READ-04` | No debe cargar sesiones (Q8) todavía | `validacion` | corregir triggers de lectura | Carga Q5 solamente |
| `V-024` | `ui.select_entry` | `EC-READ-03` | Carga Q8 y coexistencia con activa global en otra entry | `conflicto` / `validacion` | `refresh` si base obsoleta; si no, flujo normal | Foco vs activo |
| `V-025` | `Q6 active_session_global` | `EC-READ-03` | Activa global obsoleta / ausente / distinta de foco | `conflicto` | `refresh` manual | `ended_at_utc == null`, `limit 1` |
| `V-026` | `Q7 active_entry_doc_if_needed` | `EC-READ-03` | Label del activo externo no resoluble por doc obsoleto | `conflicto` / `validacion` | `refresh` manual; fallback de UI | Condicional |
| `V-027` | `Q8 sessions_selected_entry_combined` | `EC-READ-02` | Orden provisional por timestamps pendientes y activa primero | `validacion` / `conflicto` | `refresh` manual para orden final | Compatibilidad `#18` |

## Escala de severidad, impacto y prioridad

### `severidad` (4 niveles)

- `critical`: rompe invariantes centrales o puede ocultar corrupción/estado
  engañoso severo.
- `high`: comportamiento incorrecto relevante del flujo principal con alta
  fricción/riesgo.
- `medium`: inconsistencia recuperable con impacto acotado o caso menos
  frecuente.
- `low`: edge case controlado/no-op/recuperación clara con impacto menor.

### `impacto` (texto corto obligatorio)

Usar una línea breve y concreta, por ejemplo:

- `invariante de sesión activa global`
- `consistencia visual de foco vs activo`
- `integridad de totales de recursos`
- `temporal + cursor derivado`
- `recuperación on-demand refresh`

### `prioridad_verificacion`

- `P0`: crítico para MVP; debe aparecer en `#19`; su ausencia de cobertura
  bloquea `#20`.
- `P1`: importante antes del gate, pero no bloquea por sí solo si el conjunto
  crítico está cubierto.
- `P2`: cobertura recomendada / regresión posterior.

## Casos críticos mínimos a verificar en el MVP

### Regla de selección (`I17-S3`)

1. Incluir **todos los `P0`** de la matriz principal.
1. Si una familia no tiene `P0`, añadir al menos un `P1` representativo.
1. Mapear explícitamente cada caso crítico a `#19` como insumo de pruebas.

### Tabla 4 — Casos críticos MVP (`I17-S3`)

| `edge_case_id` | `motivo_criticidad` | `prioridad_verificacion` | `bloquea_#20` | `relacion_con_#19` | `notas` |
| --- | --- | --- | --- | --- | --- |
| `EC-SESSION-01` | Conflicto en `start` compuesto (`auto-stop + start`) con riesgo sobre unicidad de sesión activa | `P0` | Sí | Debe convertirse en caso de prueba de operación compuesta y recuperación | Flujo principal |
| `EC-SESSION-06` | Side-effects `auto-stop` embebidos en operaciones compuestas (`Entry.delete` / `Week.close\|reclose`) | `P0` | Sí | Requiere pruebas de conflicto en compuestos con efecto observable | Cruza `#12` y `#14` |
| `EC-WEEK-02` | Cambio de estado de week + recálculo de `week_cursor` bajo conflicto | `P0` | Sí | Caso de prueba de consistencia temporal y refresh | Afecta `current week` |
| `EC-WEEK-03` | Invariante crítica: no dejar `0` weeks abiertas | `P0` | Sí | Debe probarse como validación bloqueante | Temporal/cursor |
| `EC-RESOURCE-02` | Conflicto sobre deltas/totales de recursos con riesgo de pérdida de consistencia | `P0` | Sí | Caso de prueba de recursos con base obsoleta | `Entry.resource_deltas` + `campaign.resource_totals` |
| `EC-RESOURCE-03` | Drift/inconsistencia detectada y clasificación correcta como conflicto | `P0` | Sí | Caso de integridad y recuperación `refresh` | Si persiste tras refresh, escalar |
| `EC-TEMPORAL-01` | Extensión de año con duplicados/base obsoleta; riesgo estructural alto | `P0` | Sí | Caso de temporal estructural y atomicidad observable | `+1` año |
| `EC-READ-01` | `ui.manual_refresh` como mecanismo central de reconciliación MVP | `P0` | Sí | Caso de recuperación transversal post-conflicto | Sin realtime |
| `EC-READ-03` | Coherencia foco vs activo (Q6/Q7 + selección) en flujo principal | `P0` | Sí | Caso de consistencia visible cruzando `#14` + `#16` | Activo en otra entry |
| `EC-READ-02` | Orden provisional/final de sesiones con timestamps pendientes (`Q8`) | `P1` | No | Incluir como cobertura de orden estable en `#19` | Cubre `#18` en lecturas |
| `EC-ENTRY-01` | Reordenación con base de orden obsoleta | `P1` | No (si hay cobertura alternativa de flujo) | Caso de concurrencia de orden en entries | Recomendada antes de `#20` |
| `EC-ENTRY-02` | `Entry.update/delete` sobre entry obsoleta o inexistente | `P1` | No | Caso de clasificación conflicto vs transición inválida | Cobertura de lifecycle |

## Alineación con `#12`, `#14`, `#15`, `#16`, `#18`

### `#12` — Contrato de operaciones Firestore por agregado

1. `#17` no redefine pre/postcondiciones ni atomicidad de comportamiento.
1. `#17` traduce ese contrato a escenarios verificables (incluyendo compuestos).
1. La tabla de variantes referencia operaciones de `#12` como cobertura mínima.

### `#14` — Flujo de sesión activa y `auto-stop`

1. `#17` reutiliza el modelo de estados/errores del flujo (`conflicto`,
   `transicion_invalida`, `validacion`).
1. Los casos `session_flow` y `critical_reads_refresh_order` deben respetar la
   separación foco vs activo y la recuperación `refresh` manual + reintentar.

### `#15` — Validación y recálculo de recursos

1. `#17` reutiliza la clasificación de recursos:
   - total negativo => `validacion`
   - base obsoleta => `conflicto`
   - drift => `conflicto`
   - no-ops idempotentes => sin error
1. No se reabre el modelo de recursos de `#40`.

### `#16` — Consultas mínimas de pantalla principal

1. `#17` cubre solo lecturas críticas ligadas a sincronización/consistencia.
1. `#17` no reactiva `timeline_entries_flat`; se mantiene fuera del MVP actual.
1. `#17` usa Q1..Q8 y triggers de `#16` como base para los casos de lectura.

### `#18` — Timestamps y orden estable

1. `#17` no redefine tuplas canónicas de orden.
1. `#17` solo verifica edge cases derivados:
   - orden provisional por `serverTimestamp` pendiente;
   - estabilización tras refresh;
   - consistencia visible de listas críticas.

## Casos de aceptación / verificación documental

1. La matriz final incluye las 6 familias obligatorias y cubre sesiones,
   entries, recursos, temporal y lecturas críticas.
1. La matriz principal contiene al menos los 23 escenarios canónicos con IDs
   `EC-*` fijados.
1. Cada escenario tiene expectativa verificable, clasificación y recuperación
   esperada.
1. La tabla de variantes cubre todas las operaciones/eventos obligatorios.
1. El subset crítico incluye todos los `P0` y mapea insumos hacia `#19`.
1. `#17` no contradice `#12/#14/#15/#16/#18/#37/#40`.
1. `timeline_entries_flat` solo aparece, si se menciona, como no activado en el
   MVP actual de `#16`.

## Riesgos, límites y decisiones diferidas

- La matriz documenta escenarios y expectativas, pero no sustituye el diseño de
  pruebas detallado de `#19`.
- Algunas clasificaciones canónicas se marcan como `mixta` para evitar explotar
  filas; la clasificación final se cierra en la tabla de variantes.
- El comportamiento exacto de mensajes UI (toast/inline/modal) sigue fuera de
  alcance; aquí se fija recuperación, no diseño visual.
- Si el MVP amplía lecturas o reactiva `timeline_entries_flat`, `#17` deberá
  extender la familia `critical_reads_refresh_order`.

## Referencias

- `AGENTS.md`
- `docs/system-map.md`
- `docs/decision-log.md`
- `docs/domain-glossary.md`
- `docs/sync-strategy.md`
- `docs/conflict-policy.md`
- `docs/firestore-operation-contract.md`
- `docs/active-session-flow.md`
- `docs/resource-delta-model.md`
- `docs/resource-validation-recalculation.md`
- `docs/minimal-read-queries.md`
- `docs/timestamp-order-policy.md`
- `docs/editability-policy.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`
