from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv
load_dotenv()

from .config import Config
from .extensions import db, migrate
from .models import User, Company, Application, Model, Query
from .routes import register_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configuración CORS más específica
    CORS(app, origins=["http://127.0.0.1:5500", "http://localhost:5500"], 
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"])

    db.init_app(app)
    migrate.init_app(app, db)
    
    register_routes(app)

    return app