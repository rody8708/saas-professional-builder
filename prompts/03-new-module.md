# 03 · Añadir un módulo coherente

## Solicitud
Implementa {{capacidad, flujos, actores, datos y criterios de aceptación}}.

## Diseñar
Lee las reglas y el perfil del proyecto y la [guía de módulos](../core/modules-and-apps.md). Define los responsables del módulo, sus contratos públicos, dependencias, ciclo de vida de los datos, permisos y puntos de entrada. Elige entre un módulo interno y un despliegue separado según los requisitos reales; la comercialización por módulos es opcional.

Usa las convenciones nativas del framework. Diseña el esquema y las relaciones seguras entre tenants, los límites transaccionales, la idempotencia, las categorías de fallo y las entregas duraderas necesarias. Los demás módulos acceden a los datos del módulo mediante contratos declarados.

## Implementar y verificar
- Revalida permisos y pertenencia al tenant en las operaciones; prueba lecturas, escrituras, agregados y los trabajos/cachés/archivos pertinentes entre tenants.
- Implementa migraciones, ejemplos de configuración sin secretos, preparación y recuperación.
- Si se almacenan datos personales, implementa la política de exportación/supresión/retención seleccionada.
- Si se aplica facturación, resuelve derechos de acceso y cuotas en el backend; no inventes planes.
- Construye la UI/API y los trabajos necesarios con los estados diseñados y los idiomas/accesibilidad acordados.
- Prueba las invariantes de negocio, los adaptadores sobre el motor de producción soportado, la concurrencia y los casos de duplicados/reintentos cuando sean pertinentes.
- Ejercita los flujos principales mediante sus puntos de entrada reales en un laboratorio aislado y representativo; inspecciona estado y efectos.
- Elimina los recursos de prueba propios y verifica su ausencia.

## Entregar
Contratos del módulo, flujos implementados, modelo de datos/permisos, pruebas y evidencia, documentación para operación/desarrollo y brechas explícitas. Un módulo no está completo por el mero hecho de que funcione su primer caso de éxito.
