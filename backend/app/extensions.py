from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from sqlalchemy import create_engine

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
jwt = JWTManager()
cors = CORS()

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