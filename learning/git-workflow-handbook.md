# Handbook de Flujo Git (Aprendizaje Reusable)

## Metadatos

- `doc_id`: LEARN-GIT-WORKFLOW-HANDBOOK
- `purpose`: Enseñar un flujo GitHub Flow sencillo y profesional.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-20

## Qué aprender con este flujo

- Cómo convertir trabajo en tareas trazables.
- Cómo agrupar varios commits bajo una sola tarea.
- Cuándo usar PR y cuándo no hace falta.
- Cómo versionar sin complejidad innecesaria.

## Ciclo mínimo recomendado

1. Crear Issue para trabajo no trivial.
1. Crear rama `tipo/<issue-id>-slug`.
1. Hacer commits pequeños con convención.
1. Abrir PR si el cambio es relevante.
1. Cerrar Issue.
1. Reflejar cambios en `CHANGELOG.md`.

## Regla mental clave

- Relación correcta: `1 tarea -> 1 rama -> N commits -> 1 cierre`.
- No busques `1 tarea -> 1 commit`.

## Ejemplo práctico

Tarea: “Definir flujo de repositorio”.

- Rama: `docs/12-repo-workflow`.
- Commits:
  - `docs(repo): crear guía de flujo en docs`
  - `docs(contributing): alinear reglas con guía`
  - `chore(changelog): registrar cambios en unreleased`
- Cierre: Issue #12 queda resuelta.

## Anti patrones frecuentes

- Commit directo a `main` para cambios relevantes.
- Commits gigantes con múltiples objetivos.
- Trabajar sin Issue en tareas de proceso.
- Cerrar tareas sin actualizar changelog.

## Señales de buen uso

- El historial de commits es legible.
- Cada tarea importante tiene contexto en Issue.
- Puedes reconstruir decisiones sin leer chats externos.
- El release de hito se arma en minutos.
