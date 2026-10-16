# Preparación y uso reproducible

Esta guía prepara el paquete para leer sus instrucciones o ejecutar sus controles. No genera un SaaS ni instala herramientas en una aplicación existente.

## Obtener una copia

Con Git instalado, desde una carpeta de trabajo elegida:

```sh
git clone https://github.com/rody8708/saas-professional-builder.git
cd saas-professional-builder
git rev-parse HEAD
```

Registra el commit que vas a usar. Para repetir una validación anterior, selecciona su revisión con Git antes de ejecutar las pruebas; las versiones y resultados deben corresponder a esa revisión. Una rama propuesta en un pull request puede contener cambios que todavía no estén en `main`.

Para leer el paquete basta un editor de texto. Empieza por [SKILL.md](../SKILL.md), elige el perfil técnico y carga solo las referencias necesarias para la tarea.

## Usarlo con un agente

Puedes proporcionar el archivo `SKILL.md` junto con la carpeta del paquete como contexto y pedir una revisión, planificación o implementación concreta. Los enlaces relativos necesitan que estén disponibles también `core/`, `profiles/`, `prompts/`, `templates/` y `docs/`; copiar únicamente `SKILL.md` deja referencias incompletas.

En Codex con la instalación de skills disponible, puedes solicitar:

> Instala la skill del repositorio rody8708/saas-professional-builder. Está en la raíz del repositorio y su nombre es saas-professional-builder. Usa la revisión que acabamos de revisar y conserva cualquier instalación existente hasta comparar los cambios.

Comprueba después que la skill aparece disponible y comienza una nueva petición con `$saas-professional-builder`. El repositorio no instala ni activa la skill por ejecutar sus tests. Para otros agentes, sigue el mecanismo de skills/contexto que admita el producto; los requisitos y controles pueden usarse manualmente.

Adapta las plantillas al destino después de leer sus instrucciones. Si ya existen `AGENTS.md`, `RULES.md` o controles, integra las decisiones necesarias sin sobrescribirlos. Un perfil pendiente no autoriza sustituir el stack del proyecto.

## Herramientas para ejecutar las pruebas

Las herramientas se instalan con la distribución y el procedimiento apropiados para tu sistema. Este paquete no altera instalaciones globales. Necesitas solo las correspondientes a los perfiles que quieras probar.

| Alcance | Herramientas | Versiones elegidas en el CI del paquete |
|---|---|---|
| Catálogo y validadores Python | Python 3.10 o posterior | Python 3.13.6 |
| Node/TypeScript | Node.js | Node 24.16.0 |
| PHP | PHP con las extensiones de [su guía](../profiles/php/PROFILE.md) y Composer 2.9 o posterior | PHP 8.2 en Linux, PHP 8.5 en Windows; Composer 2.9.5 |
| .NET | SDK y runtime .NET 8, PowerShell 7 | SDK 8.0.413; PowerShell del runner |

Los resultados observados y las versiones efectivamente ejecutadas están en [validation.md](validation.md). El CI usa parches disponibles de las líneas PHP indicadas y registra su versión; no afirma probar todas las combinaciones posibles. .NET necesita SDK 8 aunque tengas instalado SDK 9 o 10; su `global.json` puede seleccionar un SDK 8 más reciente ya instalado y el CI registra esa selección efectiva.

## Ejecutar los controles

Desde la raíz del paquete:

```sh
python -B scripts/validate_package.py
python -B tests/test_package_validation.py
node --test profiles/node-typescript/tests/architecture-guard.test.mjs
python -B -m unittest discover -s profiles/python/tests -p "test_*.py" -v
python -B -m unittest discover -s profiles/php/tests -p "test_runner.py" -v
python -B profiles/php/tools/run-tests.py
pwsh -NoProfile -File profiles/dotnet/tools/Invoke-Profile.ps1 -Mode Test
```

Ejecuta cada comando y comprueba su código de salida: cero indica éxito para ese control. No consideres aprobada la lista si falla un comando y otro posterior termina bien. El último chequeo de limpieza es:

```sh
python -B scripts/validate_package.py
git status --short --ignored
```

En una copia sin cambios propios, el estado Git debe estar vacío. Los propios runners verifican además la eliminación de sus recursos temporales fuera del repositorio.

### Dependencias PHP aisladas

El [runner PHP](../profiles/php/tools/run-tests.py) prepara su propio entorno temporal con [composer.json](../profiles/php/tools/composer.json) y [composer.lock](../profiles/php/tools/composer.lock). No necesita `vendor` de Zendrhax ni de otro producto. Conserva PHPUnit 11.5.55, la versión de la evidencia inicial, y consulta los avisos de seguridad vigentes antes de instalar dependencias fijadas.

Cada ejecución necesita red para consultar avisos y descargar las dependencias, ya que la caché también es temporal. No se desactivan los bloqueos de seguridad ni se instala un plugin o script de Composer. Si el audit falla, corrige y revisa las dependencias; no ignores el aviso para obtener un resultado verde.

Si Composer no está en PATH, pasa su ejecutable o archivo PHAR:

```sh
python -B profiles/php/tools/run-tests.py --composer /ruta/a/composer.phar
```

La [guía PHP](../profiles/php/PROFILE.md) explica opciones, pruebas y límites. El runner elimina dependencias, cachés y configuración temporal al terminar; no deja un `vendor/` reutilizable en el paquete.

## CI y evidencia

[Package CI](../.github/workflows/package-ci.yml) ejecuta las suites en `ubuntu-24.04` y `windows-2025` para pull requests dirigidos a `main`, pushes a `main` y ejecución manual cuando el workflow esté disponible en la rama predeterminada. Las acciones están fijadas por SHA, el token solo tiene lectura de contenidos y no se utilizan secretos de aplicaciones.

Consulta el resultado de cada ejecución en [GitHub Actions](https://github.com/rody8708/saas-professional-builder/actions/workflows/package-ci.yml). El workflow valida este paquete. Las pruebas de autorización, aislamiento, pagos, base de datos y operación del SaaS destino requieren su propio CI y aceptación funcional.

Una rama `main` bloqueada en solo lectura no acepta merges, aunque los checks pasen. La revisión, el desbloqueo y el merge siguen siendo decisiones del propietario; las pruebas no cambian esa protección.
