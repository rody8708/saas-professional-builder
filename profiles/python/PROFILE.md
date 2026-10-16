# Perfil Python

Estado: **controles del perfil validados**. Este perfil aporta un detector de dependencias basado en AST y pruebas de regresión aisladas. No aporta una aplicación SaaS, configuración del framework, autenticación, migraciones, integración con la base de datos de producción ni despliegue.

## Estructura y adaptación al framework

La política inicial supone un paquete en `src/example_saas`, con subpaquetes `domain`, `application`, `infrastructure` y `presentation`. Configura el nombre real del paquete y la raíz del código fuente antes de adoptarla. El dominio contiene entidades, objetos de valor y contratos de puertos; la aplicación coordina los casos de uso a través de esos puertos. Las implementaciones de persistencia, clientes de proveedores y adaptadores de tareas pertenecen a infraestructura; la integración HTTP/petición/respuesta pertenece a presentación. Un punto de composición conecta las dependencias concretas.

En FastAPI o Flask, los manejadores y la conversión de peticiones/esquemas del framework permanecen fuera de dominio y aplicación. Las sesiones y repositorios SQLAlchemy pertenecen a infraestructura; pasa a los casos de uso un puerto de transacciones definido por la aplicación. En Django, mantén modelos ORM, vistas, comandos de administración y señales del framework en adaptadores externos, con una conversión explícita a modelos de dominio. Este perfil no presupone que un modelo Django sea una entidad de dominio. Conserva el framework existente y configura las migraciones reales y la estrategia transaccional del proyecto; la estructura de paquetes no demuestra su corrección.

Fija las versiones de las dependencias del proyecto y usa un entorno local a él. Los scripts y las pruebas del perfil solo necesitan la biblioteca estándar de Python; no instalan frameworks ni paquetes.

## Controles ejecutables incluidos

- `templates/architecture_guard.py`: analiza código fuente Python con `ast` sin importar ni ejecutar módulos de la aplicación.
- `templates/architecture-policy.json`: paquete/raíz requeridos, políticas de dominio y aplicación, capas internas prohibidas y prefijos conocidos de importación de persistencia/transporte.
- `tests/test_architecture_guard.py`: regresiones con `unittest` y subprocesos en proyectos sintéticos temporales; se comprueba la limpieza de `TemporaryDirectory` después de cada ejecución. Sin acceso a red, bases de datos ni `.env`.

Ambos directorios de capas inspeccionadas deben existir y contener archivos `.py`. Se rechazan rutas de política inválidas, enlaces simbólicos de archivos fuente, inspecciones vacías, errores de codificación y errores de sintaxis. Se comprueban importaciones estáticas, importaciones `from`, importaciones relativas anidadas e importaciones de `__init__` de paquetes. Se inspeccionan llamadas literales conocidas a `__import__` e `importlib.import_module`, incluidos alias comunes de importación. Los destinos no literales y las importaciones dinámicas relativas mediante esos cargadores reconocidos se rechazan por no poder resolverse. Los comentarios y contenidos de cadenas de Python no se convierten en nodos de importación.

El detector excluye `__pycache__`, `.venv`, `venv`, `.git` y `vendor`. Los códigos de salida son `0` si pasan los controles configurados, `1` ante importaciones prohibidas o no resueltas y `2` si la inspección no puede completarse. Solo lee la política JSON y el código fuente; la configuración de despliegue no forma parte de este control.

## Reproducir la validación del perfil

Desde la raíz de este repositorio:

```sh
python -B -m unittest discover -s profiles/python/tests -p "test_*.py" -v
```

Validado en Windows con Python 3.13.6: **18 pruebas aprobadas, cero fallos u omisiones**. Las pruebas verifican códigos de salida positivos y negativos de subprocesos, raíces ausentes/vacías, políticas mal formadas, dependencias de persistencia/transporte entre capas, importaciones relativas desde módulos anidados y `__init__`, alias de cargadores, destinos dinámicos no resueltos, errores de sintaxis y tratamiento de comentarios/cadenas. `-B` evita artefactos de bytecode en el árbol fuente; se eliminan los proyectos sintéticos temporales.

Para adoptarlo, copia el control a `tools/`, copia y adapta la política en la raíz del proyecto y ejecuta:

```sh
python -B tools/architecture_guard.py --project-root . --config architecture-policy.json
```

El paquete y los directorios deben corresponder al proyecto real. No añadas archivos fuente vacíos únicamente para satisfacer una inspección no vacía.

## Comprobaciones complementarias y límites

Este control analiza sintaxis AST y dependencias directas configuradas; no impone la arquitectura del programa completo. No resuelve reasignaciones arbitrarias de funciones de carga, `getattr`/`eval`/`exec`, mecanismos personalizados de importación, dependencias indirectas a través de fachadas/reexportaciones, módulos generados ni modificaciones de objetos en ejecución. Los alias comunes de cargadores se identifican por su sintaxis; los nombres ocultados por otras declaraciones pueden requerir revisión. La lista de módulos externos prohibidos es finita. Las bibliotecas desconocidas, los envoltorios personalizados de persistencia y los límites de paquetes no configurados requieren revisión y actualización de la política. Las importaciones dentro de `TYPE_CHECKING` siguen siendo dependencias arquitectónicas y se inspeccionan.

Configura las herramientas reales del proyecto para análisis de estilo, tipos y límites de dependencias con su versión de Python, rutas fuente y frameworks compatibles. Ejecútalas sobre dependencias locales de versiones fijadas. El análisis sintáctico de este script no sustituye las pruebas de la aplicación, la comprobación de tipos, la verificación de compilación/empaquetado ni un grafo completo de dependencias. Este perfil no afirma haber ejecutado esas herramientas del proyecto.

## Requisitos de aceptación del proyecto

| Requisito | Evidencia exigida al SaaS que adopte el perfil |
| --- | --- |
| Arquitectura | Control AST configurado, comprobaciones reales de tipos/estilo/dependencias y revisión de contratos y adaptadores. |
| Aislamiento entre tenants | Casos negativos entre tenants por API/tareas/repositorios y comprobación del estado almacenado en el motor elegido para producción. |
| Autorización | Operaciones sin autenticación o prohibidas, revocación de membresía, propiedad de recursos y pruebas del flujo de autenticación. |
| Integridad de datos | Migraciones reales, estrategia de reversión, restricciones, gestión de transacciones y pruebas de concurrencia. |
| Reintentos seguros | Webhooks/tareas/envíos duplicados, idempotencia, fallos parciales y reintentos seguros sin duplicar efectos. |
| Entrada real | Repetición real del flujo por navegador/HTTPS/worker, salida observable y estado persistido, datos sintéticos y sandbox del proveedor de pagos. |
| Operación | Validación de configuración, recuperación del planificador, entrega de alertas, límites de secretos, restauración de copias y limpieza comprobada. |

El comportamiento de negocio se verifica en pruebas unitarias; los repositorios y las migraciones requieren pruebas de integración aisladas contra los motores compatibles; autenticación y pagos necesitan evidencia de sus proveedores y flujos negativos. Elige umbrales de cobertura, ejecutor de pruebas y formato de informe propios del proyecto. Este perfil no incluye un lector de cobertura ni afirma cobertura del producto. El CI del paquete prueba estos controles; cada proyecto debe integrar sus comprobaciones cuando existan sus configuraciones y dependencias, y declarar explícitamente las no ejecutadas. Añadir un workflow no demuestra que una ejecución remota haya pasado; consulta los resultados registrados en [docs/validation.md](../../docs/validation.md).
