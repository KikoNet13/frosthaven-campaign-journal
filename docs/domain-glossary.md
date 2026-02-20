# Glosario de Dominio e Invariantes

## Metadatos

- `doc_id`: DOC-DOMAIN-GLOSSARY
- `purpose`: Definir entidades de dominio, invariantes y casos borde.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-06

## Alcance

Este documento cierra definiciones funcionales para:

- `Week`
- `Scenario`
- `Outpost`
- `Session`
- `ResourceChange`

No define todavía detalle final de rutas Firestore ni sincronización de runtime.

## Entidades de dominio

### Week

- Concepto de dominio:
  - Unidad temporal abstracta de campaña.
  - Contiene escenarios y un outpost.
  - Puede tener notas de “secciones a leer”.
- Detalle de implementación:
  - `week_number` entero positivo.
  - `notes` texto opcional.
  - `status` recomendado: `open|closed`.

### Scenario

- Concepto de dominio:
  - Entry jugable dentro de una `Week`.
  - Acumula cambios de recursos y tiempo de sesión.
- Detalle de implementación:
  - `scenario_index` entero secuencial dentro de la week.
  - `title` opcional para futuras versiones.
  - `is_active` derivado de sesión abierta.

### Outpost

- Concepto de dominio:
  - Entry único de gestión de ciudad dentro de una `Week`.
  - Marca el cierre operativo de la week.
- Detalle de implementación:
  - Cardinalidad exacta: uno por week.
  - `is_active` derivado de sesión abierta.

### Session

- Concepto de dominio:
  - Tiempo de juego asociado a un entry (`Scenario` o `Outpost`).
  - Puede contener uno o varios intervalos por pausas.
- Detalle de implementación:
  - Colección de intervalos con `started_at` y `ended_at`.
  - Se permite un único intervalo abierto por entry.
  - Duración total derivada de la suma de intervalos cerrados
    más el intervalo abierto, si existe.

### ResourceChange

- Concepto de dominio:
  - Evento atómico de cambio de recurso causado por acción del usuario.
  - Es la base para recalcular totales.
- Detalle de implementación:
  - `resource_key` (inglés) del catálogo permitido.
  - `delta` entero distinto de cero.
  - `created_at` y metadatos de edición opcionales.
  - Referencia obligatoria a entry (`Scenario` o `Outpost`).

## Invariantes operativas

1. `campaign_id` fijo: `campaign/01`.
1. Existe un único `week_cursor` global.
1. `week_cursor` apunta a una week existente.
1. Cada `Week` tiene exactamente un `Outpost`.
1. Cada `Week` tiene `1..N` `Scenario`.
1. `scenario_index` es único dentro de la misma week.
1. Un entry pertenece a una sola week.
1. Solo puede existir `0..1` entry activo en toda la campaña.
1. El entry activo debe pertenecer a la `week_cursor`.
1. La week avanza cuando se cierra el `Outpost` de la week actual.
1. Cada `ResourceChange` referencia un único entry válido.
1. `delta` de `ResourceChange` nunca puede ser `0`.
1. `resource_key` debe pertenecer al catálogo autorizado.
1. Totales globales se calculan por suma de `ResourceChange`.
1. Editar o borrar un cambio obliga a recálculo de totales.
1. Para cada intervalo de sesión cerrado: `started_at < ended_at`.
1. En un mismo entry no puede haber intervalos solapados.
1. Un entry no puede tener más de un intervalo abierto simultáneo.
1. Al cerrar intervalo abierto, el entry deja de estar activo.
1. No se permite crear semana nueva si la actual no tiene `Outpost` cerrado.

## Casos borde a controlar

1. Dos dispositivos intentan activar entries distintos al mismo tiempo.
1. Edición concurrente del mismo `ResourceChange`.
1. Borrado de cambio histórico que impacta totales actuales.
1. Intento de dejar `Week` sin `Outpost`.
1. Intento de cerrar week sin escenarios válidos.
1. Intervalo con `ended_at` anterior a `started_at`.
1. Intervalos de una sesión que se superponen por error de cliente.
1. Cambio con `resource_key` fuera de catálogo.
1. Cambio que provoca total negativo en recurso restringido.
1. Avance de `week_cursor` sin cerrar `Outpost`.

## Decisiones pendientes relacionadas

1. Estrategia exacta de persistencia en Firestore (ADR posterior).
1. Política final de resolución de conflictos concurrentes.
1. Regla definitiva para permitir o bloquear totales negativos por recurso.
