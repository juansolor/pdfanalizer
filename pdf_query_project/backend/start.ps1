# Script de inicio simple para PDF Query Backend
Write-Host ">> PDF Query Backend - Inicio Rapido" -ForegroundColor Green

# Intentar instalar dependencias directamente
Write-Host ">> Instalando dependencias basicas..." -ForegroundColor Yellow
try {
    pip install fastapi uvicorn python-multipart PyPDF2 python-dotenv
    if ($LASTEXITCODE -ne 0) {
        throw "Error instalando dependencias basicas"
    }
    Write-Host "OK: Dependencias instaladas correctamente" -ForegroundColor Green
} catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Intentando con instalacion individual..." -ForegroundColor Yellow
    
    # Instalar una por una
    $packages = @("fastapi", "uvicorn", "python-multipart", "PyPDF2", "python-dotenv")
    foreach ($pkg in $packages) {
        Write-Host "Instalando $pkg..." -ForegroundColor Cyan
        pip install $pkg
    }
}

# Verificar archivo .env
if (-Not (Test-Path ".env")) {
    Write-Host "AVISO: Archivo .env no encontrado. Usando configuracion por defecto." -ForegroundColor Yellow
} else {
    Write-Host "OK: Configuracion .env encontrada" -ForegroundColor Green
}

# Mostrar informacion
Write-Host "" 
Write-Host "===== INFORMACION DEL SERVIDOR =====" -ForegroundColor Cyan
Write-Host "URL: http://localhost:8000" -ForegroundColor White
Write-Host "Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Health: http://localhost:8000/health" -ForegroundColor White
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

Write-Host ">> Iniciando servidor..." -ForegroundColor Green
python main.py