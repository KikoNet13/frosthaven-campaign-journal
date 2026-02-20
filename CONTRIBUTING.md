# Guía de Contribución

## Objetivo

Mantener un flujo profesional, simple y trazable para un proyecto pequeño.

## Flujo adoptado

- Modelo: GitHub Flow minimalista.
- Rama principal: `main`.
- Tareas no triviales: Issue + rama + commits + cierre.
- Cambios relevantes: PR obligatoria.
- Cambios triviales: permitido directo a `main`.
- Decisiones de arquitectura o dominio: revisión interactiva obligatoria con
  aprobación explícita antes del cierre.

## Convención de ramas

Patrón:

`tipo/<issue-id>-slug`

Tipos permitidos:

- `feat`
- `docs`
- `chore`
- `fix`
- `refactor`
- `test`
- `hotfix`

Ejemplo:

`docs/12-repo-workflow`

## Convención de commits

Formato:

`type(scope): resumen en español`

Ejemplos:

- `docs(repo): definir flujo de ramas y releases`
- `chore(git): inicializar repositorio y remote`
- `fix(docs): corregir enlaces del changelog`

## Relación tareas y commits

- Relación recomendada: `1 Issue -> 1 rama -> N commits -> 1 cierre`.
- No se exige relación `1:1` entre tarea y commit.

## Definición de trivial y relevante

Trivial:

- typo
- formato local
- ajuste menor en una sola zona sin impacto de proceso

Relevante:

- cambio de flujo de trabajo
- cambio de convenciones
- cambio estructural de documentación
- cambio que afecte más de un archivo importante

## Pull Request

Checklist mínima:

- Referencia al Issue.
- Descripción de objetivo y alcance.
- Confirmación de compatibilidad con Markdown lint.
- Impacto documentado en `CHANGELOG.md` (si aplica).
- Si es diseño o arquitectura, incluir nota de aprobación explícita de Kiko.

## Versionado

- Política: SemVer temprano `v0.x.y`.
- Al cerrar un hito:
  - actualizar `CHANGELOG.md`
  - crear tag
  - publicar release

## Estilo de documentación

- Idioma de descripciones: castellano.
- Identificadores técnicos: inglés cuando aplique.
- Markdown compatible con `markdownlint`.
