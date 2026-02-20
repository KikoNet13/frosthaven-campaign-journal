# Handbook Evergreen de Ingeniería de Contexto

## Metadatos

- `doc_id`: LEARN-HANDBOOK
- `purpose`: Guía reusable para trabajar con agentes en software.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-20
- `next_review`: 2026-03-20

## Cómo usar este documento

1. Usa cada principio como regla operativa.
1. Revisa el criterio de uso antes de tomar decisiones.
1. Complementa con ejemplos en `learning/frosthaven-annex.md`.

## Principio 1: objetivo y éxito explícitos

- Norma: declarar objetivo y criterio de éxito antes de ejecutar.
- Ejemplo: objetivo de fase y criterio de cierre por hito.
- Anti patrón: trabajar sin definición de “terminado”.
- Criterio de uso: inicio de sesión y cambio de alcance.

## Principio 2: separar hechos de preferencias

- Norma: distinguir datos verificables de decisiones subjetivas.
- Ejemplo: “existe archivo X” es hecho, “prefiero Y” es preferencia.
- Anti patrón: convertir opiniones en restricciones técnicas.
- Criterio de uso: antes de preguntar o decidir.

## Principio 3: contexto en capas

- Norma: separar operación de aprendizaje.
- Ejemplo: `docs/` para ejecutar, `learning/` para transferir conocimiento.
- Anti patrón: mezclar reglas activas y notas didácticas.
- Criterio de uso: mover a `learning/` lo que sea reusable fuera del proyecto.

## Principio 4: trazabilidad de decisiones

- Norma: registrar problema, decisión, motivo, impacto y referencias.
- Ejemplo: entrada canónica en `docs/decision-log.md`.
- Anti patrón: decisiones dispersas en chat sin registro.
- Criterio de uso: registrar antes de cerrar el hito.

## Principio 5: verificación doble

- Norma: revisar estructura y criterios en dos pasadas.
- Ejemplo: primera pasada de presencia, segunda de edge cases.
- Anti patrón: una sola revisión superficial.
- Criterio de uso: obligatorio en cierre de hito.

## Principio 6: simplicidad de instrucciones

- Norma: instrucciones claras, concretas y verificables.
- Ejemplo: “No implementar código de app en Fase 0”.
- Anti patrón: prompts largos ambiguos.
- Criterio de uso: si no se puede verificar, hay que reescribir.

## Principio 7: gestión de alucinaciones

- Norma: asumir error posible y añadir controles.
- Ejemplo: contrastar decisiones con archivos y fuentes.
- Anti patrón: aceptar salidas sin comprobación.
- Criterio de uso: al menos una verificación cruzada por hito.

## Principio 8: cierre accionable

- Norma: cerrar con siguientes pasos concretos.
- Ejemplo: menú numerado de 3 a 5 opciones.
- Anti patrón: cierre vago sin acciones.
- Criterio de uso: siempre al finalizar una entrega.

## Playbook rápido por sesión

1. Definir objetivo y criterio de éxito.
1. Leer reglas activas.
1. Ejecutar hito.
1. Registrar decisiones.
1. Completar verificación doble.
1. Cerrar con menú de siguientes pasos.
