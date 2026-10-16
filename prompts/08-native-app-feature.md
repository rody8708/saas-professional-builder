# 08 · Añadir una funcionalidad de cliente con contrato de backend

## Funcionalidad
{{Plataformas de cliente, flujo, roles, necesidades sin conexión y criterios de aceptación}}

## Procedimiento
1. Lee las reglas, el perfil del proyecto/cliente y la [guía de API y clientes](../core/api-and-native-clients.md). Usa el framework de cliente elegido y sus convenciones existentes.
2. Define o amplía el contrato real de API: autenticación, permisos, datos, errores, compatibilidad, paginación e idempotencia cuando corresponda. Documenta los campos/endpoints propuestos antes de utilizarlos.
3. Implementa autorización en el backend y pertenencia vigente al tenant. Para rutas exclusivamente Bearer, rechaza el recurso alternativo a cookies y no modifiques sesiones del navegador; no exijas CSRF del navegador. Las rutas autenticadas mediante cookies mantienen su protección CSRF declarada.
4. Implementa estado, navegación, transporte y almacenamiento seguro de credenciales del cliente mediante la arquitectura establecida. El backend conserva la autoridad sobre las decisiones comerciales y de seguridad.
5. Si se requiere funcionamiento sin conexión, delimita cachés/colas por entorno+usuario+tenant, marca las escrituras pendientes y define conflictos, caducidad de cursores, eliminación y resincronización. Borra o cambia el ámbito de los datos al cerrar sesión, revocar acceso o cambiar de contexto.
6. Renderiza el texto como texto; el contenido enriquecido o la navegación integrada requieren saneamiento contextual y una política de URL.
7. Verifica los diseños acordados, la accesibilidad, los idiomas y todos los estados alcanzables. Aplica la política real de versiones/publicación del cliente.
8. Ejecuta las comprobaciones específicas del perfil y ejercita el cliente real contra el laboratorio aislado: inicio de sesión, autenticación reforzada, cambio de tenant, denegación, revocación, reintento y recuperación de la conexión, cuando corresponda.

## Entregar
Contrato e implementación, comprobaciones, matriz de dispositivos/clientes/versiones, evidencia del estado persistido, limpieza y casos no ejecutados. No impongas una aplicación nativa a un producto cuyo cliente solicitado sea exclusivamente web.
