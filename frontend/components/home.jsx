function Home() {
  const [messages, setMessages] = React.useState([]);
  const [input, setInput] = React.useState("");
  const [selectedDB, setSelectedDB] = React.useState(null);
  const [showDropdown, setShowDropdown] = React.useState(false);
  const [currentPage, setCurrentPage] = React.useState("home");
  const hoverTimeout = React.useRef(null);

    const handleSend = () => {
        if (!input.trim()) return;

        setMessages((prev) => [...prev, { sender: "user", text: input }]);
        setInput("");

        setTimeout(() => {
            const dbPrefix = selectedDB ? `<span class="db-badge">📁 ${selectedDB}</span><br/>` : "";
            const respuesta = `${dbPrefix}Esta es una respuesta simulada de la IA.`;
            setMessages((prev) => [
            ...prev,
            { sender: "bot", text: respuesta, isHTML: true },
                ]);
        }, 1000);
    };

    const handleKeyDown = (e) => {
        if (e.key === "Enter") handleSend();
    };

    const handleSelectDB = (dbName) => {
        setSelectedDB(dbName);
        setShowDropdown(false); // Opcional: cerrar menú al hacer clic
    };

    const handleMouseEnter = () => {
        clearTimeout(hoverTimeout.current);
        setShowDropdown(true);
    };

    const handleMouseLeave = () => {
        hoverTimeout.current = setTimeout(() => {
        setShowDropdown(false);
        }, 300);
    };

  return (
        <div className="main-layout">
            <aside className="sidebar">
                <div className="profile-section">
                    <button onClick={() => setCurrentPage("profile")}> Perfil Ejemplo </button>
                </div>
                <div className="previous-queries">
                    <h4>Consultas Anteriores</h4>
                    {messages
                        .filter((m) => m.sender === "user")
                        .map((msg, i) => (
                            <div key={i} className="query-item">{msg.text}</div>
                        ))}
                </div>
            </aside>

            <section className="chat-area">
                <div className="chat-header">
                        Chat con IA
                </div>
                <div className="chat-messages">
                        {messages.map((msg, i) => (
                            <div
                                key={i}
                                className={`message ${msg.sender}`}
                                {...(msg.isHTML ? {dangerouslySetInnerHTML: {__html: msg.text }} : {children: msg.text })}
                            />
                        ))}
                </div>
                <div className="chat-input">
                    <div
                        className="database-dropdown"
                        onMouseEnter={handleMouseEnter}
                        onMouseLeave={handleMouseLeave}
                    >
                    Bases de Datos
                    {showDropdown && (
                        <div className="dropdown-list">
                            {["bd01", "bd02", "bd03", "bd04"].map((bd) => (
                            <div key={bd} onClick={() => handleSelectDB(bd)}>{bd}</div>
                            ))}
                        </div>
                    )}
                    </div>
                </div>
                <div className="input-area">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyDown}
                        placeholder="Escribe tu mensaje..."
                    />
                    <button onClick={handleSend}>Enviar</button>
                </div> 
            </section>
        </div>

        
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Home />);
