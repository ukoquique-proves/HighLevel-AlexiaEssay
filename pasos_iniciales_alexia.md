# Pasos Iniciales – Proyecto Alexia

Este documento describe los primeros pasos recomendados para arrancar el proyecto Alexia, siguiendo el plan y priorizando el uso de HighLevel y N8N.

---

## 1. Preparación del Entorno

### a. HighLevel (HL)
1. **Crear cuenta y acceder a la prueba gratuita** en https://www.gohighlevel.com/
2. **Configurar cuenta de agencia o negocio** (según opción disponible en prueba):
   - Completar datos de empresa.
   - Personalizar logo y branding básico.
3. **Crear subcuenta para la primera PYME piloto** (si es posible en la prueba).
4. **Explorar los módulos clave**: Forms, Surveys, Funnels, Workflows, Pipelines, Memberships, Integraciones.

### b. N8N
1. **Verificar acceso y funcionamiento** de tu instancia N8N.
2. **Preparar un workspace dedicado** para el proyecto Alexia.
3. **Revisar credenciales y conexiones disponibles** (webhooks, APIs, integraciones con HL, OpenAI, Meta Ads, Stripe/ePayco).

---

## 2. Flujo de Onboarding y Captura de Información

### a. En HighLevel
1. **Crear un formulario inteligente** para onboarding inicial del empresario:
   - Nombre, empresa, sector, objetivos, canales actuales, presupuesto, etc.
   - Usar lógica condicional si HL lo permite.
2. **Crear un workflow** que:
   - Envíe el formulario tras el registro/contacto.
   - Notifique al equipo cuando un formulario es completado.
   - Cree una oportunidad en el pipeline de ventas.
3. **Diseñar una landing page/funnel** de bienvenida con acceso al formulario (opcional).

### b. Integración con N8N
1. **Configurar un webhook en N8N** para recibir los datos del formulario de HL.
2. **Crear un flujo en N8N** que:
   - Reciba los datos del formulario.
   - Almacene la información (Google Sheets, base de datos, etc.).
   - (Opcional) Envíe un email de bienvenida automatizado.

---

## 3. Siguientes pasos sugeridos
- Validar que el flujo de onboarding y captura de datos funciona de extremo a extremo (HL → N8N → almacenamiento).
- Documentar cualquier limitación encontrada en HL durante la prueba gratuita.
- Preparar la siguiente fase: generación de propuestas y activos de marketing con IA.

¿Quieres que te ayude con ejemplos específicos de formularios, workflows o flujos de N8N para estos pasos?
