# Cobros, derechos comerciales y reconciliación

Esta capacidad aplica solo cuando el producto cobra o limita acceso comercial. Define proveedor, modelos de venta, monedas, impuestos, cancelaciones, créditos y responsabilidad operativa antes de implementar; no heredes políticas de otro SaaS.

## Modelo y fronteras

El catálogo es fuente de planes y límites. El servidor resuelve entitlement, permiso y cuota por separado. El cliente muestra el resultado; un precio menor no implica automáticamente una pérdida menor de capacidades.

Un adaptador encapsula el protocolo del proveedor. Persistencia local y proveedor no comparten una transacción: usa intención durable, estados explícitos y reconciliación. Guarda importes con representación exacta y unidad/moneda definidas; no asumir que todas las monedas tienen dos decimales.

## Operaciones durables e idempotencia

1. Persiste transición, alcance exacto, operación, intento y payload congelado antes del efecto externo.
2. Asigna una clave estable por operación/intento. No reutilices una clave para payloads o efectos distintos.
3. Timeout, respuesta perdida, rate limit o error temporal no generan otra clave ni avanzan por sí solos el intento de pago. Reintenta/recupera la misma operación; un fallo local tras éxito remoto tampoco autoriza otro cobro.
4. Un intento nuevo requiere resultado anterior confirmado y una política que permita otro intento. Mientras sea desconocido, reconciliar o escalar, sin cobrar otra vez.
5. Documenta la ventana de idempotencia del proveedor; al acercarse a su fin, detener retries automáticos y resolver el estado. No rotar la clave ni reenviar a ciegas tras expirar.
6. Usa fronteras de unicidad y concurrencia para que dos workers no creen operaciones paralelas incompatibles.

La proyección de acceso se actualiza solo con confirmación verificada y vinculada al tenant, alcance, objeto, importe/moneda y periodo esperados. Un redirect de navegador o un evento no relacionado no acredita pago. Documenta qué significan trial, mora, suspensión, cancelación, reanudación y derechos permanentes.

## Webhooks y recuperación

Verifica firma sobre cuerpo crudo, timestamp y contexto/cuenta del proveedor; sin sesión de navegador ni CSRF. Rechaza firmas ausentes, inválidas o expiradas sin efectos.

Persiste el evento minimizado y reclama procesamiento con idempotencia, lease y fencing cuando corresponda. Evento completado es no-op; en curso/almacén indisponible requiere respuesta reintentable según contrato. Un lease vencido no permite que el propietario antiguo escriba después.

Eventos duplicados o fuera de orden deben converger. Consulta el estado canónico del proveedor cuando el flujo lo requiera y ejecuta reconciliación periódica; no confíes exclusivamente en la entrega del webhook. Las entregas durables derivadas usan outbox o garantía equivalente.

## Ciclo de vida y políticas

Cambios inmediatos/diferidos, cancelaciones y reversos siguen reglas comerciales explícitas. La política de reintentos de cobro tiene reloj propio independiente de emails; nunca inicia otro pago mientras el anterior sea desconocido. Una compuerta de catálogo/entitlement indisponible no deriva a un camino permisivo.

No sobrescribas historia financiera confirmada. Reembolsos, disputas y ajustes son hechos posteriores enlazados, con reversos o asientos según el modelo. Deshabilitar nuevas ventas no debe apagar reconciliación de obligaciones pendientes.

Cobros, cierre de cuenta, aceptación de solicitudes de datos y conservación de registros se definen por separado con la política de privacidad.

## Aceptación

Usa clientes y medios sintéticos en sandbox. Prueba éxito, rechazo, timeout después de aceptación, fallo local posterior, retry con la misma clave, concurrencia, firma inválida, duplicados, desorden, cancelación/reversión y recuperación tras caída. Verifica un solo cobro, proyección correcta y estado persistido.

Distingue simulación determinista de ejercicio real del proveedor; documenta casos que el sandbox no permita. No usar claves live ni desactivar TLS. La evidencia debe permitir reconstruir la decisión sin exponer datos de pago o clientes.
