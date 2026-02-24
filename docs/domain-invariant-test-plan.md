# Plan de Pruebas para Invariantes de Dominio (MVP)

## Metadatos

- `doc_id`: DOC-DOMAIN-INVARIANT-TEST-PLAN
- `purpose`: Definir un plan de pruebas documental, repetible y trazable para invariantes de dominio del MVP, reutilizando la matriz de edge cases (`#17`) y preparando el gate de `#20`.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar un plan de pruebas orientado a invariantes de dominio que traduzca las
reglas oficiales del MVP en casos verificables, con trazabilidad hacia la matriz
de edge cases (`#17`) y criterios de priorización útiles para el gate de `#20`.

## Alcance y no alcance

Incluye:

- catálogo priorizado de invariantes críticas del dominio y de consistencia
  visible del MVP;
- matriz de casos de prueba por invariante (`TC-*`);
- mapeo de casos a edge cases de `#17` (`EC-*`);
- priorización para gate `#20` (`P0/P1/P2`) y rol de cada caso en el gate;
- estrategia de evidencia mínima (plantilla clara);
- reglas de repetibilidad;
- delimitación de alcance de ejecución (single device) y diferidos explícitos.

No incluye:

- ejecución real de pruebas;
- implementación de tests en código;
- harnesses, fixtures o scripts;
- cobertura multi-dispositivo real antes del gate `#20`;
- reapertura de decisiones de dominio/backend ya cerradas.

## Entradas y prerrequisitos

- `docs/domain-glossary.md`
- `docs/sync-strategy.md` (Issue `#7`)
- `docs/conflict-policy.md` (Issue `#8`)
- `docs/campaign-temporal-controls.md` (Issue `#9`)
- `docs/campaign-temporal-initialization.md` (Issue `#13`)
- `docs/firestore-operation-contract.md` (Issue `#12`)
- `docs/active-session-flow.md` (Issue `#14`)
- `docs/resource-validation-recalculation.md` (Issue `#15`)
- `docs/minimal-read-queries.md` (Issue `#16`)
- `docs/concurrency-sync-edge-case-matrix.md` (Issue `#17`)
- `docs/timestamp-order-policy.md` (Issue `#18`)
- `docs/editability-policy.md` (Issue `#37`)
- `docs/resource-delta-model.md` (Issue `#40`)
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`

## Principios del plan (qué valida `#19` y qué no)

1. `#19` define **qué probar** y **cómo dejar evidencia mínima**, no ejecuta
   pruebas ni exige resultados reales todavía.
1. `#19` reutiliza `#17` como fuente de edge cases/criticidad; no la duplica.
1. `P0 obligatorios` significa:
   - obligatorios **en el plan**;
   - bloqueantes para el gate `#20` si no están definidos y trazados;
   - no implica ejecución real antes de empezar a programar.
1. El alcance de ejecución previsto para la fase previa al gate es
   **single device**.
1. Los casos que requieran concurrencia real multi-dispositivo se mantienen en
   el plan, pero se marcan como diferidos explícitos.

## Catálogo de invariantes priorizadas

### Criterios de selección

1. Invariantes de dominio estructural y de integridad (sesiones, temporalidad,
   entries, recursos).
1. Invariantes de consistencia visible del MVP cuando dependen de sincronización,
   refresh u orden (`#16` + `#18` + `#14`).
1. Cobertura mínima suficiente para alimentar el gate `#20`.

### Tabla 1 — Catálogo de invariantes (`I19-S1`)

| `invariant_id` | `invariante` | `tipo` | `descripcion` | `fuentes_principales` | `criticidad_base` | `notas` |
| --- | --- | --- | --- | --- | --- | --- |
| `INV-SESSION-01` | Unicidad de sesión activa global | `dominio` | Nunca hay más de una `Session` activa global (`0..1`) | `#12`, `#14`, glosario | `critical` | Incluye flujos normales y correcciones manuales |
| `INV-SESSION-02` | `auto-stop` embebido preserva invariantes | `dominio` | Operaciones compuestas con `auto-stop` (`start`, `Week.close/reclose`, `Entry.delete`) no dejan estados parciales válidos asumidos | `#12`, `#14` | `critical` | Compuesto + side-effects |
| `INV-SESSION-03` | Clasificación/recuperación de errores en flujo de sesión | `consistencia_visible` | `conflicto` vs `transicion_invalida` vs `validacion` se diferencian y recuperan según contrato | `#8`, `#12`, `#14` | `high` | Afecta UX/reintento |
| `INV-SESSION-04` | Separación foco vs activo | `consistencia_visible` | La UI distingue `selected_entry` y `active_entry` con carga/refresh coherentes | `#14`, `#16`, `#18` | `critical` | Relacionado con Q6/Q7 |
| `INV-TEMPORAL-01` | `week_cursor` = primera week abierta | `dominio` | `week_cursor` se recalcula a la primera `Week` abierta tras cambios de estado | `#37`, `#12`, `#9`, glosario | `critical` | Cursor derivado |
| `INV-TEMPORAL-02` | Nunca `0` weeks abiertas | `dominio` | `Week.close/reclose` no puede dejar `0` weeks abiertas | `#12`, `#37`, `#13` | `critical` | Validación bloqueante |
| `INV-TEMPORAL-03` | Navegación/selección no cambia `week_cursor` | `consistencia_visible` | Seleccionar week/entry no muta `campaign.week_cursor` | `#9`, `#14`, `#16`, glosario | `high` | Separa navegación de cursor |
| `INV-TEMPORAL-04` | Estructura temporal fija del MVP | `dominio` | `summer -> winter`, 10 semanas/estación, 4 años iniciales, extensión `+1` | `#13`, `#12` | `high` | Estructural |
| `INV-TEMPORAL-05` | `week_number` global único/inmutable | `dominio` | `week_number` es correlativo, único e inmutable | `#13`, glosario, `#12` | `high` | Impacta lecturas/orden |
| `INV-ENTRY-01` | `order_index` denso `1..N` | `dominio` | Tras create/reorder, la secuencia de entries de la week es densa y estable | `#12`, `#18`, glosario | `high` | Incluye auto-normalización |
| `INV-ENTRY-02` | `Entry.delete` hard delete + cascada + auto-stop | `dominio` | Borrado de entry activa cierra sesión activa y elimina dependencias según contrato | `#12`, `#14`, glosario | `critical` | Operación compuesta |
| `INV-ENTRY-03` | Mutabilidad en weeks `open|closed` | `dominio` | Entries y recursos pueden editarse en weeks cerradas según `#37/#12` | `#37`, `#12`, `#15` | `medium` | Evita bloqueos artificiales |
| `INV-RESOURCE-01` | Totales de campaña = suma de deltas de entries | `dominio` | `campaign.resource_totals` refleja la suma de `Entry.resource_deltas` | `#15`, `#40`, glosario | `critical` | Integridad de recursos |
| `INV-RESOURCE-02` | Totales finales no negativos | `dominio` | Ninguna operación puede dejar un total final `< 0` | `#15`, `#12` | `critical` | Validación central |
| `INV-RESOURCE-03` | Normalización de recursos | `dominio` | `Entry.resource_deltas` sin claves `0`; `campaign.resource_totals` conserva `0` materializado y omite nunca usadas | `#15`, `#40`, glosario | `high` | Regla revisada en `DEC-0028` |
| `INV-RESOURCE-04` | Drift de recursos => `conflicto` + `refresh` | `dominio` | Inconsistencias de base/totales se clasifican como conflicto, no validación | `#15`, `#8`, `#12` | `critical` | Protección de integridad |
| `INV-READ-01` | Arranque sin selección y cargas diferidas | `consistencia_visible` | Al abrir pantalla se cargan Q1/Q2/Q3/Q4/Q6; no Q5/Q7/Q8 hasta selección | `#16`, `#9`, `#14`, `#7` | `high` | Coste/latencia + coherencia |
| `INV-READ-02` | Orden canónico de listas críticas | `consistencia_visible` | Weeks, entries y sesiones usan las tuplas canónicas definidas en `#18` | `#18`, `#16` | `high` | Orden estable |
| `INV-READ-03` | Orden provisional se estabiliza tras refresh | `consistencia_visible` | Timestamps pendientes pueden producir orden provisional; el orden final se garantiza tras `refresh` | `#18`, `#16` | `medium` | No es conflicto de escritura |
| `INV-READ-04` | `ui.manual_refresh` reconcilia estado visible | `consistencia_visible` | `on-demand refresh` restablece consistencia visible sin realtime | `#7`, `#16`, `#14`, `#17` | `critical` | Núcleo de recuperación MVP |

## Matriz de casos por invariante

### Convenciones de diseño (`I19-S2`)

1. Un `TC-*` tiene una expectativa principal y referencia un `invariant_id`
   principal.
1. Un mismo `TC-*` puede cubrir más de una invariante; las secundarias van en
   `notas` o en la tabla de trazabilidad.
1. `clasificacion_esperada` usa:
   - `conflicto`
   - `transicion_invalida`
   - `validacion`
   - `sin_error`
1. `evidence_minima` referencia la plantilla de Tabla 4 con campos mínimos a
   completar.
1. `rol_en_gate_20` usa:
   - `bloqueante_plan` (P0)
   - `planificado_no_bloqueante` (P1/P2)
   - `diferido_aceptado` (si requiere multi-device real)

### Tabla 2 — Matriz de casos por invariante (`I19-S2`)

| `test_case_id` | `invariant_id` | `titulo_caso` | `precondicion` | `accion` | `resultado_esperado` | `clasificacion_esperada` | `evidence_minima` | `repetibilidad` | `prioridad_verificacion` | `rol_en_gate_20` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `TC-SESSION-01` | `INV-SESSION-01` | `start` con activa previa no crea doble activa | Existe sesión activa global o base potencialmente obsoleta | Intentar `Session.start` en otra entry | Nunca quedan 2 activas; conflicto se rechaza y se recupera con refresh | `conflicto` | `run_id`, `test_case_id`, resultado observado, status, evidence_refs | `defer_multi_device` / `desk_check_documental` | `P0` | `bloqueante_plan` | Cubre `auto-stop + start` |
| `TC-SESSION-02` | `INV-SESSION-02` | `Week.close/reclose` con activa embebida preserva invariante | Week con sesión activa en esa week | Cerrar/re-cerrar week | `auto-stop` embebido + cierre/reclose sin estado parcial asumido | `conflicto` / `validacion` | Campos mínimos + referencia al escenario compuesto | `desk_check_documental` | `P0` | `bloqueante_plan` | Relaciona `#12` + `#14` |
| `TC-SESSION-03` | `INV-SESSION-03` | `start` sobre entry ya activa clasifica transición inválida | `selected_entry == active_entry` | Pulsar `Iniciar` | Error local; no nueva sesión ni `auto-stop` | `transicion_invalida` | Resultado observado + status | `single_device_preparado` | `P1` | `planificado_no_bloqueante` | Flujo UI |
| `TC-SESSION-04` | `INV-SESSION-04` | Activa en otra entry y foco distinto | Existe activa global en otra entry | Cargar Q6/Q7 y seleccionar otra entry | UI distingue foco vs activo; label de activo externo coherente | `sin_error` / `conflicto` | Evidencia visual + refs de datos | `single_device_preparado` / `desk_check_documental` | `P0` | `bloqueante_plan` | Cruza `#14/#16/#18` |
| `TC-TEMPORAL-01` | `INV-TEMPORAL-01` | Recalcular `week_cursor` tras cambio de estado | Week abierta candidata a primera abierta | Ejecutar `Week.close/reopen/reclose` | `week_cursor` apunta a primera week abierta válida | `sin_error` / `conflicto` | Resultado cursor antes/después | `desk_check_documental` | `P0` | `bloqueante_plan` | Cursor derivado |
| `TC-TEMPORAL-02` | `INV-TEMPORAL-02` | Rechazo al dejar `0` weeks abiertas | Última week abierta identificada | Intentar `close/reclose` | Operación rechazada por validación; invariante preservada | `validacion` | Resultado esperado + status | `desk_check_documental` | `P0` | `bloqueante_plan` | Validación crítica |
| `TC-TEMPORAL-03` | `INV-TEMPORAL-03` | Navegación no muta `week_cursor` | `week_cursor` conocido; sin side-effect de estado | `ui.select_week` / `ui.select_entry` | Selección cambia foco; `week_cursor` no cambia | `sin_error` | Evidencia visual/estado | `single_device_preparado` / `desk_check_documental` | `P1` | `planificado_no_bloqueante` | Consistencia visible |
| `TC-TEMPORAL-04` | `INV-TEMPORAL-04` | Provisión/extensión respeta plantilla temporal | Campaña nueva o provisionada para `+1` | Provisión inicial / `extend_years_plus_one` | `summer->winter`, 10 semanas/estación, 4 años iniciales / `+1` exacto | `sin_error` / `validacion` / `conflicto` | Resultado estructural resumido | `desk_check_documental` | `P1` | `planificado_no_bloqueante` | Estructura + continuidad |
| `TC-TEMPORAL-05` | `INV-TEMPORAL-05` | `week_number` global único e inmutable | Estructura temporal conocida | Revisar create/extend y operaciones históricas | No duplicación/reutilización; numeración correlativa mantenida | `sin_error` / `validacion` | Evidencia de rangos/resultados | `desk_check_documental` | `P1` | `planificado_no_bloqueante` | Trazable en docs |
| `TC-ENTRY-01` | `INV-ENTRY-01` | Resecuencia densa tras create/reorder | Week con entries y/o secuencia inconsistente | `Entry.create` / `Entry.reorder_within_week` | `order_index` denso `1..N`; auto-normalización si aplica | `sin_error` / `conflicto` | Orden antes/después | `desk_check_documental` / `single_device_preparado` | `P1` | `planificado_no_bloqueante` | Incluye auto-normalización |
| `TC-ENTRY-02` | `INV-ENTRY-02` | Borrado de entry activa cierra sesión y elimina dependencias | Entry activa con sesiones y recursos | `Entry.delete` | Hard delete + cascada + `auto-stop`; sin activa asociada final | `conflicto` / `transicion_invalida` / `sin_error` | Resultado observable + refs | `desk_check_documental` | `P0` | `bloqueante_plan` | Compuesto |
| `TC-ENTRY-03` | `INV-ENTRY-03` | Mutaciones de entry en week `closed` permitidas | Week cerrada seleccionada | `Entry.update` / reorder / recursos | Operación permitida salvo validación específica; no bloqueo artificial | `sin_error` / `validacion` | Caso y resultado | `desk_check_documental` | `P2` | `planificado_no_bloqueante` | Alineado con `#37` |
| `TC-RESOURCE-01` | `INV-RESOURCE-01` | Totales = suma de deltas tras operación | Entries con `resource_deltas` definidos | `adjust/set/clear` o `Entry.delete` | `campaign.resource_totals` consistente con suma de entries | `sin_error` / `conflicto` | Totales antes/después + refs | `desk_check_documental` | `P1` | `planificado_no_bloqueante` | Integridad derivada |
| `TC-RESOURCE-02` | `INV-RESOURCE-02` | Total final negativo se rechaza | Delta propuesto lleva `< 0` | `adjust/set/clear` | Validación rechaza; no persiste estado inválido | `validacion` | Resultado y mensaje esperado | `single_device_preparado` / `desk_check_documental` | `P1` | `planificado_no_bloqueante` | Error local |
| `TC-RESOURCE-03` | `INV-RESOURCE-03` | Normalización `Entry` vs `campaign` respeta reglas distintas | Recursos con delta a `0` y totales materializados | `set/clear` + recálculo | `Entry.resource_deltas` sin clave `0`; `campaign.resource_totals` conserva `0` materializado | `sin_error` | Estado final representacional | `desk_check_documental` | `P1` | `planificado_no_bloqueante` | Regla de `DEC-0028` |
| `TC-RESOURCE-04` | `INV-RESOURCE-04` | Drift de recursos se clasifica como conflicto | Preestado imposible / inconsistente detectado | Operación de recursos o `Entry.delete` impacto recursos | Clasificación `conflicto`; recovery `refresh` | `conflicto` | Clasificación y recovery esperados | `desk_check_documental` | `P0` | `bloqueante_plan` | Protección de integridad |
| `TC-READ-01` | `INV-READ-01` | Arranque sin selección y carga mínima correcta | Apertura de pantalla principal | `open_main_screen` | Carga Q1/Q2/Q3/Q4/Q6; no Q5/Q7/Q8 | `sin_error` | Queries esperadas / estado inicial | `desk_check_documental` | `P1` | `planificado_no_bloqueante` | `#16` |
| `TC-READ-02` | `INV-READ-02` | Orden canónico de weeks/entries/sesiones | Datos con potencial colisión de orden | Render/merge de listas según `#18` | Tuplas canónicas aplicadas y desempates correctos | `sin_error` | Orden esperado vs observado | `desk_check_documental` | `P1` | `planificado_no_bloqueante` | `#18` + `#16` |
| `TC-READ-03` | `INV-READ-03` | Orden provisional por timestamps pendientes se estabiliza | `serverTimestamp` pendiente en sesiones | Cargar Q8 y luego `refresh` | Antes: orden provisional; después: orden final canónico | `sin_error` | Evidencia antes/después + refresh | `defer_multi_device` / `desk_check_documental` | `P1` | `diferido_aceptado` | No bloquea `#20` por ejecución |
| `TC-READ-04` | `INV-READ-04` | `ui.manual_refresh` reconcilia estado visible | UI desfasada tras conflicto o estado obsoleto | `ui.manual_refresh` | Estado visible se normaliza sin realtime | `conflicto` / `sin_error` | Resultado antes/después refresh | `single_device_preparado` / `desk_check_documental` | `P0` | `bloqueante_plan` | Núcleo de recuperación MVP |

## Mapeo a edge cases de `#17` (trazabilidad)

### Regla

1. Todos los `P0` de `#17` deben aparecer en esta tabla asociados al menos a un
   `TC-*`.
1. La relación puede ser:
   - `directa`: el `TC-*` prueba ese `EC-*` de forma explícita;
   - `parcial`: cubre solo una parte del escenario;
   - `agregada`: un `TC-*` cubre un grupo de edge cases bajo una invariante.

### Tabla 3 — Trazabilidad con `#17` (`I19-S2/I19-S4`)

| `test_case_id` | `edge_case_id_17` | `motivo_relacion` | `cobertura` | `notas` |
| --- | --- | --- | --- | --- |
| `TC-SESSION-01` | `EC-SESSION-01` | Conflicto en `start` compuesto y unicidad de activa global | `directa` | `P0` crítico |
| `TC-ENTRY-02` | `EC-SESSION-06` | `Entry.delete` activa con `auto-stop` embebido | `directa` | Compuesto |
| `TC-SESSION-02` | `EC-SESSION-06` | Variante de conflicto compuesto en cierre de sesión dentro de operación padre | `parcial` | Complementa `Entry.delete` / `Week.close` |
| `TC-TEMPORAL-01` | `EC-WEEK-02` | Conflicto en estado de week con recálculo de `week_cursor` | `directa` | `P0` crítico |
| `TC-TEMPORAL-02` | `EC-WEEK-03` | No dejar `0` weeks abiertas | `directa` | `P0` crítico |
| `TC-RESOURCE-01` | `EC-RESOURCE-02` | Recursos sobre base obsoleta afectan consistencia de totales | `parcial` | Integridad de totales |
| `TC-RESOURCE-04` | `EC-RESOURCE-03` | Drift/inconsistencia clasificada como conflicto | `directa` | `P0` crítico |
| `TC-TEMPORAL-04` | `EC-TEMPORAL-01` | Extensión temporal `+1` con conflicto/duplicado | `parcial` | Cobertura estructural + clasificación |
| `TC-READ-04` | `EC-READ-01` | `ui.manual_refresh` como mecanismo de reconciliación MVP | `directa` | `P0` crítico |
| `TC-SESSION-04` | `EC-READ-03` | Foco vs activo con activa en otra entry (`Q6/Q7`) | `parcial` | Consistencia visible |
| `TC-SESSION-03` | `EC-SESSION-03` | `start` sobre entry ya activa | `directa` | `transicion_invalida` |
| `TC-READ-01` | `EC-READ-04` | Arranque sin selección y cargas diferidas | `directa` | `#16` |
| `TC-READ-02` | `EC-READ-05` | Orden canónico de weeks por merge Q3+Q4 | `parcial` | Orden temporal visible |
| `TC-READ-03` | `EC-READ-02` | Orden provisional por timestamp pendiente en Q8 | `directa` | Diferido de ejecución real |
| `TC-ENTRY-01` | `EC-ENTRY-01` | Conflicto de reorder y consistencia de orden | `directa` | Orden de entries |
| `TC-ENTRY-01` | `EC-ENTRY-03` | Auto-normalización de `order_index` | `agregada` | Mismo caso cubre comportamiento nominal |
| `TC-RESOURCE-02` | `EC-RESOURCE-01` | Total final negativo | `directa` | Validación |
| `TC-RESOURCE-03` | `EC-RESOURCE-04` | No-ops / normalización representacional de recursos | `parcial` | Incluye reglas de claves `0` |

## Priorización para gate `#20` (`P0/P1/P2`)

### Decisión operativa fijada

`P0 obligatorios` significa **obligatorios en el plan** (definidos, trazados y
marcados como bloqueantes), no ejecución real previa al inicio de código.

### Tabla 5 — Priorización para gate `#20` (`I19-S4`)

| `prioridad_verificacion` | `criterio` | `obligatorio_para_#20` | `estado_en_#19` | `notas` |
| --- | --- | --- | --- | --- |
| `P0` | Casos críticos de invariantes / recuperación / integridad identificados en `#17` | Sí | `bloqueante` | Deben estar definidos, trazados y con evidencia/repetibilidad especificadas |
| `P1` | Casos importantes antes del gate, no bloqueantes por sí solos | No (individualmente) | `planificado` | Deben quedar priorizados y listos para ejecución posterior |
| `P2` | Cobertura recomendada / regresión posterior | No | `planificado` | Puede ejecutarse tras inicio de código o en ampliaciones |
| `P0/P1/P2` con necesidad multi-device real | Caso requiere concurrencia real que se difiere | No (por ejecución real previa) | `diferido` | Debe quedar explícito como `defer_multi_device`; no oculto |

## Estrategia de evidencia mínima y repetibilidad

### Formato elegido

Plantilla mínima clara (campos obligatorios + ejemplo breve).

### Tabla 4 — Plantilla mínima de evidencia (`I19-S3`)

| `campo` | `obligatorio` | `descripcion` | `ejemplo` | `notas` |
| --- | --- | --- | --- | --- |
| `run_id` | Sí | Identificador único de ejecución/registro | `RUN-2026-02-24-001` | Puede agrupar varios `TC-*` |
| `date_utc` | Sí | Fecha/hora UTC del registro | `2026-02-24T16:10:00Z` | UTC para trazabilidad |
| `executor` | Sí | Quién ejecuta/revisa | `Kiko` / `Codex (desk-check)` | Puede ser revisión documental |
| `scope` | Sí | Alcance de ejecución | `single_device` / `desk_check` / `deferred_multi_device` | Coherente con `repetibilidad` |
| `build_or_commit_ref` | Sí | Referencia técnica o `N/A` | `main@55faf2c` / `N/A` | `N/A` válido si aún no hay app ejecutable |
| `test_case_id` | Sí | Caso probado | `TC-RESOURCE-04` | Debe existir en Tabla 2 |
| `invariant_id` | Sí | Invariante principal | `INV-RESOURCE-04` | Debe existir en Tabla 1 |
| `precondicion_resumida` | Sí | Resumen corto de setup | `estado de recursos con drift detectado (desk-check)` | No sustituye al caso |
| `resultado_observado` | Sí | Qué ocurrió/qué se verificó | `clasificación documentada como conflicto` | Texto corto |
| `resultado_esperado` | Sí | Resultado esperado (resumen) | `conflicto + refresh` | Puede referenciar tabla/caso |
| `status` | Sí | Estado de la verificación | `pass` / `fail` / `blocked` / `deferred` | `deferred` para multi-device diferido |
| `evidence_refs` | Sí | Referencias a evidencia | `captura-001.png`, `nota-issue`, `N/A` | `N/A` solo si el caso es puramente documental |
| `notes` | No | Observaciones y decisiones | `requiere cobertura real multi-device post-MVP gate` | Libre |
| `follow_up_issue` | No | Issue de seguimiento (si aplica) | `#NN` / `N/A` | Para gaps detectados |

### Reglas de repetibilidad

1. Cada `TC-*` debe indicar una marca de repetibilidad en el campo
   `repetibilidad`:
   - `single_device_preparado`
   - `desk_check_documental`
   - `defer_multi_device`
2. Debe existir una precondición reproducible (o una justificación explícita de
   por qué el caso queda como `desk_check_documental` / `defer_multi_device`).
3. La acción debe ser concreta y el criterio de éxito verificable.

## Alcance de ejecución (single device) y diferidos

### Confirmado para `#19`

1. La cobertura de ejecución previa al gate se planifica para **single device**
   (o `desk_check_documental` mientras no exista app ejecutable).
1. La concurrencia real multi-dispositivo queda diferida.

### Reglas para diferidos multi-device

1. Si un caso requiere concurrencia real entre dispositivos, se marca:
   - `repetibilidad = defer_multi_device`
   - `status` esperado en plantilla puede ser `deferred`
   - `rol_en_gate_20` según corresponda (`diferido_aceptado` si no bloquea por
     ejecución real)
2. El caso debe permanecer:
   - definido
   - priorizado
   - trazado a `#17`
   - explícito como diferido
3. `#20` debe distinguir claramente:
   - falta de definición (bloqueante)
   - diferido explícito y aceptado (no bloqueante para entrar a código)

## Casos de aceptación / verificación documental

1. El catálogo incluye las invariantes mínimas obligatorias (`INV-*`) de
   sesiones, temporal/cursor, entries, recursos y lecturas críticas.
1. La matriz de casos (`TC-*`) cubre al menos un caso por invariante.
1. Todos los `P0` de `#17` quedan trazados a `TC-*` en la tabla de mapeo.
1. El documento distingue claramente `#17` (edge cases) de `#19` (plan de
   pruebas).
1. La priorización para `#20` deja explícito que `P0` son bloqueantes **en el
   plan**, no ejecución real pre-código.
1. Existe plantilla mínima de evidencia con campos obligatorios y ejemplos.
1. Los casos multi-device reales quedan explícitamente marcados como diferidos.

## Riesgos, límites y decisiones diferidas

- El plan no sustituye ejecución real; solo deja preparado el contrato de
  pruebas para el gate y fases posteriores.
- La cobertura multi-dispositivo real se difiere por decisión explícita; si el
  riesgo percibido cambia, `#20` puede exigir elevar algunos casos antes de
  empezar código.
- Algunos casos `TC-*` se apoyan en `desk_check_documental` hasta disponer de UI
  ejecutable; esto debe quedar visible en la evidencia.
- La automatización de estas pruebas (si se desea) queda fuera de `#19`.

## Referencias

- `AGENTS.md`
- `docs/system-map.md`
- `docs/decision-log.md`
- `docs/domain-glossary.md`
- `docs/sync-strategy.md`
- `docs/conflict-policy.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/firestore-operation-contract.md`
- `docs/active-session-flow.md`
- `docs/resource-delta-model.md`
- `docs/resource-validation-recalculation.md`
- `docs/minimal-read-queries.md`
- `docs/concurrency-sync-edge-case-matrix.md`
- `docs/timestamp-order-policy.md`
- `docs/editability-policy.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `docs/coding-readiness-gate.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`
