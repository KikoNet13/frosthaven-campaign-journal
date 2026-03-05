# Registro de Decisiones

## Metadatos

- `doc_id`: DOC-DECISION-LOG
- `purpose`: Registrar decisiones con trazabilidad y precedencia.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-12

## Formato canÃ³nico por entrada

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
- `decision`: priorizar aprendizaje de ingenierÃ­a de contexto.
- `rationale`: objetivo explÃ­cito del proyecto.
- `impact`: Fase 0 sin cÃ³digo funcional de app.
- `references`: `important.txt`

### DEC-0002

- `date`: 2026-02-20
- `status`: accepted
- `problem`: separar operaciÃ³n y aprendizaje.
- `decision`: usar `docs/` para operaciÃ³n y `learning/` para aprendizaje.
- `rationale`: mejorar foco y reutilizaciÃ³n.
- `impact`: estructura dual de documentaciÃ³n.
- `references`: `important.txt`

### DEC-0003

- `date`: 2026-02-20
- `status`: accepted
- `problem`: definir mantenimiento del contexto.
- `decision`: mantenimiento manual con checklist.
- `rationale`: baja complejidad inicial y alta claridad.
- `impact`: IA actualiza y Kiko valida por hito.
- `references`: conversaciÃ³n de planificaciÃ³n

### DEC-0004

- `date`: 2026-02-20
- `status`: accepted
- `problem`: evitar implementaciÃ³n prematura.
- `decision`: gate estricto antes de cÃ³digo.
- `rationale`: prevenir deuda de contexto.
- `impact`: bloqueo si faltan decisiones o checklist.
- `references`: `summary_initial_conversation.txt`

### DEC-0005

- `date`: 2026-02-20
- `status`: accepted
- `problem`: coherencia de idioma.
- `decision`: descripciones en castellano e identificadores tÃ©cnicos en inglÃ©s.
- `rationale`: claridad para aprendizaje y precisiÃ³n tÃ©cnica.
- `impact`: regla transversal de documentaciÃ³n.
- `references`: `summary_initial_conversation.txt`

### DEC-0006

- `date`: 2026-02-20
- `status`: accepted
- `problem`: gestiÃ³n del legado inicial.
- `decision`: convivencia temporal sin borrado en Fase 0.
- `rationale`: preservar contexto histÃ³rico.
- `impact`: precedencia oficial y registro de conflictos.
- `references`: `summary_initial_conversation.txt`, `tdd.md`, `important.txt`

### DEC-0007

- `date`: 2026-02-20
- `status`: accepted
- `problem`: reducir riesgo de alucinaciones.
- `decision`: verificaciÃ³n doble en cada hito.
- `rationale`: equilibrio entre rigor y coste.
- `impact`: evidencia obligatoria en gobierno de contexto.
- `references`: `neil.txt`

### DEC-0008

- `date`: 2026-02-20
- `status`: accepted
- `problem`: continuidad entre sesiones.
- `decision`: cierre con menÃº numerado de 3 a 5 pasos.
- `rationale`: facilita acciÃ³n inmediata.
- `impact`: estÃ¡ndar de cierre conversacional.
- `references`: conversaciÃ³n de planificaciÃ³n

### DEC-0009

- `date`: 2026-02-20
- `status`: accepted
- `problem`: conflictos entre legado y oficial.
- `decision`: prevalece la documentaciÃ³n oficial.
- `rationale`: fuente de verdad Ãºnica.
- `impact`: conflicto siempre registrado en este documento.
- `references`: `summary_initial_conversation.txt`, `tdd.md`

### DEC-0010

- `date`: 2026-02-20
- `status`: accepted
- `problem`: mezcla de objetivos en borradores.
- `decision`: separar explÃ­citamente producto y aprendizaje.
- `rationale`: menor ambigÃ¼edad de alcance.
- `impact`: navegaciÃ³n y mantenimiento mÃ¡s simples.
- `references`: `important.txt`, `tdd.md`, `neil.txt`

### DEC-0011

- `date`: 2026-02-20
- `status`: accepted
- `problem`: cerrar alcance MVP funcional antes de modelado de dominio.
- `decision`: aprobar alcance MVP v1 con lista de incluye/no incluye y
  criterios de Ã©xito.
- `rationale`: reducir ambigÃ¼edad y evitar cambios de alcance durante
  implementaciÃ³n inicial.
- `impact`: queda cerrada la Issue #5 y se habilita trabajo de Issue #6.
- `references`: `tdd.md`, `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/5`

### DEC-0012

- `date`: 2026-02-20
- `status`: accepted
- `problem`: cerrar modelo de dominio e invariantes de la Issue #6 sin abrir
  decisiones de implementaciÃ³n.
- `decision`: adoptar modelo unificado `Entry` (`scenario|outpost`) con
  jerarquÃ­a temporal explÃ­cita `campaign > year > season > week > entry`.
- `rationale`: reducir complejidad del dominio y evitar duplicaciÃ³n de
  estructura en `Session` y `ResourceChange`.
- `impact`: contrato de dominio cerrado en `docs/domain-glossary.md`; se
  elimina necesidad de `owner_type` en entidades hijas.
- `references`: `docs/domain-glossary.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/6`

### DEC-0013

- `date`: 2026-02-23
- `status`: accepted
- `problem`: falta una estrategia de sincronizaciÃ³n multidispositivo para el
  MVP con simplicidad operativa y consistencia explÃ­cita.
- `decision`: adoptar una estrategia MVP de sincronizaciÃ³n con Firestore como
  fuente de verdad, modo operativo recomendado `single writer`, escrituras
  `online-only` y actualizaciÃ³n remota `on-demand refresh`.
- `rationale`: reduce complejidad inicial, alinea expectativas del MVP y
  separa claramente la estrategia general de las decisiones especÃ­ficas de
  conflictos (#8) y orden/timestamps (#18).
- `impact`: deja trazable el comportamiento esperado en uso normal, explicita
  lÃ­mites aceptados del MVP y habilita la especificaciÃ³n de conflictos,
  timestamps y contrato de operaciones Firestore por agregado.
- `references`: `docs/sync-strategy.md`, `docs/domain-glossary.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/7`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`

### DEC-0014

- `date`: 2026-02-23
- `status`: accepted
- `problem`: hay ambigÃ¼edad operativa sobre el uso de `main`, el momento de
  cierre de Issues cuando el trabajo va en rama y la prioridad entre PRs e
  Issues al pedir â€œsiguiente pasoâ€.
- `decision`: mantener PR obligatoria para cambios relevantes; cerrar la Issue
  asociada tras merge/integraciÃ³n en `main` cuando el trabajo va en rama;
  tratar `siguiente pendiente` y `siguiente issue pendiente` como equivalentes;
  y priorizar PRs abiertas (incluyendo `draft`) antes de pasar a la siguiente
  Issue pendiente al pedir `siguiente paso`.
- `rationale`: reduce ambigÃ¼edad de ejecuciÃ³n, evita cierres tempranos como el
  caso de la Issue #7 y deja una regla de priorizaciÃ³n conversacional
  determinista.
- `impact`: estandariza el flujo de cierre en trabajo con rama y el orden de
  priorizaciÃ³n entre PRs e Issues; mejora trazabilidad de sesiones con Codex.
- `references`: `AGENTS.md`, `docs/repo-workflow.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/7`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/22`

### DEC-0015

- `date`: 2026-02-23
- `status`: accepted
- `problem`: falta una polÃ­tica de conflictos concurrentes para operaciones
  simultÃ¡neas sobre `entries`, `sessions`, `weeks` y `resource_changes` en el
  MVP con Firestore.
- `decision`: adoptar una polÃ­tica MVP estricta de rechazo en conflicto con
  `refresco` y `reintento`, sin `last-write-wins`, aplicada por familias de
  operaciÃ³n (estado crÃ­tico, `Week.notes` y `ResourceChange`), y diferir el
  mecanismo tÃ©cnico exacto de detecciÃ³n/validaciÃ³n a la Issue #12.
- `rationale`: prioriza previsibilidad y consistencia del estado frente a
  sobrescrituras silenciosas, y mantiene bajo control la complejidad antes de
  cerrar el contrato tÃ©cnico por agregado (#12) y la polÃ­tica de
  timestamps/desempates (#18).
- `impact`: cierra la Issue #8 a nivel de polÃ­tica, condiciona la definiciÃ³n de
  operaciones por agregado en #12 y la compatibilidad con orden estable en #18.
- `references`: `docs/conflict-policy.md`, `docs/sync-strategy.md`,
  `docs/domain-glossary.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`

### DEC-0016

- `date`: 2026-02-23
- `status`: accepted
- `problem`: faltaba una regla explÃ­cita de ortografÃ­a en castellano (`tildes`,
  `Ã±` y signos correctos), codificaciÃ³n `UTF-8` y limpieza sistemÃ¡tica de
  ramas locales/remotas tras merge/cierre.
- `decision`: adoptar ortografÃ­a completa en castellano para issues, PR,
  documentaciÃ³n y futuros textos de UI; usar `UTF-8` para archivos de texto;
  y limpiar por defecto ramas locales/remotas mergeadas no reutilizables tras
  cada merge/cierre, con exclusiones documentadas.
- `rationale`: mejora consistencia textual, evita correcciones errÃ³neas por
  mojibake visual de terminal y reduce ruido operativo por ramas ya integradas.
- `impact`: se actualizan `AGENTS.md`, `docs/repo-workflow.md`,
  `CONTRIBUTING.md`, plantillas `.github`, checklists operativas y se aÃ±ade
  `.editorconfig` para reforzar `UTF-8`.
- `references`: `AGENTS.md`, `docs/repo-workflow.md`, `CONTRIBUTING.md`,
  `docs/context-checklists.md`, `.github/pull_request_template.md`,
  `.github/ISSUE_TEMPLATE/decision.md`, `.github/ISSUE_TEMPLATE/task.md`,
  `.github/ISSUE_TEMPLATE/bug.md`, `.editorconfig`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/25`

### DEC-0017

- `date`: 2026-02-23
- `status`: accepted
- `problem`: el diseÃ±o de ajustes de campaÃ±a para provisiÃ³n de aÃ±os quedÃ³
  desalineado con el nuevo enfoque de pantalla Ãºnica con selector temporal
  superior.
- `decision`: reencuadrar la Issue #9 para definir controles temporales de
  campaÃ±a en la barra superior (selector de aÃ±o/semana), provisiÃ³n inicial
  automÃ¡tica de 4 aÃ±os, extensiÃ³n manual `+1` con confirmaciÃ³n, patrÃ³n de
  selector de entry en popover anclado y ajuste manual explÃ­cito de
  `week_cursor` separado de la navegaciÃ³n de semanas.
- `rationale`: simplifica la UI principal, evita una pantalla de ajustes
  separada solo para aÃ±os y mantiene coherencia con el modelo de pantalla Ãºnica
  del MVP.
- `impact`: cambia el corte funcional de la Issue #9 respecto a #13 y #14;
  exige alinear `week_cursor` en `docs/domain-glossary.md` y su polÃ­tica de
  conflicto en `docs/conflict-policy.md`.
- `references`: `docs/campaign-temporal-controls.md`, `docs/domain-glossary.md`,
  `docs/conflict-policy.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/9`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`

### DEC-0018

- `date`: 2026-02-23
- `status`: accepted
- `problem`: habÃ­a ambigÃ¼edad entre responder cuÃ¡l era el â€œsiguiente pasoâ€ y
  ejecutar ese siguiente paso en la misma sesiÃ³n.
- `decision`: cuando Kiko pide `siguiente paso`, Codex identifica el trabajo
  prioritario y lo ejecuta por defecto en la misma pasada, manteniendo la
  prioridad vigente (PRs abiertas, incluyendo `draft`, antes que issues). Si no
  hay PRs abiertas, se resuelve la siguiente issue pendiente.
- `rationale`: reduce fricciÃ³n conversacional, evita intercambios innecesarios y
  alinea la operaciÃ³n con el objetivo de avanzar de punta a punta en cada turno.
- `impact`: se actualizan `docs/repo-workflow.md` y `AGENTS.md` para reflejar
  el comportamiento por defecto y sus excepciones (`Plan Mode`, bloqueo real,
  peticiÃ³n explÃ­cita de solo plan/anÃ¡lisis).
- `references`: `AGENTS.md`, `docs/repo-workflow.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/28`

### DEC-0019

- `date`: 2026-02-23
- `status`: accepted
- `problem`: priorizar por nÃºmero de Issue al pedir `siguiente paso` ignora el
  orden tÃ©cnico del checklist cuando ya existe una secuencia recomendada
  documentada para la Fase 1.
- `decision`: mantener prioridad de PRs abiertas (incluyendo `draft`) y, si no
  hay PRs, priorizar el orden tÃ©cnico recomendado en documentaciÃ³n oficial
  aplicable usando la fuente mÃ¡s especÃ­fica (detalle > macro). Si una Issue del
  orden tÃ©cnico no es cerrable, se salta a la siguiente cerrable; si no hay
  cerrables, se toma la primera `draftable`. Solo si no existe orden tÃ©cnico
  aplicable se usa la Issue abierta de nÃºmero mÃ¡s bajo.
- `rationale`: alinea la ejecuciÃ³n conversacional con la secuencia tÃ©cnica
  documentada, reduce saltos de contexto y evita priorizaciones por nÃºmero que
  aumentan el retrabajo.
- `impact`: actualiza la selecciÃ³n de `siguiente paso` en Fase 1 (por ejemplo,
  puede priorizar `#13` antes de `#12`); mantiene sin cambios `siguiente
  pendiente`/`siguiente issue pendiente` y la regla de ejecuciÃ³n por defecto de
  `siguiente paso`.
- `references`: `AGENTS.md`, `docs/repo-workflow.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/32`

### DEC-0020

- `date`: 2026-02-24
- `status`: accepted
- `problem`: habÃ­a ambigÃ¼edad en la traducciÃ³n de `season` (usada como
  â€œtemporadaâ€) y faltaba fijar el template temporal exacto para cerrar la
  especificaciÃ³n tÃ©cnica de inicializaciÃ³n de `year/season/week` (Issue #13).
- `decision`: traducir `season` como **estaciÃ³n** (verano e invierno, en ese
  orden) en la documentaciÃ³n en castellano, y fijar para el MVP un template
  temporal determinista de `4` aÃ±os iniciales, `2` estaciones por aÃ±o
  (`summer`, `winter`) y `10` semanas por estaciÃ³n, con extensiÃ³n manual de
  `+1` aÃ±o desde el control de cambio de aÃ±o.
- `rationale`: elimina ambigÃ¼edad terminolÃ³gica, evita investigar un calendario
  externo innecesario para la Fase 1 y deja una base tÃ©cnica cerrable para
  `#13` que reduce retrabajo en `#12`, `#16` y `#20`.
- `impact`: habilita documentar `docs/campaign-temporal-initialization.md` como
  contrato tÃ©cnico temporal del MVP; corrige terminologÃ­a en documentaciÃ³n
  oficial relacionada y fija cardinalidades mÃ­nimas de creaciÃ³n temporal.
- `references`: `docs/campaign-temporal-controls.md`,
  `docs/campaign-temporal-initialization.md`, `docs/domain-glossary.md`,
  `docs/mvp-implementation-blocks.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`

### DEC-0021

- `date`: 2026-02-24
- `status`: accepted
- `problem`: la regla de `siguiente paso` priorizaba PRs abiertas y orden
  tÃ©cnico, pero no contemplaba explÃ­citamente unidades ya iniciadas con trabajo
  local/remoto pendiente de cierre (por ejemplo commits sin `push` o rama sin
  PR), lo que podÃ­a dejar tareas a medias y permitir avanzar al siguiente
  trabajo.
- `decision`: redefinir `siguiente paso` para que primero detecte y resuelva una
  **unidad pendiente de cierre** antes de iniciar trabajo nuevo; adoptar por
  defecto un cierre end-to-end (commit, `push`, PR, merge/cierre, cierre de
  Issue y limpieza de rama cuando aplique); y documentar el manejo de
  bloqueos por aprobaciÃ³n en `type:decision` y el comportamiento especÃ­fico en
  `Plan Mode`.
- `rationale`: alinea la ejecuciÃ³n con la expectativa de cierre real por unidad,
  reduce riesgo de trabajo huÃ©rfano en ramas locales/remotas y corrige el hueco
  observado en el caso de la Issue `#13` antes de su PR `#34`.
- `impact`: se actualizan `AGENTS.md`, `docs/repo-workflow.md` y
  `docs/context-checklists.md`; `siguiente paso` pasa a priorizar pendientes de
  cierre (incluyendo trabajo local sin publicar) antes de PRs abiertas y orden
  tÃ©cnico; el reporte de sesiÃ³n debe indicar estado de cierre alcanzado y
  bloqueo si existe.
- `references`: `AGENTS.md`, `docs/repo-workflow.md`,
  `docs/context-checklists.md`, `docs/decision-log.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/35`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/pull/34`

### DEC-0022

- `date`: 2026-02-24
- `status`: accepted
- `problem`: el dominio del MVP quedÃ³ demasiado restrictivo para el objetivo de
  trabajo â€œcomo papelâ€: no permitÃ­a reordenaciÃ³n manual de `Entry`, no definÃ­a
  correcciones manuales amplias de `Session` ni `Week.reopen/reclose`, y
  mantenÃ­a una semÃ¡ntica de `week_cursor` incompatible con esa editabilidad
  ampliada, lo que bloqueaba la redacciÃ³n coherente de la Issue #12.
- `decision`: introducir una polÃ­tica marco de editabilidad manual del MVP
  (`docs/editability-policy.md`, Issue #37) que permite reordenaciÃ³n manual de
  `Entry` dentro de la misma `Week` con `order_index` denso `1..N`, habilita
  correcciones manuales de `Week.status` (`reopen/reclose`) y correcciones
  manuales completas de `Session` (crear/editar/borrar, incluyendo timestamps),
  manteniendo la invariante de `0..1` sesiÃ³n activa global; ademÃ¡s, redefinir
  `campaign.week_cursor` para que apunte siempre a la primera `Week` abierta
  (menor `week_number` abierta) y rechazar operaciones que dejen `0` weeks
  abiertas provisionadas.
- `rationale`: permite un flujo de trabajo mÃ¡s flexible y cercano a papel sin
  perder invariantes crÃ­ticos, y separa correctamente la decisiÃ³n de dominio
  (editabilidad/cursor) del contrato tÃ©cnico Firestore por agregado (Issue #12).
- `impact`: actualiza `docs/domain-glossary.md`, `docs/conflict-policy.md`,
  `docs/campaign-temporal-controls.md`, `docs/campaign-temporal-initialization.md`
  y el orden tÃ©cnico en `docs/mvp-implementation-checklist.md` /
  `docs/mvp-implementation-blocks.md`; aÃ±ade `docs/editability-policy.md` como
  fuente oficial; desplaza la ejecuciÃ³n de `#12` para despuÃ©s de `#37`.
- `references`: `docs/editability-policy.md`, `docs/domain-glossary.md`,
  `docs/conflict-policy.md`, `docs/campaign-temporal-controls.md`,
  `docs/campaign-temporal-initialization.md`,
  `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`

### DEC-0023

- `date`: 2026-02-24
- `status`: accepted
- `problem`: la Issue `#12` necesitaba un contrato tÃ©cnico por agregado que
  integrara simultÃ¡neamente la temporalidad detallada (`#13`) y la nueva
  polÃ­tica de editabilidad manual (`#37`), incluyendo una distinciÃ³n explÃ­cita
  entre conflictos concurrentes y rechazos funcionales por transiciÃ³n invÃ¡lida.
- `decision`: aceptar `docs/firestore-operation-contract.md` como contrato
  oficial de operaciones Firestore por agregado del MVP; tratar
  `campaign.week_cursor` como efecto derivado (postcondiciÃ³n) y declarar
  `Campaign.set_week_cursor_manual` como operaciÃ³n excluida del contrato activo
  del MVP; modelar `Session` por timestamps (`started_at_utc`, `ended_at_utc`)
  con actividad derivada (`ended_at_utc=null`); permitir mutaciones de
  `Entry/Session/ResourceChange` tambiÃ©n en weeks `closed`; documentar
  `auto-stop + cerrar` en `Week.close/reclose` cuando haya sesiÃ³n activa; y
  distinguir en el contrato (y la polÃ­tica de conflictos alineada) entre
  `conflicto`, `validacion` y `transicion_invalida`.
- `rationale`: reduce ambigÃ¼edad de implementaciÃ³n antes de codificar, evita
  contradicciones con `#37`, y hace explÃ­cito el comportamiento esperado ante
  errores funcionales que no son conflictos concurrentes reales.
- `impact`: aÃ±ade `docs/firestore-operation-contract.md` como fuente oficial;
  actualiza `docs/conflict-policy.md` para reflejar la distinciÃ³n
  conflicto/transiciÃ³n invÃ¡lida; desbloquea el cierre de `#14`, `#15`, `#16`,
  `#17`, `#18` y `#19` con una base contractual comÃºn; actualiza seguimiento en
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
  por `Entry`) quedÃ³ desalineado con la intenciÃ³n de ediciÃ³n manual "como
  papel", y dejaba complejidad innecesaria en contratos y conflictos justo
  antes de cerrar la polÃ­tica de timestamps/orden estable (`#18`).
- `decision`: sustituir `ResourceChange` como entidad MVP por un campo
  `Entry.resource_deltas` con tipo lÃ³gico `map<resource_key, int>` y semÃ¡ntica
  de delta neto editable por recurso dentro de cada `Entry`; mantener solo
  claves con delta `!= 0` (ausencia de clave = `0`), eliminar la clave cuando
  el delta neto resulte `0`, reutilizar Ãºnicamente la auditorÃ­a de `Entry` (sin
  timestamps por recurso) y parchear `docs/firestore-operation-contract.md`
  para reemplazar `ResourceChange.*` por operaciones sobre
  `Entry.resource_deltas` sin reabrir la Issue `#12`.
- `rationale`: simplifica el modelo de dominio y la ediciÃ³n de recursos en el
  MVP, alinea el comportamiento con la editabilidad amplia definida en `#37`,
  reduce complejidad de concurrencia/contratos y evita arrastrar un log
  incremental intra-entry que no aporta valor al MVP actual.
- `impact`: aÃ±ade `docs/resource-delta-model.md` como fuente oficial; elimina
  `ResourceChange` del glosario MVP activo; actualiza `docs/conflict-policy.md`
  y parchea parcialmente `docs/firestore-operation-contract.md` (supersesiÃ³n
  parcial de la parte de recursos de `DEC-0023`); reordena el bloque tÃ©cnico
  para ejecutar esta decisiÃ³n antes de `#18`, y deja `#18` como siguiente paso
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
- `problem`: faltaba una polÃ­tica oficial de timestamps de auditorÃ­a y
  desempate de orden estable entre dispositivos para evitar divergencias
  visuales en listas del MVP (timeline, sesiones y selectores), y seguÃ­an
  abiertas decisiones sobre `deleted_at_utc`, orden canÃ³nico y reparto
  query/cliente.
- `decision`: aceptar `docs/timestamp-order-policy.md` como polÃ­tica oficial de
  timestamps y orden estable del MVP; usar `created_at_utc` y `updated_at_utc`
  como timestamps de auditorÃ­a **server-only**; eliminar `deleted_at_utc` del
  MVP (hard delete real); ampliar auditorÃ­a temporal a
  `campaign/year/season/week/entry/session`; actualizar `updated_at_utc` en
  toda escritura persistida, tambiÃ©n derivada/sistÃ©mica; definir una matriz de
  orden canÃ³nico por lista (alcance UI + `#16`) con prefijo de query + orden
  canÃ³nico final en cliente; usar desempate final por `document_id`
  lexicogrÃ¡fico ascendente; priorizar orden de dominio (`week_number`,
  `order_index`) sobre timestamps cuando exista; y considerar que el orden final
  con `serverTimestamp` pendiente solo se garantiza tras `refresh`.
- `rationale`: separa claramente auditorÃ­a/orden estable de los contratos por
  operaciÃ³n (`#12`), reduce ambigÃ¼edad para `#16/#17/#19`, y deja reglas
  trazables para listas de dominio y listas temporales sin adelantar tÃ©cnica
  Firestore especÃ­fica.
- `impact`: aÃ±ade `docs/timestamp-order-policy.md` como fuente oficial;
  actualiza `docs/domain-glossary.md` (auditorÃ­a y eliminaciÃ³n de
  `deleted_at_utc`), `docs/firestore-operation-contract.md` (referencia a la
  polÃ­tica final de `#18`), y el seguimiento tÃ©cnico en
  `docs/mvp-implementation-checklist.md` / `docs/mvp-implementation-blocks.md`;
  deja `#14` como siguiente paso tÃ©cnico tras cerrar `#18`.
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
- `problem`: faltaba una especificaciÃ³n oficial del flujo cliente/UI de sesiÃ³n
  activa (`start/stop/auto-stop`) que cerrara la separaciÃ³n entre `current
  week`, selecciÃ³n (`Week`/`Entry`) y `Entry` activa, ademÃ¡s de la recuperaciÃ³n
  esperada ante `conflicto` vs `transicion_invalida`.
- `decision`: aceptar `docs/active-session-flow.md` como contrato oficial del
  flujo de sesiÃ³n activa del MVP; ubicar `Iniciar/Parar sesiÃ³n` en el bloque de
  la `Entry` seleccionada (no en barra inferior global); separar explÃ­citamente
  `current week` (marcador derivado de `week_cursor`) de selecciÃ³n/foco y de
  `Entry` activa; definir que cambiar foco no hace `auto-stop`; clasificar
  `Session.start` sobre la misma `Entry` activa como `transicion_invalida`
  (error local); mantener `auto-stop` como side-effect sin confirmaciÃ³n extra;
  y fijar recuperaciÃ³n de `conflicto` como `refresh` manual + reintentar.
- `rationale`: reduce ambigÃ¼edad de implementaciÃ³n para `#17/#19/#20`, alinea
  el comportamiento observable del cliente con `#12` (contrato por operaciÃ³n),
  `#37` (editabilidad e invariantes) y `#18` (refresh/orden estable), y evita
  confundir navegaciÃ³n/foco con estado activo global.
- `impact`: aÃ±ade `docs/active-session-flow.md` como fuente oficial; actualiza
  `docs/campaign-temporal-controls.md` para reforzar la separaciÃ³n entre
  `week_cursor/current week` y selecciÃ³n; actualiza tracking en
  `docs/mvp-implementation-checklist.md` y `docs/mvp-implementation-blocks.md`;
  deja `#15` como siguiente paso tÃ©cnico tras cerrar `#14`.
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
- `problem`: faltaban reglas documentales explÃ­citas para validar operaciones
  sobre `Entry.resource_deltas` y recalcular `campaign.resource_totals` de forma
  consistente, con clasificaciÃ³n clara de rechazos (`validacion` vs
  `conflicto`) y manejo de correcciones/borrados tras el cambio de modelo de
  recursos de `#40`.
- `decision`: aceptar `docs/resource-validation-recalculation.md` como contrato
  oficial de validaciÃ³n y recÃ¡lculo de recursos del MVP; cubrir
  `Entry.adjust_resource_delta`, `Entry.set_resource_delta`,
  `Entry.clear_resource_delta` y el impacto de recursos de `Entry.delete`;
  validar `resource_key` contra catÃ¡logo MVP, deltas enteros y no negatividad
  de totales finales; definir equivalencia de resultado con recÃ¡lculo desde
  `Entry.resource_deltas`; normalizar claves con valor `0` fuera de
  `entry.resource_deltas` y `campaign.resource_totals`; aceptar `clear` de clave
  inexistente y no-ops triviales (`adjust=0`, `set` al mismo valor) como
  idempotentes; y clasificar inconsistencias detectadas de base/totales como
  `conflicto` para forzar `refrescar + reintentar`.
- `rationale`: completa el detalle que `#12` dejÃ³ a nivel de contrato de
  comportamiento y que `#40` dejÃ³ a nivel de modelo, reduce ambigÃ¼edad para
  `#17/#19/#20` y mantiene coherencia con la polÃ­tica estricta de conflictos de
  `#8`.
- `impact`: aÃ±ade `docs/resource-validation-recalculation.md` como fuente
  oficial; actualiza referencias en glosario, conflictos, contrato Firestore y
  modelo de recursos; actualiza tracking en `docs/mvp-implementation-checklist.md`
  y `docs/mvp-implementation-blocks.md`; deja `#16` como siguiente paso tÃ©cnico.
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
- `problem`: tras cerrar `#15` se detectÃ³ que se habÃ­an documentado defaults de
  representaciÃ³n de `campaign.resource_totals` sin revisiÃ³n explÃ­cita de Kiko,
  dejando una normalizaciÃ³n de claves `0` que no coincidÃ­a con la intenciÃ³n
  final del dominio.
- `decision`: corregir parcialmente `DEC-0027` (sin reabrir `#15`) para que
  `campaign.resource_totals` conserve claves materializadas con valor `0` cuando
  una operaciÃ³n las deja en `0`, permitiendo a la vez ausencia de clave para
  recursos nunca usados; confirmar como contrato oficial que
  `Entry.adjust_resource_delta(adjustment_delta=0)`, `Entry.set_resource_delta`
  al mismo valor y `Entry.clear_resource_delta` sobre clave inexistente son
  no-ops idempotentes; y mantener la clasificaciÃ³n de drift/inconsistencia de
  base/totales como `conflicto` con `refrescar + reintentar`.
- `rationale`: preserva la trazabilidad del cierre de `#15` sin reescribir su
  historial, alinea la representaciÃ³n de totales con la revisiÃ³n posterior de
  Kiko y mantiene consistencia con `#8`, `#12` y `#40`.
- `impact`: actualiza `docs/resource-validation-recalculation.md` y
  `docs/domain-glossary.md` para reflejar la nueva regla de claves `0` en
  `campaign.resource_totals`; deja `Entry.resource_deltas` sin cambios
  (claves `0` no persistidas); y documenta explÃ­citamente la supersesiÃ³n parcial
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
- `problem`: faltaba una especificaciÃ³n oficial y trazable de consultas mÃ­nimas
  para la pantalla principal del MVP, y `#16` seguÃ­a descrita en tÃ©rminos de
  "timeline/panel de foco" sin cerrar el inventario de lecturas por superficie,
  triggers de carga y compatibilidad con `#18`.
- `decision`: aceptar `docs/minimal-read-queries.md` como contrato oficial de
  lecturas mÃ­nimas de pantalla principal para el MVP (`#16`), fijando:
  Figma compartido por Kiko como canon de layout/superficies para esta issue;
  arranque sin `Week`/`Entry` seleccionada (barra en el aÃ±o de `current week`);
  inventario de consultas Q1..Q8; carga diferida de sesiones hasta selecciÃ³n de
  `Entry`; y ausencia de paginaciÃ³n en MVP.
- `rationale`: reduce ambigÃ¼edad entre layout heredado (`tdd.md`) y diseÃ±o
  actual, alinea lecturas con `#9`, `#14`, `#15`, `#18` y `#12`, y deja una
  base ejecutable para implementaciÃ³n sin listeners realtime ni sobrecargar el
  modelo con lecturas innecesarias.
- `impact`: cierra `#16`; actualiza tracking y trazabilidad (`AGENTS.md`,
  `docs/system-map.md`, checklist y blocks); y aÃ±ade referencias cruzadas en
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
  escenarios verificables para concurrencia/sincronizaciÃ³n, con severidad y
  prioridad trazables hacia `#19` / `#20`.
- `decision`: aceptar `docs/concurrency-sync-edge-case-matrix.md` como matriz
  oficial de edge cases del MVP (`#17`), con alcance mixto (concurrencia/sync +
  `transicion_invalida`/`validacion` cuando afectan el mismo flujo), cobertura
  de lecturas crÃ­ticas solamente, formato en 2 capas (escenarios canÃ³nicos +
  variantes por operaciÃ³n/evento), y esquema de riesgo en 3 campos
  (`severidad`, `impacto`, `prioridad_verificacion`).
- `rationale`: reduce ambigÃ¼edad antes del plan de pruebas (`#19`), evita
  duplicar diseÃ±o de pruebas en `#17`, y crea una base Ãºnica para priorizar
  verificaciÃ³n de invariantes/recuperaciÃ³n sin reabrir decisiones de dominio.
- `impact`: cierra `#17`; aÃ±ade una fuente oficial de edge cases reutilizable
  por `#19/#20`; actualiza tracking en checklist/bloques; y conecta
  sincronizaciÃ³n, conflictos, contrato por agregado, flujo de sesiÃ³n, lecturas
  mÃ­nimas y polÃ­tica de orden mediante referencias cruzadas.
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
  gate `#20`, con evidencia mÃ­nima y reglas de repetibilidad, sin exigir aÃºn
  ejecuciÃ³n real previa al inicio de cÃ³digo.
- `decision`: aceptar `docs/domain-invariant-test-plan.md` como plan oficial de
  pruebas para invariantes de dominio del MVP (`#19`), con catÃ¡logo `INV-*`,
  casos `TC-*`, trazabilidad obligatoria a `EC-*` de `#17`, priorizaciÃ³n para
  `#20` (`P0/P1/P2`), plantilla mÃ­nima de evidencia y alcance de ejecuciÃ³n
  previo al gate limitado a `single device`, dejando la concurrencia
  multi-dispositivo real como diferido explÃ­cito.
- `rationale`: reduce ambigÃ¼edad en readiness, evita confundir definiciÃ³n de
  pruebas con ejecuciÃ³n real antes de tener cÃ³digo, y permite que `#20` evalÃºe
  cobertura bloqueante (`P0`) sobre un plan trazable en lugar de sobre criterios
  ad hoc.
- `impact`: cierra `#19`; establece el contrato documental de QA/readiness para
  invariantes; enlaza `#17` con `#20`; actualiza tracking (checklist/bloques) y
  aÃ±ade una fuente oficial reutilizable para fases posteriores de ejecuciÃ³n de
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
- `problem`: faltaba un gate final operativo y trazable que definiera cuÃ¡ndo se
  puede empezar a codificar tras cerrar la preparaciÃ³n documental del MVP, y
  persistÃ­a una contradicciÃ³n en `AGENTS.md`/`context-governance` (reglas de
  Fase 0 y prohibiciÃ³n de cÃ³digo) una vez alcanzado el readiness.
- `decision`: aceptar `docs/coding-readiness-gate.md` como gate oficial de
  entrada a implementaciÃ³n (`#20`), con resultado documental en 3 estados
  (`apto`, `apto_con_diferidos_aceptados`, `no_apto`), checklist de
  bloqueo/desbloqueo, evidencia mÃ­nima, diferidos aceptados explÃ­citos y
  resultado aplicado al estado actual del repo. Se actualizan `AGENTS.md`,
  `docs/context-governance.md` y `CHK-GATE-CODE` para permitir implementaciÃ³n
  tras gate vÃ¡lido y registrar el estado de fase `implementation_enabled`.
- `rationale`: evita ambigÃ¼edad sobre el inicio de cÃ³digo, conserva rigor del
  gate de calidad, distingue bloqueantes reales de diferidos aceptados (como la
  concurrencia multi-device real diferida en `#19`) y deja una transiciÃ³n
  documental consistente sin reabrir contratos de dominio.
- `impact`: cierra `#20`; habilita inicio de implementaciÃ³n con resultado
  `apto_con_diferidos_aceptados`; actualiza gobierno de contexto y reglas
  operativas; y deja recomendaciÃ³n explÃ­cita del primer slice de cÃ³digo
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
  se decidiÃ³ mantener un visor sticky (Ãºltima entry visible) al navegar por
  years/weeks, lo que desalineaba parcialmente la semÃ¡ntica de selecciÃ³n usada
  en `docs/minimal-read-queries.md` (`#16`) y podÃ­a introducir ambigÃ¼edad con
  la separaciÃ³n foco/activo descrita en `docs/active-session-flow.md` (`#14`).
- `decision`: aceptar en la implementaciÃ³n del shell/local state (`#53`) una
  separaciÃ³n explÃ­cita entre navegaciÃ³n (`selected_year`, `selected_week`),
  entry visible en visor (sticky) y `active_entry` (sesiÃ³n activa global). La
  navegaciÃ³n por year/week puede cambiar sin limpiar la entry visible en visor.
  En el shell mock de `#53` las weeks cerradas se muestran atenuadas y la week
  seleccionada se marca visualmente, sin aÃ±adir marcador explÃ­cito de "current
  week" (que sigue siendo un concepto derivado de `week_cursor` real).
- `rationale`: mejora la continuidad visual del panel central al navegar,
  demuestra mejor la separaciÃ³n foco/activo antes de integrar datos reales
  (`#54`) y mantiene el contrato de acciones sobre la entry visible sin reabrir
  las reglas de backend/operaciones.
- `impact`: ajusta semÃ¡ntica de UI/lecturas en `#16` y aclaraciones de flujo en
  `#14`; guÃ­a la implementaciÃ³n de `#53` y deja preparada la integraciÃ³n
  read-only de `#54` con distinciÃ³n navegaciÃ³n/visor/activo.
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
  estado actual del repo, que todavÃ­a persiste/consume `campaign.week_cursor`
  como campo canÃ³nico en lecturas y writes temporales. La issue `#76` naciÃ³ como
  gap de observabilidad UI de `week_cursor`, pero esa formulaciÃ³n deja de ser
  correcta si `week_cursor` ya no debe existir como concepto vigente.
- `decision`: reencuadrar `#76` como unidad de decisiÃ³n+documentaciÃ³n para
  fijar el canon de **semana actual derivada no persistida**, marcar
  `campaign.week_cursor` como implementaciÃ³n transitoria (no contrato objetivo)
  y abrir una issue tÃ©cnica separada para migrar cÃ³digo/datos. No se realiza la
  migraciÃ³n tÃ©cnica en `#76`.
- `rationale`: simplifica el modelo conceptual (semana actual = primera week
  abierta), evita diseÃ±ar UX/testabilidad alrededor de un campo tÃ©cnico que se
  quiere retirar y reduce retrabajo al separar claramente reencuadre documental
  de migraciÃ³n de implementaciÃ³n.
- `impact`: actualiza docs nÃºcleo (temporal, editabilidad, lecturas, contrato,
  glosario, invariantes) con nota de transiciÃ³n; aÃ±ade trazabilidad histÃ³rica en
  `#70`; crea una issue tÃ©cnica de migraciÃ³n (`#81`); y deja una divergencia
  transitoria aceptada entre docs canÃ³nicas y cÃ³digo actual hasta ejecutar esa
  migraciÃ³n.
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
- `problem`: tras completar la fase fuerte de preparaciÃ³n de contexto, el ritmo de implementaciÃ³n funcional de la app quedÃ³ por debajo del objetivo personal del proyecto (uso propio y avance visible de UI/funcionalidades).
- `decision`: cambiar el modo operativo a **desarrollo-first**: priorizar cierre de UI y funcionalidades pendientes, manteniendo documentaciÃ³n, issues y PR con nivel ligero y orientado a ejecuciÃ³n. Este cambio no elimina trazabilidad; la hace proporcional al impacto real.
- `rationale`: maximiza valor prÃ¡ctico del proyecto, reduce sobrecarga documental y mantiene aprendizaje aplicable sin frenar entrega de producto.
- `impact`: se incorpora una guÃ­a reusable de arranque de proyectos personales con ingenierÃ­a de contexto ligera; se actualiza el estado de fase para priorizar implementaciÃ³n acelerada; y se crea backlog inmediato de issues de desarrollo, incluyendo una de simplificaciÃ³n de cÃ³digo.
- `references`: `AGENTS.md`, `docs/context-governance.md`, `docs/mvp-implementation-checklist.md`, `learning/personal-context-engineering-quickstart.md`

### DEC-0036

- `date`: 2026-02-27
- `status`: accepted
- `problem`: el feature `main_shell` mantenÃ­a mÃºltiples capas operativas (acciones tipadas, orquestaciÃ³n, actualizaciÃ³n incremental, composiciÃ³n de pantalla por submÃ³dulos), lo que dificultaba un flujo directo de mantenimiento para el arranque de implementaciÃ³n.
- `decision`: consolidar `main_shell` en una arquitectura estricta de tres archivos funcionales (`model.py`, `state.py`, `view.py`) mÃ¡s `__init__.py`, eliminando capas intermedias y conectando `build_app_root(page)` directamente con `MainShellState` + `build_main_shell_view`.
- `rationale`: reduce complejidad accidental, deja un punto Ãºnico de estado y otro de render, y mantiene la API pÃºblica del root para permitir iteraciÃ³n rÃ¡pida en UI.
- `impact`: se eliminaron mÃ³dulos previos del feature y se creÃ³ un documento tÃ©cnico comparativo (`docs/ui-main-shell-architecture-mvs.md`) para trazabilidad rÃ¡pida del cambio.
- `references`: `src/frosthaven_campaign_journal/ui/app_root.py`, `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`, `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`, `src/frosthaven_campaign_journal/ui/features/main_shell/view.py`, `docs/ui-main-shell-architecture-mvs.md`

### DEC-0037

- `date`: 2026-02-28
- `status`: accepted
- `problem`: tras la consolidaciÃ³n a MVS (`DEC-0036`), el root de UI quedÃ³ en
  un patrÃ³n hÃ­brido (render con `page.add(...)` + `page.update()`), lo que
  incumplÃ­a la guÃ­a declarativa recomendada para Flet y mantenÃ­a acoplamiento
  imperativo entre estado y render.
- `decision`: migrar el runtime del shell a modo declarativo de Flet, usando
  `page.render(build_app_root, page)` en el entrypoint, `@ft.component` en
  `build_app_root`, callback `notify_ui` para disparar rerender y eliminaciÃ³n
  de `page.update()`/`control.update()` en la capa `src/.../ui`.
- `rationale`: alinea la arquitectura MVS con el modelo declarativo nativo de
  Flet, reduce efectos laterales de actualizaciÃ³n manual y deja un flujo mÃ¡s
  predecible para evoluciÃ³n del feature sin reabrir la estructura de archivos.
- `impact`: actualiza `main.py`, `ui/app_root.py` y `state.py` para un ciclo
  de render declarativo; mantiene contratos de `model.py`; y refuerza la
  documentaciÃ³n de arquitectura del feature con una regla explÃ­cita de no usar
  `update` manual en UI.
- `references`: `src/main.py`,
  `src/frosthaven_campaign_journal/ui/app_root.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`,
  `docs/ui-main-shell-architecture-mvs.md`

### DEC-0038

- `date`: 2026-02-28
- `status`: accepted
- `problem`: aunque `DEC-0037` eliminÃ³ `page.update()` manual, el feature seguÃ­a
  con un patrÃ³n mÃ¡s verboso (`data + actions`) que no aprovechaba el flujo
  directo recomendado por Flet en ejemplos declarativos (`state observable`
  consumido por el componente).
- `decision`: adoptar en `main_shell` un patrÃ³n declarativo ligero: estado
  `@ft.observable` consumido por `@ft.component` con `use_state`, binding directo
  de handlers del estado desde la vista y eliminaciÃ³n de `MainShellViewActions`.
- `rationale`: reduce capas accidentales, deja una estructura mÃ¡s simple para
  iteraciÃ³n rÃ¡pida y alinea el feature con el patrÃ³n prÃ¡ctico tipo `edit_form`
  de Flet manteniendo separaciÃ³n Ãºtil de scripts (`model/state/view`).
- `impact`: `app_root` pasa a usar `use_state(MainShellState.create)`;
  `view.py` deja de depender de `actions`; `state.py` concentra handlers y
  usa `notify()` cuando aplica en mutaciones anidadas; la interacciÃ³n de la
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
- `problem`: el estado de `main_shell` seguÃ­a recibiendo `ft.Page`, lo que
  mezclaba infraestructura de runtime con estado de pantalla y alejaba el
  patrÃ³n objetivo (`model/state/view`) de una separaciÃ³n limpia.
- `decision`: desacoplar `MainShellState` de `ft.Page`; mover viewport a campos
  propios del estado e inyectar cambios de media/viewport desde `app_root`
  mediante mÃ©todo especÃ­fico (`on_viewport_change`).
- `rationale`: mantiene el estado centrado en dominio/UI local y deja `Page`
  como responsabilidad del componente root, con acoplamiento mÃ­nimo y explÃ­cito.
- `impact`: `MainShellState.create(...)` deja de recibir `page`; `build_view_data`
  usa `viewport_width/viewport_height` internos; `app_root` conserva el puente
  con `page.on_media_change` y solo reenvÃ­a datos primitivos al estado.
- `references`: `src/frosthaven_campaign_journal/ui/app_root.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `docs/ui-main-shell-architecture-mvs.md`

### DEC-0040

- `date`: 2026-02-28
- `status`: accepted
- `problem`: en el flujo actual de app fija en landscape, el puente de
  `viewport_width/viewport_height` aÃ±adÃ­a complejidad sin uso funcional real.
- `decision`: simplificar `main_shell` eliminando viewport del estado y
  retirando el bridge de `page.on_media_change`; mantener el estado observable
  centrado en interacciÃ³n de pantalla y datos de vista necesarios.
- `rationale`: reduce ruido en el patrÃ³n declarativo objetivo (`model/state/view`)
  y evita transportar datos de infraestructura que no aportan valor en el estado
  actual de la UI.
- `impact`: `MainShellViewData` deja de incluir viewport; `MainShellState.create`
  vuelve a firma sin parÃ¡metros; `app_root` usa `use_state(MainShellState.create)`
  sin hooks adicionales de media.
- `references`: `src/frosthaven_campaign_journal/ui/features/main_shell/model.py`,
  `src/frosthaven_campaign_journal/ui/features/main_shell/state.py`,
  `src/frosthaven_campaign_journal/ui/app_root.py`,
  `docs/ui-main-shell-architecture-mvs.md`

### DEC-0041

- `date`: 2026-03-01
- `status`: accepted
- `problem`: el refactor `#94` simplificÃ³ la estructura `main_shell` pero dejÃ³
  una regresiÃ³n funcional severa: se perdiÃ³ wiring real de Firestore
  (lecturas/escrituras) y gran parte del panel central operativo.
- `decision`: recuperar la paridad funcional pre-`#94` sobre arquitectura
  declarativa MVS, manteniendo `page.render(...)`, `@ft.component` en root,
  `@ft.observable` en estado y sin reintroducir `page.update()` ni
  `control.update()` en `src/.../ui`.
- `rationale`: restaura valor funcional del MVP sin volver al patrÃ³n hÃ­brido
  imperativo ni reabrir capas eliminadas (`dispatcher/reducer/effects`).
- `impact`: `model.py` amplÃ­a contrato de vista con estado declarativo de
  confirmaciones/formularios; `state.py` reintegra Q1..Q8 y operaciones de
  campaÃ±a/week/session/entry/resources con handlers directos; `view.py`
  recupera panel central funcional (modo vacÃ­o/week/entry, sesiones, recursos,
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
- `problem`: tras recuperar la funcionalidad real, seguÃ­an rastros de etapa
  bootstrap (`Mock*`, mÃ³dulos `placeholders` y archivos legacy de arranque)
  que aÃ±adÃ­an ruido semÃ¡ntico y deuda de mantenimiento.
- `decision`: retirar del Ã¡rbol activo los mocks/placeholders residuales y
  eliminar los documentos legacy de arranque, manteniendo solo trazabilidad
  histÃ³rica en documentaciÃ³n oficial.
- `rationale`: reduce ambigÃ¼edad entre runtime real y artefactos de
  preparaciÃ³n, simplifica imports/modelos y evita depender de fuentes no
  canÃ³nicas ya migradas.
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
  objetivo de foco semanal y ediciÃ³n rÃ¡pida por entry.
- `decision`: mover la selecciÃ³n/gestiÃ³n de entries al visor central con
  listado vertical por semana y acciones por icono en cada tile
  (`subir/bajar/eliminar/editar notas`), eliminar la barra externa de entries y
  retirar el sticky del visor al cambiar de semana o aÃ±o. AdemÃ¡s, extender el
  modelo de `Entry` con `notes` y `scenario_outcome` (`victory|defeat|null`),
  dejando `scenario_outcome` en modo solo lectura en UI en esta iteraciÃ³n.
- `rationale`: simplifica el flujo mental (semana -> entries -> entry),
  reduce navegaciÃ³n lateral redundante y habilita ediciÃ³n rÃ¡pida de notas sin
  abrir la vista completa de entry.
- `impact`: se actualizan lecturas/escrituras para persistir `notes` y
  `scenario_outcome`; se aÃ±ade `update_entry_notes`; se rediseÃ±a `center_focus`
  con tiles semanales y acciones icon-only; y se alinea documentaciÃ³n de dominio
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
- `problem`: la UI de recursos del visor y la barra inferior seguÃ­a orientada a
  un subconjunto reducido y no tenÃ­a catÃ¡logo Ãºnico reusable para 12 claves,
  iconografÃ­a oficial ni layout agrupado estable en mÃ³vil.
- `decision`: unificar catÃ¡logo de recursos del runtime en una fuente Ãºnica
  compartida de 12 claves (`resource_catalog`), introducir control reusable de
  fila de delta para ediciÃ³n por entry, rediseÃ±ar barra inferior con 4 columnas
  fijas y scroll horizontal, y fijar oficialmente mapeo EN->ES + assets en
  `docs/resource-ui-catalog.md`.
- `rationale`: reduce duplicidad entre dominio/UI/writes, facilita evoluciÃ³n de
  controles reusables en modo declarativo Flet y deja trazabilidad explÃ­cita de
  nomenclatura/iconos alineada con el glosario del MVP.
- `impact`: `ENTRY_RESOURCE_KEYS` pasa a depender de catÃ¡logo Ãºnico de 12
  claves; validaciÃ³n de writes de recursos usa la misma fuente; el editor de
  recursos renderiza 12 filas agrupadas con total proyectado; la barra inferior
  muestra siempre los 12 totales guardados con icono y nombre completo; se
  oficializa carpeta `assets/resource-icons/` y se aÃ±aden iconos de
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
- `problem`: la UI del shell principal en tablet no mantenÃ­a densidad Ãºtil
  (barra superior y visor central), el bloque de estado inferior ocupaba espacio
  crÃ­tico y el soporte de notas de semana dejÃ³ de ser necesario para el flujo
  objetivo.
- `decision`: rediseÃ±ar la shell para tablet con acciones contextuales en botÃ³n
  flotante (`+`), eliminar la cabecera de semana y metadatos redundantes por
  entry, mantener solo recursos totales en barra inferior (orden visual:
  `Otros -> Materiales -> Plantas`) y retirar por completo `Week.update_notes`
  del runtime y de los contratos activos del MVP.
- `rationale`: prioriza legibilidad y acciones frecuentes en viewport reducido,
  simplifica el modelo operativo semanal y elimina una vÃ­a de ediciÃ³n que ya no
  aporta valor al flujo de juego.
- `impact`: se compacta la barra temporal superior, se sustituye la fila de
  refresco por menÃº flotante contextual, se simplifica el visor semanal,
  desaparece el estado textual de la barra inferior, se actualiza el modelo
  (`WeekRead`/`WeekSummary`) sin notas de semana y se alinea la documentaciÃ³n
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
- `problem`: la UI principal seguÃ­a sin usar acento de fondo en elementos clave
  de interacciÃ³n, los iconos de recursos no cargaban de forma fiable con
  `flet run src/main.py -d -r` por ubicaciÃ³n de assets y la tarjeta de entry
  mantenÃ­a bloques textuales redundantes para el flujo tablet.
- `decision`: aplicar acento rojo `PUNCH_RED` en fondos de botones de aÃ±o,
  semana seleccionada, FAB y etiquetas de todas las `LabeledGroupBox`;
  reubicar iconos de `assets/resource-icons/` a
  `src/assets/resource-icons/`; simplificar la tarjeta de entry retirando el
  bloque de detalle textual y dejando `Recursos`/`Sesiones` como etiquetas de
  caja.
- `rationale`: mejora jerarquÃ­a visual y legibilidad de estados seleccionados,
  alinea la resoluciÃ³n de assets con el modo de arranque real del repo y reduce
  ruido visual en el visor semanal sin tocar contratos de dominio.
- `impact`: se introducen semÃ¡nticos de acento en `colors.py`, la barra
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
  etiquetas de grupo y botones de aÃ±o a estilo claro (fondo blanco con borde y
  texto rojos); aumentar legibilidad de semanas cerradas; y aÃ±adir borde visible
  a semanas abiertas y seleccionada.
- `rationale`: mejora equilibrio visual y jerarquÃ­a de foco (acciÃ³n principal y
  selecciÃ³n activa) sin perder identidad de acento ni alterar layout/flujo.
- `impact`: `colors.py` incorpora semÃ¡nticos explÃ­citos para borde/texto de
  navegaciÃ³n anual, borde de semana abierta y contraste de cerradas; en
  `temporal_bar.py` los botones de aÃ±o pasan a radio `16` con borde y texto
  rojos, y las tiles abiertas/seleccionada muestran borde visible.
- `references`: `src/frosthaven_campaign_journal/ui/common/theme/colors.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/temporal_bar.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/shell_view.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/status_bar.py`,
  `src/frosthaven_campaign_journal/ui/main_shell/view/center_focus.py`

### DEC-0048

- `date`: 2026-03-05
- `status`: accepted
- `problem`: en la barra temporal, los bordes de las tiles de semana aÃ±adÃ­an
  ruido visual y el color de semanas abiertas no diferenciaba bien el estado
  respecto al resto.
- `decision`: retirar borde en todos los botones de semana y ajustar el color
  de semanas abiertas a un tono azul claro mÃ¡s visible.
- `rationale`: prioriza lectura rÃ¡pida del strip semanal y reduce saturaciÃ³n de
  contornos en un Ã¡rea con alta densidad de elementos.
- `impact`: `temporal_bar.py` deja de renderizar bordes en tiles y
  `colors.py` actualiza `WEEK_TILE_BG` para mejorar diferenciaciÃ³n de semanas
  abiertas.
- `references`: `src/frosthaven_campaign_journal/ui/main_shell/view/temporal_bar.py`,
  `src/frosthaven_campaign_journal/ui/common/theme/colors.py`

### DEC-0049

- `date`: 2026-03-05
- `status`: accepted
- `problem`: la tarjeta de `Entry` mantenÃ­a estructura vertical poco eficiente
  para recursos/sesiones, con caja contenedora adicional de recursos y botones
  de guardar/deshacer fuera de la barra principal de acciones.
- `decision`: mover `guardar/deshacer recursos` a la barra de iconos del header
  de la entrada, eliminar la caja contenedora `Recursos`, y reordenar secciones
  en tres filas: `Otros+Materiales`, `Plantas`, `Sesiones`.
- `rationale`: reduce fricciÃ³n operativa en ediciÃ³n rÃ¡pida por entrada, mejora
  jerarquÃ­a de acciones y aprovecha mejor el ancho disponible en tablet/web.
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
  generica en `docs/repo-workflow.md`, pero faltaba un flujo operativo
  reproducible con comandos, evidencias y convencion de assets para cerrar
  implementacion de releases manuales.
- `decision`: formalizar un flujo manual oficial de release Android en
  `docs/android-release-flow.md`, introducir contrato de empaquetado Flet en
  `pyproject.toml` y fijar convencion de assets de build en `src/assets/`
  (`icon.png`, `icon_android.png`, `splash.png`, `splash_android.png`).
- `rationale`: permite cerrar `#105` con trazabilidad completa sin depender de
  CI ni de secretos remotos, manteniendo un camino estable para distribucion
  directa por `.apk`.
- `impact`: se habilita build local reproducible con `flet build apk`,
  verificacion por hash del artefacto y adjunto manual a GitHub Releases; se
  actualizan `docs/repo-workflow.md`, `docs/system-map.md` y `CHANGELOG.md`.
- `references`: `docs/android-release-flow.md`, `pyproject.toml`,
  `docs/repo-workflow.md`, `docs/system-map.md`, `CHANGELOG.md`,
  `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/105`
