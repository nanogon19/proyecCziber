from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from .config import Config
from .extensions import db, migrate
from .routes import register_routes

load_dotenv()  # carga variables de entorno (.env)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- CORS: permitir solo tu front en GitHub Pages ---
    CORS(
        app,
        resources={r"/*": {  # TODAS las rutas (incluye /health y /cziber/*)
            "origins": ["https://nanogon19.github.io"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }},
    )

    # --- Ruta de prueba ---
    @app.route("/")
    def home():
        return {"message": "Flask server is running!", "status": "OK"}

    @app.route("/health")
    def health():
        return {"status": "healthy", "app": "datasage"}

    # --- DB & Migrations ---
    try:
        db.init_app(app)
        migrate.init_app(app, db)
    except Exception as e:
        print(f"Warning: Database initialization failed: {e}")

    # --- Registrar rutas ---
    try:
        register_routes(app)
    except Exception as e:
        print(f"Warning: Routes registration failed: {e}")

    return app
