# Experiencia, idiomas, accesibilidad y asistencia

Diseña para las tareas y superficies del producto. Idiomas, temas y dispositivos son decisiones del perfil; no existe una pareja de idiomas o una tecnología de cliente obligatoria.

## Experiencia verificable

Define jerarquía, tipografía, espaciado, color semántico y patrones reutilizables. Usa el sistema del framework o uno propio consistente; extrae componentes cuando se repitan problemas reales.

Cada flujo contempla los estados que puede alcanzar: carga, vacío, éxito, validación, fallo, falta de permiso, límite comercial y offline cuando aplique. Explica qué ocurrió y qué puede hacer la persona sin exponer implementación. Las acciones destructivas muestran objeto/alcance y una confirmación proporcional; no introducir diálogos rutinarios que impidan trabajar.

La UI responde a las pantallas soportadas. Verifica contenido largo, zoom, orientación cuando corresponda, teclado, foco, etiquetas, contraste, objetivos táctiles y tecnologías de asistencia relevantes. La norma y nivel objetivo de accesibilidad se registran en el perfil y se verifican con pruebas automáticas y revisión humana.

## Localización y formatos

Usa el mecanismo de localización elegido. Los idiomas publicados tienen claves, placeholders y formato equivalentes; revisión semántica además de guards sintácticos. Preserva UTF-8 y la escritura correcta de cada idioma en UI, emails, documentos y exportaciones.

Fechas, zonas horarias, números, unidades y moneda siguen el contexto del usuario y el contrato de datos. No hardcodear nombres de planes ni límites que provengan del catálogo. El fallback de idioma es explícito y no oculta silenciosamente copy faltante.

## Ayuda

Añade ayuda donde facilite una tarea real: propósito, condiciones, pasos seguros y límites. La ayuda refleja permisos y capacidades existentes sin concederlos. Rutas y recursos servidos desde un catálogo validado; no aceptar una ruta arbitraria del sistema de archivos.

Guías operativas y de usuario tienen dueños y una fuente canónica. Actualízalas junto con el flujo y registra traducciones pendientes antes de publicarlas como completas.

## Asistente opcional

Construir un asistente requiere alcance explícito: temas, herramientas, datos disponibles, proveedores, coste y acciones permitidas. No se añade por defecto a un SaaS.

- La autoridad vive en backend: las herramientas revalidan usuario, tenant, permisos y límites en cada operación.
- Contenido recuperado, adjuntos y resultados de herramientas son datos no confiables; no pueden ampliar permisos ni ordenar acciones.
- Distingue diagnóstico observado, inferencia y estado desconocido. Las respuestas enlazan fuentes/acciones existentes sin inventar acceso o resultados.
- Acciones con efectos requieren la autorización correspondiente, idempotencia y auditoría; una conversación no sustituye al control del caso de uso.
- Minimiza datos enviados a proveedores y define retención de conversaciones, redacción, borrado, presupuesto, timeout, fallback y apagado.
- Evalúa contexto multi-turno, aislamiento, inyección de instrucciones, datos sensibles, fallos de herramienta y confirmaciones; una única demostración no acredita cobertura completa.

## Revisión

Abre el resultado real en navegador o cliente soportado con datos sintéticos. Registra ruta, viewport, tema, idioma, estado y esperado/observado. Capturas y evidencia se sanitizan. Si una superficie no se revisó visualmente, decláralo; tests de componentes no prueban por sí solos la experiencia completa.
