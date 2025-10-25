# 🗄️ Documentación de Base de Datos SQLite

## 📋 Resumen

La aplicación ahora utiliza **SQLite** con **SQLAlchemy** para persistir datos, incluyendo metadata de PDFs, historial de consultas, índices de búsqueda y estadísticas de uso.

---

## 🎯 Características Implementadas

### ✅ 1. Persistencia de Metadata de PDFs
- Nombre de archivo, ruta, tamaño
- Total de páginas
- Texto completo extraído
- Texto por páginas (JSON)
- Word count y palabras únicas
- Tags y categorías
- Fecha de subida y último acceso
- Contador de accesos

### ✅ 2. Historial de Consultas
- Pregunta realizada
- PDF(s) consultado(s)
- Tipo de búsqueda (single, multiple, all)
- Keywords encontradas
- Total de coincidencias
- Tiempo de ejecución
- Respuesta generada
- Fecha de consulta

### ✅ 3. Índice de Búsqueda
- Palabra indexada
- PDF y página donde aparece
- Número de ocurrencias
- Contextos (primeros 3)
- Fecha de indexación

### ✅ 4. Estadísticas de Uso
- Contadores diarios de consultas, uploads
- Promedios de tiempo y coincidencias
- PDFs más consultados
- Keywords más comunes
- Distribución por tipo de búsqueda

---

## 📊 Modelos de Datos

### PDFDocument

```python
{
    "id": int,
    "filename": str,           # Nombre del archivo
    "original_filename": str,
    "file_path": str,
    "file_size": int,          # En bytes
    "total_pages": int,
    
    # Metadata
    "upload_date": datetime,
    "last_accessed": datetime,
    "access_count": int,
    
    # Categorización
    "tags": List[str],         # JSON
    "category": str,
    "description": str,
    
    # Índice de contenido
    "full_text": str,          # Texto completo
    "text_by_pages": Dict,     # JSON {page_num: text}
    
    # Estadísticas
    "word_count": int,
    "unique_words": int,
    
    # Flags
    "is_indexed": bool,
    "is_searchable": bool
}
```

### QueryHistory

```python
{
    "id": int,
    "question": str,
    
    # Contexto
    "pdf_filename": str,       # NULL si múltiple
    "multiple_pdfs": List[str], # JSON
    "search_type": str,        # "single", "multiple", "all"
    
    # Resultados
    "keywords_found": List[str], # JSON
    "total_matches": int,
    "documents_found": int,
    "execution_time": float,   # En segundos
    
    # Respuesta
    "answer": str,
    "results": Dict,           # JSON completo
    
    # Timestamp
    "query_date": datetime,
    
    # Feedback
    "user_rating": int,        # 1-5 estrellas
    "was_helpful": bool
}
```

### SearchIndex

```python
{
    "id": int,
    "word": str,               # Palabra indexada
    "pdf_id": int,             # FK a PDFDocument
    "pdf_filename": str,
    
    # Ubicaciones
    "page_numbers": List[int], # JSON
    "occurrences": int,
    "contexts": List[str],     # JSON (primeros 3)
    
    "indexed_date": datetime
}
```

### UsageStatistics

```python
{
    "id": int,
    "date": datetime,
    
    # Contadores
    "total_queries": int,
    "total_uploads": int,
    "total_pdfs": int,
    
    # Promedios
    "avg_query_time": float,
    "avg_matches_per_query": float,
    
    # Top items
    "most_queried_pdf": str,
    "most_common_keywords": Dict, # JSON {keyword: count}
    
    # Tipos de búsqueda
    "single_searches": int,
    "multiple_searches": int,
    "all_searches": int
}
```

---

## 🚀 Instalación

### 1. Instalar Dependencias

```powershell
cd d:\PDFviewer\pdf_query_project\backend
.\venv\Scripts\Activate.ps1
pip install sqlalchemy==2.0.23 alembic==1.13.1
```

O usar el script automático:

```powershell
.\install-db.ps1
```

### 2. La base de datos se crea automáticamente

Al importar `database.py`, se ejecuta automáticamente `init_db()` que crea:
- Archivo: `backend/pdfs_database.db`
- Tablas: `pdf_documents`, `query_history`, `search_index`, `usage_statistics`

---

## 📖 Uso de la Base de Datos

### En los Endpoints

Todos los endpoints que necesitan BD reciben `db: Session = Depends(get_db)`:

```python
@app.get("/list-pdfs")
async def list_pdfs(db: Session = Depends(get_db)):
    pdfs = db_svc.get_all_pdfs(db)
    return {"pdfs": [pdf.filename for pdf in pdfs]}
```

### Funciones de Servicio (`db_services.py`)

#### PDFs

```python
# Crear PDF
pdf = db_svc.create_pdf_document(db, filename, file_path, file_size, total_pages)

# Obtener PDF
pdf = db_svc.get_pdf_by_filename(db, "document.pdf")

# Listar todos
pdfs = db_svc.get_all_pdfs(db)

# Actualizar acceso
db_svc.update_pdf_access(db, "document.pdf")

# Actualizar texto
db_svc.update_pdf_text(db, "document.pdf", full_text, text_by_pages)

# Agregar tags
db_svc.add_pdf_tags(db, "document.pdf", ["legal", "contrato"])

# Establecer categoría
db_svc.set_pdf_category(db, "document.pdf", "Legal")

# Eliminar
db_svc.delete_pdf_document(db, "document.pdf")

# Buscar
pdfs = db_svc.search_pdfs(db, query="contrato", category="Legal", tags=["important"])
```

#### Historial

```python
# Crear consulta
query = db_svc.create_query_history(
    db, question="¿Qué dice sobre vacaciones?",
    pdf_filename="manual.pdf",
    search_type="single",
    keywords_found=["vacaciones", "días"],
    total_matches=5,
    execution_time=1.23,
    answer="...",
    results={...}
)

# Consultas recientes
queries = db_svc.get_recent_queries(db, limit=20)

# Consultas de un PDF
queries = db_svc.get_queries_by_pdf(db, "manual.pdf")

# Consultas populares
popular = db_svc.get_popular_queries(db, limit=10)

# Calificar consulta
db_svc.rate_query(db, query_id=1, rating=5, was_helpful=True)
```

#### Estadísticas

```python
# Incrementar contador de consultas
db_svc.increment_query_count(db, query_time=1.5, matches=10, search_type="single")

# Incrementar uploads
db_svc.increment_upload_count(db)

# Actualizar keywords
db_svc.update_top_keywords(db, ["vacaciones", "salario"])

# Resumen de N días
stats = db_svc.get_statistics_summary(db, days=7)

# Estadísticas de PDF
stats = db_svc.get_pdf_statistics(db, "manual.pdf")

# Dashboard completo
dashboard = db_svc.get_dashboard_data(db)
```

---

## 🆕 Nuevos Endpoints

### 📊 Estadísticas

```bash
# Historial de consultas
GET /api/history?limit=20

# Estadísticas de uso (últimos N días)
GET /api/statistics?days=7

# Dashboard completo
GET /api/dashboard

# Estadísticas de un PDF
GET /api/pdf/{filename}/stats

# Consultas populares
GET /api/popular-queries?limit=10
```

### 🏷️ Gestión de PDFs

```bash
# Agregar tags
POST /api/pdf/{filename}/tags
Body: ["tag1", "tag2", "tag3"]

# Establecer categoría
POST /api/pdf/{filename}/category
Body: "Legal"

# Eliminar PDF
DELETE /api/pdf/{filename}
```

### 📄 Listado Mejorado

```bash
# Listar PDFs con metadata completa
GET /list-pdfs

Response:
{
  "pdfs": ["doc1.pdf", "doc2.pdf"],
  "detailed": [
    {
      "filename": "doc1.pdf",
      "upload_date": "2024-01-01T10:00:00",
      "file_size": 1024000,
      "total_pages": 50,
      "access_count": 10,
      "tags": ["legal", "contrato"],
      "category": "Legal"
    }
  ]
}
```

---

## 📈 Ejemplos de Uso

### Ejemplo 1: Upload con BD

```python
# Automático en /upload-pdf
# 1. Sube archivo
# 2. Extrae texto y metadata
# 3. Guarda en BD
# 4. Incrementa estadísticas
```

### Ejemplo 2: Consulta con Historial

```python
# Automático en /query
# 1. Realiza consulta
# 2. Guarda en historial
# 3. Actualiza acceso del PDF
# 4. Actualiza estadísticas
# 5. Actualiza keywords
```

### Ejemplo 3: Dashboard

```javascript
// Frontend
const response = await axios.get(`${API_URL}/api/dashboard`)

console.log(response.data)
/*
{
  "total_pdfs": 25,
  "total_queries": 150,
  "recent_queries": [...],
  "stats_7days": {
    "total_queries": 45,
    "avg_query_time": 1.2,
    "avg_matches": 8.5
  },
  "popular_queries": [...],
  "most_accessed_pdfs": [...]
}
*/
```

---

## 🔍 Consultas Directas

### Ver PDFs en BD

```python
python
>>> from database import SessionLocal
>>> from database import PDFDocument
>>> db = SessionLocal()
>>> pdfs = db.query(PDFDocument).all()
>>> for pdf in pdfs:
...     print(f"{pdf.filename} - {pdf.total_pages} páginas")
```

### Ver Historial

```python
>>> from database import QueryHistory
>>> queries = db.query(QueryHistory).order_by(QueryHistory.query_date.desc()).limit(5).all()
>>> for q in queries:
...     print(f"{q.question[:50]} - {q.total_matches} matches")
```

### Estadísticas

```python
>>> from database import UsageStatistics
>>> stats = db.query(UsageStatistics).order_by(UsageStatistics.date.desc()).first()
>>> print(f"Consultas hoy: {stats.total_queries}")
>>> print(f"PDFs totales: {stats.total_pdfs}")
```

---

## 🛠️ Mantenimiento

### Resetear Base de Datos

```python
python
>>> from database import reset_db
>>> reset_db()
# ⚠️ ELIMINA TODOS LOS DATOS
```

### Backup

```powershell
# Copiar base de datos
Copy-Item pdfs_database.db pdfs_database_backup.db
```

### Ver con SQLite Browser

1. Descargar: https://sqlitebrowser.org/
2. Abrir: `backend/pdfs_database.db`
3. Explorar tablas y datos

---

## 📊 Ventajas de la Base de Datos

### Antes (Sin BD)
- ❌ Procesar PDF completo en cada consulta
- ❌ Sin historial de consultas
- ❌ Sin estadísticas de uso
- ❌ Sin metadata de PDFs
- ❌ Sin caché

### Ahora (Con BD)
- ✅ Texto extraído se guarda (no re-procesar)
- ✅ Historial completo de todas las consultas
- ✅ Estadísticas detalladas de uso
- ✅ Metadata rica de cada PDF
- ✅ Base para futuro caché e índices
- ✅ Dashboard con métricas

---

## 🚀 Próximas Mejoras

### Sprint 3+ (Futuro)

1. **Índice de Búsqueda Completo**
   - Indexar automáticamente al subir PDF
   - Búsquedas 10x más rápidas
   - Full-text search

2. **Caché de Resultados**
   - Guardar resultados de consultas frecuentes
   - Retornar instantáneamente si ya se consultó

3. **Análisis Avanzado**
   - Trending keywords
   - Análisis de sentiment
   - Correlaciones entre documentos

4. **Migraciones con Alembic**
   - Versionado de esquema
   - Actualizaciones sin perder datos

---

## 🐛 Troubleshooting

### Error: "No module named 'sqlalchemy'"

```powershell
pip install sqlalchemy==2.0.23 alembic==1.13.1
```

### Error: "Database is locked"

SQLite tiene un solo escritor. Si ves este error:
- Cierra otras conexiones a la BD
- Reinicia el servidor

### Ver logs de SQL

En `database.py`, cambia:

```python
engine = create_engine(DATABASE_URL, echo=True)  # Muestra SQL
```

---

## 📁 Archivos Creados

```
backend/
├── database.py          # Modelos y configuración
├── db_services.py       # Funciones CRUD
├── pdfs_database.db     # Base de datos SQLite
├── install-db.ps1       # Script de instalación
└── main.py              # Integración en endpoints
```

---

## 📞 Soporte

**Documentación relacionada:**
- `BUSQUEDA_MULTIPLE.md` - Búsqueda multi-PDF
- `CHANGELOG_MULTISEARCH.md` - Changelog v2.0
- `ANALISIS_Y_MEJORAS.md` - Análisis completo

**Estado:** ✅ Implementado y funcional

**Versión:** 2.1.0 - SQLite Integration

---

## 🎉 Resumen

La integración de SQLite transforma la aplicación de una herramienta simple a una **plataforma completa de gestión documental** con:

- ✅ Persistencia de datos
- ✅ Historial completo
- ✅ Estadísticas avanzadas
- ✅ Metadata rica
- ✅ Base para optimizaciones futuras

**¡La aplicación ahora tiene "memoria"! 🧠💾**
