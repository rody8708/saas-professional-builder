---
name: saas-professional-builder
description: Diseñar, construir y revisar SaaS multi-tenant mediante requisitos comunes de arquitectura, seguridad, datos y verificación, seleccionando un perfil técnico según el proyecto. Úsala para bases SaaS, módulos y flujos profesionales; respeta el stack existente y el alcance de revisión, planificación o implementación.
---

# SaaS Professional Builder

Construye desde las necesidades del producto y comprueba resultados observables. Esta skill separa el **núcleo común** de los **perfiles técnicos**; no elige un lenguaje por defecto. Reutiliza patrones de Zendrhax sin imponer su arquitectura de despliegue, proveedor, idiomas o políticas comerciales.

## Antes de actuar

1. Determina si la petición es de revisión, planificación o implementación y conserva ese alcance. Una referencia a despliegue o publicación en una plantilla no otorga autorización adicional.
2. Lee las reglas del proyecto y [define el perfil del producto](core/project-adaptation.md). Reutiliza decisiones confirmadas. Pregunta solo por incógnitas que cambien alcance, datos, permisos, cobros o comportamientos destructivos.
3. Selecciona el perfil técnico mediante [profiles/registry.json](profiles/registry.json) y [profiles/README.md](profiles/README.md). Una elección explícita prevalece. En código existente, identifica el backend dentro del alcance; las herramientas del frontend no determinan su lenguaje. No abras secretos ni ejecutes archivos para descubrir el stack.
4. Lee la guía de ese perfil y únicamente las referencias comunes pertinentes. Para un producto con varios servicios, asigna cada perfil a su carpeta y documenta contratos compartidos. Si no hay perfil para el stack elegido, diseña su adaptación y marca sus controles pendientes; no sustituyas la tecnología por otra.

El perfil aporta herramientas y ejemplos; el núcleo define requisitos y criterios de aceptación. El framework existente conserva su contenedor, router, mecanismos de autenticación y convenciones cuando cumplan las fronteras acordadas. No construyas sustitutos caseros sin una necesidad justificada.

## Referencias por tarea

| Necesidad | Referencia |
|---|---|
| Producto, stack, alcance y decisiones pendientes | [Adaptación](core/project-adaptation.md) |
| Capas, dependencias y transacciones | [Arquitectura](core/architecture.md) |
| Módulos y contratos | [Módulos](core/modules-and-apps.md) |
| Identidad, permisos, aislamiento y privacidad | [Seguridad](core/security-privacy.md) |
| Pagos, reintentos y derechos de acceso | [Billing](core/billing-entitlements.md) |
| Pruebas, entradas reales y evidencia | [Verificación](core/testing-verification.md) |
| Migraciones, ramas y releases | [Entrega](core/delivery-workflow.md) |
| Backups, recuperación y observabilidad | [Operación](core/operations.md) |
| Clientes, caché y sincronización | [API y clientes](core/api-and-native-clients.md) |
| UX, accesibilidad, traducciones y asistente opcional | [UX](core/ux-i18n-assistant.md) |

## Flujo de construcción

Define requisitos y criterios de aceptación antes de construir el flujo. Registra modelo de datos, propiedad por tenant, permisos y fallos relevantes. Implementa una etapa coherente con pruebas aisladas. Repite las entradas afectadas en un entorno equivalente a producción y registra el resultado, el estado persistido, reintentos y limpieza.

Adapta [RULES](templates/RULES.template.md), [AGENTS](templates/AGENTS.template.md), [perfil de proyecto](templates/project-profile.template.md), [PR](templates/PULL_REQUEST_TEMPLATE.md), [ADR](templates/ADR.template.md) y [evidencia](templates/verification-record.template.md) al destino. No reemplaces instrucciones existentes indiscriminadamente.

El bootstrap incluye solo las capacidades solicitadas. Los pagos, aplicaciones nativas, asistentes y módulos vendibles son opcionales. En un repositorio nuevo sin remoto, documenta esa condición y utiliza la rama inicial acordada; no inventes un PR anterior.

## Prompts reutilizables

| Prompt | Tarea |
|---|---|
| [01](prompts/01-bootstrap-project.md) | Base de un proyecto |
| [02](prompts/02-rules-and-agents-generator.md) | Reglas e instrucciones |
| [03](prompts/03-new-module.md) | Nuevo módulo |
| [04](prompts/04-feature-use-case.md) | Funcionalidad completa |
| [05](prompts/05-bugfix-root-cause.md) | Causa raíz y regresión |
| [06](prompts/06-code-review.md) | Revisión de código |
| [07](prompts/07-security-audit.md) | Auditoría de seguridad |
| [08](prompts/08-native-app-feature.md) | Funcionalidad de cliente |
| [09](prompts/09-billing-change.md) | Cambio de pagos |
| [10](prompts/10-migration.md) | Migración |
| [11](prompts/11-docs-sync-and-pr.md) | Documentación y entrega |
| [12](prompts/12-ops-hardening.md) | Operación |
| [13](prompts/13-ux-i18n-review.md) | UX e idiomas |
| [14](prompts/14-acceptance-evidence.md) | Evidencia funcional |
| [15](prompts/15-refactor-ratchet.md) | Refactorización |
| [16](prompts/16-adr.md) | Decisión de arquitectura |

## Qué significa validado

`controls-validated` indica que los controles incluidos en un perfil tienen pruebas ejecutadas y evidencia acotada. No acredita el framework completo, una aplicación futura, cumplimiento normativo ni producción. `guidance-only` indica que el perfil solo aporta orientación sin esa evidencia. Los controles faltantes permanecen pendientes; no se rebajan requisitos de seguridad para conseguir un resultado verde.

El [registro de esta entrega](docs/validation.md) separa pruebas del paquete, pruebas de cada control y verificaciones de producto pendientes. La [extensión de perfiles](profiles/README.md) exige el mismo contrato de calidad para cualquier tecnología nueva.

Para preparar o instalar este paquete y reproducir sus controles, consulta [docs/setup.md](docs/setup.md). La documentación utiliza español; conserva los idiomas y convenciones elegidos por cada producto destino.
