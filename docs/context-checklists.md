# Checklists de Contexto

## Metadatos

- `doc_id`: DOC-CONTEXT-CHECKLISTS
- `purpose`: Checklists operativas para calidad y trazabilidad.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-06

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

## CHK-MILESTONE-CLOSE

- `trigger`: cierre de hito.
- `steps`:

  1. Actualizar documentos oficiales afectados.
  1. Registrar decisiones en `docs/decision-log.md`.
  1. Ejecutar verificación A de estructura.
  1. Ejecutar verificación B de criterios y edge cases.
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

## CHK-GATE-CODE

- `trigger`: solicitud de paso a implementación.
- `steps`:

  1. Confirmar que Fase 0 está validada.
  1. Verificar decisiones críticas abiertas.
  1. Verificar checklist completa.
  1. Emitir resultado habilitado o bloqueado.

- `validation`:

  1. Si falta una condición, resultado bloqueado.
  1. Si todo está completo, resultado habilitado.

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
