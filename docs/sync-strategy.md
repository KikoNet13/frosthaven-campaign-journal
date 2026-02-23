# Estrategia de Sincronización MVP

## Metadatos

- `doc_id`: DOC-SYNC-STRATEGY
- `purpose`: Definir la estrategia de sincronización multidispositivo del MVP.
- `status`: active
- `source_of_truth`: official
- `last_updated`: 2026-02-23
- `next_review`: 2026-03-09

## Objetivo

Cerrar un contrato documental de sincronización para el MVP que priorice
simplicidad operativa y consistencia de datos, sin adelantar decisiones de
conflictos concurrentes ni de orden estable que pertenecen a Issues posteriores.

## Alcance MVP de sincronización

Incluye:

- lectura y escritura multi-dispositivo sobre Firestore;
- reglas operativas de lectura/escritura para uso normal;
- criterios de consistencia esperados en el MVP;
- límites aceptados y tradeoffs explícitos.

No incluye:

- política detallada de conflictos concurrentes (ver `docs/conflict-policy.md`,
  Issue #8);
- política de timestamps y desempate estable entre dispositivos (Issue #18);
- contrato de operaciones Firestore por agregado (Issue #12);
- soporte offline con cola de escrituras.

## Estrategia elegida

- **Fuente de verdad**: Firestore.
- **Modelo general**: sincronización multi-dispositivo con consistencia
  eventual controlada.
- **Modo operativo recomendado (MVP)**: `single writer`.
  - Se recomienda un dispositivo escribiendo activamente a la vez.
  - Otros dispositivos pueden consultar.
  - Si otro dispositivo escribe de forma concurrente, el resultado queda en
    zona de `best-effort` hasta definir la política de conflictos en la
    Issue #8 (`docs/conflict-policy.md`).
- **Política de conectividad para escrituras**: `online-only writes`.
  - Sin conexión, las escrituras del MVP se bloquean.
  - No existe cola offline de escrituras en esta fase.
- **Actualización entre dispositivos**: `on-demand refresh`.
  - Sin listeners realtime en el MVP.
  - Sin polling automático en el MVP.

## Reglas de lectura

1. La lectura inicial se hace contra Firestore al abrir la app o al entrar en
   una vista que necesite estado fresco.
1. Tras una escritura local confirmada, la UI debe recargar el estado relevante
   para reflejar la fuente de verdad.
1. Los cambios hechos desde otro dispositivo se observan tras refresco manual o
   recarga de la vista.
1. El MVP no garantiza propagación visual inmediata entre dispositivos.

## Reglas de escritura

1. Las escrituras se intentan solo con conectividad disponible.
1. Si no hay conectividad, la operación se rechaza o bloquea con feedback claro
   (sin encolar para sincronización posterior).
1. El uso normal esperado es `single writer`; el segundo dispositivo escritor no
   está prohibido por contrato, pero queda fuera del flujo recomendado.
1. La resolución de conflictos de escrituras concurrentes se rige por
   `docs/conflict-policy.md` (Issue #8).

## Criterios de consistencia del MVP

Se considera consistente (para el alcance del MVP) cuando se cumple:

- una escritura confirmada en Firestore puede verse desde otro dispositivo tras
  refresco manual o recarga;
- la lectura tras refresco representa la fuente de verdad remota;
- el comportamiento normal no depende de sincronización en tiempo real;
- las limitaciones de concurrencia y offline están explícitas en documentación.

## Garantías y límites aceptados

Garantías MVP explícitas:

- lectura consistente tras refresco manual o recarga;
- visibilidad cruzada entre dispositivos tras refresco;
- contrato de operación simple y predecible para uso normal.

Límites aceptados MVP:

- `No realtime guarantee`.
- no soporte formal de `multiwriter` coordinado.
- no escrituras offline ni cola de sincronización.
- conflictos concurrentes detallados se definen en `docs/conflict-policy.md`
  (Issue #8).
- política de timestamps y desempates se define en la Issue #18.

## Escenarios normales esperados

### Escenario A: un dispositivo escribe y otro consulta

1. Dispositivo A registra un cambio.
1. Firestore confirma la escritura.
1. Dispositivo B refresca manualmente.
1. Dispositivo B observa el estado actualizado.

### Escenario B: reconexión

1. Un dispositivo pierde conectividad.
1. Las escrituras quedan bloqueadas.
1. Recupera conectividad.
1. El usuario ejecuta refresco manual y continúa trabajando.

## Edge cases documentados (sin resolución detallada)

- Dos dispositivos escriben casi al mismo tiempo sobre el mismo agregado.
  - Esta estrategia solo define el límite de soporte del MVP.
  - La política de resolución se define en `docs/conflict-policy.md`
    (Issue #8).
- Diferencias de orden visual entre dispositivos por eventos casi simultáneos.
  - La política de timestamps y desempate queda en la Issue #18.
- La definición de operaciones por agregado y atomicidad se concreta en la
  Issue #12.

## Dependencias y relación con otras Issues

- **Issue #7**: documento de decisión principal (esta estrategia).
- **Issue #8**: política de conflictos concurrentes, documentada en
  `docs/conflict-policy.md` y dependiente de este marco.
- **Issue #18**: política de timestamps y orden estable (depende de #7 y debe
  ser compatible con #8).
- **Issue #12**: contrato de operaciones Firestore por agregado, que deberá
  respetar esta estrategia de sincronización.

## Referencias

- `docs/domain-glossary.md`
- `docs/conflict-policy.md`
- `docs/decision-log.md`
- `tdd.md` (legado temporal, alineado con referencia oficial)
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/7`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/8`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/12`
- `https://github.com/KikoNet13/frosthaven-campaign-journal/issues/18`
