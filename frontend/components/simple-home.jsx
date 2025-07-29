function SimpleHome() {
  const [showConexiones, setShowConexiones] = React.useState(false);
  const [conexiones, setConexiones] = React.useState([]);
  const [loading, setLoading] = React.useState(false);

  const listarConexiones = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://localhost:5000/cziber/listar_todas_conexiones", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (response.ok) {
        const data = await response.json();
        setConexiones(data.conexiones);
        setShowConexiones(true);
        console.log("Conexiones obtenidas:", data.conexiones);
      } else {
        const errorData = await response.json();
        console.error("Error al obtener conexiones:", errorData.error);
        alert("Error al obtener conexiones: " + errorData.error);
      }
    } catch (error) {
      console.error("Error al conectar con el backend:", error);
      alert("No se pudo conectar con el servidor");
    }
    setLoading(false);
  };

  return (
    <div className="main-layout">
      <aside className="sidebar">
        <div className="profile-section">
          <button onClick={() => alert('Perfil')}>Perfil Ejemplo</button>
          <button onClick={listarConexiones} disabled={loading}>
            {loading ? "Cargando..." : "Listar Conexiones"}
          </button>
          <button onClick={() => setShowConexiones(false)}>
            Volver al Chat
          </button>
        </div>
        <div className="previous-queries">
          <h4>Consultas Anteriores</h4>
          <div className="query-item">Consulta ejemplo</div>
        </div>
      </aside>

      <section className="chat-area">
        {showConexiones ? (
          <div className="conexiones-view">
            <div className="chat-header">
              Conexiones Disponibles ({conexiones.length})
            </div>
            <div className="conexiones-list">
              {conexiones.length === 0 ? (
                <div className="no-conexiones">No hay conexiones disponibles</div>
              ) : (
                conexiones.map((conexion, index) => (
                  <div key={conexion.id_conn} className="conexion-item">
                    <div className="conexion-header">
                      <h4>Conexión #{index + 1}</h4>
                      <span className="conexion-id">{conexion.id_conn}</span>
                    </div>
                    <div className="conexion-details">
                      <p><strong>IP:</strong> {conexion.ip}</p>
                      <p><strong>Puerto:</strong> {conexion.puerto}</p>
                      <p><strong>Usuario:</strong> {conexion.usuario}</p>
                      <p><strong>Contraseña:</strong> {conexion.clave}</p>
                      {conexion.empresa_nombre && (
                        <p><strong>Empresa:</strong> {conexion.empresa_nombre}</p>
                      )}
                      {conexion.aplicacion_nombre && (
                        <p><strong>Aplicación:</strong> {conexion.aplicacion_nombre}</p>
                      )}
                      {conexion.modelo_nombre && (
                        <p><strong>Modelo:</strong> {conexion.modelo_nombre}</p>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        ) : (
          <div>
            <div className="chat-header">
              Chat con IA - Versión Simplificada
            </div>
            <div className="chat-messages">
              <div className="message bot">
                ¡Hola! Esta es la versión simplificada. 
                Haz clic en "Listar Conexiones" para ver las conexiones disponibles.
              </div>
            </div>
            <div className="input-area">
              <input type="text" placeholder="Escribe tu mensaje..." />
              <button onClick={() => alert('Función de chat no implementada en esta versión')}>
                Enviar
              </button>
            </div>
          </div>
        )}
      </section>
    </div>
  );
}

// Renderizar el componente
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<SimpleHome />);
