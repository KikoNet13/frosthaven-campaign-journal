# Flujo de Repositorio

## Metadatos

- `doc_id`: DOC-REPO-WORKFLOW
- `purpose`: Definir el flujo Git y GitHub adoptado.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-06

## Objetivo

Aplicar un flujo profesional, simple y mantenible para un solo desarrollador.

## Modelo adoptado

- GitHub Flow minimalista.
- Rama principal: `main`.
- Fuente principal de tareas: GitHub Issues.

## Reglas de ramas

- Para trabajo no trivial:
  - crear Issue
  - crear rama desde `main`
  - nomenclatura `tipo/<issue-id>-slug`
- Para trabajo trivial:
  - se permite commit y push directo a `main`

## Reglas de commits

- Formato: `type(scope): resumen en español`.
- Tipos válidos:
  - `feat`
  - `fix`
  - `docs`
  - `chore`
  - `refactor`
  - `test`
  - `hotfix`

## Reglas de PR

- PR obligatoria cuando el cambio sea relevante.
- Debe incluir:
  - referencia al Issue
  - resumen de alcance
  - checklist de calidad completada

## Definición de cambio trivial

- typo o formato local
- ajuste menor en una zona
- sin impacto en flujo ni estructura

## Definición de cambio relevante

- cambia convenciones
- cambia estructura de documentación
- afecta más de un archivo crítico
- introduce decisiones de proceso

## Versionado y releases

- Convención SemVer temprana: `v0.x.y`.
- En cada hito cerrado:
  - actualizar `CHANGELOG.md`
  - crear tag
  - publicar release notes

## Cadencia recomendada

1. Abrir Issue.
1. Ejecutar trabajo en rama.
1. Hacer N commits pequeños.
1. Abrir PR si aplica.
1. Cerrar Issue.
1. Actualizar changelog.
