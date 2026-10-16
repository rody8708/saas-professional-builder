# Verificación de {{flujo/cambio}}

Fecha: {{fecha/hora y zona horaria}}

Responsable: {{persona responsable de la verificación}}

Alcance: {{comportamiento y puntos de entrada}}
Estado: {{verificado dentro del alcance indicado / pendiente / fallido}}

## Revisión y entorno

{{Revisión del código/hash del artefacto, cambios locales, identidad del entorno de ejecución, versiones pertinentes, propiedades equivalentes a producción y diferencias conocidas. Sin credenciales ni endpoints privados.}}

## Preparación sintética y propiedad

{{Identidades/datos claramente sintéticos, proveedores aislados, identificador de ejecución y método para acreditar la propiedad.}}

| Tipo de recurso | Identificador/referencia no sensible | Propietario/ejecución | Método de limpieza |
|---|---|---|---|
| {{proceso/esquema/archivo/cuenta/etc.}} | {{referencia}} | {{ejecución}} | {{método}} |

## Reproducción o estado de referencia

{{Esperado frente a observado antes del cambio; pasos exactos seguros; regresión que falla por el defecto original. Si no está disponible, explica el motivo en lugar de inventarlo.}}

## Repetición tras el cambio

| Caso/punto de entrada | Pasos y entrada | Esperado | Observado y estado duradero | Estado |
|---|---|---|---|---|
| {{caso}} | {{pasos sintéticos}} | {{esperado}} | {{resultado/efectos}} | {{estado}} |

## Fallos, aislamiento y reintentos

{{Casos aplicables: permiso denegado/revocado, otro tenant, error de entrada, duplicado, concurrencia, fallo de dependencia, efecto aceptado con respuesta perdida, reintento, recuperación y ausencia de efectos duplicados.}}

## Comprobaciones automatizadas

| Comando/comprobación real | Entorno | Resultado/recuentos | Alcance/límites |
|---|---|---|---|
| {{comando}} | {{entorno}} | {{resultado real}} | {{límites}} |

## Ejecución externa frente a simulación

{{Separa los ejercicios reales en entornos de prueba de las simulaciones deterministas. Enumera las limitaciones de acceso a proveedores/dispositivos/entornos.}}

## Verificación de limpieza

| Recurso propio | Resultado de eliminación | Comprobación independiente de ausencia | Acción pendiente |
|---|---|---|---|
| {{recurso}} | {{resultado}} | {{comprobación}} | {{ninguna o acción}} |

{{No elimines recursos cuya propiedad no esté demostrada. Los fallos de limpieza permanecen visibles.}}

## Brechas pendientes

| Caso no ejecutado/bloqueado/fallido | Impacto | Responsable | Siguiente evidencia necesaria |
|---|---|---|---|
| {{brecha o ninguna}} | {{impacto}} | {{responsable}} | {{cierre}} |

## Tratamiento de la evidencia

{{Solo resúmenes/referencias sin datos sensibles. Sin registros sin depurar, tokens, cookies, archivos de entorno, volcados de bases de datos ni capturas privadas. Las conclusiones se aplican únicamente a la revisión, el entorno y los casos anteriores.}}
