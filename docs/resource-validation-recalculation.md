# Reglas de Validación y Recálculo de Recursos (MVP)

## Metadatos

- `doc_id`: DOC-RESOURCE-VALIDATION-RECALCULATION
- `purpose`: Definir las reglas del MVP para validar operaciones sobre `Entry.resource_deltas` y recalcular/consistir `campaign.resource_totals` sin permitir totales finales negativos.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Cerrar las reglas documentales de validación y recálculo de recursos del MVP
para que las operaciones sobre `Entry.resource_deltas` produzcan resultados
trazables, consistentes y alineados con concurrencia (`#8`), contrato por
agregado (`#12`) y modelo embebido de recursos (`#40`).

## Alcance y no alcance

Incluye:

- inventario de operaciones de recursos del MVP (`adjust`, `set`, `clear`);
- validaciones por operación sobre `Entry.resource_deltas`;
- estrategia de recálculo y consistencia de `campaign.resource_totals`;
- reglas de rechazo esperadas y respuesta cliente recomendada;
- manejo de correcciones/borrados de `Entry` con impacto en recursos;
- alineación con `#8`, `#12`, `#37`, `#40` y glosario.

No incluye:

- técnica Firestore exacta (transacción, batch, precondiciones técnicas);
- diseño UI de controles `+/-` o edición manual de recursos;
- política de timestamps/desempates (`#18`);
- código de app.

## Entradas y prerrequisitos

- `docs/domain-glossary.md`
- `docs/conflict-policy.md` (Issue `#8`)
- `docs/firestore-operation-contract.md` (Issue `#12`)
- `docs/editability-policy.md` (Issue `#37`)
- `docs/resource-delta-model.md` (Issue `#40`)
- `docs/timestamp-order-policy.md` (Issue `#18`)
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`

## Operaciones de recursos cubiertas (MVP)

### Tabla 1 — Inventario de operaciones de recursos (`I15-S1`)

| `operation_id` | `trigger_funcional` | `agregados_afectados` | `resource_key_scope` | `efecto_sobre_totales` | `notas` |
| --- | --- | --- | --- | --- | --- |
| `Entry.adjust_resource_delta` | tap `+/-` o ajuste incremental en una `Entry` | `entry`, `campaign` | una `resource_key` | recalcula/ajusta `campaign.resource_totals` para la clave afectada | permitido en weeks `open|closed` |
| `Entry.set_resource_delta` | edición manual directa del delta neto de un recurso en una `Entry` | `entry`, `campaign` | una `resource_key` | recalcula/ajusta `campaign.resource_totals` para la clave afectada | si valor final `0`, normaliza a `clear` |
| `Entry.clear_resource_delta` | limpieza explícita del delta neto de un recurso en una `Entry` | `entry`, `campaign` | una `resource_key` | recalcula/ajusta `campaign.resource_totals` para la clave afectada | idempotente si la clave ya no existe |
| `Entry.delete` (impacto recursos) | borrado de `Entry` (manual) | `entry`, `campaign` (+ `session` por cascada) | todas las claves de `entry.resource_deltas` | elimina la contribución de la `Entry` a `campaign.resource_totals` | `#15` cubre solo la parte de recursos; cascada/auto-stop siguen en `#12` |

## Convenciones y notación de cálculo

1. `resource_key`:
   - debe pertenecer al catálogo MVP (`docs/domain-glossary.md`);
   - se trata como clave de mapa.
1. `entry.resource_deltas[resource_key]`:
   - ausencia de clave == delta `0`;
   - no se persisten claves con valor `0`.
1. `campaign.resource_totals[resource_key]`:
   - ausencia de clave == total `0` para cálculo/validación;
   - si una clave materializada queda en `0` tras una operación, se conserva
     explícitamente con valor `0`;
   - claves nunca usadas pueden permanecer ausentes.
1. Para una operación sobre una clave `k`:
   - `entry_before = delta neto previo de k en la Entry` (ausencia => `0`)
   - `entry_after = delta neto resultante de k en la Entry`
   - `entry_delta_change = entry_after - entry_before`
   - `campaign_before = total previo de k en campaign.resource_totals` (ausencia => `0`)
   - `campaign_after = campaign_before + entry_delta_change`

## Reglas de validación por operación

### Tabla 2 — Validaciones y rechazos (`I15-S2`)

| `operation_id` | `payload_requerido` | `validaciones_payload` | `validaciones_dominio` | `rechazos_esperados` | `categoria_rechazo` | `respuesta_cliente_recomendada` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `Entry.adjust_resource_delta` | `entry_id`, `resource_key`, `adjustment_delta` | `resource_key` válida; `adjustment_delta` entero firmado | `campaign_after >= 0`; si `entry_after = 0` se elimina la clave; weeks `open|closed` permitidas | `resource_key` inválida; payload inválido; total final negativo; base obsoleta | `validacion` / `conflicto` | error local si validación; `refrescar + reintentar` si conflicto | `adjustment_delta = 0` se admite como no-op idempotente |
| `Entry.set_resource_delta` | `entry_id`, `resource_key`, `target_delta` | `resource_key` válida; `target_delta` entero firmado | `campaign_after >= 0`; si `target_delta = 0` normaliza a `clear`; weeks `open|closed` permitidas | `resource_key` inválida; payload inválido; total final negativo; base obsoleta | `validacion` / `conflicto` | error local si validación; `refrescar + reintentar` si conflicto | fijar el mismo valor se admite como no-op idempotente |
| `Entry.clear_resource_delta` | `entry_id`, `resource_key` | `resource_key` válida | quitar contribución de la `Entry`; `campaign_after >= 0`; weeks `open|closed` permitidas | `resource_key` inválida; total final negativo (si detecta drift); base obsoleta | `validacion` / `conflicto` | error local si validación; `refrescar + reintentar` si conflicto | limpiar clave inexistente es idempotente (sin error) |
| `Entry.delete` (impacto recursos) | `entry_id` | `entry_id` válida | sustrae todas las contribuciones de la `Entry`; no debe dejar totales negativos; coherencia con borrado/cascada | entry ya borrada; base obsoleta; inconsistencia de totales detectada | `transicion_invalida` / `conflicto` / `validacion` | error local si transición/validación; `refrescar + reintentar` si conflicto | clasificación de cascada/auto-stop se hereda de `#12`; aquí se centra la parte de totales |

### Reglas adicionales de validación

1. No se aceptan `resource_key` fuera del catálogo MVP.
1. No se aceptan deltas no enteros (float, string, `null`, etc.).
1. El criterio de validez es el **estado final** de totales:
   - se permiten deltas negativos en una `Entry`;
   - se rechaza únicamente si el total global resultante de un recurso queda
     negativo.
1. La editabilidad de recursos es válida en weeks `open|closed` (por `#37`);
   `Week.status=closed` no es rechazo por sí mismo.
1. La ausencia de clave en `entry.resource_deltas` o `campaign.resource_totals`
   equivale a valor `0` para cálculo y validación.

## Estrategia de recálculo y consistencia de totales (`I15-S3`)

### Invariante de consistencia (fuente de verdad documental)

Para cada `resource_key` del catálogo MVP:

- `campaign.resource_totals[k] == Σ entry.resource_deltas[k]` sobre todas las
  `Entry` persistidas de la campaña (tomando ausencia de clave como `0`).

Además:

- ningún total final puede ser negativo;
- `campaign.resource_totals` puede omitir claves nunca usadas;
- si una clave materializada queda en `0`, se conserva explícitamente con valor
  `0`;
- no se persisten claves fuera del catálogo MVP.

### Estrategia de recálculo (nivel de comportamiento, no técnico)

1. El resultado observable de cualquier operación de recursos debe ser
   **equivalente** a recalcular `campaign.resource_totals` desde el estado final
   de `Entry.resource_deltas`.
1. Para operaciones sobre una sola `resource_key` (`adjust`, `set`, `clear`),
   el comportamiento esperado puede calcularse con actualización por diferencia
   de esa clave:
   - `campaign_after = campaign_before + (entry_after - entry_before)`
1. Para `Entry.delete`, el comportamiento esperado es sustraer la contribución
   de **todas** las claves presentes en `entry.resource_deltas` antes del
   borrado (equivalente a recalcular desde el conjunto de entries restante).
1. Si el resultado de una clave queda `0`, se conserva la clave con valor `0`
   en `campaign.resource_totals` cuando la clave ya estaba materializada; las
   claves nunca usadas pueden permanecer ausentes.
1. `#15` no fija si la implementación materializa esto como:
   - recálculo completo;
   - actualización incremental por diferencia;
   - o combinación con checks de consistencia.
   Solo fija el resultado observable y las validaciones.

### Coherencia con atomicidad de `#12`

1. `#12` ya exige atomicidad de comportamiento para:
   - `Entry.adjust_resource_delta`
   - `Entry.set_resource_delta`
   - `Entry.clear_resource_delta`
   - `Entry.delete` (incluyendo impacto en recursos por borrar la `Entry`)
1. `#15` precisa **qué** debe considerarse consistente dentro de ese resultado:
   - `Entry.resource_deltas` normalizado;
   - `campaign.resource_totals` consistente;
   - no negatividad preservada.

## Reglas de rechazo y recuperación (alineación con `#8` y `#12`)

### Tabla 3 — Matriz de rechazos de recursos (`I15-S4`)

| `error_case_id` | `operacion` | `trigger` | `categoria` | `feedback_esperado` | `accion_usuario_recomendada` | `requiere_refresh` | `notas` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `resource_invalid_key` | `adjust/set/clear` | `resource_key` fuera de catálogo MVP | `validacion` | error local | corregir recurso/entrada | No | payload inválido |
| `resource_invalid_delta_payload` | `adjust/set` | delta no entero o payload inválido | `validacion` | error local | corregir valor | No | `#15` no define UX concreta |
| `resource_negative_total_result` | `adjust/set/clear` | el total final del recurso quedaría `< 0` | `validacion` | error local de validación | corregir delta o revisar base | No (por defecto) | si la UI sospecha base obsoleta puede ofrecer refresh manual |
| `resource_conflict_obsolete_base` | `adjust/set/clear` | base de `Entry`/totales cambió concurrentemente | `conflicto` | error de conflicto | `refrescar + reintentar` | Sí | política estricta de `#8` |
| `resource_clear_missing_key` | `clear` | la clave ya no existe en la `Entry` | *sin error* | no-op silencioso o feedback neutro | ninguna | No | idempotente por decisión de `#15` |
| `resource_delete_entry_conflict` | `Entry.delete` (impacto recursos) | entry/totales obsoletos durante borrado | `conflicto` | error de conflicto | `refrescar + reintentar` | Sí | cascada/auto-stop heredados de `#12` |
| `resource_delete_entry_not_found` | `Entry.delete` (impacto recursos) | entry ya no existe | `transicion_invalida` | error local | refrescar si necesita confirmar estado | No (por defecto) | coherente con `#12` |
| `resource_inconsistent_totals_detected` | cualquiera | el cálculo detecta drift/imposible preestado | `conflicto` (recomendado) | error de conflicto / estado desincronizado | `refrescar` y reintentar | Sí | si persiste tras refresh, escalar como incidencia de integridad |

### Regla de clasificación

1. `validacion`:
   - payload inválido o resultado final inválido (totales negativos).
1. `conflicto`:
   - base obsoleta o inconsistencia detectada que invalida la confianza en el
     estado local.
1. `transicion_invalida`:
   - solo aplica aquí por efecto heredado de `Entry.delete` cuando la `Entry` ya
     no existe.

## Manejo de correcciones y borrados (aceptación de la issue)

### Correcciones (`adjust`, `set`, `clear`)

1. Las correcciones de recursos operan sobre `Entry.resource_deltas` (no existe
   log incremental `ResourceChange` en MVP).
1. Se permite corregir recursos en weeks `open|closed`.
1. `set` a `0` y `adjust` que resulta en `0` normalizan a eliminación de clave.
1. `clear` de clave inexistente es idempotente (sin error).

### Borrado de `Entry`

1. El borrado de `Entry` elimina implícitamente los `resource_deltas` al borrar
   la `Entry` (modelo embebido de `#40`).
1. `#15` exige que `campaign.resource_totals` deje de incluir la contribución de
   esa `Entry` tras el borrado exitoso.
1. `#15` no redefine la cascada de `sessions` ni el `auto-stop` (quedan en
   `#12` y `#14`).

## Alineación con documentos oficiales

### `docs/firestore-operation-contract.md` (`#12`)

1. `#12` define operaciones y atomicidad de comportamiento.
1. `#15` define el detalle de validación y consistencia/re-cálculo esperado de
   recursos para esas operaciones.

### `docs/resource-delta-model.md` (`#40`)

1. `#40` define el modelo (`Entry.resource_deltas`, delta neto, clave `0`
   eliminada).
1. `#15` define cómo validar y recalcular totales globales a partir de ese
   modelo.

### `docs/conflict-policy.md` (`#8`)

1. `#8` mantiene política estricta de rechazo por conflicto.
1. `#15` especifica cómo clasificar errores funcionales de recursos vs
   conflictos e inconsistencias de base.

### `docs/editability-policy.md` (`#37`)

1. `#15` respeta que recursos son editables en weeks `open|closed`.
1. `#15` no reabre la política de editabilidad; solo la usa como precondición.

## Casos de aceptación / verificación documental

1. `Entry.adjust_resource_delta` con taps repetidos sobre la misma clave calcula
   un delta neto único y actualiza totales globales de forma consistente.
1. `Entry.set_resource_delta` con `target_delta = 0` elimina la clave en
   `entry.resource_deltas` y aplica la regla de representación de
   `campaign.resource_totals`:
   - clave `0` explícita si la clave estaba materializada;
   - ausencia de clave si no tenía uso previo.
1. `Entry.clear_resource_delta` sobre clave inexistente es idempotente (sin
   error).
1. Se rechaza cualquier operación que deje un total global final negativo.
1. La validación se hace sobre el estado final, no sobre el signo del delta en
   sí mismo.
1. Borrar una `Entry` elimina su contribución de recursos del total global.
1. Weeks `closed` no bloquean las operaciones de recursos por sí mismas.
1. Los conflictos de recursos se resuelven con `refrescar + reintentar`.
1. La documentación deja trazable la diferencia entre:
   - `validacion` (resultado final inválido);
   - `conflicto` (base obsoleta/inconsistente);
   - `transicion_invalida` (solo heredada por `Entry.delete` no encontrada).

## Riesgos, límites y decisiones diferidas

- La técnica exacta para materializar el recálculo (incremental vs recompute
  completo) queda para implementación; `#15` fija equivalencia de resultado.
- El comportamiento visual exacto de errores (toast/inline/modal) queda fuera de
  alcance.
- El tratamiento de una inconsistencia persistente tras `refresh` (incidencia de
  integridad) se documenta aquí como escalación conceptual, pero no define
  tooling operativo.

## Supuestos explícitos (registro)

1. `campaign.resource_totals` **no** usa la misma normalización de persistencia
   que `entry.resource_deltas`:
   - ausencia de clave == `0` para cálculo/validación;
   - conservar clave explícita con valor `0` cuando una clave materializada
     queda en `0`;
   - las claves nunca usadas pueden permanecer ausentes.
1. `adjustment_delta = 0` y `set` al mismo valor se aceptan como no-op
   idempotente para simplificar clientes.
1. Una inconsistencia detectada de totales/base se clasifica como `conflicto`
   (no como `validacion`) para forzar `refresh` y evitar operar sobre una base
   no confiable.

## Referencias

- `AGENTS.md`
- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/firestore-operation-contract.md`
- `docs/resource-delta-model.md`
- `docs/editability-policy.md`
- `docs/timestamp-order-policy.md`
- `docs/decision-log.md`
- `docs/mvp-implementation-checklist.md`
- `docs/mvp-implementation-blocks.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
