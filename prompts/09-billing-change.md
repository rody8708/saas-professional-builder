# 09 · Cambiar la facturación de forma segura

## Cambio
{{Regla comercial, ámbitos afectados, proveedor y criterios de aceptación}}
Lee las reglas y el perfil del proyecto y la [guía de facturación](../core/billing-entitlements.md). La facturación solo está dentro del alcance cuando se solicita.

## Diseñar antes de producir efectos
- Define por separado el catálogo autoritativo, los derechos de acceso, los permisos y las cuotas.
- Describe la transición/operación/intento duraderos, el contenido de solicitud fijado, los importes/moneda exactos y el ámbito de unicidad.
- Reutiliza una misma clave de idempotencia ante reintentos de transporte, tiempo de espera agotado, respuesta perdida o fallo local tras un éxito remoto. Un nuevo intento de pago requiere confirmar el resultado anterior y una política explícita.
- Define confirmación del proveedor, vinculación de cuenta/ámbito/objeto, ventana de idempotencia, reconciliación de resultados desconocidos y escalamiento manual.
- Especifica cancelación, reversión, suspensión y calendario de reintentos; la disponibilidad del correo no determina el calendario del pago.
- Mantén separadas las solicitudes de privacidad y la cancelación del servicio según la política elegida.

## Implementar
Usa el adaptador del proveedor elegido y sus API realmente soportadas. Verifica las firmas entrantes sobre el cuerpo original con controles de marca temporal/repetición, sin sesión de navegador ni CSRF. Las reclamaciones exclusivas, las concesiones temporales y la exclusión de trabajadores obsoletos protegen el procesamiento concurrente. Los efectos posteriores duraderos necesitan outbox o una entrega equivalente. Conserva los hechos financieros inmutables y modela explícitamente los ajustes posteriores.

## Verificar
Usa datos sintéticos en el entorno de pruebas del proveedor. Prueba éxito, rechazo, solicitud aceptada con respuesta perdida, fallo de persistencia local, reintento concurrente, evento duplicado/fuera de orden, firma inválida, ventana de clave caducada, cancelación/reversión y recuperación tras una interrupción. Comprueba que haya un solo cobro, derechos de acceso correctos y estado duradero. Nunca cambies una clave para eludir un resultado desconocido.

Distingue la simulación determinista de la evidencia real del entorno de pruebas del proveedor; enumera los escenarios no soportados/no ejecutados. Usa solo credenciales de prueba y TLS válido, y elimina los recursos propios.

## Entregar
Cambios de reglas/contratos, implementación, evidencia significativa automatizada y del flujo real, actualizaciones de reconciliación/manuales operativos, limpieza y requisitos pendientes.
