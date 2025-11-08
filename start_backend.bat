@echo off
REM Script para iniciar el backend con entorno virtual activado
echo Activando entorno virtual...
call "D:\PDFviewer\.venv\Scripts\activate.bat"

echo Cambiando al directorio backend...
cd /d "D:\PDFviewer\backend"

echo Iniciando servidor FastAPI...
python main.py

pause