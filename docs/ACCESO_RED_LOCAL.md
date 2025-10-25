# 🌐 Guía de Acceso en Red Local

## 📱 Acceder desde otros dispositivos en tu red

Esta guía te ayudará a acceder a tu aplicación PDF Query System desde cualquier dispositivo en tu red local (celular, tablet, otra computadora).

## 🔧 Configuración Ya Realizada

El sistema ya está configurado para permitir acceso desde red local:

✅ **Backend**: `HOST=0.0.0.0` (escucha en todas las interfaces)  
✅ **Frontend**: `host: '0.0.0.0'` en Vite  
✅ **CORS**: Configurado para permitir orígenes de red local  
✅ **API URL**: Detección automática de hostname  

## 🚀 Paso a Paso

### 1️⃣ Obtén tu IP Local

En PowerShell (Windows):
```powershell
ipconfig
```

Busca tu dirección IPv4 (ejemplo: `192.168.1.100`)

En Linux/Mac:
```bash
ifconfig
# o
ip addr show
```

### 2️⃣ Inicia el Sistema

**Terminal 1 - Backend:**
```powershell
cd d:\PDFviewer\pdf_query_project\backend
python main.py
```

Verás algo como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```powershell
cd d:\PDFviewer\pdf_query_project\frontend_new
npm run dev
```

Verás algo como:
```
  ➜  Local:   http://localhost:5173/
  ➜  Network: http://192.168.1.100:5173/
```

### 3️⃣ Accede desde otro dispositivo

Desde cualquier dispositivo en la misma red WiFi, abre el navegador y ve a:

**Formato:**
```
http://[TU_IP_LOCAL]:5173
```

**Ejemplo:**
```
http://192.168.1.100:5173
```

## 📱 Acceso desde Dispositivos Móviles

### iPhone/iPad (Safari)
1. Conecta a la misma WiFi
2. Abre Safari
3. Ve a: `http://192.168.1.100:5173`
4. ¡Listo! Puedes agregar a pantalla de inicio

### Android (Chrome)
1. Conecta a la misma WiFi
2. Abre Chrome
3. Ve a: `http://192.168.1.100:5173`
4. Menú → "Agregar a pantalla de inicio"

### Tablet
Igual que móvil, solo usa el navegador web.

## 🖥️ Acceso desde otra Computadora

1. Conecta a la misma red WiFi
2. Abre cualquier navegador
3. Ve a: `http://192.168.1.100:5173`
4. Funciona igual que en tu PC principal

## 🔥 Características de Red Local

### Ventajas:
- ✅ Sin necesidad de internet
- ✅ Velocidad máxima (red local)
- ✅ Privacidad total (no sale de tu red)
- ✅ Múltiples usuarios simultáneos
- ✅ Funciona con WiFi, Ethernet, Hotspot

### Limitaciones:
- ⚠️ Solo funciona en la misma red
- ⚠️ IP puede cambiar si reinicias el router
- ⚠️ Firewall de Windows puede bloquear (ver solución abajo)

## 🛡️ Configuración de Firewall (Windows)

Si otros dispositivos no pueden conectar:

### Opción 1: Permitir Python y Node en Firewall
```powershell
# Ejecuta como Administrador
netsh advfirewall firewall add rule name="Python Server" dir=in action=allow program="C:\Path\To\python.exe" enable=yes
netsh advfirewall firewall add rule name="Node Vite Server" dir=in action=allow program="C:\Path\To\node.exe" enable=yes
```

### Opción 2: Permitir puertos específicos
```powershell
# Ejecuta como Administrador
# Puerto 8000 para backend
netsh advfirewall firewall add rule name="PDF Backend" dir=in action=allow protocol=TCP localport=8000

# Puerto 5173 para frontend
netsh advfirewall firewall add rule name="PDF Frontend" dir=in action=allow protocol=TCP localport=5173
```

### Opción 3: Desactivar Firewall temporalmente (NO recomendado)
```powershell
# Panel de Control → Sistema y Seguridad → Firewall de Windows Defender
# Solo para pruebas, no dejar así permanentemente
```

## 🔍 Verificar Conectividad

### Desde otro dispositivo, prueba:

**Ping a tu PC:**
```bash
ping 192.168.1.100
```

**Verificar puerto backend (desde navegador):**
```
http://192.168.1.100:8000
```
Deberías ver: `{"message": "PDF Query API", "version": "1.0.0"}`

**Verificar puerto frontend:**
```
http://192.168.1.100:5173
```
Deberías ver la interfaz de la app.

## 🎯 Casos de Uso

### 1. Demo en Reunión
- Tu laptop ejecuta el servidor
- Compartes la URL `http://192.168.1.X:5173`
- Todos en la reunión acceden desde sus dispositivos

### 2. Trabajo Colaborativo
- Un equipo de trabajo en la misma oficina
- Una persona ejecuta el servidor
- Todos consultan PDFs desde sus dispositivos

### 3. Casa/Familia
- Servidor en una PC principal
- Tablets, celulares, otras PCs acceden
- Consultar PDFs familiares desde cualquier dispositivo

### 4. Presentaciones
- Laptop conectado a proyector
- Audiencia puede seguir en sus celulares
- Interacción en tiempo real

## 📊 Monitoreo de Conexiones

En el backend verás logs de todas las conexiones:

```
INFO:     192.168.1.105:52341 - "GET / HTTP/1.1" 200 OK
INFO:     192.168.1.110:52342 - "POST /query HTTP/1.1" 200 OK
```

Cada IP diferente = dispositivo diferente conectado.

## 🚨 Solución de Problemas

### No puedo conectar desde otro dispositivo

**1. Verifica que estén en la misma red:**
```powershell
# En ambos dispositivos, verifica que la IP comience igual
# Ejemplo: 192.168.1.X debe ser la misma subred
ipconfig  # Windows
ifconfig  # Linux/Mac
```

**2. Verifica que los servicios estén corriendo:**
```powershell
# Backend debe mostrar: Uvicorn running on http://0.0.0.0:8000
# Frontend debe mostrar: Network: http://192.168.1.X:5173
```

**3. Prueba el backend directamente:**
```
http://192.168.1.X:8000/health
```
Debe retornar: `{"status": "ok"}`

**4. Verifica CORS:**
Si ves errores CORS en consola del navegador, el backend ya está configurado para permitir todos los orígenes en modo DEBUG.

### Error: "Cannot GET /"

- El frontend no está corriendo
- Verifica que `npm run dev` esté activo

### Error: "Failed to fetch" o "Network Error"

- Backend no está corriendo
- Firewall bloqueando
- IP incorrecta

### Frontend funciona pero no conecta al backend

- Verifica la URL en consola del navegador (F12)
- Debe estar usando `http://192.168.1.X:8000`
- Si usa `localhost`, refresca la página

## 🔐 Seguridad en Red Local

### ✅ Buenas Prácticas:

1. **Solo usar en redes confiables** (tu WiFi personal)
2. **No exponer a internet público** (no hacer port forwarding)
3. **Cambiar SECRET_KEY** en `.env` si usas en producción
4. **Limitar acceso por MAC address** en router (opcional)
5. **Usar VPN** si necesitas acceso remoto seguro

### ⚠️ NO HACER:

- ❌ NO abrir puertos en el router hacia internet
- ❌ NO usar en redes públicas sin VPN
- ❌ NO dejar corriendo sin supervisión en red desconocida
- ❌ NO compartir la URL fuera de tu red local

## 📱 Crear Acceso Directo en Móvil

### iOS (Safari):
1. Abre `http://192.168.1.X:5173`
2. Toca el ícono de compartir
3. "Agregar a pantalla de inicio"
4. Dale un nombre: "PDF Query"
5. ¡Ahora tienes un ícono en tu iPhone!

### Android (Chrome):
1. Abre `http://192.168.1.X:5173`
2. Menú (⋮) → "Agregar a pantalla de inicio"
3. Dale un nombre: "PDF Query"
4. ¡Ahora tienes un ícono en tu Android!

## 🎉 ¡Listo!

Ahora puedes:
- 📱 Usar desde tu celular
- 💻 Acceder desde otras computadoras
- 📊 Presentar a un equipo
- 👨‍👩‍👧‍👦 Compartir con familia
- 🏢 Demostrar en oficina

Todo sin necesidad de subirlo a internet, manteniendo privacidad y velocidad máxima.

---

## 🔄 Script de Inicio Rápido

Crea un archivo `start-network.ps1`:

```powershell
# Obtener IP local
$ip = (Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias Wi-Fi*).IPAddress

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  PDF Query System - Acceso Red Local" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Tu IP Local: $ip" -ForegroundColor Green
Write-Host ""
Write-Host "URLs de Acceso:" -ForegroundColor Yellow
Write-Host "  Local:   http://localhost:5173" -ForegroundColor White
Write-Host "  Red:     http://${ip}:5173" -ForegroundColor Green
Write-Host ""
Write-Host "Comparte la URL de Red con otros dispositivos" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Iniciar servicios
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python main.py"
Start-Sleep -Seconds 3
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend_new; npm run dev"

Write-Host "Servicios iniciados!" -ForegroundColor Green
```

Ejecuta: `.\start-network.ps1`

---

**¡Disfruta tu PDF Query System en toda tu red local!** 🌐✨
