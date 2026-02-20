# Gobierno de Contexto

## Metadatos

- `doc_id`: DOC-CONTEXT-GOVERNANCE
- `purpose`: Gobierno de contexto, gate de calidad y estado verificable.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-06

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
  - Destino: referencia en `docs/system-map.md`.

## Decisiones de producto pospuestas a Fase 1

- Representación de tiempo.
- Estructura mínima de Firestore.
- Estrategia de sincronización.

## Estado actual de fase

- Estado: active
- Criterio de aceptación de Fase 0: cubierto a nivel documental.
- Siguiente paso: validación final de Kiko y transición a Fase 1.
