# Checklist Técnico de Implementación MVP

## Metadatos

- `doc_id`: DOC-MVP-IMPLEMENTATION-CHECKLIST
- `purpose`: Checklist técnico base para preparar la implementación del MVP con orden, dependencias y verificación mínima.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-24
- `next_review`: 2026-03-10

## Objetivo

Definir un checklist técnico base, accionable y ordenado para preparar la
implementación del MVP sin codificar todavía, con trazabilidad entre issues,
dependencias explícitas y criterios mínimos de verificación por bloque.

## Alcance y no alcance

Incluye:

- macro-bloques de trabajo para preparación técnica de Fase 1;
- orden recomendado de ejecución;
- matriz de dependencias entre issues abiertas y decisiones ya resueltas;
- criterios mínimos de verificación por bloque;
- reglas de paralelización y riesgos de secuencia;
- corte explícito con las Issues #11 y #20.

No incluye:

- codificación de la app;
- desglose fino en bloques ejecutables con responsables y entregables (Issue #11);
- gate final de "listo para codificar" (Issue #20);
- cierre de decisiones de dominio pendientes (si las hay).

## Entradas ya cerradas (prerrequisitos disponibles)

Las siguientes decisiones base ya están resueltas y se toman como insumo para
este checklist:

- **Sincronización MVP** (Issue #7): `docs/sync-strategy.md`
  - `single writer` recomendado, `online-only writes`, `on-demand refresh`.
- **Política de conflictos concurrentes** (Issue #8): `docs/conflict-policy.md`
  - estrategia estricta de rechazo + refresco/reintento.
- **Controles temporales de campaña** (Issue #9):
  `docs/campaign-temporal-controls.md`
  - selector temporal superior, provisión inicial de 4 años, extensión manual
    `+1`, separación entre navegación de semana y `week_cursor`.
- **Inicialización temporal de campaña (técnica)** (Issue #13):
  `docs/campaign-temporal-initialization.md`
  - estructura temporal fija del MVP (`summer -> winter`, 10 semanas por
    estación), provisión inicial y extensión `+1`.
- **Política de editabilidad manual MVP** (Issue #37):
  `docs/editability-policy.md`
  - editabilidad amplia ("como papel"), reordenación manual de `Entry`,
    `Week.reopen/reclose`, correcciones manuales de `Session` y semántica
    derivada de `week_cursor`.
- **Modelo de recursos por `Entry` (delta neto)** (Issue #40):
  `docs/resource-delta-model.md`
  - `ResourceChange` se sustituye por `Entry.resource_deltas` (delta neto por
    recurso), con supersesión parcial de la parte de recursos en `#12`.
- **Política de timestamps y orden estable** (Issue #18):
  `docs/timestamp-order-policy.md`
  - auditoría temporal server-only, sin `deleted_at_utc` en MVP, y matriz de
    orden canónico por lista para UI + `#16`.
- **Flujo de sesión activa y `auto-stop`** (Issue #14):
  `docs/active-session-flow.md`
  - separación entre `current week`, selección y `Entry` activa; reglas de
    `start/stop/auto-stop` y recuperación por `conflicto`/`transicion_invalida`.
- **Validación y recálculo de recursos** (Issue #15):
  `docs/resource-validation-recalculation.md`
  - reglas por operación (`adjust/set/clear`), recálculo de `campaign.resource_totals`
    y clasificación de rechazos de recursos.
- **Consultas mínimas para pantalla principal** (Issue #16):
  `docs/minimal-read-queries.md`
  - inventario mínimo de lecturas por superficie/estado, triggers de carga y
    refresh, orden compatible con `#18` y sin paginación en MVP.

## Corte de responsabilidades entre `#10`, `#11` y `#20`

### Issue `#10` (esta tarea) sí cierra

- checklist técnico base de preparación MVP;
- macro-bloques y secuencia recomendada;
- dependencias y paralelización a alto nivel;
- criterios mínimos de verificación por bloque.

### Issue `#11` (no se adelanta aquí)

- desglose en bloques ejecutables finos;
- responsables por bloque;
- entregables detallados por sub-bloque;
- riesgos operativos por subpaso.

### Issue `#20` (no se adelanta aquí)

- gate final de entrada a codificación;
- criterio definitivo de "listo para codificar";
- evidencia mínima de readiness para comenzar código.

## Orden recomendado de ejecución (macro-bloques)

### Bloque A — Base del plan técnico de ejecución

- **Issue**: #11
- **Objetivo**: convertir este checklist base en bloques ejecutables con
  entregables verificables.
- **Rol respecto a #10**: downstream inmediato.
- **Criterio mínimo**: desglose completo con dependencias y riesgos
  identificados.
- **Detalle operativo**: ver `docs/mvp-implementation-blocks.md` (desglose por
  issue y subbloques ejecutables).

### Bloque B — Contratos de dominio para implementación (núcleo)

- **Issues**: #13, #37, #12, #40, #18
- **Orden recomendado**:
  1. #13 — inicialización temporal detallada.
  1. #37 — política de editabilidad manual y correcciones de dominio (marco).
  1. #12 — contrato de operaciones Firestore por agregado, alineado con #13 y #37.
  1. #40 — modelo de recursos por `Entry` (delta neto; supersesión parcial de recursos).
  1. #18 — timestamps y orden estable entre dispositivos.
- **Justificación**:
  - #13 concreta la provisión/extensión temporal decidida en #9.
  - #37 actualiza invariantes/mutabilidad del dominio antes de cerrar contratos
    por agregado.
  - #12 necesita alineación con provisión temporal (#9), detalle técnico (#13)
    y política de editabilidad (#37).
  - #40 corrige el modelo de recursos del MVP y reduce ambigüedad antes de #15
    y del inventario ordenable de #18.
  - #18 cierra orden estable para lecturas y logs entre dispositivos.

### Bloque C — Flujos funcionales e invariantes de operación

- **Issues**: #14, #15
- **Orden recomendado**:
  1. #14 — flujo de sesión activa y reglas de `auto-stop`.
  1. #15 — validación y recálculo de recursos.
- **Dependencias mínimas**:
  - #14 requiere #8 (resuelta) y se beneficia del contrato #12.
  - #15 requiere #8 (resuelta) y debe alinearse con #12 y #40.

### Bloque D — Lecturas, edge cases y verificación

- **Issues**: #16, #17, #19
- **Orden recomendado**:
  1. #16 — consultas mínimas para timeline/foco.
  1. #17 — matriz de edge cases de concurrencia y sincronización.
  1. #19 — plan de pruebas de invariantes.
- **Notas**:
  - #16 debe alinearse con #9 y conviene cerrarla con #18 definido.
  - #17 se enriquece con contratos/flows definidos en #12, #14, #15 y #18.
  - #19 consolida evidencia de validación para el gate posterior (#20).

### Bloque E — Gate final de entrada a codificación

- **Issue**: #20
- **Objetivo**: definir "listo para codificar" usando #10 y sus derivadas.
- **Regla de secuencia**: debe ir al final del checklist de preparación.

## Matriz de dependencias (issues / bloques)

| Bloque / Issue | Tipo | Depende de | ¿Puede empezar en paralelo? | Condición de cierre | Impacta a |
| --- | --- | --- | --- | --- | --- |
| Bloque A / #11 | `task` | #10 | Sí, como borrador parcial; no cerrar antes de #10 | Desglose completo y trazable | #12, #13, #14, #15, #16, #17, #19, #20 |
| Bloque B / #13 | `task` | #9 (resuelta) | Sí | Flujo temporal detallado sin contradicciones | #37, #12, #16, #20 |
| Bloque B / #37 | `decision` | #8, #9 (resueltas) + coherencia con #13 | Borrador sí; cierre recomendado tras #13 | Política de editabilidad manual e invariantes actualizadas | #12, #14, #15, #17, #19, #20 |
| Bloque B / #12 | `decision` | #7, #8, #9 (resueltas) + alineación con #13 y #37 | Borrador sí; cierre recomendado tras #13 y #37 | Contrato por agregado con pre/postcondiciones | #14, #15, #16, #17, #18, #19, #20 |
| Bloque B / #40 | `decision` | #8, #12, #37 (resueltas) + coherencia con glosario | Sí, pero cierre recomendado antes de #18 y #15 | Modelo de recursos por `Entry` (`resource_deltas`) y parche de consistencia | #15, #17, #18, #19, #20 |
| Bloque B / #18 | `decision` | #7, #8 (resueltas) + coherencia con #12 y #40 | Sí, pero cierre recomendado tras #12 y #40 | Política de timestamps y desempate estable | #16, #17, #19, #20 |
| Bloque C / #14 | `task` | #8 (resuelta) + alineación con #37 | Sí, parcial | Flujo de sesión + `auto-stop` sin romper invariantes | #17, #19, #20 |
| Bloque C / #15 | `task` | #8 (resuelta) + alineación con #37 y #40 | Sí, parcial | Reglas de validación y recálculo trazables | #17, #19, #20 |
| Bloque D / #16 | `task` | #7, #9 (resueltas) | Sí | Inventario mínimo de consultas y orden estable | #19, #20 |
| Bloque D / #17 | `task` | #7, #8 (resueltas) | Sí, pero gana valor tras #12/#14/#15/#18 | Matriz de edge cases con expectativa verificable | #19, #20 |
| Bloque D / #19 | `task` | #7, #8, #9 (resueltas) | Sí, parcial | Plan de pruebas de invariantes con evidencia repetible | #20 |
| Bloque E / #20 | `task` | Base de #10 + derivadas relevantes | No, cierre al final | Gate de readiness explícito y verificable | Paso a implementación |

## Criterios mínimos de verificación por bloque

Usar esta plantilla mínima en cada issue/bloque del checklist:

1. **Artefacto principal existe**
   - Documento, diagrama, matriz o checklist creado y enlazado.
1. **Aceptación de la issue cubierta**
   - Los criterios de aceptación de la issue se traducen a evidencia verificable.
1. **Referencias cruzadas actualizadas**
   - Documentación oficial afectada actualizada (`docs/`, `AGENTS.md`, etc.).
1. **Consistencia con decisiones cerradas**
   - No contradice #7, #8, #9 ni decisiones posteriores aplicables.
1. **Dependencias downstream identificadas**
   - Queda claro qué issues se desbloquean o se condicionan.
1. **Estado trazable**
   - PR/issue/commit y cierre correcto tras merge.

## Riesgos de secuencia y reglas de paralelización

### Riesgos de secuencia

- **Solape #10 / #11 / #20**: evitar que #10 se convierta en desglose fino (#11)
  o en gate definitivo (#20).
- **Cerrar #12 antes de #13/#37**: puede introducir contrato Firestore
  desalineado con provisión temporal y/o mutabilidad real del dominio.
- **Cerrar #16 sin #18**: riesgo de definir orden de lectura sin desempate
  estable documentado.
- **Matriz #17 demasiado temprana**: puede quedar incompleta si faltan
  contratos, flujos y mutabilidad clave (#37, #12, #14, #15, #18).

### Reglas de paralelización (recomendadas)

- Se permiten **borradores** en paralelo cuando la issue lo indique, pero el
  cierre debe respetar dependencias explícitas.
- La paralelización se usa para reducir tiempo de análisis, no para forzar
  cierres prematuros.
- Las issues `type:decision` (#12, #18) requieren revisión interactiva con Kiko
  antes de cerrar.

## Checklist de seguimiento (estado actual)

- [x] Prerrequisitos base resueltos: #7, #8, #9
- [x] Checklist técnico base definido (Issue #10)
- [x] Desglose en bloques ejecutables (Issue #11)
- [x] Inicialización temporal detallada (Issue #13)
- [x] Política de editabilidad manual y correcciones de dominio (Issue #37)
- [x] Contrato de operaciones Firestore por agregado (Issue #12)
- [x] Modelo de recursos por `Entry` (delta neto; Issue #40)
- [x] Política de timestamps y orden estable (Issue #18)
- [x] Flujo de sesión activa y `auto-stop` (Issue #14)
- [x] Reglas de validación y recálculo de recursos (Issue #15)
- [x] Consultas mínimas para timeline/foco (Issue #16)
- [x] Matriz de edge cases de concurrencia y sincronización (Issue #17)
- [x] Plan de pruebas para invariantes (Issue #19)
- [x] Gate de listo para codificar (Issue #20)

## Seguimiento de implementación (post-#20)

- [x] Bootstrap de app Flet y estructura base del proyecto (Issue #51)
- [x] Shell de pantalla principal con layout base según Figma (Issue #52)
- [x] Estado local de selección/navegación + visor sticky + activo mock (Issue #53)
- [ ] Integrar lecturas mínimas read-only para arranque y navegación base (Issue #54)

## Referencias

- `AGENTS.md`
- `docs/system-map.md`
- `docs/repo-workflow.md`
- `docs/mvp-implementation-blocks.md`
- `docs/sync-strategy.md`
- `docs/conflict-policy.md`
- `docs/firestore-operation-contract.md`
- `docs/resource-delta-model.md`
- `docs/resource-validation-recalculation.md`
- `docs/timestamp-order-policy.md`
- `docs/active-session-flow.md`
- `docs/campaign-temporal-controls.md`
- `docs/campaign-temporal-initialization.md`
- `docs/editability-policy.md`
- `docs/domain-glossary.md`
- `docs/context-checklists.md`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/10`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/11`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/13`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/37`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/40`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/14`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/15`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/16`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/17`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/19`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/20`
