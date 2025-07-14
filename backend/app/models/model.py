from typing import Dict
from backend.app.extensions import db
import uuid

class Model(db.Model):
    __tablename__ = "models"

    id_model = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = db.Column(db.String, nullable=False)
    documentacion = db.Column(db.Text)
    version = db.Column(db.String)

    company_id = db.Column(db.String, db.ForeignKey('companies.id_emp'))
    app_id     = db.Column(db.String, db.ForeignKey("applications.id_app"), nullable=False)

    # Relaciones bidireccionales
    company     = db.relationship("Company", back_populates="models")       # si usás 'empresa_id'
    application  = db.relationship("Application", back_populates="models")    # verifica nombre de clase
    consultas   = db.relationship("Query", back_populates="model")          # relación 1:N
    conections = db.relationship("Conection", back_populates="model")      # relación 1:N

    # Métodos
    def obtener_contexto(self) -> str:
        return self.documentacion

    def set_contexto(self, contexto: str, version: str):
        self.documentacion = contexto
        self.version = version

    def to_dict(self) -> dict:
        return {
            "id_model": self.id_model,
            "nombre": self.nombre,
            "documentacion": self.documentacion,
            "version": self.version,
            "empresa_id": self.empresa_id,
            "app_id": self.app_id
        }

    def get_id(self) -> str:
        return self.id_model
