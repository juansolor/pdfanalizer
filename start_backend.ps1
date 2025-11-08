# Script para iniciar el backend con entorno virtual activado
# Activar el entorno virtual
& "D:\PDFviewer\.venv\Scripts\Activate.ps1"

# Cambiar al directorio backend
Set-Location "D:\PDFviewer\backend"

# Ejecutar el servidor
& "D:\PDFviewer\.venv\Scripts\python.exe" main.py