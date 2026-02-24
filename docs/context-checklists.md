# Checklists de Contexto

## Metadatos

- `doc_id`: DOC-CONTEXT-CHECKLISTS
- `purpose`: Checklists operativas para calidad y trazabilidad.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Formato canónico por checklist

- `checklist_id`
- `trigger`
- `steps`
- `validation`
- `owner`

## CHK-SESSION-START

- `trigger`: inicio de sesión.
- `steps`:

  1. Leer `AGENTS.md`.
  1. Leer `docs/system-map.md`.
  1. Confirmar objetivo y alcance en una frase.
  1. Verificar que no se rompe el no alcance de fase.

- `validation`:

  1. Objetivo y alcance explícitos.
  1. Documento oficial de referencia identificado.

- `owner`: IA ejecuta, Kiko valida.

## CHK-TASK-SPLIT

- `trigger`: petición con múltiples cambios en un mismo mensaje.
- `steps`:

  1. Identificar unidades independientes.
  1. Clasificar cada unidad como trivial o no trivial.
  1. Definir si se agrupa o se separa en Issues.
  1. Registrar criterio de separación en el reporte de sesión.

- `validation`:

  1. No hay mezcla de cambios no relacionados en una sola unidad.
  1. La trazabilidad final explica qué quedó en cada commit/Issue.

- `owner`: IA ejecuta, Kiko valida.

## CHK-MILESTONE-CLOSE

- `trigger`: cierre de hito.
- `steps`:

  1. Actualizar documentos oficiales afectados.
  1. Registrar decisiones en `docs/decision-log.md`.
  1. Ejecutar verificación A de estructura.
  1. Ejecutar verificación B de criterios y edge cases.
     - Si existe matriz oficial de edge cases (`#17`), usarla como insumo
       principal de cobertura/riesgo.
     - Si existe plan oficial de pruebas de invariantes (`#19`), usarlo para
       distinguir bloqueantes (`P0`) y diferidos aceptados antes del gate.
  1. Registrar evidencia en `docs/context-governance.md`.

- `validation`:

  1. No hay decisión crítica sin trazabilidad.
  1. La verificación doble está registrada.
  1. Los conflictos legado/oficial están registrados.

- `owner`: IA ejecuta, Kiko valida.

## CHK-SCOPE-CHANGE

- `trigger`: cambio de alcance en sesión.
- `steps`:

  1. Definir qué cambia del alcance original.
  1. Evaluar impacto sobre gate estricto.
  1. Registrar decisión en `docs/decision-log.md`.
  1. Actualizar `docs/context-governance.md` si cambia el estado.

- `validation`:

  1. Alcance nuevo documentado.
  1. No hay trabajo oculto fuera de fase.

- `owner`: IA ejecuta, Kiko valida.

## CHK-NEXT-STEP

- `trigger`: comando conversacional `siguiente paso`.
- `steps`:

  1. Verificar si existe **unidad pendiente de cierre** antes de buscar trabajo
     nuevo.
  1. Revisar en orden:
     - trabajo local sin commit;
     - commits locales sin `push`;
     - rama publicada sin PR (si aplica);
     - PR abierta (`draft` o no);
     - Issue abierta tras merge;
     - limpieza de rama pendiente.
  1. Si existe unidad pendiente de cierre, resolver esa unidad hasta el máximo
     cerrable (end-to-end por defecto).
  1. Si no existe unidad pendiente de cierre, aplicar la regla normal de
     priorización (`PRs` -> orden técnico -> `siguiente pendiente`).
  1. Si la ejecución ocurre en `Plan Mode` y se identifica una Issue/unidad
     prioritaria, abrir al menos una ronda de decisiones de esa unidad antes de
     emitir `<proposed_plan>` (sin meta-plan de "iniciar el plan").
  1. Reportar unidad priorizada, estado de cierre, bloqueo (si existe) y si se
     puede pasar a la siguiente unidad.

- `validation`:

  1. No se inicia una unidad nueva mientras exista una unidad pendiente de
     cierre no bloqueada.
  1. En `Plan Mode`, no se devuelve un `<proposed_plan>` cuyo siguiente paso sea
     empezar a planificar la misma unidad ya priorizada.
  1. El reporte final explicita el estado de cierre alcanzado.
  1. Si la unidad es `type:decision`, queda claro si falta aprobación explícita
     de Kiko o si se cerró en el mismo turno.

- `owner`: IA ejecuta, Kiko valida.

## CHK-BRANCH-CLEANUP

- `trigger`: merge/cierre de PR o cierre de Issue trabajada en rama.
- `steps`:

  1. Verificar estado de la PR asociada (mergeada o cerrada explícitamente).
  1. Confirmar que la rama no queda en uso activo.
  1. Limpiar ramas locales mergeadas no reutilizables (excepto `main` y rama
     actual).
  1. Limpiar ramas remotas mergeadas no reutilizables.
  1. Confirmar que no queda PR abierta asociada a la rama limpiada.
  1. Registrar excepciones (por ejemplo rama no mergeada conservada).

- `validation`:

  1. No se borran `main`, la rama actual ni ramas con PR abierta.
  1. La limpieza local/remota queda ejecutada o justificada.
  1. El estado final de la PR/Issue asociada es trazable.

- `owner`: IA ejecuta, Kiko valida.

## CHK-GATE-CODE

- `trigger`: solicitud de paso a implementación.
- `steps`:

  1. Confirmar que Fase 0 está validada.
  1. Verificar decisiones críticas abiertas.
  1. Verificar checklist completa.
  1. Verificar `#19`:
     - `P0` definidos y trazados;
     - diferidos aceptados explícitos (si existen).
  1. Emitir resultado del gate:
     - `apto`;
     - `apto_con_diferidos_aceptados`; o
     - `no_apto`.
  1. Registrar evidencia en `docs/context-governance.md`.

- `validation`:

  1. Si falta una condición bloqueante, resultado `no_apto`.
  1. Si todo está completo y no hay diferidos aceptados, resultado `apto`.
  1. Si todo está completo y hay diferidos aceptados explícitos, resultado
     `apto_con_diferidos_aceptados`.

- `owner`: IA ejecuta, Kiko valida.

## Registro de ejecución inicial

### RUN-H0-01

- `date`: 2026-02-20
- `checklist_id`: CHK-SESSION-START
- `result`: pass
- `notes`: inicio de fase con mapa y alcance explícito.

### RUN-H0-02

- `date`: 2026-02-20
- `checklist_id`: CHK-MILESTONE-CLOSE
- `result`: pass
- `notes`: decisiones y verificaciones registradas.
