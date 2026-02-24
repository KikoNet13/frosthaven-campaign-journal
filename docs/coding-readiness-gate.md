# Gate de Listo para Codificar (Fase 1 MVP)

## Metadatos

- `doc_id`: DOC-CODING-READINESS-GATE
- `purpose`: Definir y aplicar el gate final de entrada a implementacion para el MVP, con criterios bloqueantes, diferidos aceptados y evidencia trazable.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar un gate operativo y trazable de entrada a implementacion que permita
empezar codigo sin contradicciones documentales, reutilizando los contratos y
planes cerrados en `#10`-`#19` y dejando explicitos bloqueantes, diferidos
aceptados y recomendacion de primer slice de codigo.

## Alcance y no alcance

Incluye:

- definicion del resultado del gate en 3 estados (`apto`,
  `apto_con_diferidos_aceptados`, `no_apto`);
- inventario de precondiciones y dependencias criticas;
- checklist de bloqueo/desbloqueo;
- evidencia minima exigida para habilitar codigo;
- registro de diferidos aceptados (incluyendo concurrencia multi-device real);
- flujo de validacion final (Codex prepara, Kiko valida);
- aplicacion del gate al estado actual del repo/documentacion;
- recomendacion de primer slice de codigo (infraestructura/base app).

No incluye:

- implementacion de codigo de la app;
- ejecucion real del plan de pruebas `#19`;
- reapertura de decisiones de dominio/arquitectura cerradas;
- plan detallado de slices posteriores al primero.

## Entradas y prerrequisitos

- `AGENTS.md`
- `docs/context-governance.md`
- `docs/context-checklists.md` (`CHK-GATE-CODE`)
- `docs/decision-log.md`
- `docs/system-map.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `docs/domain-invariant-test-plan.md` (Issue `#19`)
- `docs/concurrency-sync-edge-case-matrix.md` (Issue `#17`)
- `docs/firestore-operation-contract.md` (Issue `#12`)
- `docs/active-session-flow.md` (Issue `#14`)
- `docs/resource-validation-recalculation.md` (Issue `#15`)
- `docs/minimal-read-queries.md` (Issue `#16`)
- `docs/timestamp-order-policy.md` (Issue `#18`)

## Definiciones de resultado del gate (3 estados)

### Tabla 1 - Resultados del gate (`I20-S0`)

| `gate_result` | `definicion` | `bloquea_inicio_codigo` | `requiere_diferidos_explicitos` | `requiere_follow_up_issues` | `notas` |
| --- | --- | --- | --- | --- | --- |
| `apto` | Todos los criterios bloqueantes cumplen y no quedan diferidos aceptados relevantes. | No | No | No (salvo mejoras no bloqueantes) | Estado ideal de readiness completo. |
| `apto_con_diferidos_aceptados` | Todos los criterios bloqueantes cumplen, pero existen diferidos explicitos aceptados. | No | Si | Opcional/segun diferidos | Permite iniciar codigo con deuda visible y controlada. |
| `no_apto` | Falla al menos un criterio bloqueante o falta evidencia critica del gate. | Si | N/A | Si (o accion correctiva documentada) | No se habilita codigo hasta corregir bloqueos. |

## Inventario de precondiciones y dependencias criticas

### Tabla 2 - Precondiciones y dependencias criticas (`I20-S1`)

| `precondition_id` | `categoria` | `descripcion` | `fuente_oficial` | `estado_actual` | `bloqueante` | `metodo_de_verificacion` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `PC-ISSUES-01` | `issues_base` | Issues de preparacion tecnica cerradas: `#10`, `#11`, `#12`, `#13`, `#14`, `#15`, `#16`, `#17`, `#18`, `#19`, `#37`, `#40` | GitHub Issues + checklist/blocks | `cumple` | Si | `gh issue view` por numero + tracking en docs | `#20` es la unica issue restante del backlog de preparacion. |
| `PC-TRACK-01` | `trazabilidad` | Tracking de readiness actualizado y consistente en checklist tecnico y blocks | `docs/mvp-implementation-checklist.md`, `docs/mvp-implementation-blocks.md` | `cumple` | Si | Revision documental cruzada | `#19` ya marcado y `#20` pendiente antes de este cierre. |
| `PC-DECISIONS-01` | `dominio` | Decisiones criticas de sincronizacion/conflictos/temporal/flujo/lecturas/recursos cerradas y oficiales | `docs/decision-log.md` + docs de contrato | `cumple` | Si | Revision de fuentes oficiales y `DEC-*` | Base documental consolidada hasta `DEC-0031`. |
| `PC-GATE-QUALITY-01` | `calidad` | Gate de calidad declarado y vigente (bloquea implementacion si faltan condiciones) | `AGENTS.md`, `docs/context-governance.md` | `cumple` | Si | Revision de reglas oficiales | Se alinea en `#20` con resultado en 3 estados sin perder rigor. |
| `PC-DOUBLE-VERIFY-01` | `verificacion` | Evidencia de verificacion doble y uso de checklists operativas | `docs/context-checklists.md`, `docs/context-governance.md` | `parcial_a_actualizar_en_#20` | Si | Verificacion de registro final del gate | Se completa en esta misma unidad al registrar gate final. |
| `PC-TESTPLAN-01` | `pruebas` | `#19` define `P0` bloqueantes en el plan y diferidos multi-device explicitos | `docs/domain-invariant-test-plan.md` | `cumple` | Si | Revision de `INV/TC/EC`, `P0`, `defer_multi_device` | `#20` consume este insumo, no exige ejecucion real. |
| `PC-CONTRADICTION-01` | `consistencia` | No hay contradicciones oficiales conocidas que impidan iniciar codigo | Fuentes oficiales (`AGENTS.md`, `docs/`) | `cumple_con_transicion_#20` | Si | Revision documental final | `AGENTS.md` debe actualizarse en `#20` para quitar contradiccion de Fase 0/no codigo. |
| `PC-REPO-STATE-01` | `operativo` | Sin PRs abiertas ni unidad pendiente de cierre previa a `#20` | Git/GitHub | `cumple` | No | `git status`, `gh pr list` | Condicion operativa para ejecutar el gate, no de producto. |

## Checklist de bloqueo/desbloqueo

### Tabla 3 - Checklist de bloqueo/desbloqueo (`I20-S2`)

| `gate_check_id` | `criterio` | `fuentes` | `tipo` | `resultado_actual` | `impacto_si_falla` | `accion_requerida` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `GC-01` | Prerrequisitos tecnicos y decisiones criticas cerrados (`#10`-`#19`, `#37`, `#40`) | GitHub Issues, checklist, blocks | `bloqueante` | `pass` | No se puede declarar readiness | Cerrar issue(s) faltantes o documentar bloqueo real | Confirmado al aplicar el gate. |
| `GC-02` | `#19` cubre `P0` de `#17` con trazabilidad y diferencia diferidos aceptados | `docs/domain-invariant-test-plan.md`, `docs/concurrency-sync-edge-case-matrix.md` | `bloqueante` | `pass` | Gate sin base de pruebas bloqueantes | Completar `#19` o corregir trazabilidad | `P0` definidos en plan, no ejecutados. |
| `GC-03` | Tracking oficial consistente (`system-map`, checklist, blocks, decision-log`) | `docs/` + `AGENTS.md` | `bloqueante` | `pass` | Riesgo de contradiccion operativa | Actualizar fuentes y referencias cruzadas | Se completa en esta unidad. |
| `GC-04` | `AGENTS.md` y `context-governance` permiten inicio de codigo tras gate | `AGENTS.md`, `docs/context-governance.md` | `bloqueante` | `pass` | Contradiccion oficial al empezar codigo | Aplicar transicion documental en `#20` | Cambio clave de esta issue. |
| `GC-05` | `CHK-GATE-CODE` ejecutable y alineado con 3 estados | `docs/context-checklists.md` | `bloqueante` | `pass` | Resultado del gate ambiguo | Actualizar checklist del gate | Se actualiza en `#20`. |
| `GC-06` | Diferidos aceptados explicitos (si existen) con riesgo/seguimiento | `docs/coding-readiness-gate.md`, `docs/domain-invariant-test-plan.md` | `bloqueante` | `pass` | Se oculta deuda critica | Registrar diferidos formalmente | Incluye multi-device real. |
| `GC-07` | Recomendacion de primer slice de codigo documentada | `docs/coding-readiness-gate.md` | `no_bloqueante` | `pass` | Inicio de codigo con mayor friccion | Incluir slice recomendado | Decidido por Kiko como salida deseada. |

## Evidencia minima exigida para habilitar codigo

### Tabla 4 - Evidencia minima exigida (`I20-S3`)

| `evidence_id` | `evidencia` | `obligatoria_para_gate` | `fuente_o_ubicacion` | `forma_de_validacion` | `notas` |
| --- | --- | --- | --- | --- | --- |
| `EV-01` | Estado de issues/PRs y cierre de backlog de preparacion (`#10`-`#19`, `#37`, `#40`) | Si | GitHub Issues/PRs + docs de tracking | Consulta a GitHub + trazabilidad documental | `#20` se evalua con el resto cerrado. |
| `EV-02` | Tracking oficial coherente (`checklist`, `blocks`, `system-map`, `decision-log`) | Si | `docs/` + `AGENTS.md` | Revision cruzada | Debe incluir actualizacion de `#20`. |
| `EV-03` | Evidencia de `#19`: `P0` definidos/trazados y diferidos explicitos | Si | `docs/domain-invariant-test-plan.md` | Revision de tablas `INV/TC/EC` + prioridades | No exige ejecucion real. |
| `EV-04` | Resultado de `CHK-GATE-CODE` alineado con 3 estados | Si | `docs/context-checklists.md` + `docs/coding-readiness-gate.md` | Validacion de checklist y resultado aplicado | Puede resultar `apto`, `apto_con_diferidos_aceptados` o `no_apto`. |
| `EV-05` | Registro de validacion final y estado de fase actualizado | Si | `docs/context-governance.md` | Revision de hito/evidencia + estado de fase | Debe reflejar habilitacion si gate no es `no_apto`. |
| `EV-06` | Lista de diferidos aceptados (si gate no es `apto`) | Condicional | `docs/coding-readiness-gate.md` | Revisar Tabla 5 | Obligatoria cuando el resultado es `apto_con_diferidos_aceptados`. |

## Diferidos aceptados y criterio de aceptacion

### Regla de aceptacion de diferidos

Un diferido solo se considera aceptado si tiene:

- descripcion concreta;
- riesgo explicitado;
- impacto en el gate;
- condicion de salida;
- seguimiento posterior identificable.

Diferidos implicitos o solo anotados en texto libre sin estructura se tratan como
bloqueo (`no_apto`).

### Tabla 5 - Diferidos aceptados (`I20-S3/I20-S4`)

| `deferred_id` | `descripcion` | `origen` | `riesgo` | `aceptado_por` | `impacto_en_gate` | `condicion_de_salida` | `seguimiento_posterior` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `DEF-001` | Ejecucion real de casos de concurrencia multi-device (pruebas manuales/observables) | `#19` (`defer_multi_device`) | Puede ocultar diferencias de comportamiento en escenarios concurrentes reales antes de tener cobertura empirica | Kiko (aceptacion explicita en plan de `#19/#20`) | Permite `apto_con_diferidos_aceptados`, no `apto` | Definir y ejecutar cobertura multi-device en fase de implementacion/QA posterior | Nuevo issue o bloque de pruebas posterior (derivado de `#19/#20` si hace falta) | `#19` ya exige que el diferido quede visible y trazado. |

## Flujo de validacion final (Codex/Kiko)

1. Codex inventaria precondiciones y evidencias del gate.
1. Codex clasifica checks bloqueantes/no bloqueantes y aplica `CHK-GATE-CODE`.
1. Codex propone resultado del gate (`apto`, `apto_con_diferidos_aceptados`, `no_apto`) con justificacion.
1. Kiko valida el resultado y, si aplica, acepta diferidos explicitamente.
1. Codex registra evidencia en `docs/context-governance.md` y actualiza tracking/documentacion oficial.
1. Si el resultado no es `no_apto`, se habilita inicio de codigo y se deja recomendacion de primer slice.

## Resultado del gate aplicado al estado actual

### Resultado propuesto/aplicado

El resultado aplicado al estado actual del repo es:

- **`apto_con_diferidos_aceptados`**

### Justificacion resumida

- backlog documental de preparacion (`#10`-`#19`, `#37`, `#40`) cerrado;
- contratos/flujo/lecturas/edge cases/test plan oficiales y trazables;
- `#19` define `P0` bloqueantes en el plan y marca diferidos multi-device de
  forma explicita;
- no se requiere ejecucion real pre-codigo para el gate;
- queda un diferido aceptado visible (`DEF-001`) que impide usar el estado
  `apto` puro.

### Tabla 6 - Resultado aplicado + recomendacion de primer slice (`I20-S4`)

| `campo` | `valor` | `justificacion` | `fuente` | `notas` |
| --- | --- | --- | --- | --- |
| `gate_result_final` | `apto_con_diferidos_aceptados` | Todos los bloqueantes cumplen; existe diferido multi-device aceptado | Este documento + `#19` | Estado esperado por defecto confirmado. |
| `fecha_validacion` | `2026-02-24` | Fecha de cierre documental del gate | `#20`, PR/merge | Fecha de referencia del gate. |
| `bloqueantes_abiertos` | `ninguno` | Checks bloqueantes `GC-01..GC-06` en `pass` | Tabla 3 | Si aparece alguno en `fail`, el resultado debe pasar a `no_apto`. |
| `diferidos_aceptados` | `DEF-001` | Concurrencia multi-device real diferida y visible | Tabla 5 + `#19` | Diferido no oculto, con seguimiento. |
| `habilitacion_codigo` | `si` | El resultado del gate no bloquea inicio de codigo | Tabla 1 (`apto_con_diferidos_aceptados`) | Habilitacion condicionada a respetar trazabilidad vigente. |
| `primer_slice_recomendado` | `infraestructura/base app` | Reduce friccion de arranque sin reabrir contratos de dominio | Decision de `#20` | Recomendacion, no bloqueo. |
| `motivo_slice` | `establecer shell de app, layout base y wiring minimo antes de mutaciones complejas` | Permite comenzar implementacion con bajo riesgo contractual | `#14`, `#16`, Figma/layout canónico | Alineado con lectura/flujo ya definidos. |
| `riesgos_inmediatos` | `deuda multi-device real; riesgo de drift entre docs y codigo si no se mantiene tracking` | Riesgos aceptados/observables al iniciar codigo | Tabla 5 + `AGENTS.md` | Mantener `siguiente paso` y trazabilidad de issues. |

## Recomendacion de primer slice de codigo (infraestructura/base app)

### Alcance minimo recomendado

- crear estructura inicial del proyecto app (framework, modulos base, entrypoint);
- montar shell de pantalla principal con layout base (superficies principales
  segun Figma + `#16`);
- wiring de estado minimo de seleccion (`selected_year`, `selected_week`,
  `selected_entry`) sin mutaciones de dominio complejas;
- capa de lectura inicial stub o conectada minimamente para probar flujo de
  pantalla (sin cerrar operaciones de escritura);
- mantener trazabilidad de decisiones en docs/issue del slice.

### Criterio de finalizacion del slice recomendado

- la app arranca localmente;
- el shell/layout base renderiza;
- existe estado basico de navegacion/seleccion;
- no se contradicen contratos documentales de `#12/#14/#16/#18`.

## Casos de aceptacion / verificacion documental

1. El gate define y usa 3 estados (`apto`, `apto_con_diferidos_aceptados`,
   `no_apto`).
1. El resultado aplicado al estado actual es trazable y justificado.
1. Los diferidos aceptados se registran estructuradamente (Tabla 5).
1. `#19` se usa como insumo de P0 y diferidos, sin exigir ejecucion real.
1. `AGENTS.md` y `docs/context-governance.md` quedan alineados con inicio de
   codigo tras el gate.
1. `CHK-GATE-CODE` queda alineado con el modelo de 3 estados.
1. El documento deja recomendacion explicita de primer slice (infraestructura/base app).

## Riesgos, limites y decisiones diferidas

- El gate no sustituye validaciones tecnicas de implementacion; solo habilita el
  inicio de codigo con contratos y planes ya cerrados.
- El estado `apto_con_diferidos_aceptados` requiere disciplina de seguimiento
  para evitar que los diferidos queden permanentes.
- La recomendacion del primer slice es orientativa; el siguiente trabajo puede
  ajustarla si mantiene coherencia con contratos y trazabilidad.
- Si durante la implementacion aparecen contradicciones documentales nuevas, se
  debe abrir issue correctiva y registrar decision antes de escalar el impacto.

## Referencias

- `AGENTS.md`
- `docs/context-governance.md`
- `docs/context-checklists.md`
- `docs/system-map.md`
- `docs/decision-log.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `docs/domain-invariant-test-plan.md`
- `docs/concurrency-sync-edge-case-matrix.md`
- `docs/firestore-operation-contract.md`
- `docs/active-session-flow.md`
- `docs/resource-validation-recalculation.md`
- `docs/minimal-read-queries.md`
- `docs/timestamp-order-policy.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`
