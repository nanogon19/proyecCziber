const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors({
  origin: ['http://localhost:5000', 'http://127.0.0.1:5000'], // Permitir tu backend Flask
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));

// Servir archivos estáticos
app.use('/static', express.static(path.join(__dirname, 'static')));
app.use('/styles', express.static(path.join(__dirname, 'styles')));
app.use('/components', express.static(path.join(__dirname, 'components')));

// Rutas principales
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'pages', 'datasage-home-fixed.html'));
});

app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'pages', 'login.html'));
});

app.get('/register', (req, res) => {
  res.sendFile(path.join(__dirname, 'pages', 'register.html'));
});

app.get('/home', (req, res) => {
  res.sendFile(path.join(__dirname, 'pages', 'datasage-home-fixed.html'));
});

// Servir páginas directamente
app.use('/pages', express.static(path.join(__dirname, 'pages')));

// Manejo de errores 404
app.use((req, res) => {
  res.status(404).send(`
    <h1>404 - Página no encontrada</h1>
    <p>Las páginas disponibles son:</p>
    <ul>
      <li><a href="/">Inicio</a></li>
      <li><a href="/login">Login</a></li>
      <li><a href="/register">Registro</a></li>
    </ul>
  `);
});

app.listen(PORT, () => {
  console.log(`🚀 Frontend servidor iniciado en: http://localhost:${PORT}`);
  console.log(`📁 Sirviendo archivos desde: ${__dirname}`);
  console.log('📋 Páginas disponibles:');
  console.log(`   - Home: http://localhost:${PORT}/`);
  console.log(`   - Login: http://localhost:${PORT}/login`);
  console.log(`   - Register: http://localhost:${PORT}/register`);
  console.log('\n🛑 Presiona Ctrl+C para detener el servidor');
});
