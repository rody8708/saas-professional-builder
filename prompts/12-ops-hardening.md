# 12 · Hacer recuperable la operación

## Alcance
{{Trabajos, colas, copias de seguridad, configuración, monitorización, retención o servicio definido}}
Lee las reglas y el perfil del proyecto y la [guía de operación](../core/operations.md). Confirma responsables operativos, entornos, SLO, RPO y RTO.

## Evaluar e implementar dentro del alcance
1. Configuración: requisitos previos validados, gestión de secretos, ejemplos seguros, privilegio mínimo y artefactos reproducibles.
2. Trabajos/colas: reclamaciones atómicas, concesiones temporales/exclusión de trabajadores obsoletos cuando sean necesarias, tiempo máximo de espera, recuperación tras interrupciones, reintentos acotados, visibilidad de pendientes y efectos idempotentes.
3. Durabilidad: outbox o equivalente cuando la pérdida de eventos/entregas incumpla el contrato; límites de retención y repetición.
4. Copias de seguridad: cobertura/frecuencia ligadas al RPO, copias cifradas fuera del dominio de fallo, claves recuperables por separado y retención aprobada.
5. Restauración: ensayo aislado que incluya datos/archivos/dependencias, invariantes de la aplicación, trabajos reanudados y datos ya suprimidos. Mide el tiempo transcurrido y el punto de recuperación.
6. Observabilidad: señales pertinentes de servicio/flujo, detección externa, registros seguros correlacionados, envío de alertas accionables y escalamiento.
7. Manuales operativos: responsable, señales, condiciones previas, pasos, comprobaciones, interrupción/recuperación y evidencia.

## Verificar
Inyecta fallos solo en recursos sintéticos propios del laboratorio: interrupción de trabajadores, concesión/señal de actividad obsoletas, caída del proveedor, cuota agotada, fallo de copia de seguridad y restauración. Confirma alertas, errores controlados, recuperación y ausencia de efectos duplicados. Elimina los recursos propios y verifica su ausencia.

## Entregar
Controles verificados frente a pendientes, objetivos medidos, evidencia de fallo/recuperación, manuales operativos y riesgo residual. No declares cumplidos el RTO/RPO a partir únicamente de un archivo de copia de seguridad o una respuesta de salud.
