# 01 · Crear la base de un SaaS profesional

## Solicitud
Crea la base autorizada para {{producto, usuarios, primer flujo de valor}} en {{directorio/repositorio de destino}}.

## Leer y decidir
Lee las reglas existentes del proyecto y la [guía de adaptación](../core/project-adaptation.md). Selecciona el perfil técnico acordado mediante el [catálogo de perfiles](../profiles/registry.json); utiliza las convenciones y herramientas reales de su framework. Reutiliza los requisitos confirmados.

Registra las decisiones pertinentes con el [perfil del proyecto](../templates/project-profile.template.md): tecnologías, persistencia, modelo de tenants, identidad, permisos, idiomas, clientes, facturación opcional, política de datos, CI, responsables y objetivos operativos. Pregunta solo por decisiones pendientes que afecten de forma sustancial al comportamiento o al riesgo; continúa el trabajo independiente ya autorizado.

## Implementar
1. Conserva el código y las convenciones existentes. Para un producto nuevo, elige la estructura de despliegue más sencilla que cumpla los requisitos; separa servicios solo ante una necesidad demostrada.
2. Añade las reglas del proyecto y comandos de compilación/pruebas fáciles de encontrar, tomados del perfil seleccionado. No inventes controles ni te limites a nombrar controles inexistentes.
3. Implementa un primer flujo completo con su punto de entrada real, reglas de aplicación, persistencia, autenticación/autorización cuando corresponda y una UI/API utilizable.
4. Aplica los límites entre tenants en lecturas/escrituras y en los trabajos, cachés o archivos que utilice ese flujo.
5. Añade pruebas unitarias/de integración significativas, infraestructura sintética y limpieza basada en la propiedad de los recursos. Añade controles de arquitectura/dependencias con un alcance explícitamente delimitado.
6. Prepara un entorno de aceptación aislado y representativo; ejercita los casos de éxito, denegación, otro tenant y los reintentos/fallos pertinentes.
7. Documenta la preparación, los contratos, la operación, la evidencia y los siguientes hitos. Incluye facturación, clientes nativos y asistentes solo si se solicitan.

## Entregar
Perfil y decisiones, flujo implementado, archivos modificados, verificaciones realmente ejecutadas, evidencia de aceptación sin datos sensibles, resultado de la limpieza e hitos pendientes. Distingue la base entregada de un producto completo en producción. La publicación y el despliegue siguen la autorización del usuario.
