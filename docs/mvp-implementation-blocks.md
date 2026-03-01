# Bloques de ImplementaciÃ³n MVP (Desglose Operativo)

## Metadatos

- `doc_id`: DOC-MVP-IMPLEMENTATION-BLOCKS
- `purpose`: Desglosar el checklist tÃ©cnico base de implementaciÃ³n MVP en bloques y subbloques ejecutables con trazabilidad, incluyendo decisiones marco posteriores que alteren el orden tÃ©cnico.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-01
- `next_review`: 2026-03-13

## Objetivo

Convertir el checklist tÃ©cnico base de `docs/mvp-implementation-checklist.md`
(Issue #10) en un desglose operativo por issues y subbloques ejecutables para
la preparaciÃ³n de implementaciÃ³n del MVP, sin codificar todavÃ­a.

## Alcance y no alcance

Incluye:

- desglose detallado de las Issues `#12`â€“`#20` y decisiones marco intermedias
  que afecten su secuencia (actualmente `#37` y `#40`) por subbloques
  ejecutables;
- responsables por rol (`Codex`, `Kiko`, `Codex+Kiko`);
- entregables, dependencias y criterios de finalizaciÃ³n por subbloque;
- riesgos y bloqueos por issue;
- reglas de secuencia y ejecuciÃ³n para operar el plan.

No incluye:

- implementaciÃ³n de cÃ³digo de app;
- cierre de las Issues `#12`â€“`#20` (ni de decisiones marco intermedias como
  `#37`) en este documento;
- gate final de â€œlisto para codificarâ€ (solo su desglose planificado);
- redefinir por sÃ­ mismo reglas globales de repo (eso se formaliza en la issue
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

## RelaciÃ³n con `#10`, `#20` y la regla de `siguiente paso`

- **#10** define el checklist tÃ©cnico base (macro-bloques, secuencia y
  verificaciÃ³n mÃ­nima).
- **#11** (este documento) aÃ±ade el desglose fino en bloques/subbloques
  ejecutables.
- **#20** sigue reservado al gate final de entrada a codificaciÃ³n.

### Nota operativa sobre `siguiente paso` y orden tÃ©cnico

- Si existe un **orden tÃ©cnico recomendado** documentado, `siguiente paso` lo
  prioriza.
- La fuente de orden tÃ©cnico debe ser el **documento oficial mÃ¡s especÃ­fico**
  disponible (detalle > macro).
- Si un item tÃ©cnico estÃ¡ abierto pero no es cerrable, se salta al siguiente
  item cerrable.
- Si no hay items cerrables, se toma el primer item `draftable`.
- Si no existe orden tÃ©cnico aplicable, `siguiente paso` vuelve al criterio de
  issue abierta con nÃºmero mÃ¡s bajo.

## Convenciones de bloques y subbloques

### Estados iniciales de bloque/subbloque

- `ready`: puede iniciarse y cerrarse con dependencias actuales.
- `draftable`: puede iniciarse en borrador, pero su cierre depende de otros
  bloques/issues.
- `blocked`: no debe cerrarse hasta resolver dependencias faltantes.
- `final_gate`: bloque reservado para cierre final de preparaciÃ³n.

### Roles de responsable

- `Codex`: propuesta, redacciÃ³n, estructura y trazabilidad documental.
- `Kiko`: validaciÃ³n y aprobaciÃ³n (cuando aplique).
- `Codex+Kiko`: trabajo interactivo o revisiÃ³n conjunta.

### Formato de subbloque

- `I<issue>-S<n>`
- Ejemplos: `I12-S1`, `I18-S3`

## Resumen ejecutivo de bloques

| Issue | Tipo | Estado inicial | Orden tÃ©cnico recomendado | Â¿Puede iniciar borrador? | Cierre condicionado por | Entregable principal |
| --- | --- | --- | --- | --- | --- | --- |
| #13 | `task` | `ready` | 1.Âº dentro del bloque B | SÃ­ | Coherencia con #9 y dominio | Estrategia tÃ©cnica de inicializaciÃ³n/extensiÃ³n temporal |
| #37 | `decision` | `ready` | 2.Âº dentro del bloque B | SÃ­ | Coherencia con #8/#9/#13 y dominio | PolÃ­tica de editabilidad manual y correcciones de dominio |
| #12 | `decision` | `draftable` | 3.Âº dentro del bloque B | SÃ­ | AlineaciÃ³n con #13 y #37 (cierre recomendado con ambas cerradas) | Contrato de operaciones Firestore por agregado |
| #40 | `decision` | `draftable` | 4.Âº dentro del bloque B | SÃ­ | Coherencia con #12/#37 y glosario; supersesiÃ³n parcial de recursos | Modelo de recursos por `Entry` (`resource_deltas`) |
| #14 | `task` | `draftable` | 1.Âº del bloque C | SÃ­ | AlineaciÃ³n con #12 para cierre | Flujo de sesiÃ³n activa y `auto-stop` |
| #15 | `task` | `draftable` | 2.Âº del bloque C | SÃ­ | AlineaciÃ³n con #12 para cierre | Reglas de validaciÃ³n y recÃ¡lculo de recursos |
| #16 | `task` | `draftable` | 1.Âº del bloque D | SÃ­ | Compatibilidad con #18 para cierre | Inventario mÃ­nimo de consultas y orden/paginaciÃ³n |
| #17 | `task` | `draftable` | 2.Âº del bloque D | SÃ­ | Mayor valor tras #12/#14/#15/#18 | Matriz de edge cases de concurrencia/sincronizaciÃ³n |
| #18 | `decision` | `draftable` | 5.Âº dentro del bloque B | SÃ­ | Compatibilidad con #12, #40 y lecturas | PolÃ­tica de timestamps y desempate estable |
| #19 | `task` | `draftable` | 3.Âº del bloque D | SÃ­ | Insumos suficientes de contratos/flows | Plan de pruebas de invariantes |
| #20 | `task` | `final_gate` | Ãšltimo (bloque E) | No (cierre final) | Base de #10 + derivadas relevantes | Gate de listo para codificar |

## Detalle por issue (`#12`â€“`#20`) y decisiones marco intermedias (`#37`, `#40`)

### Issue #12 â€” Definir contrato de operaciones Firestore por agregado de dominio

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `draftable` (cerrada en seguimiento; este bloque conserva el estado inicial del plan)
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: `#13` (alineaciÃ³n temporal estable), `#37`
  (editabilidad e invariantes actualizadas), mÃ¡s coherencia con `#7`, `#8`,
  `#9` (ya resueltas)
- `impacta_a`: `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I12-S1` | Inventariar operaciones por agregado (`campaign`, `week`, `entry` incl. `resource_deltas`, `session`) y casos de uso | `Codex` | `#7`, `#8`, `#9`, `#37` | Tabla de operaciones por agregado | Inventario completo y sin solapes obvios con mutabilidad vigente | `draftable` |
| `I12-S2` | Definir contrato por agregado (precondiciones, postcondiciones, validaciones, rechazo por conflicto/transiciÃ³n invÃ¡lida, atomicidad esperada) | `Codex` | `I12-S1` | Tabla de contrato por agregado | Cada agregado tiene contrato explÃ­cito y coherente con `#8` y `#37` | `draftable` |
| `I12-S3` | Alinear operaciones temporales y semÃ¡ntica de semana actual con `#13` y `#37` (provisiÃ³n/extensiÃ³n/semana actual derivada; hist. `week_cursor`) | `Codex+Kiko` | `I12-S2`, `#13`, `#37` | Nota/tabla de alineaciÃ³n `#12` â†” (`#13`, `#37`) | No quedan contradicciones con flujo temporal ni editabilidad | `draftable` |
| `I12-S4` | Cerrar la decisiÃ³n (revisiÃ³n interactiva, trazabilidad y referencias) | `Codex+Kiko` | `I12-S3` | Documento final + registro de decisiÃ³n | AprobaciÃ³n explÃ­cita de Kiko y PR mergeada | `draftable` |

#### Riesgos y bloqueos

- Riesgo de cerrar contrato desalineado con `#13` y/o `#37` si se adelanta demasiado.
- Riesgo de duplicar lÃ³gica ya fijada por `#8` (conflictos) y `#9` (temporal).

#### Criterio de cierre de la issue

- Existe contrato de operaciones por agregado con pre/postcondiciones,
  validaciones y reglas de rechazo, alineado con `#13`, `#37` y consistente con
  `#8`.

#### Notas de secuencia / paralelizaciÃ³n

- Puede iniciarse en borrador con base en `#7/#8/#9`, pero requiere alineaciÃ³n
  con `#37` para cerrar.
- El cierre se recomienda despuÃ©s de `#13` y `#37` para reducir retrabajo.

### Issue #13 â€” Especificar estrategia de inicializaciÃ³n de aÃ±os, estaciones (`season`) y semanas

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `ready`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#9` y `docs/domain-glossary.md`
- `impacta_a`: `#12`, `#16`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I13-S1` | Definir flujo tÃ©cnico de provisiÃ³n inicial de 4 aÃ±os en `campaign/01` | `Codex` | `#9` | EspecificaciÃ³n del flujo inicial | Queda descrito de forma no ambigua y sin contradicciÃ³n con `#9` | `ready` |
| `I13-S2` | Definir regla de extensiÃ³n manual `+1` aÃ±o con confirmaciÃ³n y criterios de creaciÃ³n | `Codex` | `I13-S1`, `#9` | EspecificaciÃ³n de extensiÃ³n `+1` | Se documenta comportamiento completo de extensiÃ³n manual | `ready` |
| `I13-S3` | Especificar creaciÃ³n de `year/season/week` y validaciones (estaciones `summer->winter`, 10 semanas por estaciÃ³n) para evitar duplicados/estados invÃ¡lidos | `Codex` | `I13-S1`, `I13-S2` | Reglas de inicializaciÃ³n y validaciÃ³n | Existen validaciones mÃ­nimas, cardinalidades cerradas y estructura temporal consistente | `ready` |
| `I13-S4` | Alinear referencias con `#9` y preparar insumo directo para `#12` | `Codex+Kiko` | `I13-S3` | Referencias cruzadas y nota para `#12` | `#12` puede usar el resultado sin ambigÃ¼edad temporal | `ready` |

#### Riesgos y bloqueos

- Riesgo de sobreespecificar operaciones Firestore (eso es `#12`).
- Riesgo de mezclar UX de `#9` con detalle tÃ©cnico de provisiÃ³n.

#### Criterio de cierre de la issue

- Estrategia de inicializaciÃ³n/extensiÃ³n temporal detallada (incluyendo
  estaciones `summer|winter` en orden fijo y 10 semanas por estaciÃ³n),
  consistente con `#9` y sin contradicciones con `docs/domain-glossary.md`.

#### Notas de secuencia / paralelizaciÃ³n

- Es el primer candidato tÃ©cnico recomendado tras `#11`.
- Su cierre reduce incertidumbre para `#12`.

### Issue #37 â€” Definir polÃ­tica de editabilidad manual y correcciones de estado/sesiones (MVP)

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `ready`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8`, `#9`, `#13` y
  `docs/domain-glossary.md`
- `impacta_a`: `#12`, `#14`, `#15`, `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I37-S1` | Definir matriz de operaciones manuales permitidas (editabilidad "como papel") y lÃ­mites | `Codex+Kiko` | `#8`, `#9`, `docs/domain-glossary.md` | Matriz de mutabilidad por agregado | Quedan cerradas operaciones manuales permitidas y su alcance MVP | `ready` |
| `I37-S2` | Formalizar reglas de `Entry.reorder`, `Week.reopen/reclose` y correcciones manuales de `Session` | `Codex+Kiko` | `I37-S1` | Reglas por agregado e invariantes | No quedan ambigÃ¼edades funcionales sobre mutabilidad de orden/estado/sesiones | `ready` |
| `I37-S3` | Redefinir semÃ¡ntica de semana actual derivada (hist. `week_cursor`) y su recÃ¡lculo | `Codex+Kiko` | `I37-S2`, `#13` | Reglas de semana actual y alineaciÃ³n temporal | La semana actual derivada queda coherente con temporalidad y editabilidad | `ready` |
| `I37-S4` | Actualizar trazabilidad (`glossary`, conflictos, checklist/bloques) y cerrar decisiÃ³n | `Codex+Kiko` | `I37-S3` | Documento final + referencias + registro de decisiÃ³n | AprobaciÃ³n explÃ­cita de Kiko y PR mergeada | `ready` |

#### Riesgos y bloqueos

- Riesgo de dejar `#12` parcialmente redactada con invariantes viejas si `#37`
  no se cierra antes.
- Riesgo de contradicciÃ³n entre semÃ¡ntica de semana actual derivada (hist.
  `week_cursor`) en temporal (#9/#13)
  y mutabilidad de estado si no se alinea explÃ­citamente.

#### Criterio de cierre de la issue

- Existe una decisiÃ³n marco de editabilidad manual del MVP ("como papel") que
  fija reordenaciÃ³n manual de `Entry` (intra-`Week`), `Week.reopen/reclose`,
  correcciones manuales completas de `Session` y semana actual derivada (hist.
  `week_cursor`) como primera `Week` abierta, con trazabilidad a
  `#12/#14/#15/#17/#19`.

#### Nota de transiciÃ³n temporal (`#76`)

- Las referencias histÃ³ricas a `week_cursor` en este documento se reinterpretan
  como **semana actual derivada** (primera `Week` abierta).
- La migraciÃ³n tÃ©cnica para retirar la dependencia de `campaign.week_cursor` del
  cÃ³digo y contratos residuales queda trazada en `#81`.

#### Notas de secuencia / paralelizaciÃ³n

- Debe cerrarse antes de `#12` para evitar retrabajo inmediato del contrato por
  agregado.
- Comparte naturaleza `type:decision`; requiere revisiÃ³n interactiva con Kiko
  para cierre.

### Issue #14 â€” DiseÃ±ar flujo de sesiÃ³n activa y reglas de auto-stop

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8`, `#37` y alineaciÃ³n con `#12`
- `impacta_a`: `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I14-S1` | Definir diagrama/tabla de estados y transiciones (`start`, `stop`, `auto-stop`) | `Codex` | `#8`, `docs/domain-glossary.md` | Diagrama/tabla de estados | Todas las transiciones principales estÃ¡n cubiertas | `draftable` |
| `I14-S2` | Especificar reglas operativas por evento y errores esperados | `Codex` | `I14-S1` | Reglas por evento | Se cubren `start`, `stop`, `auto-stop` y errores esperables | `draftable` |
| `I14-S3` | Definir interacciÃ³n con cierre de semana y efectos sobre sesiÃ³n activa | `Codex` | `I14-S2`, `#8` | Reglas de cierre de semana + sesiÃ³n | No rompe invariante `0..1` sesiÃ³n activa global | `draftable` |
| `I14-S4` | Alinear comportamiento con editabilidad (`#37`) y contrato de operaciones (`#12`) para cierre | `Codex+Kiko` | `I14-S3`, `#37`, `#12` | AlineaciÃ³n final `#14` â†” (`#37`, `#12`) | No quedan ambigÃ¼edades operativas/atÃ³micas para implementar | `draftable` |

#### Riesgos y bloqueos

- Riesgo de cerrar sin contrato tÃ©cnico por agregado (`#12`) y luego retrabajar.
- Riesgo de inconsistencias con `auto-stop` al cerrar semana.

#### Criterio de cierre de la issue

- Flujo completo de sesiÃ³n activa y `auto-stop` documentado, consistente con
  invariantes de dominio y concurrencia.

#### Notas de secuencia / paralelizaciÃ³n

- Puede iniciarse en borrador con `#8` ya resuelta.
- Conviene cerrar tras avances sustanciales en `#37` y `#12`.

### Issue #15 â€” DiseÃ±ar reglas de validaciÃ³n y recÃ¡lculo de recursos

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8`, `#37`, `#40` y alineaciÃ³n con `#12`
- `impacta_a`: `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I15-S1` | Inventariar operaciones sobre `Entry.resource_deltas` (ajustar, fijar, limpiar delta neto) | `Codex` | `#8`, `docs/domain-glossary.md`, `#40` | Inventario de operaciones de recursos | Operaciones y efectos quedan enumerados con modelo embebido | `draftable` |
| `I15-S2` | Definir reglas de validaciÃ³n de deltas netos y restricciÃ³n de totales no negativos | `Codex` | `I15-S1` | Reglas de validaciÃ³n | Casos vÃ¡lidos/invÃ¡lidos y rechazos quedan cerrados | `draftable` |
| `I15-S3` | Definir estrategia de recÃ¡lculo y consistencia de totales globales desde `Entry.resource_deltas` | `Codex` | `I15-S2`, `#40` | Estrategia de recÃ¡lculo | Se documenta consistencia y comportamiento esperado tras correcciones | `draftable` |
| `I15-S4` | Alinear matriz de rechazos con `#8`, editabilidad (`#37`), modelo de recursos (`#40`) y contrato de operaciones (`#12`) | `Codex+Kiko` | `I15-S3`, `#37`, `#40`, `#12` | AlineaciÃ³n final de rechazos y operaciones | No quedan contradicciones con concurrencia ni contrato | `draftable` |

#### Riesgos y bloqueos

- Riesgo de definir validaciones incompatibles con atomicidad esperada de `#12`.
- Riesgo de subestimar casos de correcciÃ³n/borrado y recÃ¡lculo en el modelo
  embebido (`Entry.resource_deltas`).

#### Criterio de cierre de la issue

- Reglas de validaciÃ³n y recÃ¡lculo trazables, con rechazos esperados y
  consistencia con concurrencia/operaciones.

#### Notas de secuencia / paralelizaciÃ³n

- Puede avanzar en borrador antes de `#12`.
- Conviene cerrar despuÃ©s de aclarar editabilidad (`#37`), modelo de recursos
  (`#40`) y contrato por agregado en `#12`.

### Issue #16 â€” Definir consultas mÃ­nimas para timeline y panel de foco

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: alineaciÃ³n con `#9`, `#14`, `#15`; compatibilidad
  con `#18`; canon de layout/superficies fijado por Figma para esta issue
- `impacta_a`: `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I16-S1` | Inventariar superficies/estados de pantalla y sus necesidades mÃ­nimas de lectura | `Codex` | `#9`, `#14`, Figma (canon de layout para `#16`) | Inventario de superficies y lecturas | Cada superficie/estado visible tiene necesidades mÃ­nimas identificadas | `draftable` |
| `I16-S2` | Definir consultas mÃ­nimas y campos requeridos por consulta | `Codex` | `I16-S1` | Lista de consultas + campos | Inventario de consultas mÃ­nimo y suficiente | `draftable` |
| `I16-S3` | Definir orden, paginaciÃ³n y estabilidad visual (compatibilidad con `#18`) | `Codex+Kiko` | `I16-S2`, `#18` | Reglas de orden/paginaciÃ³n | Orden estable y criterios de paginaciÃ³n documentados | `draftable` |
| `I16-S4` | Documentar riesgos de coste/latencia y lÃ­mites aceptables del MVP | `Codex` | `I16-S2`, `I16-S3` | SecciÃ³n de riesgos/rendimiento | Riesgos y lÃ­mites quedan explÃ­citos y trazables | `draftable` |

#### Riesgos y bloqueos

- Riesgo de usar `tdd.md` (retirado el 2026-03-01) como canon de layout en lugar del Figma acordado.
- Riesgo de cerrar consultas antes de fijar orden estable (`#18`).
- Riesgo de sobrecarga de lecturas por no recortar campos mÃ­nimos.

#### Criterio de cierre de la issue

- Conjunto mÃ­nimo de lecturas de pantalla principal documentado (superficies,
  triggers, orden y no paginaciÃ³n), con lÃ­mites de rendimiento y coherencia con
  `#9`, `#14`, `#15` y `#18`.

#### Notas de secuencia / paralelizaciÃ³n

- Puede iniciarse en borrador antes de `#18`.
- El cierre es mÃ¡s sÃ³lido con `#18` resuelta.

### Issue #17 â€” Preparar matriz de edge cases de concurrencia y sincronizaciÃ³n

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: mayor valor con `#37`, `#12`, `#14`, `#15`, `#16`,
  `#18`
- `impacta_a`: `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I17-S1` | Definir taxonomÃ­a de casos (sesiones, entries, recursos, temporales, lecturas) | `Codex` | `#7`, `#8` | TaxonomÃ­a de edge cases | TaxonomÃ­a cubre las familias crÃ­ticas del MVP | `draftable` |
| `I17-S2` | Construir matriz caso â†’ resultado esperado â†’ severidad â†’ prioridad | `Codex` | `I17-S1` | Matriz de edge cases | Cada caso tiene expectativa y prioridad verificable | `draftable` |
| `I17-S3` | Seleccionar casos crÃ­ticos de verificaciÃ³n del MVP | `Codex+Kiko` | `I17-S2` | Lista priorizada de casos crÃ­ticos | Quedan definidos casos crÃ­ticos mÃ­nimos a validar | `draftable` |
| `I17-S4` | Alinear matriz con mutabilidad y contratos/flujos (`#37`, `#12`, `#14`, `#15`, `#18`) antes de cierre | `Codex+Kiko` | `I17-S2`, `#37`, `#12`, `#14`, `#15`, `#18` | RevisiÃ³n final de consistencia | No hay expectativas en conflicto con docs previas | `draftable` |

#### Riesgos y bloqueos

- Riesgo de matriz incompleta si se cierra antes de contratos/flows clave.
- Riesgo de duplicar casos de prueba que pertenecen a `#19` (esta issue define
  matriz y expectativas, no plan de pruebas completo).

#### Criterio de cierre de la issue

- Matriz de edge cases (taxonomÃ­a + escenarios canÃ³nicos + variantes) con
  expectativas, severidad y prioridad, alineada con sincronizaciÃ³n/concurrencia
  y con insumos tÃ©cnicos suficientes.

#### Notas de secuencia / paralelizaciÃ³n

- Puede arrancar con taxonomÃ­a y borrador de matriz.
- Su cierre gana calidad despuÃ©s de `#37`, `#12`, `#14`, `#15` y `#18`.

### Issue #40 â€” Redefinir modelo de recursos por `Entry` (delta neto por recurso, sin `ResourceChange`)

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `draftable` (cerrada en seguimiento; este bloque conserva el estado inicial del plan)
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#8`, `#12`, `#37` y
  `docs/domain-glossary.md`
- `impacta_a`: `#15`, `#17`, `#18`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I40-S1` | Definir el modelo de recursos por `Entry` (`resource_deltas`) y eliminar `ResourceChange` como entidad MVP | `Codex+Kiko` | `docs/domain-glossary.md`, `#37` | DecisiÃ³n de modelo (`docs/resource-delta-model.md`) | SemÃ¡ntica neta por recurso cerrada y sin ambigÃ¼edad | `draftable` |
| `I40-S2` | Parchear consistencia en glosario, conflictos y contrato `#12` (supersesiÃ³n parcial de recursos) | `Codex` | `I40-S1`, `#12`, `#8` | Docs oficiales alineados | No quedan referencias activas contradictorias a `ResourceChange` en el MVP | `draftable` |
| `I40-S3` | Actualizar orden tÃ©cnico/trazabilidad downstream (`#15`, `#17`, `#18`, `#19`) | `Codex` | `I40-S2` | Checklist/bloques/referencias actualizados | `#18` vuelve a quedar como siguiente paso tÃ©cnico tras `#40` | `draftable` |
| `I40-S4` | Cerrar la decisiÃ³n (revisiÃ³n interactiva, registro en decision-log, PR mergeada) | `Codex+Kiko` | `I40-S3` | DecisiÃ³n aceptada + `DEC-0024` + PR mergeada | AprobaciÃ³n explÃ­cita de Kiko y cierre end-to-end | `draftable` |

#### Riesgos y bloqueos

- Riesgo de dejar `#12` contradictoria si se cambia el dominio de recursos sin
  parchear el contrato de operaciones.
- Riesgo de que `#18` inventarie eventos/listas innecesarios si se mantiene el
  modelo antiguo de `ResourceChange`.

#### Criterio de cierre de la issue

- Existe decisiÃ³n de dominio oficial que sustituye `ResourceChange` por
  `Entry.resource_deltas` (delta neto por recurso) y deja glosario, conflictos
  y contrato `#12` alineados mediante supersesiÃ³n parcial explÃ­cita.

#### Notas de secuencia / paralelizaciÃ³n

- Debe cerrarse antes de `#18` para evitar retrabajo en inventario de eventos y
  contratos de recursos.
- Comparte naturaleza `type:decision`; requiere revisiÃ³n interactiva con Kiko
  para cierre.

### Issue #18 â€” Definir polÃ­tica de timestamps y orden estable entre dispositivos

#### Ficha de bloque

- `tipo`: `decision`
- `estado_inicial`: `draftable`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: coherencia con `#7`, `#8`; compatibilidad con
  `#12`, `#40` y lecturas (`#16`)
- `impacta_a`: `#16`, `#17`, `#19`, `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I18-S1` | Inventariar eventos ordenables y puntos donde se necesita orden estable | `Codex` | `#7`, `#8`, `tdd.md` (retirado el 2026-03-01) | Inventario de eventos ordenables | Se cubren timeline, logs y lecturas crÃ­ticas | `draftable` |
| `I18-S2` | Preparar opciones de polÃ­tica (timestamps y desempate) con tradeoffs | `Codex` | `I18-S1` | Comparativa de opciones | Opciones comparables y criterios de decisiÃ³n explÃ­citos | `draftable` |
| `I18-S3` | Cerrar decisiÃ³n final con Kiko (modo interactivo) y contrato de orden estable | `Codex+Kiko` | `I18-S2` | DecisiÃ³n aceptada + polÃ­tica final | AprobaciÃ³n explÃ­cita de Kiko y contrato documentado | `draftable` |
| `I18-S4` | Alinear trazabilidad y compatibilidad con `#16`, `#17`, `#19` | `Codex+Kiko` | `I18-S3` | Referencias cruzadas actualizadas | Las issues downstream pueden usar la polÃ­tica sin ambigÃ¼edad | `draftable` |

#### Riesgos y bloqueos

- Riesgo de definir desempate incompatible con consultas mÃ­nimas (`#16`) o
  contratos/modelo de datos (`#12`, `#40`).
- Riesgo de cerrar sin inventario completo de eventos ordenables.

#### Criterio de cierre de la issue

- PolÃ­tica de timestamps y orden estable aceptada, trazable y compatible con
  sincronizaciÃ³n, concurrencia y lecturas previstas.

#### Notas de secuencia / paralelizaciÃ³n

- Puede arrancar en borrador antes de `#12`.
- Requiere revisiÃ³n interactiva con Kiko para cierre (`type:decision`).

### Issue #19 â€” Preparar plan de pruebas para invariantes de dominio

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `draftable`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: insumos suficientes de contratos/flows/orden
- `impacta_a`: `#20`

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I19-S1` | Seleccionar invariantes crÃ­ticas del dominio (a partir de `docs/domain-glossary.md` y decisiones cerradas) | `Codex` | `docs/domain-glossary.md`, `#7`, `#8`, `#9` | Lista priorizada de invariantes | Invariantes crÃ­ticas quedan seleccionadas y justificadas | `draftable` |
| `I19-S2` | DiseÃ±ar casos de prueba por invariante (precondiciÃ³n, acciÃ³n, resultado esperado) | `Codex` | `I19-S1` | Matriz de casos por invariante | Cada invariante tiene casos verificables | `draftable` |
| `I19-S3` | Definir estrategia de evidencia y repetibilidad | `Codex` | `I19-S2` | Estrategia de evidencia | Queda claro cÃ³mo registrar y repetir validaciones | `draftable` |
| `I19-S4` | Priorizar ejecuciÃ³n de pruebas para soportar `#20` | `Codex+Kiko` | `I19-S2`, `I19-S3`, `#37`, `#12`, `#14`, `#15`, `#18` | PriorizaciÃ³n para readiness | El plan sirve como insumo directo para el gate de `#20` | `draftable` |

#### Riesgos y bloqueos

- Riesgo de plan incompleto si faltan contratos/flows/orden estable.
- Riesgo de mezclar definiciÃ³n de pruebas con ejecuciÃ³n real (esta issue solo
  define el plan).

#### Criterio de cierre de la issue

- Plan de pruebas de invariantes priorizado, repetible y trazable, apto para
  sustentar el gate de `#20`.

#### Notas de secuencia / paralelizaciÃ³n

- Puede comenzar con selecciÃ³n de invariantes y estructura de casos.
- El cierre se fortalece con `#37`, `#12`, `#14`, `#15` y `#18` resueltas.

### Issue #20 â€” Definir criterios de listo para codificar en Fase 1

#### Ficha de bloque

- `tipo`: `task`
- `estado_inicial`: `final_gate`
- `responsable_de_coordinaciÃ³n`: `Codex+Kiko`
- `dependencias_de_cierre`: checklist base (`#10`) y derivados relevantes
  (`#11`â€“`#19`, mÃ¡s `#37`) segÃºn criterios definidos
- `impacta_a`: paso a implementaciÃ³n

#### Subbloques ejecutables

| subbloque_id | objetivo | responsable | depende_de | entregable | criterio_de_finalizaciÃ³n | estado_inicial |
| --- | --- | --- | --- | --- | --- | --- |
| `I20-S1` | Inventariar precondiciones y dependencias crÃ­ticas de readiness | `Codex` | `#10`, `#11` y estado de `#12`â€“`#19` + `#37` | Inventario de precondiciones | Dependencias crÃ­ticas quedan listadas y clasificadas | `final_gate` |
| `I20-S2` | Definir checklist de bloqueo/desbloqueo para entrada a codificaciÃ³n | `Codex` | `I20-S1` | Checklist de readiness | El gate de entrada es explÃ­cito y verificable | `final_gate` |
| `I20-S3` | Definir evidencia mÃ­nima exigida (documental y trazabilidad) | `Codex` | `I20-S2` | Reglas de evidencia | Queda claro quÃ© evidencia se exige para habilitar cÃ³digo | `final_gate` |
| `I20-S4` | Definir flujo de validaciÃ³n final (Codex prepara, Kiko valida) y criterio de cierre | `Codex+Kiko` | `I20-S3` | Protocolo de validaciÃ³n final | El cierre de `#20` queda operable y sin ambigÃ¼edades | `final_gate` |

#### Riesgos y bloqueos

- Riesgo de cerrar `#20` demasiado pronto y convertirlo en gate vacÃ­o.
- Riesgo de duplicar detalle de `#11` o reabrir decisiones de `#12`/`#18`/`#37`.

#### Criterio de cierre de la issue

- Gate operativo de entrada a codificaciÃ³n explÃ­cito, verificable y trazable,
  apoyado en evidencias de `#10` y derivadas.

#### Notas de secuencia / paralelizaciÃ³n

- No debe cerrarse antes de contar con insumos suficientes del resto de bloques.
- Es el Ãºltimo bloque tÃ©cnico de preparaciÃ³n antes de iniciar cÃ³digo.

## Riesgos transversales y reglas de ejecuciÃ³n

### Riesgos transversales

- **Solape entre checklist base y desglose**: `#10` define macro; `#11` detalla.
- **Cierres fuera de secuencia tÃ©cnica**: riesgo de retrabajo si se ignoran
  dependencias de cierre.
- **Cierre prematuro de issues `draftable`**: se admite borrador, no cierre sin
  dependencias satisfechas.
- **ConfusiÃ³n entre orden tÃ©cnico y nÃºmero de issue**: el orden tÃ©cnico manda
  para `siguiente paso` cuando exista y sea aplicable.

### Reglas de ejecuciÃ³n (operativas)

1. Priorizar primero **unidad pendiente de cierre** (trabajo local/rama/PR/issue
   pendiente de cierre) antes de iniciar trabajo nuevo.
1. Si no existe unidad pendiente de cierre, priorizar PRs abiertas.
1. Usar el **orden tÃ©cnico recomendado** del documento mÃ¡s especÃ­fico disponible
   para elegir el siguiente trabajo cuando no haya unidad pendiente de cierre
   ni PRs abiertas.
1. Si el siguiente item tÃ©cnico no es cerrable, saltar al siguiente cerrable.
1. Si no hay cerrables, avanzar en el primer `draftable`.
1. Si no existe orden tÃ©cnico aplicable, usar la issue abierta con nÃºmero mÃ¡s
   bajo.
1. Mantener trazabilidad de estado (`ready`, `draftable`, `blocked`,
   `final_gate`) al revisar el plan.

## Seguimiento de bloques

### Estado de bloques (actualizado tras cerrar #13, #37, #12, #40, #18, #14, #15, #16, #17, #19 y #20)

- [x] `#11` Desglose en bloques ejecutables (este documento)
- [x] `#13` InicializaciÃ³n temporal detallada (`ready`)
- [x] `#37` PolÃ­tica de editabilidad manual y correcciones de dominio (`ready`)
- [x] `#12` Contrato Firestore por agregado (`draftable`)
- [x] `#40` Modelo de recursos por `Entry` (delta neto; `draftable`)
- [x] `#18` Timestamps y orden estable (`draftable`)
- [x] `#14` Flujo de sesiÃ³n activa y `auto-stop` (`draftable`)
- [x] `#15` ValidaciÃ³n y recÃ¡lculo de recursos (`draftable`)
- [x] `#16` Consultas mÃ­nimas para timeline/foco (`draftable`)
- [x] `#17` Matriz de edge cases (`draftable`)
- [x] `#19` Plan de pruebas de invariantes (`draftable`)
- [x] `#20` Gate de listo para codificar (`final_gate`)

### Seguimiento de implementaciÃ³n (post-`#20`)

- [x] `#51` Bootstrap de app Flet y estructura base
- [x] `#52` Shell de pantalla principal (layout base Figma)
- [x] `#53` Estado local de navegaciÃ³n/visor sticky/activo mock
- [x] `#54` IntegraciÃ³n read-only inicial (`Q1/Q2/Q3/Q4/Q6/Q7`)
- [x] `#86` SelecciÃ³n temporal y feedback semanal en UI (solo tiles + feedback)
- [x] `#90` SimplificaciÃ³n de complejidad accidental en `app_root`/`main_shell_view`/placeholders
- [x] `#92` Refactor declarativo completo (MVU) de Main Shell en estructura feature-first (pre-U3)
- [x] RecuperaciÃ³n funcional pre-`#94` sobre MVS declarativo (Q1..Q8 + writes)

### PrÃ³xima secuencia tÃ©cnica esperada (segÃºn orden actual)

1. `U4-mobile-robustness-min` Mejorar robustez mÃ³vil mÃ­nima (`portrait` + `landscape`) en barra temporal y panel central
1. `U5-read-write-vertical-slice` Cerrar vertical read/write MVP de una operaciÃ³n completa con refresco visible

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

