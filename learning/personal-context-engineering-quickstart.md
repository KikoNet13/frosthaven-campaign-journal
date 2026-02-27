# Guía rápida: iniciar proyectos personales con ingeniería de contexto

## Metadatos

- `doc_id`: LEARNING-PERSONAL-CONTEXT-QUICKSTART
- `purpose`: Tutorial práctico para arrancar proyectos personales con buena ingeniería de contexto sin frenar la ejecución del producto.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-26
- `next_review`: 2026-03-12

## Objetivo

Tener un sistema ligero, reutilizable y accionable para iniciar un proyecto
personal con ayuda de IA, evitando dos extremos:

- caos sin trazabilidad;
- burocracia que bloquea el desarrollo.

Esta guía resume aciertos y errores observados en este repositorio y los
convierte en un patrón reusable.

## Principios mínimos (80/20)

1. **Producto primero, contexto suficiente**
   - El contexto debe acelerar decisiones de implementación.
   - Si un documento no ayuda a decidir o ejecutar, no se crea todavía.

1. **Fuente oficial corta y clara**
   - Define 1 archivo de reglas operativas (`AGENTS.md`) y 3–5 documentos vivos
     en `docs/`.

1. **Trazabilidad solo donde aporta**
   - Decision log breve para decisiones transversales.
   - Issues/PR para unidades no triviales.

1. **Iteración real de UI/funcionalidad**
   - Cada ciclo debe mover algo visible o verificable en la app.

1. **Rigor proporcional**
   - Proyecto personal: aceptar diferidos y deuda controlada si no rompe uso
     real.

## Errores frecuentes y cómo evitarlos

### Error 1: sobre-documentar antes de construir

- Síntoma: muchas decisiones abstractas y poca UI funcional.
- Corrección: imponer una regla de avance: por cada unidad documental, al menos
  una unidad de implementación o validación visual.

### Error 2: no separar decisiones de detalle vs. decisiones transversales

- Síntoma: discusiones largas sobre microdetalles.
- Corrección: solo elevar a decision log lo que impacta varias áreas.

### Error 3: backlog sin orden de cierre

- Síntoma: muchas tareas abiertas sin secuencia clara.
- Corrección: mantener un backlog corto (3–7 issues activas) con prioridad
  explícita y criterio de cierre por issue.

### Error 4: falta de contrato con el agente

- Síntoma: respuestas inconsistentes entre sesiones.
- Corrección: definir en `AGENTS.md` el flujo base, formato de reportes y
  criterio de priorización.

## Kit mínimo para arrancar (plantilla)

Crea esta estructura inicial:

- `AGENTS.md`
- `docs/system-map.md`
- `docs/decision-log.md`
- `docs/repo-workflow.md`
- `docs/product-scope.md` (alcance MVP y no-alcance)
- `docs/implementation-backlog.md` (issues propuestas + estado)
- `learning/` (opcional, para lecciones transferibles)

## Contenido mínimo recomendado por archivo

### `AGENTS.md`

Incluye solo:

- objetivo del proyecto;
- reglas operativas no negociables (máx. 10);
- flujo de sesión (inicio, ejecución, cierre);
- regla de priorización (`siguiente paso`);
- política de idioma y formato;
- regla de cierre con 3–5 próximos pasos.

### `docs/product-scope.md`

- problema que resuelve la app;
- usuario objetivo;
- alcance MVP (lista cerrada);
- no-alcance explícito;
- criterio de “MVP usable”.

### `docs/decision-log.md`

Formato corto por entrada:

- `decision_id`
- `date`
- `problem`
- `decision`
- `impact`
- `references`

### `docs/implementation-backlog.md`

Por cada issue propuesta:

- `issue_id` (temporal si aún no existe en GitHub);
- objetivo funcional;
- tipo (`feat`, `refactor`, `bug`, `chore`);
- criterio de cierre (2–4 checks);
- prioridad (`P0/P1/P2`);
- dependencias.

## Prompt base reutilizable para arrancar con IA

```text
Quiero construir una app personal priorizando entrega funcional.

Contexto operativo:
- Usa AGENTS.md como contrato principal.
- Mantén documentación ligera y útil para implementar.
- Si propones documentación, debe desbloquear código o validación.
- Para trabajo no trivial, crea issue -> rama -> PR.

Objetivo actual:
- [describe aquí 1 objetivo concreto de producto]

Definición de terminado:
- [lista breve de checks funcionales o de UI]

Restricciones:
- [stack, límites de tiempo, alcance]
```

## Flujo recomendado de una sesión (rápido)

1. Leer `AGENTS.md` + backlog activo.
1. Confirmar una sola unidad prioritaria.
1. Ejecutar cambios.
1. Validar (test/captura/revisión manual).
1. Registrar solo lo necesario (decision log si aplica, update backlog).
1. Cerrar con commit + PR + siguiente menú (3–5 pasos).

## Regla práctica para no volver a la sobrecarga

Antes de crear una tarea documental, responder:

- ¿Desbloquea una decisión transversal real?
- ¿Reduce retrabajo inmediato de implementación?
- ¿Se puede cerrar en < 30 min?

Si la respuesta es “no” a 2 o más preguntas, priorizar implementación.

## Checklist de arranque en 20 minutos

- [ ] Definir alcance MVP en 10–15 bullets.
- [ ] Crear backlog inicial con 5–8 issues máximas.
- [ ] Marcar una issue de simplificación/refactor temprano.
- [ ] Dejar preparado el comando de ejecución local y validación UI.
- [ ] Ejecutar la primera unidad funcional visible.

## Adaptación explícita para este repositorio

A partir de este punto, el proyecto **prioriza finalizar la app**: UI y
funcionalidades pendientes, manteniendo documentación/Issues/PR con nivel
ligero y orientado a ejecución.
