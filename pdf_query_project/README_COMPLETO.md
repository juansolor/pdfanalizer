# 📄 PDF Query System - Sistema Completo Mejorado

Sistema completo para cargar PDFs y realizar consultas inteligentes sobre su contenido.

## 🎯 Características Principales

### Backend (FastAPI)
- ✅ Extracción de texto de PDFs
- ✅ Análisis inteligente de preguntas
- ✅ Búsqueda contextual en documentos
- ✅ Identificación de palabras clave
- ✅ Respuestas basadas en contenido real
- ✅ Estadísticas de coincidencias
- ✅ CORS configurado para Vite (puerto 5173)

### Frontend (Vite + React)
- ✅ Interfaz moderna y responsive
- ✅ Indicador de estado de conexión
- ✅ Subida de archivos PDF
- ✅ Selector de PDFs disponibles
- ✅ Formulario de consultas
- ✅ Respuestas formateadas con contexto
- ✅ Estadísticas de búsqueda
- ✅ Animaciones suaves

## 🚀 Cómo Ejecutar

### 1. Backend

```bash
cd backend
python main.py
```

El backend estará en: `http://localhost:8000`
- Documentación API: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 2. Frontend

```bash
cd frontend_new
npm install  # Solo la primera vez
npm run dev
```

El frontend estará en: `http://localhost:5173`

## 📊 Funcionalidades de Análisis

### Tipos de Preguntas Soportadas
- **Definición**: "¿Qué es...?"
- **Proceso**: "¿Cómo funciona...?"
- **Temporal**: "¿Cuándo ocurrió...?"
- **Ubicación**: "¿Dónde está...?"
- **Razón**: "¿Por qué...?"
- **Cantidad**: "¿Cuánto...?"

### Análisis Inteligente
1. **Extracción de palabras clave**: Identifica términos importantes en la pregunta
2. **Búsqueda contextual**: Encuentra menciones en el PDF con contexto
3. **Agrupación de resultados**: Organiza respuestas por tema
4. **Limitación inteligente**: Muestra solo información relevante

## 💡 Ejemplo de Uso

1. **Sube un PDF**
   - Click en "Subir PDF"
   - Selecciona tu archivo
   - Espera confirmación

2. **Selecciona el PDF**
   - Elige el PDF de la lista desplegable

3. **Haz una pregunta**
   - Ejemplo: "¿Qué es la inteligencia artificial?"
   - Ejemplo: "¿Cómo funciona el sistema?"
   - Ejemplo: "¿Cuándo se fundó la empresa?"

4. **Recibe respuestas**
   - Contexto extraído del PDF
   - Número de coincidencias encontradas
   - Palabras clave utilizadas en la búsqueda

## 🔧 Configuración

### Backend (.env)
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
RELOAD=True
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
MAX_FILE_SIZE=50
```

### Frontend (vite.config.js)
```javascript
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173
  }
})
```

## 📁 Estructura del Proyecto

```
pdf_query_project/
├── backend/
│   ├── main.py              # API FastAPI mejorada
│   ├── .env                 # Configuración
│   ├── requirements.txt     # Dependencias Python
│   ├── pdfs/               # PDFs subidos
│   ├── results/            # Resultados procesados
│   └── start.ps1           # Script de inicio
│
└── frontend_new/            # Frontend con Vite
    ├── src/
    │   ├── App.jsx         # Componente principal
    │   ├── App.css         # Estilos del componente
    │   └── index.css       # Estilos globales
    ├── package.json        # Dependencias
    └── vite.config.js      # Config de Vite
```

## 🎨 Mejoras Implementadas

### Backend
- [x] Función `extract_pdf_text()` - Extracción completa de texto
- [x] Función `search_in_text()` - Búsqueda con contexto
- [x] Función `analyze_question()` - Análisis de tipo de pregunta
- [x] Función `generate_answer()` - Generación de respuestas inteligentes
- [x] Endpoint `/query` mejorado con análisis real
- [x] Manejo de errores robusto
- [x] Respuestas con estadísticas

### Frontend
- [x] Visualización de respuestas multilinea
- [x] Resaltado de líneas importantes
- [x] Estadísticas de búsqueda
- [x] Animaciones de entrada
- [x] Mejor manejo de errores
- [x] Estado de carga visual

## 🛣️ Próximas Mejoras Posibles

- [ ] Integración con OpenAI para respuestas más inteligentes
- [ ] Búsqueda semántica con embeddings
- [ ] Soporte para PDFs escaneados (OCR)
- [ ] Historial de consultas
- [ ] Exportar respuestas
- [ ] Múltiples idiomas
- [ ] Cache de PDFs procesados

## 📝 Notas

- El sistema actual funciona con **búsqueda de texto exacto**
- No requiere API keys ni conexión a internet
- Ideal para documentos con texto extraíble
- Para PDFs escaneados, considerar agregar OCR (Tesseract)

## 🆘 Solución de Problemas

### "Backend desconectado"
- Verifica que el backend esté corriendo en puerto 8000
- Revisa que CORS incluya puerto 5173

### "No encontré información"
- Verifica que el PDF tenga texto extraíble
- Intenta con palabras clave más específicas
- El PDF puede ser una imagen escaneada

### "Error al procesar"
- Verifica que el archivo sea un PDF válido
- Revisa los logs del backend
- Asegúrate de que el PDF no esté corrupto

## 📞 Soporte

Sistema desarrollado con:
- Python 3.13+
- FastAPI
- PyPDF2
- Vite 7
- React 18
- Axios

---

¡Listo para usar! 🎉