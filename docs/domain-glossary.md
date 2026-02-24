# Glosario de Dominio

## Metadatos

- `doc_id`: DOC-DOMAIN-GLOSSARY
- `purpose`: Definir el modelo de dominio e invariantes operativas del MVP.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar un contrato de dominio único y trazable para la Issue #6 con una sola
entidad `Entry` (`scenario|outpost`) y jerarquía temporal explícita:
`campaign > year > season > week > entry`.

## Entidades

### Campaign

- `campaign_id`: string fijo, valor `01`.
- `week_cursor`: entero, semana actual activa.
  - En MVP apunta a la **primera `Week` abierta** (menor `week_number` abierta)
    y se recalcula tras operaciones que cambian el estado de `Week`.
- `resource_totals`: mapa `resource_key -> int` derivado de la suma de
  `Entry.resource_deltas` en la campaña.
- `created_at_utc`, `updated_at_utc`: auditoría mínima (server-only).

### Year

- `year_number`: entero positivo.
- `created_at_utc`, `updated_at_utc`: auditoría mínima (server-only).

### Season

- `season_type`: `summer|winter`.
- `year_number`: entero positivo.
- En castellano, `season` se traduce como **estación** (`verano|invierno`), no
  “temporada”.
- `created_at_utc`, `updated_at_utc`: auditoría mínima (server-only).

### Week

- `week_number`: entero global `1..N`, inmutable y trazable.
- `status`: `open|closed`.
- `notes`: texto opcional.
- `created_at_utc`, `updated_at_utc`: auditoría mínima (server-only).

### Entry

- `entry_id`: auto-id técnico.
- `order_index`: entero positivo para orden del timeline.
  - En MVP puede corregirse manualmente dentro de la misma `Week` con
    resecuenciación densa `1..N`.
- `type`: `scenario|outpost`.
- `scenario_ref`: entero positivo obligatorio cuando `type=scenario`.
- `resource_deltas`: mapa `resource_key -> int` (delta neto por recurso en la
  `Entry`; solo claves con delta `!= 0`, ausencia de clave = `0`).
- `created_at_utc`, `updated_at_utc`: auditoría mínima (server-only).

### Session

- Cuelga de una `Entry` (owner implícito por ruta, sin `owner_type`).
- `started_at_utc`: timestamp UTC.
- `ended_at_utc`: timestamp UTC o `null` si está activa.
- `created_at_utc`, `updated_at_utc`: auditoría mínima (server-only).

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

## Reglas temporales

- Persistencia temporal en UTC.
- `week_number` global inmutable.
- Seleccionar `Week` para navegación/foco no implica cambiar `week_cursor`.
- `week_cursor` se deriva de la primera `Week` abierta (menor `week_number`
  abierta) según `docs/editability-policy.md`.
- Las correcciones manuales de `Week.status` (`reopen`/`reclose`) recalculan
  `week_cursor`.
- `year_number` y `season_type` son coherentes con `week_number` y la jerarquía.
- En esta issue no se define provisión inicial de años (por ejemplo, crear 4
  años en bloque).
- El detalle técnico de inicialización/extensión temporal y cardinalidad de
  semanas por estación se define en `docs/campaign-temporal-initialization.md`.
- La política de editabilidad manual y correcciones de estado/sesiones se define
  en `docs/editability-policy.md`.
- La política de timestamps de auditoría y orden estable se define en
  `docs/timestamp-order-policy.md`.

## Invariantes operativas cerradas

1. La diferenciación funcional entre entradas se hace por `Entry.type`.
1. `order_index` define el orden de visualización del timeline.
1. En MVP sí hay reordenación manual de `Entry`, limitada a la misma `Week`, con
   resecuenciación densa `1..N`.
1. Solo puede existir `0..1` `Session` activa global en la campaña.
1. Si se inicia una nueva sesión con otra activa, se hace `auto-stop` de la
   anterior y `start` de la nueva.
1. Si se borra una `Entry` activa, se hace `auto-stop` y luego borrado en
   cascada de `sessions`; sus `resource_deltas` se eliminan al borrar la
   `Entry`.
1. Si se cierra `Week` con sesión activa, se hace `auto-stop` y luego cierre.
1. `Week.status` puede corregirse manualmente (`reopen`/`reclose`) en MVP.
1. Se permiten correcciones manuales completas de `Session` (crear/editar/
   borrar), manteniendo `0..1` sesión activa global.
1. `week_cursor` siempre apunta a la primera `Week` abierta (menor
   `week_number` abierta) y se recalcula tras cambios de estado de `Week`;
   navegar semanas no cambia el cursor.
1. Debe existir al menos una `Week` abierta provisionada para mantener
   `week_cursor` como entero válido.
1. Cada `Entry.resource_deltas[resource_key]` es entero firmado y se valida que
   el estado final de totales no sea negativo.
1. `scenario_ref` es obligatorio y entero positivo para `scenario`.
1. No se fija cardinalidad explícita de `outpost` en esta issue.

## Casos borde y validación

1. Se reconstruye owner de `Session` únicamente por ruta.
1. `created_at_utc` y `updated_at_utc` son server-only en las entidades
   auditadas del MVP; no se usa `deleted_at_utc`.
1. Cambios en semanas históricas no alteran `week_number`.
1. Crear `Entry` tipo `scenario` sin `scenario_ref` debe rechazarse.
1. Crear `Entry` tipo `outpost` sin campos extra debe aceptarse.
1. Reordenar `Entry` solo se permite dentro de la misma `Week` y deja
   `order_index` denso `1..N`.
1. Iniciar sesión con otra activa debe cerrar la anterior y abrir la nueva.
1. Correcciones manuales de `Session` deben rechazar estados que produzcan más
   de una sesión activa global.
1. Borrar `Entry` debe eliminar en cascada sus hijos.
1. Si el delta neto de un recurso en `Entry.resource_deltas` llega a `0`, la
   clave se elimina del mapa.
1. Reabrir o re-cerrar una `Week` recalcula `week_cursor` a la primera `Week`
   abierta.
1. No se permite cerrar/re-cerrar una `Week` si la operación dejaría `0` weeks
   abiertas provisionadas.
1. Operaciones que dejen totales finales negativos deben rechazarse.
1. Cerrar `Week` con sesión activa debe cerrar sesión y recalcular `week_cursor`
   según la primera `Week` abierta.
1. Seleccionar una semana en el control temporal superior no debe cambiar
   `week_cursor` sin acción explícita adicional.
