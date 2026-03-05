# Matriz de Edge Cases de Concurrencia y SincronizaciÃ³n (MVP)

## Metadatos

- `doc_id`: DOC-CONCURRENCY-SYNC-EDGE-CASE-MATRIX
- `purpose`: Definir una matriz oficial de edge cases de concurrencia/sincronizaciÃ³n del MVP (incluyendo errores locales del mismo flujo operativo) para priorizar verificaciÃ³n y alimentar `#19` / `#20`.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-10

## Objetivo

Cerrar una matriz documental de edge cases que traduzca los contratos y flujos
oficiales del MVP (`#7`, `#8`, `#12`, `#14`, `#15`, `#16`, `#18`, `#37`, `#40`)
a escenarios verificables con clasificaciÃ³n, recuperaciÃ³n esperada y prioridad.

## Alcance y no alcance

Incluye:

- edge cases de concurrencia y sincronizaciÃ³n del MVP;
- `transicion_invalida` / `validacion` cuando forman parte del mismo flujo
  operativo que un caso de concurrencia;
- operaciones compuestas con side-effects (`auto-stop`, recÃ¡lculo de
  `week_cursor`, recÃ¡lculo de recursos);
- lecturas crÃ­ticas ligadas a consistencia visible (`#16` + `#18`);
- severidad, impacto y prioridad de verificaciÃ³n (`P0/P1/P2`);
- subset crÃ­tico mÃ­nimo para `#19` y `#20`.

No incluye:

- plan de pruebas paso a paso (`#19`);
- scripts, harnesses o fixtures de test;
- implementaciÃ³n de pruebas en cÃ³digo;
- edge cases puramente visuales/UI sin impacto de sincronizaciÃ³n/consistencia;
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
   - los side-effects compuestos requieren expectativas explÃ­citas.
1. Las escrituras son `online-only` (`#7`).
1. No hay listeners realtime; la reconciliaciÃ³n visible depende de
   `on-demand refresh` (`#7`, `#16`).
1. La polÃ­tica de conflictos es estricta (`#8`): rechazo + `refrescar` +
   `reintentar`.
1. La matriz no redefine contratos; los traduce a escenarios verificables.

## TaxonomÃ­a de edge cases (familias y criterios)

### Criterios de inclusiÃ³n

1. El caso afecta invariantes, consistencia visible, recuperaciÃ³n de usuario o
   integridad de datos del MVP.
1. El caso tiene expectativa verificable derivable de docs oficiales.
1. Si el caso es solo UI/visual y no afecta sincronizaciÃ³n/consistencia, queda
   fuera de `#17` (pasa a `#19` o a diseÃ±o/UI).

### Tabla 1 â€” TaxonomÃ­a de casos (`I17-S1`)

| `family_id` | `familia` | `descripcion` | `fuentes_principales` | `incluye_categorias_rechazo` | `notas` |
| --- | --- | --- | --- | --- | --- |
| `session_flow` | Flujo de sesiones y sesiÃ³n activa global | Casos de `Session.*`, unicidad `0..1` activa global y side-effects `auto-stop` | `#12`, `#14`, `#8` | `conflicto`, `transicion_invalida`, `validacion` | Incluye coexistencia con `Session.manual_*` |
| `week_state_cursor` | Estado de week + `week_cursor` | Transiciones `Week.close/reopen/reclose`, cursor derivado y lÃ­mite de weeks abiertas | `#12`, `#37`, `#9`, `#13`, `#8` | `conflicto`, `transicion_invalida`, `validacion` | `closed` no bloquea mutaciones por sÃ­ mismo |
| `entry_lifecycle_order` | Ciclo de vida y orden de entries | `Entry.create/update/delete/reorder` y consistencia de `order_index` | `#12`, `#14`, `#18` | `conflicto`, `transicion_invalida`, `validacion` | Incluye auto-normalizaciÃ³n de orden |
| `resource_totals_deltas` | Recursos por `Entry` + totales campaÃ±a | `Entry.adjust/set/clear_resource_delta` y recÃ¡lculo/validaciÃ³n de totales | `#15`, `#12`, `#40`, `#8` | `conflicto`, `transicion_invalida`, `validacion` | `drift` => `conflicto`; no-ops idempotentes documentados |
| `temporal_provision_extension` | ProvisiÃ³n/extensiÃ³n temporal | `Campaign.provision_initial_years` y `extend_years_plus_one` con estructura/cursor derivados | `#12`, `#13`, `#37`, `#8` | `conflicto`, `validacion` | Sin reabrir mecÃ¡nica tÃ©cnica Firestore |
| `critical_reads_refresh_order` | Lecturas crÃ­ticas / refresh / orden | Casos de `#16` + `#18` que afectan consistencia visible bajo refresh manual | `#16`, `#18`, `#14`, `#7` | `conflicto`, `validacion` (poco frecuente), `mixta` | Solo lecturas crÃ­ticas; no UX genÃ©rica |

## Matriz principal de escenarios canÃ³nicos

### Convenciones

1. `categoria_esperada = mixta` se usa solo cuando el escenario base agrupa
   variantes cuya clasificaciÃ³n final depende de la operaciÃ³n exacta.
1. `recuperacion_esperada` reutiliza la semÃ¡ntica de `#8`, `#12`, `#14`, `#15`.
1. `docs_referencia` enumera las fuentes mÃ­nimas para validar el escenario.

### Tabla 2 â€” Matriz principal (escenarios canÃ³nicos) (`I17-S2A`)

| `edge_case_id` | `family_id` | `escenario_canonico` | `precondicion_resumida` | `trigger` | `sintoma_observable` | `resultado_esperado` | `categoria_esperada` | `recuperacion_esperada` | `severidad` | `impacto` | `prioridad_verificacion` | `docs_referencia` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `EC-SESSION-01` | `session_flow` | `start` con base obsoleta y posible `auto-stop + start` en conflicto | Existe sesiÃ³n activa previa o estado leÃ­do obsoleto | `Session.start` | Error al iniciar / activa final distinta de la esperada | Rechazo por conflicto; no doble activa; sin estado parcial confirmado por cliente | `conflicto` | `refresh` manual + reintentar | `critical` | invariante de sesiÃ³n activa global | `P0` | `#12`, `#14`, `#8` | OperaciÃ³n compuesta |
| `EC-SESSION-02` | `session_flow` | `stop` sobre sesiÃ³n cambiada concurrentemente | SesiÃ³n parecÃ­a activa al cliente | `Session.stop` | Stop falla porque la base ya cambiÃ³ | Rechazo por conflicto; no asumir cierre local como definitivo | `conflicto` | `refresh` manual + reintentar | `high` | flujo principal de sesiÃ³n | `P1` | `#12`, `#14`, `#8` | Distinguir de sesiÃ³n ya cerrada |
| `EC-SESSION-03` | `session_flow` | `start` sobre entry ya activa | `selected_entry` coincide con `active_entry` | `ui.session_start_on_selected_entry` / `Session.start` | Usuario pulsa `Iniciar` sobre entry ya activa | Error local; no crea nueva sesiÃ³n; no `auto-stop` | `transicion_invalida` | error local (sin refresh por defecto) | `medium` | flujo principal de sesiÃ³n | `P1` | `#14`, `#12` | Caso de UX/flujo crÃ­tico |
| `EC-SESSION-04` | `session_flow` | `stop` sobre sesiÃ³n ya no activa | UI desfasada o acciÃ³n repetida | `ui.session_stop_on_selected_entry` / `Session.stop` | `Stop` no aplica a la sesiÃ³n actual | Error local; estado activo no cambia | `transicion_invalida` | error local (refresh opcional si sospecha obsolescencia) | `medium` | flujo principal de sesiÃ³n | `P2` | `#14`, `#12`, `#8` | Sin auto-refresh |
| `EC-SESSION-05` | `session_flow` | `Session.manual_update` rompe unicidad de activa global | CorrecciÃ³n manual sobre timestamps puede convertir sesiÃ³n a activa | `Session.manual_update` | Riesgo de >1 sesiÃ³n activa global | OperaciÃ³n rechazada o conflicto segÃºn base; unicidad preservada | `mixta` | error local si validaciÃ³n; `refresh + retry` si conflicto | `high` | invariante de sesiÃ³n activa global | `P1` | `#12`, `#37`, `#14`, `#8` | ClasificaciÃ³n final por variante |
| `EC-SESSION-06` | `session_flow` | `Entry.delete` activa / `Week.close\|reclose` con `auto-stop` embebido en conflicto compuesto | SesiÃ³n activa en la entry/week afectada | `Entry.delete` / `Week.close` / `Week.reclose` | OperaciÃ³n compuesta falla o queda en estado ambiguo al usuario | Rechazo de la operaciÃ³n compuesta; no dejar estado parcial asumido por cliente | `conflicto` | `refresh` manual + reintentar operaciÃ³n padre | `critical` | invariante + flujo principal + recuperaciÃ³n | `P0` | `#12`, `#14`, `#8` | Compuesto con side-effects |
| `EC-WEEK-01` | `week_state_cursor` | TransiciÃ³n invÃ¡lida de `Week` | Estado real no coincide con transiciÃ³n solicitada | `Week.close` / `Week.reopen` / `Week.reclose` | AcciÃ³n sobre week ya en ese estado / no aplicable | Error local por transiciÃ³n invÃ¡lida; no `refresh` por defecto | `transicion_invalida` | error local | `medium` | flujo temporal y estado | `P1` | `#12`, `#8`, `#14` | Distinguir de conflicto |
| `EC-WEEK-02` | `week_state_cursor` | Conflicto en cambio de estado de week con recÃ¡lculo de `week_cursor` | Week/cursor leÃ­dos obsoletos | `Week.close` / `Week.reopen` / `Week.reclose` | AcciÃ³n de week falla por base obsoleta; marcador `current week` puede quedar viejo | Rechazo por conflicto; `week_cursor` visible se corrige tras refresh | `conflicto` | `refresh` manual + reintentar | `critical` | temporal + consistencia visible | `P0` | `#12`, `#37`, `#9`, `#14`, `#8` | Incluye recÃ¡lculo derivado de cursor |
| `EC-WEEK-03` | `week_state_cursor` | Cierre/recierre dejarÃ­a `0` weeks abiertas | Week objetivo es la Ãºltima abierta | `Week.close` / `Week.reclose` | AcciÃ³n rechazada aunque la week exista y transiciÃ³n parezca vÃ¡lida | ValidaciÃ³n rechaza; invariante de weeks abiertas preservada | `validacion` | error local; corregir acciÃ³n | `critical` | invariante temporal | `P0` | `#12`, `#37`, `#13` | Bloquea comportamiento invÃ¡lido del cursor |
| `EC-ENTRY-01` | `entry_lifecycle_order` | `reorder` con base de orden obsoleta | Orden de entries cambiÃ³ concurrentemente | `Entry.reorder_within_week` | ReordenaciÃ³n falla / orden visible desfasado | Rechazo por conflicto; orden se restablece tras refresh | `conflicto` | `refresh` manual + reintentar | `high` | consistencia visual + flujo principal | `P1` | `#12`, `#18`, `#8` | Resecuencia densa `1..N` |
| `EC-ENTRY-02` | `entry_lifecycle_order` | `Entry.update/delete` sobre entry obsoleta o ya borrada | Cliente opera sobre entry ya modificada/eliminada | `Entry.update` / `Entry.delete` | AcciÃ³n falla; tabs/panel pueden quedar desfasados | Conflicto o transiciÃ³n invÃ¡lida segÃºn caso; no estado parcial | `mixta` | error local (`not found`) o `refresh + retry` (conflicto) | `high` | flujo principal + consistencia visible | `P1` | `#12`, `#14`, `#16`, `#8` | ClasificaciÃ³n final por variante |
| `EC-ENTRY-03` | `entry_lifecycle_order` | Secuencia inconsistente de `order_index` y auto-normalizaciÃ³n | Secuencia previa con huecos/duplicados | `Entry.create` (y/o inserciÃ³n con normalizaciÃ³n) | Orden previo inconsistente detectado | Se auto-normaliza la secuencia y la operaciÃ³n puede continuar sin error | `validacion` | no aplica; comportamiento controlado | `low` | orden de entries / robustez | `P2` | `#12` | Edge local controlado (no fallo) |
| `EC-RESOURCE-01` | `resource_totals_deltas` | Total final negativo | Delta propuesto harÃ­a `campaign_after < 0` | `Entry.adjust/set/clear_resource_delta` | OperaciÃ³n rechazada por total invÃ¡lido | ValidaciÃ³n rechaza; totales no negativos preservados | `validacion` | error local; corregir delta | `high` | integridad de totales de recursos | `P1` | `#15`, `#12` | `clear` puede revelar drift si base mala |
| `EC-RESOURCE-02` | `resource_totals_deltas` | Base obsoleta en deltas/totales | `Entry` o `campaign.resource_totals` cambiÃ³ | `Entry.adjust/set/clear_resource_delta` | Error al persistir ajuste de recursos | Rechazo por conflicto; no aplicar delta sobre base obsoleta | `conflicto` | `refresh` manual + reintentar | `critical` | integridad de datos/recursos | `P0` | `#15`, `#12`, `#8`, `#40` | Caso central de concurrencia en recursos |
| `EC-RESOURCE-03` | `resource_totals_deltas` | Drift/inconsistencia detectada de totales | CÃ¡lculo local detecta preestado imposible | Cualquier operaciÃ³n de recursos (o `Entry.delete` con impacto recursos) | Estado de recursos no cuadra con deltas/totales | Clasificar como conflicto y forzar refresh; escalar si persiste | `conflicto` | `refresh` y reintentar; escalar si persiste | `critical` | integridad de datos/recursos | `P0` | `#15`, `#8`, `#12` | DecisiÃ³n explÃ­cita: drift => conflicto |
| `EC-RESOURCE-04` | `resource_totals_deltas` | No-ops idempotentes sin error | `adjust=0`, `set` mismo valor, `clear` inexistente | `Entry.adjust/set/clear_resource_delta` | AcciÃ³n no cambia estado pero puede ejecutarse | No error; estado final permanece igual; contrato idempotente | `validacion` | no aplica; seguir flujo normal | `low` | robustez / UX tolerante | `P2` | `#15`, `#12`, `#40` | `clear` inexistente es idempotente |
| `EC-TEMPORAL-01` | `temporal_provision_extension` | `extend_years_plus_one` con base obsoleta/duplicado | Estructura temporal cambiÃ³ / aÃ±o ya existe | `Campaign.extend_years_plus_one` | ExtensiÃ³n falla por base obsoleta o duplicados | Rechazo por conflicto o validaciÃ³n; no crear aÃ±o parcial | `mixta` | error local (duplicado/estructura) o `refresh + retry` (conflicto) | `critical` | temporal + integridad estructural | `P0` | `#12`, `#13`, `#37`, `#8` | AÃ±o completo o fallo completo |
| `EC-TEMPORAL-02` | `temporal_provision_extension` | ProvisiÃ³n inicial/reprovisiÃ³n parcial invÃ¡lida | Duplicados o continuidad `week_number` rota | `Campaign.provision_initial_years` | Falla la provisiÃ³n inicial / reprovisiÃ³n accidental | Rechazo por validaciÃ³n o conflicto; no estructura temporal parcial | `mixta` | error local o `refresh + retry` segÃºn base | `high` | temporal + integridad estructural | `P1` | `#12`, `#13`, `#8` | Incluye idempotencia/rechazo de reprovisiÃ³n |
| `EC-READ-01` | `critical_reads_refresh_order` | `ui.manual_refresh` reconcilia conflicto y normaliza estado visible | Estado visible potencialmente obsoleto tras error | `ui.manual_refresh` | UI desincronizada tras conflicto | Refresco on-demand recarga queries visibles y restablece consistencia | `conflicto` | `refresh` manual (acciÃ³n del usuario) | `critical` | recuperaciÃ³n MVP | `P0` | `#7`, `#16`, `#14`, `#18` | Sin realtime listeners |
| `EC-READ-02` | `critical_reads_refresh_order` | `Q8` con `serverTimestamp` pendiente produce orden provisional | Sesiones reciÃ©n escritas con timestamps pendientes | `Q8 sessions_selected_entry_combined` | Orden temporalmente provisional en lista de sesiones | Orden final solo garantizado tras `refresh`; no prometer estabilidad antes | `validacion` | refresh manual cuando se requiera orden final | `medium` | consistencia visual / orden | `P1` | `#18`, `#16` | No es conflicto de escritura |
| `EC-READ-03` | `critical_reads_refresh_order` | Activo global en otra entry (`Q6+Q7`) vs selecciÃ³n/foco | Existe sesiÃ³n activa global y `selected_entry != active_entry` | `Q6` + `Q7` + estado UI (`#14`) | UI puede mostrar foco y activo distintos | UI distingue foco vs activo; label del activo se resuelve vÃ­a Q7 si aplica | `conflicto` | refresh manual si Q6/Q7 quedan obsoletos | `critical` | consistencia visual de foco vs activo | `P0` | `#14`, `#16`, `#18` | Caso crÃ­tico de lectura + flujo |
| `EC-READ-04` | `critical_reads_refresh_order` | Arranque sin selecciÃ³n + cargas diferidas correctas | Apertura de pantalla principal sin selecciÃ³n | `open_main_screen` | Carga excesiva o carga prematura de queries de entry | Cargar solo Q1/Q2/Q3/Q4/Q6; no Q5/Q7/Q8 hasta selecciÃ³n | `validacion` | corregir trigger/carga; no requiere refresh | `medium` | coste/latencia y consistencia de arranque | `P1` | `#16`, `#9`, `#14`, `#7` | Caso de lecturas mÃ­nimas correctas |
| `EC-READ-05` | `critical_reads_refresh_order` | Cambio de aÃ±o / merge `Q3+Q4` mantiene orden de weeks | Cambio de aÃ±o o refresh del aÃ±o visible | `ui.select_year` / refresh Q3+Q4 | Weeks mezcladas fuera de orden canÃ³nico | Merge cliente conserva orden por `week_number ASC` | `validacion` | corregir orden local / refresh si base obsoleta | `medium` | consistencia visual temporal | `P1` | `#16`, `#18`, `#13` | `summer+winter` se ordenan por `week_number` |

## Variantes por familia y operaciÃ³n (capa 2)

### Regla de uso

1. Esta tabla evita multiplicar filas canÃ³nicas.
1. Cada operaciÃ³n/evento obligatorio aparece al menos una vez.
1. Si no aporta edge case nuevo, se marca â€œsin variante crÃ­tica adicionalâ€ y se
   referencia el escenario canÃ³nico mÃ¡s cercano.

### Tabla 3 â€” Variantes por operaciÃ³n (capa 2) (`I17-S2B`)

| `variant_id` | `operation_or_event` | `edge_case_id_base` | `delta_especifico` | `clasificacion_final_esperada` | `recuperacion_final` | `notas` |
| --- | --- | --- | --- | --- | --- | --- |
| `V-001` | `Campaign.provision_initial_years` | `EC-TEMPORAL-02` | Duplicados/continuidad invÃ¡lida al reprovisionar o base obsoleta | `validacion` / `conflicto` | error local o `refresh + retry` | Crear 4 aÃ±os o fallar completo |
| `V-002` | `Campaign.extend_years_plus_one` | `EC-TEMPORAL-01` | Duplicado de aÃ±o / base obsoleta / continuidad invÃ¡lida | `validacion` / `conflicto` | error local o `refresh + retry` | Caso P0 |
| `V-003` | `Week.close` | `EC-WEEK-02` | Puede incluir `auto-stop` embebido + recÃ¡lculo de cursor | `conflicto` / `transicion_invalida` / `validacion` | error local o `refresh + retry` | Ver `EC-WEEK-03` y `EC-SESSION-06` |
| `V-004` | `Week.reopen` | `EC-WEEK-01` | TransiciÃ³n `closed -> open`; cursor derivado | `transicion_invalida` / `conflicto` | error local o `refresh + retry` | Sin caso de `0 weeks abiertas` |
| `V-005` | `Week.reclose` | `EC-WEEK-03` | Puede disparar `auto-stop` y validar `0 weeks abiertas` | `validacion` / `transicion_invalida` / `conflicto` | error local o `refresh + retry` | Compuesto cuando hay activa |
| `V-007` | `Entry.create` | `EC-ENTRY-03` | Auto-normalizaciÃ³n de `order_index` y posible conflicto de base | `validacion` / `conflicto` | no-op/normalizaciÃ³n o `refresh + retry` | Edge local controlado + conflicto posible |
| `V-008` | `Entry.update` | `EC-ENTRY-02` | Entry obsoleta / intento invÃ¡lido (ej. mover de week) | `conflicto` / `validacion` | error local o `refresh + retry` | `transicion_invalida` suele aplicar mÃ¡s a delete |
| `V-009` | `Entry.delete` | `EC-SESSION-06` | Si entry activa: `auto-stop` embebido; si ya no existe: not found | `conflicto` / `transicion_invalida` | error local o `refresh + retry` | TambiÃ©n impacta recursos (`EC-RESOURCE-03`) |
| `V-010` | `Entry.reorder_within_week` | `EC-ENTRY-01` | Base de orden obsoleta o pertenencia incoherente | `conflicto` / `validacion` | error local o `refresh + retry` | Resecuencia densa `1..N` |
| `V-011` | `Entry.adjust_resource_delta` | `EC-RESOURCE-02` | Base obsoleta; no-op si `adjust=0`; total negativo | `conflicto` / `validacion` | error local o `refresh + retry` | Ver `EC-RESOURCE-04` |
| `V-012` | `Entry.set_resource_delta` | `EC-RESOURCE-02` | Base obsoleta; set mismo valor (no-op); total negativo | `conflicto` / `validacion` | error local o `refresh + retry` | Ver `EC-RESOURCE-04` |
| `V-013` | `Entry.clear_resource_delta` | `EC-RESOURCE-03` | Drift detectado o clave inexistente idempotente | `conflicto` / `validacion` | `refresh + retry` o no-op | `clear` inexistente sin error |
| `V-014` | `Session.start` | `EC-SESSION-01` | Puede derivar a `EC-SESSION-03` si entry ya activa | `conflicto` / `transicion_invalida` / `validacion` | error local o `refresh + retry` | Compuesto si habÃ­a activa previa |
| `V-015` | `Session.stop` | `EC-SESSION-02` | Si ya no activa -> `EC-SESSION-04` | `conflicto` / `transicion_invalida` | error local o `refresh + retry` | Distinguir conflicto de acciÃ³n repetida |
| `V-016` | `Session.auto_stop` | `EC-SESSION-06` | Side-effect heredado del padre (`start`, `week close`, `entry delete`) | `conflicto` / `transicion_invalida` | heredada de la operaciÃ³n padre | No acciÃ³n manual principal |
| `V-017` | `Session.manual_create` | `EC-SESSION-05` | Crear activa manual puede violar unicidad | `validacion` / `conflicto` | error local o `refresh + retry` | Weeks `open\|closed` permitidas |
| `V-018` | `Session.manual_update` | `EC-SESSION-05` | `ended_at_utc null <-> valor`; riesgo unicidad activa | `validacion` / `conflicto` | error local o `refresh + retry` | Sin reparenting |
| `V-019` | `Session.manual_delete` | `EC-ENTRY-02` | SesiÃ³n ya borrada vs base obsoleta | `transicion_invalida` / `conflicto` | error local o `refresh + retry` | Puede afectar lectura Q8 |
| `V-020` | `open_main_screen` | `EC-READ-04` | Arranque sin selecciÃ³n; cargas diferidas obligatorias | `validacion` | corregir triggers de carga | No es conflicto, sÃ­ edge de sync/coste |
| `V-021` | `ui.manual_refresh` | `EC-READ-01` | ReconciliaciÃ³n de estado visible tras error/conflicto | `conflicto` | `refresh` manual ejecutado por usuario | NÃºcleo del MVP sin realtime |
| `V-022` | `ui.select_year` | `EC-READ-05` | Merge Q3+Q4 por `week_number`; limpiar selecciÃ³n local | `validacion` / `conflicto` | corregir orden o `refresh` | Q5/Q8 no cargan hasta nueva selecciÃ³n |
| `V-023` | `ui.select_week` | `EC-READ-04` | No debe cargar sesiones (Q8) todavÃ­a | `validacion` | corregir triggers de lectura | Carga Q5 solamente |
| `V-024` | `ui.select_entry` | `EC-READ-03` | Carga Q8 y coexistencia con activa global en otra entry | `conflicto` / `validacion` | `refresh` si base obsoleta; si no, flujo normal | Foco vs activo |
| `V-025` | `Q6 active_session_global` | `EC-READ-03` | Activa global obsoleta / ausente / distinta de foco | `conflicto` | `refresh` manual | `ended_at_utc == null`, `limit 1` |
| `V-026` | `Q7 active_entry_doc_if_needed` | `EC-READ-03` | Label del activo externo no resoluble por doc obsoleto | `conflicto` / `validacion` | `refresh` manual; fallback de UI | Condicional |
| `V-027` | `Q8 sessions_selected_entry_combined` | `EC-READ-02` | Orden provisional por timestamps pendientes y activa primero | `validacion` / `conflicto` | `refresh` manual para orden final | Compatibilidad `#18` |

## Escala de severidad, impacto y prioridad

### `severidad` (4 niveles)

- `critical`: rompe invariantes centrales o puede ocultar corrupciÃ³n/estado
  engaÃ±oso severo.
- `high`: comportamiento incorrecto relevante del flujo principal con alta
  fricciÃ³n/riesgo.
- `medium`: inconsistencia recuperable con impacto acotado o caso menos
  frecuente.
- `low`: edge case controlado/no-op/recuperaciÃ³n clara con impacto menor.

### `impacto` (texto corto obligatorio)

Usar una lÃ­nea breve y concreta, por ejemplo:

- `invariante de sesiÃ³n activa global`
- `consistencia visual de foco vs activo`
- `integridad de totales de recursos`
- `temporal + cursor derivado`
- `recuperaciÃ³n on-demand refresh`

### `prioridad_verificacion`

- `P0`: crÃ­tico para MVP; debe aparecer en `#19`; su ausencia de cobertura
  bloquea `#20`.
- `P1`: importante antes del gate, pero no bloquea por sÃ­ solo si el conjunto
  crÃ­tico estÃ¡ cubierto.
- `P2`: cobertura recomendada / regresiÃ³n posterior.

## Casos crÃ­ticos mÃ­nimos a verificar en el MVP

### Regla de selecciÃ³n (`I17-S3`)

1. Incluir **todos los `P0`** de la matriz principal.
1. Si una familia no tiene `P0`, aÃ±adir al menos un `P1` representativo.
1. Mapear explÃ­citamente cada caso crÃ­tico a `#19` como insumo de pruebas.

### Tabla 4 â€” Casos crÃ­ticos MVP (`I17-S3`)

| `edge_case_id` | `motivo_criticidad` | `prioridad_verificacion` | `bloquea_#20` | `relacion_con_#19` | `notas` |
| --- | --- | --- | --- | --- | --- |
| `EC-SESSION-01` | Conflicto en `start` compuesto (`auto-stop + start`) con riesgo sobre unicidad de sesiÃ³n activa | `P0` | SÃ­ | Debe convertirse en caso de prueba de operaciÃ³n compuesta y recuperaciÃ³n | Flujo principal |
| `EC-SESSION-06` | Side-effects `auto-stop` embebidos en operaciones compuestas (`Entry.delete` / `Week.close\|reclose`) | `P0` | SÃ­ | Requiere pruebas de conflicto en compuestos con efecto observable | Cruza `#12` y `#14` |
| `EC-WEEK-02` | Cambio de estado de week + recÃ¡lculo de `week_cursor` bajo conflicto | `P0` | SÃ­ | Caso de prueba de consistencia temporal y refresh | Afecta `current week` |
| `EC-WEEK-03` | Invariante crÃ­tica: no dejar `0` weeks abiertas | `P0` | SÃ­ | Debe probarse como validaciÃ³n bloqueante | Temporal/cursor |
| `EC-RESOURCE-02` | Conflicto sobre deltas/totales de recursos con riesgo de pÃ©rdida de consistencia | `P0` | SÃ­ | Caso de prueba de recursos con base obsoleta | `Entry.resource_deltas` + `campaign.resource_totals` |
| `EC-RESOURCE-03` | Drift/inconsistencia detectada y clasificaciÃ³n correcta como conflicto | `P0` | SÃ­ | Caso de integridad y recuperaciÃ³n `refresh` | Si persiste tras refresh, escalar |
| `EC-TEMPORAL-01` | ExtensiÃ³n de aÃ±o con duplicados/base obsoleta; riesgo estructural alto | `P0` | SÃ­ | Caso de temporal estructural y atomicidad observable | `+1` aÃ±o |
| `EC-READ-01` | `ui.manual_refresh` como mecanismo central de reconciliaciÃ³n MVP | `P0` | SÃ­ | Caso de recuperaciÃ³n transversal post-conflicto | Sin realtime |
| `EC-READ-03` | Coherencia foco vs activo (Q6/Q7 + selecciÃ³n) en flujo principal | `P0` | SÃ­ | Caso de consistencia visible cruzando `#14` + `#16` | Activo en otra entry |
| `EC-READ-02` | Orden provisional/final de sesiones con timestamps pendientes (`Q8`) | `P1` | No | Incluir como cobertura de orden estable en `#19` | Cubre `#18` en lecturas |
| `EC-ENTRY-01` | ReordenaciÃ³n con base de orden obsoleta | `P1` | No (si hay cobertura alternativa de flujo) | Caso de concurrencia de orden en entries | Recomendada antes de `#20` |
| `EC-ENTRY-02` | `Entry.update/delete` sobre entry obsoleta o inexistente | `P1` | No | Caso de clasificaciÃ³n conflicto vs transiciÃ³n invÃ¡lida | Cobertura de lifecycle |

## AlineaciÃ³n con `#12`, `#14`, `#15`, `#16`, `#18`

### `#12` â€” Contrato de operaciones Firestore por agregado

1. `#17` no redefine pre/postcondiciones ni atomicidad de comportamiento.
1. `#17` traduce ese contrato a escenarios verificables (incluyendo compuestos).
1. La tabla de variantes referencia operaciones de `#12` como cobertura mÃ­nima.

### `#14` â€” Flujo de sesiÃ³n activa y `auto-stop`

1. `#17` reutiliza el modelo de estados/errores del flujo (`conflicto`,
   `transicion_invalida`, `validacion`).
1. Los casos `session_flow` y `critical_reads_refresh_order` deben respetar la
   separaciÃ³n foco vs activo y la recuperaciÃ³n `refresh` manual + reintentar.

### `#15` â€” ValidaciÃ³n y recÃ¡lculo de recursos

1. `#17` reutiliza la clasificaciÃ³n de recursos:
   - total negativo => `validacion`
   - base obsoleta => `conflicto`
   - drift => `conflicto`
   - no-ops idempotentes => sin error
1. No se reabre el modelo de recursos de `#40`.

### `#16` â€” Consultas mÃ­nimas de pantalla principal

1. `#17` cubre solo lecturas crÃ­ticas ligadas a sincronizaciÃ³n/consistencia.
1. `#17` no reactiva `timeline_entries_flat`; se mantiene fuera del MVP actual.
1. `#17` usa Q1..Q8 y triggers de `#16` como base para los casos de lectura.

### `#18` â€” Timestamps y orden estable

1. `#17` no redefine tuplas canÃ³nicas de orden.
1. `#17` solo verifica edge cases derivados:
   - orden provisional por `serverTimestamp` pendiente;
   - estabilizaciÃ³n tras refresh;
   - consistencia visible de listas crÃ­ticas.

## Casos de aceptaciÃ³n / verificaciÃ³n documental

1. La matriz final incluye las 6 familias obligatorias y cubre sesiones,
   entries, recursos, temporal y lecturas crÃ­ticas.
1. La matriz principal contiene al menos los 23 escenarios canÃ³nicos con IDs
   `EC-*` fijados.
1. Cada escenario tiene expectativa verificable, clasificaciÃ³n y recuperaciÃ³n
   esperada.
1. La tabla de variantes cubre todas las operaciones/eventos obligatorios.
1. El subset crÃ­tico incluye todos los `P0` y mapea insumos hacia `#19`.
1. `#17` no contradice `#12/#14/#15/#16/#18/#37/#40`.
1. `timeline_entries_flat` solo aparece, si se menciona, como no activado en el
   MVP actual de `#16`.

## Riesgos, lÃ­mites y decisiones diferidas

- La matriz documenta escenarios y expectativas, pero no sustituye el diseÃ±o de
  pruebas detallado de `#19`.
- Algunas clasificaciones canÃ³nicas se marcan como `mixta` para evitar explotar
  filas; la clasificaciÃ³n final se cierra en la tabla de variantes.
- El comportamiento exacto de mensajes UI (toast/inline/modal) sigue fuera de
  alcance; aquÃ­ se fija recuperaciÃ³n, no diseÃ±o visual.
- Si el MVP amplÃ­a lecturas o reactiva `timeline_entries_flat`, `#17` deberÃ¡
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
- `docs/coding-readiness-gate.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`

