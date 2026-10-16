# 06 · Revisar defectos concretos

## Alcance
Revisa {{diff, pull request, rama o artefacto}} frente a las reglas y el perfil del proyecto. La revisión es de solo lectura salvo que las correcciones se hayan autorizado por separado.

## Inspeccionar
- Corrección: invariantes, transacciones, concurrencia, precisión, zona horaria, fallos parciales y reintentos.
- Arquitectura: límites declarados, responsabilidades, acoplamiento inadecuado y controles que no analizan código o exageran su alcance.
- Seguridad: modo real de autenticación, permisos explícitos/revalidados, acceso entre tenants en lecturas/escrituras/trabajos/cachés/archivos, CSRF/XSS según el contexto, inyección, tráfico saliente y errores seguros.
- Facturación, si existe: claves de idempotencia estables ante resultados desconocidos, confirmación del proveedor, orden de eventos, reconciliación y entrega duradera.
- Privacidad: ciclo de vida elegido para los datos, registros mínimos, propiedad compartida, exportación/supresión/retención y restauración.
- Pruebas: regresión creíble, semántica del motor de producción, aislamiento sintético, aserciones significativas y limpieza verificada.
- UX: idiomas acordados, formatos, accesibilidad, estados y verificación visual real.
- Entrega: contratos/documentación, compatibilidad/recuperación de migraciones, responsables operativos y evidencia veraz.

## Método
Lee las diferencias pertinentes y los puntos de llamada. Para cada hallazgo, establece una entrada/estado concreto y un resultado incorrecto, con evidencia de ruta/línea exactas. Separa los defectos demostrados de las decisiones sin resolver y las comprobaciones sin ejecutar. No inventes evidencia de ejecución ni ejecutes flujos de aceptación que modifiquen estado durante una revisión de solo lectura.

## Resultado
Ordena los hallazgos accionables por gravedad, con ubicación, escenario de fallo, impacto y solución. Después indica el alcance inspeccionado y las brechas de verificación relevantes. Si no se encontró ningún defecto accionable, dilo sin implicar seguridad completa ni certificación para producción.
