# Bloques de Implementación MVP (Desglose Operativo)

## Metadatos

- `doc_id`: DOC-MVP-IMPLEMENTATION-BLOCKS
- `purpose`: Desglosar el checklist técnico base de implementación MVP en bloques y subbloques ejecutables con trazabilidad, incluyendo decisiones marco posteriores que alteren el orden técnico.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-27
- `next_review`: 2026-03-13

## Objetivo

Convertir el checklist técnico base de `docs/mvp-implementation-checklist.md`
(Issue #10) en un desglose operativo por issues y subbloques ejecutables para
la preparación de implementación del MVP, sin codificar todavía.

## Alcance y no alcance

Incluye:

- desglose detallado de las Issues `#12`–`#20` y decisiones marco intermedias
  que afecten su secuencia (actualmente `#37` y `#40`) por subbloques
  ejecutables;
- responsables por rol (`Codex`, `Kiko`, `Codex+Kiko`);
- entregables, dependencias y criterios de finalización por subbloque;
- riesgos y bloqueos por issue;
- reglas de secuencia y ejecución para operar el plan.

No incluye:

- implementación de código de app;
- cierre de las Issues `#12`–`#20` (ni de decisiones marco intermedias como
  `#37`) en este documento;
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
| #13 | `task` | `ready` | 1.º dentro del bloque B | Sí | Coherencia con #9 y dominio | Estrategia técnica de inicialización/extensión temporal |
| #37 | `decision` | `ready` | 2.º dentro del bloque B | Sí | Coherencia con #8/#9/#13 y dominio | Política de editabilidad manual y correcciones de dominio |
| #12 | `decision` | `draftable` | 3.º dentro del bloque B | Sí | Alineación con #13 y #37 (cierre recomendado con ambas cerradas) | Contrato de operaciones Firestore por agregado |
| #40 | `decision` | `draftable` | 4.º dentro del bloque B | Sí | Coherencia con #12/#37 y glosario; supersesión parcial de recursos | Modelo de recursos por `Entry` (`resource_deltas`) |
| #14 | `task` | `draftable` | 1.º del bloque C | Sí | Alineación con #12 para cierre | Flujo de sesión activa y `auto-stop` |
| #15 | `task` | `draftable` | 2.º del bloque C | Sí | Alineación con #12 para cierre | Reglas de validación y recálculo de recursos |
| #16 | `task` | `draftable` | 1.º del bloque D | Sí | Compatibilidad con #18 para cierre | Inventario mínimo de consultas y orden/paginación |
| #17 | `task` | `draftable` | 2.º del bloque D | Sí | Mayor valor tras #12/#14/#15/#18 | Matriz de edge cases de concurrencia/sincronización |
| #18 | `decision` | `draftable` | 5.º dentro del bloque B | Sí | Compatibilidad con #12, #40 y lecturas | Política de timestamps y desempate estable |
| #19 | `task` | `draftable` | 3.º del bloque D | Sí | Insumos suficientes de contratos/flows | Plan de pruebas de invariantes |
| #20 | `task` | `final_gate` | Último (bloque E) | No (cierre final) | Base de #10 + derivadas relevantes | Gate de listo para codificar |

## Detalle por issue (`#12`–`#20`) y decisiones marco intermedias (`#37`, `#40`)

### Issue #12 — Definir contrato de operaciones Firestore por agregado de dominio

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `draftable` (cerrada en seguimiento; este bloque conserva el estado inicial del plan)
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: `#13` (alineación temporal estable), `#37`
  (editabilidad e invariantes actualizadas), más coherencia con `#7`, `#8`,
  `#9` (ya resueltas)
- `impacta_a`: `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I12-S1` | Inventariar operaciones por agregado (`campaign`, `week`, `entry` incl. `resource_deltas`, `session`) y casos de uso | `Codex` | `#7`, `#8`, `#9`, `#37` | Tabla de operaciones por agregado | Inventario completo y sin solapes obvios con mutabilidad vigente | `draftable` |
| `I12-S2` | Definir contrato por agregado (precondiciones, postcondiciones, validaciones, rechazo por conflicto/transición inválida, atomicidad esperada) | `Codex` | `I12-S1` | Tabla de contrato por agregado | Cada agregado tiene contrato explícito y coherente con `#8` y `#37` | `draftable` |
| `I12-S3` | Alinear operaciones temporales y semántica de semana actual con `#13` y `#37` (provisión/extensión/semana actual derivada; hist. `week_cursor`) | `Codex+Kiko` | `I12-S2`, `#13`, `#37` | Nota/tabla de alineación `#12` ↔ (`#13`, `#37`) | No quedan contradicciones con flujo temporal ni editabilidad | `draftable` |
| `I12-S4` | Cerrar la decisión (revisión interactiva, trazabilidad y referencias) | `Codex+Kiko` | `I12-S3` | Documento final + registro de decisión | Aprobación explícita de Kiko y PR mergeada | `draftable` |

#### Riesgos y bloqueos

- Riesgo de cerrar contrato desalineado con `#13` y/o `#37` si se adelanta demasiado.
- Riesgo de duplicar lógica ya fijada por `#8` (conflictos) y `#9` (temporal).

#### Criterio de cierre de la issue

- Existe contrato de operaciones por agregado con pre/postcondiciones,
  validaciones y reglas de rechazo, alineado con `#13`, `#37` y consistente con
  `#8`.

#### Notas de secuencia / paralelización

- Puede iniciarse en borrador con base en `#7/#8/#9`, pero requiere alineación
  con `#37` para cerrar.
- El cierre se recomienda después de `#13` y `#37` para reducir retrabajo.

### Issue #13 — Especificar estrategia de inicialización de años, estaciones (`season`) y semanas

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
| `I13-S3` | Especificar creación de `year/season/week` y validaciones (estaciones `summer->winter`, 10 semanas por estación) para evitar duplicados/estados inválidos | `Codex` | `I13-S1`, `I13-S2` | Reglas de inicialización y validación | Existen validaciones mínimas, cardinalidades cerradas y estructura temporal consistente | `ready` |
| `I13-S4` | Alinear referencias con `#9` y preparar insumo directo para `#12` | `Codex+Kiko` | `I13-S3` | Referencias cruzadas y nota para `#12` | `#12` puede usar el resultado sin ambigüedad temporal | `ready` |

#### Riesgos y bloqueos

- Riesgo de sobreespecificar operaciones Firestore (eso es `#12`).
- Riesgo de mezclar UX de `#9` con detalle técnico de provisión.

#### Criterio de cierre de la issue

- Estrategia de inicialización/extensión temporal detallada (incluyendo
  estaciones `summer|winter` en orden fijo y 10 semanas por estación),
  consistente con `#9` y sin contradicciones con `docs/domain-glossary.md`.

#### Notas de secuencia / paralelización

- Es el primer candidato técnico recomendado tras `#11`.
- Su cierre reduce incertidumbre para `#12`.

### Issue #37 — Definir política de editabilidad manual y correcciones de estado/sesiones (MVP)

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `ready`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8`, `#9`, `#13` y
  `docs/domain-glossary.md`
- `impacta_a`: `#12`, `#14`, `#15`, `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I37-S1` | Definir matriz de operaciones manuales permitidas (editabilidad "como papel") y límites | `Codex+Kiko` | `#8`, `#9`, `docs/domain-glossary.md` | Matriz de mutabilidad por agregado | Quedan cerradas operaciones manuales permitidas y su alcance MVP | `ready` |
| `I37-S2` | Formalizar reglas de `Entry.reorder`, `Week.reopen/reclose` y correcciones manuales de `Session` | `Codex+Kiko` | `I37-S1` | Reglas por agregado e invariantes | No quedan ambigüedades funcionales sobre mutabilidad de orden/estado/sesiones | `ready` |
| `I37-S3` | Redefinir semántica de semana actual derivada (hist. `week_cursor`) y su recálculo | `Codex+Kiko` | `I37-S2`, `#13` | Reglas de semana actual y alineación temporal | La semana actual derivada queda coherente con temporalidad y editabilidad | `ready` |
| `I37-S4` | Actualizar trazabilidad (`glossary`, conflictos, checklist/bloques) y cerrar decisión | `Codex+Kiko` | `I37-S3` | Documento final + referencias + registro de decisión | Aprobación explícita de Kiko y PR mergeada | `ready` |

#### Riesgos y bloqueos

- Riesgo de dejar `#12` parcialmente redactada con invariantes viejas si `#37`
  no se cierra antes.
- Riesgo de contradicción entre semántica de semana actual derivada (hist.
  `week_cursor`) en temporal (#9/#13)
  y mutabilidad de estado si no se alinea explícitamente.

#### Criterio de cierre de la issue

- Existe una decisión marco de editabilidad manual del MVP ("como papel") que
  fija reordenación manual de `Entry` (intra-`Week`), `Week.reopen/reclose`,
  correcciones manuales completas de `Session` y semana actual derivada (hist.
  `week_cursor`) como primera `Week` abierta, con trazabilidad a
  `#12/#14/#15/#17/#19`.

#### Nota de transición temporal (`#76`)

- Las referencias históricas a `week_cursor` en este documento se reinterpretan
  como **semana actual derivada** (primera `Week` abierta).
- La migración técnica para retirar la dependencia de `campaign.week_cursor` del
  código y contratos residuales queda trazada en `#81`.

#### Notas de secuencia / paralelización

- Debe cerrarse antes de `#12` para evitar retrabajo inmediato del contrato por
  agregado.
- Comparte naturaleza `type:decision`; requiere revisión interactiva con Kiko
  para cierre.

### Issue #14 — Diseñar flujo de sesión activa y reglas de auto-stop

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8`, `#37` y alineación con `#12`
- `impacta_a`: `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I14-S1` | Definir diagrama/tabla de estados y transiciones (`start`, `stop`, `auto-stop`) | `Codex` | `#8`, `docs/domain-glossary.md` | Diagrama/tabla de estados | Todas las transiciones principales están cubiertas | `draftable` |
| `I14-S2` | Especificar reglas operativas por evento y errores esperados | `Codex` | `I14-S1` | Reglas por evento | Se cubren `start`, `stop`, `auto-stop` y errores esperables | `draftable` |
| `I14-S3` | Definir interacción con cierre de semana y efectos sobre sesión activa | `Codex` | `I14-S2`, `#8` | Reglas de cierre de semana + sesión | No rompe invariante `0..1` sesión activa global | `draftable` |
| `I14-S4` | Alinear comportamiento con editabilidad (`#37`) y contrato de operaciones (`#12`) para cierre | `Codex+Kiko` | `I14-S3`, `#37`, `#12` | Alineación final `#14` ↔ (`#37`, `#12`) | No quedan ambigüedades operativas/atómicas para implementar | `draftable` |

#### Riesgos y bloqueos

- Riesgo de cerrar sin contrato técnico por agregado (`#12`) y luego retrabajar.
- Riesgo de inconsistencias con `auto-stop` al cerrar semana.

#### Criterio de cierre de la issue

- Flujo completo de sesión activa y `auto-stop` documentado, consistente con
  invariantes de dominio y concurrencia.

#### Notas de secuencia / paralelización

- Puede iniciarse en borrador con `#8` ya resuelta.
- Conviene cerrar tras avances sustanciales en `#37` y `#12`.

### Issue #15 — Diseñar reglas de validación y recálculo de recursos

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8`, `#37`, `#40` y alineación con `#12`
- `impacta_a`: `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I15-S1` | Inventariar operaciones sobre `Entry.resource_deltas` (ajustar, fijar, limpiar delta neto) | `Codex` | `#8`, `docs/domain-glossary.md`, `#40` | Inventario de operaciones de recursos | Operaciones y efectos quedan enumerados con modelo embebido | `draftable` |
| `I15-S2` | Definir reglas de validación de deltas netos y restricción de totales no negativos | `Codex` | `I15-S1` | Reglas de validación | Casos válidos/inválidos y rechazos quedan cerrados | `draftable` |
| `I15-S3` | Definir estrategia de recálculo y consistencia de totales globales desde `Entry.resource_deltas` | `Codex` | `I15-S2`, `#40` | Estrategia de recálculo | Se documenta consistencia y comportamiento esperado tras correcciones | `draftable` |
| `I15-S4` | Alinear matriz de rechazos con `#8`, editabilidad (`#37`), modelo de recursos (`#40`) y contrato de operaciones (`#12`) | `Codex+Kiko` | `I15-S3`, `#37`, `#40`, `#12` | Alineación final de rechazos y operaciones | No quedan contradicciones con concurrencia ni contrato | `draftable` |

#### Riesgos y bloqueos

- Riesgo de definir validaciones incompatibles con atomicidad esperada de `#12`.
- Riesgo de subestimar casos de corrección/borrado y recálculo en el modelo
  embebido (`Entry.resource_deltas`).

#### Criterio de cierre de la issue

- Reglas de validación y recálculo trazables, con rechazos esperados y
  consistencia con concurrencia/operaciones.

#### Notas de secuencia / paralelización

- Puede avanzar en borrador antes de `#12`.
- Conviene cerrar después de aclarar editabilidad (`#37`), modelo de recursos
  (`#40`) y contrato por agregado en `#12`.

### Issue #16 — Definir consultas mínimas para timeline y panel de foco

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: alineación con `#9`, `#14`, `#15`; compatibilidad
  con `#18`; canon de layout/superficies fijado por Figma para esta issue
- `impacta_a`: `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I16-S1` | Inventariar superficies/estados de pantalla y sus necesidades mínimas de lectura | `Codex` | `#9`, `#14`, Figma (canon de layout para `#16`) | Inventario de superficies y lecturas | Cada superficie/estado visible tiene necesidades mínimas identificadas | `draftable` |
| `I16-S2` | Definir consultas mínimas y campos requeridos por consulta | `Codex` | `I16-S1` | Lista de consultas + campos | Inventario de consultas mínimo y suficiente | `draftable` |
| `I16-S3` | Definir orden, paginación y estabilidad visual (compatibilidad con `#18`) | `Codex+Kiko` | `I16-S2`, `#18` | Reglas de orden/paginación | Orden estable y criterios de paginación documentados | `draftable` |
| `I16-S4` | Documentar riesgos de coste/latencia y límites aceptables del MVP | `Codex` | `I16-S2`, `I16-S3` | Sección de riesgos/rendimiento | Riesgos y límites quedan explícitos y trazables | `draftable` |

#### Riesgos y bloqueos

- Riesgo de usar `tdd.md` como canon de layout en lugar del Figma acordado.
- Riesgo de cerrar consultas antes de fijar orden estable (`#18`).
- Riesgo de sobrecarga de lecturas por no recortar campos mínimos.

#### Criterio de cierre de la issue

- Conjunto mínimo de lecturas de pantalla principal documentado (superficies,
  triggers, orden y no paginación), con límites de rendimiento y coherencia con
  `#9`, `#14`, `#15` y `#18`.

#### Notas de secuencia / paralelización

- Puede iniciarse en borrador antes de `#18`.
- El cierre es más sólido con `#18` resuelta.

### Issue #17 — Preparar matriz de edge cases de concurrencia y sincronización

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: mayor valor con `#37`, `#12`, `#14`, `#15`, `#16`,
  `#18`
- `impacta_a`: `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I17-S1` | Definir taxonomía de casos (sesiones, entries, recursos, temporales, lecturas) | `Codex` | `#7`, `#8` | Taxonomía de edge cases | Taxonomía cubre las familias críticas del MVP | `draftable` |
| `I17-S2` | Construir matriz caso → resultado esperado → severidad → prioridad | `Codex` | `I17-S1` | Matriz de edge cases | Cada caso tiene expectativa y prioridad verificable | `draftable` |
| `I17-S3` | Seleccionar casos críticos de verificación del MVP | `Codex+Kiko` | `I17-S2` | Lista priorizada de casos críticos | Quedan definidos casos críticos mínimos a validar | `draftable` |
| `I17-S4` | Alinear matriz con mutabilidad y contratos/flujos (`#37`, `#12`, `#14`, `#15`, `#18`) antes de cierre | `Codex+Kiko` | `I17-S2`, `#37`, `#12`, `#14`, `#15`, `#18` | Revisión final de consistencia | No hay expectativas en conflicto con docs previas | `draftable` |

#### Riesgos y bloqueos

- Riesgo de matriz incompleta si se cierra antes de contratos/flows clave.
- Riesgo de duplicar casos de prueba que pertenecen a `#19` (esta issue define
  matriz y expectativas, no plan de pruebas completo).

#### Criterio de cierre de la issue

- Matriz de edge cases (taxonomía + escenarios canónicos + variantes) con
  expectativas, severidad y prioridad, alineada con sincronización/concurrencia
  y con insumos técnicos suficientes.

#### Notas de secuencia / paralelización

- Puede arrancar con taxonomía y borrador de matriz.
- Su cierre gana calidad después de `#37`, `#12`, `#14`, `#15` y `#18`.

### Issue #40 — Redefinir modelo de recursos por `Entry` (delta neto por recurso, sin `ResourceChange`)

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `draftable` (cerrada en seguimiento; este bloque conserva el estado inicial del plan)
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8`, `#12`, `#37` y
  `docs/domain-glossary.md`
- `impacta_a`: `#15`, `#17`, `#18`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I40-S1` | Definir el modelo de recursos por `Entry` (`resource_deltas`) y eliminar `ResourceChange` como entidad MVP | `Codex+Kiko` | `docs/domain-glossary.md`, `#37` | Decisión de modelo (`docs/resource-delta-model.md`) | Semántica neta por recurso cerrada y sin ambigüedad | `draftable` |
| `I40-S2` | Parchear consistencia en glosario, conflictos y contrato `#12` (supersesión parcial de recursos) | `Codex` | `I40-S1`, `#12`, `#8` | Docs oficiales alineados | No quedan referencias activas contradictorias a `ResourceChange` en el MVP | `draftable` |
| `I40-S3` | Actualizar orden técnico/trazabilidad downstream (`#15`, `#17`, `#18`, `#19`) | `Codex` | `I40-S2` | Checklist/bloques/referencias actualizados | `#18` vuelve a quedar como siguiente paso técnico tras `#40` | `draftable` |
| `I40-S4` | Cerrar la decisión (revisión interactiva, registro en decision-log, PR mergeada) | `Codex+Kiko` | `I40-S3` | Decisión aceptada + `DEC-0024` + PR mergeada | Aprobación explícita de Kiko y cierre end-to-end | `draftable` |

#### Riesgos y bloqueos

- Riesgo de dejar `#12` contradictoria si se cambia el dominio de recursos sin
  parchear el contrato de operaciones.
- Riesgo de que `#18` inventarie eventos/listas innecesarios si se mantiene el
  modelo antiguo de `ResourceChange`.

#### Criterio de cierre de la issue

- Existe decisión de dominio oficial que sustituye `ResourceChange` por
  `Entry.resource_deltas` (delta neto por recurso) y deja glosario, conflictos
  y contrato `#12` alineados mediante supersesión parcial explícita.

#### Notas de secuencia / paralelización

- Debe cerrarse antes de `#18` para evitar retrabajo en inventario de eventos y
  contratos de recursos.
- Comparte naturaleza `type:decision`; requiere revisión interactiva con Kiko
  para cierre.

### Issue #18 — Definir política de timestamps y orden estable entre dispositivos

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `draftable`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#7`, `#8`; compatibilidad con
  `#12`, `#40` y lecturas (`#16`)
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
  contratos/modelo de datos (`#12`, `#40`).
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
| `I19-S4` | Priorizar ejecución de pruebas para soportar `#20` | `Codex+Kiko` | `I19-S2`, `I19-S3`, `#37`, `#12`, `#14`, `#15`, `#18` | Priorización para readiness | El plan sirve como insumo directo para el gate de `#20` | `draftable` |

#### Riesgos y bloqueos

- Riesgo de plan incompleto si faltan contratos/flows/orden estable.
- Riesgo de mezclar definición de pruebas con ejecución real (esta issue solo
  define el plan).

#### Criterio de cierre de la issue

- Plan de pruebas de invariantes priorizado, repetible y trazable, apto para
  sustentar el gate de `#20`.

#### Notas de secuencia / paralelización

- Puede comenzar con selección de invariantes y estructura de casos.
- El cierre se fortalece con `#37`, `#12`, `#14`, `#15` y `#18` resueltas.

### Issue #20 — Definir criterios de listo para codificar en Fase 1

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `final_gate`
- `responsable_de_coordinación`: `Codex+Kiko`
- `dependencias_de_cierre`: checklist base (`#10`) y derivados relevantes
  (`#11`–`#19`, más `#37`) según criterios definidos
- `impacta_a`: paso a implementación

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalización | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I20-S1` | Inventariar precondiciones y dependencias críticas de readiness | `Codex` | `#10`, `#11` y estado de `#12`–`#19` + `#37` | Inventario de precondiciones | Dependencias críticas quedan listadas y clasificadas | `final_gate` |
| `I20-S2` | Definir checklist de bloqueo/desbloqueo para entrada a codificación | `Codex` | `I20-S1` | Checklist de readiness | El gate de entrada es explícito y verificable | `final_gate` |
| `I20-S3` | Definir evidencia mínima exigida (documental y trazabilidad) | `Codex` | `I20-S2` | Reglas de evidencia | Queda claro qué evidencia se exige para habilitar código | `final_gate` |
| `I20-S4` | Definir flujo de validación final (Codex prepara, Kiko valida) y criterio de cierre | `Codex+Kiko` | `I20-S3` | Protocolo de validación final | El cierre de `#20` queda operable y sin ambigüedades | `final_gate` |

#### Riesgos y bloqueos

- Riesgo de cerrar `#20` demasiado pronto y convertirlo en gate vacío.
- Riesgo de duplicar detalle de `#11` o reabrir decisiones de `#12`/`#18`/`#37`.

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

1. Priorizar primero **unidad pendiente de cierre** (trabajo local/rama/PR/issue
   pendiente de cierre) antes de iniciar trabajo nuevo.
1. Si no existe unidad pendiente de cierre, priorizar PRs abiertas.
1. Usar el **orden técnico recomendado** del documento más específico disponible
   para elegir el siguiente trabajo cuando no haya unidad pendiente de cierre
   ni PRs abiertas.
1. Si el siguiente item técnico no es cerrable, saltar al siguiente cerrable.
1. Si no hay cerrables, avanzar en el primer `draftable`.
1. Si no existe orden técnico aplicable, usar la issue abierta con número más
   bajo.
1. Mantener trazabilidad de estado (`ready`, `draftable`, `blocked`,
   `final_gate`) al revisar el plan.

## Seguimiento de bloques

### Estado de bloques (actualizado tras cerrar #13, #37, #12, #40, #18, #14, #15, #16, #17, #19 y #20)

- [x] `#11` Desglose en bloques ejecutables (este documento)
- [x] `#13` Inicialización temporal detallada (`ready`)
- [x] `#37` Política de editabilidad manual y correcciones de dominio (`ready`)
- [x] `#12` Contrato Firestore por agregado (`draftable`)
- [x] `#40` Modelo de recursos por `Entry` (delta neto; `draftable`)
- [x] `#18` Timestamps y orden estable (`draftable`)
- [x] `#14` Flujo de sesión activa y `auto-stop` (`draftable`)
- [x] `#15` Validación y recálculo de recursos (`draftable`)
- [x] `#16` Consultas mínimas para timeline/foco (`draftable`)
- [x] `#17` Matriz de edge cases (`draftable`)
- [x] `#19` Plan de pruebas de invariantes (`draftable`)
- [x] `#20` Gate de listo para codificar (`final_gate`)

### Seguimiento de implementación (post-`#20`)

- [x] `#51` Bootstrap de app Flet y estructura base
- [x] `#52` Shell de pantalla principal (layout base Figma)
- [x] `#53` Estado local de navegación/visor sticky/activo mock
- [x] `#54` Integración read-only inicial (`Q1/Q2/Q3/Q4/Q6/Q7`)
- [x] `#86` Selección temporal y feedback semanal en UI (solo tiles + feedback)
- [x] `#90` Simplificación de complejidad accidental en `app_root`/`main_shell_view`/placeholders
- [x] `#92` Refactor declarativo completo (MVU) de Main Shell en estructura feature-first (pre-U3)

### Próxima secuencia técnica esperada (según orden actual)

1. `U3-panel-actions-real-handlers` Conectar `start`, `stop`, `add session` y `delete entry` con handlers reales
1. `U4-mobile-robustness-min` Mejorar robustez móvil mínima (`portrait` + `landscape`) en barra temporal y panel central
1. `U5-read-write-vertical-slice` Cerrar vertical read/write MVP de una operación completa con refresco visible

Al priorizar una unidad, abrir primero su issue y sustituir el identificador `U*` por `#<issue>` en seguimiento.

## Referencias

- `AGENTS.md`
- `docs/system-map.md`
- `docs/repo-workflow.md`
- `docs/mvp-implementation-checklist.md`
- `docs/sync-strategy.md`
- `docs/conflict-policy.md`
- `docs/firestore-operation-contract.md`
- `docs/resource-delta-model.md`
- `docs/resource-validation-recalculation.md`
- `docs/timestamp-order-policy.md`
- `docs/active-session-flow.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/editability-policy.md`
- `docs/domain-glossary.md`
- `docs/context-checklists.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/10`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/11`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/92`
