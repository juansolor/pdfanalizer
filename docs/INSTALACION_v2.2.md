# 🚀 INSTALACIÓN Y CONFIGURACIÓN v2.2

## 📋 Pre-requisitos

- Python 3.8+ instalado
- pip instalado
- SQLite (incluido en Python)
- Git (para clonar repositorio)

---

## 🔧 Instalación desde Cero

### 1. Clonar Repositorio
```powershell
git clone https://github.com/juansolor/pdfanalizer
cd pdfanalizer
```

### 2. Configurar Backend

```powershell
cd backend

# Crear entorno virtual (opcional pero recomendado)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```

**requirements.txt debe incluir:**
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
PyPDF2==3.0.1
python-dotenv==1.0.0
sqlalchemy==2.0.23
alembic==1.13.1
```

### 3. Inicializar Base de Datos

**Opción A: Script Automático** (Recomendado)
```powershell
python init_systems.py
```

**Opción B: Manual**
```python
# Abrir Python interactivo
python

# Ejecutar:
from database import init_db
from database import get_db
import fts_search as fts
import db_services as db_svc

# 1. Inicializar DB
init_db()
print("✅ DB inicializada")

# 2. Inicializar FTS
db = next(get_db())
fts.init_fts_tables(db)
print("✅ FTS inicializado")

# 3. Indexar PDFs existentes (si hay)
pdfs = db_svc.get_all_pdfs(db)
for pdf in pdfs:
    if pdf.text_by_pages and pdf.is_indexed:
        fts.index_pdf_for_fts(db, pdf.id, pdf.filename, pdf.text_by_pages)
        print(f"📄 {pdf.filename} indexado")

db.close()
print("✅ Setup completo")
exit()
```

### 4. Configurar Variables de Entorno

Crear archivo `.env` en `backend/`:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True
RELOAD=True

# CORS (para desarrollo local y red local)
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# File Upload
MAX_FILE_SIZE=50
UPLOAD_FOLDER=pdfs
RESULTS_FOLDER=results

# Logging
FILTER_404_LOGS=True
LOG_LEVEL=info
```

### 5. Iniciar Backend

```powershell
python main.py
```

**Output esperado:**
```
🚀 Iniciando servidor en http://0.0.0.0:8000
📁 Directorio de PDFs: D:\PDFviewer\pdf_query_project\backend\pdfs
📊 Directorio de resultados: D:\PDFviewer\pdf_query_project\backend\results
🌐 CORS habilitado para: http://localhost:3000, http://127.0.0.1:3000
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 6. Configurar Frontend

```powershell
cd ..\frontend_new

# Instalar dependencias
npm install

# Iniciar frontend
npm run dev
```

**Output esperado:**
```
VITE v7.1.14  ready in 1234 ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: http://192.168.1.100:3000/
```

---

## ✅ Verificación de Instalación

### 1. Probar Backend

```powershell
# Health check
curl http://localhost:8000/health

# Listar PDFs
curl http://localhost:8000/list-pdfs

# Cache stats
curl http://localhost:8000/api/cache/stats

# FTS stats
curl http://localhost:8000/api/fts/stats

# Analytics dashboard
curl http://localhost:8000/api/analytics/dashboard?days=7
```

### 2. Probar Frontend

Abrir navegador en:
- Local: http://localhost:3000
- Red local: http://TU_IP:3000 (ejemplo: http://192.168.1.100:3000)

---

## 🔄 Actualización desde v2.1

### Si ya tienes v2.1 instalado:

```powershell
# 1. Pull cambios
git pull origin main

# 2. Activar venv (si usas)
cd backend
.\venv\Scripts\Activate.ps1

# 3. Verificar dependencias (ya deberían estar)
pip list | Select-String -Pattern "sqlalchemy|alembic"

# 4. Inicializar sistemas nuevos
python init_systems.py

# 5. Reiniciar servidor
python main.py
```

**NO se requiere reinstalar dependencias** - SQLAlchemy y Alembic ya estaban en v2.1.

---

## 🚨 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'cache_manager'"

**Solución:**
```powershell
# Verificar que estás en el directorio correcto
cd D:\PDFviewer\pdf_query_project\backend

# Verificar que los archivos existen
dir cache_manager.py
dir fts_search.py
dir analytics.py

# Si existen, ejecutar:
python main.py
```

### Error: "OperationalError: no such table: pdf_fts"

**Solución:**
```powershell
# Ejecutar script de inicialización
python init_systems.py

# O manualmente:
python -c "from database import get_db; import fts_search as fts; db = next(get_db()); fts.init_fts_tables(db); db.close(); print('FTS inicializado')"
```

### Error: "OperationalError: no such table: query_cache"

**Solución:**
```powershell
# Inicializar base de datos
python -c "from database import init_db; init_db(); print('DB inicializada')"
```

### Error: "Failed to locate pyvenv.cfg"

**Solución 1** - Recrear venv:
```powershell
# Eliminar venv corrupto
Remove-Item -Recurse -Force venv

# Crear nuevo venv
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Solución 2** - Usar Python global:
```powershell
# Desactivar venv si está activo
deactivate

# Usar Python del sistema
python main.py
```

### Backend inicia pero endpoints de cache/FTS devuelven 500

**Solución:**
```powershell
# Verificar logs del servidor
# Buscar mensajes como "no such table: pdf_fts"

# Ejecutar init_systems.py
python init_systems.py

# Reiniciar servidor
python main.py
```

### FTS no encuentra resultados pero existen palabras

**Posibles causas:**
1. PDFs no indexados en FTS
2. Stemming normaliza palabras (vacaciones = vacación)
3. Tabla FTS vacía

**Solución:**
```powershell
# Verificar FTS stats
curl http://localhost:8000/api/fts/stats

# Si total_pages_indexed = 0, rebuild:
curl -X POST http://localhost:8000/api/fts/rebuild

# Verificar de nuevo
curl http://localhost:8000/api/fts/stats
```

---

## 📊 Verificar que Todo Funciona

### Test Completo:

```powershell
# 1. Subir un PDF de prueba
curl -X POST http://localhost:8000/upload-pdf -F "file=@test.pdf"

# 2. Hacer una query
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d "{\"question\": \"test\", \"filename\": \"test.pdf\"}"

# 3. Repetir la query (debería venir del cache)
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d "{\"question\": \"test\", \"filename\": \"test.pdf\"}"
# Buscar: "cached": true

# 4. Verificar cache stats
curl http://localhost:8000/api/cache/stats
# Debe mostrar: total_hits: 1

# 5. Probar FTS
curl "http://localhost:8000/api/fts/search?query=test"

# 6. Ver analytics
curl http://localhost:8000/api/analytics/trending?days=1
```

Si todos estos comandos funcionan, **la instalación es exitosa**! ✅

---

## 📚 Próximos Pasos

1. **Leer documentación completa**: `CACHE_FTS_ANALYTICS.md`
2. **Explorar endpoints**: http://localhost:8000/docs (Swagger UI)
3. **Subir tus PDFs**: Usar interfaz en http://localhost:3000
4. **Monitorear performance**:
   - Cache stats: `/api/cache/stats`
   - FTS stats: `/api/fts/stats`
   - Analytics: `/api/analytics/dashboard`

---

## 🔍 Scripts Útiles

### Limpiar Cache Expirado (Cron Job)
```powershell
# Crear script: clean_cache.ps1
$response = Invoke-RestMethod -Method POST -Uri "http://localhost:8000/api/cache/clear"
Write-Host $response
```

### Optimizar FTS Periódicamente
```powershell
# Crear script: optimize_fts.ps1
curl -X POST http://localhost:8000/api/fts/rebuild
```

### Backup de Base de Datos
```powershell
# Copiar pdfs_database.db
Copy-Item backend\pdfs_database.db "backup\pdfs_database_$(Get-Date -Format 'yyyyMMdd').db"
```

---

## 📞 Soporte

- **Issues**: https://github.com/juansolor/pdfanalizer/issues
- **Documentación**: Ver `CACHE_FTS_ANALYTICS.md`
- **Changelog**: Ver `CHANGELOG_v2.2.md`

---

**Versión**: 2.2  
**Última actualización**: 2025-01-15
