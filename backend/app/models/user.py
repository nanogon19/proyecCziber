from typing import Dict
from sqlalchemy import Column, String, ForeignKey
from backend.app.extensions import db
import uuid

class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    recover = db.Column(db.String, nullable=True)
    level = db.Column(db.String, nullable=False)  
    active = db.Column(db.Boolean, default=True, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False, nullable=False)

    company_id = db.Column(db.String, db.ForeignKey('companies.id_emp'), nullable=False)

    company = db.relationship("Company", back_populates="empleados")
    consultas = db.relationship("Query", back_populates="usuario", lazy=True)

    def get_empresa_id(self) -> str:
        return self.company_id
    
    def get_id(self) -> str:
        return self.id_user

    def set_password(self, new_password: str):
        self.password = new_password

    def get_models(self) -> list[str]:
        """Devuelve los IDs de los modelos accesibles por el usuario a través de su empresa"""
        return [model.id_model for model in self.company.models]

    def get_models(self) -> list[str]:
        if not self.company:
            return []
        return  [model.id_model for model in self.company.models]

    def get_consultas(self) -> list[str]:
        """Devuelve una lista de IDs de consultas del usuario"""
        return [consulta.id for consulta in self.consultas]

    def get_consulta(self, consulta_id: str):
        """Busca una consulta del usuario por su ID"""
        return next((c for c in self.consultas if c.id_query == consulta_id), None)

    def get_total_tokens(self) -> int:
        """Suma todos los tokens usados en consultas del usuario"""
        return sum((c.tokens_in or 0) + (c.tokens_out or 0) for c in self.consultas)    