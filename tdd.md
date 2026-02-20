# Frosthaven Campaign Journal - TDD (v0.2)

## Objetivo

App Android (tablet horizontal) con **Flet (Python)** y **Firestore** para:

1. Registrar recursos globales de campaña con cambios `+/-` editables.
1. Mantener un diario mínimo por semanas con entries de tipo `scenario` y
   `outpost`.
1. Registrar tiempo del entry activo con cronómetro.

## Problema a resolver

En papel, el borrado y reescritura de totales degrada legibilidad y aumenta
errores. La app debe permitir:

- Registrar cambios incrementales de recursos.
- Ver totales globales claros y consistentes.
- Editar o borrar cambios para corregir errores.

## Stack decidido

- UI: Flet (Python).
- Base de datos: Firestore (plan gratuito).
- Sin login, usuarios ni PIN.
- Campaña única fija: `campaign/01`.
- Multi dispositivo con lectura y escritura.

## Alcance MVP (datos globales)

Claves internas en inglés:

- Materiales: `lumber`, `metal`, `hide`.
- Plantas: `arrowvine`, `axenut`, `corpsecap`, `flamefruit`, `rockroot`,
  `snowthistle`.
- Otros: `inspiration`, `morale`, `soldiers`.

UI:

- Etiquetas y tooltips en castellano.
- Icono informativo por recurso.

## Alcance MVP v1 aprobado (Issue #5)

Incluye:

1. Pantalla única con tres zonas:
   - timeline,
   - panel de foco,
   - barra inferior.
1. Campaña única `campaign/01` sin login.
1. Timeline por `Week` con entries de tipo `scenario` y `outpost`.
1. Foco editable por entry y estado activo de cronómetro.
1. Registro de recursos con `+/-`, edición y borrado.
1. Totales globales derivados del log.
1. Temporizador `play/stop` para un único entry activo.
1. Campo de notas de `Week` ("secciones a leer").

No incluye en MVP:

1. Oro, XP, recursos de personaje, prosperity, perks y pegatinas.
1. Catálogo avanzado de escenarios.
1. Multi campaña.
1. Automatización de `.apk` en release.

## Criterios de éxito MVP

1. Se puede registrar una semana completa sin papel.
1. Se pueden corregir errores de log sin romper totales.
1. Estado activo y tiempo visibles y consistentes.

## No objetivos MVP

- Oro, XP o recursos de personaje.
- Prosperity.
- Perks, pegatinas o retirados.
- Cálculos de defensa total.
- Calendario real por fechas.

## Modelo de dominio cerrado (Issue #6)

- Entidad unificada `Entry` con `type=scenario|outpost`.
- Jerarquía temporal explícita:
  `campaign > year > season > week > entry`.
- `week_number` global `1..N`, inmutable y trazable.
- `scenario_ref` obligatorio para `Entry` de tipo `scenario`.
- `order_index` define orden en timeline (sin reordenación manual en MVP).
- `Session` y `ResourceChange` cuelgan de `Entry` por ruta (sin `owner_type`).

## Modelo temporal por semanas

- La campaña se organiza en years y seasons, con weeks globales.
- Cada `Week` contiene `0..N` entries (`scenario|outpost`).
- Existe `week_cursor` como semana actual.
- Al cerrar una week, avanza el cursor.
- Si hay sesión activa al cerrar week, se hace auto-stop y luego cierre.

## Tiempo de juego (sesión)

- Una sesión es un intervalo `start/stop` asociado a `Entry`.
- Se permite histórico de múltiples intervalos por entry.
- Solo puede haber `0..1` entry activo a la vez en toda la campaña.
- Si se inicia otra sesión con una activa, la anterior se cierra automáticamente.

## Pantalla principal única

### Zona izquierda: timeline

- Muestra weeks y su cursor actual.
- Muestra `FOCO` y `ACTIVO`.
- Acción de creación de entry en la week actual.

### Zona derecha: panel de edición

- Si foco = `Entry`:
  - Controles rápidos `+/-` por recurso.
  - Log editable de cambios.
- Si foco = `Week`:
  - Notas de "secciones a leer".
  - Lista de entries de la week.

### Barra inferior fija

- Totales globales.
- Tiempo `hh:mm` del entry activo.
- Acción `Play/Stop`.
- Identificador del activo (`Scenario #` o `Outpost`).

## Cambios de recursos (log)

- Cada pulsación `+/-` crea un cambio con timestamp.
- El cambio se guarda como `delta` entero firmado.
- Totales globales derivados de la suma de cambios.
- Cambios editables y borrables con recálculo.
- La validación exige que el estado final de totales no sea negativo.

## Preesquema Firestore mínimo cerrado

- `campaigns/01/years/{year_number}`
- `campaigns/01/years/{year_number}/seasons/{season_type}`
- `campaigns/01/years/{year_number}/seasons/{season_type}/weeks/{week_number}`
- `.../weeks/{week_number}/entries/{entry_id}`
- `.../entries/{entry_id}/sessions/{session_id}`
- `.../entries/{entry_id}/resource_changes/{change_id}`

## Extensibilidad prevista

- Catálogo de escenarios con búsqueda (v2).
- Snapshot informativo de totales por entry.
- Multi campaña (v3) sin refactor mayor.

## Decisiones pendientes

- Estrategia de sincronización multi dispositivo.
- Política de conflictos concurrentes.
- Proceso de provisión inicial de años (por ejemplo, crear 4 años).
