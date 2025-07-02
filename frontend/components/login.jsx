function Login() {
  return (
    <div className="login-container">
        <h2 className="login-title">Iniciar Sesión</h2>
        <div className="input-group">
            <span className="icon"></span>
            <input type="text" placeholder="Usuario o Correo" />
        </div>
        <div className="input-group">
            <span className="icon"></span>
            <input type="password" placeholder="Contraseña" />
        </div>
        <a href="/forgot-password" className="forgot-password-link">¿Olvidaste tu contraseña?</a>
        <button className="login-button">Iniciar Sesión</button>
        <hr />
        <div className="register-link">
            <span>¿No tienes cuenta? </span>
            <a href="../pages/register.html">Regístrate</a>
        </div>
        <hr />
        <div className="social-login">
            <button className="google-button">Iniciar con Google</button>
        </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<Login />);
