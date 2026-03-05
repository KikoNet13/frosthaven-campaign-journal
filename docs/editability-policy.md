# PolÃ­tica de Editabilidad Manual y Correcciones (MVP)

## Metadatos

- `doc_id`: DOC-EDITABILITY-POLICY
- `purpose`: Definir la polÃ­tica de editabilidad manual del MVP ("como papel") y las correcciones de orden, estado y sesiones que actualizan invariantes del dominio antes del contrato Firestore por agregado.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-10

## Objetivo

Cerrar una decisiÃ³n marco de dominio para el MVP que permita correcciones
manuales amplias ("como papel"), manteniendo consistencia explÃ­cita en
invariantes crÃ­ticos y dejando trazado el impacto sobre las Issues `#12`, `#14`,
`#15`, `#17` y `#19`.

## Alcance y no alcance

Incluye:

- reordenaciÃ³n manual de `Entry` dentro de una misma `Week`;
- correcciÃ³n manual de `Week.status` (`reopen`/`reclose`);
- correcciones manuales completas de `Session` (crear/editar/borrar,
  incluyendo timestamps);
- polÃ­tica derivada de semana actual (primera `Week` abierta) como concepto no persistido;
- matriz de operaciones manuales permitidas y sus lÃ­mites;
- impacto documental sobre dominio, conflictos y orden tÃ©cnico downstream.

No incluye:

- contrato Firestore por agregado (Issue `#12`);
- polÃ­tica de timestamps y desempates (Issue `#18`);
- diseÃ±o de UI detallado de flujos y pantallas (Issues `#14`, `#16`);
- implementaciÃ³n de cÃ³digo de app.

## Entradas y prerrequisitos

- `docs/domain-glossary.md` (modelo de dominio e invariantes actuales)
- `docs/conflict-policy.md` (polÃ­tica de conflictos concurrentes MVP)
- `docs/campaign-temporal-controls.md` (controles temporales y semÃ¡ntica temporal)
- `docs/campaign-temporal-initialization.md` (estructura temporal y provisiÃ³n)
- Decisiones de Kiko para esta issue marco:
  - reordenaciÃ³n manual de `Entry`: sÃ­, con operaciÃ³n "mover una entry";
  - alcance de reordenaciÃ³n: solo dentro de la misma `Week`;
  - `order_index`: secuencia densa `1..N`;
  - `Week.reopen/reclose`: sÃ­;
  - correcciones manuales de `Session`: completo (crear/editar/borrar, con timestamps);
  - semana actual derivada: primera `Week` abierta (menor `week_number` entre abiertas);
  - borrado para `#12`: hard delete real (insumo downstream);
  - `Entry.update` para `#12`: amplio (insumo downstream);
  - atomicidad en `#12`: solo comportamiento (insumo downstream).

## Principio de editabilidad del MVP ("como papel")

1. El MVP prioriza permitir correcciones manuales amplias para trabajar "como en
   papel", pero con mayor orden y trazabilidad.
1. La editabilidad amplia no elimina invariantes crÃ­ticos; los redefine de
   forma explÃ­cita cuando sea necesario.
1. Las correcciones manuales se documentan primero a nivel de dominio; el
   contrato Firestore por agregado se define despuÃ©s en la Issue `#12`.
1. La polÃ­tica de conflictos concurrentes del MVP sigue siendo de rechazo con
   `refresco` y `reintento`; esta decisiÃ³n actualiza quÃ© operaciones existen y
   quÃ© precondiciones funcionales aplican.

## Matriz de operaciones manuales permitidas (MVP)

| OperaciÃ³n manual | Agregado principal | Permitida en MVP | Alcance | Notas |
| --- | --- | --- | --- | --- |
| `Entry.reorder_within_week` | `week` + `entry` | SÃ­ | Mover una `Entry` dentro de la misma `Week` | Resecuencia `order_index` densa `1..N` |
| `Entry.update` | `entry` | SÃ­ | Amplio (campos funcionales de `Entry`) | Contrato detallado en `#12`; no cambia de `Week` aquÃ­ |
| `Week.reopen` | `week` + `campaign` | SÃ­ | `closed -> open` | Recalcula la semana actual derivada |
| `Week.reclose` | `week` + `campaign` | SÃ­ | `open -> closed` | Recalcula la semana actual derivada |
| `Session.manual_create` | `session` + `campaign` | SÃ­ | HistÃ³rica o activa | Preserva `0..1` sesiÃ³n activa global |
| `Session.manual_update` | `session` + `campaign` | SÃ­ | CorrecciÃ³n de timestamps y estado | Preserva `0..1` sesiÃ³n activa global |
| `Session.manual_delete` | `session` + `campaign` | SÃ­ | Borrado real | Preserva `0..1` sesiÃ³n activa global |
| `Entry.adjust/set/clear_resource_delta` | `entry` | SÃ­ | Weeks abiertas o cerradas | Edita `Entry.resource_deltas` (delta neto por recurso) con validaciÃ³n de totales no negativos |

## Reglas por agregado

### `Entry` / orden del timeline

1. Se permite reordenaciÃ³n manual de `Entry` en el MVP.
1. La operaciÃ³n funcional documentada es **mover una `Entry`** a una nueva
   posiciÃ³n dentro de la **misma `Week`**.
1. No se permite mover `Entry` entre weeks en esta decisiÃ³n.
1. Tras una reordenaciÃ³n vÃ¡lida, `order_index` se recalcula a secuencia **densa
   `1..N`** dentro de la `Week`.
1. Rechazos esperados a nivel funcional:
   - `Entry` inexistente o ya borrada;
   - `Week` de referencia inconsistente;
   - colisiÃ³n o resecuenciaciÃ³n imposible por estado obsoleto concurrente.

### `Week` / estado

1. Se permite correcciÃ³n manual de `Week.status`:
   - `Week.reopen`: `closed -> open`
   - `Week.reclose`: `open -> closed`
1. Las operaciones de estado (`reopen/reclose`) son correcciones manuales
   explÃ­citas y no equivalen a navegaciÃ³n temporal.
1. Las operaciones que dependan de `Week.status=open` deben declararlo
   explÃ­citamente en sus contratos (`#12`, `#14`, `#15`).

### `Session`

1. Se permiten correcciones manuales completas:
   - crear sesiÃ³n manualmente;
   - editar sesiÃ³n manualmente;
   - borrar sesiÃ³n manualmente.
1. La ediciÃ³n manual incluye, como mÃ­nimo, correcciÃ³n de timestamps
   (`started_at_utc`, `ended_at_utc`).
1. Se mantiene la invariante de `0..1` `Session` activa global en la campaÃ±a.
1. Si una correcciÃ³n manual producirÃ­a mÃ¡s de una sesiÃ³n activa global, la
   operaciÃ³n debe rechazarse.
1. `auto-stop` sigue existiendo como comportamiento de `Session.start` (flujo
   normal), pero las correcciones manuales no deben introducir cambios implÃ­citos
   opacos; el contrato detallado se fija en `#12` y el flujo en `#14`.

### Recursos en `Entry` (`resource_deltas`)

1. La editabilidad de recursos se mantiene en el MVP, pero se expresa sobre
   `Entry.resource_deltas` (delta neto por `resource_key`), no mediante una
   entidad `ResourceChange`.
1. Se permiten ajustes incrementales (`+/-`), ediciÃ³n manual directa del delta
   neto y limpieza de clave cuando el resultado es `0`.
1. La polÃ­tica de editabilidad amplia no elimina la validaciÃ³n de totales
   finales no negativos.
1. El modelo detallado se define en `docs/resource-delta-model.md` y el
   contrato de pre/postcondiciones/rechazos en `#12` (parcheado por supersesiÃ³n
   parcial de recursos).

## Reglas de estado y semana actual derivada (`Week.status`, concepto derivado)

### PolÃ­tica global de semana actual derivada

1. La **semana actual** del MVP se define como la **primera `Week` abierta**,
   es decir, la `Week` abierta con **menor `week_number`** entre las weeks
   provisionadas.
1. Navegar o seleccionar una `Week` para foco/ediciÃ³n no cambia automÃ¡ticamente
   la semana actual derivada.
1. La semana actual se trata como un valor derivado de la estructura de weeks
   abiertas y sus estados, en lugar de una selecciÃ³n manual libre.
1. **Nota de transiciÃ³n (`#76`)**: la implementaciÃ³n actual todavÃ­a
   persiste/consume `campaign.week_cursor` en cÃ³digo como mecanismo transitorio;
   la migraciÃ³n tÃ©cnica para retirarlo se sigue en `#81`.

### Reglas de recÃ¡lculo

La semana actual derivada se recalcula tras operaciones que puedan cambiar la
primera week abierta:

- `Week.close`
- `Week.reopen`
- `Week.reclose`
- provisiÃ³n inicial / extensiÃ³n temporal

### RelaciÃ³n con el ajuste manual previo de `week_cursor`

1. La semÃ¡ntica de `Campaign.set_week_cursor` como ajuste manual explÃ­cito (Issue
   `#9`) queda **sustituida** en MVP por la polÃ­tica derivada de cursor de esta
   decisiÃ³n (`#37`).
1. El detalle de la transiciÃ³n contractual se alinea en:
   - `docs/campaign-temporal-controls.md`
   - `docs/campaign-temporal-initialization.md`
   - `#12` (contrato por agregado)

### Invariante de existencia de week abierta (soporte de la semana actual)

1. Debe existir al menos una `Week` abierta provisionada para mantener
   una semana actual derivada vÃ¡lida.
1. Si una operaciÃ³n (`Week.close`/`Week.reclose`) dejara **0 weeks abiertas**,
   la operaciÃ³n se rechaza.

## Reglas para sesiones manuales

### `Session.manual_create`

1. Puede crear una sesiÃ³n histÃ³rica (con `ended_at_utc` definido) o activa
   (`ended_at_utc=null`).
1. Si crea una sesiÃ³n activa, debe validarse que no exista otra sesiÃ³n activa
   global en la campaÃ±a.

### `Session.manual_update`

1. Permite corregir timestamps de una sesiÃ³n existente.
1. Si la correcciÃ³n cambia el estado a activa (`ended_at_utc=null`), debe
   validarse la unicidad de sesiÃ³n activa global.
1. Si la correcciÃ³n cambia una sesiÃ³n activa a cerrada, la sesiÃ³n deja de contar
   como activa sin requerir `auto-stop`.

### `Session.manual_delete`

1. Permite borrar manualmente una sesiÃ³n histÃ³rica o activa.
1. Si se borra una sesiÃ³n activa, el resultado debe mantener `0..1` sesiones
   activas globales (normalmente `0`).

## Invariantes preservadas y modificadas

### Invariantes preservadas

- `0..1` `Session` activa global en la campaÃ±a.
- `week_number` global inmutable.
- ValidaciÃ³n de totales finales no negativos en recursos.
- JerarquÃ­a temporal `campaign > year > season > week > entry`.

### Invariantes modificadas / ampliadas

- Se sustituye â€œsin reordenaciÃ³n manual de `Entry` en MVPâ€ por:
  - reordenaciÃ³n manual permitida dentro de la misma `Week` con secuencia densa
    `1..N`.
- Se amplÃ­a la mutabilidad de `Week.status`:
  - se permiten `reopen` y `reclose`.
- Se amplÃ­a la mutabilidad de `Session`:
  - correcciones manuales completas (crear/editar/borrar).
- Se redefine la semana actual:
  - pasa a ser la primera `Week` abierta (menor `week_number` abierta).

## Impacto sobre conflictos y contratos downstream

### Impacto sobre `docs/conflict-policy.md` / Issue `#8`

- Se aÃ±aden/ajustan operaciones concurrentes de:
  - `Week.reopen`
  - `Week.reclose`
  - correcciones manuales de `Session`
  - reordenaciÃ³n manual de `Entry`
- Se mantiene la polÃ­tica de rechazo con `refresco` y `reintento`.

### Impacto sobre `#12` (contrato Firestore por agregado)

- AÃ±ade operaciones y precondiciones nuevas a documentar.
- Debe alinearse con:
  - hard delete real (input ya acordado)
  - `Entry.update` amplio (input ya acordado)
  - atomicidad descrita como comportamiento (sin tÃ©cnica obligatoria)

### Impacto sobre `#14`, `#15`, `#17`, `#19`

- `#14`: flujo de sesiÃ³n activa / `auto-stop` debe coexistir con correcciones
  manuales de sesiÃ³n y `Week.reopen/reclose`.
- `#15`: reglas de recursos deben considerar editabilidad en weeks cerradas y
  correcciones amplias sobre `Entry.resource_deltas`.
- `#17`: matriz de edge cases debe incorporar reordenaciÃ³n, reopen/reclose y
  correcciones manuales de sesiÃ³n.
- `#19`: el plan de pruebas de invariantes debe incluir los nuevos casos de
  cursor derivado y mutabilidad ampliada.

## Casos de aceptaciÃ³n / verificaciÃ³n documental

1. **Mover `Entry` dentro de una `Week`**
   - `order_index` queda denso `1..N`.
   - No hay movimiento entre weeks.
1. **Reabrir una `Week` cerrada**
   - `Week.status` cambia a `open`.
   - la semana actual derivada se recalcula a la primera week abierta.
1. **Re-cerrar una `Week` reabierta**
   - `Week.status` vuelve a `closed`.
   - la semana actual derivada se recalcula con la misma regla global.
1. **CorrecciÃ³n manual completa de `Session`**
   - Se permiten create/edit/delete con timestamps.
   - No se rompe la invariante `0..1` sesiÃ³n activa global.
1. **LÃ­mite de cursor vÃ¡lido**
   - Se rechaza una operaciÃ³n que deje `0` weeks abiertas provisionadas.
1. **AlineaciÃ³n con conflictos**
   - `docs/conflict-policy.md` queda coherente con la nueva editabilidad.
1. **Desbloqueo de `#12`**
   - `#12` puede redactarse con dominio actualizado y trazabilidad explÃ­cita.

## Riesgos y lÃ­mites

- Riesgo de ampliar demasiado el alcance de `#12` si no se separa claramente
  esta decisiÃ³n de dominio del contrato Firestore.
- Riesgo de contradicciÃ³n temporal si no se alinean `#9`, `#13` y esta decisiÃ³n
  respecto a la semana actual derivada (histÃ³ricamente `week_cursor`).
- Riesgo de aumentar edge cases concurrentes; se asume mitigaciÃ³n mediante la
  polÃ­tica de rechazo ya vigente en `#8`.

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

