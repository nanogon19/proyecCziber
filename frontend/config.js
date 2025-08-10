// Configuración de URLs del backend
const CONFIG = {
  // Detectar si estamos en desarrollo local o en producción
  isDevelopment: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1',
  
  // URLs del backend
  BACKEND_URL: (() => {
    // Si estamos en localhost, usar el backend local
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      return 'http://localhost:5000';
    }
    
    // Si estamos en GitHub Pages o cualquier otro hosting, usar Render
    return 'https://datasage-k86t.onrender.com'; // Tu URL real de Render
  })(),
  
  // Endpoints de la API
  ENDPOINTS: {
    CONSULTAR: '/cziber/consultar',
    LISTAR_CONEXIONES: '/cziber/listar_todas_conexiones',
    LOGIN_CONEXION: '/cziber/login_conexion',
    AGREGAR_CONEXION: '/cziber/agregar_conexion',
    LISTAR_EMPRESAS: '/cziber/listar_empresas_id',
  }
};

// Función helper para construir URLs completas
function getApiUrl(endpoint) {
  return CONFIG.BACKEND_URL + endpoint;
}

// Función para hacer fetch con la URL correcta
async function apiCall(endpoint, options = {}) {
  const url = getApiUrl(endpoint);
  
  // Agregar headers por defecto
  const defaultOptions = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers
    },
    ...options
  };
  
  console.log(`API Call: ${url}`);
  
  try {
    const response = await fetch(url, defaultOptions);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error(`Error calling ${url}:`, error);
    throw error;
  }
}

// Log de configuración para debugging
console.log('Backend Configuration:', {
  hostname: window.location.hostname,
  isDevelopment: CONFIG.isDevelopment,
  backendUrl: CONFIG.BACKEND_URL
});
