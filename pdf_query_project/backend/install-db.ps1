# Script para instalar SQLAlchemy y Alembic
# Ejecutar en el entorno virtual del backend

Write-Host "📦 Instalando dependencias de base de datos..." -ForegroundColor Cyan

# Navegar al directorio del backend
$backendPath = "d:\PDFviewer\pdf_query_project\backend"
Set-Location $backendPath

# Activar entorno virtual
Write-Host "`n🔧 Activando entorno virtual..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Instalar SQLAlchemy y Alembic
Write-Host "`n📥 Instalando SQLAlchemy y Alembic..." -ForegroundColor Green
pip install sqlalchemy==2.0.23 alembic==1.13.1

# Verificar instalación
Write-Host "`n✅ Verificando instalación..." -ForegroundColor Cyan
python -c "import sqlalchemy; print(f'SQLAlchemy {sqlalchemy.__version__} instalado correctamente')"
python -c "import alembic; print(f'Alembic {alembic.__version__} instalado correctamente')"

# Inicializar base de datos
Write-Host "`n🗄️ Inicializando base de datos..." -ForegroundColor Magenta
python -c "from database import init_db; init_db(); print('Base de datos inicializada')"

Write-Host "`n✨ ¡Instalación completada!" -ForegroundColor Green
Write-Host "`nLa base de datos SQLite ha sido creada en:" -ForegroundColor White
Write-Host "  $backendPath\pdfs_database.db" -ForegroundColor Yellow

Write-Host "`n📊 Tablas creadas:" -ForegroundColor Cyan
Write-Host "  • pdf_documents      - Metadata de PDFs" -ForegroundColor White
Write-Host "  • query_history      - Historial de consultas" -ForegroundColor White
Write-Host "  • search_index       - Índice de búsqueda" -ForegroundColor White
Write-Host "  • usage_statistics   - Estadísticas de uso" -ForegroundColor White

Write-Host "`n🚀 Puedes iniciar el servidor con:" -ForegroundColor Cyan
Write-Host "  python main.py" -ForegroundColor Yellow
