# Módulos, ownership y capacidades

Un módulo representa una capacidad coherente con datos y reglas propios. Puede ser interno a un producto; no necesita ser una aplicación vendible ni un servicio desplegable. Define los límites antes de separar repositorios o bases de datos.

## Contrato mínimo proporcional

Documenta propósito, propietario, entradas públicas, dependencias permitidas, datos que posee, permisos, configuración y criterios de aceptación. Cuando el módulo exponga API, eventos o tareas, publica contratos versionados o una política de compatibilidad. Nombres de carpetas, registro y descubrimiento pertenecen al perfil técnico.

- Cada dato tiene un propietario que controla sus migraciones y su ciclo de vida. Los módulos acceden a otros mediante contratos declarados; no escriben en tablas ajenas por comodidad.
- Una base de datos compartida puede ser válida. Documenta fronteras de transacción, permisos y consultas conjuntas autorizadas; bases separadas requieren recuperación y consistencia entre fronteras.
- El registro dinámico, si existe, falla cerrado: instalar archivos no debe activar rutas o conceder capacidades por sí solo.
- La configuración requerida tiene un ejemplo sanitizado y validación. No se heredan silenciosamente credenciales o secretos de otro módulo.
- Los datos personales del módulo participan en exportación, supresión y retención según la política del producto.
- Un módulo deshabilitado deja de aceptar operaciones nuevas donde corresponda, pero no abandona pagos, trabajos o entregas pendientes que requieran reconciliación.

## Aislamiento y autorización

Define capacidades por operación, incluidas las compuestas. La autorización se revalida en el punto de ejecución y no depende de que la interfaz haya ocultado un botón. El tenant efectivo proviene de la identidad y membresía vigentes, no de un identificador confiado del cliente.

El aislamiento incluye lecturas, escrituras, búsquedas, agregados, exportaciones, jobs, cachés, archivos, adjuntos y eventos. Las claves y rutas de almacenamiento llevan el alcance correcto; los enlaces de descarga verifican acceso o tienen capacidad limitada y expiración. Jobs y consumidores transportan contexto explícito y vuelven a comprobar los requisitos aplicables.

Prueba dos tenants con identificadores de recurso similares, pertenencias cambiadas y tareas retrasadas. Comprueba tanto denegación directa como ausencia de filtración en conteos, resultados, cachés y archivos.

## Capacidades comerciales opcionales

Si hay módulos vendibles, define por separado permiso, entitlement y cuota; ninguno sustituye a los demás. Planes, bundles, activación y límites se resuelven en servidor desde un catálogo. El copy refleja ese catálogo y los idiomas acordados.

El setup posterior a una compra puede usar pasos declarados por código, sondas de solo lectura y destinos permitidos. No permitas que contenido configurable convierta sondas, rutas o URLs en ejecución arbitraria. Un estado desconocido no se presenta como completado.

## Criterios de módulo listo

- Contratos y ownership definidos; migraciones y recuperación ensayadas.
- Permisos y aislamiento verificados en entradas y almacenamiento.
- Invariantes del negocio, concurrencia y reintentos probados.
- UI, API y jobs afectados ejercitados por sus entradas reales.
- Política de datos implementada y configuración documentada.
- Guía del módulo, operación, cambios y evidencia actualizados.
- Recursos temporales retirados; brechas y capacidades no implementadas explícitas.

Para una entrega por etapas, fija por etapa alcance, dependencias, datos, rutas, permisos y gates de activación. Un flujo de demostración no certifica el módulo completo.
