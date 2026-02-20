# AGENTS

## Metadatos

- `doc_id`: AGENTS
- `purpose`: Contrato operativo de trabajo entre IA y humano.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-06

## Propósito

Este archivo define cómo se trabaja en este repositorio durante la Fase 0.
La prioridad es aprender ingeniería de contexto con un flujo profesional y
sencillo.

## Alcance de la fase

- Diseñar y mantener el sistema documental de contexto.
- Preparar la organización de Git y GitHub.
- Evitar implementación de código de aplicación.

## Reglas no negociables

- No crear código funcional de la app durante Fase 0.
- No cerrar decisiones de runtime de producto en esta fase.
- La documentación oficial vive en `AGENTS.md`, `docs/` y `learning/`.
- `summary_initial_conversation.txt`, `tdd.md`, `important.txt` y `neil.txt`
  son legado temporal.
- Si hay conflicto entre legado y oficial, prevalece lo oficial.
- Descripciones en castellano.
- Identificadores técnicos en inglés cuando aplique.
- Mantenimiento manual con checklist.
- La IA actualiza y Kiko valida.
- Cadencia de actualización por hito.
- Verificación doble obligatoria en cada cierre de hito.
- Gate estricto antes de pasar a código.

## Flujo operativo

### Inicio de sesión

1. Leer `AGENTS.md`.
1. Leer `docs/system-map.md`.
1. Confirmar objetivo y alcance.

### Durante la sesión

1. Registrar decisiones en `docs/decision-log.md`.
1. Ejecutar checklists de `docs/context-checklists.md`.
1. Mantener trazabilidad de conflictos y precedencia.

### Cierre de hito

1. Actualizar documentos oficiales.
1. Ejecutar verificación de estructura.
1. Ejecutar verificación de criterios y edge cases.
1. Registrar evidencia en `docs/context-governance.md`.

## Gate de calidad

Se bloquea el paso a implementación si se cumple al menos una condición:

- Falta una decisión crítica.
- Hay conflicto legado/oficial sin registrar.
- La checklist del hito está incompleta.
- No hay evidencia de verificación doble.

## Cierre de conversación

Cada interacción termina con un menú numerado fijo de 3 a 5 siguientes pasos.

## Fuentes oficiales del repo

- Mapa del sistema: `docs/system-map.md`
- Gobierno de contexto: `docs/context-governance.md`
- Registro de decisiones: `docs/decision-log.md`
- Checklists operativas: `docs/context-checklists.md`
- Guía reusable: `learning/handbook.md`
- Anexo Frosthaven: `learning/frosthaven-annex.md`
- Bibliografía anotada: `learning/sources.md`
- Flujo Git y GitHub: `docs/repo-workflow.md`
- Guía didáctica de flujo Git: `learning/git-workflow-handbook.md`

## Nota de legado

El legado temporal se mantiene hasta completar dos hitos verificados con éxito.
