# Inicialización Temporal de Campaña (MVP)

## Metadatos

- `doc_id`: DOC-CAMPAIGN-TEMPORAL-INITIALIZATION
- `purpose`: Especificar la estrategia técnica de provisión inicial y extensión de años, estaciones y semanas del MVP sin definir aún el contrato Firestore por agregado.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar la especificación técnica de inicialización/extensión temporal para la
Issue #13, detallando cómo se crean `year`, `season` y `week` en `campaign/01`
de forma determinista y sin ambigüedad operativa, alineada con
`docs/campaign-temporal-controls.md` (Issue #9) y `docs/domain-glossary.md`.

## Alcance y no alcance

Incluye:

- template temporal fijo del MVP por `year/season/week`;
- provisión inicial automática de `4` años al crear `campaign/01`;
- extensión manual de `+1` año desde el control de cambio de año de la UI;
- reglas de creación y validación para evitar duplicados y estados inválidos;
- continuidad de `week_number` global y relación con `week_cursor`.

No incluye:

- implementación de código de app;
- mecánica exacta de transacciones/atomicidad Firestore (Issue #12);
- política de timestamps o desempates de orden estable (Issue #18);
- detalle de UX del selector de año/semana o del botón `+` (Issue #9 ya fija el
  contrato funcional).

## Entradas y prerrequisitos

- `docs/campaign-temporal-controls.md` (Issue #9):
  - provisión inicial automática de `4` años;
  - extensión manual `+1` con confirmación;
  - trigger de extensión desde el control de año;
  - separación entre navegación de semana y cambio de `week_cursor`.
- `docs/domain-glossary.md`:
  - jerarquía `campaign > year > season > week > entry`;
  - `week_number` global inmutable;
  - `week_cursor` separado de la navegación de semana.
- `docs/editability-policy.md` (Issue #37):
  - `week_cursor` = primera `Week` abierta;
  - recálculo tras cambios de `Week.status`.
- Aclaración de Kiko (fuente de verdad para `#13`):
  - `season` = **estación** (`summer|winter`);
  - orden fijo: `summer` -> `winter`;
  - `10` semanas por estación.

## Convenciones y terminología

- En documentación en castellano, `season` se traduce como **estación**.
- Se mantienen identificadores técnicos:
  - `season`
  - `season_type`
  - `summer|winter`
- El orden canónico de estaciones por año en el MVP es:
  1. `summer` (verano)
  1. `winter` (invierno)

## Template temporal del MVP (fijo)

### Estructura por año

Por cada `year_number`:

- estación `summer`
  - `10` semanas
- estación `winter`
  - `10` semanas

### Cardinalidades fijas del MVP

| Nivel | Cardinalidad |
| --- | --- |
| `seasons` por `year` | `2` (`summer`, `winter`) |
| `weeks` por `season` | `10` |
| `weeks` por `year` | `20` |
| `years` iniciales por `campaign/01` | `4` |
| `weeks` iniciales totales | `80` |

### Reglas globales de numeración

- `week_number` es global, correlativo e inmutable.
- `week_number` no se reutiliza aunque existan cambios históricos.
- La creación inicial de `4` años genera por defecto `week_number` `1..80`.
- Supuesto operativo adoptado en `#13`: el primer año provisionado usa
  `year_number = 1`.

### Tabla de referencia para la provisión inicial (`campaign/01`)

| Año | Estación | Rango de `week_number` |
| --- | --- | --- |
| `1` | `summer` | `1..10` |
| `1` | `winter` | `11..20` |
| `2` | `summer` | `21..30` |
| `2` | `winter` | `31..40` |
| `3` | `summer` | `41..50` |
| `3` | `winter` | `51..60` |
| `4` | `summer` | `61..70` |
| `4` | `winter` | `71..80` |

## Flujo técnico de provisión inicial de 4 años (`I13-S1`)

1. Al crear `campaign/01`, se provisiona automáticamente la estructura temporal
   inicial del MVP.
1. Se crean `4` años completos consecutivos comenzando en `year_number = 1`.
1. Para cada año:
   - crear estación `summer`;
   - crear `10` `weeks` consecutivas;
   - crear estación `winter`;
   - crear `10` `weeks` consecutivas.
1. La numeración `week_number` se asigna de forma global y correlativa.
1. El resultado esperado es una estructura inicial consistente de `80` semanas.

## Flujo técnico de extensión manual `+1` año (`I13-S2`)

1. El trigger funcional de la extensión es la acción `+` del control de año en
   la UI (definido en `docs/campaign-temporal-controls.md`).
1. Tras la confirmación del usuario (definida en `#9`), la extensión técnica
   crea exactamente `1` año nuevo completo.
1. El nuevo año usa el siguiente `year_number` consecutivo al último año
   provisionado.
1. La creación del nuevo año respeta el mismo template:
   - `summer` -> `10` semanas;
   - `winter` -> `10` semanas.
1. La numeración `week_number` continúa desde la última semana existente.
1. La extensión `+1` no reprovisiona ni modifica años ya existentes.

## Reglas de creación y validación (`I13-S3`)

### Reglas de creación de `year`

- Solo se crea un `year` nuevo si su `year_number` no existe ya en
  `campaigns/01/years/`.
- En provisión inicial, los `year_number` creados son consecutivos (`1..4`).
- En extensión manual, el único `year_number` válido es el siguiente consecutivo
  al máximo existente.

### Reglas de creación de `season`

- `season_type` permitido: solo `summer|winter`.
- Cada `year` debe contener exactamente dos estaciones.
- El orden de creación por año es fijo:
  1. `summer`
  1. `winter`
- No se permite invertir el orden (`winter` antes de `summer`).
- No se permite crear estaciones adicionales fuera de `summer|winter`.
- No se permite duplicar `season_type` dentro del mismo `year`.

### Reglas de creación de `week`

- Cada estación debe contener exactamente `10` `weeks`.
- Cada `week` tiene `week_number` global único.
- La numeración es correlativa y continúa desde el máximo existente.
- No se permite crear más o menos de `10` semanas por estación dentro del
  template del MVP.
- `year_number` y `season_type` deben ser coherentes con el `week_number`
  asignado y la jerarquía persistida.

### Validaciones mínimas y rechazos esperados

- Rechazar provisión inicial si la estructura temporal inicial ya existe y la
  operación implicaría duplicados.
- Rechazar extensión `+1` si intenta crear un `year_number` ya existente.
- Rechazar creación de estación con `season_type` distinto de `summer|winter`.
- Rechazar creación de estación en orden inválido para un año.
- Rechazar creación de semanas si la cardinalidad de la estación no queda en
  `10`.
- Rechazar cualquier creación que duplique `week_number` global.

## Relación con `week_cursor` (consistencia con `#9` y glosario)

- Navegar o seleccionar una semana en el control temporal superior **no**
  cambia automáticamente `campaign.week_cursor`.
- La política de recálculo de `week_cursor` (primera `Week` abierta) se define
  en `docs/editability-policy.md` (Issue #37).
- Esta especificación (#13) define la estructura temporal creada; no redefine la
  semántica funcional de navegación/cursor ya cerrada en `#9`.

## Insumo para la Issue #12 (sin invadir su alcance) (`I13-S4`)

Este documento deja cerrados los insumos temporales que `#12` necesita para el
contrato de operaciones Firestore por agregado:

- qué crea la provisión inicial (`4` años, `80` semanas, orden fijo);
- qué crea la extensión `+1` (un año completo, `20` semanas);
- qué validaciones mínimas temporales deben respetarse;
- qué no cambia (navegación de semana no altera `week_cursor`);
- que la semántica de recálculo de `week_cursor` se alinea con `#37`.

`#13` no define:

- atomicidad técnica;
- transacciones;
- pre/postcondiciones Firestore por agregado;
- estrategia de conflicto/timestamps.

## Casos de aceptación y verificación documental

1. **Provisión inicial de campaña nueva**
   - Se documenta creación de `4` años completos.
   - Resultado esperado: `80` semanas totales con `week_number` correlativo.
1. **Estructura por año**
   - Cada año tiene `summer` y `winter` en ese orden.
   - Resultado esperado: no hay años con una sola estación ni orden invertido.
1. **Cardinalidad de weeks por estación**
   - Cada estación define exactamente `10` `weeks`.
   - Resultado esperado: no hay estaciones con cardinalidad `!= 10`.
1. **Extensión manual `+1`**
   - Desde el botón de cambio de año (UI) se genera `1` año adicional.
   - Resultado esperado: se añade un año completo sin duplicados y con
     continuidad de `week_number`.
1. **Consistencia con `week_cursor`**
   - Navegar/seleccionar semana no cambia `week_cursor` automáticamente.
   - Resultado esperado: separación de responsabilidades mantenida (referencia a
     `#9`).
1. **No invasión de `#12`**
   - El documento no define transacciones/atomicidad Firestore.
   - Resultado esperado: `#13` queda técnico-temporal y `#12` conserva el
     contrato de operaciones.

## Riesgos y límites

- Riesgo de mezclar aquí detalles de UX del selector temporal: fuera de alcance.
- Riesgo de anticipar decisiones de `#12` (operaciones Firestore): fuera de
  alcance.
- Riesgo de anticipar `#18` (timestamps/desempates): fuera de alcance.

## Referencias

- `docs/campaign-temporal-controls.md`
- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/editability-policy.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `docs/decision-log.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/9`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
