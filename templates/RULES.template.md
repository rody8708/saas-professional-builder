# Reglas del proyecto

Estado: {{borrador/aceptado}}

Responsable: {{responsable}}

Perfil: {{ruta y revisión del perfil del proyecto}}
Arquitectura: {{referencias de arquitectura/decisiones}}

Adapta esta plantilla al producto. DEBE equivale a MUST y expresa una invariante obligatoria; DEBERÍA equivale a SHOULD y permite una excepción documentada. Toda excepción registra responsable, motivo, alcance, mitigación y condición de revisión. Los requisitos se aplican a las capacidades realmente presentes.

## Producto y arquitectura

- Se DEBE conservar la propiedad declarada de módulos/datos y los contratos de compatibilidad.
- Se DEBE poder hacer cumplir la autoridad y las invariantes de negocio con independencia del comportamiento de la UI.
- Se DEBERÍAN usar los mecanismos mantenidos del framework seleccionado y la estructura de despliegue más sencilla que cumpla los requisitos.
- Se DEBERÍAN añadir abstracciones para límites/variaciones reales, no una interfaz o servicio por clase de forma predeterminada.
- Se DEBEN documentar los efectos que atraviesan límites transaccionales y proporcionar recuperación cuando la pérdida o duplicación incumpla el contrato.
- Controles de arquitectura: {{controles reales, alcance y limitaciones conocidas}}.

## Identidad y tenants

- Se DEBE autenticar mediante mecanismos mantenidos y validar el estado de credenciales/usuarios.
- Se DEBEN revalidar permisos, pertenencia activa y estado del tenant en las operaciones protegidas, incluidos los puntos de entrada alternativos.
- Se DEBE aplicar el modelo de tenants elegido en lecturas, escrituras, relaciones, trabajos, cachés, archivos, búsquedas y exportaciones.
- Se DEBEN probar la denegación entre tenants y la ausencia de filtraciones indirectas.
- Modos de autenticación y política de autenticación reforzada: {{referencias}}.
- Modelo de tenants y propietarios de datos: {{referencias}}.

## Seguridad y privacidad

- Se DEBEN proteger contra CSRF las modificaciones autenticadas mediante credenciales adjuntadas automáticamente; las rutas exclusivamente Bearer rechazan el recurso alternativo a cookies; los webhooks verifican las firmas del cuerpo original y los controles contra repetición.
- Se DEBE codificar/sanear la salida según el contexto, validar esquemas de URL y usar API de consulta seguras con valores parametrizados.
- Se DEBEN limitar las llamadas externas, las cargas de archivos y el coste de endpoints públicos; aplicar la política acordada de tráfico saliente/TLS.
- Se DEBEN mantener seguros los errores públicos y minimizar/depurar los registros con acceso controlado.
- Se DEBEN mantener secretos y datos operativos/de clientes fuera del control de versiones y de los datos de prueba.
- Se DEBEN definir exportación, supresión, retención, propiedad compartida y comportamiento de restauración antes de implementar políticas destructivas de datos.
- Política de datos: {{referencia}}. No se implica ninguna regla universal de retención, plazo de gracia ni bloqueo por suscripción.

## Consistencia y operaciones comerciales

- Se DEBEN definir límites transaccionales y de concurrencia para las operaciones que cambien invariantes.
- Se DEBEN conservar una clave de idempotencia y un contenido de solicitud estables en los reintentos de una misma operación externa.
- Se DEBEN reconciliar los resultados desconocidos antes de iniciar otro efecto que pueda duplicar un cobro o una modificación.
- Se DEBE usar outbox o un mecanismo duradero equivalente cuando la pérdida de una entrega incumpla el contrato.
- Política de facturación/derechos de acceso, si aplica: {{referencia o no aplicable}}.

## Verificación y limpieza

- Se DEBEN usar identidades sintéticas e infraestructura aislada; las pruebas no pueden leer archivos de entorno/bases de datos operativos.
- Se DEBEN registrar los recursos propios, desmontarlos tanto ante fallo como ante éxito y verificar su ausencia.
- Se DEBE probar la semántica de la base de datos en el motor de producción soportado y en cualquier otro motor prometido.
- Se DEBEN demostrar las regresiones de defectos antes/después y repetir los flujos significativos afectados mediante sus puntos de entrada reales.
- Se DEBEN registrar resultados reales y brechas explícitas; salud, cobertura y revisión por sí solas no demuestran aceptación funcional.
- Comandos, matriz y umbrales de pruebas: {{referencias reales del perfil del proyecto}}.

## Experiencia y documentación

- Se DEBEN cumplir la accesibilidad, los idiomas, formatos, dispositivos/temas soportados y estados del flujo acordados.
- Se DEBEN actualizar los contratos, las guías para usuarios/desarrolladores y la documentación de operación afectados por cambios de comportamiento.
- Se DEBERÍAN mantener claros los textos de usuario y vinculados a su fuente los límites/nombres de planes dinámicos.
- Estándares de experiencia/publicación: {{referencias}}.

## Entrega y operación

- Se DEBE inspeccionar el diff final, buscar datos privados y verificar la limpieza antes de publicar.
- Se DEBEN usar migraciones versionadas y documentar compatibilidad, despliegue y reversión/recuperación hacia delante.
- Se DEBEN definir responsables operativos, destino de alertas, SLO y objetivos de recuperación; solo la evidencia medida demuestra su cumplimiento.
- Se DEBEN seguir la autorización del usuario y la política real de ramas/CI/publicación del repositorio.
- Referencias de entrega, CI, restauración e incidentes: {{rutas}}.
