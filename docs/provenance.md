# Procedencia y alcance de la copia

Esta edición deriva de [saas-enterprise-builder](https://github.com/rody8708/saas-enterprise-builder), commit `3f5a130ea7632b1497514cd3f5e6ff1721493326`, conservado como repositorio independiente. El origen conceptual son las reglas y patrones de Zendrhax SaaS; no se copia la aplicación ni sus datos.

La edición anterior agrupaba guías comunes con ejemplos y herramientas PHP. Esta copia mueve los controles PHP a su perfil, reescribe el núcleo y los prompts sin stack predeterminado, incorpora perfiles separados y define un contrato común de verificación.

El repositorio fuente, su ZIP y Zendrhax se conservan sin modificaciones. La publicación de esta copia se realiza en un repositorio privado nuevo. El contenido se limita a documentación, plantillas, controles y fixtures sintéticos; no incluye secretos, configuraciones de despliegue, datos operativos ni dependencias instaladas.

Los controles probados acreditan únicamente sus escenarios registrados en [validation.md](validation.md). Cada SaaS futuro necesita su diseño, implementación, pruebas funcionales y operación verificadas.
