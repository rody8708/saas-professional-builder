# 02 · Generar las reglas del proyecto

## Solicitud
Crea o actualiza las reglas para {{proyecto y alcance}} a partir de los requisitos confirmados.

## Procedimiento
1. Lee las reglas existentes y el perfil del proyecto; selecciona el perfil técnico mediante el [catálogo](../profiles/registry.json). Conserva las convenciones establecidas y las instrucciones del usuario.
2. Usa [RULES.template.md](../templates/RULES.template.md) y [AGENTS.template.md](../templates/AGENTS.template.md) como puntos de partida, no como archivos que sobrescribir sin revisión.
3. Define la arquitectura real, los responsables, el modelo de tenants, los modos de autenticación, la autorización, el tratamiento de datos, los niveles de prueba, las obligaciones de documentación y los requisitos de entrega del proyecto.
4. Enumera solo comandos, rutas y controles reales. Marca como pendiente un control sin implementar y asígnale un responsable, en lugar de afirmar que ya se aplica.
5. Mantén los comandos de cada tecnología en las secciones específicas del proyecto/perfil; las reglas comunes describen garantías.
6. Distingue los controles obligatorios de las recomendaciones. Cada excepción identifica motivo, responsable, alcance, caducidad/condición de revisión y verificación compensatoria.
7. Incluye límites de alcance: una revisión de solo lectura sigue siendo de solo lectura; implementar no implica desplegar; respeta los permisos ya concedidos.
8. Valida enlaces, comandos y coherencia con el repositorio real sin modificar código ajeno al alcance.

## Entregar
Diferencias en las reglas, decisiones conservadas/modificadas, relación entre requisitos y controles que los aplican, y requisitos pendientes. No instales dependencias, publiques ni implementes funcionalidades por el mero hecho de que las reglas generadas las mencionen.
