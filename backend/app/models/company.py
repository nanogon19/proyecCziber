from typing import List
from uuid import uuid4

from backend.app.models.asoc import company_application
from backend.app.extensions import db

class Company(db.Model):
    __tablename__ = "companies"

    id_emp = db.Column(db.String, primary_key=True, default=lambda: str(uuid4()))
    name   = db.Column(db.String, nullable=False)
    rut    = db.Column(db.String)
    logo   = db.Column(db.String)  # Ruta o nombre del archivo

    # Relaciones
    empleados     = db.relationship("User", back_populates="company")
    models        = db.relationship("Model", back_populates="company")        # ← nombre corregido
    application  = db.relationship("Application", secondary=company_application, back_populates="company")  # ← corregir nombre en Application
    conections    = db.relationship("Conection", back_populates="company")

    def __repr__(self):
        return f"<Company {self.name}>"

    # Métodos de ayuda
    def agregar_empleado(self, empleado):
        self.empleados.append(empleado)

    def agregar_aplicacion(self, app):
        self.application.append(app)

    def agregar_modelo(self, modelo):
        self.models.append(modelo)

    def agregar_conexion(self, conexion):
        self.conections.append(conexion)

    def obtener_empleados(self) -> List[str]:
        return [empleado.id_user for empleado in self.empleados]
    
    def obtener_admins(self) -> List[str]:
        return [empleado.id_user for empleado in self.empleados if empleado.isAdmin]

    def obtener_empleado(self, id_user: str):
        return next((e for e in self.empleados if e.id_user == id_user), None)

    def obtener_aplicaciones(self) -> List[str]:
        return [app.id_app for app in self.application]

    def obtener_aplicacion(self, app_id: str):
        return next((a for a in self.application if a.id_app == app_id), None)

    def get_tokens(self) -> int:
        return sum(e.get_total_tokens() for e in self.empleados)
