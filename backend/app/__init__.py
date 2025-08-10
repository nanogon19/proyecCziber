from flask import Flask, send_from_directory, jsonify
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
    # Crear app Flask básica
    app = Flask(__name__)
    app.config.from_object(Config)

    # --- CORS configurado para GitHub Pages y desarrollo local ---
    CORS(app, origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500", 
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "http://localhost:3000",  # Vite dev server
        "https://nanogon19.github.io",  # Tu GitHub Pages
        "https://datasage-k86t.onrender.com",  # Tu backend en Render
        "*"  # Temporalmente permitir todo para debugging
    ])

    # --- Ruta de prueba básica ---
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

    # Rutas de API
    try:
        register_routes(app)
    except Exception as e:
        print(f"Warning: Routes registration failed: {e}")

    return app
