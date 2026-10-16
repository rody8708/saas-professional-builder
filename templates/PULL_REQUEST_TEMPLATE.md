## Problema y comportamiento resultante

{{Desencadenante concreto y comportamiento antes/después; alcance útil para quien revisa sin conocer el historial de la conversación.}}

## Verificación

| Comprobación o flujo | Entorno/revisión | Resultado real | Evidencia |
|---|---|---|---|
| {{comprobación}} | {{entorno}} | {{aprobada/fallida/bloqueada/no ejecutada; recuentos reales}} | {{referencia sin datos sensibles}} |

{{Para una corrección: reproducción, regresión que falla antes, pasa después y repetición del punto de entrada real afectado. Para cambios solo documentales: indica las comprobaciones documentales y la ausencia de afirmaciones sobre ejecución.}}

## Controles aplicables

Marca casillas únicamente con evidencia de respaldo. Identifica explícitamente los elementos no aplicables y su motivo.

- [ ] Permisos y pertenencia/contexto de tenant vigentes validados.
- [ ] Lecturas/escrituras entre tenants y trabajos/cachés/archivos afectados comprobados.
- [ ] Protección acorde con el modo de autenticación; tratamiento contextual de la salida comprobado.
- [ ] Idempotencia, concurrencia, fallos parciales y entrega duradera cubiertos donde corresponda.
- [ ] Ciclo de vida de datos y propiedad compartida conforme a una política explícita.
- [ ] UX, accesibilidad, idiomas e interfaces de cliente requeridos verificados.
- [ ] Documentación y contratos reflejan el comportamiento implementado.
- [ ] Diff completo inspeccionado; secretos/datos privados excluidos.
- [ ] Recursos temporales propios eliminados y ausencia verificada.

## Datos, compatibilidad y despliegue

{{Migración/relleno de datos; coexistencia con código/clientes antiguos; orden de despliegue; criterios de interrupción; reversión/recuperación hacia delante; responsable. Indica que no aplica y el motivo cuando corresponda.}}

## Impacto operativo

{{Cambios de configuración sin secretos; capacidad/coste, monitorización, alertas, manuales operativos e impacto en recuperación.}}

## Brechas y excepciones pendientes

| Brecha/excepción | Impacto | Responsable | Evidencia necesaria para cerrar |
|---|---|---|---|
| {{elemento o ninguno}} | {{impacto}} | {{responsable}} | {{cierre}} |

{{No declares aprobada una comprobación no ejecutada, resuelta una brecha de evidencia pendiente ni certificado para producción un subconjunto de pruebas.}}
