# Entrega y cambios de datos

Una entrega es un cambio coherente con evidencia y recuperación conocidas. La estrategia de ramas, remotos y publicación pertenece al proyecto; no se presupone una rama con nombre fijo.

## Preparación y alcance

Lee reglas, perfil, documentación y estado actual. Respeta cambios ajenos. Parte de una base actualizada según la política elegida y verifica dependencias con cambios pendientes; no apiles cambios accidentalmente. En un repositorio sin remoto, declara esa condición.

Una petición de implementar autoriza su trabajo y verificación; publicación, merge y despliegue siguen la autorización de la conversación. No pidas de nuevo una autorización ya concedida. Si una decisión de datos, permisos, cobro o destrucción está indefinida, concreta lo revisable y resuelve esa decisión antes de ejecutar el efecto.

## Antes de entregar o publicar

- Inspeccionar lista de archivos y diff completo del cambio; confirmar alcance.
- Escanear secretos y datos privados; excluir configuración real, bases, logs, backups y adjuntos operativos.
- Ejecutar checks y aceptación definidos por el perfil y el impacto; registrar lo pendiente.
- Verificar limpieza de recursos temporales, incluidos los ignorados y externos.
- Sincronizar contratos, guías y operación con el comportamiento implementado.
- Documentar migraciones, compatibilidad, orden de despliegue y recuperación.
- Preparar descripción concreta y verificable con [PULL_REQUEST_TEMPLATE.md](../templates/PULL_REQUEST_TEMPLATE.md).

## Migraciones y compatibilidad

Usa el mecanismo versionado del stack; registra qué se aplicó y quién es dueño de cada cambio. Prueba en base vacía y poblada con datos sintéticos en cada motor soportado, incluido producción.

Para despliegues con versiones coexistentes, aplicar expand-contract: introducir estructura compatible, desplegar lectores/escritores compatibles, backfill idempotente y por lotes, verificar invariantes, retirar uso antiguo y solo después contraer. El paso destructivo requiere alcance explícito y evidencia de compatibilidad/recuperación.

El rollback de código no revierte automáticamente datos ni efectos externos. Define rollback cuando sea seguro o recuperación hacia adelante cuando no lo sea; ensaya la opción elegida. Contempla DDL parcial, locks, permisos del motor, interrupción y reanudación. No declarar reversible una migración que pierde información.

## CI y cadena de suministro

Los workflows usan herramientas del perfil, dependencias fijadas y permisos mínimos. Verifica que los comandos existen, los tests se descubren y los controles fallan ante una infracción real. Mantén logs/artefactos sanitizados y retención limitada.

La matriz refleja plataformas y motores soportados. Configura checks requeridos en la rama de integración cuando corresponda; un workflow presente no demuestra protección activa. Actualizaciones de runtime/dependencias requieren revisión de compatibilidad y validación proporcional.

Runners, secretos y artefactos se aíslan por confianza; código de contribuciones no confiables no recibe credenciales privilegiadas. Define quién administra CI y qué ocurre si un runner o servicio requerido no está disponible.

## Versiones, documentación y despliegue

La política de versiones distingue contratos públicos, aplicación y clientes distribuibles; no impongas un formato de archivo común. Las notas describen cambios visibles y compatibilidad en los idiomas acordados. Una entrega documental explica que no acredita ejecución de una aplicación.

Valida configuración y prerrequisitos antes de migrar; después verifica runtime, trabajos y flujos críticos. Define estrategia de rollout, observación, umbrales de abortar y rollback/recuperación. Registra revisión desplegada y evidencia. Un despliegue exitoso técnicamente no reemplaza aceptación del producto.
