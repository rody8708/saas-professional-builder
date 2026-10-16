# Pruebas y aceptación verificable

Las herramientas se toman del perfil técnico; el alcance de la prueba se decide por el riesgo y el comportamiento cambiado. No confundir cobertura con corrección ni una suite con evidencia completa de producción.

## Niveles

| Nivel | Demuestra | Entorno |
|---|---|---|
| Unitario | Invariantes, decisiones y fallos de lógica aislada | Dobles controlados, sin servicios reales innecesarios |
| Integración/contrato | Persistencia, migraciones, adaptadores, protocolos y límites entre componentes | Infraestructura temporal y versiones soportadas |
| Aceptación | Flujo completo por su entrada real, resultado y estado durable | Laboratorio representativo de producción |

No sustituir el motor de producción por otro para acreditar locks, DDL o concurrencia. Si se prometen varios motores, probar los soportados. En integraciones externas usar sandbox; diferenciar ejecución real, simulación determinista y caso no ejecutado.

## Aislamiento y propiedad

Cada ejecución crea un identificador y un inventario de recursos propios: procesos, puertos, cuentas, schemas, archivos, volúmenes, colas, mail y artefactos. Usa identidades obviamente sintéticas como user-1@example.invalid.

La configuración de tests impide leer credenciales o bases operativas reales; crea configuración temporal explícita. No copies datos de clientes ni captures tráfico privado para fabricar fixtures.

El teardown corre ante éxito y fallo, elimina solo recursos cuya propiedad está demostrada y verifica su ausencia. Comprueba también archivos ignorados, recursos externos y procesos; un árbol Git limpio no basta. Los fallos de cleanup son fallos visibles de la ejecución.

## Matriz por cambio

| Cambio | Evidencia pertinente |
|---|---|
| Invariante o bug | Test que falla por el defecto antes y pasa después; casos límite |
| Persistencia/migración | Motor real aislado, restricciones, concurrencia y recuperación |
| Ruta/permiso | Autenticación adecuada, permiso, cross-tenant, entrada real y errores |
| UI/cliente | Navegador o cliente soportado; estados, accesibilidad y matriz visual |
| Job/cola | Launcher/consumidor real, lease, interrupción, retry y efectos |
| Cobro | Intención durable, pérdida de respuesta, firmas, duplicados y reconciliación en sandbox |
| Operación | Fallo controlado, alerta, restauración/recuperación medidos |
| Documentación | Enlaces, ejemplos, consistencia y declaración de alcance sin runtime |

Ejecuta tests enfocados y los checks obligatorios acordados; amplía solo por impacto o hallazgos. Cambios de bajo riesgo no necesitan pruebas que repitan literalmente la implementación. Umbrales de cobertura y análisis pertenecen al perfil del proyecto y deben medirse con herramientas reales.

## Correcciones

1. Define esperado, observado, causa sospechada y entradas afectadas.
2. Reproduce en recursos sintéticos o registra por qué no pudo reproducirse.
3. Ejecuta una regresión contra la versión defectuosa; verifica que falla por esa causa.
4. Corrige la causa y ejecuta regresión/checks afectados. No debilites aserciones ni sustituyas errores por éxito.
5. Repite el flujo por su entrada real; comprueba respuesta, persistencia y efectos.
6. Registra límites y cleanup. Sin evidencia requerida, el estado sigue pendiente de verificación.

## Laboratorio y evidencia

El laboratorio reproduce las propiedades relevantes: versión de runtime, motor, transporte seguro, workers/scheduler, almacenamiento y servicios simulados o sandbox. Usa recursos aislados; no perturbar cargas ajenas. Vincula el artefacto ejecutado a revisión/hash y configuración no sensible; no editar manualmente una proyección generada.

En cada aceptación incluye casos pertinentes de permiso denegado, otro tenant, expiración/revocación, duplicado, dependencia caída, timeout, reintento y recuperación. Verifica resultado observable y estado durable, no solo status o health.

Usa [verification-record.template.md](../templates/verification-record.template.md). Conserva resúmenes sanitizados, recuentos reales y referencias reproducibles; nunca tokens, cookies, dumps, logs crudos o capturas privadas. Los checks no ejecutados, bloqueados o simulados llevan su estado exacto y la acción que cerraría la brecha.
