# 10 · Migrar datos con compatibilidad y recuperación

## Cambio
{{Cambio de esquema/datos, módulo propietario, motores soportados y estructura de despliegue}}

## Procedimiento
1. Lee las reglas y el perfil y la [guía de entrega](../core/delivery-workflow.md). Usa el mecanismo de migraciones versionadas del framework.
2. Describe los esquemas actual/destino, la propiedad de los datos, las relaciones seguras entre tenants, los índices, las invariantes y el impacto en los consumidores antiguos.
3. Planifica expansión y contracción cuando coexistan versiones: expansión compatible, código compatible, relleno de datos idempotente por lotes, validación, retirada y contracción controlada por separado.
4. Define límites de transacciones/DDL, privilegios, bloqueos, duración, interrupción y capacidad de reanudación para cada motor soportado.
5. Proporciona una reversión segura cuando sea posible; de lo contrario, identifica el paso como irreversible y define recuperación/corrección hacia delante. No finjas revertir una pérdida de datos por restaurar el nombre de una columna.
6. Prueba bases de datos sintéticas vacías y pobladas sobre todos los motores soportados, incluido el de producción. Ejercita interrupción/reintento, concurrencia y restricciones.
7. Ejecuta ciclos de reversión/aplicación para cambios reversibles; ensaya el plan real de recuperación para cambios irreversibles.
8. Documenta orden de despliegue, observabilidad, criterios de interrupción y responsable. La ejecución destructiva en producción requiere la autorización aplicable del usuario y no queda implícita al escribir una migración.

## Entregar
Migración y relleno de datos, matriz de compatibilidad, resultados medidos de pruebas, evidencia de recuperación y riesgos pendientes. Las pruebas usan datos aislados y limpieza verificada, nunca copias de bases de datos de clientes.
