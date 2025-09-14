# Guía de Integración de APIs: OpenAI, Meta Developers, ePayco/Stripe

Esta guía explica cómo utilizar estas APIs en el proyecto Alexia, tanto con cuentas reales como con mocks y alternativas gratuitas para pruebas y desarrollo inicial.

---

## 1. OpenAI (GPT-4)

### Uso Real
- **Requiere**: Cuenta en https://platform.openai.com/
- **API Key**: Generar desde el dashboard de OpenAI.
- **Integración**: Usar librerías oficiales (`openai` para Python/Node.js).
- **Costo**: Pago por uso (hay créditos gratuitos limitados al crear cuenta nueva).

### Mock/Alternativa Gratuita
- **Mock**: Simular respuestas usando scripts locales o endpoints que devuelvan textos predefinidos.
- **Alternativas gratuitas**:
  - [Hugging Face Inference API](https://huggingface.co/inference-api): Algunos modelos gratuitos (requiere registro).
  - [OpenRouter.ai](https://openrouter.ai/): Ofrece acceso a modelos gratuitos y de pago.
  - [Cohere](https://cohere.com/): Tiene free tier con modelos de lenguaje.

---

## 2. Meta Developers (Meta Ads API)

### Uso Real
- **Requiere**: Cuenta en https://developers.facebook.com/
- **App**: Crear una app y obtener `App ID` y `App Secret`.
- **Token de acceso**: Generar tokens para pruebas y producción.
- **Integración**: Usar SDK oficial de Meta para Python/Node.js.
- **Costo**: Gratis, pero requiere cuenta de Facebook Business y página activa.

### Mock/Alternativa Gratuita
- **Mock**: Simular endpoints con herramientas como [Mockoon](https://mockoon.com/) o scripts que devuelvan estructuras JSON similares a la API real.
- **Alternativas gratuitas**: No existen APIs públicas equivalentes para anuncios Meta, pero puedes simular campañas y respuestas.

---

## 3. ePayco / Stripe (Pagos)

### Uso Real
- **ePayco**: Crear cuenta en https://epayco.co/, obtener `public_key` y `private_key`.
- **Stripe**: Crear cuenta en https://dashboard.stripe.com/, obtener claves de API.
- **Integración**: Usar SDKs oficiales según el lenguaje.
- **Costo**: Comisiones por transacción, pero modo test es gratuito.

### Mock/Alternativa Gratuita
- **Modo Test**: Tanto Stripe como ePayco ofrecen modo test para simular pagos sin dinero real.
- **Mock**: Simular endpoints de pago con respuestas de éxito/fallo usando herramientas como Mockoon o scripts locales.
- **Alternativas gratuitas**:
  - [MercadoPago Sandbox](https://www.mercadopago.com.co/developers/es/guides/online-payments/checkout-api/testing): Permite pruebas gratuitas de integración.
  - [Paypal Sandbox](https://developer.paypal.com/tools/sandbox/): Simulación de pagos sin costo.

---

## Recomendaciones para Desarrollo Inicial
- Implementar funciones de integración con las APIs usando variables de entorno para las claves.
- Crear una capa de abstracción para alternar entre modo real, test o mock según el entorno.
- Documentar bien los endpoints simulados y las diferencias con los reales.

---

¿Dudas o quieres ejemplos de código para mocks o integración real? ¡Avísame!
