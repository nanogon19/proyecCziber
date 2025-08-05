function DataSageHome() {
  const [prompt, setPrompt] = React.useState("");
  const [results, setResults] = React.useState([]);
  const [showConexiones, setShowConexiones] = React.useState(false);
  const [conexiones, setConexiones] = React.useState([]);
  const [loading, setLoading] = React.useState(false);
  const [currentView, setCurrentView] = React.useState("listar");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    try {
      const response = await fetch('http://localhost:5000/cziber/consultar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ prompt })
      });

      const json = await response.json();
      console.log("Respuesta del servidor:", json);
      
      if (json.mensaje) {
        alert(json.mensaje);
        return;
      }

      const { columns, data } = json;
      
      // Agregar resultado a la lista
      const newResult = {
        id: Date.now(),
        prompt: prompt,
        columns: columns,
        data: data,
        timestamp: new Date().toLocaleString()
      };

      setResults(prev => [newResult, ...prev]);
      setPrompt("");

    } catch (error) {
      console.error("Error al enviar la consulta:", error);
      alert("Error al enviar la consulta. Por favor, inténtelo de nuevo.");
    }
  };

  const exportToExcel = (result) => {
    const worksheetData = [result.columns, ...result.data];
    const worksheet = XLSX.utils.aoa_to_sheet(worksheetData);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Resultado");

    const filename = `consulta_${Date.now()}.xlsx`;
    XLSX.writeFile(workbook, filename);
  };

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

  const DataGrid = ({ columns, data }) => {
    const gridRef = React.useRef(null);

    React.useEffect(() => {
      if (gridRef.current && columns && data) {
        gridRef.current.innerHTML = '';
        
        try {
          const grid = new gridjs.Grid({
            columns: columns,
            data: data,
            pagination: {
              enabled: true,
              limit: 10
            },
            search: true,
            sort: true,
            resizable: true,
            fixedHeader: true,
            height: '400px',
            width: '100%',
            style: {
              table: {
                'border-radius': '10px',
                'overflow': 'hidden',
                'box-shadow': '0 2px 10px rgba(0, 0, 0, 0.1)',
                'width': '100%'
              },
              th: {
                'background-color': '#f4b142',
                'color': '#fff',
                'text-align': 'center',
                'padding': '12px'
              },
              td: {
                'text-align': 'center',
                'padding': '8px'
              }
            }
          });
          
          grid.render(gridRef.current);
        } catch (error) {
          console.error('Error rendering grid:', error);
          gridRef.current.innerHTML = '<p>Error al cargar la tabla</p>';
        }
      }
    }, [columns, data]);

    return (
      <div className="grid-container">
        <div ref={gridRef}></div>
      </div>
    );
  };

  return (
    <div className="app-container">
      <div className="sidebar">
        <header>
          <p 
            className="conexiones" 
            onClick={() => {
              setShowConexiones(true);
              setCurrentView("listar");
              listarConexiones();
            }}
            style={{ cursor: 'pointer' }}
          >
            Conexiones
          </p>
        </header>
        <h2>Consultas anteriores</h2>
        <div className="previous-queries">
          {results.length === 0 ? (
            <div className="no-queries">
              <p>No hay consultas anteriores</p>
            </div>
          ) : (
            results.map((result, index) => (
              <div key={result.id} className="query-item">
                <div className="query-text">
                  {result.prompt.length > 50 ? 
                    `${result.prompt.substring(0, 50)}...` : 
                    result.prompt
                  }
                </div>
                <div className="query-time">
                  {result.timestamp}
                </div>
              </div>
            ))
          )}
        </div>
      </div>

      <div className="main-container">
        <header className="header">
          <div className="logo">DATASAGE</div>
          <img src="../static/img/logo.png" alt="Logo" className="logo-img" />
        </header>

        <div className="result-box" id="resultBox">
          {results.length === 0 ? (
            <div className="no-results">
              <p>No hay consultas realizadas aún. Escribe una consulta para comenzar.</p>
            </div>
          ) : (
            results.map((result) => (
              <div key={result.id} className="result-item">
                <div className="result-header">
                  <h3>Consulta: {result.prompt}</h3>
                  <button 
                    className="export-btn"
                    onClick={() => exportToExcel(result)}
                  >
                    Exportar a Excel
                  </button>
                </div>
                <DataGrid columns={result.columns} data={result.data} />
              </div>
            ))
          )}
        </div>

        <form onSubmit={handleSubmit} className="input-area">
          <textarea 
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Escriba su consulta aquí..."
            rows="3"
          />
          <button type="submit" disabled={!prompt.trim()}>
            Enviar
          </button>
        </form>
      </div>

      {/* Modal de Conexiones */}
      {showConexiones && (
        <div className="modal-conexiones">
          <div className="contenido-conexiones">
            <span 
              className="cerrar"
              onClick={() => setShowConexiones(false)}
            >
              &times;
            </span>
            <h2>Conexiones</h2>
            
            <div className="opciones-conexiones">
              <p 
                className={`conexion-op ${currentView === 'listar' ? 'active' : ''}`}
                onClick={() => {
                  setCurrentView("listar");
                  listarConexiones();
                }}
              >
                Listar conexiones
              </p>
              <p 
                className={`conexion-op ${currentView === 'agregar' ? 'active' : ''}`}
                onClick={() => setCurrentView("agregar")}
              >
                Agregar conexión
              </p>
            </div>

            <div className="conexiones-content">
              {currentView === "listar" ? (
                <div className="conexiones-list">
                  {loading ? (
                    <div className="loading">Cargando conexiones...</div>
                  ) : conexiones.length === 0 ? (
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
                          {conexion.modelo_version && (
                            <p><strong>Versión:</strong> {conexion.modelo_version}</p>
                          )}
                        </div>
                      </div>
                    ))
                  )}
                </div>
              ) : (
                <div className="agregar-conexion">
                  <p>Funcionalidad de agregar conexión en desarrollo...</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Renderizar el componente
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<DataSageHome />);
