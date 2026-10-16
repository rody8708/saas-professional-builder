# 11 · Sincronizar la documentación y preparar la revisión

## Solicitud
Prepara {{cambio}} para revisión/publicación dentro de la autorización del usuario.

## Documentación
A partir del diff final, identifica cambios en comportamiento, preparación, arquitectura, API, módulos, privacidad, pruebas, operación y flujos de usuario. Actualiza la documentación responsable en los idiomas acordados del proyecto. Describe el comportamiento implementado; identifica las propuestas y los controles pendientes.

Usa [verification-record.template.md](../templates/verification-record.template.md) para la evidencia funcional significativa. Incluye revisión/entorno, comandos realmente ejecutados, recuentos reales, resultados de aceptación y brechas explícitas. Explica cuándo la documentación no resulta afectada.

## Higiene
Inspecciona la lista exacta de archivos y el diff completo preparado antes de crear commits o hacer push. Ejecuta los controles de secretos/datos privados del proyecto; confirma que se excluyan configuración operativa, datos de clientes, registros, bases de datos y copias de seguridad. Verifica la limpieza de los recursos propios de prueba, incluidos los ignorados/externos.

Valida el repositorio previsto, su visibilidad, la rama base y la coherencia del alcance antes de publicar. Conserva el trabajo ajeno al alcance y sigue la política de ramas del proyecto. Si la publicación ya está autorizada, complétala una vez preparado el trabajo concreto revisable y superadas las comprobaciones; no añadas una solicitud de aprobación redundante.

## Descripción para revisión
Usa [PULL_REQUEST_TEMPLATE.md](../templates/PULL_REQUEST_TEMPLATE.md): problema y comportamiento resultante, alcance, verificación, migración/compatibilidad, despliegue/recuperación, impacto en privacidad/seguridad y brechas relevantes. Marca casillas solo con evidencia; no hagas una afirmación universal de preparación para producción.

## Entregar
Resumen de documentación/higiene y descripción final para revisión. Comunica el resultado de la publicación solo si ocurrió realmente; de lo contrario, indica el artefacto preparado y cualquier requisito obligatorio aún pendiente.
