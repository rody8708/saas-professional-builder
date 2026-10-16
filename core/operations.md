# Operación, recuperación y objetivos de servicio

Antes de declarar disponibilidad, define responsable, servicios críticos, SLO, presupuesto de error, RPO, RTO y coste. Son objetivos del producto; solo evidencia medida permite afirmar que se alcanzaron.

## Configuración y despliegue

Configura entornos y secretos con mecanismos del stack. Ejemplos contienen placeholders, nunca valores operativos. El validador distingue errores bloqueantes y avisos; comprueba prerrequisitos antes de migrar y salud funcional después.

El runtime ejecuta un artefacto identificable y reproducible. Datos, logs y secretos viven fuera del artefacto fuente. Define rollout, compatibilidad de esquema, observación y condiciones de abortar; no editar a mano una release generada.

## Jobs y colas

Documenta scheduler/launcher, dueños y frecuencia según el trabajo. Claims atómicos, leases con fencing cuando corresponda, timeout y recuperación de ejecuciones abandonadas. Reintentos con límites/backoff y tratamiento visible de agotamiento; efectos idempotentes.

Emite inicio, resultado y heartbeat minimizados. Un heartbeat del launcher no acredita que cada job termine: vigila atraso de cola, ejecución y resultado. Evita múltiples registros divergentes de tareas. Las tareas durables perdidas se recuperan mediante outbox o mecanismo equivalente.

## Backups y restauración

- Cadencia y cobertura derivadas del RPO; copias cifradas fuera del dominio de fallo, acceso mínimo y retención explícita.
- Claves y versiones históricas necesarias se recuperan desde un mecanismo separado; una copia cifrada sin claves recuperables no es una estrategia de restauración.
- Verifica integridad y restaura periódicamente en recursos aislados; mide tiempo y punto de recuperación, incluyendo archivos, datos, configuración no secreta y dependencias necesarias.
- Comprueba invariantes de la aplicación tras restaurar, reanudación de trabajos y obligaciones de supresión/retención.
- Registra evidencia del ensayo, fallos y acción correctiva. No afirmar RTO/RPO demostrados con una mera copia completada.

## Observabilidad e incidentes

Define señales de disponibilidad, errores, latencia, saturación y flujos de negocio. Correlación de solicitudes/trabajos sin introducir PII innecesaria; logs y trazas redactados antes de exportar, con permisos y retención.

Una comprobación ligera de salud sirve al enrutamiento; una monitorización externa independiente detecta pérdida del sistema. La profundidad de readiness y alertas corresponde al modo de fallo. Prueba que una alerta llega al responsable y que existe escalamiento.

Agotamiento de conexiones, almacenamiento o dependencias debe producir rechazo controlado, backpressure y errores seguros, no éxito aparente. La respuesta reintentable y su demora se ajustan al protocolo; nunca exponer credenciales ni detalles internos.

Retención atrasada, recuperación fallida y trabajos estancados se clasifican según severidad y plazos del producto; no silenciarlos porque el proceso siga vivo.

## Runbooks y aceptación

Para incidentes críticos, documenta señales, propietario, precondiciones, pasos, comprobaciones, rollback/recuperación y evidencia segura. Incluye pérdida de proveedor, restauración, rotación de secretos y backlog cuando apliquen.

Ensaya fallos sintéticos en recursos propios: worker interrumpido, lease vencido, dependencia caída, disco/cuota, heartbeat viejo, backup inválido y restauración. Verifica alerta, recuperación y efectos únicos. Limpia solo los recursos registrados y comprueba que desaparecieron.

La salida es un mapa de controles verificados, pendientes y no aplicables con dueño. Un health verde no certifica ni operación recuperable ni flujos comerciales.
