# 13 · Revisar experiencia, accesibilidad y localización

## Alcance
{{Pantallas, flujos, dispositivos soportados, idiomas y temas}}
Lee el perfil del proyecto y la [guía de UX](../core/ux-i18n-assistant.md). Las solicitudes de revisión de solo lectura siguen siendo de solo lectura.

## Inspeccionar
- Claridad del flujo, jerarquía, espaciado, tipografía y coherencia de componentes/variables de diseño.
- Estados alcanzables: carga, vacío, éxito, validación, error, denegación, límite comercial y sin conexión cuando corresponda.
- Dispositivos/tamaños de ventana acordados, contenido largo, ampliación y orientación cuando sean pertinentes.
- Objetivo de accesibilidad: teclado, orden del foco, etiquetas, errores, contraste, áreas táctiles y tecnología de asistencia.
- Textos localizados, marcadores de posición, UTF-8, idioma alternativo y fechas/zonas horarias/números/monedas correctos.
- Planes/límites dinámicos desde su fuente; lenguaje sencillo en lugar de terminología de implementación.
- Las acciones destructivas identifican objeto/impacto con una confirmación proporcional.
- La ayuda refleja las capacidades reales y no afirma autorización ni finalización.

## Verificar
Abre las pantallas reales en el navegador/cliente soportado con datos sintéticos. Registra ruta, tamaño de ventana, idioma, tema, estado y resultado esperado/observado. Ejecuta las comprobaciones disponibles e informa de los controles ausentes. Para correcciones autorizadas, vuelve a comprobar la matriz afectada después de editar.

## Entregar
Hallazgos accionables con evidencia, combinaciones verificadas y brechas explícitas. Elimina los datos sensibles de las capturas. Las pruebas de componentes o capturas estáticas por sí solas no demuestran el flujo completo.
