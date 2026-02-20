# Anexo Frosthaven (Casos Aplicados)

## Metadatos

- `doc_id`: LEARN-FROSTHAVEN-ANNEX
- `purpose`: Casos reales del proyecto para reforzar el método.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-20

## Caso 1: arranque con legado disperso

- Decisión real: mantener cuatro archivos legado sin borrado inmediato.
- Error evitado: perder contexto histórico temprano.
- Principio relacionado: contexto en capas y trazabilidad.
- Aplicación general: conservar legado hasta cerrar hitos verificados.

## Caso 2: conflicto entre objetivos

- Decisión real: priorizar aprendizaje de contexto frente a implementación.
- Error evitado: mezclar producto y proceso en una sola fase.
- Principio relacionado: objetivo y éxito explícitos.
- Aplicación general: fijar una prioridad por fase.

## Caso 3: separación documental

- Decisión real: `docs/` para operación y `learning/` para aprendizaje.
- Error evitado: documentos ambiguos con doble propósito.
- Principio relacionado: contexto en capas.
- Aplicación general: separar siempre ejecución y material didáctico.

## Caso 4: política de idioma

- Decisión real: castellano en descripciones, inglés en identificadores.
- Error evitado: inconsistencias terminológicas.
- Principio relacionado: simplicidad de instrucciones.
- Aplicación general: definir política de idioma al inicio.

## Caso 5: gate estricto antes de código

- Decisión real: bloquear implementación con decisiones abiertas.
- Error evitado: construir sobre supuestos inestables.
- Principio relacionado: verificación doble y trazabilidad.
- Aplicación general: definir criterios de entrada a implementación.

## Caso 6: verificación doble documentada

- Decisión real: registrar dos rondas de verificación en Fase 0.
- Error evitado: declarar cierre sin evidencia.
- Principio relacionado: verificación doble.
- Aplicación general: separar chequeo de estructura y chequeo lógico.

## Resumen operativo

1. El proyecto funcionó como laboratorio de método.
1. Las decisiones quedaron trazadas.
1. La capa oficial permite operar sin leer todo el legado.
