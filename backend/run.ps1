# Script mejorado para PDF Query Backend
$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $SCRIPT_DIR

Write-Host "===== PDF QUERY BACKEND =====" -ForegroundColor Cyan
Write-Host "Directorio: $SCRIPT_DIR" -ForegroundColor Gray

# Verificar Python
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python detectado: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Python no encontrado en PATH" -ForegroundColor Red
    Read-Host "Presiona Enter para salir"
    exit 1
}

# Instalar dependencias si es necesario
Write-Host ">> Verificando dependencias..." -ForegroundColor Yellow

$requiredPackages = @{
    "fastapi" = "pip install fastapi"
    "uvicorn" = "pip install uvicorn"
    "python-multipart" = "pip install python-multipart"
    "PyPDF2" = "pip install PyPDF2"
    "python-dotenv" = "pip install python-dotenv"
}

foreach ($package in $requiredPackages.Keys) {
    try {
        $result = python -c "import $package" 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ $package instalado" -ForegroundColor Green
        } else {
            Write-Host "  × Instalando $package..." -ForegroundColor Yellow
            Invoke-Expression $requiredPackages[$package]
        }
    } catch {
        Write-Host "  × Instalando $package..." -ForegroundColor Yellow
        Invoke-Expression $requiredPackages[$package]
    }
}

# Verificar archivos necesarios
if (Test-Path "main.py") {
    Write-Host "✓ main.py encontrado" -ForegroundColor Green
} else {
    Write-Host "ERROR: main.py no encontrado" -ForegroundColor Red
    exit 1
}

if (Test-Path ".env") {
    Write-Host "✓ Configuracion .env encontrada" -ForegroundColor Green
} else {
    Write-Host "! Usando configuracion por defecto" -ForegroundColor Yellow
}

# Crear directorios necesarios
New-Item -ItemType Directory -Path "pdfs" -Force | Out-Null
New-Item -ItemType Directory -Path "results" -Force | Out-Null

Write-Host "" 
Write-Host "===== SERVIDOR INICIADO =====" -ForegroundColor Green
Write-Host "URL Principal: http://localhost:8000" -ForegroundColor White
Write-Host "Documentacion: http://localhost:8000/docs" -ForegroundColor White
Write-Host "Estado: http://localhost:8000/health" -ForegroundColor White
Write-Host "" 
Write-Host "Presiona Ctrl+C para detener el servidor" -ForegroundColor Gray
Write-Host "==============================" -ForegroundColor Green

# Iniciar servidor
python main.py