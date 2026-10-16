# 07 · Auditar seguridad, aislamiento entre tenants y privacidad

## Alcance
{{Áreas, entornos y modo autorizado: revisión de solo lectura o pruebas activas aisladas}}
Lee las reglas y el perfil del proyecto y la [guía de seguridad](../core/security-privacy.md). Mantén el modo de solo lectura si no se han solicitado pruebas activas o correcciones.

## Identificar y evaluar
1. Identidad: mecanismos de autenticación soportados, ciclo de vida de credenciales, recuperación, equivalencia de autenticación reforzada, fijación de sesión, revocación y límites frente al abuso.
2. Autoridad: permiso explícito en cada operación; estado actual de pertenencia/rol/tenant; acciones compuestas; suplantación administrativa, si existe.
3. Aislamiento entre tenants: lecturas, escrituras, agregados, búsqueda, trabajos, cachés, archivos, exportaciones y eventos; relaciones seguras entre tenants.
4. Modos de ruta: CSRF con credenciales adjuntadas automáticamente; rutas exclusivamente Bearer sin recurrir a cookies; webhooks con firma sobre el cuerpo original y controles de marca temporal/repetición.
5. Entrada/salida: codificación/saneamiento contextual, esquemas de URL, consultas parametrizadas, cargas de archivos, redirecciones y tráfico saliente.
6. Privacidad: matriz explícita de datos, exportación/supresión/retención, propiedad compartida, restauración de copias de seguridad, registros mínimos y procesamiento externo.
7. Pagos, si existen: intención duradera, claves estables ante resultados desconocidos, confirmación, reclamación exclusiva y exclusión de trabajadores obsoletos, y reconciliación.

## Verificar dentro de la autorización
Para las pruebas activas, usa únicamente recursos sintéticos aislados. Incluye CSRF ausente/inválido, cookie válida con Bearer ausente/inválido, tenants contradictorios entre cookie y token, pertenencias revocadas, acceso directo a archivos y trabajos en cola. Para webhooks, prueba firmas inválidas/caducadas y duplicados; para contenido renderizado, prueba cada contexto ejecutable. Inyecta fallos solo en recursos propios.

El análisis de solo lectura no debe crear cuentas, enviar mensajes, modificar registros ni ejecutar sondeos destructivos. Cuando se autoricen correcciones, demuestra el defecto, añade una regresión que falle, corrige y repite el punto de entrada real afectado. Limpia todos los recursos propios y verifica su ausencia.

## Resultado
Hallazgo, gravedad, evidencia, causa raíz, solución y estado; separa las decisiones de política de los defectos. Incluye el alcance probado, pruebas no ejecutadas, limpieza y evidencia exacta necesaria para cerrar cada brecha. No declares cumplimiento legal ni certificación universal de seguridad.
