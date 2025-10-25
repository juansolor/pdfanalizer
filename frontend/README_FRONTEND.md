# PDF Query System - Frontend con Vite

Este es el nuevo frontend del proyecto construido con **Vite + React**, mucho más rápido y moderno que Create React App.

## 🚀 Características

- ⚡ Vite para desarrollo ultra-rápido
- ⚛️ React 18
- 🎨 Diseño moderno con gradientes y animaciones
- 📱 Completamente responsive
- 🔌 Conexión en tiempo real con el backend FastAPI
- 📊 Estado de conexión visible

## 📦 Instalación

```bash
npm install
```

## 🏃 Ejecución

```bash
npm run dev
```

El frontend estará disponible en: `http://localhost:5173`

## 🔧 Configuración

### URL del Backend

El frontend se conecta al backend en `http://localhost:8000` por defecto.

Para cambiar la URL, edita `src/App.jsx`:

```javascript
const API_BASE_URL = 'http://localhost:8000'
```

### Puerto del Frontend

Vite usa el puerto 5173 por defecto. Para cambiarlo, edita `vite.config.js`:

```javascript
export default defineConfig({
  server: {
    port: 3000 // tu puerto preferido
  }
})
```

## 🌐 CORS

Asegúrate de que el backend permita conexiones desde `http://localhost:5173`.

En el archivo `backend/.env`:

```
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

## 📝 Scripts Disponibles

- `npm run dev` - Inicia el servidor de desarrollo
- `npm run build` - Construye para producción
- `npm run preview` - Vista previa de la versión de producción

## 🛠️ Tecnologías

- Vite 7
- React 18
- Axios para peticiones HTTP
- CSS moderno con variables CSS

## 🎨 Estructura del Proyecto

```
frontend_new/
├── src/
│   ├── App.jsx          # Componente principal
│   ├── App.css          # Estilos del componente
│   ├── index.css        # Estilos globales
│   └── main.jsx         # Punto de entrada
├── public/              # Archivos estáticos
├── index.html           # HTML base
├── vite.config.js       # Configuración de Vite
└── package.json         # Dependencias
```

## 🔄 Migración desde Create React App

Este frontend reemplaza al anterior que usaba Create React App. Beneficios:

- ✅ Inicio ~10x más rápido
- ✅ Hot Module Replacement instantáneo
- ✅ Build optimizado y más pequeño
- ✅ Sin problemas de dependencias de Babel
- ✅ Configuración más simple

## 📡 API Endpoints Usados

- `GET /` - Verificar estado del backend
- `GET /list-pdfs` - Listar PDFs disponibles
- `POST /upload-pdf` - Subir nuevo PDF
- `POST /query` - Realizar consulta sobre PDF

## 🎯 Próximos Pasos

1. Asegúrate de que el backend esté corriendo en `http://localhost:8000`
2. Inicia el frontend con `npm run dev`
3. Abre `http://localhost:5173` en tu navegador
4. ¡Empieza a subir PDFs y hacer preguntas!
