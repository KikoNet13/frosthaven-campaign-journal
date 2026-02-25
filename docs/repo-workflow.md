# Flujo de Repositorio

## Metadatos

- `doc_id`: DOC-REPO-WORKFLOW
- `purpose`: Definir el flujo Git y GitHub adoptado.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-25
- `next_review`: 2026-03-11

## Objetivo

Aplicar un flujo profesional, simple y mantenible para un solo desarrollador.

## Modelo adoptado

- GitHub Flow minimalista.
- Rama principal: `main`.
- Fuente principal de tareas: GitHub Issues.

## Reglas de ramas

- Para trabajo no trivial:
  - crear Issue
  - crear rama desde `main`
  - nomenclatura `tipo/<issue-id>-slug`
- Para trabajo trivial:
  - se permite commit y push directo a `main`
- `main` es la rama principal del repositorio, pero el trabajo directo a
  `main` se reserva para cambios triviales y aislados.

## Flujo recomendado con Codex

1. Kiko pide objetivo o cambio.
1. Codex lo traduce a unidades ejecutables.
1. Si hay varias unidades, se crean Issues separadas.
1. Si una unidad es no trivial, va en rama con patrón
   `tipo/<issue-id>-slug`.
1. Si una unidad es trivial y aislada, puede ir a `main`.
1. Si una unidad se ejecuta en rama, la Issue asociada se cierra tras integrar
   el trabajo en `main` (merge/PR), salvo instrucción explícita de Kiko.
1. Codex reporta siempre:
   - qué unidad ejecutó,
   - qué commit generó,
   - qué Issue cerró o dejó abierta.

### Reglas de priorización conversacional (`siguiente paso`, `siguiente pendiente`)

- `siguiente pendiente` y `siguiente issue pendiente` son equivalentes.

- Si Kiko pide `siguiente pendiente`, Codex selecciona por defecto la Issue
  abierta (`state=open`) con número más bajo.
- Si Kiko indica filtros (por ejemplo `type`, `label` o `phase`), Codex aplica
  esos filtros antes de ordenar por número.
- Si no hay Issues abiertas que cumplan el criterio, Codex lo reporta de forma
  explícita.

#### Regla de `siguiente paso`

- Codex revisa primero si existe una **unidad pendiente de cierre**.
- Si existe una unidad pendiente de cierre, el siguiente paso es resolver esa
  unidad antes de iniciar trabajo nuevo.
- Solo si no existe una unidad pendiente de cierre, Codex revisa las PRs
  abiertas del repo (incluyendo `draft`).
- Si hay varias PRs abiertas, prioriza la PR con número más bajo.
- Si existe al menos una PR abierta, el siguiente paso es llevar esa PR a
  cierre (merge o cierre explícito si se descarta).
- Si no hay PRs abiertas, Codex busca un **orden técnico recomendado** en la
  documentación oficial aplicable.
- Si existe orden técnico recomendado:
  - usa la fuente oficial más específica disponible (detalle > macro);
  - recorre el orden y elige la primera Issue abierta **cerrable**;
  - si una Issue abierta no es cerrable, la salta y evalúa la siguiente;
  - si no hay Issues cerrables en ese orden, elige la primera Issue
    `draftable`.
- Si no existe orden técnico aplicable, el siguiente paso es resolver la
  `siguiente pendiente` (`siguiente issue pendiente`).
- Definición operativa para esta regla:
  - `unidad pendiente de cierre`: unidad ya iniciada (issue/rama/PR asociada)
    que todavía no completó su pipeline de cierre. Se detecta en este orden de
    prioridad:
    1. trabajo local sin commit relacionado con la unidad activa;
    1. commit(s) locales en rama sin `push`;
    1. rama publicada con trabajo de la unidad pero sin PR (cuando corresponde
       PR por reglas del repo);
    1. PR abierta (incluyendo `draft`);
    1. PR mergeada pero Issue asociada aún abierta;
    1. rama local/remota mergeada pendiente de limpieza.
  - `cerrable`: Issue abierta con dependencias de cierre satisfechas según la
    documentación oficial vigente.
  - `draftable`: Issue abierta que puede iniciarse en borrador, pero cuyo cierre
    depende de otras Issues.
  - `blocked`: Issue abierta que no debe cerrarse hasta resolver dependencias
    faltantes.
- Cuando Kiko pide `siguiente paso`, Codex identifica el paso prioritario y lo
  ejecuta en la misma sesión/pasada por defecto.
- En trabajo no trivial con rama, el objetivo por defecto es completar el
  **cierre end-to-end** de la unidad, hasta donde sea posible en la misma
  pasada:
  1. implementar/cerrar cambios pendientes de la unidad;
  1. commit;
  1. `push` de rama;
  1. abrir PR;
  1. llevar PR a cierre (merge o cierre explícito si se descarta);
  1. cerrar la Issue asociada tras integración en `main`;
  1. limpiar rama local/remota (si aplica).
- Regla específica para `type:decision`:
  - Codex llega hasta el máximo cerrable.
  - Si falta aprobación explícita de Kiko, deja la unidad bloqueada por
    aprobación y no salta a otra unidad por defecto.
  - Si Kiko aprueba explícitamente en el mismo turno, Codex completa
    merge/cierre/limpieza en esa misma pasada.
- Regla en `Plan Mode`:
  - `siguiente paso` identifica la unidad pendiente de cierre (si existe) y
    planifica su cierre end-to-end, sin ejecutar mutaciones.
  - Si `siguiente paso` identifica una issue/unidad prioritaria (sin mutaciones
    pendientes previas), Codex debe entrar en las decisiones de esa unidad en
    ese mismo turno antes de emitir el `<proposed_plan>`.
  - No se admite cerrar con un meta-plan cuyo siguiente paso sea iniciar el
    plan de la misma unidad ya priorizada.
  - Debe dejar explícito cuál sería el siguiente acto mutante al salir de
    `Plan Mode`.
- Reporte obligatorio tras `siguiente paso`:
  - unidad priorizada;
  - estado de cierre alcanzado (`local`, `push`, `PR`, `merge`, `issue`,
    `cleanup`);
  - bloqueo (si existe) y su motivo;
  - confirmación explícita de si puede o no pasar a la siguiente unidad.
- Excepciones explícitas:
  - `Plan Mode` (se planifica y no se ejecuta).
  - Bloqueo real que impida continuar.
  - Petición explícita de solo plan o solo análisis.

##### Nota de aplicación (caso #13)

- El caso de la Issue `#13` (especificación temporal) dejó documentado el hueco
  de comportamiento: había commit local en rama sin `push`/sin PR y, aun así,
  se llegó a evaluar trabajo nuevo.
- Con esta regla, ese estado se clasifica como `unidad pendiente de cierre` y el
  siguiente `siguiente paso` correcto es publicar/cerrar esa unidad primero.

## Reglas de commits

- Formato: `type(scope): resumen en español`.
- Tipos válidos:
  - `feat`
  - `fix`
  - `docs`
  - `chore`
  - `refactor`
  - `test`
  - `hotfix`

## Redacción y codificación de texto

- En textos en castellano (issues, PR, documentación y futuros textos de UI)
  usar ortografía completa: tildes, `ñ` y signos correctos.
- Mantener identificadores técnicos en inglés cuando aplique.
- Archivos de texto del repo en `UTF-8`.
- Si aparece mojibake en la terminal, verificar primero la codificación real
  del archivo antes de editar contenido ya correcto.

## Reglas de PR

- PR obligatoria cuando el cambio sea relevante.
- Si el trabajo se hace en rama, la Issue asociada se cierra tras merge o
  integración en `main`, salvo instrucción explícita de Kiko.
- Debe incluir:
  - referencia al Issue
  - resumen de alcance
  - checklist de calidad completada

## Patrón operativo de validación UI Flet (web) con Playwright/DevTools

### Objetivo

Definir un patrón simple y repetible para validar UI/flujo visual durante la
implementación en Flet, evitando bloquear la CLI de Codex con procesos largos.

### Convención por defecto

- Kiko lanza y mantiene el servidor web de Flet cuando haga falta validar UI.
- Codex usa Playwright/DevTools para inspección visual y técnica.
- La evidencia se adapta al tipo de tarea (no se fuerza un paquete completo en
  cada validación).

### Comando estándar de arranque (Kiko)

```powershell
pipenv run flet run src/main.py --web -d -r --port 8550 --host 127.0.0.1
```

- `--web`: ejecuta la app como sitio web local.
- `-d -r`: autoreload recursivo para iteración de UI.
- `--port 8550`: URL estable para validación repetible.
- `--host 127.0.0.1`: escucha local explícita.

### Roles y flujo

#### Fase A — Preparación (Kiko)

1. Cambiar a la rama de trabajo de la issue en curso (si aplica).
1. Lanzar el servidor con el comando estándar.
1. Confirmar a Codex:
   - URL activa (por defecto `http://127.0.0.1:8550`);
   - warnings relevantes al arranque (si existen).

#### Fase B — Validación (Codex)

1. Abrir la URL activa con Playwright.
1. Verificar el estado esperado según la tarea (layout, navegación,
   placeholders, etc.).
1. Inspeccionar según necesidad:
   - snapshot/captura;
   - consola del navegador;
   - requests/red;
   - observación visual y estados.
1. Reportar resultado:
   - qué se comprobó;
   - evidencia usada;
   - resultado (`ok`, `problema`, `bloqueado`);
   - siguiente acción (seguir, ajustar, refresh, relanzar).

#### Fase C — Iteración (Kiko + Codex)

1. Codex implementa cambios de la issue.
1. Kiko mantiene el servidor en marcha.
1. Codex revalida en la misma URL.
1. Repetir hasta aceptación del alcance.

#### Fase D — Cierre de validación de tarea

En el cierre de la unidad (issue/PR), Codex deja una nota breve de validación:

- tipo de evidencia usada;
- estados/pantallas comprobados;
- limitaciones o partes no validadas (si las hay).

### Evidencia adaptativa (regla)

- Ligera: observación + snapshot/captura puntual (cambios pequeños).
- Media: capturas + observaciones + consola si hay warning/error (layout/flujo).
- Alta: captura + consola + red + pasos de reproducción (fallos raros o bloqueos).

Codex escala el nivel cuando:

- hay errores de consola;
- el layout no coincide con Figma/contrato;
- hay comportamiento intermitente;
- la validación bloquea el cierre de la issue.

### Fallbacks operativos

- Puerto `8550` ocupado:
  - Kiko relanza en otro puerto (por ejemplo `8551`) y comunica la URL exacta.
- Autoreload no refleja cambios:
  - Codex pide refresh manual;
  - si persiste, Kiko relanza servidor;
  - registrar incidencia solo si es repetitiva o bloqueante.

## Limpieza de ramas

- Tras cada merge/cierre, limpiar ramas locales y remotas mergeadas que no se
  vayan a reutilizar.
- Exclusiones por defecto:
  - `main`
  - rama actual
  - ramas con PR abierta
  - ramas no mergeadas (salvo descarte explícito)
- Si una rama fue integrada por `rebase` y `git branch -d` avisa que no está
  mergeada en `HEAD`, se permite borrarla tras verificar que la PR fue mergeada.

## Regla especial para diseño y arquitectura

- Si la tarea es de dominio, arquitectura o proceso crítico:
  - se discute primero en conversación interactiva;
  - se documenta después de aprobación explícita de Kiko;
  - no se cierra la Issue sin esa aprobación.
  - si hace falta interfaz de respuestas clicables, Codex avisa para activar
    `Plan Mode`.

## Definición de cambio trivial

- typo o formato local
- ajuste menor en una zona
- sin impacto en flujo ni estructura

## Definición de cambio relevante

- cambia convenciones
- cambia estructura de documentación
- afecta más de un archivo crítico
- introduce decisiones de proceso

## Versionado y releases

- Convención SemVer temprana: `v0.x.y`.
- En cada hito cerrado:
  - actualizar `CHANGELOG.md`
  - crear tag
  - publicar release notes

## Estrategia de APK en releases

Estado actual:

- No hay pipeline de build Android en GitHub Actions.
- No hay adjunto automático de `.apk` en releases.

Opciones para Fase 1:

1. Manual:
   - compilar localmente y adjuntar `.apk` en la release.
1. Automática:
   - workflow de GitHub Actions al crear tag;
   - generar `.apk` y adjuntarlo a la release.

Requisitos de automatización:

- toolchain Android en CI;
- secretos de firma (`keystore`, passwords y alias);
- definición de variante (`debug` o `release`).

## Cadencia recomendada

### Flujo en rama (trabajo no trivial o relevante)

1. Abrir Issue.
1. Ejecutar trabajo en rama.
1. Hacer N commits pequeños.
1. Abrir PR.
1. Mergear en `main`.
1. Cerrar Issue.
1. Limpiar rama local/remota si ya no se reutiliza.
1. Actualizar changelog.

### Flujo directo a `main` (trabajo trivial y aislado)

1. Ejecutar ajuste trivial en `main`.
1. Hacer commit y push.
1. Cerrar Issue (si aplica).
1. Actualizar changelog si corresponde.
