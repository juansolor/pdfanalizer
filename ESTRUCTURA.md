# 📁 Estructura del Proyecto - PDF Query System v2.2.1

## 🎯 Organización Limpia y Profesional

```
pdfanalizer/
│
├── 📄 README.md                    # Documentación principal
├── 📘 GUIA_RAPIDA.md               # Tutorial rápido de uso
├── 📚 INDICE.md                    # Índice de toda la documentación
├── 🚀 START.ps1                    # Script inicio rápido (localhost)
├── 🌐 start-network.ps1            # Script inicio red local
├── 🔒 .gitignore                   # Archivos ignorados por git
│
├── 📂 backend/                     # ⚙️ Backend FastAPI + Python
│   ├── main.py                     # 🎯 Aplicación principal (33 endpoints)
│   ├── database.py                 # 💾 Modelos SQLAlchemy (4 tablas)
│   ├── db_services.py              # 🔧 CRUD y lógica de negocio
│   ├── cache_manager.py            # ⚡ Sistema de cache inteligente
│   ├── fts_search.py               # 🔍 Full-Text Search (FTS5)
│   ├── analytics.py                # 📊 Analytics y estadísticas
│   ├── translator.py               # 🌐 Traducción DE↔EN (232 palabras)
│   ├── init_systems.py             # 🔄 Inicialización de sistemas
│   │
│   ├── requirements.txt            # 📦 Dependencias Python
│   ├── .env                        # 🔐 Variables de entorno
│   ├── pdfs_database.db            # 💾 Base de datos SQLite
│   │
│   ├── 📂 pdfs/                    # 📄 PDFs subidos por usuarios
│   ├── 📂 results/                 # 📊 Resultados de procesamiento
│   ├── 📂 venv/                    # 🐍 Entorno virtual Python
│   └── 📂 __pycache__/             # 🗂️ Cache de Python compilado
│
├── 📂 frontend/                    # 🎨 Frontend React + Vite
│   ├── 📂 src/
│   │   ├── App.jsx                 # ⚛️ Componente principal
│   │   ├── App.css                 # 🎨 Estilos principales
│   │   ├── main.jsx                # 🚪 Punto de entrada React
│   │   └── 📂 assets/              # 🖼️ Imágenes y recursos
│   │
│   ├── 📂 public/                  # 🌐 Archivos públicos estáticos
│   ├── package.json                # 📦 Dependencias Node.js
│   ├── package-lock.json           # 🔒 Versiones exactas de paquetes
│   ├── vite.config.js              # ⚙️ Configuración de Vite
│   ├── index.html                  # 🌐 HTML principal
│   └── .gitignore                  # 🔒 Ignorados de git frontend
│
└── 📂 docs/                        # 📚 Documentación completa
    ├── CHECKLIST_MEJORAS.md        # ✅ Estado implementación (73%)
    ├── TRADUCTOR.md                # 🌐 Sistema de traducción
    ├── DATABASE.md                 # 💾 Estructura de BD
    ├── CACHE_FTS_ANALYTICS.md      # ⚡ Cache y FTS
    ├── ANALISIS_Y_MEJORAS.md       # 📊 Análisis completo
    ├── BUSQUEDA_MULTIPLE.md        # 🔍 Búsqueda multi-PDF
    ├── CHANGELOG_v2.2.md           # 📝 Cambios v2.2
    ├── INSTALACION_v2.2.md         # 🔧 Guía de instalación
    ├── RESUMEN_EJECUTIVO.md        # 📊 Overview ejecutivo
    ├── EJEMPLOS_USO.md             # 💡 Casos de uso
    ├── NUEVA_FUNCIONALIDAD.md      # 🆕 Nuevas features
    ├── GITHUB_INSTRUCTIONS.md      # 🐙 Instrucciones GitHub
    ├── ACCESO_RED_LOCAL.md         # 🌐 Config red local
    └── ... (más documentos)
```

## 📊 Estadísticas

| Categoría | Cantidad | Detalles |
|-----------|----------|----------|
| **Total Archivos Python** | 8 | main.py, database.py, db_services.py, cache_manager.py, fts_search.py, analytics.py, translator.py, init_systems.py |
| **Total Líneas Backend** | ~3,500 | Código Python |
| **Total Endpoints API** | 33 | FastAPI REST |
| **Documentos Markdown** | 22+ | En /docs |
| **Tablas Base de Datos** | 4 | SQLite |
| **Módulos Principales** | 7 | Backend modular |

## 🎯 Archivos Clave por Funcionalidad

### 🔍 Búsqueda y Consultas
- `backend/main.py` - Endpoints de consulta (líneas 200-600)
- `backend/db_services.py` - Lógica de búsqueda
- `backend/fts_search.py` - Full-Text Search
- `frontend/src/App.jsx` - UI de búsqueda

### 💾 Base de Datos
- `backend/database.py` - Modelos SQLAlchemy
- `backend/pdfs_database.db` - SQLite database
- `backend/db_services.py` - CRUD operations

### ⚡ Performance
- `backend/cache_manager.py` - Sistema de caché
- `backend/fts_search.py` - Índice FTS5

### 📊 Analytics
- `backend/analytics.py` - 8 funciones de análisis
- `backend/main.py` - Endpoints analytics (líneas 1100-1200)

### 🌐 Traducción
- `backend/translator.py` - 232 palabras DE↔EN
- `backend/main.py` - 5 endpoints traducción (líneas 1250-1400)

### 🎨 Frontend
- `frontend/src/App.jsx` - Componente principal React
- `frontend/src/App.css` - Estilos y animaciones
- `frontend/index.html` - HTML base

## 📦 Dependencias Principales

### Backend (`backend/requirements.txt`)
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
python-multipart==0.0.6
PyPDF2==3.0.1
python-dotenv==1.0.0
```

### Frontend (`frontend/package.json`)
```json
{
  "react": "^18.3.1",
  "react-dom": "^18.3.1",
  "axios": "^1.6.2",
  "vite": "^5.0.8"
}
```

## 🚀 Scripts de Inicio

### Windows
```powershell
# Inicio local
.\START.ps1

# Inicio red local (acceso desde otros dispositivos)
.\start-network.ps1
```

### Backend Manual
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Frontend Manual
```bash
cd frontend
npm install
npm run dev
```

## 📁 Carpetas Generadas en Tiempo de Ejecución

### Backend
- `backend/pdfs/` - PDFs subidos por usuarios (creada automáticamente)
- `backend/results/` - Resultados temporales (opcional)
- `backend/venv/` - Entorno virtual Python (crear con `python -m venv venv`)
- `backend/__pycache__/` - Cache Python (auto-generada)

### Frontend
- `frontend/node_modules/` - Dependencias Node.js (crear con `npm install`)
- `frontend/dist/` - Build de producción (crear con `npm run build`)

## 🗄️ Base de Datos SQLite

### Archivo
`backend/pdfs_database.db` (aprox. 5MB por 100 PDFs)

### Tablas
1. **pdf_documents** - Metadata de PDFs (14 columnas)
2. **query_history** - Historial de consultas (12 columnas)
3. **search_index** - Índice invertido (7 columnas)
4. **usage_statistics** - Estadísticas de uso (11 columnas)

Ver `docs/DATABASE.md` para detalles completos.

## 📝 Convenciones de Nombres

### Archivos Python
- `snake_case.py` - Módulos
- `PascalCase` - Clases
- `snake_case()` - Funciones

### Archivos Frontend
- `PascalCase.jsx` - Componentes React
- `camelCase.js` - Utilidades
- `kebab-case.css` - Estilos

### Documentación
- `MAYUSCULAS.md` - Docs importantes
- `PascalCase.md` - Docs técnicos

## 🔐 Archivos Sensibles (No en Git)

```
.gitignore incluye:
├── backend/.env                 # Variables de entorno
├── backend/venv/                # Entorno virtual
├── backend/__pycache__/         # Cache Python
├── backend/pdfs/                # PDFs subidos
├── backend/pdfs_database.db     # Base de datos
├── frontend/node_modules/       # Dependencias Node
└── frontend/dist/               # Build frontend
```

## 📊 Tamaños Aproximados

| Item | Tamaño | Notas |
|------|--------|-------|
| Backend código | ~500 KB | 8 archivos Python |
| Frontend código | ~200 KB | React + CSS |
| Documentación | ~300 KB | 22+ archivos MD |
| Base de datos | ~5 MB | Por 100 PDFs |
| Venv Python | ~50 MB | Incluye dependencias |
| node_modules | ~200 MB | Dependencias Node |
| PDFs subidos | Variable | Por usuario |

## 🎯 Próximos Cambios Estructurales

### v2.3 (Planeado)
- `backend/api/` - Separar endpoints en módulos
- `backend/services/` - Lógica de negocio separada
- `backend/models/` - Modelos en archivos separados
- `frontend/components/` - Componentes React separados
- `frontend/hooks/` - Custom hooks

### v3.0 (Futuro)
- `backend/auth/` - Sistema de autenticación
- `backend/ai/` - Integración con IA
- `backend/ocr/` - Sistema OCR
- `tests/` - Tests automatizados
- `docker/` - Dockerización

## ✅ Limpieza Realizada

### ❌ Eliminado
- ✅ Carpeta `pdf_query_project/` duplicada
- ✅ Archivos `.md` duplicados en raíz
- ✅ Carpeta `backend_old/` obsoleta
- ✅ `.git` anidado en `pdf_query_project/`

### ✅ Reorganizado
- ✅ Toda la documentación → `docs/`
- ✅ Backend actualizado → `backend/`
- ✅ Frontend actualizado → `frontend/`
- ✅ Archivos principales en raíz
- ✅ Scripts de inicio en raíz

## 📞 Referencias Rápidas

| Necesito... | Ver archivo... |
|-------------|----------------|
| Empezar rápido | `GUIA_RAPIDA.md` |
| Ver toda la doc | `INDICE.md` |
| Estructura BD | `docs/DATABASE.md` |
| API endpoints | `docs/CACHE_FTS_ANALYTICS.md` |
| Traducción | `docs/TRADUCTOR.md` |
| Estado proyecto | `docs/CHECKLIST_MEJORAS.md` |
| Instalar v2.2 | `docs/INSTALACION_v2.2.md` |

---

**Estructura reorganizada:** Octubre 2025  
**Versión:** v2.2.1  
**Total archivos:** ~150+ (incluyendo dependencias)  
**Líneas de código:** ~5,000+ (backend + frontend)
