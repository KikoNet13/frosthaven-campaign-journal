# PolÃ­tica de Timestamps y Orden Estable entre Dispositivos (MVP)

## Metadatos

- `doc_id`: DOC-TIMESTAMP-ORDER-POLICY
- `purpose`: Definir la polÃ­tica MVP de auditorÃ­a temporal y orden estable entre dispositivos (timestamps server-only, reglas de escritura y tuplas canÃ³nicas por lista).
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-10

## Objetivo

Cerrar una decisiÃ³n documental oficial para la auditorÃ­a temporal del MVP y el
orden estable entre dispositivos, de forma compatible con sincronizaciÃ³n,
conflictos, contrato de operaciones por agregado y modelo de recursos vigente.

## Alcance y no alcance

Incluye:

- polÃ­tica de `created_at_utc` / `updated_at_utc` (server-only);
- reglas de escritura de timestamps en create/update/side-effects/hard delete;
- matriz explÃ­cita de orden canÃ³nico por lista (alcance UI + consultas mÃ­nimas
  de `#16`);
- manejo de timestamps pendientes (`serverTimestamp` no confirmado);
- alineaciÃ³n con `#12`, `#16`, `#40` y `docs/domain-glossary.md`.

No incluye:

- tÃ©cnica Firestore exacta para materializar `serverTimestamp`;
- diseÃ±o de queries finales de `#16` (solo reglas de orden y prefijos);
- UX detallada de indicadores de estado provisional;
- cÃ³digo de app.

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

1. Alcance de matriz de orden: listas visibles del MVP + consultas mÃ­nimas de
   `#16`.
1. AuditorÃ­a temporal: `server-only`.
1. `deleted_at_utc`: fuera del MVP.
1. Matriz de orden estable explÃ­cita por lista.
1. Orden canÃ³nico: prefijo de query + normalizaciÃ³n final en cliente.
1. Ãšltimo desempate global: `document_id` lexicogrÃ¡fico ascendente.
1. Sesiones en listas combinadas: activa primero.
1. HistÃ³rico de sesiones: `started_at_utc` descendente.
1. Timeline: orden de dominio (`week_number`, `order_index`) primero; timestamps
   solo como fallback/desempate.
1. Timestamps pendientes: orden canÃ³nico final solo garantizado tras `refresh`.
1. AuditorÃ­a ampliada a `campaign/year/season/week/entry/session`.
1. Forma de auditorÃ­a por entidad: `created_at_utc` + `updated_at_utc` en todas
   las entidades auditadas.
1. `updated_at_utc` cambia en toda escritura persistida, tambiÃ©n derivada.
1. La matriz incluye tambiÃ©n listas con orden de dominio (timestamps `N/A` o
   fallback), para dejar `#16` mÃ¡s cerrada.

## PolÃ­tica de auditorÃ­a temporal (server-only)

### Regla de origen

- `created_at_utc` y `updated_at_utc` se escriben como timestamps de servidor.
- El cliente no persiste timestamps â€œdefinitivosâ€ locales para auditorÃ­a.

### Regla de escritura

1. En creaciÃ³n de documento se escriben `created_at_utc` y `updated_at_utc` en
   la misma operaciÃ³n lÃ³gica.
1. En actualizaciÃ³n se preserva `created_at_utc` y se actualiza
   `updated_at_utc`.
1. Si una operaciÃ³n compuesta/derivada modifica un documento (por ejemplo
   `auto-stop`, recÃ¡lculo o side-effect), ese documento tambiÃ©n actualiza su
   `updated_at_utc`.
1. En hard delete no se usa `deleted_at_utc`; el documento se elimina
   directamente.

## Entidades auditadas y campos por entidad

| entity | created_at_utc | updated_at_utc | deleted_at_utc_mvp | timestamp_fields_adicionales | notas |
| --- | --- | --- | --- | --- | --- |
| `campaign` | SÃ­ | SÃ­ | No | `week_cursor` / `resource_totals` son datos, no timestamps | `updated_at_utc` cambia en provisiÃ³n/extensiÃ³n y cambios persistidos de campaÃ±a |
| `year` | SÃ­ | SÃ­ | No | Ninguno | AuditorÃ­a de documento temporal aunque su mutabilidad sea baja |
| `season` | SÃ­ | SÃ­ | No | Ninguno | AuditorÃ­a de documento temporal aunque su mutabilidad sea baja |
| `week` | SÃ­ | SÃ­ | No | Ninguno | Incluye cierres/reaperturas |
| `entry` | SÃ­ | SÃ­ | No | Ninguno | Incluye cambios de `resource_deltas` y reordenaciÃ³n si el doc cambia |
| `session` | SÃ­ | SÃ­ | No | `started_at_utc`, `ended_at_utc` | `started_at_utc`/`ended_at_utc` modelan el intervalo; auditorÃ­a es aparte |

## Reglas de escritura de timestamps (create/update/side-effects/hard delete)

| familia_operacion | docs_que_crea | docs_que_actualiza | campos_timestamp_en_create | campos_timestamp_en_update | side_effects_actualizan_updated_at | notas |
| --- | --- | --- | --- | --- | --- | --- |
| `Campaign.provision_initial_years` | `campaign` (si aplica), `year`, `season`, `week` | `campaign` | `created_at_utc`, `updated_at_utc` | `updated_at_utc` | SÃ­ | `campaign.updated_at_utc` refleja provisiÃ³n/ajuste de cursor/totales si cambian |
| `Campaign.extend_years_plus_one` | `year`, `season`, `week` | `campaign` | `created_at_utc`, `updated_at_utc` | `updated_at_utc` | SÃ­ | Incluye postcondiciÃ³n de `week_cursor` |
| `Week.*` (`close/reopen/reclose`) | Ninguno | `week` (y `session` si `auto-stop`) | N/A | `updated_at_utc` | SÃ­ | `auto-stop` actualiza `session.updated_at_utc` |
| `Entry.create/update/reorder` | `entry` (create) | `entry` | `created_at_utc`, `updated_at_utc` | `updated_at_utc` | SÃ­ | `reorder` puede afectar mÃºltiples entries; las entries modificadas actualizan `updated_at_utc` |
| `Entry.resource_deltas` (`adjust/set/clear`) | Ninguno | `entry`, `campaign` | N/A | `updated_at_utc` | SÃ­ | `Entry` y `campaign` actualizan `updated_at_utc` si persisten cambios |
| `Entry.delete` | Ninguno | `session` (auto-stop previo, si aplica) | N/A | `updated_at_utc` (en la sesiÃ³n antes de borrar) | SÃ­ | Hard delete de `entry` y `session`; sin `deleted_at_utc` |
| `Session.start/stop/auto_stop/manual_*` | `session` (start/manual_create) | `session` (stop/auto/manual_update) | `created_at_utc`, `updated_at_utc` | `updated_at_utc` | SÃ­ | `started_at_utc`/`ended_at_utc` son campos funcionales del intervalo |

## PolÃ­tica de orden estable (query + cliente)

### Regla general

1. Cada lista define una **tupla canÃ³nica de orden**.
1. La query aplica el prefijo de orden que Firestore puede garantizar.
1. El cliente completa la tupla canÃ³nica y reordena localmente.
1. El Ãºltimo desempate canÃ³nico es `document_id` lexicogrÃ¡fico ascendente.

### Regla de dominio vs timestamp

Cuando exista orden de dominio explÃ­cito (por ejemplo `week_number` u
`order_index`), ese orden es primario. Los timestamps se usan como fallback o
desempate estable, no como reemplazo del orden funcional del dominio.

## Manejo de timestamps pendientes

- El orden canÃ³nico final solo se garantiza con timestamps de servidor ya
  confirmados.
- Antes de confirmaciÃ³n puede existir estado/lista provisional en UI.
- Tras `refresh`, el cliente reaplica la tupla canÃ³nica final.
- Esta polÃ­tica no obliga a ocultar elementos pendientes; solo evita prometer
  estabilidad final antes del `refresh`.

## Matriz de listas y tuplas canÃ³nicas

| logical_list_id | uso_ui_o_lectura | query_order_prefix | client_canonical_tuple | timestamp_role | null_handling | pending_timestamp_behavior | notas |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `year_selector_list` | Selector temporal de aÃ±o (UI) | `year_number ASC` (si aplica) | `(year_number ASC)` | `N/A` | `N/A` | `N/A` | Lista de dominio |
| `season_list_within_year` | NavegaciÃ³n/estructura dentro de aÃ±o | Sin prefijo natural Ãºtil por orden semÃ¡ntico | `(season_rank ASC, season_type ASC)` con `summer=0`, `winter=1` | `N/A` | `N/A` | `N/A` | Orden canÃ³nico fijo `summer -> winter` |
| `week_selector_list` | Selector temporal de semana (UI) | `week_number ASC` | `(week_number ASC)` | `N/A` | `N/A` | `N/A` | Lista de dominio |
| `timeline_week_groups` | Grupos/secciones de week en timeline | `week_number ASC` | `(week_number ASC)` | `N/A` | `N/A` | `N/A` | Compatible con `#16` |
| `week_entries_list` | Lista de entries de una `Week` (panel foco / selector de entry) | `order_index ASC` | `(order_index ASC, created_at_utc ASC, entry_id ASC)` | Fallback/desempate | `N/A` | `created_at_utc` pendiente puede dar orden provisional hasta `refresh` | `updated_at_utc` no se usa para evitar drift visual por ediciones no relacionadas con orden |
| `timeline_entries_flat` | Timeline aplanado multi-week (si `#16` lo define) | Prefijo mÃ¡ximo posible segÃºn query de `#16` | `(week_number ASC, order_index ASC, created_at_utc ASC, entry_id ASC)` | Fallback/desempate | `N/A` | `created_at_utc` pendiente => orden provisional | Lista condicional; `#16` cerrada no la activa en el MVP actual |
| `entry_sessions_combined_list` | Sesiones de una `Entry` (activa + histÃ³rico) | `started_at_utc DESC` | `(is_active DESC, started_at_utc DESC, updated_at_utc DESC, session_id ASC)` | Principal + desempate | `ended_at_utc = null` => `is_active=1` | timestamps pendientes => orden provisional hasta `refresh` | Activa primero por regla de dominio |
| `entry_sessions_history_list` | HistÃ³rico de sesiones (sin activa o filtrando activas) | `started_at_utc DESC` | `(started_at_utc DESC, updated_at_utc DESC, session_id ASC)` | Principal + desempate | `N/A` | timestamps pendientes => orden provisional hasta `refresh` | HistÃ³rico descendente |

## AlineaciÃ³n con #12, #16 y #40

### `#12` (`docs/firestore-operation-contract.md`)

- `#12` sigue definiendo contrato por operaciÃ³n (pre/post/rechazos/atomicidad).
- `#18` define auditorÃ­a temporal y orden estable por lista.
- `#12` debe referenciar este documento y dejar de decir que la polÃ­tica de
  timestamps/desempates estÃ¡ â€œdiferidaâ€.

### `#16` (consultas mÃ­nimas)

- `#16` queda desbloqueada con una matriz de orden explÃ­cita por lista.
- `#16` puede centrarse en inventario de consultas, paginaciÃ³n y coste,
  reutilizando las tuplas canÃ³nicas definidas aquÃ­.
- `#16` adopta `timeline_week_groups` (weeks) y deja `timeline_entries_flat`
  fuera del MVP actual.

### `#40` (modelo de recursos por `Entry`)

- No existe log `ResourceChange` en el MVP activo.
- `#18` no necesita inventariar listas/eventos de `ResourceChange`.
- Los cambios de recursos quedan cubiertos por auditorÃ­a/orden del documento
  `Entry` cuando el contexto de UI lo requiera.

## Casos de aceptaciÃ³n / verificaciÃ³n documental

1. La polÃ­tica elimina `deleted_at_utc` del MVP y documenta hard delete sin
   soft delete.
1. `Campaign`, `Year`, `Season`, `Week`, `Entry` y `Session` quedan con
   `created_at_utc` + `updated_at_utc`.
1. `updated_at_utc` se actualiza tambiÃ©n en side-effects (`auto-stop`,
   recÃ¡lculos, etc.) cuando el documento cambia persistentemente.
1. Las listas de dominio (`year/season/week`) tienen orden canÃ³nico explÃ­cito
   aunque no usen timestamps como criterio principal.
1. El timeline de entries usa orden de dominio primero (`week_number`,
   `order_index`) y timestamps solo como fallback/desempate.
1. La lista combinada de sesiones pone la activa primero y mantiene histÃ³rico
   estable con desempates.
1. Los timestamps pendientes solo garantizan orden provisional hasta `refresh`.
1. `#12`, `#16` y `#40` quedan alineadas sin contradicciones de orden/timestamps.

## Riesgos, lÃ­mites y decisiones diferidas

- La tÃ©cnica exacta para resolver `serverTimestamp` pendiente en la UI queda a
  implementaciÃ³n.
- La forma exacta de Ã­ndices/`orderBy` en Firestore se concreta en `#16` y
  cÃ³digo.
- La paginaciÃ³n real de listas largas (si aplica) se define en `#16`.

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

