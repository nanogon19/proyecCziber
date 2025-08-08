# Frontend CZiber

Este directorio contiene el frontend del proyecto CZiber.

## 🚀 Formas de hospedar el frontend

### 1. Servidor local con Python (Recomendado para desarrollo)

```bash
# Opción 1: Ejecutar el script Python
python server.py

# Opción 2: Usar el batch file (Windows)
start-frontend.bat

# Opción 3: Usar PowerShell (Windows)
.\start-frontend.ps1

# Opción 4: Servidor Python simple
python -m http.server 3000
```

### 2. Servidor con Node.js (Más profesional)

```bash
# Instalar dependencias
npm install

# Iniciar servidor
npm start

# O usando http-server
npm run serve
```

### 3. Hosting en la nube (Producción)

#### Netlify (Gratis)

1. Arrastra la carpeta `frontend` a [netlify.com](https://netlify.com)
2. O conecta tu repositorio de GitHub
3. Configuración:
   - Build command: `echo "No build needed"`
   - Publish directory: `.`

#### Vercel (Gratis)

1. Instala Vercel CLI: `npm i -g vercel`
2. Ejecuta: `vercel`
3. O conecta tu repositorio en [vercel.com](https://vercel.com)

#### GitHub Pages

1. Sube tu código a GitHub
2. Ve a Settings > Pages
3. Selecciona la carpeta `frontend` como source

#### Firebase Hosting

```bash
npm install -g firebase-tools
firebase init hosting
firebase deploy
```

### 4. Hosting compartido tradicional

- Sube los archivos via FTP/SFTP
- Asegúrate de que `datasage-home-fixed.html` sea accesible

## 📁 Estructura de archivos

```
frontend/
├── pages/           # Páginas HTML
├── styles/          # Archivos CSS
├── static/          # Imágenes y assets
├── components/      # Componentes reutilizables
├── server.py        # Servidor Python
├── server.js        # Servidor Node.js
└── package.json     # Configuración Node.js
```

## ⚙️ Configuración

### Variables de entorno

El frontend se conecta al backend en `http://localhost:5000`

Para cambiar la URL del backend, edita los archivos HTML y busca:

```javascript
fetch('http://localhost:5000/cziber/consultar'
```

### CORS

Asegúrate de que tu backend Flask tenga configurado CORS para permitir el dominio del frontend.

## 🌐 URLs una vez hosteado

- Home: `/` o `/pages/datasage-home-fixed.html`
- Login: `/login` o `/pages/login.html`
- Register: `/register` o `/pages/register.html`

## 🔧 Troubleshooting

### Problema: Error de CORS

**Solución**: Configura CORS en tu backend Flask para permitir el dominio del frontend

### Problema: 404 en rutas

**Solución**: Usa rutas completas como `/pages/login.html`

### Problema: Recursos no cargan

**Solución**: Verifica las rutas relativas en los archivos HTML
