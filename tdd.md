# Frosthaven Campaign Journal — TDD (v0.2)

## Objetivo

App Android (tablet horizontal) con **Flet (Python)** y **Firestore** para:

1. Registrar recursos globales de campaña con cambios `+/-` editables.
1. Mantener un diario mínimo por semanas con `Scenario` y `Outpost`.
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
1. Timeline por `Week` con `Scenario(s)` y `Outpost`.
1. Foco editable por entry y estado activo de cronómetro.
1. Registro de recursos con `+/-`, edición y borrado.
1. Totales globales derivados del log.
1. Temporizador `play/stop` para un único entry activo.
1. Campo de notas de `Week` (“secciones a leer”).

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

## Modelo temporal por semanas

- La campaña se organiza en `Weeks`.
- Cada `Week` contiene:
  - `1..N` `Scenarios`.
  - `1` `Outpost`.
- Existe `week_cursor` como semana actual.
- `week_cursor` avanza al finalizar el `Outpost`.

## Tiempo de juego (sesión)

- Una sesión es tiempo `start/stop` asociado a `Scenario` o `Outpost`.
- Puede ser intervalo único o múltiples intervalos.
- Solo puede haber `0..1` entry activo a la vez.

## Pantalla principal única

### Zona izquierda: timeline

- Muestra weeks y su cursor actual.
- Muestra `FOCO` y `ACTIVO`.
- Acción `+ Escenario` solo en la semana actual.

### Zona derecha: panel de edición

- Si foco = `Scenario/Outpost`:
  - Controles rápidos `+/-` por recurso.
  - Log editable de cambios.
- Si foco = `Week`:
  - Notas de “secciones a leer”.
  - Lista de entries de la week.

### Barra inferior fija

- Totales globales.
- Tiempo `hh:mm` del entry activo.
- Acción `Play/Stop`.
- Identificador del activo (`Scenario #` o `Outpost`).

## Cambios de recursos (log)

- Cada pulsación `+/-` crea un cambio con timestamp.
- Totales globales derivados de la suma de cambios.
- Cambios editables y borrables con recálculo.

## Extensibilidad prevista

- Catálogo de escenarios con búsqueda (v2).
- Snapshot informativo de totales por entry.
- Multi campaña (v3) sin refactor mayor.

## Decisiones pendientes

- Representación de tiempo: intervalo único o múltiples.
- Estructura mínima Firestore.
- Estrategia de sincronización multi dispositivo.
- Política de conflictos concurrentes.
