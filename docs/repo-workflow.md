# Flujo de Repositorio

## Metadatos

- `doc_id`: DOC-REPO-WORKFLOW
- `purpose`: Definir el flujo Git y GitHub adoptado.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-03-05
- `next_review`: 2026-03-19

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
1. Si una unidad es no trivial, va en rama con patrÃ³n
   `tipo/<issue-id>-slug`.
1. Si una unidad es trivial y aislada, puede ir a `main`.
1. Si una unidad se ejecuta en rama, la Issue asociada se cierra tras integrar
   el trabajo en `main` (merge/PR), salvo instrucciÃ³n explÃ­cita de Kiko.
1. Codex reporta siempre:
   - quÃ© unidad ejecutÃ³,
   - quÃ© commit generÃ³,
   - quÃ© Issue cerrÃ³ o dejÃ³ abierta.

### Reglas de priorizaciÃ³n conversacional (`siguiente paso`, `siguiente pendiente`)

- `siguiente pendiente` y `siguiente issue pendiente` son equivalentes.

- Si Kiko pide `siguiente pendiente`, Codex selecciona por defecto la Issue
  abierta (`state=open`) con nÃºmero mÃ¡s bajo.
- Si Kiko indica filtros (por ejemplo `type`, `label` o `phase`), Codex aplica
  esos filtros antes de ordenar por nÃºmero.
- Si no hay Issues abiertas que cumplan el criterio, Codex lo reporta de forma
  explÃ­cita.

#### Regla de `siguiente paso`

- Codex revisa primero si existe una **unidad pendiente de cierre**.
- Si existe una unidad pendiente de cierre, el siguiente paso es resolver esa
  unidad antes de iniciar trabajo nuevo.
- Solo si no existe una unidad pendiente de cierre, Codex revisa las PRs
  abiertas del repo (incluyendo `draft`).
- Si hay varias PRs abiertas, prioriza la PR con nÃºmero mÃ¡s bajo.
- Si existe al menos una PR abierta, el siguiente paso es llevar esa PR a
  cierre (merge o cierre explÃ­cito si se descarta).
- Si no hay PRs abiertas, Codex busca un **orden tÃ©cnico recomendado** en la
  documentaciÃ³n oficial aplicable.
- Si existe orden tÃ©cnico recomendado:
  - usa la fuente oficial mÃ¡s especÃ­fica disponible (detalle > macro);
  - recorre el orden y elige la primera Issue abierta **cerrable**;
  - si una Issue abierta no es cerrable, la salta y evalÃºa la siguiente;
  - si no hay Issues cerrables en ese orden, elige la primera Issue
    `draftable`.
- Si no existe orden tÃ©cnico aplicable, el siguiente paso es resolver la
  `siguiente pendiente` (`siguiente issue pendiente`).
- DefiniciÃ³n operativa para esta regla:
  - `unidad pendiente de cierre`: unidad ya iniciada (issue/rama/PR asociada)
    que todavÃ­a no completÃ³ su pipeline de cierre. Se detecta en este orden de
    prioridad:
    1. trabajo local sin commit relacionado con la unidad activa;
    1. commit(s) locales en rama sin `push`;
    1. rama publicada con trabajo de la unidad pero sin PR (cuando corresponde
       PR por reglas del repo);
    1. PR abierta (incluyendo `draft`);
    1. PR mergeada pero Issue asociada aÃºn abierta;
    1. rama local/remota mergeada pendiente de limpieza.
  - `cerrable`: Issue abierta con dependencias de cierre satisfechas segÃºn la
    documentaciÃ³n oficial vigente.
  - `draftable`: Issue abierta que puede iniciarse en borrador, pero cuyo cierre
    depende de otras Issues.
  - `blocked`: Issue abierta que no debe cerrarse hasta resolver dependencias
    faltantes.
- Cuando Kiko pide `siguiente paso`, Codex identifica el paso prioritario y lo
  ejecuta en la misma sesiÃ³n/pasada por defecto.
- En trabajo no trivial con rama, el objetivo por defecto es completar el
  **cierre end-to-end** de la unidad, hasta donde sea posible en la misma
  pasada:
  1. implementar/cerrar cambios pendientes de la unidad;
  1. commit;
  1. `push` de rama;
  1. abrir PR;
  1. llevar PR a cierre (merge o cierre explÃ­cito si se descarta);
  1. cerrar la Issue asociada tras integraciÃ³n en `main`;
  1. limpiar rama local/remota (si aplica).
- Regla especÃ­fica para `type:decision`:
  - Codex llega hasta el mÃ¡ximo cerrable.
  - Si falta aprobaciÃ³n explÃ­cita de Kiko, deja la unidad bloqueada por
    aprobaciÃ³n y no salta a otra unidad por defecto.
  - Si Kiko aprueba explÃ­citamente en el mismo turno, Codex completa
    merge/cierre/limpieza en esa misma pasada.
- Regla en `Plan Mode`:
  - `siguiente paso` identifica la unidad pendiente de cierre (si existe) y
    planifica su cierre end-to-end, sin ejecutar mutaciones.
  - Si `siguiente paso` identifica una issue/unidad prioritaria (sin mutaciones
    pendientes previas), Codex debe entrar en las decisiones de esa unidad en
    ese mismo turno antes de emitir el `<proposed_plan>`.
  - No se admite cerrar con un meta-plan cuyo siguiente paso sea iniciar el
    plan de la misma unidad ya priorizada.
  - Debe dejar explÃ­cito cuÃ¡l serÃ­a el siguiente acto mutante al salir de
    `Plan Mode`.
- Reporte obligatorio tras `siguiente paso`:
  - unidad priorizada;
  - estado de cierre alcanzado (`local`, `push`, `PR`, `merge`, `issue`,
    `cleanup`);
  - bloqueo (si existe) y su motivo;
  - confirmaciÃ³n explÃ­cita de si puede o no pasar a la siguiente unidad.
- Excepciones explÃ­citas:
  - `Plan Mode` (se planifica y no se ejecuta).
  - Bloqueo real que impida continuar.
  - PeticiÃ³n explÃ­cita de solo plan o solo anÃ¡lisis.

##### Nota de aplicaciÃ³n (caso #13)

- El caso de la Issue `#13` (especificaciÃ³n temporal) dejÃ³ documentado el hueco
  de comportamiento: habÃ­a commit local en rama sin `push`/sin PR y, aun asÃ­,
  se llegÃ³ a evaluar trabajo nuevo.
- Con esta regla, ese estado se clasifica como `unidad pendiente de cierre` y el
  siguiente `siguiente paso` correcto es publicar/cerrar esa unidad primero.

## Reglas de commits

- Formato: `type(scope): resumen en espaÃ±ol`.
- Tipos vÃ¡lidos:
  - `feat`
  - `fix`
  - `docs`
  - `chore`
  - `refactor`
  - `test`
  - `hotfix`

## RedacciÃ³n y codificaciÃ³n de texto

- En textos en castellano (issues, PR, documentaciÃ³n y futuros textos de UI)
  usar ortografÃ­a completa: tildes, `Ã±` y signos correctos.
- Mantener identificadores tÃ©cnicos en inglÃ©s cuando aplique.
- Archivos de texto del repo en `UTF-8`.
- Si aparece mojibake en la terminal, verificar primero la codificaciÃ³n real
  del archivo antes de editar contenido ya correcto.

## Reglas de PR

- PR obligatoria cuando el cambio sea relevante.
- Si el trabajo se hace en rama, la Issue asociada se cierra tras merge o
  integraciÃ³n en `main`, salvo instrucciÃ³n explÃ­cita de Kiko.
- Debe incluir:
  - referencia al Issue
  - resumen de alcance
  - checklist de calidad completada

## PatrÃ³n operativo de validaciÃ³n UI Flet (web) con Playwright/DevTools

### Objetivo

Definir un patrÃ³n simple y repetible para validar UI/flujo visual durante la
implementaciÃ³n en Flet, evitando bloquear la CLI de Codex con procesos largos.

### ConvenciÃ³n por defecto

- Kiko lanza y mantiene el servidor web de Flet cuando haga falta validar UI.
- Codex usa Playwright/DevTools para inspecciÃ³n visual y tÃ©cnica.
- La evidencia se adapta al tipo de tarea (no se fuerza un paquete completo en
  cada validaciÃ³n).

### Comando estÃ¡ndar de arranque (Kiko)

```powershell
pipenv run flet run src/main.py --web -d -r --port 8550 --host 127.0.0.1
```

- `--web`: ejecuta la app como sitio web local.
- `-d -r`: autoreload recursivo para iteraciÃ³n de UI.
- `--port 8550`: URL estable para validaciÃ³n repetible.
- `--host 127.0.0.1`: escucha local explÃ­cita.

### Roles y flujo

#### Fase A â€” PreparaciÃ³n (Kiko)

1. Cambiar a la rama de trabajo de la issue en curso (si aplica).
1. Lanzar el servidor con el comando estÃ¡ndar.
1. Confirmar a Codex:
   - URL activa (por defecto `http://127.0.0.1:8550`);
   - warnings relevantes al arranque (si existen).

#### Fase B â€” ValidaciÃ³n (Codex)

1. Abrir la URL activa con Playwright.
1. Verificar el estado esperado segÃºn la tarea (layout, navegaciÃ³n,
   placeholders, etc.).
1. Inspeccionar segÃºn necesidad:
   - snapshot/captura;
   - consola del navegador;
   - requests/red;
   - observaciÃ³n visual y estados.
1. Reportar resultado:
   - quÃ© se comprobÃ³;
   - evidencia usada;
   - resultado (`ok`, `problema`, `bloqueado`);
   - siguiente acciÃ³n (seguir, ajustar, refresh, relanzar).

#### Fase C â€” IteraciÃ³n (Kiko + Codex)

1. Codex implementa cambios de la issue.
1. Kiko mantiene el servidor en marcha.
1. Codex revalida en la misma URL.
1. Repetir hasta aceptaciÃ³n del alcance.

#### Fase D â€” Cierre de validaciÃ³n de tarea

En el cierre de la unidad (issue/PR), Codex deja una nota breve de validaciÃ³n:

- tipo de evidencia usada;
- estados/pantallas comprobados;
- limitaciones o partes no validadas (si las hay).

### Evidencia adaptativa (regla)

- Ligera: observaciÃ³n + snapshot/captura puntual (cambios pequeÃ±os).
- Media: capturas + observaciones + consola si hay warning/error (layout/flujo).
- Alta: captura + consola + red + pasos de reproducciÃ³n (fallos raros o bloqueos).

Codex escala el nivel cuando:

- hay errores de consola;
- el layout no coincide con Figma/contrato;
- hay comportamiento intermitente;
- la validaciÃ³n bloquea el cierre de la issue.

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
  - ramas no mergeadas (salvo descarte explÃ­cito)
- Si una rama fue integrada por `rebase` y `git branch -d` avisa que no estÃ¡
  mergeada en `HEAD`, se permite borrarla tras verificar que la PR fue mergeada.

## Regla especial para diseÃ±o y arquitectura

- Si la tarea es de dominio, arquitectura o proceso crÃ­tico:
  - se discute primero en conversaciÃ³n interactiva;
  - se documenta despuÃ©s de aprobaciÃ³n explÃ­cita de Kiko;
  - no se cierra la Issue sin esa aprobaciÃ³n.
  - si hace falta interfaz de respuestas clicables, Codex avisa para activar
    `Plan Mode`.

## DefiniciÃ³n de cambio trivial

- typo o formato local
- ajuste menor en una zona
- sin impacto en flujo ni estructura

## DefiniciÃ³n de cambio relevante

- cambia convenciones
- cambia estructura de documentaciÃ³n
- afecta mÃ¡s de un archivo crÃ­tico
- introduce decisiones de proceso

## Versionado y releases

- ConvenciÃ³n SemVer temprana: `v0.x.y`.
- En cada hito cerrado:
  - actualizar `CHANGELOG.md`
  - crear tag
  - publicar release notes

## Estrategia de APK en releases

Estado actual:

- No hay pipeline de build Android en GitHub Actions.
- No hay adjunto automático de `.apk` en releases.
- El flujo manual de build y adjunto de `.apk` está operativo y documentado en
  `docs/android-release-flow.md`.

Opciones para Fase 1:

1. Manual:
   - compilar localmente y adjuntar `.apk` en la release.
   - usar como referencia operativa `docs/android-release-flow.md`.
1. Automática:
   - workflow de GitHub Actions al crear tag;
   - generar `.apk` y adjuntarlo a la release.
Requisitos de automatización:

- toolchain Android en CI;
- secretos de firma (`keystore`, passwords y alias);
- definiciÃ³n de variante (`debug` o `release`).

## Cadencia recomendada

### Flujo en rama (trabajo no trivial o relevante)

1. Abrir Issue.
1. Ejecutar trabajo en rama.
1. Hacer N commits pequeÃ±os.
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

