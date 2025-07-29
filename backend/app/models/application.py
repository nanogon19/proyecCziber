from typing import List
from uuid import uuid4

from backend.app.models.asoc import company_application
from backend.app.extensions import db

class Application(db.Model):
    __tablename__ = "applications"  # ← corregido

    id_app = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    nombre = db.Column(db.String, nullable=False)

    company_id = db.Column(db.String, db.ForeignKey('companies.id_emp'))

    # Relaciones
    models     = db.relationship("Model", back_populates="application")       # relación 1:N
    conections  = db.relationship("Conection", back_populates="application")   # relación 1:N
    company     = db.relationship("Company", secondary=company_application, back_populates="application")   # relación N:1

    # Métodos de ayuda
    def agregar_modelo(self, modelo):
        self.models.append(modelo)

    def obtener_modelo(self, modelo_id: str):
        return next((m for m in self.models if m.id_model == modelo_id), None)

    def obtener_modelos(self) -> List:
        return self.models

    def agregar_conexion(self, conexion):
        self.conections.append(conexion)

    def agregar_empresa(self, empresa):
        self.company.append(empresa)
