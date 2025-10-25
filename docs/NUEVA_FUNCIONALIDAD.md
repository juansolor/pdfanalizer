# 🎯 Nueva Funcionalidad: Ubicación de Páginas en PDF

## ✨ ¿Qué se agregó?

Ahora el sistema **muestra exactamente en qué páginas** del PDF está la información relacionada con tu pregunta y **te permite abrir el PDF directamente en esa página**.

## 🚀 Características Nuevas

### 1️⃣ Búsqueda por Páginas
- El backend ahora extrae texto **página por página**
- Identifica en qué página(s) específica(s) aparece cada palabra clave
- Muestra el contexto exacto de cada coincidencia

### 2️⃣ Visualización de Ubicaciones
- **Tarjetas de ubicación** con información clara:
  - 📄 Número de página
  - 📝 Vista previa del contexto
  - 🔍 Palabras clave encontradas
  - 🔗 Botón para abrir el PDF

### 3️⃣ Apertura Directa del PDF
- Click en **"🔗 Abrir"** abre el PDF en una nueva pestaña
- El navegador se posiciona **automáticamente en la página correcta**
- Usa el formato estándar: `archivo.pdf#page=X`

### 4️⃣ Resumen Visual de Páginas
- **Chips interactivos** que muestran todas las páginas con coincidencias
- Click en cualquier chip para abrir esa página específica
- Diseño visual con gradientes y animaciones

## 🎨 Interfaz Mejorada

### Antes:
```
💡 Respuesta:
Basándome en el documento 'ejemplo.pdf', encontré lo siguiente:
...
```

### Ahora:
```
💡 Respuesta:
📄 Basándome en el documento 'ejemplo.pdf', encontré lo siguiente:

📍 Página 3:
   • [Contexto relevante...]

📍 Página 7:
   • [Contexto relevante...]

📊 Resumen:
• Encontré 5 coincidencias en 2 páginas
• Palabras clave buscadas: sistema, datos, proceso

[Tarjetas interactivas con botones para abrir cada página]

📄 Páginas con coincidencias:
[Pág. 3] [Pág. 7] ← Click para abrir
```

## 🔧 Cambios Técnicos

### Backend (main.py)

#### Nueva función: `extract_pdf_text_by_pages()`
```python
def extract_pdf_text_by_pages(file_path: Path) -> Dict[int, str]:
    """Extraer texto de un PDF separado por páginas"""
    # Retorna diccionario: {1: "texto pág 1", 2: "texto pág 2", ...}
```

#### Nueva función: `search_in_pages()`
```python
def search_in_pages(pages_text: Dict[int, str], keywords: List[str]) -> List[Dict]:
    """Buscar palabras clave en páginas específicas"""
    # Retorna lista con: página, línea, contexto, keyword
```

#### Nueva función: `generate_answer_with_pages()`
```python
def generate_answer_with_pages(question: str, file_path: Path, filename: str) -> Dict:
    """Generar respuesta con ubicaciones de página"""
    # Retorna:
    # {
    #   "answer": "Texto de respuesta",
    #   "keywords": ["palabra1", "palabra2"],
    #   "locations": [{"page": 3, "keywords": [...], "preview": "..."}],
    #   "total_matches": 5,
    #   "pages_found": [3, 7]
    # }
```

#### Nuevo endpoint: `/view-pdf/{filename}`
```python
@app.get("/view-pdf/{filename}")
async def view_pdf(filename: str, page: int = 1):
    """Servir PDF para visualización en el navegador"""
    # Retorna el archivo PDF con headers apropiados
    # Permite visualización inline en el navegador
```

#### Endpoint actualizado: `/query`
- Ahora usa `generate_answer_with_pages()` en lugar de `generate_answer()`
- Retorna estructura completa con ubicaciones
- Incluye páginas encontradas y contextos

### Frontend (App.jsx)

#### Nuevos estados:
```javascript
const [locations, setLocations] = useState([])        // Ubicaciones detalladas
const [pagesFound, setPagesFound] = useState([])      // Lista de páginas
```

#### Nueva función: `openPdfAtPage()`
```javascript
const openPdfAtPage = (page) => {
  const pdfUrl = `${API_BASE_URL}/view-pdf/${currentPdf}#page=${page}`
  window.open(pdfUrl, '_blank')
}
```

#### Actualización de `handleQuery()`:
- Ahora captura `locations` y `pages_found` de la respuesta
- Actualiza los estados correspondientes

### Frontend (App.css)

#### Nuevos estilos:
- `.locations-container`: Contenedor principal de ubicaciones
- `.locations-grid`: Grid de tarjetas de ubicación
- `.location-card`: Tarjeta individual con efecto hover
- `.location-header`: Header con página y botón
- `.page-badge`: Badge con número de página (gradiente)
- `.btn-open-pdf`: Botón para abrir PDF
- `.location-preview`: Vista previa del contexto
- `.keywords-found`: Sección de palabras clave
- `.pages-summary`: Resumen de páginas
- `.page-chips`: Chips interactivos de páginas

## 📊 Ejemplo de Respuesta del Backend

```json
{
  "answer": "📄 Basándome en el documento 'manual.pdf'...\n\n📍 **Página 3:**\n   • El sistema permite...",
  "keywords": ["sistema", "usuario", "proceso"],
  "locations": [
    {
      "page": 3,
      "keywords": ["sistema", "usuario"],
      "preview": "El sistema permite a los usuarios gestionar sus datos de forma..."
    },
    {
      "page": 7,
      "keywords": ["proceso"],
      "preview": "El proceso de validación consta de tres etapas principales..."
    }
  ],
  "total_matches": 5,
  "pages_found": [3, 7],
  "question": "¿Cómo funciona el sistema?",
  "filename": "manual.pdf"
}
```

## 🎯 Flujo de Usuario

1. **Usuario sube un PDF** ✅
2. **Usuario selecciona el PDF** ✅
3. **Usuario hace una pregunta** ✅
4. **Sistema muestra respuesta** ✅
5. **🆕 Sistema muestra tarjetas con ubicaciones**
6. **🆕 Usuario puede ver en qué páginas está la info**
7. **🆕 Usuario hace click en "Abrir"**
8. **🆕 Se abre el PDF en nueva pestaña en la página exacta**
9. **🆕 Usuario puede navegar el PDF desde esa página**

## 🎨 Diseño Visual

### Tarjeta de Ubicación
```
┌─────────────────────────────────────┐
│ 📄 Página 3        [🔗 Abrir]       │
├─────────────────────────────────────┤
│ │ El sistema permite a los          │
│ │ usuarios gestionar sus datos...   │
├─────────────────────────────────────┤
│ Palabras: sistema, usuario          │
└─────────────────────────────────────┘
```

### Chips de Páginas
```
📄 Páginas con coincidencias:
[Pág. 3] [Pág. 7] [Pág. 12]
  ↑        ↑         ↑
Click para abrir cada página
```

## 🔥 Ventajas

✅ **Localización Precisa**: Sabes exactamente dónde buscar
✅ **Ahorro de Tiempo**: No necesitas leer todo el PDF
✅ **Navegación Rápida**: Un click te lleva a la página correcta
✅ **Contexto Visual**: Ves previsualizaciones de cada ubicación
✅ **Multi-ubicación**: Si aparece en varias páginas, las ves todas
✅ **Experiencia Fluida**: Todo integrado en la interfaz

## 📱 Responsive Design

- En **desktop**: Grid de 2 columnas para ubicaciones
- En **móvil**: Stack vertical con tarjetas completas
- Botones adaptables al tamaño de pantalla
- Chips que se ajustan con flex-wrap

## 🚀 Próximas Mejoras Posibles

- [ ] **Highlight del texto** en el PDF al abrirlo
- [ ] **Scroll automático** a la línea exacta
- [ ] **Visor de PDF integrado** sin abrir nueva pestaña
- [ ] **Exportar ubicaciones** a JSON/CSV
- [ ] **Comparación entre páginas** lado a lado
- [ ] **Historial de búsquedas** con ubicaciones guardadas
- [ ] **Anotaciones** en las páginas encontradas

## 🎓 Cómo Usar

### Paso 1: Inicia el Sistema
```powershell
# Terminal 1 - Backend
cd backend
python main.py

# Terminal 2 - Frontend
cd frontend_new
npm run dev
```

### Paso 2: Sube y Consulta
1. Sube tu PDF
2. Selecciónalo de la lista
3. Haz una pregunta

### Paso 3: Explora las Ubicaciones
- 📄 Ve las páginas donde está la respuesta
- 📝 Lee las previsualizaciones
- 🔗 Click en "Abrir" para ver el PDF completo
- 💡 Usa los chips para navegar entre páginas

## 🎉 Resultado Final

Ahora tienes un **sistema de consulta de PDFs inteligente** que no solo responde tus preguntas, sino que **te muestra exactamente dónde encontrar la información** en el documento original.

¡Es como tener un asistente que te señala con el dedo las páginas importantes! 👆📄✨
