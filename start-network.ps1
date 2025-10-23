#!/usr/bin/env pwsh
# Script de inicio para acceso en red local

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PDF Query System - Red Local" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Obtener IP local
$ip = $null
try {
    $ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.IPAddress -like "192.168.*" -or $_.IPAddress -like "10.*" -or $_.IPAddress -like "172.*"} | Select-Object -First 1).IPAddress
} catch {
    Write-Host "  No se pudo detectar IP automáticamente" -ForegroundColor Yellow
}

if ($ip) {
    Write-Host "Tu IP Local: $ip" -ForegroundColor Green
    Write-Host ""
    Write-Host "URLs de Acceso:" -ForegroundColor Yellow
    Write-Host "  Localhost:  http://localhost:5173" -ForegroundColor White
    Write-Host "  Red Local:  http://${ip}:5173" -ForegroundColor Green
    Write-Host ""
    Write-Host "Backend API:  http://${ip}:8000" -ForegroundColor Cyan
    Write-Host "API Docs:     http://${ip}:8000/docs" -ForegroundColor Cyan
} else {
    Write-Host "URLs de Acceso:" -ForegroundColor Yellow
    Write-Host "  Local: http://localhost:5173" -ForegroundColor White
    Write-Host ""
    Write-Host "Para obtener tu IP, ejecuta: ipconfig" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Preguntar si desea abrir firewall
Write-Host "Deseas configurar el firewall? (s/N): " -ForegroundColor Yellow -NoNewline
$respuesta = Read-Host

if ($respuesta -eq 's' -or $respuesta -eq 'S') {
    Write-Host ""
    Write-Host "Configurando firewall..." -ForegroundColor Yellow
    Write-Host "Ejecuta estos comandos como Administrador:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host 'netsh advfirewall firewall add rule name="PDF Backend" dir=in action=allow protocol=TCP localport=8000' -ForegroundColor White
    Write-Host 'netsh advfirewall firewall add rule name="PDF Frontend" dir=in action=allow protocol=TCP localport=5173' -ForegroundColor White
    Write-Host ""
}

Write-Host "Iniciando servicios..." -ForegroundColor Green
Write-Host ""

# Iniciar backend
Write-Host "[1/2] Iniciando Backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\backend'; Write-Host 'Backend iniciado en http://0.0.0.0:8000' -ForegroundColor Green; python main.py"

Start-Sleep -Seconds 3

# Iniciar frontend
Write-Host "[2/2] Iniciando Frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PSScriptRoot\frontend_new'; Write-Host 'Frontend iniciado' -ForegroundColor Green; npm run dev"

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Servicios Iniciados!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

if ($ip) {
    Write-Host "Comparte esta URL con otros dispositivos:" -ForegroundColor Yellow
    Write-Host "  http://${ip}:5173" -ForegroundColor Green
    Write-Host ""
    Write-Host "Asegurate de que esten en la misma red WiFi" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "Presiona Ctrl+C para detener los servicios" -ForegroundColor Gray
Write-Host ""

# Mantener script abierto
while ($true) {
    Start-Sleep -Seconds 1
}
