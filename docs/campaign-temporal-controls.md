# Controles Temporales de CampaÃ±a (MVP)

## Metadatos

- `doc_id`: DOC-CAMPAIGN-TEMPORAL-CONTROLS
- `purpose`: Definir el contrato funcional de navegaciÃ³n temporal y provisiÃ³n/extensiÃ³n de aÃ±os en la pantalla principal del MVP.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar el contrato funcional del selector temporal superior (aÃ±o/semana) en la
pantalla principal Ãºnica del MVP, incluyendo la provisiÃ³n inicial y extensiÃ³n
manual de aÃ±os sin depender de una pantalla separada de ajustes de campaÃ±a solo
para esta funciÃ³n.

## Alcance MVP y no alcance

Incluye:

- ubicaciÃ³n funcional del control temporal en la barra superior;
- selector de aÃ±o y selector de semanas del aÃ±o seleccionado;
- provisiÃ³n inicial automÃ¡tica de aÃ±os en `campaign/01`;
- extensiÃ³n manual de aÃ±os (`+1`) con confirmaciÃ³n;
- semÃ¡ntica de navegaciÃ³n de semana vs semana actual derivada;
- patrÃ³n de UI del selector de entry al pulsar semana (a nivel de intenciÃ³n).

No incluye:

- detalle de creaciÃ³n de `year/season/week` (Issue #13);
- detalle del contenido y acciones del popover de entries (Issue #14 o
  equivalente);
- polÃ­ticas de conflicto/timestamps mÃ¡s allÃ¡ de las referencias a `#8` y `#18`;
- acciones destructivas de reset o reprovisiÃ³n completa de la estructura
  temporal.

## Estructura funcional de la pantalla principal (MVP)

- **Barra superior**:
  - navegaciÃ³n temporal (`year` + semanas);
  - acceso a provisiÃ³n/extensiÃ³n de aÃ±os;
  - reemplaza la funciÃ³n de navegaciÃ³n temporal de la barra izquierda del
    boceto anterior.
- **Zona central**:
  - formulario de la `Entry` actual (sin cambios de alcance en esta issue).
- **Barra inferior**:
  - totales de campaÃ±a (sin cambios de alcance en esta issue).

## Selector de aÃ±o

1. Muestra el aÃ±o actualmente seleccionado en la barra superior.
1. Permite navegaciÃ³n entre aÃ±os ya provisionados.
1. Si existen aÃ±os anteriores, se muestra acciÃ³n de navegaciÃ³n a la izquierda
   (`â†`).
1. Si existen aÃ±os posteriores ya provisionados, se muestra acciÃ³n de
   navegaciÃ³n a la derecha (`â†’`).
1. Si el aÃ±o seleccionado es el Ãºltimo aÃ±o provisionado, la acciÃ³n derecha se
   reemplaza por `+` para extensiÃ³n manual.

## Selector de semana

1. El selector de semanas muestra semanas del **aÃ±o seleccionado**.
1. Su funciÃ³n principal en esta issue es navegaciÃ³n/foco temporal.
1. Pulsar una semana **no cambia automÃ¡ticamente** la semana actual derivada
   (primera `Week` abierta).
1. Al pulsar una semana se abre el flujo de selecciÃ³n de entry (popover/modal
   anclado), definido en esta issue a nivel de patrÃ³n e intenciÃ³n.

## ProvisiÃ³n inicial de aÃ±os (automÃ¡tica)

1. La provisiÃ³n inicial ocurre automÃ¡ticamente al crear `campaign/01`.
1. El valor por defecto del MVP es **4 aÃ±os**.
1. Esta issue cierra el contrato funcional de provisiÃ³n inicial, pero no el
   detalle tÃ©cnico de cÃ³mo se crean `year/season/week` (Issue #13).

## ExtensiÃ³n manual de aÃ±os (`+1` con confirmaciÃ³n)

1. La extensiÃ³n de aÃ±os es manual y explÃ­cita en el MVP.
1. Cuando el selector estÃ¡ en el Ãºltimo aÃ±o provisionado, se muestra `+` en la
   posiciÃ³n de la acciÃ³n derecha.
1. Pulsar `+` solicita confirmaciÃ³n.
1. Tras confirmar, se aÃ±ade **1 aÃ±o** nuevo.
1. No hay extensiÃ³n automÃ¡tica por umbral en el MVP.

## PolÃ­tica de semana actual derivada (actualizaciÃ³n posterior de dominio y reencuadre `#76`)

1. La semÃ¡ntica original de ajuste manual explÃ­cito de `week_cursor` definida en
   esta issue fue **actualizada** por la Issue `#37`
   (`docs/editability-policy.md`).
1. El canon de producto/documentaciÃ³n vigente define la **semana actual** como
   concepto **derivado no persistido**: la primera `Week` abierta (menor
   `week_number` abierta), recalculada tras cambios de estado de `Week`.
1. Seleccionar semana para navegar/focalizar sigue siendo una acciÃ³n separada de
   la navegaciÃ³n temporal y no cambia automÃ¡ticamente la semana actual derivada.
1. El marcador visual de `current week` (derivado de la semana actual) y la
   selecciÃ³n `Week`/`Entry` usada por el flujo de sesiÃ³n se tratan como
   conceptos separados (ver `docs/active-session-flow.md`, Issue `#14`).
1. Default de arranque de pantalla principal (`#16`): la barra superior se
   sitÃºa en el aÃ±o de `current week`, pero la selecciÃ³n inicial de `Week` y
   `Entry` es vacÃ­a (`none`).
1. **Nota de transiciÃ³n (`#76`)**: la implementaciÃ³n actual del repo todavÃ­a
   persiste/lee `campaign.week_cursor` en backend/UI como mecanismo transitorio.
   La migraciÃ³n tÃ©cnica para retirar esa dependencia se sigue en `#81`.

## Click en semana y selector de entry (patrÃ³n + intenciÃ³n)

1. PatrÃ³n de UI adoptado: **popover/modal anclado** al control de semana.
1. IntenciÃ³n funcional:
   - permitir seleccionar la `Entry` a editar dentro de la semana;
   - mostrar estado vacÃ­o y/o acciÃ³n hacia creaciÃ³n cuando no existan entries.
1. El detalle del contenido del popover (layout, copy, orden y acciones de
   creaciÃ³n rÃ¡pida) queda fuera de esta issue y se difiere a Issue #14 o una
   issue especÃ­fica equivalente.

## LÃ­mites y dependencias

- **Issue #9** (esta decisiÃ³n): navegaciÃ³n temporal superior + provisiÃ³n/
  extensiÃ³n de aÃ±os + semÃ¡ntica de semana actual derivada (histÃ³ricamente
  referida como `week_cursor`).
- **Issue #13**: detalle tÃ©cnico de inicializaciÃ³n y extensiÃ³n de
  `year/season/week`.
- **Issue #14** (o equivalente): detalle del popover de entries y flujo de
  selecciÃ³n/creaciÃ³n de entry desde semana, incluyendo flujo de sesiÃ³n activa y
  separaciÃ³n entre `current week`, foco y activo (`docs/active-session-flow.md`).
- **Issue #16**: inventario mÃ­nimo de lecturas/consultas de pantalla principal
  (arranque sin selecciÃ³n, cargas por selecciÃ³n de week/entry y triggers de
  refresh on-demand).
- **Issue #12**: contrato de operaciones Firestore por agregado (implementaciÃ³n
  tÃ©cnica de operaciones como provisiÃ³n/extensiÃ³n/cambio de cursor).
- **Issue #37**: polÃ­tica de editabilidad manual del MVP y semÃ¡ntica derivada de
  la semana actual (primera `Week` abierta), que actualiza esta decisiÃ³n.
- **Issue #18**: timestamps y desempates de orden estable entre dispositivos.

## Referencias

- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/decision-log.md`
- `docs/editability-policy.md`
- `docs/active-session-flow.md`
- `docs/minimal-read-queries.md`
- `tdd.md` (retirado el 2026-03-01) (legado temporal, alineado con referencia oficial)
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/9`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`

