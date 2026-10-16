# Perfil PHP

Este perfil conserva los controles ejecutables de SaaS Enterprise Builder. PHP es una opción entre los perfiles del catálogo; no es el stack implícito del núcleo.

## Stack y fronteras

Usa la versión de PHP y el framework acordados para el producto. En un proyecto Laravel/Symfony existente, conserva su contenedor, rutas, autenticación y herramientas nativas; no lo conviertas en un sistema vanilla. Entidades y casos de uso de dominio mantienen contratos explícitos, y el driver/ORM queda en infraestructura. El ORM no sustituye filtros de tenant, permisos ni constraints.

Las plantillas de guard usan como ejemplo `app/Application`, `app/Presentation/Controllers` y `modules/<slug>/Application`. Adapta esas rutas y el namespace a la estructura real. El test falla si falta una raíz requerida o está vacía; no desactives esa protección para ocultar una integración incompleta.

## Plantillas incluidas

| Archivo | Integración |
|---|---|
| [ArchitectureBoundaryGuardTest.template.php](templates/ArchitectureBoundaryGuardTest.template.php) | Copiar al árbol PHPUnit del proyecto, adaptar namespace, rutas y hosts de proveedor |
| [check-coverage.template.php](templates/check-coverage.template.php) | Copiar a `tools/check-coverage.php`; requiere DOM; umbral acordado por proyecto |
| [composer.scripts.template.json](templates/composer.scripts.template.json) | Fusionar `scripts`, sin reemplazar dependencias ni autoload existentes |
| [ci.template.yml](templates/ci.template.yml) | Workflow de ejemplo para un destino PHP/MySQL; configurar versiones y adaptar/eliminar el job de ese motor si se usa otro |

La plantilla CI es un ejemplo para la aplicación destino; el workflow del propio paquete es independiente. Genera cobertura antes de comprobar el umbral. El destino necesita `composer.json`, lockfile, PHPUnit/PHPStan configurados, código y pruebas propios. Las dependencias de las regresiones de este paquete se declaran por separado en [tools/composer.json](tools/composer.json) y [tools/composer.lock](tools/composer.lock).

## Integración de herramientas

Define suites Unit e Integration, bootstrap exclusivo de pruebas y fuentes de cobertura reales con archivos no ejecutados incluidos. El ejemplo tiene una suite MySQL separada con grupo `mysql`, puerto de servicio dinámico y fallo ante tests omitidos/vacíos; si el motor es otro, configura y verifica su gate real. Los tests nunca cargan archivos de configuración ni bases de datos reales. El primer job excluye el grupo de motor dedicado.

Configura PHPStan para los paths/nivel acordados; complementa el guard sintáctico con resolución de tipos, dependencias y pruebas de aislamiento. Usa Composer lock y auditoría de dependencias. Activa PCOV/Xdebug para generar Clover y ejecuta el checker sobre un informe nuevo. `80` en el fragmento es un umbral de ejemplo, no una garantía de calidad.

La publicación requiere los [gates del catálogo](../README.md#mismo-estándar-pruebas-del-proyecto) descritos en el núcleo: permisos, integridad, aislamiento, idempotencia, flujos reales y operación. La aplicación concreta debe probarlos; los tests de estas plantillas solo validan sus controles.

## Regresiones del perfil

Requisitos preinstalados: Python 3.10+, PHP 8.2+ con DOM, JSON, libxml, mbstring, Phar, tokenizer, XML y XMLWriter, y Composer **2.9.8 o posterior**. La versión validada actualmente es **2.10.3**. Composer 2.9.5 queda solo como evidencia histórica: está afectado por [GHSA-f9f8-rm49-7jv2](https://github.com/composer/composer/security/advisories/GHSA-f9f8-rm49-7jv2), corregido en 2.9.8. Se necesita acceso de red a Packagist y a los archivos de distribución de sus dependencias. No hace falta instalar PHPUnit globalmente ni tener otro proyecto.

Desde la raíz del repositorio, tanto en Windows como en Linux:

```text
python -B profiles/php/tools/run-tests.py
python -B -m unittest discover -s profiles/php/tests -p test_runner.py
```

En sistemas donde Python 3 se llama `python3`, sustituye `python` en ambos comandos. Para seleccionar instalaciones concretas:

```text
python -B profiles/php/tools/run-tests.py --php /ruta/a/php --composer /ruta/a/composer.phar
```

El primer comando copia los manifiestos a un directorio temporal propio, valida el lock, ejecuta `composer audit --locked`, instala las 27 dependencias bloqueadas con plugins y scripts deshabilitados y comprueba los requisitos de la plataforma real. El lock conserva PHPUnit **11.5.55** y resuelve para PHP **8.2.0**; esa plataforma simulada no sustituye la comprobación del PHP real. No se ignoran avisos: una auditoría fallida detiene el proceso antes de instalar.

Después ejecuta las 24 regresiones del guard con `--no-configuration`, su propio autoloader y sin caché de resultados; ejecuta las 12 pruebas del lector de informes Clover con `PHP_BINARY` explícito. Esas 12 pruebas usan XML sintético: no generan cobertura ni miden la cobertura de una aplicación. Los tests no necesitan red ni base de datos; la preparación y auditoría de dependencias sí necesitan red.

El runner aísla `COMPOSER_HOME`, caché, manifiesto, autenticación y temporales; descarta overrides heredados de Composer y del guard. No modifica configuración global, no abre archivos `.env` y no usa el `vendor` de otra aplicación. Mantiene PATH, certificados y proxy del sistema. Composer se ejecuta siempre con el PHP elegido, tanto su PHAR como un script PHP Unix sin extensión. El wrapper oficial de Windows se resuelve a su PHAR; wrappers de shell arbitrarios se rechazan. No se invoca un shell.

Cada comando dispone de 900 segundos. Ante timeout o interrupción, el runner termina el árbol de procesos antes de esperar y limpiar: `taskkill /T /F` en Windows y una sesión propia con `killpg` en POSIX. Al terminar, incluso tras fallo o timeout, elimina y verifica el área propia de dependencias, caché y fixtures. Propaga el primer código de fallo (124 para timeout); una limpieza fallida también impide éxito.

El segundo comando verifica ese aislamiento, la detención en cada etapa, la propagación de fallos y la limpieza con 12 tests; no descarga dependencias. Incluye procesos sintéticos reales: un hijo conserva el directorio de trabajo e intenta escribir después del timeout. La regresión exige que el árbol termine, la limpieza finalice antes del retorno y esa escritura nunca ocurra. Estos 12 tests pasan en Windows y en Ubuntu WSL.

La ejecución real nueva en Windows pasó con PHP 8.5.1, Python 3.13.6, Composer **2.10.3** y PHPUnit 11.5.55: 24 tests del guard (455 aserciones) y 12 del lector, auditoría sin avisos y limpieza verificada. Se descargó el PHAR desde [la distribución oficial de Composer](https://getcomposer.org/download/), se cotejó su SHA-256 con la página y el archivo oficial de checksums, y se ejecutó mediante `--composer` desde un temporal propio; no se modificó Composer global. El checksum verificado fue `7a2d379d5b8ffdaa028580ef26494c36d2feef4b178d3dd1473a4dbc5e17c8d6`. El mismo lock funcionó sin cambios.

La ejecución anterior con Composer 2.9.5 también aprobó 24 tests del guard (455 aserciones) y 12 del lector; ese resultado histórico no valida la seguridad del ejecutable Composer. `composer audit --locked` audita las dependencias del lock, no al propio Composer cuando se ejecuta como PHAR externo. El número de aserciones del caso sin marcador depende de la profundidad del temporal, porque comprueba cada ascenso hasta la raíz; no representa un porcentaje de cobertura. El historial y la evidencia de otros entornos están en [validación](../../docs/validation.md).

Para actualizar dependencias, genera y revisa un lock nuevo dentro de un temporal aislado, audítalo sin exclusiones y repite estas pruebas. No uses `composer update` en el árbol del perfil ni desactives auditorías para conseguir una ejecución verde. Si aparece un advisory nuevo, la reproducción debe fallar hasta resolverlo; un resultado histórico no certifica la seguridad futura.

## Límites

El guard reconoce llamadas SQL directas, locators literales, hosts cURL literales, declaraciones de strict types y longitud de controladores. No resuelve todos los tipos, aliases, llamadas dinámicas ni HTTP indirecto. Un method-name match también puede señalar métodos no SQL con el mismo nombre. Encoding, paridad de catálogos, configuración de módulos y unit isolation necesitan sus propios checks cuando apliquen. La revisión rechaza aumento de allowlists; el guard detecta entradas obsoletas/duplicadas.

El comprobador de informes de cobertura rechaza archivos ausentes o inválidos, métricas vacías y porcentajes insuficientes. La generación real del informe y el workflow de la aplicación deben probarse en el destino. Ningún resultado aquí certifica un SaaS.
