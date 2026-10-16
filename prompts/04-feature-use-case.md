# 04 · Implementar una funcionalidad de principio a fin

## Solicitud
{{Historia de usuario, criterios de aceptación, actores permitidos, datos e interfaces afectados}}

## Procedimiento
1. Lee las reglas del proyecto, el perfil seleccionado y los contratos afectados. Identifica decisiones pendientes sobre permisos, tenants, aspectos comerciales o destrucción de datos antes de implementarlas.
2. Describe la operación: entrada, salida, fallos, autoridad, invariantes, transacción y efectos externos. Usa la composición y estructura establecidas por el framework.
3. Define una matriz de pruebas significativa: éxito, validación, denegación, otro tenant y los fallos pertinentes de concurrencia/reintento/dependencias.
4. Implementa en el límite adecuado. Mantén los detalles de protocolo en adaptadores y las decisiones de negocio comprobables; usa abstracciones cuando protejan un límite real.
5. Para efectos que no puedan perderse, persiste la intención con outbox o una garantía equivalente; haz que la entrega sea idempotente.
6. Aplica la protección correspondiente a la autenticación: CSRF para credenciales adjuntadas automáticamente, aislamiento estricto de rutas exclusivamente Bearer o verificación de webhooks firmados. Codifica la salida para su contexto real.
7. Implementa los estados de UI diseñados y la localización/accesibilidad acordadas, si la funcionalidad es visible.
8. Ejecuta las comprobaciones focalizadas y obligatorias del proyecto; después ejercita el punto de entrada real afectado en el laboratorio. Inspecciona el estado persistido y los efectos secundarios.
9. Sincroniza contratos y documentación; registra las brechas y la limpieza.

## Entregar
Comportamiento modificado y motivo, archivos, pruebas significativas, evidencia de aceptación y riesgos pendientes. Consulta la [guía de pruebas](../core/testing-verification.md); no declares aprobada una comprobación que no se haya ejecutado.
