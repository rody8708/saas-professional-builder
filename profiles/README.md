# Selección y extensión de perfiles

Elige el stack según las decisiones del producto y su código existente. Este catálogo no tiene un perfil predeterminado.

| Perfil | Guía | Uso |
|---|---|---|
| `php` | [PHP](php/PROFILE.md) | Backend PHP, respetando su framework o perfil vanilla |
| `node-typescript` | [Node/TypeScript](node-typescript/PROFILE.md) | Servicios de backend en el runtime de Node con tipos cuando corresponda |
| `python` | [Python](python/PROFILE.md) | Backend Python con sus convenciones y framework elegidos |
| `dotnet` | [.NET](dotnet/PROFILE.md) | Backend C# con las herramientas y proyectos de .NET |

## Resolución del perfil

1. Conserva la tecnología elegida explícitamente por el usuario. Verifica versiones y compatibilidad en su entorno.
2. En un repositorio existente, inspecciona sus manifiestos y estructura sin ejecutar scripts ni abrir archivos de secretos. Un paquete de frontend no identifica por sí solo el backend.
3. Identifica qué servicio y carpeta se van a cambiar. En un sistema con varios lenguajes, asigna perfiles por servicio y documenta sus contratos de API/eventos; no homogeneices todo el sistema.
4. Si la elección sigue ambigua y cambia arquitectura, pregunta antes de generar código. Las tareas independientes de esa decisión pueden continuar.
5. Si no existe un perfil adecuado, usa el núcleo para diseñarlo; marca los controles no probados como pendientes. No recurras automáticamente al primer perfil de la lista.

## Contrato de un perfil

Cada directorio contiene `PROFILE.md`, `profile.json`, sus plantillas y sus pruebas. El registro [registry.json](registry.json) enlaza el manifiesto de cada perfil. Las rutas del manifiesto son relativas a su directorio y no pueden salir de él.

`profile.json` declara `id`, `name`, `languages`, `status`, `guide`, `templates`, `tests`, `implemented_controls`, `project_gates` y `validation` (entorno, comando reproducible, resultado y límites). Un perfil `controls-validated` debe aportar controles ejecutables, pruebas y resultados reales. Una guía nueva puede comenzar como `guidance-only`, sin afirmar ejecución.

Los comandos declarados son documentación para operadores. El validador del catálogo no los ejecuta automáticamente.

## Mismo estándar, pruebas del proyecto

Cada perfil debe conservar estas siete obligaciones del núcleo. Si una no aplica, el proyecto registra su motivo concreto; no se considera aprobada por omisión.

| Gate | Evidencia exigida al producto |
|---|---|
| `architecture` | Dependencias permitidas, reglas de dominio testeables y controles con alcance documentado |
| `tenant-isolation` | Dos tenants; lecturas, cambios, jobs, cachés, archivos y exports sin cruce de datos |
| `authorization` | Permisos por operación, denegaciones y revocación; contexto de identidad actual |
| `data-integrity` | Invariantes, transacciones, constraints, concurrencia y migraciones en el motor real aislado |
| `retry-safety` | Duplicados, respuesta perdida, fallo parcial, idempotencia y recuperación sin repetir efectos |
| `real-entrypoint` | Flujo afectado por navegador/API/job/cliente real, resultado observable y estado persistido |
| `operations` | Configuración segura, observabilidad, restauración/rollback y limpieza con responsables |

Un detector sintáctico de imports solo aporta parte de `architecture`. No demuestra los otros gates ni sustituye un análisis con resolución de símbolos. Los checks de frontend, accesibilidad, idiomas y privacidad definidos por el producto se registran además de estos mínimos.

## Añadir o cambiar un perfil

Documenta las herramientas elegidas y cómo usar las bibliotecas del framework sin duplicarlas. Añade controles útiles con fixtures sintéticos, casos permitidos y prohibidos, errores de configuración, rutas ausentes/vacías y cleanup comprobado. Verifica comandos contra el runtime objetivo; registra versiones y límites. Ejecuta `python scripts/validate_package.py` desde la raíz y las regresiones del perfil. Revisa que el núcleo y los prompts sigan libres de dependencias de ese lenguaje.
