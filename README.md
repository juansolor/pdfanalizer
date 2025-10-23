# PDF Query Project

Este proyecto permite realizar consultas a documentos PDF utilizando inteligencia artificial.

## Estructura del Proyecto

- **backend/**: Servidor Python con FastAPI para procesar PDFs y realizar consultas
- **frontend/**: Interfaz de usuario en React para interactuar con el sistema

## Instalación y Uso

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Funcionalidades

- Subida de archivos PDF
- Procesamiento y análisis de documentos
- Consultas en lenguaje natural sobre el contenido
- Interfaz web intuitiva

## Tecnologías

- **Backend**: Python, FastAPI, PyPDF2, OpenAI/Langchain
- **Frontend**: React, JavaScript, HTML/CSS