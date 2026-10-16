# API y clientes

Web, clientes nativos e integraciones consumen contratos del backend. El servidor decide identidad, permisos, tenant, invariantes y derechos comerciales; el estado local solo representa una proyección.

## Contrato

Antes de implementar, define entrada, autenticación, permisos, esquema, errores estables, compatibilidad y límites. Incluye paginación, idempotencia, cargas de archivo y sincronización únicamente cuando apliquen. Usa la especificación de API y generación de clientes acordadas en el perfil.

- Valida tipos, tamaños y rangos en servidor, aunque el cliente ya valide.
- Errores seguros y códigos estables; identificador de correlación sin exponer datos privados.
- Una incompatibilidad necesita versión nueva o transición demostrada con clientes anteriores.
- JSON se serializa como JSON con tipo de contenido correcto; no escapes todos sus campos como HTML.
- Las rutas documentadas deben existir o figurar expresamente como propuestas.

## Autenticación según la superficie

| Modo | Frontera y verificación |
|---|---|
| Navegador con sesión/cookies | Protección CSRF en operaciones con cambios de estado, cookies seguras y autorización |
| Bearer-only | Credencial explícita de autorización, sin fallback a cookie ni dependencia de sesión de navegador |
| Webhook firmado | Firma sobre cuerpo crudo, tolerancia temporal, replay/idempotencia, sin CSRF de navegador |

Una ruta no queda exenta de CSRF por llamarse API. Los flujos públicos de login, recuperación y challenge tienen su propio contrato y controles de abuso. En rutas Bearer-only, una cookie válida sin token válido no autoriza; cuando ambos llegan, solo el token fija el contexto y la sesión de navegador permanece intacta.

Tokens revocables y de duración definida; almacenamiento seguro del cliente. Define rotación, revocación y recuperación si hay credenciales de renovación. No embebas secretos del backend en un cliente distribuido. La autenticación reforzada y los cambios de membresía tienen efecto coherente entre superficies.

Cada petición protegida valida usuario, credencial, membresía, permisos y requisitos comerciales aplicables. La selección de tenant del cliente se verifica contra la identidad vigente.

## Caché y offline, si se necesitan

Acota caché y colas por entorno, usuario, tenant y módulo. Cifra datos sensibles según el diseño de almacenamiento; define expiración, invalidación y limpieza al cerrar sesión, revocar o cambiar identidad/tenant.

Operaciones offline se muestran pendientes hasta confirmación. Define conflictos, orden, borrados, reintentos e idempotencia; no sobrescribas silenciosamente cambios remotos. Una sincronización incremental requiere cursor consistente y política de caducidad/reinicio, incluidas las bajas. Una membresía revocada no se revalida con una copia local antigua.

## Arquitectura de cliente

Adopta las convenciones del framework elegido. Separa presentación, estado y transporte para probar flujos sin renderizar toda la app. Centraliza navegación protegida, errores y almacenamiento sensible; no dupliques reglas comerciales del backend como autoridad.

Versionado, identificador de build, distribución, actualización y notas visibles pertenecen al perfil del cliente. No impongas herramientas móviles a un producto solo web.

## Aceptación

Prueba contratos, permisos, aislamiento, credenciales expiradas/revocadas, cookie mezclada con Bearer, errores y duplicados. En dispositivos/superficies soportados verifica login reforzado, cambio de tenant, cierre de sesión, actualización y sincronización cuando existan. Comprueba resultado observable y estado persistido contra el laboratorio representativo.

Si hay contenido enriquecido o navegador embebido, define sanitización contextual y esquemas URL permitidos; prueba inyección y navegación externa. Registra las combinaciones de cliente, versión y entorno que no se ejecutaron.
