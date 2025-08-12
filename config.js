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
  
  console.log(`🔗 API Call: ${url}`);
  console.log('📤 Request options:', defaultOptions);
  
  try {
    const response = await fetch(url, defaultOptions);
    
    console.log(`📥 Response status: ${response.status} ${response.statusText}`);
    
    if (!response.ok) {
      // Intentar leer el cuerpo de la respuesta para más detalles del error
      const errorText = await response.text();
      console.error('❌ Error response body:', errorText);
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    // Verificar que la respuesta sea JSON válido
    const contentType = response.headers.get('content-type');
    if (!contentType || !contentType.includes('application/json')) {
      const responseText = await response.text();
      console.error('⚠️ Response is not JSON:', responseText.substring(0, 200));
      throw new Error('Server returned non-JSON response');
    }
    
    const data = await response.json();
    console.log('✅ Success response:', data);
    return data;
    
  } catch (error) {
    console.error(`❌ Error calling ${url}:`, error);
    
    // Mostrar un mensaje más amigable al usuario
    if (error.message.includes('Failed to fetch')) {
      throw new Error('No se puede conectar al servidor. Verifica tu conexión a internet.');
    } else if (error.message.includes('Server returned non-JSON')) {
      throw new Error('El servidor devolvió una respuesta inválida. Puede estar temporalmente fuera de servicio.');
    }
    
    throw error;
  }
}

// Log de configuración para debugging
console.log('Backend Configuration:', {
  hostname: window.location.hostname,
  isDevelopment: CONFIG.isDevelopment,
  backendUrl: CONFIG.BACKEND_URL
});
