# Flujo de Repositorio

## Metadatos

- `doc_id`: DOC-REPO-WORKFLOW
- `purpose`: Definir el flujo Git y GitHub adoptado.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-23
- `next_review`: 2026-03-09

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
- `main` es la rama principal del repositorio, pero el trabajo directo a
  `main` se reserva para cambios triviales y aislados.

## Flujo recomendado con Codex

1. Kiko pide objetivo o cambio.
1. Codex lo traduce a unidades ejecutables.
1. Si hay varias unidades, se crean Issues separadas.
1. Si una unidad es no trivial, va en rama con patrón
   `tipo/<issue-id>-slug`.
1. Si una unidad es trivial y aislada, puede ir a `main`.
1. Si una unidad se ejecuta en rama, la Issue asociada se cierra tras integrar
   el trabajo en `main` (merge/PR), salvo instrucción explícita de Kiko.
1. Codex reporta siempre:
   - qué unidad ejecutó,
   - qué commit generó,
   - qué Issue cerró o dejó abierta.

### Reglas de priorización conversacional (`siguiente paso`, `siguiente pendiente`)

- `siguiente pendiente` y `siguiente issue pendiente` son equivalentes.

- Si Kiko pide `siguiente pendiente`, Codex selecciona por defecto la Issue
  abierta (`state=open`) con número más bajo.
- Si Kiko indica filtros (por ejemplo `type`, `label` o `phase`), Codex aplica
  esos filtros antes de ordenar por número.
- Si no hay Issues abiertas que cumplan el criterio, Codex lo reporta de forma
  explícita.

#### Regla de `siguiente paso`

- Codex revisa primero las PRs abiertas del repo (incluyendo `draft`).
- Si hay varias PRs abiertas, prioriza la PR con número más bajo.
- Si existe al menos una PR abierta, el siguiente paso es llevar esa PR a
  cierre (merge o cierre explícito si se descarta).
- Si no hay PRs abiertas, Codex busca un **orden técnico recomendado** en la
  documentación oficial aplicable.
- Si existe orden técnico recomendado:
  - usa la fuente oficial más específica disponible (detalle > macro);
  - recorre el orden y elige la primera Issue abierta **cerrable**;
  - si una Issue abierta no es cerrable, la salta y evalúa la siguiente;
  - si no hay Issues cerrables en ese orden, elige la primera Issue
    `draftable`.
- Si no existe orden técnico aplicable, el siguiente paso es resolver la
  `siguiente pendiente` (`siguiente issue pendiente`).
- Definición operativa para esta regla:
  - `cerrable`: Issue abierta con dependencias de cierre satisfechas según la
    documentación oficial vigente.
  - `draftable`: Issue abierta que puede iniciarse en borrador, pero cuyo cierre
    depende de otras Issues.
  - `blocked`: Issue abierta que no debe cerrarse hasta resolver dependencias
    faltantes.
- Cuando Kiko pide `siguiente paso`, Codex identifica el paso prioritario y lo
  ejecuta en la misma sesión/pasada por defecto.
- Excepciones explícitas:
  - `Plan Mode` (se planifica y no se ejecuta).
  - Bloqueo real que impida continuar.
  - Petición explícita de solo plan o solo análisis.

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

## Redacción y codificación de texto

- En textos en castellano (issues, PR, documentación y futuros textos de UI)
  usar ortografía completa: tildes, `ñ` y signos correctos.
- Mantener identificadores técnicos en inglés cuando aplique.
- Archivos de texto del repo en `UTF-8`.
- Si aparece mojibake en la terminal, verificar primero la codificación real
  del archivo antes de editar contenido ya correcto.

## Reglas de PR

- PR obligatoria cuando el cambio sea relevante.
- Si el trabajo se hace en rama, la Issue asociada se cierra tras merge o
  integración en `main`, salvo instrucción explícita de Kiko.
- Debe incluir:
  - referencia al Issue
  - resumen de alcance
  - checklist de calidad completada

## Limpieza de ramas

- Tras cada merge/cierre, limpiar ramas locales y remotas mergeadas que no se
  vayan a reutilizar.
- Exclusiones por defecto:
  - `main`
  - rama actual
  - ramas con PR abierta
  - ramas no mergeadas (salvo descarte explícito)
- Si una rama fue integrada por `rebase` y `git branch -d` avisa que no está
  mergeada en `HEAD`, se permite borrarla tras verificar que la PR fue mergeada.

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

### Flujo en rama (trabajo no trivial o relevante)

1. Abrir Issue.
1. Ejecutar trabajo en rama.
1. Hacer N commits pequeños.
1. Abrir PR.
1. Mergear en `main`.
1. Cerrar Issue.
1. Limpiar rama local/remota si ya no se reutiliza.
1. Actualizar changelog.

### Flujo directo a `main` (trabajo trivial y aislado)

1. Ejecutar ajuste trivial en `main`.
1. Hacer commit y push.
1. Cerrar Issue (si aplica).
1. Actualizar changelog si corresponde.
