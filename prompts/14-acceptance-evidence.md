# 14 · Demostrar un flujo mediante su punto de entrada real

## Objetivo
{{Funcionalidad, defecto o versión publicada}} en la revisión {{identificador de revisión/artefacto}}.

## Preparación
Lee el perfil del proyecto y la [guía de pruebas](../core/testing-verification.md). Confirma que el entorno de ejecución aislado corresponda al código/artefacto previsto. Reproduce las propiedades pertinentes de producción y usa únicamente identidades/datos sintéticos y proveedores en modo de pruebas.

Registra cada recurso creado con un identificador de ejecución y un propietario: procesos, puertos, esquemas, archivos, volúmenes, cuentas, colas y correo. Nunca edites una versión generada ni interrumpas otra carga de trabajo.

## Ejecutar
1. Reproduce el defecto si corresponde; de lo contrario, registra que no pudo reproducirse.
2. Ejecuta el punto de entrada real: navegador/cliente, API, planificador, consumidor de cola o entrega firmada del proveedor.
3. Compara el resultado esperado/observado de UI o protocolo e inspecciona estado persistido, auditoría y efectos externos.
4. Prueba las entradas inválidas pertinentes, autoridad denegada/revocada, otro tenant, duplicados, caída de dependencias, tiempo de espera agotado, reintentos y fallos parciales.
5. Verifica autenticación/CSRF/firmas adecuados al modo, errores seguros y aislamiento de datos.
6. Confirma que la recuperación no duplique efectos; distingue la ejecución externa real de la simulación controlada.

## Registrar y limpiar
Usa [verification-record.template.md](../templates/verification-record.template.md). Incluye comandos/resultados/recuentos reales, entorno/revisión, límites, comprobaciones bloqueadas y lo necesario para cerrar cada brecha. No guardes credenciales, registros o volcados sin depurar, ni capturas privadas.

Desmonta los recursos propios incluso ante fallos y verifica su ausencia de forma independiente. Si no está clara su propiedad, no los elimines; comunica la limpieza concreta que queda pendiente.

## Entregar
Estado de aceptación por caso, evidencia sin datos sensibles, limpieza y requisitos pendientes. Ninguna comprobación está aprobada si no se ejecutó y observó; un endpoint saludable o una suite aprobada no sustituyen el flujo.
