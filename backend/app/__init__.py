from flask import Flask, send_from_directory
from flask_cors import CORS
from pathlib import Path
from dotenv import load_dotenv
import os

from .config import Config
from .extensions import db, migrate
from .models import User, Company, Application, Model, Query  # mantiene modelos importados
from .routes import register_routes

load_dotenv()  # carga .env (incluye DATABASE_URL)

def create_app():
    # Ruta a 'dist' (Vite)
    DIST_DIR = Path(__file__).resolve().parents[2] / "proyectoCziber" / "dist"

    app = Flask(
        __name__,
        static_folder=str(DIST_DIR),
        static_url_path=""
    )
    app.config.from_object(Config)

    # --- CORS (ajustá dominios cuando tengas prod) ---
    CORS(
        app,
        origins=[
            "http://127.0.0.1:5500",
            "http://localhost:5500",
            "http://localhost:5000",
            "http://127.0.0.1:5000",
        ],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization"],
    )

    # --- DB & Migrations ---
    # Requiere que DATABASE_URL esté en .env con formato:
    # postgresql+psycopg2://USER:PASSWORD@HOST/DB?sslmode=require
    db.init_app(app)
    migrate.init_app(app, db)

    # Rutas de API
    register_routes(app)

    # --- SPA catch-all ---
    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def spa(path):
        requested = Path(app.static_folder) / path
        if path and requested.exists():
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, "index.html")

    # (Opcional) Comprobación de conexión a DB al arranque
    # Útil mientras configurás Neon; podés borrar esto luego.
    if app.config.get("SQLALCHEMY_DATABASE_URI"):
        from sqlalchemy import text
        with app.app_context():
            try:
                db.session.execute(text("SELECT 1"))
                # print("✅ Conexión a DB OK")
            except Exception as e:
                print(f"⚠️ Error conectando a la DB: {e}")

    return app
