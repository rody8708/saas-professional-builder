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
| Instalación PHP desde cero con manifiesto y lock propios | Windows, PHP 8.5.1, Composer 2.10.3, PHPUnit 11.5.55 | 27 dependencias fijadas; auditoría sin avisos; 24 tests/455 aserciones y 12 tests del lector Clover; PASS |
| Aislamiento y fallos del runner PHP | Python 3.13.6, Windows | 12 tests; fallos de comandos, timeout real con proceso hijo, selección de PHP, configuración heredada y limpieza; PASS |
| Catálogo y regresiones | Python 3.13.6, Windows | Validador PASS y 23 tests aprobados |
| Guard Node/TypeScript | Node 24.16.0, Windows | 28 tests; PASS |
| Guard Python | Python 3.13.6, Windows | 18 tests; PASS |
| Guard .NET/C# | SDK 8.0.413, PowerShell 7.6.5, Windows | 48 escenarios; sin warnings/errors; limpieza verificada; PASS |
| Workflow del paquete | actionlint 1.7.12 | Sin errores; binario temporal con checksum verificado y eliminado |

El nuevo runner PHP instala las herramientas en un directorio temporal, sin usar dependencias de otra aplicación. Ejecuta `validate --strict`, `audit --locked` y `check-platform-reqs`; no desactiva avisos ni ejecuta plugins/scripts de Composer. Conserva PHPUnit 11.5.55 y resuelve el lock para PHP 8.2.0. El número de aserciones del guard depende también de la profundidad del temporal en un caso que busca el manifiesto en directorios ascendentes; no es una métrica de cobertura.

La revisión independiente reprodujo dos defectos del runner antes de su publicación: un timeout podía dejar un hijo vivo e impedir la limpieza en Windows, y Composer Unix podía usar el PHP de PATH en lugar del seleccionado. Se corrigieron la terminación del árbol de procesos y la invocación explícita de PHP. La regresión real verifica salida 124, limpieza antes del retorno y ausencia de la escritura tardía del hijo; otra ejecución real comprueba la propagación de salida 19. Los scripts PHP de Composer y los wrappers incompatibles tienen casos específicos.

La primera ejecución remota señaló que Composer 2.9.5 estaba afectado por [GHSA-f9f8-rm49-7jv2](https://github.com/composer/composer/security/advisories/GHSA-f9f8-rm49-7jv2). La acción deshabilitó su autenticación como mitigación. Se actualizó el CI a Composer 2.10.3 y el requisito documentado a 2.9.8 o posterior; la auditoría del lock no comprueba vulnerabilidades del ejecutable Composer instalado.

La repetición local con Composer 2.10.3 usó un PHAR temporal descargado del proveedor y contrastado con su SHA-256 publicado (`7a2d379d5b8ffdaa028580ef26494c36d2feef4b178d3dd1473a4dbc5e17c8d6`). La instalación global no se modificó y el PHAR temporal también se eliminó.

En [la primera ejecución de CI](https://github.com/rody8708/saas-professional-builder/actions/runs/38958840568), Ubuntu aprobó las suites y Windows detectó un fallo en la fixture que simulaba un directorio reparse. El mock comparaba una ruta sin normalizar con la ruta canónica utilizada por el validador. Se reprodujo el fallo con un alias sintético `normalization-hop/..` antes del arreglo y se corrigió únicamente la prueba; el caso ahora comprueba ambas representaciones y sigue fallando si el validador enumera el directorio rechazado. El control del paquete no se debilitó ni se omitió la prueba.

## CI remoto ejecutado

[Package CI, ejecución 38959450626](https://github.com/rody8708/saas-professional-builder/actions/runs/38959450626), commit `2d0978dac410b1b9beff3038aefde97a1fea55bc`, terminó con ambos jobs aprobados el 2026-10-16. Cada entorno instaló las dependencias PHP desde cero y aprobó la auditoría del lock y las comprobaciones finales de limpieza.

| Suite o control | Windows Server 2025 | Ubuntu 24.04 |
|---|---|---|
| Validador del paquete | PASS | PASS |
| Regresiones del validador | 23 tests; PASS | 23 tests; PASS |
| Guard Node/TypeScript | 28 tests; PASS | 28 tests; PASS |
| Guard Python | 18 tests; PASS | 18 tests; PASS |
| Ejecutor PHP: aislamiento y fallos | 12 tests; PASS | 12 tests; PASS |
| Guard PHP | 24 tests/455 aserciones; PASS | 24 tests/451 aserciones; PASS |
| Lector Clover | 12 tests; PASS | 12 tests; PASS |
| Guard .NET/C# | 48 escenarios; PASS | 48 escenarios; PASS |

Son 165 tests/escenarios por entorno, sin contar el validador general como test adicional. Las dos compilaciones .NET terminaron sin advertencias ni errores. Los checks finales comprobaron que el checkout no contenía cambios, archivos ignorados ni archivos no versionados.

Versiones observadas en ambos jobs: Python 3.13.6, Node 24.16.0, Composer 2.10.3, PHPUnit 11.5.55, SDK .NET 8.0.425 y PowerShell 7.6.6. PHP fue 8.5.11 en Windows y 8.2.34 en Ubuntu. El workflow instala SDK 8.0.413; `global.json` seleccionó 8.0.425, ya presente y compatible con su política de avance. No se confunden estas versiones remotas con las de la evidencia local anterior.

El registro corresponde al commit enlazado. Los cambios posteriores tienen su ejecución independiente en los [checks del PR](https://github.com/rody8708/saas-professional-builder/pull/1/checks); una ejecución anterior no acredita automáticamente otra revisión. El workflow configura salida Python UTF-8 para conservar también los mensajes en español en Windows.

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
- El CI remoto ejecutado corresponde al paquete. No se han ejecutado CI de una aplicación, despliegue, workflows de negocio, autenticación, cobros sandbox, pruebas de navegador ni restauración de un SaaS: este paquete no implementa esas capacidades.
- Los perfiles no proporcionan parsers de cobertura universales; cada proyecto debe configurar su runner, medición y umbrales reales.
- El chequeo de enlaces verifica destinos de archivos locales; no comprueba anchors Markdown ni disponibilidad de sitios web.
- Un perfil con `controls-validated` acredita únicamente la ejecución de los controles enumerados. El proyecto debe cumplir sus siete requisitos de aceptación con evidencia funcional independiente.

Registrar una herramienta, un checklist o un comando no equivale a haberlo ejecutado. Todo caso pendiente debe conservar ese estado hasta contar con evidencia.
