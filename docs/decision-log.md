# Registro de Decisiones

## Metadatos

- `doc_id`: DOC-DECISION-LOG
- `purpose`: Registrar decisiones con trazabilidad y precedencia.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Formato canónico por entrada

- `decision_id`
- `date`
- `status`: `proposed`, `accepted` o `superseded`
- `problem`
- `decision`
- `rationale`
- `impact`
- `references`

## Entradas

### DEC-0001

- `date`: 2026-02-20
- `status`: accepted
- `problem`: definir prioridad del arranque.
- `decision`: priorizar aprendizaje de ingeniería de contexto.
- `rationale`: objetivo explícito del proyecto.
- `impact`: Fase 0 sin código funcional de app.
- `references`: `important.txt`

### DEC-0002

- `date`: 2026-02-20
- `status`: accepted
- `problem`: separar operación y aprendizaje.
- `decision`: usar `docs/` para operación y `learning/` para aprendizaje.
- `rationale`: mejorar foco y reutilización.
- `impact`: estructura dual de documentación.
- `references`: `important.txt`

### DEC-0003

- `date`: 2026-02-20
- `status`: accepted
- `problem`: definir mantenimiento del contexto.
- `decision`: mantenimiento manual con checklist.
- `rationale`: baja complejidad inicial y alta claridad.
- `impact`: IA actualiza y Kiko valida por hito.
- `references`: conversación de planificación

### DEC-0004

- `date`: 2026-02-20
- `status`: accepted
- `problem`: evitar implementación prematura.
- `decision`: gate estricto antes de código.
- `rationale`: prevenir deuda de contexto.
- `impact`: bloqueo si faltan decisiones o checklist.
- `references`: `summary_initial_conversation.txt`

### DEC-0005

- `date`: 2026-02-20
- `status`: accepted
- `problem`: coherencia de idioma.
- `decision`: descripciones en castellano e identificadores técnicos en inglés.
- `rationale`: claridad para aprendizaje y precisión técnica.
- `impact`: regla transversal de documentación.
- `references`: `summary_initial_conversation.txt`

### DEC-0006

- `date`: 2026-02-20
- `status`: accepted
- `problem`: gestión del legado inicial.
- `decision`: convivencia temporal sin borrado en Fase 0.
- `rationale`: preservar contexto histórico.
- `impact`: precedencia oficial y registro de conflictos.
- `references`: `summary_initial_conversation.txt`, `tdd.md`, `important.txt`

### DEC-0007

- `date`: 2026-02-20
- `status`: accepted
- `problem`: reducir riesgo de alucinaciones.
- `decision`: verificación doble en cada hito.
- `rationale`: equilibrio entre rigor y coste.
- `impact`: evidencia obligatoria en gobierno de contexto.
- `references`: `neil.txt`

### DEC-0008

- `date`: 2026-02-20
- `status`: accepted
- `problem`: continuidad entre sesiones.
- `decision`: cierre con menú numerado de 3 a 5 pasos.
- `rationale`: facilita acción inmediata.
- `impact`: estándar de cierre conversacional.
- `references`: conversación de planificación

### DEC-0009

- `date`: 2026-02-20
- `status`: accepted
- `problem`: conflictos entre legado y oficial.
- `decision`: prevalece la documentación oficial.
- `rationale`: fuente de verdad única.
- `impact`: conflicto siempre registrado en este documento.
- `references`: `summary_initial_conversation.txt`, `tdd.md`

### DEC-0010

- `date`: 2026-02-20
- `status`: accepted
- `problem`: mezcla de objetivos en borradores.
- `decision`: separar explícitamente producto y aprendizaje.
- `rationale`: menor ambigüedad de alcance.
- `impact`: navegación y mantenimiento más simples.
- `references`: `important.txt`, `tdd.md`, `neil.txt`

### DEC-0011

- `date`: 2026-02-20
- `status`: accepted
- `problem`: cerrar alcance MVP funcional antes de modelado de dominio.
- `decision`: aprobar alcance MVP v1 con lista de incluye/no incluye y
  criterios de éxito.
- `rationale`: reducir ambigüedad y evitar cambios de alcance durante
  implementación inicial.
- `impact`: queda cerrada la Issue #5 y se habilita trabajo de Issue #6.
- `references`: `tdd.md`, `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/5`

### DEC-0012

- `date`: 2026-02-20
- `status`: accepted
- `problem`: cerrar modelo de dominio e invariantes de la Issue #6 sin abrir
  decisiones de implementación.
- `decision`: adoptar modelo unificado `Entry` (`scenario|outpost`) con
  jerarquía temporal explícita `campaign > year > season > week > entry`.
- `rationale`: reducir complejidad del dominio y evitar duplicación de
  estructura en `Session` y `ResourceChange`.
- `impact`: contrato de dominio cerrado en `docs/domain-glossary.md`; se
  elimina necesidad de `owner_type` en entidades hijas.
- `references`: `docs/domain-glossary.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/6`

### DEC-0013

- `date`: 2026-02-23
- `status`: accepted
- `problem`: falta una estrategia de sincronización multidispositivo para el
  MVP con simplicidad operativa y consistencia explícita.
- `decision`: adoptar una estrategia MVP de sincronización con Firestore como
  fuente de verdad, modo operativo recomendado `single writer`, escrituras
  `online-only` y actualización remota `on-demand refresh`.
- `rationale`: reduce complejidad inicial, alinea expectativas del MVP y
  separa claramente la estrategia general de las decisiones específicas de
  conflictos (#8) y orden/timestamps (#18).
- `impact`: deja trazable el comportamiento esperado en uso normal, explicita
  límites aceptados del MVP y habilita la especificación de conflictos,
  timestamps y contrato de operaciones Firestore por agregado.
- `references`: `docs/sync-strategy.md`, `docs/domain-glossary.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/7`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`

### DEC-0014

- `date`: 2026-02-23
- `status`: accepted
- `problem`: hay ambigüedad operativa sobre el uso de `main`, el momento de
  cierre de Issues cuando el trabajo va en rama y la prioridad entre PRs e
  Issues al pedir “siguiente paso”.
- `decision`: mantener PR obligatoria para cambios relevantes; cerrar la Issue
  asociada tras merge/integración en `main` cuando el trabajo va en rama;
  tratar `siguiente pendiente` y `siguiente issue pendiente` como equivalentes;
  y priorizar PRs abiertas (incluyendo `draft`) antes de pasar a la siguiente
  Issue pendiente al pedir `siguiente paso`.
- `rationale`: reduce ambigüedad de ejecución, evita cierres tempranos como el
  caso de la Issue #7 y deja una regla de priorización conversacional
  determinista.
- `impact`: estandariza el flujo de cierre en trabajo con rama y el orden de
  priorización entre PRs e Issues; mejora trazabilidad de sesiones con Codex.
- `references`: `AGENTS.md`, `docs/repo-workflow.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/7`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/22`

### DEC-0015

- `date`: 2026-02-23
- `status`: accepted
- `problem`: falta una política de conflictos concurrentes para operaciones
  simultáneas sobre `entries`, `sessions`, `weeks` y `resource_changes` en el
  MVP con Firestore.
- `decision`: adoptar una política MVP estricta de rechazo en conflicto con
  `refresco` y `reintento`, sin `last-write-wins`, aplicada por familias de
  operación (estado crítico, `Week.notes` y `ResourceChange`), y diferir el
  mecanismo técnico exacto de detección/validación a la Issue #12.
- `rationale`: prioriza previsibilidad y consistencia del estado frente a
  sobrescrituras silenciosas, y mantiene bajo control la complejidad antes de
  cerrar el contrato técnico por agregado (#12) y la política de
  timestamps/desempates (#18).
- `impact`: cierra la Issue #8 a nivel de política, condiciona la definición de
  operaciones por agregado en #12 y la compatibilidad con orden estable en #18.
- `references`: `docs/conflict-policy.md`, `docs/sync-strategy.md`,
  `docs/domain-glossary.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`

### DEC-0016

- `date`: 2026-02-23
- `status`: accepted
- `problem`: faltaba una regla explícita de ortografía en castellano (`tildes`,
  `ñ` y signos correctos), codificación `UTF-8` y limpieza sistemática de
  ramas locales/remotas tras merge/cierre.
- `decision`: adoptar ortografía completa en castellano para issues, PR,
  documentación y futuros textos de UI; usar `UTF-8` para archivos de texto;
  y limpiar por defecto ramas locales/remotas mergeadas no reutilizables tras
  cada merge/cierre, con exclusiones documentadas.
- `rationale`: mejora consistencia textual, evita correcciones erróneas por
  mojibake visual de terminal y reduce ruido operativo por ramas ya integradas.
- `impact`: se actualizan `AGENTS.md`, `docs/repo-workflow.md`,
  `CONTRIBUTING.md`, plantillas `.github`, checklists operativas y se añade
  `.editorconfig` para reforzar `UTF-8`.
- `references`: `AGENTS.md`, `docs/repo-workflow.md`, `CONTRIBUTING.md`,
  `docs/context-checklists.md`, `.github/pull_request_template.md`,
  `.github/ISSUE_TEMPLATE/decision.md`, `.github/ISSUE_TEMPLATE/task.md`,
  `.github/ISSUE_TEMPLATE/bug.md`, `.editorconfig`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/25`

### DEC-0017

- `date`: 2026-02-23
- `status`: accepted
- `problem`: el diseño de ajustes de campaña para provisión de años quedó
  desalineado con el nuevo enfoque de pantalla única con selector temporal
  superior.
- `decision`: reencuadrar la Issue #9 para definir controles temporales de
  campaña en la barra superior (selector de año/semana), provisión inicial
  automática de 4 años, extensión manual `+1` con confirmación, patrón de
  selector de entry en popover anclado y ajuste manual explícito de
  `week_cursor` separado de la navegación de semanas.
- `rationale`: simplifica la UI principal, evita una pantalla de ajustes
  separada solo para años y mantiene coherencia con el modelo de pantalla única
  del MVP.
- `impact`: cambia el corte funcional de la Issue #9 respecto a #13 y #14;
  exige alinear `week_cursor` en `docs/domain-glossary.md` y su política de
  conflicto en `docs/conflict-policy.md`.
- `references`: `docs/campaign-temporal-controls.md`, `docs/domain-glossary.md`,
  `docs/conflict-policy.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/9`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`

### DEC-0018

- `date`: 2026-02-23
- `status`: accepted
- `problem`: había ambigüedad entre responder cuál era el “siguiente paso” y
  ejecutar ese siguiente paso en la misma sesión.
- `decision`: cuando Kiko pide `siguiente paso`, Codex identifica el trabajo
  prioritario y lo ejecuta por defecto en la misma pasada, manteniendo la
  prioridad vigente (PRs abiertas, incluyendo `draft`, antes que issues). Si no
  hay PRs abiertas, se resuelve la siguiente issue pendiente.
- `rationale`: reduce fricción conversacional, evita intercambios innecesarios y
  alinea la operación con el objetivo de avanzar de punta a punta en cada turno.
- `impact`: se actualizan `docs/repo-workflow.md` y `AGENTS.md` para reflejar
  el comportamiento por defecto y sus excepciones (`Plan Mode`, bloqueo real,
  petición explícita de solo plan/análisis).
- `references`: `AGENTS.md`, `docs/repo-workflow.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/28`

### DEC-0019

- `date`: 2026-02-23
- `status`: accepted
- `problem`: priorizar por número de Issue al pedir `siguiente paso` ignora el
  orden técnico del checklist cuando ya existe una secuencia recomendada
  documentada para la Fase 1.
- `decision`: mantener prioridad de PRs abiertas (incluyendo `draft`) y, si no
  hay PRs, priorizar el orden técnico recomendado en documentación oficial
  aplicable usando la fuente más específica (detalle > macro). Si una Issue del
  orden técnico no es cerrable, se salta a la siguiente cerrable; si no hay
  cerrables, se toma la primera `draftable`. Solo si no existe orden técnico
  aplicable se usa la Issue abierta de número más bajo.
- `rationale`: alinea la ejecución conversacional con la secuencia técnica
  documentada, reduce saltos de contexto y evita priorizaciones por número que
  aumentan el retrabajo.
- `impact`: actualiza la selección de `siguiente paso` en Fase 1 (por ejemplo,
  puede priorizar `#13` antes de `#12`); mantiene sin cambios `siguiente
  pendiente`/`siguiente issue pendiente` y la regla de ejecución por defecto de
  `siguiente paso`.
- `references`: `AGENTS.md`, `docs/repo-workflow.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/32`

### DEC-0020

- `date`: 2026-02-24
- `status`: accepted
- `problem`: había ambigüedad en la traducción de `season` (usada como
  “temporada”) y faltaba fijar el template temporal exacto para cerrar la
  especificación técnica de inicialización de `year/season/week` (Issue #13).
- `decision`: traducir `season` como **estación** (verano e invierno, en ese
  orden) en la documentación en castellano, y fijar para el MVP un template
  temporal determinista de `4` años iniciales, `2` estaciones por año
  (`summer`, `winter`) y `10` semanas por estación, con extensión manual de
  `+1` año desde el control de cambio de año.
- `rationale`: elimina ambigüedad terminológica, evita investigar un calendario
  externo innecesario para la Fase 1 y deja una base técnica cerrable para
  `#13` que reduce retrabajo en `#12`, `#16` y `#20`.
- `impact`: habilita documentar `docs/campaign-temporal-initialization.md` como
  contrato técnico temporal del MVP; corrige terminología en documentación
  oficial relacionada y fija cardinalidades mínimas de creación temporal.
- `references`: `docs/campaign-temporal-controls.md`,
  `docs/campaign-temporal-initialization.md`, `docs/domain-glossary.md`,
  `docs/mvp-implementation-blocks.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`

### DEC-0021

- `date`: 2026-02-24
- `status`: accepted
- `problem`: la regla de `siguiente paso` priorizaba PRs abiertas y orden
  técnico, pero no contemplaba explícitamente unidades ya iniciadas con trabajo
  local/remoto pendiente de cierre (por ejemplo commits sin `push` o rama sin
  PR), lo que podía dejar tareas a medias y permitir avanzar al siguiente
  trabajo.
- `decision`: redefinir `siguiente paso` para que primero detecte y resuelva una
  **unidad pendiente de cierre** antes de iniciar trabajo nuevo; adoptar por
  defecto un cierre end-to-end (commit, `push`, PR, merge/cierre, cierre de
  Issue y limpieza de rama cuando aplique); y documentar el manejo de
  bloqueos por aprobación en `type:decision` y el comportamiento específico en
  `Plan Mode`.
- `rationale`: alinea la ejecución con la expectativa de cierre real por unidad,
  reduce riesgo de trabajo huérfano en ramas locales/remotas y corrige el hueco
  observado en el caso de la Issue `#13` antes de su PR `#34`.
- `impact`: se actualizan `AGENTS.md`, `docs/repo-workflow.md` y
  `docs/context-checklists.md`; `siguiente paso` pasa a priorizar pendientes de
  cierre (incluyendo trabajo local sin publicar) antes de PRs abiertas y orden
  técnico; el reporte de sesión debe indicar estado de cierre alcanzado y
  bloqueo si existe.
- `references`: `AGENTS.md`, `docs/repo-workflow.md`,
  `docs/context-checklists.md`, `docs/decision-log.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/35`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/pull/34`

### DEC-0022

- `date`: 2026-02-24
- `status`: accepted
- `problem`: el dominio del MVP quedó demasiado restrictivo para el objetivo de
  trabajo “como papel”: no permitía reordenación manual de `Entry`, no definía
  correcciones manuales amplias de `Session` ni `Week.reopen/reclose`, y
  mantenía una semántica de `week_cursor` incompatible con esa editabilidad
  ampliada, lo que bloqueaba la redacción coherente de la Issue #12.
- `decision`: introducir una política marco de editabilidad manual del MVP
  (`docs/editability-policy.md`, Issue #37) que permite reordenación manual de
  `Entry` dentro de la misma `Week` con `order_index` denso `1..N`, habilita
  correcciones manuales de `Week.status` (`reopen/reclose`) y correcciones
  manuales completas de `Session` (crear/editar/borrar, incluyendo timestamps),
  manteniendo la invariante de `0..1` sesión activa global; además, redefinir
  `campaign.week_cursor` para que apunte siempre a la primera `Week` abierta
  (menor `week_number` abierta) y rechazar operaciones que dejen `0` weeks
  abiertas provisionadas.
- `rationale`: permite un flujo de trabajo más flexible y cercano a papel sin
  perder invariantes críticos, y separa correctamente la decisión de dominio
  (editabilidad/cursor) del contrato técnico Firestore por agregado (Issue #12).
- `impact`: actualiza `docs/domain-glossary.md`, `docs/conflict-policy.md`,
  `docs/campaign-temporal-controls.md`, `docs/campaign-temporal-initialization.md`
  y el orden técnico en `docs/mvp-implementation-checklist.md` /
  `docs/mvp-implementation-blocks.md`; añade `docs/editability-policy.md` como
  fuente oficial; desplaza la ejecución de `#12` para después de `#37`.
- `references`: `docs/editability-policy.md`, `docs/domain-glossary.md`,
  `docs/conflict-policy.md`, `docs/campaign-temporal-controls.md`,
  `docs/campaign-temporal-initialization.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`

### DEC-0023

- `date`: 2026-02-24
- `status`: accepted
- `problem`: la Issue `#12` necesitaba un contrato técnico por agregado que
  integrara simultáneamente la temporalidad detallada (`#13`) y la nueva
  política de editabilidad manual (`#37`), incluyendo una distinción explícita
  entre conflictos concurrentes y rechazos funcionales por transición inválida.
- `decision`: aceptar `docs/firestore-operation-contract.md` como contrato
  oficial de operaciones Firestore por agregado del MVP; tratar
  `campaign.week_cursor` como efecto derivado (postcondición) y declarar
  `Campaign.set_week_cursor_manual` como operación excluida del contrato activo
  del MVP; modelar `Session` por timestamps (`started_at_utc`, `ended_at_utc`)
  con actividad derivada (`ended_at_utc=null`); permitir mutaciones de
  `Entry/Session/ResourceChange` también en weeks `closed`; documentar
  `auto-stop + cerrar` en `Week.close/reclose` cuando haya sesión activa; y
  distinguir en el contrato (y la política de conflictos alineada) entre
  `conflicto`, `validacion` y `transicion_invalida`.
- `rationale`: reduce ambigüedad de implementación antes de codificar, evita
  contradicciones con `#37`, y hace explícito el comportamiento esperado ante
  errores funcionales que no son conflictos concurrentes reales.
- `impact`: añade `docs/firestore-operation-contract.md` como fuente oficial;
  actualiza `docs/conflict-policy.md` para reflejar la distinción
  conflicto/transición inválida; desbloquea el cierre de `#14`, `#15`, `#16`,
  `#17`, `#18` y `#19` con una base contractual común; actualiza seguimiento en
  `docs/mvp-implementation-checklist.md` y `docs/mvp-implementation-blocks.md`.
- `references`: `docs/firestore-operation-contract.md`,
  `docs/conflict-policy.md`, `docs/domain-glossary.md`,
  `docs/campaign-temporal-initialization.md`, `docs/editability-policy.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `AGENTS.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`

### DEC-0024

- `date`: 2026-02-24
- `status`: accepted
- `problem`: el modelo MVP de recursos basado en `ResourceChange` (log `0..N`
  por `Entry`) quedó desalineado con la intención de edición manual "como
  papel", y dejaba complejidad innecesaria en contratos y conflictos justo
  antes de cerrar la política de timestamps/orden estable (`#18`).
- `decision`: sustituir `ResourceChange` como entidad MVP por un campo
  `Entry.resource_deltas` con tipo lógico `map<resource_key, int>` y semántica
  de delta neto editable por recurso dentro de cada `Entry`; mantener solo
  claves con delta `!= 0` (ausencia de clave = `0`), eliminar la clave cuando
  el delta neto resulte `0`, reutilizar únicamente la auditoría de `Entry` (sin
  timestamps por recurso) y parchear `docs/firestore-operation-contract.md`
  para reemplazar `ResourceChange.*` por operaciones sobre
  `Entry.resource_deltas` sin reabrir la Issue `#12`.
- `rationale`: simplifica el modelo de dominio y la edición de recursos en el
  MVP, alinea el comportamiento con la editabilidad amplia definida en `#37`,
  reduce complejidad de concurrencia/contratos y evita arrastrar un log
  incremental intra-entry que no aporta valor al MVP actual.
- `impact`: añade `docs/resource-delta-model.md` como fuente oficial; elimina
  `ResourceChange` del glosario MVP activo; actualiza `docs/conflict-policy.md`
  y parchea parcialmente `docs/firestore-operation-contract.md` (supersesión
  parcial de la parte de recursos de `DEC-0023`); reordena el bloque técnico
  para ejecutar esta decisión antes de `#18`, y deja `#18` como siguiente paso
  tras su cierre.
- `references`: `docs/resource-delta-model.md`, `docs/domain-glossary.md`,
  `docs/firestore-operation-contract.md`, `docs/conflict-policy.md`,
  `docs/editability-policy.md`, `docs/mvp-implementation-checklist.md`,
  `docs/mvp-implementation-blocks.md`, `AGENTS.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`

### DEC-0025

- `date`: 2026-02-24
- `status`: accepted
- `problem`: faltaba una política oficial de timestamps de auditoría y
  desempate de orden estable entre dispositivos para evitar divergencias
  visuales en listas del MVP (timeline, sesiones y selectores), y seguían
  abiertas decisiones sobre `deleted_at_utc`, orden canónico y reparto
  query/cliente.
- `decision`: aceptar `docs/timestamp-order-policy.md` como política oficial de
  timestamps y orden estable del MVP; usar `created_at_utc` y `updated_at_utc`
  como timestamps de auditoría **server-only**; eliminar `deleted_at_utc` del
  MVP (hard delete real); ampliar auditoría temporal a
  `campaign/year/season/week/entry/session`; actualizar `updated_at_utc` en
  toda escritura persistida, también derivada/sistémica; definir una matriz de
  orden canónico por lista (alcance UI + `#16`) con prefijo de query + orden
  canónico final en cliente; usar desempate final por `document_id`
  lexicográfico ascendente; priorizar orden de dominio (`week_number`,
  `order_index`) sobre timestamps cuando exista; y considerar que el orden final
  con `serverTimestamp` pendiente solo se garantiza tras `refresh`.
- `rationale`: separa claramente auditoría/orden estable de los contratos por
  operación (`#12`), reduce ambigüedad para `#16/#17/#19`, y deja reglas
  trazables para listas de dominio y listas temporales sin adelantar técnica
  Firestore específica.
- `impact`: añade `docs/timestamp-order-policy.md` como fuente oficial;
  actualiza `docs/domain-glossary.md` (auditoría y eliminación de
  `deleted_at_utc`), `docs/firestore-operation-contract.md` (referencia a la
  política final de `#18`), y el seguimiento técnico en
  `docs/mvp-implementation-checklist.md` / `docs/mvp-implementation-blocks.md`;
  deja `#14` como siguiente paso técnico tras cerrar `#18`.
- `references`: `docs/timestamp-order-policy.md`, `docs/domain-glossary.md`,
  `docs/firestore-operation-contract.md`, `docs/conflict-policy.md`,
  `docs/resource-delta-model.md`, `docs/mvp-implementation-checklist.md`,
  `docs/mvp-implementation-blocks.md`, `AGENTS.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`

### DEC-0026

- `date`: 2026-02-24
- `status`: accepted
- `problem`: faltaba una especificación oficial del flujo cliente/UI de sesión
  activa (`start/stop/auto-stop`) que cerrara la separación entre `current
  week`, selección (`Week`/`Entry`) y `Entry` activa, además de la recuperación
  esperada ante `conflicto` vs `transicion_invalida`.
- `decision`: aceptar `docs/active-session-flow.md` como contrato oficial del
  flujo de sesión activa del MVP; ubicar `Iniciar/Parar sesión` en el bloque de
  la `Entry` seleccionada (no en barra inferior global); separar explícitamente
  `current week` (marcador derivado de `week_cursor`) de selección/foco y de
  `Entry` activa; definir que cambiar foco no hace `auto-stop`; clasificar
  `Session.start` sobre la misma `Entry` activa como `transicion_invalida`
  (error local); mantener `auto-stop` como side-effect sin confirmación extra;
  y fijar recuperación de `conflicto` como `refresh` manual + reintentar.
- `rationale`: reduce ambigüedad de implementación para `#17/#19/#20`, alinea
  el comportamiento observable del cliente con `#12` (contrato por operación),
  `#37` (editabilidad e invariantes) y `#18` (refresh/orden estable), y evita
  confundir navegación/foco con estado activo global.
- `impact`: añade `docs/active-session-flow.md` como fuente oficial; actualiza
  `docs/campaign-temporal-controls.md` para reforzar la separación entre
  `week_cursor/current week` y selección; actualiza tracking en
  `docs/mvp-implementation-checklist.md` y `docs/mvp-implementation-blocks.md`;
  deja `#15` como siguiente paso técnico tras cerrar `#14`.
- `references`: `docs/active-session-flow.md`,
  `docs/firestore-operation-contract.md`, `docs/editability-policy.md`,
  `docs/timestamp-order-policy.md`, `docs/campaign-temporal-controls.md`,
  `docs/domain-glossary.md`, `docs/mvp-implementation-checklist.md`,
  `docs/mvp-implementation-blocks.md`, `AGENTS.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`

### DEC-0027

- `date`: 2026-02-24
- `status`: accepted
- `problem`: faltaban reglas documentales explícitas para validar operaciones
  sobre `Entry.resource_deltas` y recalcular `campaign.resource_totals` de forma
  consistente, con clasificación clara de rechazos (`validacion` vs
  `conflicto`) y manejo de correcciones/borrados tras el cambio de modelo de
  recursos de `#40`.
- `decision`: aceptar `docs/resource-validation-recalculation.md` como contrato
  oficial de validación y recálculo de recursos del MVP; cubrir
  `Entry.adjust_resource_delta`, `Entry.set_resource_delta`,
  `Entry.clear_resource_delta` y el impacto de recursos de `Entry.delete`;
  validar `resource_key` contra catálogo MVP, deltas enteros y no negatividad
  de totales finales; definir equivalencia de resultado con recálculo desde
  `Entry.resource_deltas`; normalizar claves con valor `0` fuera de
  `entry.resource_deltas` y `campaign.resource_totals`; aceptar `clear` de clave
  inexistente y no-ops triviales (`adjust=0`, `set` al mismo valor) como
  idempotentes; y clasificar inconsistencias detectadas de base/totales como
  `conflicto` para forzar `refrescar + reintentar`.
- `rationale`: completa el detalle que `#12` dejó a nivel de contrato de
  comportamiento y que `#40` dejó a nivel de modelo, reduce ambigüedad para
  `#17/#19/#20` y mantiene coherencia con la política estricta de conflictos de
  `#8`.
- `impact`: añade `docs/resource-validation-recalculation.md` como fuente
  oficial; actualiza referencias en glosario, conflictos, contrato Firestore y
  modelo de recursos; actualiza tracking en `docs/mvp-implementation-checklist.md`
  y `docs/mvp-implementation-blocks.md`; deja `#16` como siguiente paso técnico.
- `references`: `docs/resource-validation-recalculation.md`,
  `docs/domain-glossary.md`, `docs/conflict-policy.md`,
  `docs/firestore-operation-contract.md`, `docs/resource-delta-model.md`,
  `docs/editability-policy.md`, `docs/mvp-implementation-checklist.md`,
  `docs/mvp-implementation-blocks.md`, `AGENTS.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`

### DEC-0028

- `date`: 2026-02-24
- `status`: accepted
- `problem`: tras cerrar `#15` se detectó que se habían documentado defaults de
  representación de `campaign.resource_totals` sin revisión explícita de Kiko,
  dejando una normalización de claves `0` que no coincidía con la intención
  final del dominio.
- `decision`: corregir parcialmente `DEC-0027` (sin reabrir `#15`) para que
  `campaign.resource_totals` conserve claves materializadas con valor `0` cuando
  una operación las deja en `0`, permitiendo a la vez ausencia de clave para
  recursos nunca usados; confirmar como contrato oficial que
  `Entry.adjust_resource_delta(adjustment_delta=0)`, `Entry.set_resource_delta`
  al mismo valor y `Entry.clear_resource_delta` sobre clave inexistente son
  no-ops idempotentes; y mantener la clasificación de drift/inconsistencia de
  base/totales como `conflicto` con `refrescar + reintentar`.
- `rationale`: preserva la trazabilidad del cierre de `#15` sin reescribir su
  historial, alinea la representación de totales con la revisión posterior de
  Kiko y mantiene consistencia con `#8`, `#12` y `#40`.
- `impact`: actualiza `docs/resource-validation-recalculation.md` y
  `docs/domain-glossary.md` para reflejar la nueva regla de claves `0` en
  `campaign.resource_totals`; deja `Entry.resource_deltas` sin cambios
  (claves `0` no persistidas); y documenta explícitamente la supersesión parcial
  de `DEC-0027` en este punto.
- `references`: `docs/resource-validation-recalculation.md`,
  `docs/domain-glossary.md`, `docs/decision-log.md`,
  `docs/firestore-operation-contract.md`, `docs/conflict-policy.md`,
  `docs/resource-delta-model.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/45`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`

### DEC-0029

- `date`: 2026-02-24
- `status`: accepted
- `problem`: faltaba una especificación oficial y trazable de consultas mínimas
  para la pantalla principal del MVP, y `#16` seguía descrita en términos de
  "timeline/panel de foco" sin cerrar el inventario de lecturas por superficie,
  triggers de carga y compatibilidad con `#18`.
- `decision`: aceptar `docs/minimal-read-queries.md` como contrato oficial de
  lecturas mínimas de pantalla principal para el MVP (`#16`), fijando:
  Figma compartido por Kiko como canon de layout/superficies para esta issue;
  arranque sin `Week`/`Entry` seleccionada (barra en el año de `current week`);
  inventario de consultas Q1..Q8; carga diferida de sesiones hasta selección de
  `Entry`; y ausencia de paginación en MVP.
- `rationale`: reduce ambigüedad entre layout heredado (`tdd.md`) y diseño
  actual, alinea lecturas con `#9`, `#14`, `#15`, `#18` y `#12`, y deja una
  base ejecutable para implementación sin listeners realtime ni sobrecargar el
  modelo con lecturas innecesarias.
- `impact`: cierra `#16`; actualiza tracking y trazabilidad (`AGENTS.md`,
  `docs/system-map.md`, checklist y blocks); y añade referencias cruzadas en
  docs temporales/flujo/orden para que `#17` y `#19` usen el mismo contrato de
  lectura.
- `references`: `docs/minimal-read-queries.md`, `docs/timestamp-order-policy.md`,
  `docs/campaign-temporal-controls.md`, `docs/active-session-flow.md`,
  `docs/firestore-operation-contract.md`, `docs/decision-log.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `AGENTS.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`

### DEC-0030

- `date`: 2026-02-24
- `status`: accepted
- `problem`: faltaba una matriz oficial de edge cases que tradujera los
  contratos y flujos ya cerrados (`#12`, `#14`, `#15`, `#16`, `#18`) a
  escenarios verificables para concurrencia/sincronización, con severidad y
  prioridad trazables hacia `#19` / `#20`.
- `decision`: aceptar `docs/concurrency-sync-edge-case-matrix.md` como matriz
  oficial de edge cases del MVP (`#17`), con alcance mixto (concurrencia/sync +
  `transicion_invalida`/`validacion` cuando afectan el mismo flujo), cobertura
  de lecturas críticas solamente, formato en 2 capas (escenarios canónicos +
  variantes por operación/evento), y esquema de riesgo en 3 campos
  (`severidad`, `impacto`, `prioridad_verificacion`).
- `rationale`: reduce ambigüedad antes del plan de pruebas (`#19`), evita
  duplicar diseño de pruebas en `#17`, y crea una base única para priorizar
  verificación de invariantes/recuperación sin reabrir decisiones de dominio.
- `impact`: cierra `#17`; añade una fuente oficial de edge cases reutilizable
  por `#19/#20`; actualiza tracking en checklist/bloques; y conecta
  sincronización, conflictos, contrato por agregado, flujo de sesión, lecturas
  mínimas y política de orden mediante referencias cruzadas.
- `references`: `docs/concurrency-sync-edge-case-matrix.md`,
  `docs/sync-strategy.md`, `docs/conflict-policy.md`,
  `docs/firestore-operation-contract.md`, `docs/active-session-flow.md`,
  `docs/resource-validation-recalculation.md`, `docs/minimal-read-queries.md`,
  `docs/timestamp-order-policy.md`, `docs/editability-policy.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `AGENTS.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`

### DEC-0031

- `date`: 2026-02-24
- `status`: accepted
- `problem`: faltaba traducir la matriz de edge cases (`#17`) y las invariantes
  de dominio/consistencia ya cerradas a un plan de pruebas reutilizable para el
  gate `#20`, con evidencia mínima y reglas de repetibilidad, sin exigir aún
  ejecución real previa al inicio de código.
- `decision`: aceptar `docs/domain-invariant-test-plan.md` como plan oficial de
  pruebas para invariantes de dominio del MVP (`#19`), con catálogo `INV-*`,
  casos `TC-*`, trazabilidad obligatoria a `EC-*` de `#17`, priorización para
  `#20` (`P0/P1/P2`), plantilla mínima de evidencia y alcance de ejecución
  previo al gate limitado a `single device`, dejando la concurrencia
  multi-dispositivo real como diferido explícito.
- `rationale`: reduce ambigüedad en readiness, evita confundir definición de
  pruebas con ejecución real antes de tener código, y permite que `#20` evalúe
  cobertura bloqueante (`P0`) sobre un plan trazable en lugar de sobre criterios
  ad hoc.
- `impact`: cierra `#19`; establece el contrato documental de QA/readiness para
  invariantes; enlaza `#17` con `#20`; actualiza tracking (checklist/bloques) y
  añade una fuente oficial reutilizable para fases posteriores de ejecución de
  pruebas.
- `references`: `docs/domain-invariant-test-plan.md`,
  `docs/concurrency-sync-edge-case-matrix.md`, `docs/domain-glossary.md`,
  `docs/conflict-policy.md`, `docs/firestore-operation-contract.md`,
  `docs/active-session-flow.md`, `docs/resource-validation-recalculation.md`,
  `docs/minimal-read-queries.md`, `docs/timestamp-order-policy.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `AGENTS.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`
