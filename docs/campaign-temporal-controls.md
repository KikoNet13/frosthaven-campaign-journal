# Controles Temporales de Campaña (MVP)

## Metadatos

- `doc_id`: DOC-CAMPAIGN-TEMPORAL-CONTROLS
- `purpose`: Definir el contrato funcional de navegación temporal y provisión/extensión de años en la pantalla principal del MVP.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar el contrato funcional del selector temporal superior (año/semana) en la
pantalla principal única del MVP, incluyendo la provisión inicial y extensión
manual de años sin depender de una pantalla separada de ajustes de campaña solo
para esta función.

## Alcance MVP y no alcance

Incluye:

- ubicación funcional del control temporal en la barra superior;
- selector de año y selector de semanas del año seleccionado;
- provisión inicial automática de años en `campaign/01`;
- extensión manual de años (`+1`) con confirmación;
- semántica de navegación de semana vs cambio de `week_cursor`;
- patrón de UI del selector de entry al pulsar semana (a nivel de intención).

No incluye:

- detalle de creación de `year/season/week` (Issue #13);
- detalle del contenido y acciones del popover de entries (Issue #14 o
  equivalente);
- políticas de conflicto/timestamps más allá de las referencias a `#8` y `#18`;
- acciones destructivas de reset o reprovisión completa de la estructura
  temporal.

## Estructura funcional de la pantalla principal (MVP)

- **Barra superior**:
  - navegación temporal (`year` + semanas);
  - acceso a provisión/extensión de años;
  - reemplaza la función de navegación temporal de la barra izquierda del
    boceto anterior.
- **Zona central**:
  - formulario de la `Entry` actual (sin cambios de alcance en esta issue).
- **Barra inferior**:
  - totales de campaña (sin cambios de alcance en esta issue).

## Selector de año

1. Muestra el año actualmente seleccionado en la barra superior.
1. Permite navegación entre años ya provisionados.
1. Si existen años anteriores, se muestra acción de navegación a la izquierda
   (`←`).
1. Si existen años posteriores ya provisionados, se muestra acción de
   navegación a la derecha (`→`).
1. Si el año seleccionado es el último año provisionado, la acción derecha se
   reemplaza por `+` para extensión manual.

## Selector de semana

1. El selector de semanas muestra semanas del **año seleccionado**.
1. Su función principal en esta issue es navegación/foco temporal.
1. Pulsar una semana **no cambia automáticamente** `campaign.week_cursor`.
1. Al pulsar una semana se abre el flujo de selección de entry (popover/modal
   anclado), definido en esta issue a nivel de patrón e intención.

## Provisión inicial de años (automática)

1. La provisión inicial ocurre automáticamente al crear `campaign/01`.
1. El valor por defecto del MVP es **4 años**.
1. Esta issue cierra el contrato funcional de provisión inicial, pero no el
   detalle técnico de cómo se crean `year/season/week` (Issue #13).

## Extensión manual de años (`+1` con confirmación)

1. La extensión de años es manual y explícita en el MVP.
1. Cuando el selector está en el último año provisionado, se muestra `+` en la
   posición de la acción derecha.
1. Pulsar `+` solicita confirmación.
1. Tras confirmar, se añade **1 año** nuevo.
1. No hay extensión automática por umbral en el MVP.

## Política de `week_cursor` (actualización posterior de dominio)

1. La semántica original de ajuste manual explícito de `week_cursor` definida en
   esta issue fue **actualizada** por la Issue `#37`
   (`docs/editability-policy.md`).
1. En el MVP actual, `week_cursor` apunta a la **primera `Week` abierta**
   (menor `week_number` abierta) y se recalcula tras cambios de estado de
   `Week`.
1. Seleccionar semana para navegar/focalizar sigue siendo una acción separada de
   la navegación temporal y no cambia automáticamente `week_cursor`.
1. El marcador visual de `current week` (derivado de `week_cursor`) y la
   selección `Week`/`Entry` usada por el flujo de sesión se tratan como
   conceptos separados (ver `docs/active-session-flow.md`, Issue `#14`).
1. Default de arranque de pantalla principal (`#16`): la barra superior se
   sitúa en el año de `current week`, pero la selección inicial de `Week` y
   `Entry` es vacía (`none`).

## Click en semana y selector de entry (patrón + intención)

1. Patrón de UI adoptado: **popover/modal anclado** al control de semana.
1. Intención funcional:
   - permitir seleccionar la `Entry` a editar dentro de la semana;
   - mostrar estado vacío y/o acción hacia creación cuando no existan entries.
1. El detalle del contenido del popover (layout, copy, orden y acciones de
   creación rápida) queda fuera de esta issue y se difiere a Issue #14 o una
   issue específica equivalente.

## Límites y dependencias

- **Issue #9** (esta decisión): navegación temporal superior + provisión/
  extensión de años + semántica de `week_cursor`.
- **Issue #13**: detalle técnico de inicialización y extensión de
  `year/season/week`.
- **Issue #14** (o equivalente): detalle del popover de entries y flujo de
  selección/creación de entry desde semana, incluyendo flujo de sesión activa y
  separación entre `current week`, foco y activo (`docs/active-session-flow.md`).
- **Issue #16**: inventario mínimo de lecturas/consultas de pantalla principal
  (arranque sin selección, cargas por selección de week/entry y triggers de
  refresh on-demand).
- **Issue #12**: contrato de operaciones Firestore por agregado (implementación
  técnica de operaciones como provisión/extensión/cambio de cursor).
- **Issue #37**: política de editabilidad manual del MVP y semántica derivada de
  `week_cursor` (primera `Week` abierta), que actualiza esta decisión.
- **Issue #18**: timestamps y desempates de orden estable entre dispositivos.

## Referencias

- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/decision-log.md`
- `docs/editability-policy.md`
- `docs/active-session-flow.md`
- `docs/minimal-read-queries.md`
- `tdd.md` (legado temporal, alineado con referencia oficial)
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/9`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
