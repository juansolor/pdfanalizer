# 🚀 Guía Rápida de Ejecución - PDF Query System

## ✅ Nuevas Funcionalidades Agregadas

### 🎯 **NUEVO: Ubicación de Páginas en PDF**
- **📍 Muestra en qué páginas** está la respuesta a tu pregunta
- **🔗 Abre el PDF** directamente en la página correcta
- **📊 Tarjetas visuales** con contexto de cada ubicación
- **💡 Chips interactivos** para navegar entre páginas

### 📊 Análisis Avanzado
1. **Resumen Automático** - Genera un resumen del documento con estadísticas
2. **Palabras Frecuentes** - Top 20 palabras más repetidas (excluyendo stop words)
3. **Estadísticas Completas** - Palabras, caracteres, líneas, palabras únicas
4. **Análisis Completo** - Todos los análisis en un solo click

### 🎯 Botones de Análisis
- 📋 **Resumen**: Extrae las primeras oraciones importantes + estadísticas básicas
- 📊 **Palabras Frecuentes**: Muestra las 20 palabras más usadas con conteo
- 📈 **Estadísticas**: Total de palabras, caracteres, líneas, promedio
- 🚀 **Análisis Completo**: Ejecuta todos los análisis a la vez

## 🏃 Iniciar el Sistema

### 1️⃣ Backend (Terminal 1)

```powershell
cd d:\PDFviewer\pdf_query_project\backend
python main.py
```

**URL Backend**: http://localhost:8000
**Documentación**: http://localhost:8000/docs

### 2️⃣ Frontend (Terminal 2)

```powershell
cd d:\PDFviewer\pdf_query_project\frontend_new
npm run dev
```

**URL Frontend**: http://localhost:5173

## 📝 Cómo Usar las Nuevas Funciones

### Paso 1: Sube tu PDF
1. Click en el input de archivo
2. Selecciona tu PDF
3. Click en "📤 Subir PDF"

### Paso 2: Selecciona el PDF
Elige el PDF de la lista desplegable

### Paso 3: Haz una Pregunta y Ve las Ubicaciones ⭐ NUEVO

**Funcionalidad de Ubicación:**
1. Escribe tu pregunta sobre el PDF
2. Click en "🔍 Hacer Pregunta"
3. **📍 VE EN QUÉ PÁGINAS** está la respuesta
4. **🔗 ABRE EL PDF** en la página exacta con un click

**Ejemplo de respuesta:**
```
📄 Basándome en el documento 'manual.pdf', encontré:

📍 Página 3:
   • El sistema permite a los usuarios...

📍 Página 7:
   • El proceso de validación consta...

📊 Resumen:
• Encontré 5 coincidencias en 2 páginas
• Palabras clave: sistema, usuario, proceso

[Tarjetas con botón "🔗 Abrir" para cada página]

📄 Páginas con coincidencias:
[Pág. 3] [Pág. 7] ← Click para abrir
```

### Paso 4: Usa el Análisis Avanzado

**Opción A - Análisis Individual:**
- Click en "📋 Resumen" para ver resumen + estadísticas
- Click en "📊 Palabras Frecuentes" para top 20 palabras
- Click en "📈 Estadísticas" para números del documento

**Opción B - Análisis Completo:**
- Click en "🚀 Análisis Completo" para todo a la vez

## 📊 Endpoints Nuevos del Backend

### 1. Query con Ubicaciones (Actualizado)
```http
POST /query
Body: {"question": "...", "filename": "..."}
Response: {
  "answer": "...",
  "keywords": ["palabra1", "palabra2"],
  "locations": [
    {"page": 3, "keywords": [...], "preview": "..."}
  ],
  "pages_found": [3, 7, 12],
  "total_matches": 5
}
```

### 2. Ver PDF en el Navegador (Nuevo)
```http
GET /view-pdf/{filename}
Response: Archivo PDF para visualización inline
Uso: http://localhost:8000/view-pdf/documento.pdf#page=3
```

### 3. Análisis Individual
```http
POST /analyze/{filename}?analysis_type=summary
POST /analyze/{filename}?analysis_type=word_frequency  
POST /analyze/{filename}?analysis_type=statistics
```

### 4. Análisis Completo (Batch)
```http
POST /batch-analyze/{filename}
```

Retorna todo en una sola respuesta:
- Resumen completo
- Top 15 palabras frecuentes
- Todas las estadísticas

## 🎨 Visualización en el Frontend

### Resumen
- Formato pre-formateado con saltos de línea
- Emojis para mejor lectura
- Estadísticas al final

### Palabras Frecuentes
- Grid con ranking (#1, #2, etc.)
- Nombre de la palabra
- Conteo de apariciones
- Scroll si hay muchas palabras
- Hover effects

### Estadísticas
- Cards con gradientes
- Números grandes y legibles
- Formato con separadores de miles
- Responsive grid

## 🔥 Funciones Implementadas

### Backend (`main.py`)

```python
# Nuevas funciones
generate_summary(text, max_sentences=5)      # Resumen automático
get_word_frequency(text, top_n=20)          # Palabras más frecuentes
translate_text(text, target_lang="en")       # Placeholder traducción

# Nuevos endpoints
@app.post("/analyze/{filename}")             # Análisis individual
@app.post("/batch-analyze/{filename}")       # Análisis completo
```

### Frontend (`App.jsx`)

```javascript
// Nuevos estados
const [analysisResult, setAnalysisResult] = useState(null)
const [showAnalysis, setShowAnalysis] = useState(false)

// Nueva función
const handleAnalysis = async (analysisType) => { ... }
```

## 🎯 Ejemplo de Respuesta - Análisis Completo

```json
{
  "filename": "documento.pdf",
  "summary": "📋 RESUMEN DEL DOCUMENTO\n\n• Primera oración...\n• Segunda oración...",
  "word_frequency": [
    {"word": "sistema", "count": 45},
    {"word": "datos", "count": 32},
    ...
  ],
  "statistics": {
    "total_words": 5420,
    "total_characters": 35678,
    "total_lines": 342,
    "unique_words": 1256,
    "average_word_length": 6.58
  }
}
```

## 🐛 Solución de Problemas

### "Backend desconectado"
```powershell
# Asegúrate de tener las dependencias
pip install fastapi uvicorn python-multipart PyPDF2 python-dotenv

# Inicia el backend
cd backend
python main.py
```

### "Error al analizar"
- Verifica que el PDF tenga texto extraíble
- Los PDFs escaneados (imágenes) no funcionarán
- Tamaño máximo: 50MB

### Frontend no carga
```powershell
cd frontend_new
npm install
npm run dev
```

## 📈 Próximas Mejoras

- [ ] OCR para PDFs escaneados
- [ ] Traducción real con API (Google Translate/DeepL)
- [ ] Exportar análisis a PDF/Excel
- [ ] Comparación entre múltiples PDFs
- [ ] Gráficos de palabras (Word Cloud)
- [ ] IA para resúmenes más inteligentes
- [x] **✅ Mostrar ubicación exacta (páginas) en el PDF**
- [x] **✅ Abrir PDF directamente en la página correcta**
- [ ] Highlight del texto encontrado en el PDF
- [ ] Visor de PDF integrado en la app

## 🎉 ¡Listo!

Tu sistema ahora tiene:
- ✅ Consultas inteligentes
- ✅ **Ubicación de páginas con la información** 🆕
- ✅ **Apertura directa del PDF en la página correcta** 🆕
- ✅ Resúmenes automáticos
- ✅ Análisis de frecuencia
- ✅ Estadísticas completas
- ✅ Interfaz moderna con Vite

---

**¡Disfruta analizando tus PDFs con ubicación precisa!** 📄📍✨
