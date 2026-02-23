# Bloques de Implementación MVP (Desglose Operativo)

## Metadatos

- `doc_id`: DOC-MVP-IMPLEMENTATION-BLOCKS
- `purpose`: Desglosar el checklist técnico base de implementación MVP en bloques y subbloques ejecutables con trazabilidad.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-23
- `next_review`: 2026-03-09

## Objetivo

Convertir el checklist técnico base de `docs/mvp-implementation-checklist.md`
(Issue #10) en un desglose operativo por issues y subbloques ejecutables para
la preparación de implementación del MVP, sin codificar todavía.

## Alcance y no alcance

Incluye:

- desglose detallado de las Issues `#12`–`#20` por subbloques ejecutables;
- responsables por rol (`Codex`, `Kiko`, `Codex+Kiko`);
- entregables, dependencias y criterios de finalización por subbloque;
- riesgos y bloqueos por issue;
- reglas de secuencia y ejecución para operar el plan.

No incluye:

- implementación de código de app;
- cierre de las Issues `#12`–`#20` en este documento;
- gate final de “listo para codificar” (solo su desglose planificado);
- redefinir por sí mismo reglas globales de repo (eso se formaliza en la issue
  de proceso correspondiente).

## Entradas y prerrequisitos

### Prerrequisitos ya resueltos

- Issue #7 -> `docs/sync-strategy.md`
- Issue #8 -> `docs/conflict-policy.md`
- Issue #9 -> `docs/campaign-temporal-controls.md`
- Issue #10 -> `docs/mvp-implementation-checklist.md`

### Dependencia de trabajo para este documento

- Issue #11 (esta issue) debe usar como base el orden macro y la matriz de
  dependencias de `docs/mvp-implementation-checklist.md`.

## Relación con `#10`, `#20` y la regla de `siguiente paso`

- **#10** define el checklist técnico base (macro-bloques, secuencia y
  verificación mínima).
- **#11** (este documento) añade el desglose fino en bloques/subbloques
  ejecutables.
- **#20** sigue reservado al gate final de entrada a codificación.

### Nota operativa sobre `siguiente paso` y orden técnico

- Si existe un **orden técnico recomendado** documentado, `siguiente paso` lo
  prioriza.
- La fuente de orden técnico debe ser el **documento oficial más específico**
  disponible (detalle > macro).
- Si un item técnico está abierto pero no es cerrable, se salta al siguiente
  item cerrable.
- Si no hay items cerrables, se toma el primer item `draftable`.
- Si no existe orden técnico aplicable, `siguiente paso` vuelve al criterio de
  issue abierta con número más bajo.

## Convenciones de bloques y subbloques

### Estados iniciales de bloque/subbloque

- `ready`: puede iniciarse y cerrarse con dependencias actuales.
- `draftable`: puede iniciarse en borrador, pero su cierre depende de otros
  bloques/issues.
- `blocked`: no debe cerrarse hasta resolver dependencias faltantes.
- `final_gate`: bloque reservado para cierre final de preparación.

### Roles de responsable

- `Codex`: propuesta, redacción, estructura y trazabilidad documental.
- `Kiko`: validación y aprobación (cuando aplique).
- `Codex+Kiko`: trabajo interactivo o revisión conjunta.

### Formato de subbloque

- `I<issue>-S<n>`
- Ejemplos: `I12-S1`, `I18-S3`

## Resumen ejecutivo de bloques

| Issue | Tipo | Estado inicial | Orden técnico recomendado | ¿Puede iniciar borrador? | Cierre condicionado por | Entregable principal |
| --- | --- | --- | --- | --- | --- | --- |
| #12 | `decision` | `draftable` | 2.º dentro del bloque B | Sí | Alineación con #13 (cierre recomendado con #13 cerrada) | Contrato de operaciones Firestore por agregado |
| #13 | `task` | `ready` | 2.º del bloque B (1.º dentro de B) | Sí | Coherencia con #9 y dominio | Estrategia técnica de inicialización/extensión temporal |
| #14 | `task` | `draftable` | 1.º del bloque C | Sí | Alineación con #12 para cierre | Flujo de sesión activa y `auto-stop` |
| #15 | `task` | `draftable` | 2.º del bloque C | Sí | Alineación con #12 para cierre | Reglas de validación y recálculo de recursos |
| #16 | `task` | `draftable` | 1.º del bloque D | Sí | Compatibilidad con #18 para cierre | Inventario mínimo de consultas y orden/paginación |
| #17 | `task` | `draftable` | 2.º del bloque D | Sí | Mayor valor tras #12/#14/#15/#18 | Matriz de edge cases de concurrencia/sincronización |
| #18 | `decision` | `draftable` | 3.º dentro del bloque B | Sí | Compatibilidad con #12 y lecturas | Política de timestamps y desempate estable |
| #19 | `task` | `draftable` | 3.º del bloque D | Sí | Insumos suficientes de contratos/flows | Plan de pruebas de invariantes |
| #20 | `task` | `final_gate` | Último (bloque E) | No (cierre final) | Base de #10 + derivadas relevantes | Gate de listo para codificar |

## Detalle por issue (`#12`–`#20`)

### Issue #12 — Definir contrato de operaciones Firestore por agregado de dominio

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: `#13` (alineación temporal estable), más coherencia
  con `#7`, `#8`, `#9` (ya resueltas)
- `impacta_a`: `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I12-S1` | Inventariar operaciones por agregado (`campaign`, `week`, `entry`, `session`, `resource_change`) y casos de uso | `Codex` | `#7`, `#8`, `#9` | Tabla de operaciones por agregado | Inventario completo y sin solapes obvios | `draftable` |
| `I12-S2` | Definir contrato por agregado (precondiciones, postcondiciones, validaciones, rechazo por conflicto, atomicidad esperada) | `Codex` | `I12-S1` | Tabla de contrato por agregado | Cada agregado tiene contrato explícito y coherente con `#8` | `draftable` |
| `I12-S3` | Alinear operaciones temporales con la especificación de `#13` (provisión/extensión/cambio de `week_cursor`) | `Codex+Kiko` | `I12-S2`, `#13` | Nota/tabla de alineación `#12` ↔ `#13` | No quedan contradicciones con flujo temporal | `draftable` |
| `I12-S4` | Cerrar la decisión (revisión interactiva, trazabilidad y referencias) | `Codex+Kiko` | `I12-S3` | Documento final + registro de decisión | Aprobación explícita de Kiko y PR mergeada | `draftable` |

#### Riesgos y bloqueos

- Riesgo de cerrar contrato desalineado con `#13` si se adelanta demasiado.
- Riesgo de duplicar lógica ya fijada por `#8` (conflictos) y `#9` (temporal).

#### Criterio de cierre de la issue

- Existe contrato de operaciones por agregado con pre/postcondiciones,
  validaciones y reglas de rechazo, alineado con `#13` y consistente con `#8`.

#### Notas de secuencia / paralelización

- Puede iniciarse en borrador antes de cerrar `#13`.
- El cierre se recomienda después de `#13` para reducir retrabajo.

### Issue #13 — Especificar estrategia de inicialización de años, temporadas y semanas

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `ready`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#9` y `docs/domain-glossary.md`
- `impacta_a`: `#12`, `#16`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I13-S1` | Definir flujo técnico de provisión inicial de 4 años en `campaign/01` | `Codex` | `#9` | Especificación del flujo inicial | Queda descrito de forma no ambigua y sin contradicción con `#9` | `ready` |
| `I13-S2` | Definir regla de extensión manual `+1` año con confirmación y criterios de creación | `Codex` | `I13-S1`, `#9` | Especificación de extensión `+1` | Se documenta comportamiento completo de extensión manual | `ready` |
| `I13-S3` | Especificar creación de `year/season/week` y validaciones para evitar duplicados/estados inválidos | `Codex` | `I13-S1`, `I13-S2` | Reglas de inicialización y validación | Existen validaciones mínimas y estructura temporal consistente | `ready` |
| `I13-S4` | Alinear referencias con `#9` y preparar insumo directo para `#12` | `Codex+Kiko` | `I13-S3` | Referencias cruzadas y nota para `#12` | `#12` puede usar el resultado sin ambigüedad temporal | `ready` |

#### Riesgos y bloqueos

- Riesgo de sobreespecificar operaciones Firestore (eso es `#12`).
- Riesgo de mezclar UX de `#9` con detalle técnico de provisión.

#### Criterio de cierre de la issue

- Estrategia de inicialización/extensión temporal detallada, consistente con `#9`
  y sin contradicciones con `docs/domain-glossary.md`.

#### Notas de secuencia / paralelización

- Es el primer candidato técnico recomendado tras `#11`.
- Su cierre reduce incertidumbre para `#12`.

### Issue #14 — Diseñar flujo de sesión activa y reglas de auto-stop

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8` y alineación con `#12`
- `impacta_a`: `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I14-S1` | Definir diagrama/tabla de estados y transiciones (`start`, `stop`, `auto-stop`) | `Codex` | `#8`, `docs/domain-glossary.md` | Diagrama/tabla de estados | Todas las transiciones principales están cubiertas | `draftable` |
| `I14-S2` | Especificar reglas operativas por evento y errores esperados | `Codex` | `I14-S1` | Reglas por evento | Se cubren `start`, `stop`, `auto-stop` y errores esperables | `draftable` |
| `I14-S3` | Definir interacción con cierre de semana y efectos sobre sesión activa | `Codex` | `I14-S2`, `#8` | Reglas de cierre de semana + sesión | No rompe invariante `0..1` sesión activa global | `draftable` |
| `I14-S4` | Alinear comportamiento con contrato de operaciones (`#12`) para cierre | `Codex+Kiko` | `I14-S3`, `#12` | Alineación final `#14` ↔ `#12` | No quedan ambigüedades operativas/atómicas para implementar | `draftable` |

#### Riesgos y bloqueos

- Riesgo de cerrar sin contrato técnico por agregado (`#12`) y luego retrabajar.
- Riesgo de inconsistencias con `auto-stop` al cerrar semana.

#### Criterio de cierre de la issue

- Flujo completo de sesión activa y `auto-stop` documentado, consistente con
  invariantes de dominio y concurrencia.

#### Notas de secuencia / paralelización

- Puede iniciarse en borrador con `#8` ya resuelta.
- Conviene cerrar tras avances sustanciales en `#12`.

### Issue #15 — Diseñar reglas de validación y recálculo de recursos

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8` y alineación con `#12`
- `impacta_a`: `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I15-S1` | Inventariar operaciones sobre `ResourceChange` (crear, editar, borrar, corregir) | `Codex` | `#8`, `docs/domain-glossary.md` | Inventario de operaciones de recursos | Operaciones y efectos quedan enumerados | `draftable` |
| `I15-S2` | Definir reglas de validación de `delta` y restricción de totales no negativos | `Codex` | `I15-S1` | Reglas de validación | Casos válidos/inválidos y rechazos quedan cerrados | `draftable` |
| `I15-S3` | Definir estrategia de recálculo y consistencia de totales globales | `Codex` | `I15-S2` | Estrategia de recálculo | Se documenta consistencia y comportamiento esperado tras correcciones | `draftable` |
| `I15-S4` | Alinear matriz de rechazos con `#8` y contrato de operaciones (`#12`) | `Codex+Kiko` | `I15-S3`, `#12` | Alineación final de rechazos y operaciones | No quedan contradicciones con concurrencia ni contrato | `draftable` |

#### Riesgos y bloqueos

- Riesgo de definir validaciones incompatibles con atomicidad esperada de `#12`.
- Riesgo de subestimar casos de corrección/borrado y recálculo.

#### Criterio de cierre de la issue

- Reglas de validación y recálculo trazables, con rechazos esperados y
  consistencia con concurrencia/operaciones.

#### Notas de secuencia / paralelización

- Puede avanzar en borrador antes de `#12`.
- Conviene cerrar después de aclarar contrato por agregado en `#12`.

### Issue #16 — Definir consultas mínimas para timeline y panel de foco

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: alineación con `#9`; orden estable recomendado con
  `#18`
- `impacta_a`: `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I16-S1` | Inventariar vistas/zonas de UI y sus necesidades mínimas de lectura | `Codex` | `#9`, `tdd.md` (referencia de producto) | Inventario de vistas y lecturas | Cada zona de UI tiene necesidades mínimas identificadas | `draftable` |
| `I16-S2` | Definir consultas mínimas y campos requeridos por consulta | `Codex` | `I16-S1` | Lista de consultas + campos | Inventario de consultas mínimo y suficiente | `draftable` |
| `I16-S3` | Definir orden, paginación y estabilidad visual (compatibilidad con `#18`) | `Codex+Kiko` | `I16-S2`, `#18` | Reglas de orden/paginación | Orden estable y criterios de paginación documentados | `draftable` |
| `I16-S4` | Documentar riesgos de coste/latencia y límites aceptables del MVP | `Codex` | `I16-S2`, `I16-S3` | Sección de riesgos/rendimiento | Riesgos y límites quedan explícitos y trazables | `draftable` |

#### Riesgos y bloqueos

- Riesgo de cerrar consultas antes de fijar orden estable (`#18`).
- Riesgo de sobrecarga de lecturas por no recortar campos mínimos.

#### Criterio de cierre de la issue

- Conjunto mínimo de lecturas y reglas de orden/paginación documentado, con
  límites de rendimiento y coherencia con `#9`.

#### Notas de secuencia / paralelización

- Puede iniciarse en borrador antes de `#18`.
- El cierre es más sólido con `#18` resuelta.

### Issue #17 — Preparar matriz de edge cases de concurrencia y sincronización

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: mayor valor con `#12`, `#14`, `#15`, `#18`
- `impacta_a`: `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I17-S1` | Definir taxonomía de casos (sesiones, entries, recursos, temporales, lecturas) | `Codex` | `#7`, `#8` | Taxonomía de edge cases | Taxonomía cubre las familias críticas del MVP | `draftable` |
| `I17-S2` | Construir matriz caso → resultado esperado → severidad → prioridad | `Codex` | `I17-S1` | Matriz de edge cases | Cada caso tiene expectativa y prioridad verificable | `draftable` |
| `I17-S3` | Seleccionar casos críticos de verificación del MVP | `Codex+Kiko` | `I17-S2` | Lista priorizada de casos críticos | Quedan definidos casos críticos mínimos a validar | `draftable` |
| `I17-S4` | Alinear matriz con contratos y flujos (`#12`, `#14`, `#15`, `#18`) antes de cierre | `Codex+Kiko` | `I17-S2`, `#12`, `#14`, `#15`, `#18` | Revisión final de consistencia | No hay expectativas en conflicto con docs previas | `draftable` |

#### Riesgos y bloqueos

- Riesgo de matriz incompleta si se cierra antes de contratos/flows clave.
- Riesgo de duplicar casos de prueba que pertenecen a `#19` (esta issue define
  matriz y expectativas, no plan de pruebas completo).

#### Criterio de cierre de la issue

- Matriz de edge cases con expectativas, severidad y prioridad, alineada con
  sincronización/concurrencia y con insumos técnicos suficientes.

#### Notas de secuencia / paralelización

- Puede arrancar con taxonomía y borrador de matriz.
- Su cierre gana calidad después de `#12`, `#14`, `#15` y `#18`.

### Issue #18 — Definir política de timestamps y orden estable entre dispositivos

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#7`, `#8`; compatibilidad con
  `#12` y lecturas (`#16`)
- `impacta_a`: `#16`, `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I18-S1` | Inventariar eventos ordenables y puntos donde se necesita orden estable | `Codex` | `#7`, `#8`, `tdd.md` | Inventario de eventos ordenables | Se cubren timeline, logs y lecturas críticas | `draftable` |
| `I18-S2` | Preparar opciones de política (timestamps y desempate) con tradeoffs | `Codex` | `I18-S1` | Comparativa de opciones | Opciones comparables y criterios de decisión explícitos | `draftable` |
| `I18-S3` | Cerrar decisión final con Kiko (modo interactivo) y contrato de orden estable | `Codex+Kiko` | `I18-S2` | Decisión aceptada + política final | Aprobación explícita de Kiko y contrato documentado | `draftable` |
| `I18-S4` | Alinear trazabilidad y compatibilidad con `#16`, `#17`, `#19` | `Codex+Kiko` | `I18-S3` | Referencias cruzadas actualizadas | Las issues downstream pueden usar la política sin ambigüedad | `draftable` |

#### Riesgos y bloqueos

- Riesgo de definir desempate incompatible con consultas mínimas (`#16`) o
  contrato de operaciones (`#12`).
- Riesgo de cerrar sin inventario completo de eventos ordenables.

#### Criterio de cierre de la issue

- Política de timestamps y orden estable aceptada, trazable y compatible con
  sincronización, concurrencia y lecturas previstas.

#### Notas de secuencia / paralelización

- Puede arrancar en borrador antes de `#12`.
- Requiere revisión interactiva con Kiko para cierre (`type:decision`).

### Issue #19 — Preparar plan de pruebas para invariantes de dominio

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: insumos suficientes de contratos/flows/orden
- `impacta_a`: `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I19-S1` | Seleccionar invariantes críticas del dominio (a partir de `docs/domain-glossary.md` y decisiones cerradas) | `Codex` | `docs/domain-glossary.md`, `#7`, `#8`, `#9` | Lista priorizada de invariantes | Invariantes críticas quedan seleccionadas y justificadas | `draftable` |
| `I19-S2` | Diseñar casos de prueba por invariante (precondición, acción, resultado esperado) | `Codex` | `I19-S1` | Matriz de casos por invariante | Cada invariante tiene casos verificables | `draftable` |
| `I19-S3` | Definir estrategia de evidencia y repetibilidad | `Codex` | `I19-S2` | Estrategia de evidencia | Queda claro cómo registrar y repetir validaciones | `draftable` |
| `I19-S4` | Priorizar ejecución de pruebas para soportar `#20` | `Codex+Kiko` | `I19-S2`, `I19-S3`, `#12`, `#14`, `#15`, `#18` | Priorización para readiness | El plan sirve como insumo directo para el gate de `#20` | `draftable` |

#### Riesgos y bloqueos

- Riesgo de plan incompleto si faltan contratos/flows/orden estable.
- Riesgo de mezclar definición de pruebas con ejecución real (esta issue solo
  define el plan).

#### Criterio de cierre de la issue

- Plan de pruebas de invariantes priorizado, repetible y trazable, apto para
  sustentar el gate de `#20`.

#### Notas de secuencia / paralelización

- Puede comenzar con selección de invariantes y estructura de casos.
- El cierre se fortalece con `#12`, `#14`, `#15` y `#18` resueltas.

### Issue #20 — Definir criterios de listo para codificar en Fase 1

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `final_gate`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: checklist base (`#10`) y derivados relevantes
  (`#11`–`#19`) según criterios definidos
- `impacta_a`: paso a implementación

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I20-S1` | Inventariar precondiciones y dependencias críticas de readiness | `Codex` | `#10`, `#11` y estado de `#12`–`#19` | Inventario de precondiciones | Dependencias críticas quedan listadas y clasificadas | `final_gate` |
| `I20-S2` | Definir checklist de bloqueo/desbloqueo para entrada a codificación | `Codex` | `I20-S1` | Checklist de readiness | El gate de entrada es explícito y verificable | `final_gate` |
| `I20-S3` | Definir evidencia mínima exigida (documental y trazabilidad) | `Codex` | `I20-S2` | Reglas de evidencia | Queda claro qué evidencia se exige para habilitar código | `final_gate` |
| `I20-S4` | Definir flujo de validación final (Codex prepara, Kiko valida) y criterio de cierre | `Codex+Kiko` | `I20-S3` | Protocolo de validación final | El cierre de `#20` queda operable y sin ambigüedades | `final_gate` |

#### Riesgos y bloqueos

- Riesgo de cerrar `#20` demasiado pronto y convertirlo en gate vacío.
- Riesgo de duplicar detalle de `#11` o reabrir decisiones de `#12`/`#18`.

#### Criterio de cierre de la issue

- Gate operativo de entrada a codificación explícito, verificable y trazable,
  apoyado en evidencias de `#10` y derivadas.

#### Notas de secuencia / paralelización

- No debe cerrarse antes de contar con insumos suficientes del resto de bloques.
- Es el último bloque técnico de preparación antes de iniciar código.

## Riesgos transversales y reglas de ejecución

### Riesgos transversales

- **Solape entre checklist base y desglose**: `#10` define macro; `#11` detalla.
- **Cierres fuera de secuencia técnica**: riesgo de retrabajo si se ignoran
  dependencias de cierre.
- **Cierre prematuro de issues `draftable`**: se admite borrador, no cierre sin
  dependencias satisfechas.
- **Confusión entre orden técnico y número de issue**: el orden técnico manda
  para `siguiente paso` cuando exista y sea aplicable.

### Reglas de ejecución (operativas)

1. Priorizar PRs abiertas antes de iniciar trabajo nuevo.
1. Usar el **orden técnico recomendado** del documento más específico disponible
   para elegir el siguiente trabajo cuando no haya PRs abiertas.
1. Si el siguiente item técnico no es cerrable, saltar al siguiente cerrable.
1. Si no hay cerrables, avanzar en el primer `draftable`.
1. Si no existe orden técnico aplicable, usar la issue abierta con número más
   bajo.
1. Mantener trazabilidad de estado (`ready`, `draftable`, `blocked`,
   `final_gate`) al revisar el plan.

## Seguimiento inicial de bloques

### Estado de bloques (tras cerrar #11)

- [x] `#11` Desglose en bloques ejecutables (este documento)
- [ ] `#13` Inicialización temporal detallada (`ready`)
- [ ] `#12` Contrato Firestore por agregado (`draftable`)
- [ ] `#18` Timestamps y orden estable (`draftable`)
- [ ] `#14` Flujo de sesión activa y `auto-stop` (`draftable`)
- [ ] `#15` Validación y recálculo de recursos (`draftable`)
- [ ] `#16` Consultas mínimas para timeline/foco (`draftable`)
- [ ] `#17` Matriz de edge cases (`draftable`)
- [ ] `#19` Plan de pruebas de invariantes (`draftable`)
- [ ] `#20` Gate de listo para codificar (`final_gate`)

### Próxima secuencia técnica esperada (según orden actual)

1. `#13` (cerrable)
1. `#12` (borrador/cierre condicionado por alineación con `#13`)
1. `#18`
1. `#14`
1. `#15`
1. `#16`
1. `#17`
1. `#19`
1. `#20`

## Referencias

- `AGENTS.md`
- `docs/system-map.md`
- `docs/repo-workflow.md`
- `docs/mvp-implementation-checklist.md`
- `docs/sync-strategy.md`
- `docs/conflict-policy.md`
- `docs/campaign-temporal-controls.md`
- `docs/domain-glossary.md`
- `docs/context-checklists.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/10`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/11`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`
