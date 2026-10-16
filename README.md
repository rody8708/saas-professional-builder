# SaaS Professional Builder

Una base reutilizable para **diseñar, construir y revisar SaaS profesionales sin imponer PHP ni otro lenguaje**. Combina instrucciones para agentes, requisitos comunes, prompts de trabajo, plantillas de documentación y controles técnicos con pruebas.

El paquete ayuda a organizar una construcción con evidencia. No contiene una aplicación SaaS terminada ni genera automáticamente autenticación, cobros, paneles o despliegues. Cada producto necesita su implementación y aceptación funcional.

## Núcleo común y perfiles técnicos

El núcleo define los resultados exigidos: aislamiento entre tenants, autorización, integridad, reintentos seguros, pruebas por entradas reales y recuperación operativa. Cada perfil explica cómo adaptar esas exigencias a una tecnología y aporta controles de alcance concreto.

| Perfil | Control incluido | Regresiones del control |
|---|---|---|
| [PHP](profiles/php/PROFILE.md) | Fronteras de arquitectura y lector de umbral Clover | 24 de arquitectura y 12 del parser/umbral con XML sintético; Windows y WSL |
| [Node.js / TypeScript](profiles/node-typescript/PROFILE.md) | Imports y rutas prohibidas, con análisis léxico y política explícita | 28 tests; Node sin paquetes externos |
| [Python](profiles/python/PROFILE.md) | Imports estáticos y loaders conocidos mediante AST | 18 tests; biblioteca estándar |
| [.NET / C#](profiles/dotnet/PROFILE.md) | Sintaxis C# y referencias literales entre proyectos, con Roslyn del SDK | 48 escenarios; sin paquetes NuGet externos |

Consulta los resultados, versiones y límites en [docs/validation.md](docs/validation.md). `controls-validated` significa que **esos controles** tienen pruebas ejecutadas; no certifica la aplicación, un framework entero, seguridad absoluta ni preparación para producción. Las reglas sintácticas no sustituyen compilación, resolución de dependencias o tests de comportamiento.

## Cómo usarlo

1. Abre [SKILL.md](SKILL.md) como punto de entrada. Indica si necesitas revisión, planificación o implementación.
2. Describe producto, stack elegido o existente, base de datos, usuarios/tenants y capacidades solicitadas. Completa el [perfil del proyecto](templates/project-profile.template.md) con decisiones confirmadas y pendientes.
3. Selecciona el [perfil técnico](profiles/README.md) correspondiente. Una decisión explícita prevalece; si el backend ya existe, se conserva su tecnología y framework. Un `package.json` del frontend no convierte el backend en Node.
4. Lee los documentos pertinentes de [core/](core/) y usa un prompt de [prompts/](prompts/). Adapta las plantillas a las reglas del destino; no reemplaces archivos existentes sin revisar su contenido.
5. Implementa por etapas y registra pruebas, fallos, estado persistido, limpieza y brechas pendientes con la [plantilla de evidencia](templates/verification-record.template.md).

Ejemplo para un proyecto nuevo:

> Usa SaaS Professional Builder para planificar un SaaS de gestión de equipos. Backend Python, PostgreSQL y frontend web. Primero define requisitos, modelo de tenants, permisos, arquitectura y criterios de aceptación. No implementes todavía ni agregues cobros.

Ejemplo para una funcionalidad existente:

> Usa esta skill para implementar invitaciones de miembros en nuestro backend .NET. Lee primero las reglas del repositorio. Conserva el framework y la base de datos existentes; prueba permisos, cruce de tenants, expiración, duplicados y el flujo real, con datos sintéticos.

No hace falta instalar todos los runtimes para usar la documentación. Los comandos de cada perfil requieren únicamente las herramientas que su guía especifica. Este repositorio no instala ni activa la skill en tu entorno automáticamente.

La [guía de preparación](docs/setup.md) explica cómo obtener una revisión, usar la skill y ejecutar los controles desde cero con dependencias aisladas. El español es el idioma de la documentación y las plantillas; los identificadores de código, comandos y el texto legal original de MIT conservan su forma original.

## Qué cambia respecto al paquete original

- Las reglas y prompts comunes describen comportamientos y evidencia; las herramientas de cada lenguaje viven en su perfil.
- PHP sigue disponible como una opción, junto con Node/TypeScript, Python y .NET.
- No hay lenguaje predeterminado. En sistemas con varios servicios, cada servicio conserva su perfil y sus contratos.
- Un stack adicional, por ejemplo Go, puede incorporar otro perfil con el mismo contrato. Hasta validar sus controles, se identifica como `guidance-only`; no se cambia automáticamente a PHP.
- Los patrones procedentes de Zendrhax se adaptan al producto: no se heredan por defecto su proveedor, sistema operativo, idiomas, política comercial ni estructura de despliegue.

La [procedencia](docs/provenance.md) identifica la versión de origen. Esta entrega es una copia independiente.

## Estándar de construcción

Cada funcionalidad define criterios observables antes de implementarse. Los [siete requisitos de aceptación](profiles/README.md#mismo-estándar-pruebas-del-proyecto) exigen evidencia de arquitectura, aislamiento, permisos, integridad, reintentos, entrada real y operación. Los checks de privacidad, accesibilidad, traducción y producto se agregan según su alcance.

Los tests usan recursos aislados y datos sintéticos. Para acreditar transacciones, locks y migraciones se usa el motor real soportado. La aceptación comprueba el resultado visible, el estado persistido y los fallos relevantes; una suite verde o un endpoint de salud no reemplazan ese flujo. Los cobros se verifican en sandbox cuando existan; no se añaden como capacidad obligatoria.

Una brecha no ejecutada permanece pendiente. Los umbrales de cobertura, herramientas y entornos se definen para el proyecto; ningún porcentaje por sí solo demuestra que un SaaS está listo.

## Contenido

```text
SKILL.md                 Entrada y selección de referencias
core/                    10 documentos comunes
profiles/                Catálogo, 4 perfiles, controles y pruebas
prompts/                 16 tareas reutilizables
templates/               6 plantillas comunes de documentación
scripts/                 Validador del paquete y catálogo
tests/                   Regresiones del validador
docs/                    Procedencia, evidencia y límites
LICENSE                  Licencia MIT
.github/workflows/       CI del paquete en Windows y Linux
```

## Verificar este paquete

Desde la raíz, con Python 3.10 o posterior:

```sh
python -B scripts/validate_package.py
python -B tests/test_package_validation.py
```

El validador revisa estructura, rutas del catálogo, evidencias declaradas, requisitos comunes, archivos operativos y enlaces locales a archivos. No ejecuta comandos contenidos en manifiestos, no prueba enlaces web ni valida el comportamiento de una aplicación. El escaneo de credenciales reconoce formatos conocidos y requiere revisión humana adicional antes de publicar.

Para los controles de cada perfil:

```sh
node --test profiles/node-typescript/tests/architecture-guard.test.mjs
python -B -m unittest discover -s profiles/python/tests -p "test_*.py" -v
python -B -m unittest discover -s profiles/php/tests -p "test_runner.py" -v
python -B profiles/php/tools/run-tests.py
pwsh -NoProfile -File profiles/dotnet/tools/Invoke-Profile.ps1 -Mode Test
```

PHP necesita PHP y Composer instalados. Su runner instala las dependencias fijadas en un directorio temporal propio; no usa el autoloader de otra aplicación. Los comandos y requisitos completos están en [su guía](profiles/php/PROFILE.md). El wrapper .NET requiere SDK 8 y PowerShell 7. Ambos eliminan sus artefactos temporales.

[Package CI](.github/workflows/package-ci.yml) ejecuta las suites del paquete en Windows y Linux para cambios propuestos a `main`; sus [resultados](https://github.com/rody8708/saas-professional-builder/actions/workflows/package-ci.yml) se registran por revisión. La plantilla de CI del perfil PHP sigue destinada al SaaS que la adopte y requiere adaptación. Cada aplicación integra sus propios checks funcionales.

## Licencia

Este paquete se distribuye bajo [MIT](LICENSE), elegida por su propietario. Permite uso, modificación y distribución, incluidos usos comerciales, conservando el aviso de autoría y la licencia. Las dependencias mantienen sus propias licencias. La licencia no concede permisos de escritura sobre este repositorio ni modifica la protección de `main`.

## Extender con responsabilidad

Sigue [el contrato de perfiles](profiles/README.md). Añade casos permitidos, prohibidos, rutas/configuración inválidas y cleanup verificable. Documenta límites y resultados con versiones reproducibles. Un nuevo perfil conserva los siete requisitos comunes, aunque sus herramientas sean distintas.

No publiques secretos, archivos `.env` operativos, bases de datos, logs, backups, dependencias instaladas ni datos de clientes. Las plantillas deben contener solo ejemplos sintéticos y placeholders. Revisa lista y diff de archivos antes de cualquier publicación, incluso en repositorios privados.
