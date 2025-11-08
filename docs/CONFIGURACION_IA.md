# 🤖 Configuración de IA para Traducción

El sistema ahora soporta traducción con IA para obtener resultados de mucha mejor calidad.

## 🔧 Configuración de API Keys

### 1. Google Gemini (Recomendado - Gratis)
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una API key gratuita
3. Edita el archivo `backend/.env`
4. Descomenta y agrega tu key:
   ```
   GEMINI_API_KEY=tu_api_key_de_gemini_aqui
   ```

### 2. OpenAI ChatGPT (Alternativa - Pago)
1. Ve a [OpenAI Platform](https://platform.openai.com/api-keys)
2. Crea una API key
3. Edita el archivo `backend/.env`
4. Descomenta y agrega tu key:
   ```
   OPENAI_API_KEY=tu_api_key_de_openai_aqui
   ```

## 🎯 Beneficios de la IA

### Sin IA (Solo Diccionario Local):
- ✅ Gratis y privado
- ❌ Cobertura limitada (~86%)
- ❌ Traducción palabra por palabra
- ❌ No entiende contexto

### Con IA (Gemini/ChatGPT):
- ✅ Cobertura >95%
- ✅ Entiende contexto técnico
- ✅ Traducción fluida y natural
- ✅ Mantiene terminología técnica
- ✅ Preserva formato y estructura
- ❌ Requiere API key

## 🚀 Uso

1. **Sin configurar IA**: El sistema usa diccionario local automáticamente
2. **Con IA configurada**: 
   - Aparece checkbox "🤖 IA" en la interfaz
   - Marca activado por defecto
   - Muestra qué IA está disponible (🟢 Gemini/GPT)
   - Fallback automático si falla la IA

## 📊 Comparación de Calidad

### Texto Original (Alemán):
```
Die Function AutoVR dient zum Herstellen einer gültigen Transition 
für die Ablaufsteuerung, wenn der Anlagenzustand im Handbetrieb 
manuell verändert wurde und beim Umschalten in den Automatikbetrieb 
keine gültige Transition gefunden wird.
```

### Traducción Local (Diccionario):
```
The Function AutoVR serves to Establish a valid Transition for the 
Sequence control, when the Plant status in Manual operation manual 
changed was and when Switching in the Automatic mode no valid 
Transition found is.
```

### Traducción con IA:
```
The AutoVR function serves to establish a valid transition for the 
sequence control when the system status has been manually changed 
in manual operation and no valid transition is found when switching 
to automatic mode.
```

## 🔄 Fallback Automático

El sistema tiene 3 niveles de traducción:
1. **Gemini** (si está configurado)
2. **OpenAI** (si Gemini falla y está configurado)  
3. **Diccionario local** (siempre disponible como último recurso)

## 💡 Recomendación

**Para uso personal/testing**: Usa Gemini (gratis, excelente calidad)
**Para uso empresarial**: Configura ambos (Gemini + OpenAI) para máxima confiabilidad
