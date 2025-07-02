function Register() {
  return (
    <div className="register-container">
        <h2 className="register-title">Registrarse</h2>
        <div className="input-group">
            <input type="text" placeholder="Nombre completo" />
        </div>
        <div className="input-group">
            <input type="email" placeholder="Correo electrónico" />
        </div>
        <div className="input-group">
            <input type="text" placeholder="Codigo de Empresa" />
            </div>
        <div className="input-group">
            <input type="password" placeholder="Contraseña" />
        </div>
        <div className="input-group">
            <input type="password" placeholder="Confirmar contraseña" />
        </div>
        <button className="register-button">Registrarse</button>
        <div className="register-link">
            <span>¿Ya tienes cuenta? </span>
            <a href="../pages/login.html">Iniciar sesión</a>
        </div>
        <hr />
        <div className="social-login">
            <button className="google-button">Registrarse con Google</button>
        </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(<Register />);

