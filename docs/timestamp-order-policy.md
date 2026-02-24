# Política de Timestamps y Orden Estable entre Dispositivos (MVP)

## Metadatos

- `doc_id`: DOC-TIMESTAMP-ORDER-POLICY
- `purpose`: Definir la política MVP de auditoría temporal y orden estable entre dispositivos (timestamps server-only, reglas de escritura y tuplas canónicas por lista).
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar una decisión documental oficial para la auditoría temporal del MVP y el
orden estable entre dispositivos, de forma compatible con sincronización,
conflictos, contrato de operaciones por agregado y modelo de recursos vigente.

## Alcance y no alcance

Incluye:

- política de `created_at_utc` / `updated_at_utc` (server-only);
- reglas de escritura de timestamps en create/update/side-effects/hard delete;
- matriz explícita de orden canónico por lista (alcance UI + consultas mínimas
  de `#16`);
- manejo de timestamps pendientes (`serverTimestamp` no confirmado);
- alineación con `#12`, `#16`, `#40` y `docs/domain-glossary.md`.

No incluye:

- técnica Firestore exacta para materializar `serverTimestamp`;
- diseño de queries finales de `#16` (solo reglas de orden y prefijos);
- UX detallada de indicadores de estado provisional;
- código de app.

## Entradas y prerrequisitos

- `docs/sync-strategy.md` (Issue `#7`)
- `docs/conflict-policy.md` (Issue `#8`)
- `docs/firestore-operation-contract.md` (Issue `#12`)
- `docs/campaign-temporal-controls.md` (Issue `#9`)
- `docs/campaign-temporal-initialization.md` (Issue `#13`)
- `docs/editability-policy.md` (Issue `#37`)
- `docs/resource-delta-model.md` (Issue `#40`)
- `docs/domain-glossary.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`

## Decisiones cerradas de esta issue

1. Alcance de matriz de orden: listas visibles del MVP + consultas mínimas de
   `#16`.
1. Auditoría temporal: `server-only`.
1. `deleted_at_utc`: fuera del MVP.
1. Matriz de orden estable explícita por lista.
1. Orden canónico: prefijo de query + normalización final en cliente.
1. Último desempate global: `document_id` lexicográfico ascendente.
1. Sesiones en listas combinadas: activa primero.
1. Histórico de sesiones: `started_at_utc` descendente.
1. Timeline: orden de dominio (`week_number`, `order_index`) primero; timestamps
   solo como fallback/desempate.
1. Timestamps pendientes: orden canónico final solo garantizado tras `refresh`.
1. Auditoría ampliada a `campaign/year/season/week/entry/session`.
1. Forma de auditoría por entidad: `created_at_utc` + `updated_at_utc` en todas
   las entidades auditadas.
1. `updated_at_utc` cambia en toda escritura persistida, también derivada.
1. La matriz incluye también listas con orden de dominio (timestamps `N/A` o
   fallback), para dejar `#16` más cerrada.

## Política de auditoría temporal (server-only)

### Regla de origen

- `created_at_utc` y `updated_at_utc` se escriben como timestamps de servidor.
- El cliente no persiste timestamps “definitivos” locales para auditoría.

### Regla de escritura

1. En creación de documento se escriben `created_at_utc` y `updated_at_utc` en
   la misma operación lógica.
1. En actualización se preserva `created_at_utc` y se actualiza
   `updated_at_utc`.
1. Si una operación compuesta/derivada modifica un documento (por ejemplo
   `auto-stop`, recálculo o side-effect), ese documento también actualiza su
   `updated_at_utc`.
1. En hard delete no se usa `deleted_at_utc`; el documento se elimina
   directamente.

## Entidades auditadas y campos por entidad

| entity | created_at_utc | updated_at_utc | deleted_at_utc_mvp | timestamp_fields_adicionales | notas |
| --- | --- | --- | --- | --- | --- |
| `campaign` | Sí | Sí | No | `week_cursor` / `resource_totals` son datos, no timestamps | `updated_at_utc` cambia en provisión/extensión y cambios persistidos de campaña |
| `year` | Sí | Sí | No | Ninguno | Auditoría de documento temporal aunque su mutabilidad sea baja |
| `season` | Sí | Sí | No | Ninguno | Auditoría de documento temporal aunque su mutabilidad sea baja |
| `week` | Sí | Sí | No | Ninguno | Incluye cierres/reaperturas y `notes` |
| `entry` | Sí | Sí | No | Ninguno | Incluye cambios de `resource_deltas` y reordenación si el doc cambia |
| `session` | Sí | Sí | No | `started_at_utc`, `ended_at_utc` | `started_at_utc`/`ended_at_utc` modelan el intervalo; auditoría es aparte |

## Reglas de escritura de timestamps (create/update/side-effects/hard delete)

| familia_operacion | docs_que_crea | docs_que_actualiza | campos_timestamp_en_create | campos_timestamp_en_update | side_effects_actualizan_updated_at | notas |
| --- | --- | --- | --- | --- | --- | --- |
| `Campaign.provision_initial_years` | `campaign` (si aplica), `year`, `season`, `week` | `campaign` | `created_at_utc`, `updated_at_utc` | `updated_at_utc` | Sí | `campaign.updated_at_utc` refleja provisión/ajuste de cursor/totales si cambian |
| `Campaign.extend_years_plus_one` | `year`, `season`, `week` | `campaign` | `created_at_utc`, `updated_at_utc` | `updated_at_utc` | Sí | Incluye postcondición de `week_cursor` |
| `Week.*` (`close/reopen/reclose/update_notes`) | Ninguno | `week` (y `session` si `auto-stop`) | N/A | `updated_at_utc` | Sí | `auto-stop` actualiza `session.updated_at_utc` |
| `Entry.create/update/reorder` | `entry` (create) | `entry` | `created_at_utc`, `updated_at_utc` | `updated_at_utc` | Sí | `reorder` puede afectar múltiples entries; las entries modificadas actualizan `updated_at_utc` |
| `Entry.resource_deltas` (`adjust/set/clear`) | Ninguno | `entry`, `campaign` | N/A | `updated_at_utc` | Sí | `Entry` y `campaign` actualizan `updated_at_utc` si persisten cambios |
| `Entry.delete` | Ninguno | `session` (auto-stop previo, si aplica) | N/A | `updated_at_utc` (en la sesión antes de borrar) | Sí | Hard delete de `entry` y `session`; sin `deleted_at_utc` |
| `Session.start/stop/auto_stop/manual_*` | `session` (start/manual_create) | `session` (stop/auto/manual_update) | `created_at_utc`, `updated_at_utc` | `updated_at_utc` | Sí | `started_at_utc`/`ended_at_utc` son campos funcionales del intervalo |

## Política de orden estable (query + cliente)

### Regla general

1. Cada lista define una **tupla canónica de orden**.
1. La query aplica el prefijo de orden que Firestore puede garantizar.
1. El cliente completa la tupla canónica y reordena localmente.
1. El último desempate canónico es `document_id` lexicográfico ascendente.

### Regla de dominio vs timestamp

Cuando exista orden de dominio explícito (por ejemplo `week_number` u
`order_index`), ese orden es primario. Los timestamps se usan como fallback o
desempate estable, no como reemplazo del orden funcional del dominio.

## Manejo de timestamps pendientes

- El orden canónico final solo se garantiza con timestamps de servidor ya
  confirmados.
- Antes de confirmación puede existir estado/lista provisional en UI.
- Tras `refresh`, el cliente reaplica la tupla canónica final.
- Esta política no obliga a ocultar elementos pendientes; solo evita prometer
  estabilidad final antes del `refresh`.

## Matriz de listas y tuplas canónicas

| logical_list_id | uso_ui_o_lectura | query_order_prefix | client_canonical_tuple | timestamp_role | null_handling | pending_timestamp_behavior | notas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `year_selector_list` | Selector temporal de año (UI) | `year_number ASC` (si aplica) | `(year_number ASC)` | `N/A` | `N/A` | `N/A` | Lista de dominio |
| `season_list_within_year` | Navegación/estructura dentro de año | Sin prefijo natural útil por orden semántico | `(season_rank ASC, season_type ASC)` con `summer=0`, `winter=1` | `N/A` | `N/A` | `N/A` | Orden canónico fijo `summer -> winter` |
| `week_selector_list` | Selector temporal de semana (UI) | `week_number ASC` | `(week_number ASC)` | `N/A` | `N/A` | `N/A` | Lista de dominio |
| `timeline_week_groups` | Grupos/secciones de week en timeline | `week_number ASC` | `(week_number ASC)` | `N/A` | `N/A` | `N/A` | Compatible con `#16` |
| `week_entries_list` | Lista de entries de una `Week` (panel foco / selector de entry) | `order_index ASC` | `(order_index ASC, created_at_utc ASC, entry_id ASC)` | Fallback/desempate | `N/A` | `created_at_utc` pendiente puede dar orden provisional hasta `refresh` | `updated_at_utc` no se usa para evitar drift visual por ediciones no relacionadas con orden |
| `timeline_entries_flat` | Timeline aplanado multi-week (si `#16` lo define) | Prefijo máximo posible según query de `#16` | `(week_number ASC, order_index ASC, created_at_utc ASC, entry_id ASC)` | Fallback/desempate | `N/A` | `created_at_utc` pendiente => orden provisional | Lista condicional según diseño de `#16` |
| `entry_sessions_combined_list` | Sesiones de una `Entry` (activa + histórico) | `started_at_utc DESC` | `(is_active DESC, started_at_utc DESC, updated_at_utc DESC, session_id ASC)` | Principal + desempate | `ended_at_utc = null` => `is_active=1` | timestamps pendientes => orden provisional hasta `refresh` | Activa primero por regla de dominio |
| `entry_sessions_history_list` | Histórico de sesiones (sin activa o filtrando activas) | `started_at_utc DESC` | `(started_at_utc DESC, updated_at_utc DESC, session_id ASC)` | Principal + desempate | `N/A` | timestamps pendientes => orden provisional hasta `refresh` | Histórico descendente |

## Alineación con #12, #16 y #40

### `#12` (`docs/firestore-operation-contract.md`)

- `#12` sigue definiendo contrato por operación (pre/post/rechazos/atomicidad).
- `#18` define auditoría temporal y orden estable por lista.
- `#12` debe referenciar este documento y dejar de decir que la política de
  timestamps/desempates está “diferida”.

### `#16` (consultas mínimas)

- `#16` queda desbloqueada con una matriz de orden explícita por lista.
- `#16` puede centrarse en inventario de consultas, paginación y coste,
  reutilizando las tuplas canónicas definidas aquí.

### `#40` (modelo de recursos por `Entry`)

- No existe log `ResourceChange` en el MVP activo.
- `#18` no necesita inventariar listas/eventos de `ResourceChange`.
- Los cambios de recursos quedan cubiertos por auditoría/orden del documento
  `Entry` cuando el contexto de UI lo requiera.

## Casos de aceptación / verificación documental

1. La política elimina `deleted_at_utc` del MVP y documenta hard delete sin
   soft delete.
1. `Campaign`, `Year`, `Season`, `Week`, `Entry` y `Session` quedan con
   `created_at_utc` + `updated_at_utc`.
1. `updated_at_utc` se actualiza también en side-effects (`auto-stop`,
   recálculos, etc.) cuando el documento cambia persistentemente.
1. Las listas de dominio (`year/season/week`) tienen orden canónico explícito
   aunque no usen timestamps como criterio principal.
1. El timeline de entries usa orden de dominio primero (`week_number`,
   `order_index`) y timestamps solo como fallback/desempate.
1. La lista combinada de sesiones pone la activa primero y mantiene histórico
   estable con desempates.
1. Los timestamps pendientes solo garantizan orden provisional hasta `refresh`.
1. `#12`, `#16` y `#40` quedan alineadas sin contradicciones de orden/timestamps.

## Riesgos, límites y decisiones diferidas

- La técnica exacta para resolver `serverTimestamp` pendiente en la UI queda a
  implementación.
- La forma exacta de índices/`orderBy` en Firestore se concreta en `#16` y
  código.
- La paginación real de listas largas (si aplica) se define en `#16`.

## Referencias

- `docs/domain-glossary.md`
- `docs/sync-strategy.md`
- `docs/conflict-policy.md`
- `docs/firestore-operation-contract.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/editability-policy.md`
- `docs/resource-delta-model.md`
- `docs/decision-log.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
