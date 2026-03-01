# Gobierno de Contexto

## Metadatos

- `doc_id`: DOC-CONTEXT-GOVERNANCE
- `purpose`: Gobierno de contexto, gate de calidad y estado verificable.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-01
- `next_review`: 2026-03-12

## Alcance de Fase 0

- Institucionalizar un sistema de contexto agent-first.
- Separar operación (`docs/`) y aprendizaje (`learning/`).
- Migrar conocimiento útil desde legado a oficial.

## No alcance de Fase 0

- Código de aplicación.
- Cierre de decisiones de runtime de producto.
- Automatización CI adicional en esta fase.

## Modelo operativo

- Cadencia: por hito.
- Mantenimiento: manual con checklist.
- Ejecución: IA actualiza.
- Validación: Kiko valida.
- Precedencia: oficial sobre legado.

## Gate estricto

No se habilita implementación de código si falta alguna condición:

- Checklist de hito completa.
- Decisiones críticas cerradas para el siguiente paso.
- Trazabilidad de conflictos legado/oficial.
- Evidencia de verificación doble.

## Verificación doble

### Verificación A: estructura

Se valida presencia y formato de:

- `AGENTS.md`
- `docs/system-map.md`
- `docs/context-governance.md`
- `docs/decision-log.md`
- `docs/context-checklists.md`
- `docs/repo-workflow.md`
- `learning/handbook.md`
- `learning/frosthaven-annex.md`
- `learning/git-workflow-handbook.md`
- `learning/sources.md`

### Verificación B: criterios y edge cases

Se valida:

- Regla de precedencia.
- Política de idioma e identificadores.
- Gate estricto declarado.
- Cierre con menú numerado.
- Evidencia de decisiones y fuentes.

## Registro de hitos y evidencia

### Hito H0-01

- Fecha: 2026-02-20
- Objetivo: crear estructura oficial de contexto.
- Resultado: aprobado
- Verificación A: aprobado
- Verificación B: aprobado
- Evidencia: alta de `AGENTS.md`, `docs/` y `learning/`.

### Hito H0-02

- Fecha: 2026-02-20
- Objetivo: migrar reglas activas desde legado.
- Resultado: aprobado
- Verificación A: aprobado
- Verificación B: aprobado
- Evidencia: decisiones y checklists registradas.

### Hito H0-03

- Fecha: 2026-02-24
- Objetivo: ejecutar y registrar gate final de listo para codificar (Issue #20).
- Resultado: aprobado con diferidos aceptados
- Verificación A: aprobado
- Verificación B: aprobado
- Evidencia:
  - `docs/coding-readiness-gate.md` (resultado `apto_con_diferidos_aceptados`)
  - `docs/domain-invariant-test-plan.md` (`#19`, `P0` definidos y trazados)
  - `docs/context-checklists.md` (`CHK-GATE-CODE` actualizado)
  - `AGENTS.md` y `docs/system-map.md` alineados con transición a implementación.

### Hito H1-01

- Fecha: 2026-02-26
- Objetivo: ejecutar P0 single-device del plan de invariantes (`#70`) y registrar evidencia trazable.
- Resultado: completado con bloqueos y diferidos
- Verificación A: aprobado (registro de evidencia en issue + follow-ups)
- Verificación B: aprobado (clasificación completa `pass/fail/blocked/deferred`)
- Evidencia:
  - Issue `#70` (matriz P0, resultados por lotes y resumen de cierre operativo)
  - Follow-up `#75` (`TC-ENTRY-02` fail: `Entry.delete` activa no elimina tras confirmar)
  - Follow-up `#76` (bloqueo de observabilidad temporal UI para `week_cursor`)
  - PR de la unidad `#70` (resumen y cierre end-to-end)
- Resumen:
  - `pass`: 4 (`TC-SESSION-04`, `TC-READ-04`, `TC-SESSION-02`, `TC-RESOURCE-04`)
  - `fail`: 1 (`TC-ENTRY-02`)
  - `blocked`: 2 (`TC-TEMPORAL-01`, `TC-TEMPORAL-02`)
  - `deferred`: 1 (`TC-SESSION-01`)
  - Alcance aplicado: P0 estricto de `#19`; `EC-TEMPORAL-01` (`#17`) queda fuera de `#70` por trazabilidad de prioridades (`TC-TEMPORAL-04`, `P1` en `#19`).

### Hito H1-02

- Fecha: 2026-02-26
- Objetivo: validar uso individual en dispositivo alterno (`DEF-001` reenfocado) con Charlotte y viewports equivalentes (`#71`).
- Resultado: completado con gap de usabilidad móvil y un bloqueo opcional de harness
- Verificación A: aprobado (ejecución y evidencia registradas en issue `#71`)
- Verificación B: aprobado (todos los escenarios `S1..S7` clasificados)
- Evidencia:
  - Issue `#71` (matriz de escenarios, resultados por lotes y resumen operativo)
  - Follow-up `#79` (barra temporal superior no usable en viewport móvil)
  - PR de la unidad `#71` (resumen y cierre end-to-end)
- Resumen:
  - `pass`: 5 (`S1`, `S2`, `S3`, `S4`, `S5`)
  - `fail`: 1 (`S7`, robustez visual móvil)
  - `blocked`: 1 (`S6`, opcional por limitación de harness/alcance del run)
  - Alcance aplicado: validación de uso individual con alternancia en dos tabs y `Refresh`, sin claims multi-writer concurrente real.
  - Reencuadre explícito: `DEF-001` se ejecuta como viewport equivalente (`desktop` + `mobile/tablet`) en vez de dispositivo físico en esta unidad.

### Hito H1-03

- Fecha: 2026-02-26
- Objetivo: reencuadrar el modelo temporal del MVP a “semana actual derivada no persistida” (`#76`) y dejar trazabilidad de transición.
- Resultado: completado (decisión+docs+trazabilidad) con migración técnica diferida
- Verificación A: aprobado (issue `#76` reencuadrada + comentario histórico en `#70`)
- Verificación B: aprobado (docs núcleo alineados y issue técnica de migración creada)
- Evidencia:
  - Issue `#76` (reencuadre de discrepancia de modelo temporal)
  - Issue `#81` (migración técnica de implementación para retirar dependencia de `campaign.week_cursor`)
  - Comentario en `#70` (reinterpretación/superseded del bloqueo temporal)
  - PR de la unidad `#76` (decisión+docs)
- Resumen:
  - Canon documental actualizado: la “semana actual” pasa a definirse como concepto derivado (primera `Week` abierta) y no como campo persistido canónico.
  - Se acepta divergencia transitoria: el código actual sigue usando `campaign.week_cursor` hasta ejecutar `#81`.
  - `#76` se cierra como unidad de decisión+docs; no incluye migración técnica ni revalidación de `TC-TEMPORAL-01/02`.

### Hito H1-04

- Fecha: 2026-02-26
- Objetivo: restaurar la usabilidad de la barra temporal superior en viewport móvil horizontal (`#79`) con bloques estacionales y overflow scrollable.
- Resultado: completado
- Verificación A: aprobado (validación Charlotte en `desktop` + `mobile landscape` registrada en issue `#79`)
- Verificación B: aprobado (weeks finales accesibles y selección funcional en móvil horizontal sin regresión visible en desktop)
- Evidencia:
  - Issue `#79` (hallazgo original + comentario de validación de cierre con Charlotte)
  - PR de la unidad `#79` (implementación UI y cierre end-to-end)
- Resumen:
  - Top bar responsive con compactación solo en modo móvil horizontal (`landscape`).
  - Weeks del año visible reestructuradas en 2 bloques visuales (verano/invierno) con scroll horizontal de overflow.
  - Desktop pequeño (`800x600`) preservado sin compactación accidental tras ajustar la heurística responsiva.
  - `portrait` queda fuera de alcance explícito de la unidad.



### Hito H1-05

- Fecha: 2026-02-26
- Objetivo: reorientar la ejecución a desarrollo acelerado de la app (UI + funcionalidades) con contexto ligero reutilizable.
- Resultado: aprobado
- Verificación A: aprobado (nueva guía reusable publicada y trazada en mapa del sistema)
- Verificación B: aprobado (decisión registrada y backlog de implementación actualizado con próximas issues)
- Evidencia:
  - `learning/personal-context-engineering-quickstart.md`
  - `docs/system-map.md`
  - `docs/decision-log.md` (DEC-0035)
  - `docs/mvp-implementation-checklist.md` (nuevas issues pendientes post-#20)
- Resumen:
  - Se adopta modo `development_first_light_context`.
  - La documentación pasa a criterio de soporte a implementación, no de protagonismo.
  - Se mantiene trazabilidad mínima profesional (issue/commit/PR) para cambios no triviales.


## Conocimiento migrado desde legado

- `important.txt`
  - Migrado: prioridad de aprendizaje de contexto.
  - Destino: `AGENTS.md`, `docs/decision-log.md` (DEC-0001).
- `neil.txt`
  - Migrado: rigor, primeros principios y edge cases.
  - Destino: `learning/handbook.md`, `docs/decision-log.md` (DEC-0007).
- `summary_initial_conversation.txt`
  - Migrado: restricciones de fase y trazabilidad.
  - Destino: `AGENTS.md`, `docs/context-checklists.md`.
- `tdd.md`
  - Migrado: contexto de producto para Fase 1.
  - Destino: decisión documental y trazabilidad histórica.

### Estado actual de legacy textual

- Los archivos legacy de arranque fueron retirados del repo activo el `2026-03-01`.
- Las referencias históricas permanecen únicamente en `docs/decision-log.md`.

## Decisiones de producto pospuestas a Fase 1

- Representación de tiempo.
- Estructura mínima de Firestore.
- Estrategia de sincronización (resuelta en Fase 1; ver DEC-0013 y
  `docs/sync-strategy.md`).

## Estado actual de fase

- Estado: development_first_light_context
- Criterio de aceptación de Fase 0: cubierto a nivel documental y gate `#20`
  validado.
- Siguiente paso: ejecutar la siguiente issue funcional prioritaria de UI/lecturas y completar el backlog corto de implementación.
