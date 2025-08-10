# DataSage - Frontend

Este es el frontend de DataSage desplegado en GitHub Pages.

## 🌐 Enlaces

- **Frontend (GitHub Pages)**: https://nanogon19.github.io/proyecCziber/
- **Backend (Render)**: https://datasage-k86t.onrender.com/
- **Aplicación Principal**: https://nanogon19.github.io/proyecCziber/frontend/pages/home.html

## 🚀 Funcionalidades

- Conexión a bases de datos SQL Server
- Generación de consultas SQL con IA (OpenAI)
- Visualización de resultados en tablas interactivas
- Gestión de conexiones múltiples

## 🔧 Configuración

El frontend está configurado para conectarse automáticamente al backend en Render.
La configuración se encuentra en `frontend/config.js` y detecta automáticamente el entorno:

- **Desarrollo local**: `http://localhost:5000`
- **Producción**: `https://datasage-k86t.onrender.com`

## 📁 Estructura

```
/
├── index.html                    # Página de entrada
├── frontend/
│   ├── config.js                # Configuración de URLs del backend
│   ├── pages/
│   │   ├── home.html            # Aplicación principal
│   │   ├── login.html           # Página de login
│   │   └── register.html        # Página de registro
│   └── styles/                  # Archivos CSS
└── README.md                    # Este archivo
```

## 🐛 Debugging

Si hay problemas de conexión:

1. Abre las herramientas de desarrollador (F12)
2. Ve a la pestaña Console
3. Verifica los logs de configuración del backend
4. Comprueba que las URLs sean correctas

## 📝 Notas

- El frontend usa React con Babel para renderizado
- Las consultas SQL se generan con OpenAI GPT-4
- Los resultados se muestran con GridJS
