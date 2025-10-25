# Backend - PDF Query API

Este es el backend del proyecto PDF Query, construido con FastAPI.

## Instalación y Uso Rápido

### Opción 1: Inicio Automático (Recomendado)
```bash
# En PowerShell
.\start.ps1

# O en CMD
start.bat
```

### Opción 2: Manual
1. Crear un entorno virtual:
```bash
python -m venv venv
venv\Scripts\activate  # En Windows
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecutar el servidor:
```bash
python main.py
```

## Configuración (.env)

El proyecto utiliza un archivo `.env` para configuración automática:

```env
# Servidor
HOST=0.0.0.0
PORT=8000
DEBUG=True

# CORS
CORS_ORIGINS=http://localhost:3000

# Archivos
MAX_FILE_SIZE=50  # MB
UPLOAD_FOLDER=pdfs
RESULTS_FOLDER=results
```

### Archivos de configuración disponibles:
- `.env` - Configuración por defecto
- `.env.development` - Configuración para desarrollo

2. El servidor estará disponible en: `http://localhost:8000`

3. Documentación automática en: `http://localhost:8000/docs`

## Endpoints

- `GET /` - Información de la API y configuración
- `GET /health` - Verificación de salud del servicio
- `POST /upload-pdf` - Subir archivo PDF (máx. 50MB)
- `POST /extract-text/{filename}` - Extraer texto de PDF
- `POST /query` - Realizar consulta sobre PDF
- `GET /list-pdfs` - Listar PDFs subidos

### Ejemplos de uso:

```bash
# Verificar estado
curl http://localhost:8000/

# Subir PDF
curl -X POST -F "file=@documento.pdf" http://localhost:8000/upload-pdf

# Listar PDFs
curl http://localhost:8000/list-pdfs
```

## Directorios

- `pdfs/` - Archivos PDF subidos
- `results/` - Resultados de procesamiento

## Configuración

- Puerto: 8000
- CORS habilitado para frontend en puerto 3000