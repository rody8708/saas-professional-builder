# 05 · Corregir una causa raíz demostrada

## Defecto
{{Comportamiento observado, comportamiento esperado, usuarios/interfaces afectados y evidencia sin datos sensibles}}

## Condiciones previas
Lee las reglas y el perfil, los puntos de llamada pertinentes y la evidencia existente. Usa la política de rama/base del proyecto; conserva el trabajo ajeno al alcance. Opera únicamente sobre recursos sintéticos y aislados; nunca leas credenciales operativas ni datos de clientes para preparar datos de prueba.

## Procedimiento
1. Relaciona el síntoma, la posible causa y cada punto de entrada que alcance la lógica afectada.
2. Reproduce el fallo con entrada sintética o inyección controlada de fallos. Si no es posible reproducirlo, comunica la limitación sin llamar demostrada a la causa.
3. Añade una prueba de regresión y ejecútala sobre la versión sin corregir; debe fallar por el defecto original.
4. Corrige la causa en el límite responsable. Inspecciona rutas equivalentes por si comparten el mismo defecto y atiéndelas dentro del alcance o comunícalas.
5. Ejecuta la regresión focalizada y las comprobaciones obligatorias; amplía las pruebas según el impacto, sin repetir por repetir.
6. Repite el flujo afectado mediante su punto de entrada real en el laboratorio, incluidas las rutas pertinentes de denegación, tiempo de espera agotado, reintento, duplicado y fallo parcial. Verifica el resultado observable, el estado duradero y los efectos secundarios.
7. Registra revisión, preparación, resultados esperados/reales, pruebas y evidencia pendiente con la [plantilla de verificación](../templates/verification-record.template.md).
8. Desmonta únicamente los recursos propios y verifica su ausencia.

## Entregar
Causa, corrección, evidencia de fallo previo/éxito posterior, repetición del flujo real, limpieza y brechas. Un endpoint saludable o una suite aprobada por sí solos no cierran el defecto. No debilites las aserciones, presentes fallos suprimidos como éxitos ni ocultes infracciones mediante exclusiones.
