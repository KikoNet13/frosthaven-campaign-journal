# Política de Conflictos Concurrentes MVP

## Metadatos

- `doc_id`: DOC-CONFLICT-POLICY
- `purpose`: Definir la política de resolución de conflictos concurrentes del MVP.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar una política de conflictos concurrentes para Firestore en el MVP que
priorice simplicidad, previsibilidad y consistencia de datos, sin adelantar el
contrato técnico por agregado de la Issue #12 ni la política de timestamps y
desempates de la Issue #18.

## Alcance MVP y no alcance

Incluye:

- reglas de resolución de conflictos por familia de operación;
- reglas de precedencia y rechazo;
- flujo esperado de cliente tras conflicto (`refrescar` y `reintentar`);
- límites y dependencias con Issues #12 y #18.

No incluye:

- definición técnica exacta de transacciones/precondiciones por agregado
  (Issue #12);
- política de timestamps y desempate de orden estable (Issue #18);
- lock/lease explícito entre dispositivos;
- soporte offline con cola de escrituras.

## Principios de la política de conflictos

1. En el MVP se adopta una política **estricta de rechazo en conflicto** con
   `refresco` y `reintento`.
1. Se mantiene la recomendación operativa de `single writer` definida en
   `docs/sync-strategy.md`.
1. No se usa `last-write-wins` para operaciones de estado, edición de notas,
   reordenación manual ni edición de `Entry.resource_deltas`.
1. La política define comportamiento esperado; el mecanismo técnico exacto de
   detección queda para la Issue #12.

## Matriz de operaciones y resolución (MVP)

| Operación | Agregado principal | Riesgo de conflicto | Política MVP | Acción cliente | Notas / dependencias |
| --- | --- | --- | --- | --- | --- |
| `Session.start` | `campaign` + `entry` + `session` | Alto | `rechazar` | `refrescar` + `reintentar` | Depende de unicidad de sesión activa global; detalle técnico en #12 |
| `Session.stop` | `campaign` + `entry` + `session` | Alto | `rechazar` | `refrescar` + `reintentar` (conflicto) / error local (transición inválida) | Distinguir sesión ya cerrada (transición inválida) de base obsoleta; contrato en #12 |
| `auto-stop` por nuevo `start` | `campaign` + `session` | Alto | `rechazar` | `refrescar` + `reintentar` | No usar LWW sobre estado de sesión |
| `Week.close` | `week` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` (conflicto) / error local (transición inválida) | Distinguir `close` sobre `closed` (transición inválida) de base obsoleta; contrato en #12 |
| `Week.reopen` | `week` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` (conflicto) / error local (transición inválida) | Recalcula `week_cursor`; `reopen` sobre `open` es transición inválida |
| `Week.reclose` | `week` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` (conflicto) / error local (transición inválida/validación) | Recalcula `week_cursor`; rechazar si dejaría cursor inválido |
| `Entry.reorder_within_week` | `week` + `entry` | Medio/Alto | `rechazar` | `refrescar` + `reintentar` | Resecuencia densa `1..N`; detalle contractual en #12 |
| `Session.manual_create/update/delete` | `session` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` | Mantener `0..1` sesión activa global; detalle contractual en #12 |
| Borrado de `Entry` activa (con cascada) | `entry` + `session` + `campaign` | Alto | `rechazar` | `refrescar` + `reintentar` | Incluye auto-stop; borra `sessions` y elimina `resource_deltas` embebidos con la `Entry`; contrato técnico en #12 |
| Edición de `Week.notes` | `week` | Medio | `rechazar` | `refrescar` + reingresar cambios | No usar `last-write-wins` en MVP |
| `Entry.adjust_resource_delta` | `entry` (+ totales derivados) | Medio/Alto | `rechazar` | `refrescar` + `reintentar` | Ajusta delta neto en `Entry.resource_deltas`; valida totales finales no negativos |
| `Entry.set_resource_delta` | `entry` (+ totales derivados) | Alto | `rechazar` | `refrescar` + `reintentar` | Edición manual directa del delta neto; opera sobre `Entry` y totales |
| `Entry.clear_resource_delta` | `entry` (+ totales derivados) | Medio/Alto | `rechazar` | `refrescar` + `reintentar` | Elimina clave del mapa (`delta -> 0`); rechazar si base está obsoleta |

## Reglas de precedencia y rechazo

1. Si una entidad fue modificada por otro dispositivo desde la lectura base del
   cliente, la operación se **rechaza por conflicto**.
1. Si una entidad fue borrada (o marcada como borrada) concurrentemente,
   prevalece el estado remoto actual y la operación local se **rechaza**.
1. Si una operación específica define como precondición `Week.status=open` y la
   semana ya fue cerrada, la operación se **rechaza**.
1. Si una operación depende de la sesión activa global y esa condición cambió,
   la operación se **rechaza**.
1. Si una operación de cambio de estado de `Week` (`close`, `reopen`,
   `reclose`) encuentra que `week.status` o el recálculo de `week_cursor`
   quedó invalidado por cambios concurrentes, la operación se **rechaza** y
   requiere `refresco`.
1. Si una transición de estado solicitada ya no corresponde al estado actual
   (por ejemplo `Week.close` sobre `closed` o `Session.stop` sobre una sesión no
   activa), el rechazo puede clasificarse como **transición inválida** (no
   conflicto concurrente), con error local sin `refresco` por defecto.
1. Si el rechazo ocurre durante una operación compuesta (por ejemplo `auto-stop`
   + `start`, cierre/reapertura de semana, borrado con cascada), se considera
   fallo de la operación completa y se requiere `refresco`.
1. La precedencia de orden temporal fino y desempates entre eventos casi
   simultáneos queda fuera de esta issue y se define en la Issue #18.

## Flujo esperado tras conflicto (cliente)

1. Mostrar error de conflicto concurrente (mensaje breve en castellano).
1. Ejecutar `refresco` del estado relevante desde Firestore.
1. Recalcular foco/estado visible en la UI según la fuente de verdad.
1. Permitir `reintentar` manualmente si la acción sigue siendo válida.
1. No reintentar automáticamente en el MVP (para evitar efectos duplicados y
   comportamiento opaco).

## Flujo esperado tras rechazo funcional (transición inválida / validación)

1. Mostrar error local en castellano (transición inválida o validación).
1. No forzar `refresco` por defecto si el problema es puramente funcional.
1. Permitir corregir la acción y volver a intentar manualmente.

## Edge cases documentados

- Dos dispositivos intentan iniciar sesión activa casi a la vez.
  - Resultado MVP: uno de los intentos puede quedar inválido tras refresco;
    conflicto se resuelve por rechazo y reintento.
- Un dispositivo cierra una `Week` mientras otro edita `Week.notes`.
  - Resultado MVP: la edición depende del estado actual; si el estado cambió de
    forma incompatible, se rechaza y se refresca.
- Un dispositivo reabre una `Week` mientras otro la re-cierra o cierra una week
  distinta que afecta al `week_cursor`.
  - Resultado MVP: una de las operaciones puede quedar obsoleta; se rechaza y
    requiere `refresco`.
- Dos dispositivos reordenan entries de la misma `Week` a la vez.
  - Resultado MVP: rechazo en conflicto y reintento; no se aplica LWW.
- Corrección manual de sesión mientras otro dispositivo ejecuta `Session.start`
  o `Session.stop`.
  - Resultado MVP: rechazo en conflicto si cambia la condición de sesión activa
    global.
- Un dispositivo borra una `Entry` activa mientras otro registra recursos sobre
  esa `Entry`.
  - Resultado MVP: una de las operaciones quedará inválida; se rechaza la que
    opere sobre estado obsoleto.
- Ediciones concurrentes sobre `Entry.resource_deltas` de la misma `Entry`.
  - Resultado MVP: rechazo en conflicto; no `last-write-wins`.

## Dependencias y relación con otras Issues

- **Issue #7**: `docs/sync-strategy.md` define el marco de sincronización
  (`single writer`, `online-only writes`, `on-demand refresh`).
- **Issue #8**: esta política de conflictos concurrentes.
- **Issue #12**: define el contrato técnico por agregado y el mecanismo de
  detección/validación de conflictos, además de la distinción documental entre
  conflicto y transición inválida para operaciones de estado.
- **Issue #37**: actualiza la política de editabilidad manual del MVP y la
  semántica de `week_cursor`, añadiendo operaciones de corrección manual
  que deben respetar esta política de conflictos.
- **Issue #40**: redefine el modelo de recursos del MVP como
  `Entry.resource_deltas` (sin entidad `ResourceChange`) y actualiza la matriz
  de conflictos de recursos sobre `Entry`.
- **Issue #18**: define timestamps y desempates de orden estable entre
  dispositivos, compatibles con esta política.

## Referencias

- `docs/domain-glossary.md`
- `docs/sync-strategy.md`
- `docs/decision-log.md`
- `docs/firestore-operation-contract.md`
- `docs/resource-delta-model.md`
- `docs/timestamp-order-policy.md`
- `tdd.md` (legado temporal, alineado con referencia oficial)
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
