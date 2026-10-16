# Arquitectura comprobable

La arquitectura debe facilitar cambios, pruebas y operación. Elige su estructura con el perfil del proyecto y las convenciones del framework; no impongas un árbol de carpetas o un número de servicios universal.

## Fronteras y responsabilidades

| Responsabilidad | Regla verificable |
|---|---|
| Entrada y presentación | Traducir solicitudes, validar su forma, resolver el modo de autenticación y llamar a la operación de aplicación |
| Aplicación | Coordinar el caso de uso, autorización, transacción, idempotencia y resultado |
| Negocio | Expresar invariantes y decisiones sin depender innecesariamente del transporte o de un proveedor |
| Persistencia e integraciones | Encapsular consultas, almacenamiento y protocolos externos con contratos comprobables en pruebas |
| Composición | Configurar dependencias y ciclos de vida en los puntos previstos por el framework |

Estas responsabilidades pueden convivir en módulos o cortes verticales. Usa interfaces en fronteras donde permiten sustituir infraestructura o proteger ownership; no añadas una interfaz, factory o repositorio genérico por cada clase. Los servicios pequeños y condicionales legibles no son defectos por sí mismos. Extrae estrategias cuando existan variaciones reales con cambios independientes.

## Datos y efectos

- Una operación atómica define su frontera transaccional explícitamente. Las transacciones anidadas, bloqueos y niveles de aislamiento deben corresponder al motor elegido.
- La autoridad se resuelve en servidor y se comprueba en la operación, también cuando la invocan un job o una API diferente. El repositorio impide acceso cruzado según el modelo de tenancy.
- Efectos externos no comparten automáticamente la transacción de la base de datos. Si perder una entrega viola el contrato, persiste intención y estado; usa outbox transaccional o una garantía durable equivalente.
- El consumidor de una entrega durable es idempotente. Define reintentos, orden, duplicados, agotamiento, retención y reconciliación; un bus en memoria no ofrece esa garantía.
- Para consistencia entre servicios, documenta estados intermedios y compensaciones. Evita presentar una compensación como rollback de un efecto irreversible.
- Llamadas externas tienen timeout, límites de recursos y clasificación de errores. Ningún retry puede duplicar una mutación cuya respuesta se perdió.

## Framework y dependencias

Aprovecha mecanismos soportados del framework para inyección de dependencias, rutas, validación, sesiones, trabajos y acceso a datos. No inventes un contenedor, router, autenticación o criptografía salvo necesidad explícita y evaluada. Usa consultas parametrizadas o el mecanismo seguro equivalente; un ORM no elimina las obligaciones de autorización, tenancy y rendimiento.

Documenta las versiones soportadas, procedencia de dependencias, lockfiles y proceso de actualización. El análisis de tipos, lint y pruebas se seleccionan mediante el [registro de perfiles](../profiles/registry.json).

## Controles de arquitectura

Define reglas concretas: dependencias permitidas, acceso entre módulos, ubicación de adaptadores, ownership y límites relevantes. El guard debe declarar qué detecta y qué no; falla si faltan raíces o no descubre el código esperado. Combina análisis de dependencias, pruebas y revisión donde un escáner textual sea insuficiente.

Para deuda existente, registra excepciones con responsable, motivo y criterio de retirada. Compara contra la base para impedir crecimiento accidental; no ocultes defectos subiendo umbrales o excluyendo rutas. Un cambio intencional de arquitectura exige decisión documentada y revisión de los controles afectados.

## Cuándo usar un ADR

Registra decisiones costosas de revertir: frontera de módulo/servicio, tenancy, consistencia, proveedor, modelo de permisos o recuperación. Describe alternativas y consecuencias, y señala qué pruebas sostienen la decisión. Usa [ADR.template.md](../templates/ADR.template.md); no conviertas cada refactor local en un trámite.
