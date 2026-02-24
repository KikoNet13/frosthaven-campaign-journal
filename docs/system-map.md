# Mapa del Sistema

## Metadatos

- `doc_id`: DOC-SYSTEM-MAP
- `purpose`: Mapa navegable de la documentación oficial y legado temporal.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

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
- `docs/domain-glossary.md`
  - Contrato de modelo de dominio e invariantes.
- `docs/sync-strategy.md`
  - Estrategia de sincronización multidispositivo del MVP.
- `docs/conflict-policy.md`
  - Política de conflictos concurrentes del MVP.
- `docs/firestore-operation-contract.md`
  - Contrato de operaciones de escritura por agregado del MVP.
- `docs/resource-delta-model.md`
  - Modelo de recursos del MVP por `Entry` (`resource_deltas`, delta neto).
- `docs/resource-validation-recalculation.md`
  - Reglas de validación y recálculo de `resource_deltas`/totales globales.
- `docs/timestamp-order-policy.md`
  - Política de timestamps de auditoría y orden estable entre dispositivos.
- `docs/active-session-flow.md`
  - Flujo de sesión activa (`start/stop/auto-stop`) y separación foco/activo.
- `docs/minimal-read-queries.md`
  - Consultas mínimas para pantalla principal (superficies, triggers, orden y
    límites de carga) del MVP.
- `docs/concurrency-sync-edge-case-matrix.md`
  - Matriz de edge cases de concurrencia/sincronización y subset crítico para
    verificación del MVP.
- `docs/campaign-temporal-controls.md`
  - Controles temporales de campaña y provisión/extensión de años del MVP.
- `docs/campaign-temporal-initialization.md`
  - Estrategia técnica de inicialización/extensión de años y creación de
    `year/season/week` del MVP.
- `docs/editability-policy.md`
  - Política de editabilidad manual y correcciones de estado/sesiones del MVP.
- `docs/mvp-implementation-checklist.md`
  - Checklist técnico base para preparar la implementación del MVP.
- `docs/mvp-implementation-blocks.md`
  - Desglose operativo de bloques y subbloques ejecutables del MVP.
- `docs/context-checklists.md`
  - Checklists por trigger de trabajo.
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
- Modelo de dominio -> `docs/domain-glossary.md`
- Sincronización MVP -> `docs/sync-strategy.md`
- Conflictos concurrentes MVP -> `docs/conflict-policy.md`
- Contrato Firestore por agregado -> `docs/firestore-operation-contract.md`
- Modelo de recursos por `Entry` -> `docs/resource-delta-model.md`
- Validación y recálculo de recursos -> `docs/resource-validation-recalculation.md`
- Timestamps y orden estable -> `docs/timestamp-order-policy.md`
- Flujo de sesión activa y `auto-stop` -> `docs/active-session-flow.md`
- Consultas mínimas de pantalla principal -> `docs/minimal-read-queries.md`
- Edge cases de concurrencia/sincronización -> `docs/concurrency-sync-edge-case-matrix.md`
- Controles temporales de campaña -> `docs/campaign-temporal-controls.md`
- Inicialización temporal técnica -> `docs/campaign-temporal-initialization.md`
- Editabilidad manual MVP -> `docs/editability-policy.md`
- Checklist técnico MVP -> `docs/mvp-implementation-checklist.md`
- Bloques de implementación MVP -> `docs/mvp-implementation-blocks.md`
- Estado de fase -> `docs/context-governance.md`
- Pasos operativos -> `docs/context-checklists.md`
- Material reutilizable -> `learning/handbook.md`
