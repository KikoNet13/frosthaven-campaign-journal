# Mapa del Sistema

## Metadatos

- `doc_id`: DOC-SYSTEM-MAP
- `purpose`: Mapa navegable de la documentación oficial y su trazabilidad.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-01
- `next_review`: 2026-03-15

## Objetivo

Este documento permite entender rápidamente:

- Dónde están las reglas activas.
- Dónde se registran decisiones.
- Qué documentos son canónicos en implementación.

## Documentación oficial

- `AGENTS.md`
  - Contrato operativo.
- `docs/context-governance.md`
  - Estado de fase y evidencia de hitos.
- `docs/decision-log.md`
  - Registro de decisiones y trazabilidad.
- `docs/context-checklists.md`
  - Checklists por trigger.
- `docs/repo-workflow.md`
  - Flujo Git/GitHub del repo.
- `docs/domain-glossary.md`
  - Contrato de modelo de dominio e invariantes.
- `docs/sync-strategy.md`
  - Estrategia de sincronización MVP.
- `docs/conflict-policy.md`
  - Política de conflictos concurrentes MVP.
- `docs/firestore-operation-contract.md`
  - Contrato de escrituras por agregado.
- `docs/resource-delta-model.md`
  - Modelo de recursos por `Entry`.
- `docs/resource-validation-recalculation.md`
  - Reglas de validación y recálculo de recursos.
- `docs/timestamp-order-policy.md`
  - Política de timestamps y orden estable.
- `docs/active-session-flow.md`
  - Flujo de sesión activa y `auto-stop`.
- `docs/minimal-read-queries.md`
  - Consultas mínimas de pantalla principal.
- `docs/concurrency-sync-edge-case-matrix.md`
  - Matriz de edge cases de concurrencia/sincronización.
- `docs/domain-invariant-test-plan.md`
  - Plan de pruebas por invariantes.
- `docs/coding-readiness-gate.md`
  - Gate de listo para codificar.
- `docs/campaign-temporal-controls.md`
  - Controles temporales de campaña.
- `docs/campaign-temporal-initialization.md`
  - Inicialización/expansión temporal técnica.
- `docs/editability-policy.md`
  - Política de editabilidad manual MVP.
- `docs/mvp-implementation-checklist.md`
  - Checklist técnico de implementación.
- `docs/mvp-implementation-blocks.md`
  - Bloques ejecutables de implementación.
- `learning/handbook.md`
  - Guía reusable de ingeniería de contexto.
- `learning/frosthaven-annex.md`
  - Anexo aplicado al proyecto.
- `learning/git-workflow-handbook.md`
  - Guía didáctica de flujo Git.
- `learning/sources.md`
  - Bibliografía anotada.

## Estado de legacy

- Los archivos legacy de arranque (`summary_initial_conversation.txt`,
  `tdd.md`, `important.txt`, `neil.txt`) fueron retirados del árbol activo el
  `2026-03-01`.
- Su contexto histórico permanece trazado en `docs/decision-log.md`.

## Regla de precedencia

- Si hay conflicto, prevalece documentación oficial.
- Todo conflicto debe registrarse en `docs/decision-log.md`.

## Navegación rápida

- Regla activa -> `AGENTS.md`
- Decisión tomada -> `docs/decision-log.md`
- Estado de fase -> `docs/context-governance.md`
- Pasos operativos -> `docs/context-checklists.md`
- Flujo Git/GitHub -> `docs/repo-workflow.md`
