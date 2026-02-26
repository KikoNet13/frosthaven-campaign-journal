# Política de Editabilidad Manual y Correcciones (MVP)

## Metadatos

- `doc_id`: DOC-EDITABILITY-POLICY
- `purpose`: Definir la política de editabilidad manual del MVP ("como papel") y las correcciones de orden, estado y sesiones que actualizan invariantes del dominio antes del contrato Firestore por agregado.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar una decisión marco de dominio para el MVP que permita correcciones
manuales amplias ("como papel"), manteniendo consistencia explícita en
invariantes críticos y dejando trazado el impacto sobre las Issues `#12`, `#14`,
`#15`, `#17` y `#19`.

## Alcance y no alcance

Incluye:

- reordenación manual de `Entry` dentro de una misma `Week`;
- corrección manual de `Week.status` (`reopen`/`reclose`);
- correcciones manuales completas de `Session` (crear/editar/borrar,
  incluyendo timestamps);
- política derivada de semana actual (primera `Week` abierta) como concepto no persistido;
- matriz de operaciones manuales permitidas y sus límites;
- impacto documental sobre dominio, conflictos y orden técnico downstream.

No incluye:

- contrato Firestore por agregado (Issue `#12`);
- política de timestamps y desempates (Issue `#18`);
- diseño de UI detallado de flujos y pantallas (Issues `#14`, `#16`);
- implementación de código de app.

## Entradas y prerrequisitos

- `docs/domain-glossary.md` (modelo de dominio e invariantes actuales)
- `docs/conflict-policy.md` (política de conflictos concurrentes MVP)
- `docs/campaign-temporal-controls.md` (controles temporales y semántica temporal)
- `docs/campaign-temporal-initialization.md` (estructura temporal y provisión)
- Decisiones de Kiko para esta issue marco:
  - reordenación manual de `Entry`: sí, con operación "mover una entry";
  - alcance de reordenación: solo dentro de la misma `Week`;
  - `order_index`: secuencia densa `1..N`;
  - `Week.reopen/reclose`: sí;
  - correcciones manuales de `Session`: completo (crear/editar/borrar, con timestamps);
  - semana actual derivada: primera `Week` abierta (menor `week_number` entre abiertas);
  - borrado para `#12`: hard delete real (insumo downstream);
  - `Entry.update` para `#12`: amplio (insumo downstream);
  - atomicidad en `#12`: solo comportamiento (insumo downstream).

## Principio de editabilidad del MVP ("como papel")

1. El MVP prioriza permitir correcciones manuales amplias para trabajar "como en
   papel", pero con mayor orden y trazabilidad.
1. La editabilidad amplia no elimina invariantes críticos; los redefine de
   forma explícita cuando sea necesario.
1. Las correcciones manuales se documentan primero a nivel de dominio; el
   contrato Firestore por agregado se define después en la Issue `#12`.
1. La política de conflictos concurrentes del MVP sigue siendo de rechazo con
   `refresco` y `reintento`; esta decisión actualiza qué operaciones existen y
   qué precondiciones funcionales aplican.

## Matriz de operaciones manuales permitidas (MVP)

| Operación manual | Agregado principal | Permitida en MVP | Alcance | Notas |
| --- | --- | --- | --- | --- |
| `Entry.reorder_within_week` | `week` + `entry` | Sí | Mover una `Entry` dentro de la misma `Week` | Resecuencia `order_index` densa `1..N` |
| `Entry.update` | `entry` | Sí | Amplio (campos funcionales de `Entry`) | Contrato detallado en `#12`; no cambia de `Week` aquí |
| `Week.update_notes` | `week` | Sí | Weeks abiertas o cerradas | Editabilidad de contenido amplia |
| `Week.reopen` | `week` + `campaign` | Sí | `closed -> open` | Recalcula la semana actual derivada |
| `Week.reclose` | `week` + `campaign` | Sí | `open -> closed` | Recalcula la semana actual derivada |
| `Session.manual_create` | `session` + `campaign` | Sí | Histórica o activa | Preserva `0..1` sesión activa global |
| `Session.manual_update` | `session` + `campaign` | Sí | Corrección de timestamps y estado | Preserva `0..1` sesión activa global |
| `Session.manual_delete` | `session` + `campaign` | Sí | Borrado real | Preserva `0..1` sesión activa global |
| `Entry.adjust/set/clear_resource_delta` | `entry` | Sí | Weeks abiertas o cerradas | Edita `Entry.resource_deltas` (delta neto por recurso) con validación de totales no negativos |

## Reglas por agregado

### `Entry` / orden del timeline

1. Se permite reordenación manual de `Entry` en el MVP.
1. La operación funcional documentada es **mover una `Entry`** a una nueva
   posición dentro de la **misma `Week`**.
1. No se permite mover `Entry` entre weeks en esta decisión.
1. Tras una reordenación válida, `order_index` se recalcula a secuencia **densa
   `1..N`** dentro de la `Week`.
1. Rechazos esperados a nivel funcional:
   - `Entry` inexistente o ya borrada;
   - `Week` de referencia inconsistente;
   - colisión o resecuenciación imposible por estado obsoleto concurrente.

### `Week` / estado y notas

1. `Week.notes` es editable tanto en `open` como en `closed`.
1. Se permite corrección manual de `Week.status`:
   - `Week.reopen`: `closed -> open`
   - `Week.reclose`: `open -> closed`
1. Las operaciones de estado (`reopen/reclose`) son correcciones manuales
   explícitas y no equivalen a navegación temporal.
1. Las operaciones que dependan de `Week.status=open` deben declararlo
   explícitamente en sus contratos (`#12`, `#14`, `#15`).

### `Session`

1. Se permiten correcciones manuales completas:
   - crear sesión manualmente;
   - editar sesión manualmente;
   - borrar sesión manualmente.
1. La edición manual incluye, como mínimo, corrección de timestamps
   (`started_at_utc`, `ended_at_utc`).
1. Se mantiene la invariante de `0..1` `Session` activa global en la campaña.
1. Si una corrección manual produciría más de una sesión activa global, la
   operación debe rechazarse.
1. `auto-stop` sigue existiendo como comportamiento de `Session.start` (flujo
   normal), pero las correcciones manuales no deben introducir cambios implícitos
   opacos; el contrato detallado se fija en `#12` y el flujo en `#14`.

### Recursos en `Entry` (`resource_deltas`)

1. La editabilidad de recursos se mantiene en el MVP, pero se expresa sobre
   `Entry.resource_deltas` (delta neto por `resource_key`), no mediante una
   entidad `ResourceChange`.
1. Se permiten ajustes incrementales (`+/-`), edición manual directa del delta
   neto y limpieza de clave cuando el resultado es `0`.
1. La política de editabilidad amplia no elimina la validación de totales
   finales no negativos.
1. El modelo detallado se define en `docs/resource-delta-model.md` y el
   contrato de pre/postcondiciones/rechazos en `#12` (parcheado por supersesión
   parcial de recursos).

## Reglas de estado y semana actual derivada (`Week.status`, concepto derivado)

### Política global de semana actual derivada

1. La **semana actual** del MVP se define como la **primera `Week` abierta**,
   es decir, la `Week` abierta con **menor `week_number`** entre las weeks
   provisionadas.
1. Navegar o seleccionar una `Week` para foco/edición no cambia automáticamente
   la semana actual derivada.
1. La semana actual se trata como un valor derivado de la estructura de weeks
   abiertas y sus estados, en lugar de una selección manual libre.
1. **Nota de transición (`#76`)**: la implementación actual todavía
   persiste/consume `campaign.week_cursor` en código como mecanismo transitorio;
   la migración técnica para retirarlo se sigue en `#81`.

### Reglas de recálculo

La semana actual derivada se recalcula tras operaciones que puedan cambiar la
primera week abierta:

- `Week.close`
- `Week.reopen`
- `Week.reclose`
- provisión inicial / extensión temporal

### Relación con el ajuste manual previo de `week_cursor`

1. La semántica de `Campaign.set_week_cursor` como ajuste manual explícito (Issue
   `#9`) queda **sustituida** en MVP por la política derivada de cursor de esta
   decisión (`#37`).
1. El detalle de la transición contractual se alinea en:
   - `docs/campaign-temporal-controls.md`
   - `docs/campaign-temporal-initialization.md`
   - `#12` (contrato por agregado)

### Invariante de existencia de week abierta (soporte de la semana actual)

1. Debe existir al menos una `Week` abierta provisionada para mantener
   una semana actual derivada válida.
1. Si una operación (`Week.close`/`Week.reclose`) dejara **0 weeks abiertas**,
   la operación se rechaza.

## Reglas para sesiones manuales

### `Session.manual_create`

1. Puede crear una sesión histórica (con `ended_at_utc` definido) o activa
   (`ended_at_utc=null`).
1. Si crea una sesión activa, debe validarse que no exista otra sesión activa
   global en la campaña.

### `Session.manual_update`

1. Permite corregir timestamps de una sesión existente.
1. Si la corrección cambia el estado a activa (`ended_at_utc=null`), debe
   validarse la unicidad de sesión activa global.
1. Si la corrección cambia una sesión activa a cerrada, la sesión deja de contar
   como activa sin requerir `auto-stop`.

### `Session.manual_delete`

1. Permite borrar manualmente una sesión histórica o activa.
1. Si se borra una sesión activa, el resultado debe mantener `0..1` sesiones
   activas globales (normalmente `0`).

## Invariantes preservadas y modificadas

### Invariantes preservadas

- `0..1` `Session` activa global en la campaña.
- `week_number` global inmutable.
- Validación de totales finales no negativos en recursos.
- Jerarquía temporal `campaign > year > season > week > entry`.

### Invariantes modificadas / ampliadas

- Se sustituye “sin reordenación manual de `Entry` en MVP” por:
  - reordenación manual permitida dentro de la misma `Week` con secuencia densa
    `1..N`.
- Se amplía la mutabilidad de `Week.status`:
  - se permiten `reopen` y `reclose`.
- Se amplía la mutabilidad de `Session`:
  - correcciones manuales completas (crear/editar/borrar).
- Se redefine la semana actual:
  - pasa a ser la primera `Week` abierta (menor `week_number` abierta).

## Impacto sobre conflictos y contratos downstream

### Impacto sobre `docs/conflict-policy.md` / Issue `#8`

- Se añaden/ajustan operaciones concurrentes de:
  - `Week.reopen`
  - `Week.reclose`
  - correcciones manuales de `Session`
  - reordenación manual de `Entry`
- Se mantiene la política de rechazo con `refresco` y `reintento`.

### Impacto sobre `#12` (contrato Firestore por agregado)

- Añade operaciones y precondiciones nuevas a documentar.
- Debe alinearse con:
  - hard delete real (input ya acordado)
  - `Entry.update` amplio (input ya acordado)
  - atomicidad descrita como comportamiento (sin técnica obligatoria)

### Impacto sobre `#14`, `#15`, `#17`, `#19`

- `#14`: flujo de sesión activa / `auto-stop` debe coexistir con correcciones
  manuales de sesión y `Week.reopen/reclose`.
- `#15`: reglas de recursos deben considerar editabilidad en weeks cerradas y
  correcciones amplias sobre `Entry.resource_deltas`.
- `#17`: matriz de edge cases debe incorporar reordenación, reopen/reclose y
  correcciones manuales de sesión.
- `#19`: el plan de pruebas de invariantes debe incluir los nuevos casos de
  cursor derivado y mutabilidad ampliada.

## Casos de aceptación / verificación documental

1. **Mover `Entry` dentro de una `Week`**
   - `order_index` queda denso `1..N`.
   - No hay movimiento entre weeks.
1. **Reabrir una `Week` cerrada**
   - `Week.status` cambia a `open`.
   - la semana actual derivada se recalcula a la primera week abierta.
1. **Re-cerrar una `Week` reabierta**
   - `Week.status` vuelve a `closed`.
   - la semana actual derivada se recalcula con la misma regla global.
1. **Corrección manual completa de `Session`**
   - Se permiten create/edit/delete con timestamps.
   - No se rompe la invariante `0..1` sesión activa global.
1. **Límite de cursor válido**
   - Se rechaza una operación que deje `0` weeks abiertas provisionadas.
1. **Alineación con conflictos**
   - `docs/conflict-policy.md` queda coherente con la nueva editabilidad.
1. **Desbloqueo de `#12`**
   - `#12` puede redactarse con dominio actualizado y trazabilidad explícita.

## Riesgos y límites

- Riesgo de ampliar demasiado el alcance de `#12` si no se separa claramente
  esta decisión de dominio del contrato Firestore.
- Riesgo de contradicción temporal si no se alinean `#9`, `#13` y esta decisión
  respecto a la semana actual derivada (históricamente `week_cursor`).
- Riesgo de aumentar edge cases concurrentes; se asume mitigación mediante la
  política de rechazo ya vigente en `#8`.

## Referencias

- `AGENTS.md`
- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `docs/resource-delta-model.md`
- `docs/decision-log.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
