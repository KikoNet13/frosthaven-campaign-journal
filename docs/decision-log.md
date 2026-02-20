# Registro de Decisiones

## Metadatos

- `doc_id`: DOC-DECISION-LOG
- `purpose`: Registrar decisiones con trazabilidad y precedencia.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-06

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
