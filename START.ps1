#!/usr/bin/env pwsh
# Script de inicio rápido para todo el sistema

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PDF Query System - Inicio Rapido" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar Python
Write-Host "[1/4] Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK Python encontrado: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Python no encontrado" -ForegroundColor Red
    exit 1
}

# Verificar Node
Write-Host "[2/4] Verificando Node.js..." -ForegroundColor Yellow
$nodeVersion = node --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  OK Node.js encontrado: $nodeVersion" -ForegroundColor Green
} else {
    Write-Host "  ERROR: Node.js no encontrado" -ForegroundColor Red
    exit 1
}

# Instalar dependencias Python si es necesario
Write-Host "[3/4] Verificando dependencias Python..." -ForegroundColor Yellow
$packages = @("fastapi", "uvicorn", "python-multipart", "PyPDF2", "python-dotenv")
foreach ($pkg in $packages) {
    $installed = pip show $pkg 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  Instalando $pkg..." -ForegroundColor Yellow
        pip install $pkg --quiet
    }
}
Write-Host "  OK Todas las dependencias instaladas" -ForegroundColor Green

# Verificar dependencias Node
Write-Host "[4/4] Verificando dependencias Node..." -ForegroundColor Yellow
if (Test-Path "frontend_new/node_modules") {
    Write-Host "  OK node_modules existe" -ForegroundColor Green
} else {
    Write-Host "  Instalando dependencias de Node..." -ForegroundColor Yellow
    Set-Location frontend_new
    npm install --silent
    Set-Location ..
    Write-Host "  OK Dependencias instaladas" -ForegroundColor Green
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Sistema Listo!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "INSTRUCCIONES:" -ForegroundColor Yellow
Write-Host ""
Write-Host "Abre 2 terminales:" -ForegroundColor White
Write-Host ""
Write-Host "Terminal 1 - Backend:" -ForegroundColor Cyan
Write-Host "  cd backend" -ForegroundColor White
Write-Host "  python main.py" -ForegroundColor White
Write-Host ""
Write-Host "Terminal 2 - Frontend:" -ForegroundColor Cyan
Write-Host "  cd frontend_new" -ForegroundColor White
Write-Host "  npm run dev" -ForegroundColor White
Write-Host ""
Write-Host "Luego abre: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "NUEVAS FUNCIONALIDADES:" -ForegroundColor Magenta
Write-Host "  - Muestra en que paginas esta la respuesta" -ForegroundColor White
Write-Host "  - Abre el PDF directamente en la pagina correcta" -ForegroundColor White
Write-Host "  - Tarjetas visuales con contexto de cada ubicacion" -ForegroundColor White
Write-Host "  - Chips interactivos para navegar entre paginas" -ForegroundColor White
Write-Host ""
