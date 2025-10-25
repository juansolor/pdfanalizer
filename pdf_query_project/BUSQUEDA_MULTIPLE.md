# 🔍 Búsqueda en Múltiples PDFs

## 📋 Nueva Funcionalidad Implementada

La aplicación ahora permite **buscar en múltiples PDFs simultáneamente**, comparando información entre documentos y encontrando datos sin necesidad de saber qué PDF específico contiene la información.

---

## 🎯 Características Principales

### 1. **Búsqueda Individual** (Modo Clásico)
- Selecciona un PDF específico del dropdown
- Realiza consultas enfocadas en un solo documento
- Muestra ubicaciones exactas con páginas y previews

### 2. **Búsqueda en Todos los PDFs**
- Checkbox: "🔍 Buscar en todos los PDFs"
- Busca automáticamente en todos los documentos disponibles
- Ideal para encontrar información sin saber dónde está

### 3. **Búsqueda Selectiva Múltiple**
- Selecciona PDFs específicos con checkboxes
- Compara información entre documentos seleccionados
- Perfecto para comparar contratos, manuales, reportes, etc.

---

## 🚀 Cómo Usar

### **Opción 1: Buscar en Todos los PDFs**

1. ✅ Marca el checkbox "🔍 Buscar en todos los PDFs"
2. ✏️ Escribe tu pregunta
3. 🔍 Haz clic en "Hacer Pregunta"
4. 📊 Visualiza resultados organizados por documento

**Ejemplo:**
```
Pregunta: "¿Cuáles son las políticas de vacaciones?"

Resultados:
📄 Manual_Empleados.pdf - 15 coincidencias en 3 páginas
📄 Contrato_Laboral.pdf - 8 coincidencias en 2 páginas
📄 Politicas_RRHH.pdf - 22 coincidencias en 5 páginas
```

---

### **Opción 2: Búsqueda Selectiva**

1. ❌ Asegúrate que el checkbox "Buscar en todos" NO esté marcado
2. ✅ Selecciona los PDFs específicos que quieres buscar (checkboxes)
3. ✏️ Escribe tu pregunta
4. 🔍 Haz clic en "Hacer Pregunta"

**Ejemplo:**
```
Seleccionados:
✓ Presupuesto_2024.pdf
✓ Presupuesto_2023.pdf
✓ Presupuesto_2022.pdf

Pregunta: "¿Cuál fue el presupuesto de marketing?"

Resultados comparativos mostrando la evolución año a año
```

---

### **Opción 3: Búsqueda Individual**

1. ❌ Asegúrate que el checkbox "Buscar en todos" NO esté marcado
2. 📄 Selecciona UN PDF del dropdown
3. ✏️ Escribe tu pregunta
4. 🔍 Haz clic en "Hacer Pregunta"

**Comportamiento clásico** con ubicaciones detalladas y navegación directa a páginas.

---

## 📊 Visualización de Resultados

### Resultados Múltiples
Cada documento muestra:

- **📄 Nombre del archivo**
- **Badges de estadísticas:**
  - 🟣 Número de coincidencias
  - 🔵 Número de páginas con resultados
- **Páginas interactivas:** Haz clic en cualquier página para abrir el PDF
- **Vista previa:** Contexto de las primeras coincidencias
- **Comparación estadística:**
  - Documento más relevante
  - Documentos con/sin resultados
  - Promedio de coincidencias por documento

### Tarjetas por Documento

```
┌─────────────────────────────────────────┐
│ 📄 Documento.pdf                        │
│ [15 coincidencias] [3 páginas]          │
├─────────────────────────────────────────┤
│ Páginas: [Pág. 5] [Pág. 12] [Pág. 18]  │
│                                         │
│ 📍 Pág. 5                         [🔗]  │
│ "...contexto de la coincidencia..."    │
│                                         │
│ 📍 Pág. 12                        [🔗]  │
│ "...otro contexto relevante..."        │
└─────────────────────────────────────────┘
```

---

## 🎨 Características de UI

### Diseño Intuitivo
- ✅ **Checkbox principal** con fondo gradiente púrpura
- 📋 **Grid de checkboxes** para selección múltiple con hover effects
- 📊 **Contador de seleccionados** con badge verde
- 🎯 **Deshabilitado automático** de controles mutuamente excluyentes

### Resultados Visuales
- 🟣 **Badges de coincidencias** con gradiente púrpura
- 🔵 **Badges de páginas** con gradiente azul
- 📄 **Chips de página** interactivos con hover animations
- 📊 **Resumen comparativo** con fondo amarillo y estadísticas

### Responsive
- 📱 **Mobile-friendly**: Columnas únicas en pantallas pequeñas
- 💻 **Desktop optimizado**: Grids multi-columna para aprovechar espacio
- ✨ **Transiciones suaves** en todos los elementos

---

## 🔧 Implementación Técnica

### Backend (`/query-multiple`)

**Endpoint:** `POST /query-multiple`

**Request Body:**
```json
{
  "question": "¿Qué dice sobre las vacaciones?",
  "filenames": ["doc1.pdf", "doc2.pdf", "doc3.pdf"],
  "search_all": false
}
```

**Response:**
```json
{
  "answer": "Texto formateado con resultados por documento",
  "keywords": ["vacaciones", "días", "periodo"],
  "results": [
    {
      "filename": "doc1.pdf",
      "matches": 15,
      "pages_found": [5, 12, 18],
      "locations": [
        {
          "page": 5,
          "keywords": ["vacaciones"],
          "preview": "...contexto de 150 caracteres..."
        }
      ],
      "total_pages": 50
    }
  ],
  "total_matches": 42,
  "documents_found": 2,
  "comparison": {
    "most_relevant": "doc1.pdf",
    "documents_with_results": 2,
    "documents_without_results": 1,
    "average_matches_per_doc": 21.0
  }
}
```

### Función `search_multiple_pdfs()`

**Proceso:**
1. Analiza la pregunta una sola vez (optimización)
2. Extrae palabras clave relevantes
3. Itera sobre cada PDF seleccionado
4. Extrae texto página por página de cada PDF
5. Busca keywords en cada página
6. Agrupa resultados por documento y página
7. Ordena documentos por relevancia (más coincidencias primero)
8. Genera respuesta comparativa
9. Calcula estadísticas y métricas de comparación

**Optimizaciones:**
- ⚡ Análisis de pregunta único (no por cada PDF)
- 🔄 Continúa si un PDF falla (robustez)
- 📊 Máximo 3 páginas por documento en preview
- 🎯 Top 5 documentos más relevantes

---

## 📈 Casos de Uso

### 1. **Investigación Legal**
```
Pregunta: "¿Qué cláusulas mencionan indemnización?"
PDFs: Contrato_A.pdf, Contrato_B.pdf, Contrato_C.pdf

Resultado: Comparación de cláusulas entre contratos
```

### 2. **Análisis Financiero**
```
Pregunta: "¿Cuál fue el EBITDA del último trimestre?"
Buscar en todos: ✓

Resultado: Información de todos los reportes trimestrales
```

### 3. **Estudio Académico**
```
Pregunta: "¿Qué papers mencionan machine learning?"
PDFs: Paper1.pdf, Paper2.pdf, Paper3.pdf, Paper4.pdf

Resultado: Referencias cruzadas entre investigaciones
```

### 4. **Compliance y Auditoría**
```
Pregunta: "¿Dónde se menciona GDPR o protección de datos?"
Buscar en todos: ✓

Resultado: Todos los documentos que referencian normativas
```

### 5. **Gestión de Proyectos**
```
Pregunta: "¿Cuáles son los entregables del Q1?"
PDFs: Plan_Proyecto.pdf, Roadmap_2024.pdf, Sprints_Q1.pdf

Resultado: Consolidación de información de planificación
```

---

## 🎯 Ventajas vs Búsqueda Individual

| Característica | Individual | Múltiple |
|---------------|-----------|----------|
| **Velocidad** | Rápido en 1 doc | Busca N docs en una consulta |
| **Alcance** | Limitado a 1 PDF | Toda la biblioteca |
| **Comparación** | No disponible | Automática entre docs |
| **Desconocimiento** | Debes saber dónde buscar | Encuentra sin saber dónde |
| **Análisis** | Profundo en 1 doc | Amplio en múltiples |
| **Uso ideal** | Lectura detallada | Research & Discovery |

---

## 💡 Tips y Mejores Prácticas

### ✅ Hacer

- ✅ Usa "Buscar en todos" cuando NO sepas dónde está la info
- ✅ Selecciona PDFs específicos para comparaciones directas
- ✅ Haz preguntas concisas y específicas
- ✅ Revisa el resumen comparativo para identificar el doc más relevante
- ✅ Haz clic en los chips de página para ver contexto completo

### ❌ Evitar

- ❌ Combinar búsqueda individual con checkboxes múltiples (está deshabilitado)
- ❌ Preguntas demasiado genéricas en búsqueda múltiple
- ❌ Seleccionar PDFs irrelevantes (aumenta tiempo de procesamiento)
- ❌ Ignorar el documento "más relevante" del resumen

---

## 🔮 Próximas Mejoras Planificadas

### Sprint 1 Completado ✅
- [x] Endpoint `/query-multiple`
- [x] Función `search_multiple_pdfs()`
- [x] UI con checkboxes y toggle
- [x] Visualización de resultados por documento
- [x] Comparación estadística

### Sprint 2 (Próximo)
- [ ] Base de datos SQLite para caché
- [ ] Búsqueda más rápida con resultados cacheados
- [ ] Filtros avanzados (por fecha, tamaño, etc.)
- [ ] Export de resultados comparativos a Excel/PDF

### Sprint 3 (Futuro)
- [ ] Búsqueda semántica con embeddings
- [ ] Gráficos de comparación visual
- [ ] Timeline de información entre documentos
- [ ] Resumen automático de diferencias

---

## 🧪 Cómo Probar

### Test 1: Búsqueda en Todos
1. Sube 3+ PDFs diferentes
2. Marca "Buscar en todos los PDFs"
3. Pregunta: "¿Qué información hay sobre [tema común]?"
4. Verifica que aparecen resultados de múltiples documentos

### Test 2: Comparación Selectiva
1. Sube PDFs relacionados (ej: reportes anuales)
2. Selecciona 2-3 PDFs con checkboxes
3. Pregunta: "¿Cuáles son las cifras principales?"
4. Compara resultados entre documentos

### Test 3: Sin Resultados
1. Busca en todos los PDFs
2. Pregunta algo que NO esté en ningún documento
3. Verifica mensaje: "No encontré información relacionada..."

### Test 4: Un Solo Resultado
1. Pregunta muy específica de un solo PDF
2. Verifica que solo un documento aparece con resultados
3. Verifica estadísticas: "1 documento con resultados"

---

## 📱 Interfaz de Usuario

### Estados de los Controles

**Cuando "Buscar en todos" está ACTIVADO:**
- ✅ Checkbox "Buscar en todos" marcado con fondo gradiente
- ⛔ Dropdown individual deshabilitado
- ⛔ Checkboxes múltiples ocultos
- ✅ Input de pregunta habilitado
- ✅ Botón de búsqueda habilitado

**Cuando checkboxes múltiples están SELECCIONADOS:**
- ⛔ Dropdown individual deshabilitado
- ✅ Checkboxes múltiples habilitados
- ✅ Contador de seleccionados visible con badge verde
- ✅ Input de pregunta habilitado
- ✅ Botón de búsqueda habilitado

**Cuando dropdown individual está SELECCIONADO:**
- ✅ Dropdown con PDF seleccionado
- ⛔ Checkboxes múltiples deshabilitados
- ✅ Input de pregunta habilitado
- ✅ Botón de búsqueda habilitado

---

## 🎨 Código de Colores

### Badges y Estados
- 🟣 **Púrpura** (#667eea - #764ba2): Coincidencias y páginas principales
- 🔵 **Azul** (#4facfe - #00f2fe): Número de páginas y botones de acción
- 🟢 **Verde** (#48bb78): Contador de seleccionados
- 🟡 **Amarillo** (#faf089): Resumen comparativo y estadísticas
- ⚪ **Blanco**: Fondo de tarjetas y chips

### Gradientes
- **Principal**: 135deg, #667eea → #764ba2
- **Acción**: 135deg, #4facfe → #00f2fe
- **Éxito**: 135deg, #48bb78 → #38a169
- **Atención**: 135deg, #faf089 → #f6e05e

---

## 🔐 Consideraciones de Rendimiento

### Optimizaciones Implementadas
- ⚡ **Análisis único de pregunta**: No repite análisis por cada PDF
- 📊 **Límites de resultados**: Máx 3 páginas preview por doc, top 5 docs
- 🔄 **Manejo de errores**: Continúa si un PDF falla
- 💾 **Memoria eficiente**: Procesa PDFs secuencialmente, no en paralelo

### Tiempos Estimados
- **1-3 PDFs**: < 3 segundos
- **4-10 PDFs**: 3-8 segundos
- **10-20 PDFs**: 8-15 segundos
- **20+ PDFs**: 15-30 segundos

*Nota: Depende del tamaño de los PDFs y complejidad de la pregunta*

---

## 🐛 Troubleshooting

### Problema: "No encontré información"
**Solución:**
- Verifica que las palabras clave estén en los PDFs
- Intenta reformular la pregunta
- Revisa que los PDFs tengan texto extraíble (no sean solo imágenes)

### Problema: Búsqueda muy lenta
**Solución:**
- Reduce el número de PDFs seleccionados
- Usa búsqueda individual para documentos grandes
- Considera implementar caché (Sprint 2)

### Problema: Checkboxes no responden
**Solución:**
- Limpia la selección del dropdown individual
- Desmarca "Buscar en todos los PDFs"
- Recarga la lista de PDFs

---

## 📚 Referencias

- **Backend**: `d:\PDFviewer\pdf_query_project\backend\main.py`
  - Función: `search_multiple_pdfs()` (líneas ~298-415)
  - Endpoint: `/query-multiple` (líneas ~613-650)
  - Modelo: `MultiQueryRequest` (líneas ~59-62)

- **Frontend**: `d:\PDFviewer\pdf_query_project\frontend_new\src\App.jsx`
  - Estados: líneas 36-39
  - Función búsqueda: `handleQuery()` (líneas ~120-190)
  - UI multi-search: líneas ~280-350
  - Resultados múltiples: líneas ~410-520

- **Estilos**: `d:\PDFviewer\pdf_query_project\frontend_new\src\App.css`
  - Multi-search: líneas ~703-1020

---

## 🎉 ¡Listo para Usar!

La búsqueda en múltiples PDFs está **completamente implementada y lista para producción**.

### Comandos para iniciar:

**Backend:**
```powershell
cd d:\PDFviewer\pdf_query_project\backend
.\venv\Scripts\Activate.ps1
python main.py
```

**Frontend:**
```powershell
cd d:\PDFviewer\pdf_query_project\frontend_new
npm run dev
```

**O usa el script de red local:**
```powershell
cd d:\PDFviewer\pdf_query_project
.\start-network.ps1
```

---

## 📞 Soporte

¿Preguntas o problemas? Consulta:
- 📖 **ANALISIS_Y_MEJORAS.md** - Análisis completo de la app
- 📖 **GUIA_RAPIDA.md** - Guía de inicio rápido
- 📖 **NUEVA_FUNCIONALIDAD.md** - Ubicaciones de página
- 📖 **ACCESO_RED_LOCAL.md** - Configuración de red

---

**Versión:** 2.0.0 - Multi-PDF Search  
**Fecha:** 2024  
**Autor:** PDF Query System Team  
**Estado:** ✅ Producción
