import {
  useState,
  useEffect,
  useMemo,
  useCallback,
  useRef,
  memo,
} from "react";
import type { FormEvent, ChangeEvent } from "react";
import "../styles/consulta.css";
import "gridjs/dist/theme/mermaid.min.css";
import { Grid } from "gridjs";
import * as XLSX from "xlsx";

type Conexion = {
  id_conn: number;
  nombre?: string;
  ip: string;
  puerto?: number;
  port?: number;
  database: string;
  empresa_nombre?: string;
  aplicacion_nombre?: string;
  modelo_nombre?: string;
  modelo_version?: string;
};

type Resultado = {
  id: number;
  prompt: string;
  columns: string[];
  data: unknown[][];
  timestamp: string;
};

const API = 'https://croatia-pursue-abstracts-whale.trycloudflare.com';
const api = (path: string) => `${API}${path.startsWith('/') ? '' : '/'}${path}`;

/** Grid de resultados (gridjs) */
const DataGrid = memo(function DataGrid({
  columns,
  data,
}: {
  columns: string[];
  data: unknown[][];
}) {
  const gridRef = useRef<HTMLDivElement | null>(null);
  const gridInstanceRef = useRef<any>(null);

  useEffect(() => {
    if (!gridRef.current) return;

    // destruir instancia previa si existe
    if (gridInstanceRef.current) {
      try {
        gridInstanceRef.current.destroy();
      } catch {
        /* ignore */
      }
    }
    gridRef.current.innerHTML = "";

    try {
      const grid = new Grid({
        columns,
        data: data as any[][], // puede ser [], gridjs lo soporta
        pagination: { limit: 10 }, // ✅ OBLIGATORIO: pagination:true y limit
        search: true,
        sort: true,
        resizable: true,
        fixedHeader: true,
        height: "400px",
        width: "100%",
        style: {
          table: {
            "border-radius": "10px",
            overflow: "hidden",
            "box-shadow": "0 2px 10px rgba(0, 0, 0, 0.1)",
            width: "100%",
          },
          th: {
            "background-color": "#f4b142",
            color: "#fff",
            "text-align": "center",
            padding: "12px",
          },
          td: { "text-align": "center", padding: "8px" },
        } as any,
      });

      grid.render(gridRef.current as HTMLElement);
      gridInstanceRef.current = grid;
    } catch (err) {
      console.error("Error rendering grid:", err);
      gridRef.current.innerHTML =
        '<p style="color: red; padding: 20px;">Error al cargar la tabla.</p>';
    }

    return () => {
      if (gridInstanceRef.current) {
        try {
          gridInstanceRef.current.destroy();
        } catch {
          /* ignore */
        }
      }
    };
  }, [columns, data]); // cuando cambian columnas/datos, re-render

  return (
    <div className="grid-container">
      <div ref={gridRef} />
    </div>
  );
});


export default function Home() {
  // ---- state ----
  const [prompt, setPrompt] = useState("");
  const [results, setResults] = useState<Resultado[]>([]);
  const [showConexiones, setShowConexiones] = useState(false);
  const [conexiones, setConexiones] = useState<Conexion[]>([]);
  const [loading, setLoading] = useState(false);
  const [queryLoading, setQueryLoading] = useState(false);
  const [currentView, setCurrentView] = useState<"listar" | "agregar">("listar");
  const [formData, setFormData] = useState({
    ip: "",
    port: "",
    database_name: "",
  });
  const [tempConnectionData, setTempConnectionData] = useState<any>(null);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showCreateConnectionModal, setShowCreateConnectionModal] =
    useState(false);
  const [selectedConnection, setSelectedConnection] = useState<Conexion | null>(
    null
  );
  const [loginData, setLoginData] = useState({ username: "", password: "" });
  const [currentConnectionString, setCurrentConnectionString] = useState("");

  // ---- helpers ----
  const scrollResultBoxBottom = () => {
    const box = document.getElementById("resultBox");
    if (box) box.scrollTop = box.scrollHeight;
  };

  // ---- effects ----
  useEffect(() => {
    loadConexiones();
  }, []);

  // ---- API calls / actions ----
  const loadConexiones = async () => {
    try {
      const r = await fetch(api(`/cziber/listar_todas_conexiones`), {
        credentials: "same-origin",
      });
      const data = await r.json();
      setConexiones(data.conexiones || []);
    } catch (e) {
      console.error("Error al cargar conexiones:", e);
      alert("Error al cargar las conexiones disponibles");
    }
  };

  const handleSelectConnection = (conexion: Conexion) => {
    setSelectedConnection(conexion);
    setShowConexiones(false);
    setShowLoginModal(true);
  };

  const handleLogin = async (e: FormEvent) => {
    e.preventDefault();
    if (!selectedConnection || !loginData.username || !loginData.password) {
      alert("Complete todos los campos");
      return;
    }

    try {
      const r = await fetch(api(`/cziber/login_conexion`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({
          conexion_id: selectedConnection.id_conn,
          username: loginData.username,
          password: loginData.password,
        }),
      });
      const result = await r.json();

      if (result.error) {
        alert(result.error);
        return;
      }
      if (result.connection_string) {
        setCurrentConnectionString(result.connection_string);
        setShowLoginModal(false);
        setLoginData({ username: "", password: "" });
        alert(
          `Conectado exitosamente a ${selectedConnection.ip}:${
            selectedConnection.puerto ?? selectedConnection.port
          }/${selectedConnection.database}`
        );
      }
    } catch (e) {
      console.error("Error al conectar:", e);
      alert("Error al intentar conectar a la base de datos");
    }
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;

    if (!currentConnectionString && !selectedConnection) {
      alert("Debe seleccionar y conectarse a una base de datos primero");
      setShowConexiones(true);
      return;
    }

    setQueryLoading(true);
    setTimeout(scrollResultBoxBottom, 50);

    try {
      const body: any = { prompt };
      if (currentConnectionString) {
        body.connection_string = currentConnectionString;
      } else if (selectedConnection && loginData.username && loginData.password) {
        body.conexion_id = selectedConnection.id_conn;
        body.username = loginData.username;
        body.password = loginData.password;
      }

      const r = await fetch(api(`/cziber/consultar`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify(body),
      });

      const json = await r.json();
      if (json.mensaje) {
        alert(json.mensaje);
        setQueryLoading(false);
        return;
      }

      const { columns, data } = json;
      const newResult: Resultado = {
        id: Date.now(),
        prompt,
        columns,
        data,
        timestamp: new Date().toLocaleString(),
      };

      setResults((prev) => [...prev, newResult]);
      setPrompt("");
      setTimeout(scrollResultBoxBottom, 100);
    } catch (e) {
      console.error("Error al enviar la consulta:", e);
      alert("Error al enviar la consulta. Por favor, inténtelo de nuevo.");
    } finally {
      setQueryLoading(false);
    }
  };

  const exportToExcel = useCallback((result: Resultado) => {
    const worksheetData = [result.columns, ...result.data];
    const worksheet = XLSX.utils.aoa_to_sheet(worksheetData as any[]);
    const workbook = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(workbook, worksheet, "Resultado");
    const filename = `consulta_${Date.now()}.xlsx`;
    XLSX.writeFile(workbook, filename);
  }, []);

  const memoizedResults = useMemo(() => results, [results]);

  const listarConexiones = async () => {
    setLoading(true);
    try {
      const r = await fetch(api(`/cziber/listar_todas_conexiones`), {
        method: "GET",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
      });
      if (r.ok) {
        const data = await r.json();
        setConexiones(data.conexiones || []);
      } else {
        const err = await r.json();
        alert("Error al obtener conexiones: " + err.error);
      }
    } catch (e) {
      console.error("Error al conectar con el backend:", e);
      alert("No se pudo conectar con el servidor");
    }
    setLoading(false);
  };

  const handleSubmitConexion = async (e: FormEvent) => {
    e.preventDefault();
    const requiredFields = ["ip", "port", "database_name"] as const;
    for (const f of requiredFields) {
      if (!formData[f as keyof typeof formData]) {
        alert(`Por favor complete el campo: ${f}`);
        return;
      }
    }
    setTempConnectionData(formData);
    setShowCreateConnectionModal(true);
    setLoginData({ username: "", password: "" });
  };

  const handleCreateConnectionWithCredentials = async (e: FormEvent) => {
    e.preventDefault();
    if (!tempConnectionData || !loginData.username || !loginData.password) {
      alert("Complete todos los campos incluyendo usuario y contraseña");
      return;
    }
    try {
      const payload = {
        ...tempConnectionData,
        username: loginData.username,
        password: loginData.password,
      };
      const r = await fetch(api(`/cziber/agregar_conexion`), {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify(payload),
      });

      if (r.ok) {
        const data = await r.json();
        let msg = "Conexión creada exitosamente!";
        if (data.defaults_used) {
          msg += `\n\nValores asignados automáticamente:`;
          msg += `\n• Empresa: ${data.defaults_used.empresa}`;
          msg += `\n• Aplicación: ${data.defaults_used.aplicacion}`;
          msg += `\n• Modelo: ${data.defaults_used.modelo}`;
        }
        alert(msg);

        setFormData({ ip: "", port: "", database_name: "" });
        setTempConnectionData(null);
        setLoginData({ username: "", password: "" });
        setShowCreateConnectionModal(false);
        setCurrentView("listar");
        listarConexiones();
      } else {
        const err = await r.json();
        alert("Error al crear conexión: " + err.error);
      }
    } catch (e) {
      console.error("Error creando conexión:", e);
      alert("Error al conectar con el servidor");
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  // ---- UI ----
  return (
    <div className="app-container">
      {/* Sidebar */}
      <div className="sidebar">
        <header>
          <p
            className="conexiones"
            onClick={() => {
              setShowConexiones(true);
              setCurrentView("listar");
              listarConexiones();
            }}
            style={{ cursor: "pointer" }}
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
            results.map((r) => (
              <div key={r.id} className="query-item">
                <div className="query-text">
                  {r.prompt.length > 50 ? `${r.prompt.substring(0, 50)}...` : r.prompt}
                </div>
                <div className="query-time">{r.timestamp}</div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Main */}
      <div className="main-container">
        <header className="header">
          <div className="logo">DATASAGE</div>
          {/* ✅ logo desde /public */}
          <img src="/logo.png" alt="Logo" className="logo-img" />
        </header>

        {/* Resultados */}
        <div className="result-box" id="resultBox">
          {memoizedResults.length === 0 && !queryLoading ? (
            <div className="no-results">
              <p>No hay consultas realizadas aún. Escribe una consulta para comenzar.</p>
            </div>
          ) : (
            <>
              {memoizedResults.map((res) => (
                <div key={res.id} className="result-item">
                  <div className="result-header">
                    <h3>Consulta: {res.prompt}</h3>
                    <button className="export-btn" onClick={() => exportToExcel(res)}>
                      Exportar a Excel
                    </button>
                  </div>
                  <DataGrid columns={res.columns} data={res.data} />
                </div>
              ))}
              {queryLoading && (
                <div className="loading-query">
                  <div className="loading-spinner" />
                  <p>Procesando consulta...</p>
                </div>
              )}
            </>
          )}
        </div>

        {/* Form consulta */}
        <form onSubmit={handleSubmit} className="input-area">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Escriba su consulta aquí..."
            rows={3}
            disabled={queryLoading}
          />
          <button type="submit" disabled={!prompt.trim() || queryLoading}>
            {queryLoading ? "Procesando..." : "Enviar"}
          </button>
        </form>
      </div>

      {/* Modal Conexiones */}
      {showConexiones && (
        <div className="modal-conexiones">
          <div className="contenido-conexiones">
            <span className="cerrar" onClick={() => setShowConexiones(false)}>
              &times;
            </span>
            <h2>Conexiones</h2>

            <div className="opciones-conexiones">
              <p
                className={`conexion-op ${currentView === "listar" ? "active" : ""}`}
                onClick={() => {
                  setCurrentView("listar");
                  listarConexiones();
                }}
              >
                Listar conexiones
              </p>
              <p
                className={`conexion-op ${currentView === "agregar" ? "active" : ""}`}
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
                    <>
                      <p style={{ marginBottom: "15px", color: "#666" }}>
                        Selecciona una conexión para conectarte:
                      </p>
                      {conexiones.map((conexion, index) => {
                        const selected =
                          selectedConnection?.id_conn === conexion.id_conn;
                        return (
                          <div
                            key={conexion.id_conn}
                            className="conexion-item selectable"
                            onClick={() => handleSelectConnection(conexion)}
                            style={{
                              cursor: "pointer",
                              border: selected ? "2px solid #007bff" : "1px solid #ddd",
                              backgroundColor: selected ? "#f0f8ff" : "white",
                            }}
                          >
                            <div className="conexion-header">
                              <h4>
                                {conexion.nombre || `Conexión #${index + 1}`}
                              </h4>
                              <span className="conexion-id">{conexion.id_conn}</span>
                            </div>
                            <div className="conexion-details">
                              <p>
                                <strong>IP:</strong> {conexion.ip}
                              </p>
                              <p>
                                <strong>Puerto:</strong>{" "}
                                {conexion.puerto ?? conexion.port}
                              </p>
                              <p>
                                <strong>Base de Datos:</strong> {conexion.database}
                              </p>
                              {conexion.empresa_nombre && (
                                <p>
                                  <strong>Empresa:</strong> {conexion.empresa_nombre}
                                </p>
                              )}
                              {conexion.aplicacion_nombre && (
                                <p>
                                  <strong>Aplicación:</strong>{" "}
                                  {conexion.aplicacion_nombre}
                                </p>
                              )}
                              {conexion.modelo_nombre && (
                                <p>
                                  <strong>Modelo:</strong> {conexion.modelo_nombre}
                                </p>
                              )}
                              {conexion.modelo_version && (
                                <p>
                                  <strong>Versión:</strong> {conexion.modelo_version}
                                </p>
                              )}
                            </div>
                            <div
                              style={{
                                marginTop: "10px",
                                fontSize: "12px",
                                color: "#007bff",
                              }}
                            >
                              Clic para seleccionar esta conexión
                            </div>
                          </div>
                        );
                      })}
                    </>
                  )}
                </div>
              ) : (
                <div className="agregar-conexion">
                  <h3>Agregar Nueva Conexión</h3>
                  <p style={{ marginBottom: "15px", color: "#666", fontSize: "14px" }}>
                    ℹ️ La empresa, aplicación y modelo se asignarán automáticamente
                    usando los primeros registros disponibles en el sistema.
                  </p>

                  <form onSubmit={handleSubmitConexion} className="form-conexion">
                    <div className="form-row">
                      <div className="form-group">
                        <label htmlFor="ip">Dirección IP:</label>
                        <input
                          type="text"
                          id="ip"
                          name="ip"
                          value={formData.ip}
                          onChange={handleInputChange}
                          placeholder="192.168.1.100"
                          required
                        />
                      </div>
                      <div className="form-group">
                        <label htmlFor="port">Puerto:</label>
                        <input
                          type="number"
                          id="port"
                          name="port"
                          value={formData.port}
                          onChange={handleInputChange}
                          placeholder="5432"
                          required
                        />
                      </div>
                    </div>

                    <div className="form-row">
                      <div className="form-group">
                        <label htmlFor="database_name">Nombre de Base de Datos:</label>
                        <input
                          type="text"
                          id="database_name"
                          name="database_name"
                          value={formData.database_name}
                          onChange={handleInputChange}
                          placeholder="nombre_database"
                          required
                        />
                      </div>
                    </div>

                    <div className="form-buttons">
                      <button type="submit" className="btn-submit">
                        Continuar con Credenciales
                      </button>
                      <button
                        type="button"
                        className="btn-cancel"
                        onClick={() => setCurrentView("listar")}
                      >
                        Cancelar
                      </button>
                    </div>
                  </form>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Modal Login conexión existente */}
      {showLoginModal && selectedConnection && (
        <div className="modal-conexiones">
          <div className="contenido-conexiones" style={{ maxWidth: "400px" }}>
            <span
              className="cerrar"
              onClick={() => {
                setShowLoginModal(false);
                setSelectedConnection(null);
                setLoginData({ username: "", password: "" });
              }}
            >
              &times;
            </span>
            <h2>Conectar a Base de Datos</h2>

            <div
              style={{
                marginBottom: "20px",
                padding: "10px",
                backgroundColor: "#f8f9fa",
                borderRadius: "4px",
              }}
            >
              <p>
                <strong>Conexión:</strong> {selectedConnection.nombre || "Sin nombre"}
              </p>
              <p>
                <strong>Servidor:</strong> {selectedConnection.ip}:
                {selectedConnection.puerto ?? selectedConnection.port}
              </p>
              <p>
                <strong>Base de Datos:</strong> {selectedConnection.database}
              </p>
            </div>

            <form onSubmit={handleLogin} className="form-conexion">
              <div className="form-group">
                <label>Usuario de Base de Datos:</label>
                <input
                  type="text"
                  value={loginData.username}
                  onChange={(e) =>
                    setLoginData((prev) => ({ ...prev, username: e.target.value }))
                  }
                  placeholder="Ingrese su usuario"
                  required
                />
              </div>
              <div className="form-group">
                <label>Contraseña:</label>
                <input
                  type="password"
                  value={loginData.password}
                  onChange={(e) =>
                    setLoginData((prev) => ({ ...prev, password: e.target.value }))
                  }
                  placeholder="Ingrese su contraseña"
                  required
                />
              </div>
              <div className="form-buttons">
                <button type="submit" className="btn-submit">
                  Conectar
                </button>
                <button
                  type="button"
                  className="btn-cancel"
                  onClick={() => {
                    setShowLoginModal(false);
                    setSelectedConnection(null);
                    setLoginData({ username: "", password: "" });
                  }}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Modal credenciales nueva conexión */}
      {showCreateConnectionModal && tempConnectionData && (
        <div className="modal-conexiones">
          <div className="contenido-conexiones" style={{ maxWidth: "450px" }}>
            <span
              className="cerrar"
              onClick={() => {
                setShowCreateConnectionModal(false);
                setTempConnectionData(null);
                setLoginData({ username: "", password: "" });
              }}
            >
              &times;
            </span>
            <h2>Credenciales de Base de Datos</h2>

            <div
              style={{
                marginBottom: "20px",
                padding: "10px",
                backgroundColor: "#f8f9fa",
                borderRadius: "4px",
              }}
            >
              <p>
                <strong>Nueva Conexión:</strong>
              </p>
              <p>
                <strong>Servidor:</strong> {tempConnectionData.ip}:{tempConnectionData.port}
              </p>
              <p>
                <strong>Base de Datos:</strong> {tempConnectionData.database_name}
              </p>
            </div>

            <p style={{ marginBottom: "15px", color: "#666", fontSize: "14px" }}>
              Para completar la creación de la conexión, proporcione las credenciales:
            </p>

            <form onSubmit={handleCreateConnectionWithCredentials} className="form-conexion">
              <div className="form-group">
                <label>Usuario de Base de Datos:</label>
                <input
                  type="text"
                  value={loginData.username}
                  onChange={(e) =>
                    setLoginData((prev) => ({ ...prev, username: e.target.value }))
                  }
                  placeholder="Ingrese usuario de la base de datos"
                  required
                />
              </div>
              <div className="form-group">
                <label>Contraseña:</label>
                <input
                  type="password"
                  value={loginData.password}
                  onChange={(e) =>
                    setLoginData((prev) => ({ ...prev, password: e.target.value }))
                  }
                  placeholder="Ingrese contraseña de la base de datos"
                  required
                />
              </div>
              <div className="form-buttons">
                <button type="submit" className="btn-submit">
                  Crear Conexión
                </button>
                <button
                  type="button"
                  className="btn-cancel"
                  onClick={() => {
                    setShowCreateConnectionModal(false);
                    setTempConnectionData(null);
                    setLoginData({ username: "", password: "" });
                  }}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
