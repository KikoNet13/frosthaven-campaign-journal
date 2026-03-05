# Consultas MÃ­nimas para Pantalla Principal (MVP)

## Metadatos

- `doc_id`: DOC-MINIMAL-READ-QUERIES
- `purpose`: Definir el inventario mÃ­nimo de lecturas/consultas para la pantalla principal del MVP (superficies visibles, triggers, orden y lÃ­mites de carga).
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-10

## Objetivo

Cerrar un contrato documental de lecturas mÃ­nimas para la pantalla principal
del MVP que permita implementar la UI con consultas suficientes, orden estable
y lÃ­mites explÃ­citos de coste/latencia, sin adelantar cÃ³digo ni detalles
tÃ©cnicos de Firestore que no pertenecen a esta issue.

## Alcance y no alcance

Incluye:

- inventario de superficies de pantalla y estados relevantes para lecturas;
- consultas mÃ­nimas necesarias por superficie/estado;
- campos mÃ­nimos lÃ³gicos por consulta;
- triggers de carga y refresh (`on-demand`);
- orden/prefijos compatibles con `docs/timestamp-order-policy.md` (Issue `#18`);
- decisiÃ³n explÃ­cita de no paginaciÃ³n en el MVP;
- riesgos de coste/latencia y lÃ­mites aceptados.

No incluye:

- implementaciÃ³n de queries en cÃ³digo;
- Ã­ndices Firestore fÃ­sicos definitivos;
- listeners realtime (excluidos por `docs/sync-strategy.md`, Issue `#7`);
- paginaciÃ³n avanzada;
- rediseÃ±o visual detallado de Figma;
- cambios de modelo de dominio o de operaciones de escritura.

## Entradas y prerrequisitos

- `docs/sync-strategy.md` (Issue `#7`)
- `docs/campaign-temporal-controls.md` (Issue `#9`)
- `docs/campaign-temporal-initialization.md` (Issue `#13`)
- `docs/firestore-operation-contract.md` (Issue `#12`)
- `docs/editability-policy.md` (Issue `#37`)
- `docs/active-session-flow.md` (Issue `#14`)
- `docs/resource-delta-model.md` (Issue `#40`)
- `docs/resource-validation-recalculation.md` (Issue `#15`)
- `docs/timestamp-order-policy.md` (Issue `#18`)
- `docs/domain-glossary.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- Figma compartido por Kiko (captura de distribuciÃ³n de frames usada como canon
  de layout para `#16`; referencia visual fuera del repo).

## Canon de layout/superficies para `#16` (Figma + contratos oficiales)

### Regla de precedencia para esta issue

1. **Layout/superficies visibles**:
   - manda el diseÃ±o de Figma compartido por Kiko para la distribuciÃ³n de
     frames de la pantalla principal (referencia visual de esta sesiÃ³n).
1. **Reglas de dominio/flujo/orden**:
   - mandan los documentos oficiales ya cerrados (`#9`, `#12`, `#14`, `#15`,
     `#18`, `#37`, `#40`).
1. `tdd.md` (retirado el 2026-03-01):
   - se trata como legado y referencia histÃ³rica;
   - **no** es canon de layout para `#16`.

### Decisiones de layout/lecturas cerradas en `#16`

1. El flujo de lectura se modela para la **pantalla principal** (no solo
   â€œtimeline y panel de focoâ€ en sentido legacy).
1. El timeline del MVP se basa en **weeks** (no se activa un timeline plano de
   entries multi-week en esta issue).
1. La carga temporal visible se resuelve sobre el **aÃ±o seleccionado completo**
   (sin ventana de weeks).
1. Las sesiones de una `Entry` se cargan al **seleccionar la `Entry`**.
1. No hay paginaciÃ³n en el MVP para years/weeks/entries/sesiones.
1. Estado inicial de pantalla:
  - barra superior en el aÃ±o de `current week` (semana actual derivada);
   - sin `Week` seleccionada;
   - sin `Entry` seleccionada;
   - sin bloque de `Entry` visible.

## Superficies de lectura y estados de pantalla

### Tabla 1 â€” Superficies/estados de pantalla (`I16-S1`)

| `surface_id` | `descripcion` | `visible_en_estado` | `datos_necesarios` | `notas` |
| --- | --- | --- | --- | --- |
| `top_year_selector` | Barra superior con aÃ±o actual seleccionado, navegaciÃ³n prev/next y `+` de extensiÃ³n | Todos | aÃ±os provisionados, aÃ±o seleccionado, condiciÃ³n de Ãºltimo aÃ±o | `+` depende del Ãºltimo aÃ±o provisionado (`#9`) |
| `top_week_selector` | Tira de semanas del aÃ±o seleccionado (navegaciÃ³n/foco temporal) | Todos | weeks del aÃ±o seleccionado (`week_number`, `status`), marcador `current week` (semana actual derivada) | Seleccionar week no cambia la semana actual derivada (`#9`) |
| `top_entry_selector_tabs` | Selector de `Entry` de la week seleccionada (tabs) | `week_selected_no_entry`, `entry_selected_*` | entries de la week seleccionada ordenadas | Puede mostrar estado vacÃ­o/acciÃ³n de creaciÃ³n si no hay entries |
| `focus_panel_week_state` | Panel central en modo `Week` (semana seleccionada y estado) | `week_selected_no_entry` | `Week` seleccionada (`status`) | Consume datos ya presentes en lecturas de weeks |
| `focus_panel_entry_state` | Panel central en modo `Entry` (datos de entry, recursos, bloque sesiÃ³n) | `entry_selected_*` | `Entry` seleccionada + sesiones de esa entry | `total jugado` y desplegable de sesiones dependen de lectura de `sessions` |
| `bottom_totals_bar` | Barra inferior con totales globales y resumen de activo | Todos | `campaign.resource_totals`, resumen de sesiÃ³n activa, label del activo si aplica | El detalle visual no cambia las lecturas mÃ­nimas |
| `active_session_indicator_summary` | Indicadores de foco vs activo / estado de sesiÃ³n global | Todos (condicional si hay activa) | sesiÃ³n activa global + owner (`Entry`) si no coincide con la seleccionada | Alineado con separaciÃ³n foco/activo de `#14` |

Estados de pantalla del MVP (canon para lecturas):

- `screen_open_no_selection`
- `week_selected_no_entry`
- `entry_selected_no_active_session`
- `entry_selected_active_session_here`
- `entry_selected_active_session_other_entry`

## Inventario de consultas mÃ­nimas

### Tabla 2 â€” Inventario de consultas mÃ­nimas (`I16-S2`)

| `query_id` | `superficies_que_alimenta` | `path_o_scope` | `filtros` | `query_order_prefix` | `client_canonical_order` (ref `#18`) | `trigger_de_carga` | `trigger_de_refresh` | `paginacion_mvp` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Q1 campaign_main_doc` | `bottom_totals_bar`, `active_session_indicator_summary` (+ transiciÃ³n temporal) | `campaigns/01` (doc) | N/A | N/A | N/A | abrir pantalla | refresh manual; post-escrituras que cambian `campaign` | No aplica | CanÃ³nico: `resource_totals`; transiciÃ³n: implementaciÃ³n actual aÃºn usa `week_cursor` |
| `Q2 years_list` | `top_year_selector` | `campaigns/01/years` | N/A | `year_number ASC` | `(year_number ASC)` | abrir pantalla | refresh manual; extensiÃ³n `+1` aÃ±o | No | Volumen bajo |
| `Q3 weeks_selected_year_summer` | `top_week_selector`, `focus_panel_week_state` | `.../years/{selected_year}/seasons/summer/weeks` | N/A | `week_number ASC` | `(week_number ASC)` | abrir pantalla (aÃ±o inicial); cambio de aÃ±o | refresh manual; cambios de `Week` del aÃ±o visible; provisiÃ³n/extensiÃ³n que afecte aÃ±o visible | No | 10 weeks por estaciÃ³n |
| `Q4 weeks_selected_year_winter` | `top_week_selector`, `focus_panel_week_state` | `.../years/{selected_year}/seasons/winter/weeks` | N/A | `week_number ASC` | `(week_number ASC)` | abrir pantalla (aÃ±o inicial); cambio de aÃ±o | refresh manual; cambios de `Week` del aÃ±o visible; provisiÃ³n/extensiÃ³n que afecte aÃ±o visible | No | Se fusiona en cliente con Q3 por `week_number` |
| `Q5 entries_selected_week` | `top_entry_selector_tabs`, `focus_panel_entry_state`, `focus_panel_week_state` | `.../weeks/{selected_week}/entries` | N/A | `order_index ASC` | `(order_index ASC, created_at_utc ASC, entry_id ASC)` | selecciÃ³n de `Week` | refresh manual (si hay week seleccionada); post `Entry.*`; cambios de recursos que afecten render de `Entry` | No | TambiÃ©n sirve para estado vacÃ­o de week |
| `Q6 active_session_global` | `active_session_indicator_summary`, `bottom_totals_bar` | `collection group sessions` | `ended_at_utc == null`, `limit 1` | (segÃºn capacidad de query; no crÃ­tico para `limit 1`) | N/A (single result) | abrir pantalla | refresh manual; post `Session.*`; `Week.close/reclose`; `Entry.delete` con posible `auto-stop` | No aplica | Invariante `0..1` activa global |
| `Q7 active_entry_doc_if_needed` | `active_session_indicator_summary`, `bottom_totals_bar` | doc `Entry` owner de Q6 (derivado por ruta) | condicional | N/A | N/A | tras Q6 si aplica | refresh manual (si aplica) | No aplica | Solo si activa != `selected_entry` o se necesita label del activo |
| `Q8 sessions_selected_entry_combined` | `focus_panel_entry_state`, `active_session_indicator_summary` | `.../entries/{selected_entry}/sessions` | N/A | `started_at_utc DESC` | `(is_active DESC, started_at_utc DESC, updated_at_utc DESC, session_id ASC)` | selecciÃ³n de `Entry` | refresh manual (si hay `selected_entry`); post `Session.*` que afecten esa entry | No | Alimenta total jugado + lista desplegable |

### DefiniciÃ³n operativa de cada consulta (resumen normativo)

#### Q1 â€” `campaign_main_doc`

- **Campos lÃ³gicos mÃ­nimos**:
  - `resource_totals`
  - `updated_at_utc` (y `created_at_utc` opcional tÃ©cnico)
- **Uso**:
  - barra de totales
  - estado general persistido de campaÃ±a
  - **transiciÃ³n**: la implementaciÃ³n actual todavÃ­a puede leer `week_cursor`
    hasta la migraciÃ³n del modelo temporal (`#76` -> `#81`)

#### Q2 â€” `years_list`

- **Campos lÃ³gicos mÃ­nimos**:
  - `year_number`
  - `created_at_utc`, `updated_at_utc` (opcionales tÃ©cnicos)
- **Uso**:
  - selector de aÃ±o y validaciÃ³n de lÃ­mites prev/next
  - disponibilidad de `+` cuando el aÃ±o seleccionado es el Ãºltimo provisionado

#### Q3/Q4 â€” `weeks_selected_year_{summer|winter}`

- **Campos lÃ³gicos mÃ­nimos**:
  - `week_number`
  - `status`
  - `updated_at_utc` (opcional tÃ©cnico)
- **Uso**:
  - tira de weeks del aÃ±o seleccionado
  - datos de panel `Week` sin query extra cuando se selecciona una week

#### Q5 â€” `entries_selected_week`

- **Campos lÃ³gicos mÃ­nimos**:
  - `entry_id` (doc id)
  - `type`
  - `scenario_ref` (si aplica)
  - `order_index`
  - `resource_deltas`
  - `created_at_utc`, `updated_at_utc`
- **Uso**:
  - tabs/selector de entries de la week
  - panel de foco en modo `Entry`
  - estado vacÃ­o si la week no tiene entries

#### Q6 â€” `active_session_global`

- **Campos lÃ³gicos mÃ­nimos**:
  - `session_id` (doc id)
  - `started_at_utc`
  - `ended_at_utc`
  - `created_at_utc`, `updated_at_utc`
  - ruta del documento (para derivar owner `Entry`/`Week`)
- **Uso**:
  - resumen de activo global
  - barra inferior (tiempo/activo)
  - separaciÃ³n foco vs activo (`#14`)

#### Q7 â€” `active_entry_doc_if_needed` (condicional)

- **Campos lÃ³gicos mÃ­nimos**:
  - `type`
  - `scenario_ref`
  - `updated_at_utc` (opcional tÃ©cnico)
- **Uso**:
  - label/identificador del activo cuando la sesiÃ³n activa pertenece a otra
    `Entry` distinta de la seleccionada

#### Q8 â€” `sessions_selected_entry_combined`

- **Campos lÃ³gicos mÃ­nimos**:
  - `started_at_utc`
  - `ended_at_utc`
  - `created_at_utc`
  - `updated_at_utc`
- **Uso**:
  - total jugado (calculado en cliente)
  - lista de sesiones desplegable de la `Entry` seleccionada
  - estado activo/histÃ³rico de esa `Entry`

## Campos mÃ­nimos lÃ³gicos por consulta

### Tabla 3 â€” Campos mÃ­nimos lÃ³gicos por consulta (`I16-S2`)

| `query_id` | `entity` | `campos_minimos_logicos` | `campos_para_orden` | `campos_para_render` | `campos_para_estado` | `notas` |
| --- | --- | --- | --- | --- | --- | --- |
| `Q1 campaign_main_doc` | `campaign` | `resource_totals`, `updated_at_utc` | N/A | `resource_totals` | `updated_at_utc` | `week_cursor` solo en implementaciÃ³n transitoria previa a `#81` |
| `Q2 years_list` | `year` | `year_number` | `year_number` | `year_number` | `updated_at_utc` opcional | AuditorÃ­a no es primaria de UI |
| `Q3 weeks_selected_year_summer` | `week` | `week_number`, `status` | `week_number` | `week_number`, `status` | `status`, `updated_at_utc` | Parte `summer` del aÃ±o |
| `Q4 weeks_selected_year_winter` | `week` | `week_number`, `status` | `week_number` | `week_number`, `status` | `status`, `updated_at_utc` | Parte `winter` del aÃ±o |
| `Q5 entries_selected_week` | `entry` | `type`, `scenario_ref`, `order_index`, `resource_deltas`, `created_at_utc`, `updated_at_utc` | `order_index`, `created_at_utc`, `entry_id` | `type`, `scenario_ref`, `resource_deltas` | `updated_at_utc`, `order_index` | `entry_id` viene del doc id |
| `Q6 active_session_global` | `session` | `started_at_utc`, `ended_at_utc`, `created_at_utc`, `updated_at_utc` + ruta | `N/A (single)` | `started_at_utc`, `ended_at_utc` | `ended_at_utc`, `updated_at_utc` | `limit 1` por invariante |
| `Q7 active_entry_doc_if_needed` | `entry` | `type`, `scenario_ref` | N/A | `type`, `scenario_ref` | `updated_at_utc` opcional | Solo si activa != seleccionada |
| `Q8 sessions_selected_entry_combined` | `session` | `started_at_utc`, `ended_at_utc`, `created_at_utc`, `updated_at_utc` | `started_at_utc`, `updated_at_utc`, `session_id` | `started_at_utc`, `ended_at_utc` | `ended_at_utc`, `updated_at_utc` | Orden canÃ³nico final en cliente segÃºn `#18` |

## Orden estable y compatibilidad con `#18`

1. `#16` **no redefine** la polÃ­tica de desempate ni timestamps:
   reutiliza `docs/timestamp-order-policy.md`.
1. AplicaciÃ³n directa de `#18` en `#16`:
   - `year_selector_list` -> Q2
   - `week_selector_list` / `timeline_week_groups` -> Q3 + Q4 (merge cliente)
   - `week_entries_list` -> Q5
   - `entry_sessions_combined_list` -> Q8
1. `timeline_entries_flat`:
   - permanece documentado en `#18` como opciÃ³n condicional;
   - **no se activa** en el MVP actual de `#16`.
1. Timestamps pendientes (`serverTimestamp`) mantienen orden provisional hasta
   `refresh`, segÃºn `#18`.

## Triggers de carga y refresh (`on-demand`)

### Estado inicial de pantalla (decisiÃ³n cerrada)

- `selected_year` inicial = aÃ±o de `current week` (semana actual derivada)
- `selected_week` inicial = `none`
- `selected_entry` inicial = `none`

Notas de implementaciÃ³n posteriores (`#53+`):

- La UI puede separar **navegaciÃ³n** (`selected_year` / `selected_week`) de la
  **entry visible en visor** (sticky).
- En este documento, `selected_entry` se usa como shorthand de la entry cuyo
  detalle/sesiones se muestran en visor cuando existe; cambiar de year/week de
  navegaciÃ³n no obliga a limpiar ese visor.

### Consecuencia de lecturas iniciales

- **Cargar al abrir pantalla**: Q1 + Q2 + Q3 + Q4 + Q6
- **No cargar hasta selecciÃ³n**: Q5 + Q7 + Q8

### Tabla 4 â€” Refresco por tipo de evento (`I16-S3`)

| `evento_ui_o_operacion` | `queries_a_refrescar` | `motivo` | `requiere_refresh_manual` | `notas` |
| --- | --- | --- | --- | --- |
| `open_main_screen` | Q1, Q2, Q3, Q4, Q6 | Estado inicial mÃ­nimo visible | No | AÃ±o inicial derivado de la semana actual (transiciÃ³n: hoy puede venir de `week_cursor`) |
| `ui.manual_refresh` | Q1, Q2, Q3, Q4, Q6 + (Q5/Q7/Q8 si hay selecciÃ³n/activa aplicable) | `on-demand refresh` global del contexto visible | SÃ­ (trigger del usuario) | Sin listeners realtime (`#7`) |
| `ui.select_year` | Q3, Q4 (resetea navegaciÃ³n de `Week`) | Cambia el conjunto de weeks visibles | No | Puede mantenerse una entry en visor sticky; Q5/Q8 no cargan hasta nueva selecciÃ³n de entry |
| `ui.select_week` | Q5 | Cargar entries de la week seleccionada | No | No cambia la semana actual derivada ni obliga a limpiar la entry en visor sticky |
| `ui.select_entry` | Q8 (+ Q7 solo si sigue activo global en otra entry y la UI lo necesita) | Cargar sesiones de la entry seleccionada para el visor | No | Q5 ya aporta datos base de la entry |
| `Week.close/reopen/reclose` | Q1 (si cambia estado de campaÃ±a / transiciÃ³n temporal), Q3/Q4 (aÃ±o visible), Q6 (si hubo `auto-stop`) | Reflejar estado de week, semana actual derivada y sesiÃ³n activa | No (post-escritura local) | Si la week afectada no estÃ¡ en aÃ±o visible, Q3/Q4 puede diferirse a refresh manual |
| `Campaign.extend_years_plus_one` | Q1, Q2, Q3/Q4 si el aÃ±o visible queda afectado | Reflejar nuevo aÃ±o / estado de campaÃ±a | No (post-escritura local) | `+` vive en selector de aÃ±o (`#9`) |
| `Entry.create/update/delete/reorder` sobre `selected_week` | Q5 (+ Q8 si afecta la entry en visor) | Actualizar tabs/lista y panel de entry | No (post-escritura local) | `Entry.delete` puede requerir tambiÃ©n Q6 si habÃ­a activa |
| `Entry.adjust/set/clear_resource_delta` sobre la entry en visor | Q1, Q5 | Totales globales + `resource_deltas` de entry | No (post-escritura local) | Reglas de recursos en `#15` |
| `Session.start/stop/auto-stop/manual_*` | Q6, Q8 (si afecta la entry en visor), Q7 (si aplica) | Reflejar activo global y sesiones de la entry | No (post-escritura local) | RecuperaciÃ³n por conflicto sigue `#14/#8` |

### Regla de refresh post-escritura (MVP)

1. Tras una escritura local confirmada, el cliente refresca **solo las queries
   del Ã¡mbito afectado** (no recarga global indiscriminada por defecto).
1. Ante `conflicto`, la recuperaciÃ³n sigue el patrÃ³n `refresh` manual +
   reintento (`#8`, `#14`, `#15`, `#12`).

## PaginaciÃ³n y lÃ­mites del MVP

### DecisiÃ³n cerrada

- **No hay paginaciÃ³n en el MVP** para:
  - years
  - weeks del aÃ±o seleccionado
  - entries de la week seleccionada
  - sesiones de la entry seleccionada

### JustificaciÃ³n documental

1. `years_list` y `weeks_selected_year_*` tienen volumen pequeÃ±o y acotado.
1. `entries_selected_week` solo se carga tras seleccionar week.
1. `sessions_selected_entry_combined` solo se carga tras seleccionar entry y el
   volumen esperado es bajo (normalmente ~1 sesiÃ³n por entry).
1. La UI puede plegar sesiones sin exigir paginaciÃ³n.

### LÃ­mite explÃ­cito aceptado

Si el histÃ³rico de sesiones de una `Entry` crece de forma anÃ³mala o el nÃºmero
de entries por week se vuelve alto para el dispositivo objetivo, la paginaciÃ³n
se tratarÃ¡ como ampliaciÃ³n posterior (no bloquea `#16`).

## Riesgos de coste/latencia y mitigaciones

### Riesgos principales

1. **Sobrecarga por recargar de mÃ¡s tras escrituras**
   - Riesgo: degradar UX si se recarga toda la pantalla tras cada operaciÃ³n.
   - MitigaciÃ³n: refresco por Ã¡mbito (tabla 4) y refresh manual para conflictos.

1. **Q3+Q4 incluyen solo estado (`status`)**
   - Riesgo: bajo; se mantiene lectura mínima de week para selector temporal.
   - MitigaciÃ³n: aceptar el coste por simplicidad del MVP; evita query extra
     para panel `Week`.

1. **Dependencia de `collection group` para Q6**
   - Riesgo: Ã­ndice/consulta no disponible si se implementa sin soporte.
   - MitigaciÃ³n: documentar la dependencia en `#16`; si la implementaciÃ³n no la
     usa, deberÃ¡ ofrecer una alternativa equivalente sin cambiar el contrato
     observable.

1. **Figma incompleto (bloque central / barra inferior)**
   - Riesgo: lecturas faltantes si luego aparecen nuevos datos requeridos.
   - MitigaciÃ³n: cerrar `#16` con supuestos explÃ­citos y limitar el contrato a
     datos ya cerrados por dominio/flujo.

### Supuestos de lectura por superficies incompletas (obligatorios)

1. **Bloque central**
   - modo `Week`: consume `status` desde Q3/Q4 (sin query extra)
   - modo `Entry`: consume `Entry` desde Q5 y sesiones desde Q8
1. **Barra inferior**
   - requiere Q1 (`resource_totals`) + Q6 (activo global) + Q7 (label del
     activo si activa != seleccionada)
   - el detalle visual no introduce nuevas entidades/queries en `#16`

## Casos de aceptaciÃ³n / verificaciÃ³n documental

1. Al abrir pantalla:
   - la barra superior se sitÃºa en el aÃ±o de `current week`;
   - no hay `Week` ni `Entry` seleccionada;
   - se cargan Q1 + Q2 + Q3 + Q4 + Q6, pero no Q5/Q7/Q8.
1. Seleccionar una week carga Q5 (`entries_selected_week`) y no dispara Q8
   hasta seleccionar una nueva `Entry` para el visor.
1. Seleccionar una entry carga Q8 (`sessions_selected_entry_combined`) para
   total jugado y desplegable de sesiones.
1. La navegaciÃ³n (`selected_year` / `selected_week`) puede cambiar sin limpiar
   la entry visible en visor (sticky), y eso no cambia quÃ© evento dispara Q8:
   solo la selecciÃ³n de una nueva `Entry`.
1. La UI puede distinguir foco vs activo con Q6 (+ Q7 si aplica), alineado con
   `#14`.
1. Cambiar de aÃ±o recarga weeks del aÃ±o seleccionado completo (Q3+Q4), sin
   paginaciÃ³n por ventana.
1. `#16` reutiliza las tuplas canÃ³nicas de `#18` y no redefine desempates.
1. `timeline_entries_flat` queda explÃ­citamente no activado en el MVP actual.
1. La ausencia de paginaciÃ³n queda documentada como decisiÃ³n explÃ­cita con
   lÃ­mites aceptados.

## Riesgos, lÃ­mites y decisiones diferidas

- La implementaciÃ³n concreta de queries/Ã­ndices Firestore queda fuera de esta
  issue.
- La matriz de edge cases de lecturas crÃ­ticas y refresh/sync se documenta en
  `docs/concurrency-sync-edge-case-matrix.md` (Issue `#17`) y reutiliza este
  inventario como base.
- La paginaciÃ³n real (si se necesitara por volumen) se difiere a una ampliaciÃ³n
  posterior.
- El Figma usado como canon de layout para `#16` no estÃ¡ archivado aÃºn en el
  repo; se recomienda incorporar referencia persistente en una issue/doco de UI
  futura.

## Referencias

- `AGENTS.md`
- `docs/system-map.md`
- `docs/decision-log.md`
- `docs/domain-glossary.md`
- `docs/sync-strategy.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/firestore-operation-contract.md`
- `docs/editability-policy.md`
- `docs/active-session-flow.md`
- `docs/resource-delta-model.md`
- `docs/resource-validation-recalculation.md`
- `docs/timestamp-order-policy.md`
- `docs/concurrency-sync-edge-case-matrix.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `tdd.md` (retirado el 2026-03-01) (legado, no canÃ³nico para layout de `#16`)
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/7`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/9`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`



