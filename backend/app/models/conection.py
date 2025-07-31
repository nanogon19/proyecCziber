from backend.app.extensions import db
from backend.app.utils.security import EncryptionManager
import uuid

encryptor = EncryptionManager()

class Conection(db.Model):
    __tablename__ = "conections"

    id_conn = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    ip_enc = db.Column("ip", db.String, nullable=False)
    port_enc = db.Column("port", db.String, nullable=False)
    user_enc = db.Column("user", db.String, nullable=False)
    password_enc = db.Column("password", db.String, nullable=False)
    # database_enc = db.Column("database_name", db.String, nullable=True)  # Comentado temporalmente

    app_id   = db.Column(db.String, db.ForeignKey("applications.id_app"), nullable=False)
    company_id = db.Column(db.String, db.ForeignKey('companies.id_emp'))
    model_id = db.Column(db.String, db.ForeignKey("models.id_model"), nullable=False)

    # Relaciones
    application = db.relationship("Application", back_populates="conections")
    company    = db.relationship("Company", back_populates="conections")
    model      = db.relationship("Model", back_populates="conections")

    # Constructor personalizado con cifrado
    def __init__(self, ip, port, user, password, database_name=None, app_id=None, company_id=None, model_id=None):
        self.ip_enc = encryptor.encrypt_data(ip)
        self.port_enc = encryptor.encrypt_data(str(port))
        self.user_enc = encryptor.encrypt_data(user)
        self.password_enc = encryptor.encrypt_data(password)
        
        # Solo encriptar database_name si se proporciona y existe la columna
        # if database_name:
        #     self.database_enc = encryptor.encrypt_data(database_name)
        # else:
        #     self.database_enc = None
            
        self.app_id = app_id
        self.company_id = company_id
        self.model_id = model_id

    # Métodos de acceso a datos desencriptados
    def obtener_ip(self) -> str:
        return encryptor.decrypt_data(self.ip_enc)
    
    def obtener_port(self) -> int:
        return int(encryptor.decrypt_data(self.port_enc))

    def obtener_usuario(self) -> str:
        return encryptor.decrypt_data(self.user_enc)
    
    def obtener_clave(self) -> str:
        return encryptor.decrypt_data(self.password_enc)
    
    def obtener_database(self) -> str:
        # Temporalmente retornamos un valor fijo hasta resolver el problema de la columna
        return "Gamma_CZ"  # Cambia esto por el nombre de tu base de datos

    def to_dict(self) -> dict:
        return {
            "id_conn": self.id_conn,
            "ip": self.obtener_ip(),
            "port": self.obtener_port(),
            "user": self.obtener_usuario(),
            "password": self.obtener_clave(),
            "database": self.obtener_database(),
            "app_id": self.app_id,
            "company_id": self.company_id,
            "model_id": self.model_id
        }
