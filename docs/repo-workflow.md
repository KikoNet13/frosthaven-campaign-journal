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

## Flujo recomendado con Codex

1. Kiko pide objetivo o cambio.
1. Codex lo traduce a unidades ejecutables.
1. Si hay varias unidades, se crean Issues separadas.
1. Si una unidad es no trivial, va en rama con patrón
   `tipo/<issue-id>-slug`.
1. Si una unidad es trivial y aislada, puede ir a `main`.
1. Codex reporta siempre:
   - qué unidad ejecutó,
   - qué commit generó,
   - qué Issue cerró o dejó abierta.

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

## Regla especial para diseño y arquitectura

- Si la tarea es de dominio, arquitectura o proceso crítico:
  - se discute primero en conversación interactiva;
  - se documenta después de aprobación explícita de Kiko;
  - no se cierra la Issue sin esa aprobación.
  - si hace falta interfaz de respuestas clicables, Codex avisa para activar
    `Plan Mode`.

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

## Estrategia de APK en releases

Estado actual:

- No hay pipeline de build Android en GitHub Actions.
- No hay adjunto automático de `.apk` en releases.

Opciones para Fase 1:

1. Manual:
   - compilar localmente y adjuntar `.apk` en la release.
1. Automática:
   - workflow de GitHub Actions al crear tag;
   - generar `.apk` y adjuntarlo a la release.

Requisitos de automatización:

- toolchain Android en CI;
- secretos de firma (`keystore`, passwords y alias);
- definición de variante (`debug` o `release`).

## Cadencia recomendada

1. Abrir Issue.
1. Ejecutar trabajo en rama.
1. Hacer N commits pequeños.
1. Abrir PR si aplica.
1. Cerrar Issue.
1. Actualizar changelog.
