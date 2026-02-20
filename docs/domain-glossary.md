# Glosario de Dominio

## Metadatos

- `doc_id`: DOC-DOMAIN-GLOSSARY
- `purpose`: Definir el modelo de dominio e invariantes operativas del MVP.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-06

## Objetivo

Cerrar un contrato de dominio único y trazable para la Issue #6 con una sola
entidad `Entry` (`scenario|outpost`) y jerarquía temporal explícita:
`campaign > year > season > week > entry`.

## Entidades

### Campaign

- `campaign_id`: string fijo, valor `01`.
- `week_cursor`: entero, semana actual activa.
- `resource_totals`: mapa `resource_key -> int` derivado del log de cambios.

### Year

- `year_number`: entero positivo.

### Season

- `season_type`: `summer|winter`.
- `year_number`: entero positivo.

### Week

- `week_number`: entero global `1..N`, inmutable y trazable.
- `status`: `open|closed`.
- `notes`: texto opcional.
- `created_at_utc`, `updated_at_utc`, `deleted_at_utc`: auditoría mínima.

### Entry

- `entry_id`: auto-id técnico.
- `order_index`: entero positivo para orden del timeline.
- `type`: `scenario|outpost`.
- `scenario_ref`: entero positivo obligatorio cuando `type=scenario`.
- `created_at_utc`, `updated_at_utc`, `deleted_at_utc`: auditoría mínima.

### Session

- Cuelga de una `Entry` (owner implícito por ruta, sin `owner_type`).
- `started_at_utc`: timestamp UTC.
- `ended_at_utc`: timestamp UTC o `null` si está activa.
- `created_at_utc`, `updated_at_utc`, `deleted_at_utc`: auditoría mínima.

### ResourceChange

- Cuelga de una `Entry` (owner implícito por ruta, sin `owner_type`).
- `resource_key`: recurso del MVP.
- `delta`: entero firmado (`+/-`, distinto de cero).
- `created_at_utc`, `updated_at_utc`, `deleted_at_utc`: auditoría mínima.

## Recursos MVP (`resource_key`)

- `lumber`
- `metal`
- `hide`
- `arrowvine`
- `axenut`
- `corpsecap`
- `flamefruit`
- `rockroot`
- `snowthistle`
- `inspiration`
- `morale`
- `soldiers`

## Jerarquía y preesquema Firestore

- `campaigns/01/years/{year_number}`
- `campaigns/01/years/{year_number}/seasons/{season_type}`
- `campaigns/01/years/{year_number}/seasons/{season_type}/weeks/{week_number}`
- `.../weeks/{week_number}/entries/{entry_id}`
- `.../entries/{entry_id}/sessions/{session_id}`
- `.../entries/{entry_id}/resource_changes/{change_id}`

## Reglas temporales

- Persistencia temporal en UTC.
- `week_number` global inmutable.
- `year_number` y `season_type` son coherentes con `week_number` y la jerarquía.
- En esta issue no se define provisión inicial de años (por ejemplo, crear 4
  años en bloque).

## Invariantes operativas cerradas

1. La diferenciación funcional entre entradas se hace por `Entry.type`.
1. `order_index` define el orden de visualización del timeline.
1. En MVP no hay reordenación manual de `Entry`.
1. Solo puede existir `0..1` `Session` activa global en la campaña.
1. Si se inicia una nueva sesión con otra activa, se hace `auto-stop` de la
   anterior y `start` de la nueva.
1. Si se borra una `Entry` activa, se hace `auto-stop` y luego borrado en
   cascada (`sessions` y `resource_changes`).
1. Si se cierra `Week` con sesión activa, se hace `auto-stop` y luego cierre.
1. `ResourceChange.delta` es entero firmado y se valida que el estado final de
   totales no sea negativo.
1. `scenario_ref` es obligatorio y entero positivo para `scenario`.
1. No se fija cardinalidad explícita de `outpost` en esta issue.

## Casos borde y validación

1. Se reconstruye owner de `Session` y `ResourceChange` únicamente por ruta.
1. Cambios en semanas históricas no alteran `week_number`.
1. Crear `Entry` tipo `scenario` sin `scenario_ref` debe rechazarse.
1. Crear `Entry` tipo `outpost` sin campos extra debe aceptarse.
1. Iniciar sesión con otra activa debe cerrar la anterior y abrir la nueva.
1. Borrar `Entry` debe eliminar en cascada sus hijos.
1. Operaciones que dejen totales finales negativos deben rechazarse.
1. Cerrar `Week` con sesión activa debe cerrar sesión y avanzar cursor.
