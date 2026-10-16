# Perfil .NET / C#

Este perfil aporta un control ejecutable de arquitectura sobre código fuente y pruebas de regresión aisladas. Es un punto de partida para una arquitectura ASP.NET Core acordada, no una aplicación SaaS, una implementación de autenticación, una certificación de cumplimiento ni evidencia de que el proyecto destino apruebe sus requisitos.

Lee primero las reglas comunes del producto. Conserva el framework, la base de datos, los idiomas, el ciclo de vida de cuentas y las decisiones arquitectónicas existentes del destino. La configuración de ejemplo usa proyectos separados `Domain` y `Application`; adapta sus rutas y los nombres de espacios de nombres/proyectos prohibidos antes de adoptarla. Una aplicación existente con un solo proyecto necesita un control adaptado o una brecha documentada, no una reescritura automática de su arquitectura.

## Herramientas y entorno compatibles

- El control incluido se compila y ejecuta con **SDK/runtime .NET 8** y PowerShell 7 para el script de ejecución. [global.json](global.json) selecciona la banda de características más reciente instalada de .NET 8, igual o posterior a 8.0.100. Si solo hay SDK 9/10 en la máquina, también debe instalarse SDK 8 para reproducir este perfil tal como se entrega.
- Roslyn procede del directorio `Roslyn/bincore` del SDK seleccionado. No hay dependencias de paquetes NuGet. [NuGet.Offline.Config](tools/NuGet.Offline.Config) vacía las fuentes de paquetes únicamente para este control; no se cambia configuración de usuario ni global.
- El SaaS destino puede usar otra versión compatible de .NET. Su compilación real, analizadores y pruebas deben usar el SDK elegido. El analizador sintáctico del control admite la sintaxis C# que entiende Roslyn del SDK 8 seleccionado; no certifica características más recientes del lenguaje.
- El ejecutor de regresiones del paquete es un programa independiente, por lo que `dotnet test` no lo ejecutaría. Usa los comandos siguientes. Las pruebas de la aplicación deben usar un framework seleccionado explícitamente, como xUnit, NUnit o MSTest, y su adaptador real de pruebas; registra las versiones elegidas y ejecuta el comando `dotnet test` del destino.

## Ejecutar las pruebas de regresión incluidas

Desde `profiles/dotnet`:

```powershell
pwsh -NoProfile -File ./tools/Invoke-Profile.ps1 -Mode Test
```

El script compila [el control](tools/ArchitectureGuard/ArchitectureGuard.csproj) y [el ejecutable de regresiones](tests/ArchitectureGuard.Regression.csproj), y después ejecuta este último. La salida de compilación, los metadatos de restauración de dependencias, la caché de paquetes y el directorio de usuario de la CLI se colocan en un directorio temporal propio del sistema. La reutilización de servidores de compilación está desactivada. El script restaura las variables de entorno de su proceso, comprueba el destino de limpieza y elimina ese directorio temporal en `finally`.

Cada escenario crea archivos sintéticos `.cs`, `.csproj` y JSON en un directorio temporal distinto y lo elimina en `finally`. No se arranca ninguna aplicación, no se carga ningún `.env` ni base de datos real, y no se contacta con proveedores ni servicios de red. Los escenarios de CLI invocan la entrada real del control y comprueban su código de salida.

## Aplicar el control a un proyecto

1. Copia [architecture-guard.example.json](templates/architecture-guard.example.json) a la raíz del repositorio destino como `architecture-guard.json`.
2. Define las dos raíces de código fuente con los directorios reales de los proyectos Domain/Application. Cada una requiere código C# con declaraciones o instrucciones y al menos un `.csproj`. Sustituye `Example.*` por prefijos reales de espacios de nombres y revisa los fragmentos de nombres de proyectos prohibidos y las bibliotecas de persistencia. Una lista vacía de prohibiciones se rechaza. Los cambios de configuración deben revisarse junto con el código; este control no impide que alguien debilite deliberadamente su configuración.
3. Ejecuta el control desde el directorio del perfil, indicando una ruta absoluta al destino:

```powershell
pwsh -NoProfile -File ./tools/Invoke-Profile.ps1 -Mode Check -ProjectRoot '/absolute/path/to/target-repository'
```

En Windows, pasa una ruta entre comillas como `D:\Projects\Example`. El control solo lee la configuración y el código fuente C#/de proyectos; no compila ni ejecuta la aplicación destino. Devuelve **0** si no hay hallazgos, **1** ante hallazgos de arquitectura/configuración y **2** ante uso inválido de la CLI o un fallo de entrada/salida durante la inspección. Un fallo de compilación o de requisitos previos del script también produce una salida distinta de cero.

En el CI del proyecto destino, instala o selecciona el SDK .NET 8 y PowerShell 7 requeridos y ejecuta el mismo comando del script. Guarda en el repositorio la configuración revisada del destino y conserva el código de salida del comando. El CI del paquete prueba estos controles; cada proyecto debe integrar su propio workflow y configurar las comprobaciones obligatorias de rama. Las versiones de las acciones de terceros y el aprovisionamiento de ejecutores corresponden a la política de entrega del destino. Añadir un workflow no demuestra que una ejecución remota haya pasado.

## Qué comprueba el control incluido

- Se rechazan configuraciones ausentes/mal formadas, raíces de código fuente ausentes, ausencia de archivos C#, archivos vacíos o que solo contienen comentarios, y ausencia de archivos de proyecto en las capas. Se rechazan código fuente fuera del repositorio declarado y rutas de código/proyectos que sean enlaces.
- Roslyn analiza nombres y expresiones de miembros del código fuente. Los prefijos de espacios de nombres configurados se rechazan en importaciones de Domain/Application, referencias a tipos, expresiones calificadas, alias de espacios de nombres, alias globales y contextos relevantes de los espacios de nombres que los contienen. Los comentarios y contenidos de cadenas no se consideran dependencias de código; las expresiones dentro de cadenas interpoladas se inspeccionan.
- Las relaciones literales `ProjectReference` se inspeccionan transitivamente. Los fragmentos prohibidos de nombres de proyectos y las identidades de ensamblado/espacio de nombres raíz producen hallazgos. Los identificadores literales `PackageReference`, `FrameworkReference` y `Reference` de ensamblados se comparan con las reglas de prefijos de espacios de nombres.
- Se rechazan referencias a proyectos ausentes, identificadores dinámicos/con comodines, XML de proyecto mal formado y DTD de XML. Las condiciones de los proyectos se inspeccionan de forma conservadora, independientemente de que una compilación concreta las active.
- Se excluyen los directorios `bin`, `obj` y `.git`. Los errores de sintaxis y el código condicional inactivo son hallazgos explícitos; no se aceptan silenciosamente.

La implementación está en [ArchitectureScanner.cs](tools/ArchitectureGuard/ArchitectureScanner.cs); las [regresiones](tests/Program.cs) cubren casos permitidos y prohibidos, comportamiento de la CLI y limpieza.

## Límites del control

Se trata de **inspección de sintaxis y referencias literales entre proyectos**, no de un analizador semántico Roslyn ni de un grafo de dependencias MSBuild evaluado. La ambigüedad entre espacios de nombres y tipos puede producir hallazgos que requieran revisión. No resuelve reflexión, despacho dinámico, registro de servicios en ejecución, código generado, dependencias introducidas por `.props`/`.targets` importados, paquetes NuGet transitivos ni directivas `using` globales declaradas fuera de las raíces de capas configuradas. Sigue siendo necesario compilar y analizar la arquitectura con resolución de tipos, además de revisar el código. Una salida cero solo demuestra los controles configurados sobre el código inspeccionado.

El control informa deliberadamente del código de preprocesador inactivo como no resuelto; no puede certificar todas las configuraciones de símbolos/compilación. Los proyectos con implementaciones condicionales necesitan un control adicional que considere la compilación antes de tratar esa cobertura arquitectónica como completa. No suprimas el hallazgo para después afirmar que el código omitido fue comprobado.

No inspecciona la pertenencia de recursos a tenants, autorización, transacciones, reintentos, corrección SQL, seguridad de autenticación ni políticas legales. La matriz siguiente sigue siendo verificación obligatoria del proyecto; enumerar un requisito no lo implementa.

## Guía de implementación ASP.NET Core

Usa los mecanismos reales de rutas, inyección de dependencias, configuración, registro y autorización de ASP.NET Core. Los endpoints/controladores de ASP.NET y los `DbContext`, mapeos y migraciones de EF Core pertenecen a proyectos externos API/Infrastructure/Persistence. Application coordina los casos de uso mediante los puertos acordados; Domain permanece independiente del transporte y la persistencia. El control incluido permite EF Core fuera de Domain/Application. Evita cargar un tenant implícito en un singleton o en un campo estático mutable.

Usa componentes de identidad mantenidos o el proveedor de identidad elegido; por ejemplo, ASP.NET Core Identity y middleware consolidado de OpenID Connect/OAuth. No inventes funciones de hash de contraseñas, formatos de tokens, gestión de sesiones ni criptografía. Define por ruta la autenticación mediante cookies/CSRF o exclusivamente Bearer, valida las llamadas de retorno del proveedor y prueba el ciclo de vida real de cuentas. Una biblioteca de identidad no sustituye la autorización de negocio ni las comprobaciones de membresía del tenant.

Usa el motor de base de datos de producción para pruebas de integración de transacciones, restricciones, migraciones y concurrencia. El proveedor en memoria de EF Core o SQLite no demuestra el comportamiento de bloqueos/DDL de otro motor. Los filtros de consulta pueden añadir defensa, pero no bastan como autorización: valida membresía y propiedad de recursos, cubre SQL directo y mecanismos que omitan filtros, y aplica claves/restricciones apropiadas en la base de datos. Usa bases de datos/contenedores temporales aislados con identidades sintéticas y limpieza comprobada.

## Requisitos obligatorios del proyecto destino

| Requisito | Evidencia exigida | Aporte de este perfil |
|---|---|---|
| `architecture` | Compilación/analizadores y límites de dependencias acordados sobre el código y las configuraciones reales de compilación | Solo el control acotado de sintaxis/referencias literales y sus regresiones |
| `tenant-isolation` | Lecturas/escrituras negativas con dos tenants, exportaciones/tareas, membresía obsoleta, cambios de caché/contexto y restricciones de base de datos | Guía; requiere pruebas del destino |
| `authorization` | Decisiones de recursos/capacidades en el límite del caso de uso, operaciones denegadas y modos reales de autenticación/CSRF por ruta | Guía; requiere pruebas del destino |
| `data-integrity` | Migraciones en el motor real, reversión/recuperación, transacciones, concurrencia optimista o de filas y fallos de restricciones | Guía; requiere pruebas del destino |
| `retry-safety` | Identidad durable de operación, contenido/clave estables, entrega duplicada, resultados desconocidos y comportamiento de outbox/conciliación cuando sea necesario | Guía; requiere pruebas del destino |
| `real-entrypoint` | Flujo real HTTPS/API/worker con entradas sintéticas; verificar respuesta, estado persistido y resultados relevantes de fallos/reintentos | Guía; requiere evidencia funcional del destino |
| `operations` | Validación de configuración de producción, telemetría segura, preparación para servicio, planificador/workers, restauración de copias y objetivos de recuperación | Guía; requiere evidencia operativa del destino |

Para pagos, conserva una operación durable y su clave de idempotencia cuando se desconozca el resultado del proveedor; las políticas de reintentos, como las de fallos transitorios HTTP/EF, no deben duplicar efectos secundarios silenciosamente. Usa un adaptador de proveedor y prueba los flujos de sandbox/conciliación en el destino. Para la operación, elimina datos sensibles de la telemetría, propaga la cancelación cuando corresponda y verifica la recuperación en lugar de deducirla de un endpoint saludable.

## Registro de validación

El manifiesto registra la ejecución local real y sus límites en [profile.json](profile.json). `controls-validated` describe únicamente estos controles; no aprueba un SaaS destino. Los resultados históricos no acreditan ejecuciones posteriores de GitHub CI o Linux: consulta la evidencia de cada entorno en [docs/validation.md](../../docs/validation.md). Los flujos de la aplicación y del dominio siempre requieren evidencia propia.
