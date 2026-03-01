# PolÃ­tica de Conflictos Concurrentes MVP

## Metadatos

- `doc_id`: DOC-CONFLICT-POLICY
- `purpose`: Definir la polÃ­tica de resoluciÃ³n de conflictos concurrentes del MVP.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar una polÃ­tica de conflictos concurrentes para Firestore en el MVP que
priorice simplicidad, previsibilidad y consistencia de datos, sin adelantar el
contrato tÃ©cnico por agregado de la Issue #12 ni la polÃ­tica de timestamps y
desempates de la Issue #18.

## Alcance MVP y no alcance

Incluye:

- reglas de resoluciÃ³n de conflictos por familia de operaciÃ³n;
- reglas de precedencia y rechazo;
- flujo esperado de cliente tras conflicto (`refrescar` y `reintentar`);
- lÃ­mites y dependencias con Issues #12 y #18.

No incluye:

- definiciÃ³n tÃ©cnica exacta de transacciones/precondiciones por agregado
  (Issue #12);
- polÃ­tica de timestamps y desempate de orden estable (Issue #18);
- lock/lease explÃ­cito entre dispositivos;
- soporte offline con cola de escrituras.

## Principios de la polÃ­tica de conflictos

1. En el MVP se adopta una polÃ­tica **estricta de rechazo en conflicto** con
   `refresco` y `reintento`.
1. Se mantiene la recomendaciÃ³n operativa de `single writer` definida en
   `docs/sync-strategy.md`.
1. No se usa `last-write-wins` para operaciones de estado, ediciÃ³n de notas,
   reordenaciÃ³n manual ni ediciÃ³n de `Entry.resource_deltas`.
1. La polÃ­tica define comportamiento esperado; el mecanismo tÃ©cnico exacto de
   detecciÃ³n queda para la Issue #12.

## Matriz de operaciones y resoluciÃ³n (MVP)

| OperaciÃ³n | Agregado principal | Riesgo de conflicto | PolÃ­tica MVP | AcciÃ³n cliente | Notas / dependencias |
| --- | --- | --- | --- | --- | --- |
| `Session.start` | `campaign` + `entry` + `session` | Alto | `rechazar` | `refrescar` + `reintentar` | Depende de unicidad de sesiÃ³n activa global; detalle tÃ©cnico en #12 |
| `Session.stop` | `campaign` + `entry` + `session` | Alto | `rechazar` | `refrescar` + `reintentar` (conflicto) / error local (transiciÃ³n invÃ¡lida) | Distinguir sesiÃ³n ya cerrada (transiciÃ³n invÃ¡lida) de base obsoleta; contrato en #12 |
| `auto-stop` por nuevo `start` | `campaign` + `session` | Alto | `rechazar` | `refrescar` + `reintentar` | No usar LWW sobre estado de sesiÃ³n |
| `Week.close` | `week` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` (conflicto) / error local (transiciÃ³n invÃ¡lida) | Distinguir `close` sobre `closed` (transiciÃ³n invÃ¡lida) de base obsoleta; contrato en #12 |
| `Week.reopen` | `week` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` (conflicto) / error local (transiciÃ³n invÃ¡lida) | Recalcula `week_cursor`; `reopen` sobre `open` es transiciÃ³n invÃ¡lida |
| `Week.reclose` | `week` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` (conflicto) / error local (transiciÃ³n invÃ¡lida/validaciÃ³n) | Recalcula `week_cursor`; rechazar si dejarÃ­a cursor invÃ¡lido |
| `Entry.reorder_within_week` | `week` + `entry` | Medio/Alto | `rechazar` | `refrescar` + `reintentar` | Resecuencia densa `1..N`; detalle contractual en #12 |
| `Session.manual_create/update/delete` | `session` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` | Mantener `0..1` sesiÃ³n activa global; detalle contractual en #12 |
| Borrado de `Entry` activa (con cascada) | `entry` + `session` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` | Incluye auto-stop; borra `sessions` y elimina `resource_deltas` embebidos con la `Entry`; contrato tÃ©cnico en #12 |
| EdiciÃ³n de `Week.notes` | `week` | Medio | `rechazar` | `refrescar` + reingresar cambios | No usar `last-write-wins` en MVP |
| `Entry.adjust_resource_delta` | `entry` (+ totales derivados) | Medio/Alto | `rechazar` | `refrescar` + `reintentar` | Ajusta delta neto en `Entry.resource_deltas`; valida totales finales no negativos |
| `Entry.set_resource_delta` | `entry` (+ totales derivados) | Alto | `rechazar` | `refrescar` + `reintentar` | EdiciÃ³n manual directa del delta neto; opera sobre `Entry` y totales |
| `Entry.clear_resource_delta` | `entry` (+ totales derivados) | Medio/Alto | `rechazar` | `refrescar` + `reintentar` | Elimina clave del mapa (`delta -> 0`); rechazar si base estÃ¡ obsoleta |

## Reglas de precedencia y rechazo

1. Si una entidad fue modificada por otro dispositivo desde la lectura base del
   cliente, la operaciÃ³n se **rechaza por conflicto**.
1. Si una entidad fue borrada (o marcada como borrada) concurrentemente,
   prevalece el estado remoto actual y la operaciÃ³n local se **rechaza**.
1. Si una operaciÃ³n especÃ­fica define como precondiciÃ³n `Week.status=open` y la
   semana ya fue cerrada, la operaciÃ³n se **rechaza**.
1. Si una operaciÃ³n depende de la sesiÃ³n activa global y esa condiciÃ³n cambiÃ³,
   la operaciÃ³n se **rechaza**.
1. Si una operaciÃ³n de cambio de estado de `Week` (`close`, `reopen`,
   `reclose`) encuentra que `week.status` o el recÃ¡lculo de `week_cursor`
   quedÃ³ invalidado por cambios concurrentes, la operaciÃ³n se **rechaza** y
   requiere `refresco`.
1. Si una transiciÃ³n de estado solicitada ya no corresponde al estado actual
   (por ejemplo `Week.close` sobre `closed` o `Session.stop` sobre una sesiÃ³n no
   activa), el rechazo puede clasificarse como **transiciÃ³n invÃ¡lida** (no
   conflicto concurrente), con error local sin `refresco` por defecto.
1. Si el rechazo ocurre durante una operaciÃ³n compuesta (por ejemplo `auto-stop`
   + `start`, cierre/reapertura de semana, borrado con cascada), se considera
   fallo de la operaciÃ³n completa y se requiere `refresco`.
1. La precedencia de orden temporal fino y desempates entre eventos casi
   simultÃ¡neos queda fuera de esta issue y se define en la Issue #18.

## Flujo esperado tras conflicto (cliente)

1. Mostrar error de conflicto concurrente (mensaje breve en castellano).
1. Ejecutar `refresco` del estado relevante desde Firestore.
1. Recalcular foco/estado visible en la UI segÃºn la fuente de verdad.
1. Permitir `reintentar` manualmente si la acciÃ³n sigue siendo vÃ¡lida.
1. No reintentar automÃ¡ticamente en el MVP (para evitar efectos duplicados y
   comportamiento opaco).

## Flujo esperado tras rechazo funcional (transiciÃ³n invÃ¡lida / validaciÃ³n)

1. Mostrar error local en castellano (transiciÃ³n invÃ¡lida o validaciÃ³n).
1. No forzar `refresco` por defecto si el problema es puramente funcional.
1. Permitir corregir la acciÃ³n y volver a intentar manualmente.

## Edge cases documentados

- Dos dispositivos intentan iniciar sesiÃ³n activa casi a la vez.
  - Resultado MVP: uno de los intentos puede quedar invÃ¡lido tras refresco;
    conflicto se resuelve por rechazo y reintento.
- Un dispositivo cierra una `Week` mientras otro edita `Week.notes`.
  - Resultado MVP: la ediciÃ³n depende del estado actual; si el estado cambiÃ³ de
    forma incompatible, se rechaza y se refresca.
- Un dispositivo reabre una `Week` mientras otro la re-cierra o cierra una week
  distinta que afecta al `week_cursor`.
  - Resultado MVP: una de las operaciones puede quedar obsoleta; se rechaza y
    requiere `refresco`.
- Dos dispositivos reordenan entries de la misma `Week` a la vez.
  - Resultado MVP: rechazo en conflicto y reintento; no se aplica LWW.
- CorrecciÃ³n manual de sesiÃ³n mientras otro dispositivo ejecuta `Session.start`
  o `Session.stop`.
  - Resultado MVP: rechazo en conflicto si cambia la condiciÃ³n de sesiÃ³n activa
    global.
- Un dispositivo borra una `Entry` activa mientras otro registra recursos sobre
  esa `Entry`.
  - Resultado MVP: una de las operaciones quedarÃ¡ invÃ¡lida; se rechaza la que
    opere sobre estado obsoleto.
- Ediciones concurrentes sobre `Entry.resource_deltas` de la misma `Entry`.
  - Resultado MVP: rechazo en conflicto; no `last-write-wins`.

## Dependencias y relaciÃ³n con otras Issues

- **Issue #7**: `docs/sync-strategy.md` define el marco de sincronizaciÃ³n
  (`single writer`, `online-only writes`, `on-demand refresh`).
- **Issue #8**: esta polÃ­tica de conflictos concurrentes.
- **Issue #12**: define el contrato tÃ©cnico por agregado y el mecanismo de
  detecciÃ³n/validaciÃ³n de conflictos, ademÃ¡s de la distinciÃ³n documental entre
  conflicto y transiciÃ³n invÃ¡lida para operaciones de estado.
- **Issue #37**: actualiza la polÃ­tica de editabilidad manual del MVP y la
  semÃ¡ntica de `week_cursor`, aÃ±adiendo operaciones de correcciÃ³n manual
  que deben respetar esta polÃ­tica de conflictos.
- **Issue #40**: redefine el modelo de recursos del MVP como
  `Entry.resource_deltas` (sin entidad `ResourceChange`) y actualiza la matriz
  de conflictos de recursos sobre `Entry`.
- **Issue #15**: detalla validaciÃ³n y recÃ¡lculo de recursos (`Entry.resource_deltas`
  y `campaign.resource_totals`) y alinea la clasificaciÃ³n de rechazos sobre
  recursos con esta polÃ­tica.
- **Issue #18**: define timestamps y desempates de orden estable entre
  dispositivos, compatibles con esta polÃ­tica.
- **Issue #17**: traduce esta polÃ­tica y los contratos/flows relacionados a una
  matriz verificable de edge cases de concurrencia/sincronizaciÃ³n del MVP.

## Referencias

- `docs/domain-glossary.md`
- `docs/sync-strategy.md`
- `docs/decision-log.md`
- `docs/firestore-operation-contract.md`
- `docs/resource-delta-model.md`
- `docs/resource-validation-recalculation.md`
- `docs/timestamp-order-policy.md`
- `docs/concurrency-sync-edge-case-matrix.md`
- `tdd.md` (retirado el 2026-03-01) (legado temporal, alineado con referencia oficial)
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`

