# AGENTS

## Metadatos

- `doc_id`: AGENTS
- `purpose`: Contrato operativo de trabajo entre IA y humano.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-23
- `next_review`: 2026-03-09

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
- Las decisiones de arquitectura o dominio se trabajan en modo interactivo.
- Ninguna Issue de diseño se cierra sin aprobación explícita de Kiko.
- Si una decisión requiere respuestas interactivas, Codex debe avisar
  explícitamente para activar `Plan Mode` antes de continuar.

## Flujo operativo

### Inicio de sesión

1. Leer `AGENTS.md`.
1. Leer `docs/system-map.md`.
1. Confirmar objetivo y alcance.

### Durante la sesión

1. Registrar decisiones en `docs/decision-log.md`.
1. Ejecutar checklists de `docs/context-checklists.md`.
1. Mantener trazabilidad de conflictos y precedencia.

### Protocolo de colaboración con Codex

1. Kiko puede pedir implementación directa en lenguaje natural.
1. Codex se encarga de convertir la petición en unidades de trabajo.
1. Si la petición incluye cambios independientes, Codex los separa.
1. Regla por defecto:
   - trabajo trivial aislado: puede ir directo a `main`;
   - trabajo no trivial o con varias unidades: Issue por unidad.
1. Relación objetivo:
   - `1 Issue -> 1 rama -> N commits -> 1 cierre`.
1. Aclaración de `main`:
   - `main` es rama principal;
   - el trabajo directo a `main` se reserva a cambios triviales y aislados.
1. Si una unidad se ejecuta en rama, su Issue se cierra tras integración en
   `main` (merge/PR), salvo instrucción explícita de Kiko.
1. Comandos conversacionales de priorización:
   - `siguiente pendiente` y `siguiente issue pendiente` son equivalentes;
   - `siguiente paso` revisa primero PRs pendientes (incluyendo `draft`);
   - si no hay PRs pendientes, `siguiente paso` pasa a resolver la siguiente
     Issue pendiente.
1. Ejecución por defecto de `siguiente paso`:
   - `siguiente paso` implica identificar el trabajo prioritario y ejecutarlo
     en la misma pasada por defecto;
   - excepciones: `Plan Mode`, bloqueo real o petición explícita de solo plan/
     análisis.
1. Redacción en castellano:
   - usar ortografía completa (tildes, `ñ` y signos correctos) en issues, PR,
     documentación y futuros textos de UI;
   - mantener identificadores técnicos en inglés cuando aplique;
   - usar `UTF-8` en archivos de texto del repo.
1. Limpieza de ramas:
   - tras cada merge/cierre, limpiar ramas locales y remotas mergeadas no
     reutilizables;
   - excluir `main`, la rama actual, ramas con PR abierta y ramas no mergeadas
     (salvo descarte explícito).
1. Si Kiko pide varias cosas pequeñas juntas, Codex decide el corte y deja
   trazabilidad de cómo las agrupó.
1. En tareas de diseño (`type:decision` o equivalentes), Codex primero
   propone, luego revisa con Kiko y solo después documenta como cerrado.
1. Cuando sea necesario responder con interfaz interactiva, Codex debe indicar
   “activa `Plan Mode`” antes de lanzar decisiones.
1. Al inicio de una sesión, Kiko puede pedir “dame 3-5 tareas recomendadas”
   y Codex propondrá un menú priorizado.
1. Al cierre de cada sesión, Codex devuelve siguiente menú numerado.

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
- Estrategia de sincronización MVP: `docs/sync-strategy.md`
- Política de conflictos concurrentes MVP: `docs/conflict-policy.md`
- Controles temporales de campaña: `docs/campaign-temporal-controls.md`
- Checklist técnico de implementación MVP: `docs/mvp-implementation-checklist.md`
- Guía reusable: `learning/handbook.md`
- Anexo Frosthaven: `learning/frosthaven-annex.md`
- Bibliografía anotada: `learning/sources.md`
- Flujo Git y GitHub: `docs/repo-workflow.md`
- Guía didáctica de flujo Git: `learning/git-workflow-handbook.md`

## Nota sobre APK y releases

La subida automática de `.apk` a Releases no está activa en Fase 0.
Cuando se implemente build Android, se definirá si el `.apk` se adjunta
manualmente o mediante GitHub Actions al crear tags de release.

## Nota de legado

El legado temporal se mantiene hasta completar dos hitos verificados con éxito.
