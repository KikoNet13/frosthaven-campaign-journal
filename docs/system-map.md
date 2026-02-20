# Mapa del Sistema

## Metadatos

- `doc_id`: DOC-SYSTEM-MAP
- `purpose`: Mapa navegable de la documentación oficial y legado temporal.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-06

## Objetivo

Este documento permite que una persona o agente nuevo entienda rápidamente:

- Dónde están las reglas activas.
- Dónde se registran decisiones.
- Qué documentos son legado y cómo se usan.

## Documentación oficial

- `AGENTS.md`
  - Contrato operativo.
  - Reglas activas y gate de calidad.
- `docs/context-governance.md`
  - Estado de fase.
  - Evidencias de verificación.
- `docs/decision-log.md`
  - Decisiones aceptadas y trazabilidad.
- `docs/context-checklists.md`
  - Checklists por trigger de trabajo.
- `docs/domain-glossary.md`
  - Definiciones de dominio, invariantes y casos borde.
- `docs/repo-workflow.md`
  - Flujo GitHub Flow minimalista para este proyecto.
- `learning/handbook.md`
  - Principios transferibles de ingeniería de contexto.
- `learning/frosthaven-annex.md`
  - Casos aplicados al proyecto.
- `learning/git-workflow-handbook.md`
  - Guía didáctica para aprender el flujo Git.
- `learning/sources.md`
  - Bibliografía anotada.

## Legado temporal

- `summary_initial_conversation.txt`
  - Prompt inicial y alcance preliminar.
- `tdd.md`
  - Borrador inicial de producto.
- `important.txt`
  - Objetivo explícito de aprendizaje de contexto.
- `neil.txt`
  - Resumen de prácticas observadas sobre trabajo con agentes.

## Trazabilidad legado a oficial

- `important.txt` -> `AGENTS.md`, `docs/decision-log.md`
- `neil.txt` -> `learning/handbook.md`, `docs/decision-log.md`
- `summary_initial_conversation.txt` -> `AGENTS.md`,
  `docs/context-checklists.md`
- `tdd.md` -> referencia de producto para Fase 1

## Regla de precedencia

- Si hay conflicto, prevalece documentación oficial.
- Todo conflicto debe registrarse en `docs/decision-log.md`.
- El legado no se elimina durante Fase 0.

## Navegación rápida

- Regla activa -> `AGENTS.md`
- Decisión tomada -> `docs/decision-log.md`
- Estado de fase -> `docs/context-governance.md`
- Pasos operativos -> `docs/context-checklists.md`
- Material reutilizable -> `learning/handbook.md`
