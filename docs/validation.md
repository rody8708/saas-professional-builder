# Evidencia de validación del paquete

Fecha: 2026-10-16. Alcance: instrucciones, catálogo, plantillas y controles del paquete independiente. Las pruebas no arrancan Zendrhax ni una aplicación SaaS, no acceden a bases operativas ni utilizan credenciales de proveedores.

## Evidencia inicial de la copia independiente

| Componente | Entorno | Resultado |
|---|---|---|
| Guard PHP reubicado | Windows, PHP 8.5.1, PHPUnit 11.5.55 | 24 tests, 453 assertions; PASS |
| Guard PHP reubicado | Ubuntu WSL, PHP 8.2.34, PHPUnit 11.5.55 | 24 tests, 449 assertions; PASS |
| Parser/umbral Clover PHP | Python 3.13.6 + PHP 8.5.1, Windows | 12 tests; PASS |
| Parser/umbral Clover PHP | Python 3.12.3 + PHP 8.2.34, Ubuntu WSL | 12 tests; PASS |
| Catálogo y límites del validador | Python 3.13.6, Windows | 23 tests; PASS |
| Guard Node/TypeScript | Node.js 24.16.0, Windows | 28 tests, 0 fallos/omitidos; PASS |
| Guard Python | Python 3.13.6, Windows | 18 tests, 0 fallos/omitidos; PASS |
| Guard .NET/C# | SDK 8.0.413, PowerShell 7.6.5, Windows | 48 escenarios, 0 fallos; build sin warnings/errors; PASS |

Las suites se ejecutaron desde esta copia por sus comandos documentados. .NET incluye cinco escenarios por el CLI real; Node y Python comprueban códigos de salida con procesos separados. La evidencia detallada de cada perfil se conserva en su `profile.json` y guía. Estos recuentos no son porcentajes de cobertura.

## Preparación reproducible y CI del paquete

La mejora de distribución añade MIT, documentación común en español, una guía de preparación y el workflow [Package CI](../.github/workflows/package-ci.yml). La licencia no cambia los permisos del repositorio ni desbloquea `main`.

Validación local del cambio, 2026-10-16:

| Componente | Entorno | Resultado |
|---|---|---|
| Instalación PHP desde cero con manifiesto y lock propios | Windows, PHP 8.5.1, Composer 2.9.5, PHPUnit 11.5.55 | 27 dependencias fijadas; auditoría sin avisos; 24 tests/455 aserciones y 12 tests del lector Clover; PASS |
| Aislamiento y fallos del runner PHP | Python 3.13.6, Windows | 12 tests; fallos de comandos, timeout real con proceso hijo, selección de PHP, configuración heredada y limpieza; PASS |
| Catálogo y regresiones | Python 3.13.6, Windows | Validador PASS y 23 tests aprobados |
| Guard Node/TypeScript | Node 24.16.0, Windows | 28 tests; PASS |
| Guard Python | Python 3.13.6, Windows | 18 tests; PASS |
| Guard .NET/C# | SDK 8.0.413, PowerShell 7.6.5, Windows | 48 escenarios; sin warnings/errors; limpieza verificada; PASS |
| Workflow del paquete | actionlint 1.7.12 | Sin errores; binario temporal con checksum verificado y eliminado |

El nuevo runner PHP instala las herramientas en un directorio temporal, sin usar dependencias de otra aplicación. Ejecuta `validate --strict`, `audit --locked` y `check-platform-reqs`; no desactiva avisos ni ejecuta plugins/scripts de Composer. Conserva PHPUnit 11.5.55 y resuelve el lock para PHP 8.2.0. El número de aserciones del guard depende también de la profundidad del temporal en un caso que busca el manifiesto en directorios ascendentes; no es una métrica de cobertura.

La revisión independiente reprodujo dos defectos del runner antes de su publicación: un timeout podía dejar un hijo vivo e impedir la limpieza en Windows, y Composer Unix podía usar el PHP de PATH en lugar del seleccionado. Se corrigieron la terminación del árbol de procesos y la invocación explícita de PHP. La regresión real verifica salida 124, limpieza antes del retorno y ausencia de la escritura tardía del hijo; otra ejecución real comprueba la propagación de salida 19. Los scripts PHP de Composer y los wrappers incompatibles tienen casos específicos.

La ejecución remota del workflow permanece pendiente hasta tener una ejecución de GitHub Actions aprobada. La validación sintáctica y las pruebas locales no sustituyen esa evidencia.

## Reproducción

Los comandos del [README](../README.md#verificar-este-paquete), la [guía de preparación](setup.md) y las guías de [PHP](../profiles/php/PROFILE.md), [Node/TypeScript](../profiles/node-typescript/PROFILE.md), [Python](../profiles/python/PROFILE.md) y [.NET](../profiles/dotnet/PROFILE.md) son los puntos de entrada reales de estas pruebas. El validador del catálogo solo lee los comandos declarados; no los ejecuta.

PHPUnit se ejecutó con `--no-configuration`, el autoloader de dependencias y `--do-not-cache-result`. No se cargó el bootstrap del producto ni configuración de entorno. Los reportes Clover son fixtures XML sintéticos: prueban el parser y sus límites, no una medición de cobertura del SaaS. La diferencia de assertions entre runtimes proviene del harness; no indica una cobertura porcentual.

## Datos y limpieza

Las pruebas generan únicamente fixtures propios bajo directorios temporales. Deben eliminarse incluso ante fallos. Los runners no importan ni ejecutan el código de las aplicaciones analizadas. Los controles solo inspeccionan fuentes, políticas y manifiestos.

El wrapper .NET mantiene build, restore, caché y CLI home fuera del repositorio y comprueba su eliminación. Python se ejecuta con `-B` para evitar bytecode en el paquete. La revisión de publicación incluye archivos ignorados y residuos, además del diff de Git.

## Revisión independiente de uso

Se evaluaron las instrucciones por lectura y simulación de decisiones; no se construyeron aplicaciones para estos casos.

| Escenario | Resultado de la revisión |
|---|---|
| Revisar Laravel con frontend React e idiomas fr/en | Perfil PHP; solo lectura; framework e idiomas conservados |
| Planificar Python/PostgreSQL sin remoto ni pagos | Perfil Python; planificación; ausencia de remoto explícita y pagos no aplicables |
| Cambiar backend .NET con frontend Node y otros servicios | Perfil por servicio/carpeta; frontend no determina backend |
| Proyecto Go sin perfil registrado | Conservar Go; adaptación pendiente, sin fallback a PHP |
| Guard verde, flujo de negocio sin ejecutar | Evidencia del guard acotada; aceptación funcional pendiente |

La revisión también detectó omisiones del escaneo en extensiones de texto y `.env.example`, además de una excepción con URLs Markdown malformadas. Se corrigieron con regresiones. El catálogo comprueba tipos inválidos sin abortar y rechaza enlaces/reparse points antes de enumerarlos. La comprobación de atributos de reparse y de no recorrido usa mocks sintéticos; no se creó una junction real como prueba de integración.

En .NET se reprodujo una omisión al componer namespaces anidados: la regresión añadida falló antes del arreglo (42 escenarios, un fallo esperado). Se corrigió la composición de scopes y se ampliaron casos permitidos/prohibidos; la suite final pasó 48 escenarios, incluido el caso por el CLI real, con limpieza verificada.

## Límites y pendientes del producto

- Los guards de arquitectura tienen alcance limitado; no son prueba de corrección de negocio ni un análisis completo de símbolos y dependencias.
- No se ha generado Clover mediante PCOV/Xdebug. Solo se ha validado el lector de reportes sintéticos.
- No se han ejecutado CI remoto, despliegue, workflows de negocio, autenticación, cobros sandbox, pruebas de navegador ni restauración de una aplicación: este paquete no implementa esas capacidades.
- Los perfiles no proporcionan parsers de cobertura universales; cada proyecto debe configurar su runner, medición y umbrales reales.
- El chequeo de enlaces verifica destinos de archivos locales; no comprueba anchors Markdown ni disponibilidad de sitios web.
- Un perfil con `controls-validated` acredita únicamente la ejecución de los controles enumerados. El proyecto debe cumplir sus siete requisitos de aceptación con evidencia funcional independiente.

Registrar una herramienta, un checklist o un comando no equivale a haberlo ejecutado. Todo caso pendiente debe conservar ese estado hasta contar con evidencia.
