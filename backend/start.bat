@echo off
chcp 65001 >nul
echo [INFO] Configurando entorno PDF Query Backend...

REM Verificar si existe el entorno virtual
if not exist "venv\" (
    echo [INFO] Creando entorno virtual...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Error creando entorno virtual. Verifica que Python este instalado.
        pause
        exit /b 1
    )
)

REM Activar entorno virtual
echo [INFO] Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo [INFO] Instalando dependencias...
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Error instalando dependencias.
    pause
    exit /b 1
)

REM Verificar archivo .env
if not exist ".env" (
    echo [AVISO] Archivo .env no encontrado. Usando configuracion por defecto.
)

echo [OK] Configuracion completada!
echo [INFO] Iniciando servidor...
python main.py