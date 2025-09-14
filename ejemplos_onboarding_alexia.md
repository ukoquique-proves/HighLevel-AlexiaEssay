# Ejemplos de Formularios, Workflows y Flujos N8N según el Plan Alexia

Estos ejemplos están alineados con el plan del archivo seleccionado y cubren el onboarding, captura de estrategia y la integración inicial HL ↔ N8N.

---

## 1. Ejemplo de Formulario Inteligente (HighLevel)
**Nombre:** Onboarding Empresario Moda LATAM

**Campos sugeridos:**
- Nombre del empresario
- Nombre de la empresa
- País y ciudad
- Sector (desplegable: moda femenina, masculina, infantil, accesorios, etc.)
- ¿Vendes online actualmente? (Sí/No)
- ¿Qué canales usas? (checkbox: Instagram, Facebook, WhatsApp, Tienda física, Otro)
- Volumen de ventas mensual (opcional)
- Objetivo principal (desplegable: aumentar ventas, captar leads, lanzar producto, fidelizar clientes)
- Presupuesto mensual estimado para marketing
- ¿Tienes imágenes/videos de tus productos? (Sí/No)
- ¿Qué hace única a tu marca? (texto libre)

**Lógica condicional sugerida:**
- Si responde "Sí" a "¿Vendes online?", mostrar campo para URL de tienda o redes sociales.
- Si "Otro" en canales, mostrar campo para especificar.

---

## 2. Ejemplo de Workflow (HighLevel)
**Nombre:** Onboarding → Notificación y Pipeline

**Disparador:** Formulario "Onboarding Empresario Moda LATAM" completado.

**Acciones:**
1. Crear oportunidad en pipeline "Nuevos Leads Alexia" (etapa: Captura de datos).
2. Notificar por email/WhatsApp al equipo de Alexia.
3. Enviar email de bienvenida al empresario (puede incluir link a funnel de propuestas si está listo).
4. Llamar a webhook de N8N con los datos del formulario.

---

## 3. Ejemplo de Webhook y Flujo en N8N
**Nombre:** Recibir Onboarding Alexia

**Pasos:**
1. Webhook N8N recibe datos del formulario HL.
2. Guardar datos en Google Sheets, Airtable o base de datos.
3. (Opcional) Enviar un email de bienvenida personalizado usando nodos de correo.
4. (Opcional) Activar flujo para generación automática de buyer persona/copy con IA (GPT-4/OpenAI) y guardar resultados.

---

## 4. Ejemplo de Pipeline en HL
- Etapas: Captura de datos → Análisis → Propuesta enviada → Aprobada → Campaña publicada → Seguimiento

---

## 5. Landing/Funnel de Bienvenida (HL)
- Página con explicación breve del proceso Alexia, beneficios y botón para iniciar el onboarding.

---

¿Quieres que prepare ejemplos de mensajes automáticos, propuestas de copy para emails, o flujos de generación de activos con IA para las siguientes fases?
