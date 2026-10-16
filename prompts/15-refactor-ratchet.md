# 15 · Refactorizar un límite declarado sin cambiar el comportamiento

## Objetivo
{{Infracción de un límite o elemento de deuda, excepción actual y módulo responsable}}

## Procedimiento
1. Lee las reglas y el perfil del proyecto y la [guía de arquitectura](../core/architecture.md). Confirma que la regla proteja un límite real y no una preferencia de estilo.
2. Caracteriza el comportamiento y los fallos pertinentes antes de mover código; añade la cobertura significativa que falte.
3. Refactoriza mediante la composición y las convenciones nativas del framework. Añade interfaces/adaptadores solo donde mejoren el aislamiento o la capacidad de sustitución.
4. Conserva la semántica de transacciones, autorización, tenants y efectos secundarios. Una nueva abstracción no debe ocultar cambios en reintentos o durabilidad.
5. Elimina la excepción resuelta en el mismo cambio. Ejecuta el control y compara su alcance/umbrales con la base para comprobar que no se haya reducido silenciosamente la cobertura.
6. Ejecuta las pruebas afectadas y las comprobaciones obligatorias; repite el punto de entrada real relevante cuando pueda verse alterado el comportamiento.
7. Actualiza la documentación de arquitectura y el estado de la deuda; limpia los recursos propios.

## Restricciones
No mezcles cambios de comportamiento ajenos al alcance. Si un defecto recién descubierto requiere un comportamiento diferente, asígnale una decisión explícita, una regresión y un cambio coherente. No amplíes las exclusiones para que la refactorización supere las pruebas; un cambio intencional de regla requiere una decisión de arquitectura documentada.

## Entregar
Cambio de límite/deuda, evidencia de comportamiento antes/después, comprobaciones, excepciones eliminadas y riesgo pendiente. No sustituyas el framework acordado por infraestructura propia como parte de una refactorización.
