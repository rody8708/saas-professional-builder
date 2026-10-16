# Seguridad, tenancy y privacidad

Los controles se seleccionan por amenazas y superficies reales. Usa los mecanismos mantenidos del stack acordado y verifica su configuración; la existencia de un middleware no prueba su cobertura.

## Identidad y autorización

- Autenticación con bibliotecas/proveedores mantenidos; si gestionas contraseñas, hashing resistente y parámetros revisados según el entorno. No diseñes criptografía propia.
- Recuperación, verificación de identidad, enrolamiento y autenticación reforzada con tokens de vida limitada, uso único, rate limits y respuestas que reduzcan enumeración.
- Regenera la sesión tras autenticación/elevación; cookies seguras y revocación comprobable. Si existe registro de sesión, fallos de lectura/escritura no dejan autenticación parcial utilizable.
- Permisos explícitos en la operación de aplicación. Revalida membresía, estado del usuario/tenant y autoridad de plataforma; ocultar UI no autoriza.
- Suplantación, si existe, requiere autoridad, auditoría, límites y restauración completa del contexto. Revocarla debe tener efecto inmediato según el contrato.
- Deniega por defecto cuando no pueda determinarse la autoridad; distingue dependencia caída de permiso denegado sin filtrar internals.

## Aislamiento de datos

El modelo de tenancy puede ser por fila, esquema, base o frontera equivalente. Documenta cómo se aplica en lecturas/escrituras, joins, agregados, búsquedas, jobs, cachés, archivos, exportaciones y eventos. En esquema compartido, claves/relaciones deben impedir asociaciones entre tenants, no solo filtrar listas.

No confíes en tenant, propietario o rol enviados por cliente. Trabajos diferidos llevan contexto explícito, comprueban autoridad según su contrato y no heredan una sesión global. Caches y archivos se particionan por identidad y alcance adecuados.

Prueba dos tenants, cambio de membresía, identificadores manipulados, colisiones de cache, descarga directa y tareas pendientes. Comprueba que no se revelan conteos ni metadatos ajenos.

## Controles de entrada y salida

| Riesgo | Control y prueba |
|---|---|
| CSRF | Con cookies/credenciales ambientales: protección en toda mutación, incluidos métodos parciales; ningún GET muta. Probar token ausente/inválido/válido |
| Bearer-only | Autorización explícita sin fallback a cookie; probar cookie válida con token ausente/inválido y cookie/token de distintos tenants |
| Webhook | Firma sobre cuerpo crudo, timestamp y replay/idempotencia; entrega válida sin sesión, firma inválida/expirada sin efectos |
| XSS | Codificación según contexto HTML/atributo, inserción segura de datos en scripts, validación de esquemas URL; sanitización por allowlist si hay HTML enriquecido |
| Inyección | Consultas parametrizadas y APIs seguras; campos estructurales como ordenación se eligen de una allowlist |
| Archivos | Tamaño/tipo/contenido permitidos, nombres no confiables, almacenamiento sin ejecución, autorización de lectura y política de análisis según riesgo |
| SSRF | Restringir destinos, resolver y validar las IP para bloquear redes internas/metadatos y fijar el destino de conexión conservando hostname/TLS; si el cliente no garantiza esa frontera, usar un control de egreso equivalente o rechazar la operación. Validar cada redirect o deshabilitarlo; no aceptar proxies de entorno no controlados |
| Proxy y TLS | Confiar solo en proxies declarados; origen/HTTPS canónicos, certificados verificados, sin bypass de TLS |
| Abuso | Límites de frecuencia, tamaño, concurrencia y coste con claves de alcance correctas; recuperación y endpoints públicos incluidos |

Un escape HTML no protege URLs ni contextos ejecutables. Prueba ruptura de atributos, esquema peligroso y cierre de contexto de script donde exista. SameSite complementa CSRF; un prefijo de ruta no concede excepciones.

## Secretos, errores y observabilidad

Secretos en mecanismos de configuración/gestión aprobados; rotación y alcance mínimo. No poner valores reales en ejemplos, repositorios, clientes distribuidos o logs. El cifrado de secretos persistidos necesita recuperación de claves separada de las copias de datos.

Errores públicos categorizados y seguros, sin consultas, credenciales, trazas o rutas privadas. Logs estructurados minimizados con correlación y redacción previa a servicios externos; acceso y retención definidos. No asumir que un redactor detecta todos los secretos.

## Política de datos explícita

Antes de exportar, suprimir o retener, documenta categorías, finalidad, ownership, plazos, excepciones y jurisdicciones aplicables. Esta guía técnica no certifica cumplimiento legal ni fija plazos universales.

- Exportación autenticada, completa según contrato y aislada; no inferir que un rol operativo posee datos de otro cliente.
- Solicitud, verificación, gracia si corresponde, ejecución y cancelación de supresión definidas. Distinguir borrado, conservación limitada, seudonimización y anonimización; no prometer irreversibilidad sin demostrarla.
- Cobros, cierre del servicio y aceptación de solicitudes se deciden por separado. No bloquear automáticamente derechos de datos por una suscripción.
- Workspaces compartidos, último propietario, transferencia y registros de otros clientes necesitan reglas explícitas antes de cualquier purga.
- Retención por categoría aplicada mediante trabajos idempotentes, métricas y alertas. Incluir backups, exportaciones, cachés, adjuntos y datos de personas sin cuenta.
- Restaurar una copia no debe reintroducir silenciosamente datos ya suprimidos; documentar y ensayar el mecanismo aplicable.

Prueba con identidades sintéticas exportación aislada, borrado parcial/reintento, estados de suscripción, propiedad compartida y conservación/purga conforme a la matriz. Una política indefinida se registra como decisión pendiente; no se inventa mediante una migración.
