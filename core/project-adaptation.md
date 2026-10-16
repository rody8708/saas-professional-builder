# Perfil del proyecto y adaptación

El núcleo define resultados verificables; el perfil técnico elige cómo alcanzarlos. No contiene una aplicación terminada ni autoriza instalar herramientas o desplegarla.

## Punto de partida

1. Identifica la tarea: revisión, diseño, implementación o entrega. Una revisión permanece de solo lectura. Respeta las autorizaciones ya dadas y los cambios ajenos.
2. Lee las reglas, arquitectura y contratos existentes. Reutiliza las decisiones confirmadas; no reemplaces el gobierno del proyecto para hacer encajar una plantilla.
3. Consulta el [registro de perfiles](../profiles/registry.json). Selecciona el perfil del stack acordado y lee sus instrucciones. Un perfil ausente se documenta como pendiente; no improvises comandos de otro stack.
4. Completa las secciones pertinentes de [project-profile.template.md](../templates/project-profile.template.md). En proyectos existentes conserva las convenciones que ya funcionan; en proyectos nuevos propone la opción más sencilla que cubra los requisitos.
5. Vincula cada capacidad necesaria con su contrato, responsable y evidencia de aceptación. Implementa solo las capacidades del encargo.

## Decisiones que deben ser explícitas

| Área | Decisión que afecta la implementación |
|---|---|
| Producto | Usuarios, trabajos que realizan, límites, funcionalidades y criterios de éxito |
| Stack | Perfil, lenguaje, runtime, framework y versiones soportadas; comandos reales de build, análisis y pruebas |
| Datos | Motor de producción, motores soportados, modelo de tenancy, ownership, consistencia y migraciones |
| Identidad | Proveedor o implementación, credenciales, recuperación, autenticación reforzada y modos de autenticación por ruta |
| Autorización | Roles/capacidades, cambios de membresía, permisos compuestos y autoridad de plataforma |
| Clientes | Web, API, clientes nativos u otras superficies realmente necesarias |
| Comercial | Si hay cobros, modelo, proveedor, monedas, cuotas, cancelaciones y acceso |
| Privacidad | Categorías de datos, finalidades, exportación, supresión, retención y excepciones justificadas |
| Experiencia | Idiomas, accesibilidad, dispositivos, temas y sistema de diseño |
| Entrega | Repositorio, rama de integración, estrategia de cambios, CI y autoridad para publicar/desplegar |
| Operación | Entornos, responsables, SLO, RPO/RTO, alertas, recuperación y coste operativo |

Una decisión desconocida se marca pendiente con su impacto. Pregunta antes de programar una política ambigua de cobro, permisos, privacidad o destrucción de datos; avanza con trabajo independiente que ya esté autorizado. No conviertas una preferencia del paquete en un requisito del negocio.

## Escala proporcional

- Un producto puede empezar con un solo despliegue y módulos internos. Servicios separados requieren una necesidad demostrada de aislamiento, escalado u ownership.
- Facturación, bundles, aplicaciones nativas, sincronización offline y asistentes son capacidades opcionales.
- Usa el router, contenedor, autenticación y mecanismos de migración del framework elegido cuando sean adecuados; no construyas sustitutos por seguir un diagrama.
- Conserva las garantías comunes: autoridad del servidor, aislamiento de datos, efectos recuperables, pruebas sintéticas, evidencia honesta y documentación sincronizada.
- Los comandos y checks del perfil deben existir y ejecutarse en el destino. Una ruta de documentación o un nombre de herramienta no prueba que el control esté instalado.

## Entregable de adaptación

Perfil cumplimentado con decisiones, supuestos y pendientes; mapa de requisitos a controles; primer flujo completo con aceptación definida; lista de herramientas reales y responsables. El estado de cada control es implementado y verificado, implementado sin verificar, pendiente o no aplicable con motivo.
