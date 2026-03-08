# AGENTS

## Metadatos

- `doc_id`: AGENTS
- `purpose`: Contrato operativo de trabajo entre IA y humano.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-06
- `next_review`: 2026-03-16

## Propósito

Este archivo define cómo se trabaja en este repositorio durante la transición
de preparación documental a implementación y en el arranque de implementación.
La prioridad es mantener un flujo profesional, trazable y sencillo.

## Alcance de la etapa actual

- Mantener el sistema documental de contexto y su trazabilidad.
- Aplicar y registrar el gate de readiness para entrada a código.
- Permitir implementación de código de la app tras gate `#20` válido.

## Reglas no negociables

- No iniciar código de la app antes de validar el gate `#20` con resultado
  `apto` o `apto_con_diferidos_aceptados`.
- Si el gate `#20` resulta `no_apto`, la implementación queda bloqueada hasta
  corregir los bloqueantes.
- Las decisiones de runtime/arquitectura con impacto transversal deben quedar
  registradas en documentación oficial; las de diseño requieren aprobación
  explícita de Kiko.
- La documentación oficial vive en `AGENTS.md`, `docs/` y `learning/`.
- Los documentos legacy de arranque (`summary_initial_conversation.txt`,
  `tdd.md`, `important.txt`, `neil.txt`) fueron retirados del repo el
  `2026-03-01`; su trazabilidad histórica se conserva en `docs/decision-log.md`.
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
   - `siguiente paso` revisa primero si existe una **unidad pendiente de
     cierre** (trabajo local sin commit, commits sin `push`, rama sin PR cuando
     aplica, PR abierta, Issue abierta tras merge o limpieza de rama pendiente);
   - si existe unidad pendiente de cierre, `siguiente paso` resuelve esa unidad
     antes de iniciar trabajo nuevo;
   - solo si no existe unidad pendiente de cierre, `siguiente paso` revisa PRs
     pendientes (incluyendo `draft`);
   - si no hay PRs pendientes ni unidad pendiente de cierre, `siguiente paso`
     usa orden técnico recomendado (si existe) tomando la fuente oficial más
     específica (detalle > macro);
   - si no existe orden técnico aplicable, `siguiente paso` pasa a resolver la
     siguiente Issue pendiente;
   - si el siguiente item técnico no es cerrable, salta al siguiente cerrable;
   - si no hay cerrables en el orden técnico, toma el primer `draftable`.
1. Ejecución por defecto de `siguiente paso`:
   - `siguiente paso` implica identificar el trabajo prioritario y ejecutarlo
     en la misma pasada por defecto;
   - en trabajo no trivial con rama, el objetivo por defecto es **cierre
     end-to-end** de la unidad: cambios -> commit -> `push` -> PR -> merge/cierre
     -> cierre de Issue -> limpieza de rama (cuando aplique);
   - en `type:decision`, si falta aprobación explícita de Kiko, la unidad se
     deja bloqueada por aprobación y sigue siendo prioritaria en el siguiente
     `siguiente paso`; si Kiko aprueba explícitamente en el mismo turno, Codex
     completa el cierre en esa misma pasada;
   - en `Plan Mode`, si `siguiente paso` identifica una Issue/unidad
     prioritaria (no una unidad pendiente de cierre), Codex debe entrar en las
     decisiones de esa unidad en ese mismo turno; no debe cerrar con un
     meta-plan cuyo siguiente paso sea "iniciar el plan" de esa misma unidad;
   - tras cada `siguiente paso`, Codex reporta: unidad priorizada, estado de
     cierre alcanzado (`local`, `push`, `PR`, `merge`, `issue`, `cleanup`),
     bloqueo (si existe) y si puede pasar o no a la siguiente unidad;
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
1. Validación UI en implementación (Flet web):
   - Kiko lanza el servidor cuando haga falta validar UI/flujo visual;
   - comando por defecto: `pipenv run flet run src/main.py --web -d -r --port 8550 --host 127.0.0.1`;
   - Kiko confirma URL activa y warnings relevantes;
   - Codex valida con Playwright/DevTools y usa evidencia adaptativa (solo la necesaria según la tarea);
   - fallback por defecto si `8550` está ocupado: puerto alternativo y URL explícita comunicada por Kiko;
   - detalles operativos en `docs/repo-workflow.md`.
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
- Contrato de operaciones Firestore por agregado (MVP): `docs/firestore-operation-contract.md`
- Modelo de recursos por `Entry` (MVP): `docs/resource-delta-model.md`
- Reglas de validación y recálculo de recursos (MVP): `docs/resource-validation-recalculation.md`
- Política de timestamps y orden estable (MVP): `docs/timestamp-order-policy.md`
- Flujo de sesión activa y `auto-stop` (MVP): `docs/active-session-flow.md`
- Consultas mínimas para pantalla principal (MVP): `docs/minimal-read-queries.md`
- Matriz de edge cases de concurrencia/sincronización (MVP): `docs/concurrency-sync-edge-case-matrix.md`
- Plan de pruebas para invariantes de dominio (MVP): `docs/domain-invariant-test-plan.md`
- Gate de listo para codificar (Fase 1 MVP): `docs/coding-readiness-gate.md`
- Controles temporales de campaña: `docs/campaign-temporal-controls.md`
- Inicialización temporal de campaña (técnica): `docs/campaign-temporal-initialization.md`
- Política de editabilidad manual MVP: `docs/editability-policy.md`
- Checklist técnico de implementación MVP: `docs/mvp-implementation-checklist.md`
- Bloques de implementación MVP: `docs/mvp-implementation-blocks.md`
- Guía reusable: `learning/handbook.md`
- Anexo Frosthaven: `learning/frosthaven-annex.md`
- Bibliografía anotada: `learning/sources.md`
- Flujo Git y GitHub: `docs/repo-workflow.md`
- Flujo de release GitHub automatizada: `docs/github-release-automation.md`
- Guía didáctica de flujo Git: `learning/git-workflow-handbook.md`

## Nota sobre APK y releases

La subida automática de `.apk` a Releases no está activa en Fase 0.
Cuando se implemente build Android, se definirá si el `.apk` se adjunta
manualmente o mediante GitHub Actions al crear tags de release.

## Nota de legado

El legado textual inicial ya fue retirado del árbol activo.
