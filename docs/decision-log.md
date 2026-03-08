# Registro de Decisiones

## Metadatos

- `doc_id`: DOC-DECISION-LOG
- `purpose`: Registrar decisiones con trazabilidad y precedencia.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-08
- `next_review`: 2026-03-12

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

### DEC-0032

- `date`: 2026-02-24
- `status`: accepted
- `problem`: faltaba un gate final operativo y trazable que definiera cuándo se
  puede empezar a codificar tras cerrar la preparación documental del MVP, y
  persistía una contradicción en `AGENTS.md`/`context-governance` (reglas de
  Fase 0 y prohibición de código) una vez alcanzado el readiness.
- `decision`: aceptar `docs/coding-readiness-gate.md` como gate oficial de
  entrada a implementación (`#20`), con resultado documental en 3 estados
  (`apto`, `apto_con_diferidos_aceptados`, `no_apto`), checklist de
  bloqueo/desbloqueo, evidencia mínima, diferidos aceptados explícitos y
  resultado aplicado al estado actual del repo. Se actualizan `AGENTS.md`,
  `docs/context-governance.md` y `CHK-GATE-CODE` para permitir implementación
  tras gate válido y registrar el estado de fase `implementation_enabled`.
- `rationale`: evita ambigüedad sobre el inicio de código, conserva rigor del
  gate de calidad, distingue bloqueantes reales de diferidos aceptados (como la
  concurrencia multi-device real diferida en `#19`) y deja una transición
  documental consistente sin reabrir contratos de dominio.
- `impact`: cierra `#20`; habilita inicio de implementación con resultado
  `apto_con_diferidos_aceptados`; actualiza gobierno de contexto y reglas
  operativas; y deja recomendación explícita del primer slice de código
  (infraestructura/base app).
- `references`: `docs/coding-readiness-gate.md`, `AGENTS.md`,
  `docs/context-governance.md`, `docs/context-checklists.md`,
  `docs/domain-invariant-test-plan.md`,
  `docs/concurrency-sync-edge-case-matrix.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`

### DEC-0033

- `date`: 2026-02-25
- `status`: accepted
- `problem`: al implementar el wiring local de la pantalla principal (`#53`)
  se decidió mantener un visor sticky (última entry visible) al navegar por
  years/weeks, lo que desalineaba parcialmente la semántica de selección usada
  en `docs/minimal-read-queries.md` (`#16`) y podía introducir ambigüedad con
  la separación foco/activo descrita en `docs/active-session-flow.md` (`#14`).
- `decision`: aceptar en la implementación del shell/local state (`#53`) una
  separación explícita entre navegación (`selected_year`, `selected_week`),
  entry visible en visor (sticky) y `active_entry` (sesión activa global). La
  navegación por year/week puede cambiar sin limpiar la entry visible en visor.
  En el shell mock de `#53` las weeks cerradas se muestran atenuadas y la week
  seleccionada se marca visualmente, sin añadir marcador explícito de "current
  week" (que sigue siendo un concepto derivado de `week_cursor` real).
- `rationale`: mejora la continuidad visual del panel central al navegar,
  demuestra mejor la separación foco/activo antes de integrar datos reales
  (`#54`) y mantiene el contrato de acciones sobre la entry visible sin reabrir
  las reglas de backend/operaciones.
- `impact`: ajusta semántica de UI/lecturas en `#16` y aclaraciones de flujo en
  `#14`; guía la implementación de `#53` y deja preparada la integración
  read-only de `#54` con distinción navegación/visor/activo.
- `references`: `docs/minimal-read-queries.md`, `docs/active-session-flow.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `src/frosthaven_campaign_journal/ui/app_root.py`,
  `src/frosthaven_campaign_journal/ui/views/main_shell_view.py`,
  `src/frosthaven_campaign_journal/state/placeholders.py`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/53`

### DEC-0034

- `date`: 2026-02-26
- `status`: accepted
- `problem`: existe una discrepancia entre el modelo temporal deseado por
  producto (semana actual derivada no persistida = primera `Week` abierta) y el
  estado actual del repo, que todavía persiste/consume `campaign.week_cursor`
  como campo canónico en lecturas y writes temporales. La issue `#76` nació como
  gap de observabilidad UI de `week_cursor`, pero esa formulación deja de ser
  correcta si `week_cursor` ya no debe existir como concepto vigente.
- `decision`: reencuadrar `#76` como unidad de decisión+documentación para
  fijar el canon de **semana actual derivada no persistida**, marcar
  `campaign.week_cursor` como implementación transitoria (no contrato objetivo)
  y abrir una issue técnica separada para migrar código/datos. No se realiza la
  migración técnica en `#76`.
- `rationale`: simplifica el modelo conceptual (semana actual = primera week
  abierta), evita diseñar UX/testabilidad alrededor de un campo técnico que se
  quiere retirar y reduce retrabajo al separar claramente reencuadre documental
  de migración de implementación.
- `impact`: actualiza docs núcleo (temporal, editabilidad, lecturas, contrato,
  glosario, invariantes) con nota de transición; añade trazabilidad histórica en
  `#70`; crea una issue técnica de migración (`#81`); y deja una divergencia
  transitoria aceptada entre docs canónicas y código actual hasta ejecutar esa
  migración.
- `references`: `docs/campaign-temporal-controls.md`,
  `docs/editability-policy.md`, `docs/minimal-read-queries.md`,
  `docs/firestore-operation-contract.md`, `docs/domain-glossary.md`,
  `docs/domain-invariant-test-plan.md`, `docs/context-governance.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/76`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/81`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/70`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`


### DEC-0035

- `date`: 2026-02-26
- `status`: accepted
- `problem`: tras completar la fase fuerte de preparación de contexto, el ritmo de implementación funcional de la app quedó por debajo del objetivo personal del proyecto (uso propio y avance visible de UI/funcionalidades).
- `decision`: cambiar el modo operativo a **desarrollo-first**: priorizar cierre de UI y funcionalidades pendientes, manteniendo documentación, issues y PR con nivel ligero y orientado a ejecución. Este cambio no elimina trazabilidad; la hace proporcional al impacto real.
- `rationale`: maximiza valor práctico del proyecto, reduce sobrecarga documental y mantiene aprendizaje aplicable sin frenar entrega de producto.
- `impact`: se incorpora una guía reusable de arranque de proyectos personales con ingeniería de contexto ligera; se actualiza el estado de fase para priorizar implementación acelerada; y se crea backlog inmediato de issues de desarrollo, incluyendo una de simplificación de código.
- `references`: `AGENTS.md`, `docs/context-governance.md`, `docs/mvp-implementation-checklist.md`, `learning/personal-context-engineering-quickstart.md`

### DEC-0036

- `date`: 2026-02-27
- `status`: accepted
- `problem`: el feature `main_shell` mantenía múltiples capas operativas (acciones tipadas, orquestación, actualización incremental, composición de pantalla por submódulos), lo que dificultaba un flujo directo de mantenimiento para el arranque de implementación.
- `decision`: consolidar `main_shell` en una arquitectura estricta de tres archivos funcionales (`model.py`, `state.py`, `view.py`) más `__init__.py`, eliminando capas intermedias y conectando `build_app_root(page)` directamente con `MainShellState` + `build_main_shell_view`.
- `rationale`: reduce complejidad accidental, deja un punto único de estado y otro de render, y mantiene la API pública del root para permitir iteración rápida en UI.
- `impact`: se eliminaron módulos previos del feature y se creó un documento técnico comparativo (`docs/ui-main-shell-architecture-mvs.md`) para trazabilidad rápida del cambio.
- `references`: `src/frosthaven_campaign_journal/ui/app_root.py`, `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`, `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`, `src/frosthaven_campaign_journal/ui/features/main_shell/view.py`, `docs/ui-main-shell-architecture-mvs.md`

### DEC-0037

- `date`: 2026-02-28
- `status`: accepted
- `problem`: tras la consolidación a MVS (`DEC-0036`), el root de UI quedó en
  un patrón híbrido (render con `page.add(...)` + `page.update()`), lo que
  incumplía la guía declarativa recomendada para Flet y mantenía acoplamiento
  imperativo entre estado y render.
- `decision`: migrar el runtime del shell a modo declarativo de Flet, usando
  `page.render(build_app_root, page)` en el entrypoint, `@ft.component` en
  `build_app_root`, callback `notify_ui` para disparar rerender y eliminación
  de `page.update()`/`control.update()` en la capa `src/.../ui`.
- `rationale`: alinea la arquitectura MVS con el modelo declarativo nativo de
  Flet, reduce efectos laterales de actualización manual y deja un flujo más
  predecible para evolución del feature sin reabrir la estructura de archivos.
- `impact`: actualiza `main.py`, `ui/app_root.py` y `state.py` para un ciclo
  de render declarativo; mantiene contratos de `model.py`; y refuerza la
  documentación de arquitectura del feature con una regla explícita de no usar
  `update` manual en UI.
- `references`: `src/main.py`,
  `src/frosthaven_campaign_journal/ui/app_root.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`,
  `docs/ui-main-shell-architecture-mvs.md`

### DEC-0038

- `date`: 2026-02-28
- `status`: accepted
- `problem`: aunque `DEC-0037` eliminó `page.update()` manual, el feature seguía
  con un patrón más verboso (`data + actions`) que no aprovechaba el flujo
  directo recomendado por Flet en ejemplos declarativos (`state observable`
  consumido por el componente).
- `decision`: adoptar en `main_shell` un patrón declarativo ligero: estado
  `@ft.observable` consumido por `@ft.component` con `use_state`, binding directo
  de handlers del estado desde la vista y eliminación de `MainShellViewActions`.
- `rationale`: reduce capas accidentales, deja una estructura más simple para
  iteración rápida y alinea el feature con el patrón práctico tipo `edit_form`
  de Flet manteniendo separación útil de scripts (`model/state/view`).
- `impact`: `app_root` pasa a usar `use_state(MainShellState.create)`;
  `view.py` deja de depender de `actions`; `state.py` concentra handlers y
  usa `notify()` cuando aplica en mutaciones anidadas; la interacción de la
  vista se enlaza de forma directa con handlers del estado; `model.py` mantiene
  solo contrato de datos de vista.
- `references`: `src/frosthaven_campaign_journal/ui/app_root.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/view.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`,
  `docs/ui-main-shell-architecture-mvs.md`,
  `https://github.com/flet-dev/flet/blob/main/sdk/python/examples/apps/declarative/edit_form.py`

### DEC-0039

- `date`: 2026-02-28
- `status`: superseded
- `problem`: el estado de `main_shell` seguía recibiendo `ft.Page`, lo que
  mezclaba infraestructura de runtime con estado de pantalla y alejaba el
  patrón objetivo (`model/state/view`) de una separación limpia.
- `decision`: desacoplar `MainShellState` de `ft.Page`; mover viewport a campos
  propios del estado e inyectar cambios de media/viewport desde `app_root`
  mediante método específico (`on_viewport_change`).
- `rationale`: mantiene el estado centrado en dominio/UI local y deja `Page`
  como responsabilidad del componente root, con acoplamiento mínimo y explícito.
- `impact`: `MainShellState.create(...)` deja de recibir `page`; `build_view_data`
  usa `viewport_width/viewport_height` internos; `app_root` conserva el puente
  con `page.on_media_change` y solo reenvía datos primitivos al estado.
- `references`: `src/frosthaven_campaign_journal/ui/app_root.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `docs/ui-main-shell-architecture-mvs.md`

### DEC-0040

- `date`: 2026-02-28
- `status`: accepted
- `problem`: en el flujo actual de app fija en landscape, el puente de
  `viewport_width/viewport_height` añadía complejidad sin uso funcional real.
- `decision`: simplificar `main_shell` eliminando viewport del estado y
  retirando el bridge de `page.on_media_change`; mantener el estado observable
  centrado en interacción de pantalla y datos de vista necesarios.
- `rationale`: reduce ruido en el patrón declarativo objetivo (`model/state/view`)
  y evita transportar datos de infraestructura que no aportan valor en el estado
  actual de la UI.
- `impact`: `MainShellViewData` deja de incluir viewport; `MainShellState.create`
  vuelve a firma sin parámetros; `app_root` usa `use_state(MainShellState.create)`
  sin hooks adicionales de media.
- `references`: `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `src/frosthaven_campaign_journal/ui/app_root.py`,
  `docs/ui-main-shell-architecture-mvs.md`

### DEC-0041

- `date`: 2026-03-01
- `status`: accepted
- `problem`: el refactor `#94` simplificó la estructura `main_shell` pero dejó
  una regresión funcional severa: se perdió wiring real de Firestore
  (lecturas/escrituras) y gran parte del panel central operativo.
- `decision`: recuperar la paridad funcional pre-`#94` sobre arquitectura
  declarativa MVS, manteniendo `page.render(...)`, `@ft.component` en root,
  `@ft.observable` en estado y sin reintroducir `page.update()` ni
  `control.update()` en `src/.../ui`.
- `rationale`: restaura valor funcional del MVP sin volver al patrón híbrido
  imperativo ni reabrir capas eliminadas (`dispatcher/reducer/effects`).
- `impact`: `model.py` amplía contrato de vista con estado declarativo de
  confirmaciones/formularios; `state.py` reintegra Q1..Q8 y operaciones de
  campaña/week/session/entry/resources con handlers directos; `view.py`
  recupera panel central funcional (modo vacío/week/entry, sesiones, recursos,
  acciones y editores inline).
- `references`: `src/main.py`,
  `src/frosthaven_campaign_journal/ui/app_root.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/view.py`,
  `docs/ui-main-shell-architecture-mvs.md`,
  `docs/mvp-implementation-checklist.md`,
  `docs/mvp-implementation-blocks.md`

### DEC-0042

- `date`: 2026-03-01
- `status`: accepted
- `problem`: tras recuperar la funcionalidad real, seguían rastros de etapa
  bootstrap (`Mock*`, módulos `placeholders` y archivos legacy de arranque)
  que añadían ruido semántico y deuda de mantenimiento.
- `decision`: retirar del árbol activo los mocks/placeholders residuales y
  eliminar los documentos legacy de arranque, manteniendo solo trazabilidad
  histórica en documentación oficial.
- `rationale`: reduce ambigüedad entre runtime real y artefactos de
  preparación, simplifica imports/modelos y evita depender de fuentes no
  canónicas ya migradas.
- `impact`: se reemplaza `state/placeholders.py` por `state/models.py`,
  `main_shell` y `data` consumen tipos neutrales (`EntrySummary`,
  `WeekSummary`); se eliminan `data/firestore_placeholder.py` y
  `domain_adapters/placeholders.py`; y se retiran
  `summary_initial_conversation.txt`, `tdd.md`, `important.txt`, `neil.txt`.
- `references`: `src/frosthaven_campaign_journal/state/models.py`,
  `src/frosthaven_campaign_journal/state/__init__.py`,
  `src/frosthaven_campaign_journal/data/__init__.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/view.py`,
  `AGENTS.md`,
  `README.md`,
  `docs/system-map.md`,
  `docs/context-governance.md`

### DEC-0043

- `date`: 2026-03-02
- `status`: accepted
- `problem`: el selector de entries fuera del visor central y el comportamiento
  sticky del visor al cambiar de semana generaban una UX poco coherente con el
  objetivo de foco semanal y edición rápida por entry.
- `decision`: mover la selección/gestión de entries al visor central con
  listado vertical por semana y acciones por icono en cada tile
  (`subir/bajar/eliminar/editar notas`), eliminar la barra externa de entries y
  retirar el sticky del visor al cambiar de semana o año. Además, extender el
  modelo de `Entry` con `notes` y `scenario_outcome` (`victory|defeat|null`),
  dejando `scenario_outcome` en modo solo lectura en UI en esta iteración.
- `rationale`: simplifica el flujo mental (semana -> entries -> entry),
  reduce navegación lateral redundante y habilita edición rápida de notas sin
  abrir la vista completa de entry.
- `impact`: se actualizan lecturas/escrituras para persistir `notes` y
  `scenario_outcome`; se añade `update_entry_notes`; se rediseña `center_focus`
  con tiles semanales y acciones icon-only; y se alinea documentación de dominio
  y contrato Firestore con el nuevo alcance.
- `references`: `src/frosthaven_campaign_journal/models/__init__.py`,
  `src/frosthaven_campaign_journal/data/main_screen_reads.py`,
  `src/frosthaven_campaign_journal/data/entry_writes.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/state/navigation.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/state/week_entry_resources.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/shell_view.py`,
  `docs/domain-glossary.md`,
  `docs/firestore-operation-contract.md`

### DEC-0044

- `date`: 2026-03-04
- `status`: accepted
- `problem`: la UI de recursos del visor y la barra inferior seguía orientada a
  un subconjunto reducido y no tenía catálogo único reusable para 12 claves,
  iconografía oficial ni layout agrupado estable en móvil.
- `decision`: unificar catálogo de recursos del runtime en una fuente única
  compartida de 12 claves (`resource_catalog`), introducir control reusable de
  fila de delta para edición por entry, rediseñar barra inferior con 4 columnas
  fijas y scroll horizontal, y fijar oficialmente mapeo EN->ES + assets en
  `docs/resource-ui-catalog.md`.
- `rationale`: reduce duplicidad entre dominio/UI/writes, facilita evolución de
  controles reusables en modo declarativo Flet y deja trazabilidad explícita de
  nomenclatura/iconos alineada con el glosario del MVP.
- `impact`: `ENTRY_RESOURCE_KEYS` pasa a depender de catálogo único de 12
  claves; validación de writes de recursos usa la misma fuente; el editor de
  recursos renderiza 12 filas agrupadas con total proyectado; la barra inferior
  muestra siempre los 12 totales guardados con icono y nombre completo; se
  oficializa carpeta `assets/resource-icons/` y se añaden iconos de
  `inspiration`, `morale` y `soldiers` en SVG+PNG.
- `references`: `src/frosthaven_campaign_journal/resource_catalog.py`,
  `src/frosthaven_campaign_journal/models/__init__.py`,
  `src/frosthaven_campaign_journal/data/resource_writes.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/resource_delta_row.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/status_bar.py`,
  `assets/resource-icons/`,
  `docs/resource-ui-catalog.md`,
  `docs/domain-glossary.md`

### DEC-0045

- `date`: 2026-03-05
- `status`: accepted
- `problem`: la UI del shell principal en tablet no mantenía densidad útil
  (barra superior y visor central), el bloque de estado inferior ocupaba espacio
  crítico y el soporte de notas de semana dejó de ser necesario para el flujo
  objetivo.
- `decision`: rediseñar la shell para tablet con acciones contextuales en botón
  flotante (`+`), eliminar la cabecera de semana y metadatos redundantes por
  entry, mantener solo recursos totales en barra inferior (orden visual:
  `Otros -> Materiales -> Plantas`) y retirar por completo `Week.update_notes`
  del runtime y de los contratos activos del MVP.
- `rationale`: prioriza legibilidad y acciones frecuentes en viewport reducido,
  simplifica el modelo operativo semanal y elimina una vía de edición que ya no
  aporta valor al flujo de juego.
- `impact`: se compacta la barra temporal superior, se sustituye la fila de
  refresco por menú flotante contextual, se simplifica el visor semanal,
  desaparece el estado textual de la barra inferior, se actualiza el modelo
  (`WeekRead`/`WeekSummary`) sin notas de semana y se alinea la documentación
  oficial eliminando referencias activas a `Week.update_notes`.
- `references`: `src/frosthaven_campaign_journal/ui/main_shell/view/temporal_bar.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/shell_view.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/center_panel.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/status_bar.py`,
  `src/frosthaven_campaign_journal/ui/common/resources/groups.py`,
  `src/frosthaven_campaign_journal/ui/common/resources/resource_total_row.py`,
  `src/frosthaven_campaign_journal/models/__init__.py`,
  `src/frosthaven_campaign_journal/data/main_screen_reads.py`,
  `src/frosthaven_campaign_journal/data/week_writes.py`,
  `docs/firestore-operation-contract.md`,
  `docs/conflict-policy.md`,
  `docs/editability-policy.md`,
  `docs/minimal-read-queries.md`,
  `docs/timestamp-order-policy.md`,
  `docs/concurrency-sync-edge-case-matrix.md`,
  `docs/resource-ui-catalog.md`,
  `docs/ui-main-shell-architecture-mvs.md`

### DEC-0046

- `date`: 2026-03-05
- `status`: accepted
- `problem`: la UI principal seguía sin usar acento de fondo en elementos clave
  de interacción, los iconos de recursos no cargaban de forma fiable con
  `flet run src/main.py -d -r` por ubicación de assets y la tarjeta de entry
  mantenía bloques textuales redundantes para el flujo tablet.
- `decision`: aplicar acento rojo `PUNCH_RED` en fondos de botones de año,
  semana seleccionada, FAB y etiquetas de todas las `LabeledGroupBox`;
  reubicar iconos de `assets/resource-icons/` a
  `src/assets/resource-icons/`; simplificar la tarjeta de entry retirando el
  bloque de detalle textual y dejando `Recursos`/`Sesiones` como etiquetas de
  caja.
- `rationale`: mejora jerarquía visual y legibilidad de estados seleccionados,
  alinea la resolución de assets con el modo de arranque real del repo y reduce
  ruido visual en el visor semanal sin tocar contratos de dominio.
- `impact`: se introducen semánticos de acento en `colors.py`, la barra
  temporal y el FAB usan fondo de acento en estado habilitado, las cajas
  etiquetadas de recursos/sesiones/estaciones pasan a etiqueta roja, y los
  assets oficiales quedan bajo `src/assets`. Se abren follow-ups de UX:
  `#102`, `#103`, `#104`.
- `references`: `src/frosthaven_campaign_journal/ui/common/theme/colors.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/temporal_bar.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/shell_view.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`,
  `docs/resource-ui-catalog.md`,
  `src/assets/resource-icons/`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/102`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/103`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/104`

### DEC-0047

- `date`: 2026-03-05
- `status`: accepted
- `problem`: tras aplicar acento rojo global en `DEC-0046`, la barra superior y
  las etiquetas de grupo quedaron demasiado llamativas y las semanas cerradas
  perdieron legibilidad por contraste de texto insuficiente.
- `decision`: reducir el acento rojo a `FAB` y semana seleccionada; pasar
  etiquetas de grupo y botones de año a estilo claro (fondo blanco con borde y
  texto rojos); aumentar legibilidad de semanas cerradas; y añadir borde visible
  a semanas abiertas y seleccionada.
- `rationale`: mejora equilibrio visual y jerarquía de foco (acción principal y
  selección activa) sin perder identidad de acento ni alterar layout/flujo.
- `impact`: `colors.py` incorpora semánticos explícitos para borde/texto de
  navegación anual, borde de semana abierta y contraste de cerradas; en
  `temporal_bar.py` los botones de año pasan a radio `16` con borde y texto
  rojos, y las tiles abiertas/seleccionada muestran borde visible.
- `references`: `src/frosthaven_campaign_journal/ui/common/theme/colors.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/temporal_bar.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/shell_view.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/status_bar.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`

### DEC-0048

- `date`: 2026-03-05
- `status`: accepted
- `problem`: en la barra temporal, los bordes de las tiles de semana añadían
  ruido visual y el color de semanas abiertas no diferenciaba bien el estado
  respecto al resto.
- `decision`: retirar borde en todos los botones de semana y ajustar el color
  de semanas abiertas a un tono azul claro más visible.
- `rationale`: prioriza lectura rápida del strip semanal y reduce saturación de
  contornos en un área con alta densidad de elementos.
- `impact`: `temporal_bar.py` deja de renderizar bordes en tiles y
  `colors.py` actualiza `WEEK_TILE_BG` para mejorar diferenciación de semanas
  abiertas.
- `references`: `src/frosthaven_campaign_journal/ui/main_shell/view/temporal_bar.py`,
  `src/frosthaven_campaign_journal/ui/common/theme/colors.py`

### DEC-0049

- `date`: 2026-03-05
- `status`: accepted
- `problem`: la tarjeta de `Entry` mantenía estructura vertical poco eficiente
  para recursos/sesiones, con caja contenedora adicional de recursos y botones
  de guardar/deshacer fuera de la barra principal de acciones.
- `decision`: mover `guardar/deshacer recursos` a la barra de iconos del header
  de la entrada, eliminar la caja contenedora `Recursos`, y reordenar secciones
  en tres filas: `Otros+Materiales`, `Plantas`, `Sesiones`.
- `rationale`: reduce fricción operativa en edición rápida por entrada, mejora
  jerarquía de acciones y aprovecha mejor el ancho disponible en tablet/web.
- `impact`: `center_focus.py` compone grupos de recursos por fila (sin wrapper
  `Recursos`), mantiene errores de recursos visibles sobre la primera fila y
  aplica estilo visual de cajas `status bar` a `Otros`, `Materiales`, `Plantas`
  y `Sesiones`.
- `references`: `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/status_bar.py`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/106`

### DEC-0050

- `date`: 2026-03-05
- `status`: accepted
- `problem`: la estrategia de `.apk` para Android estaba definida de forma
  genérica en `docs/repo-workflow.md`, pero faltaba un flujo operativo
  reproducible con comandos, evidencias y convención de assets para cerrar
  implementación de releases manuales.
- `decision`: formalizar un flujo manual oficial de release Android en
  `docs/android-release-flow.md`, introducir contrato de empaquetado Flet en
  `pyproject.toml` y fijar convención de assets de build en `src/assets/`
  (`icon.png`, `icon_android.png`, `splash.png`, `splash_android.png`).
- `rationale`: permite cerrar `#105` con trazabilidad completa sin depender de
  CI ni de secretos remotos, manteniendo un camino estable para distribución
  directa por `.apk`.
- `impact`: se habilita build local reproducible con `flet build apk`,
  verificación por hash del artefacto y adjunto manual a GitHub Releases; se
  actualizan `docs/repo-workflow.md`, `docs/system-map.md` y `CHANGELOG.md`.
- `references`: `docs/android-release-flow.md`, `pyproject.toml`,
  `docs/repo-workflow.md`, `docs/system-map.md`, `CHANGELOG.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/105`

### DEC-0051

- `date`: 2026-03-05
- `status`: accepted
- `problem`: el APK publicado en `v0.2.0` no pudo conectar con Firestore en
  Android porque el runtime empaquetado no incluía `.env` ni archivo local de
  `GOOGLE_APPLICATION_CREDENTIALS`.
- `decision`: añadir fallback de secretos móviles embebidos en runtime
  (`_mobile_runtime_secrets.py` generado en build), mantener precedencia de
  `.env`/entorno en desktop-web, y formalizar script operativo
  `scripts/build-android-with-mobile-secrets.ps1` para release `v0.2.1`.
- `rationale`: permite resolver el bloqueo de conectividad Android de forma
  táctica y reproducible sin activar backend intermedio ni CI adicional.
- `impact`: `settings.py` pasa a resolver configuración en dos capas
  (entorno/.env -> secretos móviles embebidos); el build Android puede inyectar
  credenciales desde `.secrets/firestore-mobile-rw.json`; se actualiza flujo
  oficial en `docs/android-release-flow.md` con advertencia de riesgo y
  rotación obligatoria post-release.
- `references`: `src/frosthaven_campaign_journal/config/settings.py`,
  `src/frosthaven_campaign_journal/data/firestore_client.py`,
  `scripts/build-android-with-mobile-secrets.ps1`,
  `docs/android-release-flow.md`, `CHANGELOG.md`

### DEC-0052

- `date`: 2026-03-06
- `status`: accepted
- `problem`: tras la compactación previa de la shell tablet, la tarjeta de
  `Entry` seguía dejando demasiado hueco vertical entre título y recursos, los
  controles de delta desperdiciaban ancho y las etiquetas rojas competían
  visualmente con la semana seleccionada/FAB en un viewport contractual
  `2560x1600` landscape.
- `decision`: compactar la geometría de `LabeledGroupBox` y de la tarjeta de
  `Entry`, rehacer `ResourceDeltaRow` con una zona fija derecha para `- valor +`
  y una zona izquierda expandible con truncado seguro, pasar etiquetas de grupo
  y botones de año a azul claro con texto oscuro, y alinear `Eliminar entrada`
  con el color claro del resto del popup.
- `rationale`: recupera densidad útil en tablet sin reintroducir lógica
  responsive por viewport, mantiene el rojo reservado para focos activos
  principales y evita solapes entre etiqueta, total proyectado y delta.
- `impact`: `center_focus.py` reduce padding/spacing en la tarjeta semanal y en
  las cajas de recursos/sesiones; `resource_delta_row.py` fija una huella más
  compacta para los botones `+/-` y el valor; `colors.py` redefine los
  semánticos de etiquetas y navegación anual hacia la paleta azul; y
  `labeled_group_box.py` reduce el overlap superior por defecto.
- `references`: `src/frosthaven_campaign_journal/ui/common/components/labeled_group_box.py`,
  `src/frosthaven_campaign_journal/ui/common/resources/resource_delta_row.py`,
  `src/frosthaven_campaign_journal/ui/common/theme/colors.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/temporal_bar.py`,
  `https://www.mi.com/global/product/xiaomi-pad-5/specs`
### DEC-0053

- `date`: 2026-03-06
- `status`: accepted
- `problem`: `main_shell` mostraba mensajes informativos y confirmaciones como bloques inline en el panel central, ocupando espacio útil y mezclando feedback transitorio con edición persistente.
- `decision`: mover mensajes informativos a `SnackBar` flotante y preguntas de confirmación a `AlertDialog` modal, manteniendo `MainShellState` como fuente de verdad y concentrando el bridge hacia overlays de Flet en `ui/app_root.py` mediante `event_id` transitorios.
- `rationale`: separa feedback efímero del contenido principal, evita acoplar la capa de estado a `Page`, y permite reemitir el mismo mensaje o la misma confirmación sin perder eventos por igualdad de contenido.
- `impact`: `model.py` y `view_data.py` dejan de exponer `info_message`/confirmación inline; `app_root.py` pasa a abrir/cerrar overlays; los botones del diálogo heredan la paleta del FAB; y se añaden tests para `toast_state`/`confirmation_state` con `event_id`.
- `references`: `src/frosthaven_campaign_journal/ui/app_root.py`, `src/frosthaven_campaign_journal/ui/main_shell/state/types.py`, `src/frosthaven_campaign_journal/ui/main_shell/state/runtime_support.py`, `src/frosthaven_campaign_journal/ui/main_shell/view/center_panel.py`, `docs/ui-main-shell-architecture-mvs.md`, `CHANGELOG.md`

### DEC-0054

- `date`: 2026-03-06
- `status`: accepted
- `problem`: la tarjeta de `Entry` seguía separando demasiado la operativa de sesiones entre botones redundantes dentro de la caja `Sesiones` y ausencia de resumen visible de la sesión activa global en la barra inferior.
- `decision`: mover el `play/stop` rápido al header de cada tarjeta de `Entry`, compactar la caja `Sesiones` a formato resumen con total jugado + listado manual editable, y recuperar en la barra inferior una caja fija de sesión activa global con reloj vivo `hh:mm:ss` y subtítulo `{Entry activa} · Semana X`.
- `rationale`: mejora jerarquía visual, acerca la acción frecuente al título de la entrada, y hace visible el estado de sesión activa aunque el usuario navegue por otra `Week`/`Entry`.
- `impact`: supersede parcialmente `DEC-0045` en el punto que dejó la barra inferior solo para recursos; `center_focus.py` reordena acciones y filas de sesiones; `status_bar.py` vuelve a mostrar resumen activo; y `docs/active-session-flow.md` se alinea con la nueva ubicación del control rápido.
- `references`: `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`, `src/frosthaven_campaign_journal/ui/main_shell/view/status_bar.py`, `src/frosthaven_campaign_journal/ui/main_shell/view/session_timing.py`, `docs/active-session-flow.md`, `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/103`

### DEC-0055

- `date`: 2026-03-06
- `status`: accepted
- `problem`: existía flujo manual de release Android y convención `v0.x.y`,
  pero faltaba un procedimiento determinista para ejecutar una release diaria
  desde Codex App sin ocultar la lógica dentro de un script versionado.
- `decision`: las releases GitHub se operan manualmente por Codex en sesión,
  lanzando los comandos necesarios de validación, build, git y `gh` sobre
  `main` limpio y sincronizado; `CHANGELOG.md` es la fuente de verdad para las
  notas en Markdown y no se versiona ningún script de release en el repo.
- `rationale`: mantiene el control explícito del flujo en cada sesión, evita
  lógica opaca o divergente en scripts de release y deja la publicación
  completamente auditable en la conversación y en el historial Git.
- `impact`: se añade `docs/github-release-automation.md`, se actualizan
  `docs/system-map.md` y `docs/repo-workflow.md`, Codex App pasa a ejecutar la
  release con comandos directos y `scripts/build-android-with-mobile-secrets.ps1`
  queda acotado a helper de build Android, no de publicación.
- `references`: `docs/github-release-automation.md`,
  `docs/android-release-flow.md`,
  `scripts/build-android-with-mobile-secrets.ps1`,
  `docs/repo-workflow.md`, `docs/system-map.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/114`
