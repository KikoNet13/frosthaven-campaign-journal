# Modelo de Recursos por Entry (MVP)

## Metadatos

- `doc_id`: DOC-RESOURCE-DELTA-MODEL
- `purpose`: Definir el modelo MVP de recursos como delta neto por `resource_key` dentro de `Entry`, sustituyendo el modelo previo basado en `ResourceChange`.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar una decisión de dominio para el MVP que sustituya la entidad
`ResourceChange` por un modelo de recursos embebido en `Entry`, con semántica
de delta neto editable por recurso y trazabilidad suficiente para alinear
dominio, conflictos y contrato de operaciones.

## Alcance y no alcance

Incluye:

- modelo lógico/persistido de recursos del MVP dentro de `Entry`;
- semántica de edición (`+/-` y edición manual) sobre deltas netos;
- invariantes y validaciones de recursos;
- impacto documental sobre `docs/domain-glossary.md`, `docs/conflict-policy.md`
  y `docs/firestore-operation-contract.md`;
- impacto downstream sobre `#15`, `#17`, `#18` y `#19`.

No incluye:

- implementación de código de app;
- técnica Firestore concreta (transacciones, batches, índices);
- política de timestamps/desempates de orden estable (`#18`);
- diseño de UI detallado de controles de recursos.

## Entradas y prerrequisitos

- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/firestore-operation-contract.md` (Issue `#12`)
- `docs/editability-policy.md` (Issue `#37`)
- Decisiones de Kiko para esta unidad:
  - eliminar `ResourceChange` como entidad/log incremental del MVP;
  - usar un mapa en `Entry` con delta neto por `resource_key`;
  - eliminar la clave si el delta neto queda en `0`;
  - mantener solo auditoría de `Entry` (sin timestamps por recurso);
  - parchear `#12` por supersesión parcial sin reabrir la issue.

## Problema del modelo previo (log `ResourceChange`)

1. El modelo `ResourceChange` como log `0..N` por `Entry` no encaja con la
   intención de edición manual "como papel" para recursos en el MVP.
1. Registrar múltiples cambios del mismo recurso dentro de una sola `Entry`
   introduce complejidad adicional (historial intra-entry) que no aporta valor
   al MVP actual.
1. El contrato de operaciones y la política de conflictos se vuelven más
   complejos al tratar recursos como entidad hija separada cuando el objetivo es
   editar un **resultado neto** por recurso en la `Entry`.

## Decisión de modelo (delta neto por recurso en `Entry`)

1. Se elimina `ResourceChange` como entidad persistida/documentada del MVP.
1. Los cambios de recursos del MVP se modelan en `Entry` como un mapa
   `resource_deltas`.
1. Cada `resource_key` puede aparecer **como máximo una vez** dentro de una
   `Entry` (delta neto por recurso).
1. Repetidos `+/-` sobre el mismo recurso en la misma `Entry` actualizan el
   **mismo delta neto**.
1. Si el delta neto resultante de un recurso pasa a `0`, la clave se elimina
   del mapa (`ausencia == delta 0`).
1. No existe historial incremental intra-entry por recurso en el MVP.

## Estructura de datos del MVP

### `Entry.resource_deltas`

- tipo lógico: `map<resource_key, int>`
- semántica: delta neto por recurso dentro de esa `Entry`
- cardinalidad efectiva:
  - por `resource_key`: `0..1`
  - por `Entry`: `0..N` claves (solo recursos con delta `!= 0`)

### Reglas de representación

1. `resource_key` debe pertenecer al catálogo de recursos MVP definido en
   `docs/domain-glossary.md`.
1. `delta` es un entero firmado (`int`).
1. No se persisten claves con valor `0`.
1. La ausencia de una clave equivale a delta `0` para esa `Entry`.

## Semántica de edición (`+/-` y edición manual)

1. Acciones UI `+/-` sobre un recurso dentro de una `Entry` ajustan el delta
   neto existente para esa `resource_key`.
1. La edición manual de recursos puede:
   - reemplazar el delta neto;
   - ajustarlo;
   - borrarlo explícitamente (o implícitamente al llegar a `0`).
1. Si una operación deja el delta neto en `0`, la clave se elimina del mapa.
1. No se conserva un historial de microcambios del mismo recurso dentro de una
   `Entry` en el MVP.

## Validaciones e invariantes

1. Los totales globales (`Campaign.resource_totals`) siguen derivándose de la
   suma de `Entry.resource_deltas` a través de las `Entry` de la campaña.
1. Se mantiene la validación de **totales finales no negativos**.
1. La editabilidad de recursos es compatible con weeks `open|closed` (alineado
   con `#37`).
1. No hay auditoría por recurso; la auditoría de recursos usa la auditoría de
   `Entry` (`updated_at_utc`, etc.).
1. El borrado de `Entry` elimina implícitamente sus deltas de recursos al
   eliminar el documento `Entry` (sin subcolección `resource_changes`).

## Impacto en contratos y conflictos

### Supersesión parcial de `#12`

1. `DEC-0023` y `docs/firestore-operation-contract.md` quedan **parcialmente
   supersedidos** en la parte de operaciones `ResourceChange.*`.
1. La Issue `#12` permanece cerrada; la corrección se documenta mediante esta
   nueva decisión y un parche de consistencia en el contrato.

### Parche esperado en `docs/firestore-operation-contract.md`

Se sustituyen operaciones `ResourceChange.*` por operaciones sobre
`Entry.resource_deltas`:

- `Entry.adjust_resource_delta`
- `Entry.set_resource_delta`
- `Entry.clear_resource_delta`

### Alineación con `docs/conflict-policy.md`

1. Las colisiones de recursos pasan a modelarse como conflicto sobre `Entry`
   (y totales derivados), no sobre una entidad `ResourceChange`.
1. Se mantiene la política estricta de `rechazar` + `refrescar` + `reintentar`
   para conflictos concurrentes reales.
1. Se mantiene la validación de totales finales no negativos.

## Impacto en issues downstream (`#15`, `#17`, `#18`, `#19`)

- `#15`: debe definir reglas de validación y recálculo sobre
  `Entry.resource_deltas`, no sobre `ResourceChange`.
- `#17`: sustituir edge cases de concurrencia sobre `ResourceChange` por casos
  de edición concurrente de `Entry.resource_deltas`.
- `#18`: se simplifica el inventario de eventos/listas ordenables al eliminar el
  log de `ResourceChange` por `Entry`.
- `#19`: el plan de pruebas debe cubrir deltas netos por recurso y eliminación
  de clave al llegar a `0`.

## Casos de aceptación / verificación documental

1. Múltiples taps sobre el mismo recurso en una `Entry` terminan en un único
   delta neto por `resource_key`.
1. Si el delta neto llega a `0`, la clave se elimina de `resource_deltas`.
1. La edición de recursos en weeks `closed` sigue permitida (alineado con `#37`)
   y mantiene validación de totales no negativos.
1. `docs/domain-glossary.md` ya no define `ResourceChange` como entidad MVP.
1. `docs/firestore-operation-contract.md` ya no expone `ResourceChange.*` y
   define operaciones sobre `Entry.resource_deltas`.
1. `docs/conflict-policy.md` modela conflictos de recursos sobre `Entry` (más
   totales derivados), no sobre `ResourceChange`.
1. La decisión deja a `#18` (timestamps y orden estable) con menor ambigüedad
   de inventario, al eliminar el log `ResourceChange` del MVP.

## Riesgos, límites y decisiones diferidas

- Se pierde historial detallado intra-entry de cambios de recursos en favor de
  simplicidad de edición neta (aceptado en MVP).
- La estrategia exacta de persistencia/atomicidad Firestore sigue diferida a la
  implementación.
- La política de timestamps y orden estable se define en
  `docs/timestamp-order-policy.md` (Issue `#18`).

## Referencias

- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/firestore-operation-contract.md`
- `docs/editability-policy.md`
- `docs/timestamp-order-policy.md`
- `docs/decision-log.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
