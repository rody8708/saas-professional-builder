# Perfil del proyecto: {{nombre del proyecto}}

Estado: {{borrador / aceptado / parcialmente decidido}}

Responsable: {{responsable}}

Actualizado: {{fecha}}

Perfil técnico: {{id y ruta del catálogo de perfiles}}
Referencias de decisiones: {{decisiones y requisitos aceptados}}

Completa lo que afecte a la tarea actual. Marca las incógnitas como pendientes con impacto/responsable; no las sustituyas silenciosamente por valores predeterminados. El perfil selecciona mecanismos y la guía del núcleo define garantías.

## Producto y alcance

| Campo | Decisión |
|---|---|
| Usuarios y flujos de valor | {{actores y tareas}} |
| Hito actual y aceptación | {{entregable delimitado}} |
| Capacidades explícitamente excluidas | {{alcance}} |
| Sensibilidad de datos y restricciones de despliegue | {{restricciones}} |
| Responsables de decisiones de producto/ingeniería/seguridad | {{roles}} |

## Tecnologías y repositorio

| Campo | Decisión |
|---|---|
| Lenguaje/entorno de ejecución y versiones soportadas | {{decisión}} |
| Framework y convenciones | {{decisión}} |
| Gestor de paquetes y estrategia de fijación de dependencias | {{decisión}} |
| Interfaces/frameworks de cliente | {{decisión}} |
| Arquitectura/estructura de despliegue y motivo | {{decisión}} |
| Límites de módulos y responsables | {{decisión}} |
| Repositorio/visibilidad y rama de integración | {{decisión; sin remoto si no existe}} |
| Política de base/ramas/cambios | {{decisión}} |
| Autoridad para publicar, fusionar y desplegar | {{roles y autorización existente}} |

Usa las funciones del framework cuando sean adecuadas; la infraestructura propia necesita un motivo concreto.

## Persistencia y tenants

| Campo | Decisión |
|---|---|
| Motor/versión de producción y otros motores soportados | {{decisión}} |
| Modelo de tenants y resolución del contexto efectivo | {{fila/esquema/base de datos/otro}} |
| Restricciones de relaciones y propiedad de datos compartidos | {{decisión}} |
| Aislamiento de lecturas/escrituras/búsquedas/exportaciones | {{mecanismos}} |
| Aislamiento de trabajos/colas/cachés/archivos | {{mecanismos}} |
| Transacciones, concurrencia y representación numérica exacta | {{decisión}} |
| Migración/relleno de datos/expansión y contracción/recuperación | {{mecanismo y responsables}} |
| Eventos duraderos, outbox y reconciliación | {{efectos requeridos y mecanismo}} |

## Identidad y autoridad

| Campo | Decisión |
|---|---|
| Proveedor de identidad/mecanismo de credenciales | {{decisión}} |
| Registro, recuperación y controles contra abuso | {{decisión}} |
| Requisitos de autenticación reforzada y equivalencia entre interfaces | {{decisión}} |
| Duración de sesiones/tokens, revocación y almacenamiento seguro | {{decisión}} |
| Contratos de rutas con cookies, exclusivamente Bearer y webhooks | {{decisión}} |
| Roles/capacidades y permisos compuestos | {{decisión}} |
| Cambios de pertenencia y revalidación | {{decisión}} |
| Autoridad de plataforma/suplantación administrativa, si se necesita | {{decisión o no aplicable}} |

## Capacidad comercial

| Campo | Decisión |
|---|---|
| Necesidad de facturación | {{sí/no y alcance}} |
| Proveedor, modelo de cuentas y ciclo de vida de API | {{decisión o no aplicable}} |
| Planes/derechos de acceso/cuotas y fuente de verdad | {{decisión}} |
| Dinero, monedas, impuestos y redondeo | {{decisión}} |
| Cancelación, reembolsos, disputas y política de reintentos | {{decisión}} |
| Ventana de idempotencia, resultados desconocidos y reconciliación | {{decisión}} |
| Interacción entre aspectos comerciales y privacidad | {{política explícita, no inferida}} |

## Ciclo de vida de los datos

| Categoría/finalidad | Propietario/ámbito | Exportación | Supresión/conservación | Retención/inicio | Tratamiento al restaurar |
|---|---|---|---|---|---|
| {{categoría}} | {{propietario}} | {{contrato}} | {{política}} | {{duración/evento}} | {{método}} |

{{Incluye registros, archivos subidos, copias de seguridad, visitantes sin cuenta y cualquier procesamiento externo. Indica revisión de política/jurisdicción aplicable, excepciones, propiedad compartida, atención de solicitudes y plazo de gracia solo si se ha elegido. Sin afirmaciones legales universales ni plazos fijos predeterminados.}}

## Experiencia e idioma

| Campo | Decisión |
|---|---|
| Idiomas del producto y de ingeniería/documentación | {{decisión}} |
| Idioma alternativo, zona horaria, moneda y formatos | {{decisión}} |
| Objetivo de accesibilidad y verificación | {{decisión}} |
| Dispositivos, tamaños de ventana, temas y sistema de diseño | {{decisión}} |
| Funcionamiento sin conexión/compatibilidad de clientes y política de versiones | {{decisión o no aplicable}} |
| Capacidad y autoridad de ayuda/asistente | {{decisión o no aplicable}} |

## Compilación, comprobaciones y CI

Enumera los comandos verificados en el proyecto real; los marcadores de posición no son instrucciones ejecutables.

| Finalidad | Comando/herramienta real | Entorno requerido | Evidencia/estado |
|---|---|---|---|
| Instalación/compilación | {{comando}} | {{entorno}} | {{estado}} |
| Formato/lint/tipos o análisis estático | {{comando}} | {{entorno}} | {{estado}} |
| Pruebas unitarias/de contratos | {{comando}} | {{entorno}} | {{estado}} |
| Pruebas de integración/motor de producción | {{comando}} | {{entorno}} | {{estado}} |
| UI/cliente/aceptación | {{comando o flujo}} | {{entorno}} | {{estado}} |
| Controles de arquitectura y dependencias | {{comando}} | {{entorno}} | {{alcance/límites}} |
| Búsqueda de secretos/datos privados | {{comando}} | {{entorno}} | {{estado}} |

Proveedor/agentes de ejecución de CI, límites de confianza, permisos, comprobaciones obligatorias, retención de artefactos y responsable: {{decisiones}}. Propiedad de recursos de prueba y desmontaje/verificación de ausencia: {{mecanismos}}.

## Operación y requisitos de aprobación

| Campo | Decisión |
|---|---|
| Entornos y laboratorio de aceptación representativo de producción | {{decisión}} |
| SLO/SLI, presupuesto de error y responsable de monitorización | {{decisión}} |
| RPO/RTO, cobertura de copias y frecuencia de restauración | {{decisión}} |
| Salud de trabajos/colas/retención y escalamiento | {{decisión}} |
| Gestión y rotación de configuración/secretos | {{decisión}} |
| Despliegue, interrupción, reversión/recuperación hacia delante | {{decisión}} |
| Manuales de incidentes y roles responsables | {{decisión}} |

| Requisito de aprobación | Evidencia necesaria | Responsable | Estado actual |
|---|---|---|---|
| {{requisito de capacidad/publicación}} | {{evidencia}} | {{responsable}} | {{verificado/pendiente/no aplicable con motivo}} |

## Decisiones pendientes

| Decisión | Trabajo afectado | Responsable | Siguiente acción |
|---|---|---|---|
| {{incógnita o ninguna}} | {{impacto}} | {{responsable}} | {{resolución}} |
