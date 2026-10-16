# Perfil Node.js / TypeScript

Estado: **controles del perfil validados**. Este perfil aporta un detector de dependencias con alcance limitado y sus pruebas de regresión. No aporta una aplicación SaaS, autenticación, migraciones, un ORM, despliegue ni una arquitectura TypeScript certificada.

## Estructura y adaptación al framework

Usa `src/domain` para entidades, objetos de valor y puertos, y `src/application` para casos de uso y coordinación a través de esos puertos. Mantén los clientes SQL, SDK de pagos, colas y adaptadores de persistencia en `src/infrastructure`. Coloca los manejadores HTTP, tipos de petición del framework y serializadores en `src/presentation`. Conecta las dependencias concretas en un punto de composición fuera de las capas internas.

En Express o Fastify, los manejadores adaptan HTTP a los DTO de aplicación. En NestJS, mantén los decoradores del framework y la configuración de inyección de adaptadores fuera de los paquetes puros de dominio y aplicación. En Next.js, los manejadores de rutas y las acciones de servidor son adaptadores de entrada; un archivo exclusivo del servidor no queda autorizado ni aislado por tenant automáticamente. El código de interfaz JSX/TSX pertenece fuera de las dos raíces inspeccionadas. Conserva el framework del proyecto y fija sus versiones y las de sus paquetes; este perfil no instala ninguno.

## Controles ejecutables incluidos

- `templates/architecture-guard.mjs`: herramienta de línea de comandos basada en bibliotecas estándar; lee el código fuente sin ejecutar ni importar la aplicación.
- `templates/architecture-policy.json`: raíces explícitas, alias de importación, rutas internas prohibidas y paquetes de persistencia/transporte prohibidos para ambas capas internas. Adapta los alias a la resolución real de módulos del proyecto y revisa los cambios de política.
- `tests/architecture-guard.test.mjs`: pruebas mediante subprocesos sobre proyectos sintéticos temporales. No acceden a red, bases de datos, arranque de la aplicación ni `.env`. La limpieza elimina cada recurso de prueba propio en `finally`.

El detector exige que ambas raíces existan y contengan archivos fuente compatibles. Rechaza enlaces simbólicos de archivos fuente y rutas de política mal formadas. Inspecciona importaciones ES estáticas, importaciones y reexportaciones solo de tipos, importaciones con efectos secundarios, llamadas literales a `require`, `module.require`, `require.resolve` e importaciones dinámicas mediante `import`. Los cargadores reconocidos con destinos no literales se rechazan ante la imposibilidad de resolverlos. Las rutas relativas y los alias configurados explícitamente se comparan con las rutas prohibidas. Las claves de alias son prefijos sin `/` ni `*` al final (por ejemplo, `@domain`, no `@domain/*`). Las importaciones de rutas absolutas y URL se rechazan; los módulos integrados `node:` configurados se comprueban como paquetes. Los prefijos de paquete se comparan respetando los límites `/`. Se omiten comentarios, cadenas entre comillas, texto de plantillas y expresiones regulares literales ordinarias; se inspecciona el código dentro de interpolaciones de plantillas. JSX en las capas internas produce un error explícito de sintaxis no compatible.

El analizador léxico admite `.ts`, `.mts`, `.cts`, `.js`, `.mjs` y `.cjs`; excluye `node_modules`, `vendor`, `.git`, `dist` y `build`. Los códigos de salida son `0` si pasan los controles léxicos configurados, `1` ante una infracción de dependencias y `2` si la inspección no puede completarse. Un resultado cero no equivale a una comprobación de tipos ni a aceptación funcional en ejecución.

## Reproducir la validación del perfil

Desde la raíz de este repositorio, con Node.js 24 disponible:

```sh
node --test profiles/node-typescript/tests/architecture-guard.test.mjs
```

Validado en Windows con Node.js v24.16.0: **28 pruebas aprobadas, cero fallos u omisiones**. Las pruebas verifican importaciones permitidas y rechazos reales de la herramienta: raíces ausentes/vacías, importaciones prohibidas entre capas, alias, subrutas de paquetes, dependencias solo de tipos, cargadores dinámicos, nombres de módulo con escapes, comentarios/cadenas, interpolaciones de plantillas, políticas mal formadas y JSX no compatible. Todos los recursos temporales se eliminan después de cada prueba.

Para adoptarlo, copia los dos archivos de plantilla a `tools/` y a la ubicación de la política en la raíz del proyecto, adapta la política y ejecuta:

```sh
node tools/architecture-guard.mjs --project-root . --config architecture-policy.json
```

Las raíces inspeccionadas deben contener código fuente real. No debilites la política ni añadas archivos vacíos únicamente para que un proyecto nuevo pase los controles.

## Comprobaciones obligatorias de TypeScript y dependencias

Este analizador léxico no es un parser ni un resolvedor de TypeScript. La distinción entre expresiones regulares y división depende del contexto y es incompleta; los nombres locales que ocultan cargadores pueden producir falsos positivos. No resuelve alias ausentes de la política, `exports` de paquetes, dependencias transitivas, alias arbitrarios de cargadores, acceso calculado a módulos, `eval`, código generado ni infracciones arquitectónicas sin importaciones. La lista configurada de paquetes prohibidos es finita; un paquete desconocido no es seguro automáticamente. Estos límites deben quedar visibles en la evidencia del proyecto.

Cada proyecto TypeScript que lo adopte debe configurar y aprobar por separado el compilador y una regla de dependencias que resuelva los alias reales de `tsconfig` y los límites entre paquetes. Para una dependencia TypeScript de versión fijada e instalada localmente, el comando del compilador es:

```sh
node node_modules/typescript/bin/tsc --noEmit --project tsconfig.json
```

Este perfil no proporciona ni afirma haber ejecutado el `tsconfig`, la compilación del framework, la configuración de análisis de estilo ni las reglas de dependencias de ese proyecto. Un proyecto exclusivamente JavaScript también necesita análisis de estilo o dependencias que interprete la sintaxis y resuelva módulos. No sustituyas esas comprobaciones por el analizador léxico incluido.

## Requisitos de aceptación del proyecto

| Requisito | Evidencia exigida al SaaS que adopte el perfil |
| --- | --- |
| Arquitectura | Control configurado, compilación real y análisis de dependencias con resolución de módulos; revisión de límites entre puertos y adaptadores. |
| Aislamiento entre tenants | Pruebas negativas entre tenants por rutas/tareas y comprobaciones del estado persistido en el motor de base de datos elegido para producción. |
| Autorización | Acciones denegadas, cambios/revocación de membresía, propiedad de recursos y pruebas de entradas autenticadas. |
| Integridad de datos | Migraciones reales, reversión o irreversibilidad documentada, restricciones, límites transaccionales y escrituras concurrentes. |
| Reintentos seguros | Envíos/webhooks duplicados, claves de idempotencia, fallos de dependencias y carreras de reintentos sin duplicar efectos. |
| Entrada real | Repetición del flujo HTTP/navegador/worker en el entorno exigido, resultado comprobado y estado almacenado; sandbox del proveedor para pagos. |
| Operación | Configuración validada, aislamiento de secretos, recuperación de planificador/colas, alertas, restauración de copias y evidencia de limpieza. |

Usa pruebas unitarias para el comportamiento de negocio, pruebas de integración con datos sintéticos aislados y aceptación mediante entradas reales, por separado de estos controles. Los flujos de pagos/autenticación necesitan sus propios proveedores implementados, pruebas negativas y evidencia en sandbox. Define umbrales de cobertura para el proyecto y obtén cobertura con su ejecutor real de pruebas; este perfil no incluye un lector de informes ni un control de umbral de cobertura y no afirma cobertura del producto. El CI del paquete prueba estos controles; cada proyecto debe integrar sus comandos cuando existan las dependencias, la política y los demás requisitos, y registrar evidencia saneada de las comprobaciones no ejecutadas. Añadir un workflow no demuestra que una ejecución remota haya pasado; consulta los resultados registrados en [docs/validation.md](../../docs/validation.md).
