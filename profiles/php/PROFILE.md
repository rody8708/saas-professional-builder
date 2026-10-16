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

La plantilla CI no está activa en este repositorio. Genera cobertura antes de comprobar el umbral. El destino necesita `composer.json`, lockfile, PHPUnit/PHPStan configurados, código y pruebas propios; el paquete no incluye esas dependencias.

## Integración de herramientas

Define suites Unit e Integration, bootstrap exclusivo de pruebas y fuentes de cobertura reales con archivos no ejecutados incluidos. El ejemplo tiene una suite MySQL separada con grupo `mysql`, puerto de servicio dinámico y fallo ante tests omitidos/vacíos; si el motor es otro, configura y verifica su gate real. Los tests nunca cargan archivos de configuración ni bases de datos reales. El primer job excluye el grupo de motor dedicado.

Configura PHPStan para los paths/nivel acordados; complementa el guard sintáctico con resolución de tipos, dependencias y pruebas de aislamiento. Usa Composer lock y auditoría de dependencias. Activa PCOV/Xdebug para generar Clover y ejecuta el checker sobre un informe nuevo. `80` en el fragmento es un umbral de ejemplo, no una garantía de calidad.

La publicación requiere los [gates del catálogo](../README.md#mismo-estándar-pruebas-del-proyecto) descritos en el núcleo: permisos, integridad, aislamiento, idempotencia, flujos reales y operación. La aplicación concreta debe probarlos; los tests de estas plantillas solo validan sus controles.

## Regresiones del perfil

Desde la raíz del repositorio, con PHPUnit 11 instalado y su autoloader (sin configuración/bootstrap de otra aplicación):

```text
php /absolute/path/to/vendor/phpunit/phpunit/phpunit --no-configuration --bootstrap /absolute/path/to/vendor/autoload.php --do-not-cache-result profiles/php/tests/ArchitectureTemplateRegressionTest.php
python profiles/php/tests/test_coverage_cli.py
```

El segundo comando usa `php` en PATH o `PHP_BINARY`. Ambos crean archivos sintéticos temporales y comprueban su limpieza. No usan red ni base de datos. El entorno y los resultados de esta copia están en [validation](../../docs/validation.md).

## Límites

El guard reconoce llamadas SQL directas, locators literales, hosts cURL literales, declaraciones de strict types y longitud de controladores. No resuelve todos los tipos, aliases, llamadas dinámicas ni HTTP indirecto. Un method-name match también puede señalar métodos no SQL con el mismo nombre. Encoding, paridad de catálogos, configuración de módulos y unit isolation necesitan sus propios checks cuando apliquen. La revisión rechaza aumento de allowlists; el guard detecta entradas obsoletas/duplicadas.

El checker de cobertura rechaza informes ausentes o inválidos, métricas vacías y porcentajes insuficientes. La generación real del informe y el workflow remoto deben probarse en el destino. Ningún resultado aquí certifica un SaaS.
