# Registro de Decisiones

## Metadatos

- `doc_id`: DOC-DECISION-LOG
- `purpose`: Registrar decisiones con trazabilidad y precedencia.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-23
- `next_review`: 2026-03-09

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
