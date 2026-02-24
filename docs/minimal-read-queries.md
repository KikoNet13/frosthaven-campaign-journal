# Consultas Mínimas para Pantalla Principal (MVP)

## Metadatos

- `doc_id`: DOC-MINIMAL-READ-QUERIES
- `purpose`: Definir el inventario mínimo de lecturas/consultas para la pantalla principal del MVP (superficies visibles, triggers, orden y límites de carga).
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar un contrato documental de lecturas mínimas para la pantalla principal
del MVP que permita implementar la UI con consultas suficientes, orden estable
y límites explícitos de coste/latencia, sin adelantar código ni detalles
técnicos de Firestore que no pertenecen a esta issue.

## Alcance y no alcance

Incluye:

- inventario de superficies de pantalla y estados relevantes para lecturas;
- consultas mínimas necesarias por superficie/estado;
- campos mínimos lógicos por consulta;
- triggers de carga y refresh (`on-demand`);
- orden/prefijos compatibles con `docs/timestamp-order-policy.md` (Issue `#18`);
- decisión explícita de no paginación en el MVP;
- riesgos de coste/latencia y límites aceptados.

No incluye:

- implementación de queries en código;
- índices Firestore físicos definitivos;
- listeners realtime (excluidos por `docs/sync-strategy.md`, Issue `#7`);
- paginación avanzada;
- rediseño visual detallado de Figma;
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
- Figma compartido por Kiko (captura de distribución de frames usada como canon
  de layout para `#16`; referencia visual fuera del repo).

## Canon de layout/superficies para `#16` (Figma + contratos oficiales)

### Regla de precedencia para esta issue

1. **Layout/superficies visibles**:
   - manda el diseño de Figma compartido por Kiko para la distribución de
     frames de la pantalla principal (referencia visual de esta sesión).
1. **Reglas de dominio/flujo/orden**:
   - mandan los documentos oficiales ya cerrados (`#9`, `#12`, `#14`, `#15`,
     `#18`, `#37`, `#40`).
1. `tdd.md`:
   - se trata como legado y referencia histórica;
   - **no** es canon de layout para `#16`.

### Decisiones de layout/lecturas cerradas en `#16`

1. El flujo de lectura se modela para la **pantalla principal** (no solo
   “timeline y panel de foco” en sentido legacy).
1. El timeline del MVP se basa en **weeks** (no se activa un timeline plano de
   entries multi-week en esta issue).
1. La carga temporal visible se resuelve sobre el **año seleccionado completo**
   (sin ventana de weeks).
1. Las sesiones de una `Entry` se cargan al **seleccionar la `Entry`**.
1. No hay paginación en el MVP para years/weeks/entries/sesiones.
1. Estado inicial de pantalla:
   - barra superior en el año de `current week` (`week_cursor` derivado);
   - sin `Week` seleccionada;
   - sin `Entry` seleccionada;
   - sin bloque de `Entry` visible.

## Superficies de lectura y estados de pantalla

### Tabla 1 — Superficies/estados de pantalla (`I16-S1`)

| `surface_id` | `descripcion` | `visible_en_estado` | `datos_necesarios` | `notas` |
| --- | --- | --- | --- | --- |
| `top_year_selector` | Barra superior con año actual seleccionado, navegación prev/next y `+` de extensión | Todos | años provisionados, año seleccionado, condición de último año | `+` depende del último año provisionado (`#9`) |
| `top_week_selector` | Tira de semanas del año seleccionado (navegación/foco temporal) | Todos | weeks del año seleccionado (`week_number`, `status`), marcador `current week` | Seleccionar week no cambia `week_cursor` (`#9`) |
| `top_entry_selector_tabs` | Selector de `Entry` de la week seleccionada (tabs) | `week_selected_no_entry`, `entry_selected_*` | entries de la week seleccionada ordenadas | Puede mostrar estado vacío/acción de creación si no hay entries |
| `focus_panel_week_state` | Panel central en modo `Week` (semana seleccionada, notas, estado) | `week_selected_no_entry` | `Week` seleccionada (`status`, `notes`) | Consume datos ya presentes en lecturas de weeks |
| `focus_panel_entry_state` | Panel central en modo `Entry` (datos de entry, recursos, bloque sesión) | `entry_selected_*` | `Entry` seleccionada + sesiones de esa entry | `total jugado` y desplegable de sesiones dependen de lectura de `sessions` |
| `bottom_totals_bar` | Barra inferior con totales globales y resumen de activo | Todos | `campaign.resource_totals`, resumen de sesión activa, label del activo si aplica | El detalle visual no cambia las lecturas mínimas |
| `active_session_indicator_summary` | Indicadores de foco vs activo / estado de sesión global | Todos (condicional si hay activa) | sesión activa global + owner (`Entry`) si no coincide con la seleccionada | Alineado con separación foco/activo de `#14` |

Estados de pantalla del MVP (canon para lecturas):

- `screen_open_no_selection`
- `week_selected_no_entry`
- `entry_selected_no_active_session`
- `entry_selected_active_session_here`
- `entry_selected_active_session_other_entry`

## Inventario de consultas mínimas

### Tabla 2 — Inventario de consultas mínimas (`I16-S2`)

| `query_id` | `superficies_que_alimenta` | `path_o_scope` | `filtros` | `query_order_prefix` | `client_canonical_order` (ref `#18`) | `trigger_de_carga` | `trigger_de_refresh` | `paginacion_mvp` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `Q1 campaign_main_doc` | `top_week_selector`, `bottom_totals_bar`, `active_session_indicator_summary` | `campaigns/01` (doc) | N/A | N/A | N/A | abrir pantalla | refresh manual; post-escrituras que cambian `campaign` | No aplica | Fuente de `week_cursor` y `resource_totals` |
| `Q2 years_list` | `top_year_selector` | `campaigns/01/years` | N/A | `year_number ASC` | `(year_number ASC)` | abrir pantalla | refresh manual; extensión `+1` año | No | Volumen bajo |
| `Q3 weeks_selected_year_summer` | `top_week_selector`, `focus_panel_week_state` | `.../years/{selected_year}/seasons/summer/weeks` | N/A | `week_number ASC` | `(week_number ASC)` | abrir pantalla (año inicial); cambio de año | refresh manual; cambios de `Week` del año visible; provisión/extensión que afecte año visible | No | 10 weeks por estación |
| `Q4 weeks_selected_year_winter` | `top_week_selector`, `focus_panel_week_state` | `.../years/{selected_year}/seasons/winter/weeks` | N/A | `week_number ASC` | `(week_number ASC)` | abrir pantalla (año inicial); cambio de año | refresh manual; cambios de `Week` del año visible; provisión/extensión que afecte año visible | No | Se fusiona en cliente con Q3 por `week_number` |
| `Q5 entries_selected_week` | `top_entry_selector_tabs`, `focus_panel_entry_state`, `focus_panel_week_state` | `.../weeks/{selected_week}/entries` | N/A | `order_index ASC` | `(order_index ASC, created_at_utc ASC, entry_id ASC)` | selección de `Week` | refresh manual (si hay week seleccionada); post `Entry.*`; cambios de recursos que afecten render de `Entry` | No | También sirve para estado vacío de week |
| `Q6 active_session_global` | `active_session_indicator_summary`, `bottom_totals_bar` | `collection group sessions` | `ended_at_utc == null`, `limit 1` | (según capacidad de query; no crítico para `limit 1`) | N/A (single result) | abrir pantalla | refresh manual; post `Session.*`; `Week.close/reclose`; `Entry.delete` con posible `auto-stop` | No aplica | Invariante `0..1` activa global |
| `Q7 active_entry_doc_if_needed` | `active_session_indicator_summary`, `bottom_totals_bar` | doc `Entry` owner de Q6 (derivado por ruta) | condicional | N/A | N/A | tras Q6 si aplica | refresh manual (si aplica) | No aplica | Solo si activa != `selected_entry` o se necesita label del activo |
| `Q8 sessions_selected_entry_combined` | `focus_panel_entry_state`, `active_session_indicator_summary` | `.../entries/{selected_entry}/sessions` | N/A | `started_at_utc DESC` | `(is_active DESC, started_at_utc DESC, updated_at_utc DESC, session_id ASC)` | selección de `Entry` | refresh manual (si hay `selected_entry`); post `Session.*` que afecten esa entry | No | Alimenta total jugado + lista desplegable |

### Definición operativa de cada consulta (resumen normativo)

#### Q1 — `campaign_main_doc`

- **Campos lógicos mínimos**:
  - `week_cursor`
  - `resource_totals`
  - `updated_at_utc` (y `created_at_utc` opcional técnico)
- **Uso**:
  - marcador `current week` (vía `week_cursor`)
  - barra de totales
  - estado general persistido de campaña

#### Q2 — `years_list`

- **Campos lógicos mínimos**:
  - `year_number`
  - `created_at_utc`, `updated_at_utc` (opcionales técnicos)
- **Uso**:
  - selector de año y validación de límites prev/next
  - disponibilidad de `+` cuando el año seleccionado es el último provisionado

#### Q3/Q4 — `weeks_selected_year_{summer|winter}`

- **Campos lógicos mínimos**:
  - `week_number`
  - `status`
  - `notes`
  - `updated_at_utc` (opcional técnico)
- **Uso**:
  - tira de weeks del año seleccionado
  - datos de panel `Week` sin query extra cuando se selecciona una week

#### Q5 — `entries_selected_week`

- **Campos lógicos mínimos**:
  - `entry_id` (doc id)
  - `type`
  - `scenario_ref` (si aplica)
  - `order_index`
  - `resource_deltas`
  - `created_at_utc`, `updated_at_utc`
- **Uso**:
  - tabs/selector de entries de la week
  - panel de foco en modo `Entry`
  - estado vacío si la week no tiene entries

#### Q6 — `active_session_global`

- **Campos lógicos mínimos**:
  - `session_id` (doc id)
  - `started_at_utc`
  - `ended_at_utc`
  - `created_at_utc`, `updated_at_utc`
  - ruta del documento (para derivar owner `Entry`/`Week`)
- **Uso**:
  - resumen de activo global
  - barra inferior (tiempo/activo)
  - separación foco vs activo (`#14`)

#### Q7 — `active_entry_doc_if_needed` (condicional)

- **Campos lógicos mínimos**:
  - `type`
  - `scenario_ref`
  - `updated_at_utc` (opcional técnico)
- **Uso**:
  - label/identificador del activo cuando la sesión activa pertenece a otra
    `Entry` distinta de la seleccionada

#### Q8 — `sessions_selected_entry_combined`

- **Campos lógicos mínimos**:
  - `started_at_utc`
  - `ended_at_utc`
  - `created_at_utc`
  - `updated_at_utc`
- **Uso**:
  - total jugado (calculado en cliente)
  - lista de sesiones desplegable de la `Entry` seleccionada
  - estado activo/histórico de esa `Entry`

## Campos mínimos lógicos por consulta

### Tabla 3 — Campos mínimos lógicos por consulta (`I16-S2`)

| `query_id` | `entity` | `campos_minimos_logicos` | `campos_para_orden` | `campos_para_render` | `campos_para_estado` | `notas` |
| --- | --- | --- | --- | --- | --- | --- |
| `Q1 campaign_main_doc` | `campaign` | `week_cursor`, `resource_totals`, `updated_at_utc` | N/A | `resource_totals`, `week_cursor` | `week_cursor`, `updated_at_utc` | `created_at_utc` opcional técnico |
| `Q2 years_list` | `year` | `year_number` | `year_number` | `year_number` | `updated_at_utc` opcional | Auditoría no es primaria de UI |
| `Q3 weeks_selected_year_summer` | `week` | `week_number`, `status`, `notes` | `week_number` | `week_number`, `status`, `notes` | `status`, `updated_at_utc` | Parte `summer` del año |
| `Q4 weeks_selected_year_winter` | `week` | `week_number`, `status`, `notes` | `week_number` | `week_number`, `status`, `notes` | `status`, `updated_at_utc` | Parte `winter` del año |
| `Q5 entries_selected_week` | `entry` | `type`, `scenario_ref`, `order_index`, `resource_deltas`, `created_at_utc`, `updated_at_utc` | `order_index`, `created_at_utc`, `entry_id` | `type`, `scenario_ref`, `resource_deltas` | `updated_at_utc`, `order_index` | `entry_id` viene del doc id |
| `Q6 active_session_global` | `session` | `started_at_utc`, `ended_at_utc`, `created_at_utc`, `updated_at_utc` + ruta | `N/A (single)` | `started_at_utc`, `ended_at_utc` | `ended_at_utc`, `updated_at_utc` | `limit 1` por invariante |
| `Q7 active_entry_doc_if_needed` | `entry` | `type`, `scenario_ref` | N/A | `type`, `scenario_ref` | `updated_at_utc` opcional | Solo si activa != seleccionada |
| `Q8 sessions_selected_entry_combined` | `session` | `started_at_utc`, `ended_at_utc`, `created_at_utc`, `updated_at_utc` | `started_at_utc`, `updated_at_utc`, `session_id` | `started_at_utc`, `ended_at_utc` | `ended_at_utc`, `updated_at_utc` | Orden canónico final en cliente según `#18` |

## Orden estable y compatibilidad con `#18`

1. `#16` **no redefine** la política de desempate ni timestamps:
   reutiliza `docs/timestamp-order-policy.md`.
1. Aplicación directa de `#18` en `#16`:
   - `year_selector_list` -> Q2
   - `week_selector_list` / `timeline_week_groups` -> Q3 + Q4 (merge cliente)
   - `week_entries_list` -> Q5
   - `entry_sessions_combined_list` -> Q8
1. `timeline_entries_flat`:
   - permanece documentado en `#18` como opción condicional;
   - **no se activa** en el MVP actual de `#16`.
1. Timestamps pendientes (`serverTimestamp`) mantienen orden provisional hasta
   `refresh`, según `#18`.

## Triggers de carga y refresh (`on-demand`)

### Estado inicial de pantalla (decisión cerrada)

- `selected_year` inicial = año de `current week` (`week_cursor` derivado)
- `selected_week` inicial = `none`
- `selected_entry` inicial = `none`

### Consecuencia de lecturas iniciales

- **Cargar al abrir pantalla**: Q1 + Q2 + Q3 + Q4 + Q6
- **No cargar hasta selección**: Q5 + Q7 + Q8

### Tabla 4 — Refresco por tipo de evento (`I16-S3`)

| `evento_ui_o_operacion` | `queries_a_refrescar` | `motivo` | `requiere_refresh_manual` | `notas` |
| --- | --- | --- | --- | --- |
| `open_main_screen` | Q1, Q2, Q3, Q4, Q6 | Estado inicial mínimo visible | No | Año inicial derivado de `week_cursor` |
| `ui.manual_refresh` | Q1, Q2, Q3, Q4, Q6 + (Q5/Q7/Q8 si hay selección/activa aplicable) | `on-demand refresh` global del contexto visible | Sí (trigger del usuario) | Sin listeners realtime (`#7`) |
| `ui.select_year` | Q3, Q4 (+ limpiar selección local de `Week`/`Entry`) | Cambia el conjunto de weeks visibles | No | Q5/Q8 no cargan hasta nueva selección |
| `ui.select_week` | Q5 | Cargar entries de la week seleccionada | No | No cambia `week_cursor` |
| `ui.select_entry` | Q8 (+ Q7 solo si sigue activo global en otra entry y la UI lo necesita) | Cargar sesiones de la entry seleccionada | No | Q5 ya aporta datos base de la entry |
| `Week.close/reopen/reclose/update_notes` | Q1 (si cambia `week_cursor`), Q3/Q4 (año visible), Q6 (si hubo `auto-stop`) | Reflejar estado de week, cursor y sesión activa | No (post-escritura local) | Si la week afectada no está en año visible, Q3/Q4 puede diferirse a refresh manual |
| `Campaign.extend_years_plus_one` | Q1, Q2, Q3/Q4 si el año visible queda afectado | Reflejar nuevo año / estado de campaña | No (post-escritura local) | `+` vive en selector de año (`#9`) |
| `Entry.create/update/delete/reorder` sobre `selected_week` | Q5 (+ Q8 si afecta `selected_entry`) | Actualizar tabs/lista y panel de entry | No (post-escritura local) | `Entry.delete` puede requerir también Q6 si había activa |
| `Entry.adjust/set/clear_resource_delta` sobre `selected_entry` | Q1, Q5 | Totales globales + `resource_deltas` de entry | No (post-escritura local) | Reglas de recursos en `#15` |
| `Session.start/stop/auto-stop/manual_*` | Q6, Q8 (si afecta `selected_entry`), Q7 (si aplica) | Reflejar activo global y sesiones de la entry | No (post-escritura local) | Recuperación por conflicto sigue `#14/#8` |

### Regla de refresh post-escritura (MVP)

1. Tras una escritura local confirmada, el cliente refresca **solo las queries
   del ámbito afectado** (no recarga global indiscriminada por defecto).
1. Ante `conflicto`, la recuperación sigue el patrón `refresh` manual +
   reintento (`#8`, `#14`, `#15`, `#12`).

## Paginación y límites del MVP

### Decisión cerrada

- **No hay paginación en el MVP** para:
  - years
  - weeks del año seleccionado
  - entries de la week seleccionada
  - sesiones de la entry seleccionada

### Justificación documental

1. `years_list` y `weeks_selected_year_*` tienen volumen pequeño y acotado.
1. `entries_selected_week` solo se carga tras seleccionar week.
1. `sessions_selected_entry_combined` solo se carga tras seleccionar entry y el
   volumen esperado es bajo (normalmente ~1 sesión por entry).
1. La UI puede plegar sesiones sin exigir paginación.

### Límite explícito aceptado

Si el histórico de sesiones de una `Entry` crece de forma anómala o el número
de entries por week se vuelve alto para el dispositivo objetivo, la paginación
se tratará como ampliación posterior (no bloquea `#16`).

## Riesgos de coste/latencia y mitigaciones

### Riesgos principales

1. **Sobrecarga por recargar de más tras escrituras**
   - Riesgo: degradar UX si se recarga toda la pantalla tras cada operación.
   - Mitigación: refresco por ámbito (tabla 4) y refresh manual para conflictos.

1. **Q3+Q4 incluyen `notes`**
   - Riesgo: cargar campos de week que no siempre se muestran.
   - Mitigación: aceptar el coste por simplicidad del MVP; evita query extra
     para panel `Week`.

1. **Dependencia de `collection group` para Q6**
   - Riesgo: índice/consulta no disponible si se implementa sin soporte.
   - Mitigación: documentar la dependencia en `#16`; si la implementación no la
     usa, deberá ofrecer una alternativa equivalente sin cambiar el contrato
     observable.

1. **Figma incompleto (bloque central / barra inferior)**
   - Riesgo: lecturas faltantes si luego aparecen nuevos datos requeridos.
   - Mitigación: cerrar `#16` con supuestos explícitos y limitar el contrato a
     datos ya cerrados por dominio/flujo.

### Supuestos de lectura por superficies incompletas (obligatorios)

1. **Bloque central**
   - modo `Week`: consume `status` + `notes` desde Q3/Q4 (sin query extra)
   - modo `Entry`: consume `Entry` desde Q5 y sesiones desde Q8
1. **Barra inferior**
   - requiere Q1 (`resource_totals`) + Q6 (activo global) + Q7 (label del
     activo si activa != seleccionada)
   - el detalle visual no introduce nuevas entidades/queries en `#16`

## Casos de aceptación / verificación documental

1. Al abrir pantalla:
   - la barra superior se sitúa en el año de `current week`;
   - no hay `Week` ni `Entry` seleccionada;
   - se cargan Q1 + Q2 + Q3 + Q4 + Q6, pero no Q5/Q7/Q8.
1. Seleccionar una week carga Q5 (`entries_selected_week`) y no dispara Q8
   hasta seleccionar `Entry`.
1. Seleccionar una entry carga Q8 (`sessions_selected_entry_combined`) para
   total jugado y desplegable de sesiones.
1. La UI puede distinguir foco vs activo con Q6 (+ Q7 si aplica), alineado con
   `#14`.
1. Cambiar de año recarga weeks del año seleccionado completo (Q3+Q4), sin
   paginación por ventana.
1. `#16` reutiliza las tuplas canónicas de `#18` y no redefine desempates.
1. `timeline_entries_flat` queda explícitamente no activado en el MVP actual.
1. La ausencia de paginación queda documentada como decisión explícita con
   límites aceptados.

## Riesgos, límites y decisiones diferidas

- La implementación concreta de queries/índices Firestore queda fuera de esta
  issue.
- La matriz de edge cases de lecturas críticas y refresh/sync se documenta en
  `docs/concurrency-sync-edge-case-matrix.md` (Issue `#17`) y reutiliza este
  inventario como base.
- La paginación real (si se necesitara por volumen) se difiere a una ampliación
  posterior.
- El Figma usado como canon de layout para `#16` no está archivado aún en el
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
- `tdd.md` (legado, no canónico para layout de `#16`)
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
