from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import create_engine
import os

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()
cors = CORS()

# Usar variables de entorno para la conexión
# Estas credenciales deberían estar en el archivo .env o variables de entorno de Render
connection_string = os.getenv("DATABASE_URL")

if connection_string:
    engine = create_engine(connection_string, connect_args={"timeout": 5})
else:
    # Fallback para desarrollo local con credenciales hardcodeadas
    # ⚠️ SOLO PARA DESARROLLO - NO usar en producción
    user = "igonzalez"
    password = "Zig1-Red6{Voc1"
    ip = "192.168.0.5:1433"
    name_db = "Gamma_CZ"

    connection_string = (
        "mssql+pyodbc://igonzalez:Zig1-Red6{Voc1@192.168.0.5,1433/Gamma_CZ"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes"
        "&Encrypt=no"
    )
    engine = create_engine(connection_string, connect_args={"timeout": 5})