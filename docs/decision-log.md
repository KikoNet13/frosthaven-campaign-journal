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
