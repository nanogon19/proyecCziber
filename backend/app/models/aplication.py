from typing import Dict

from backend.app.models.model import Model
from backend.app.models.company import Company
from backend.app.models.conection import Conection 

class Aplication:
    def __init__(self, id: str, nombre: str, typebd: str, conexion: str, usuario: str, clave: str):
        self.id = id
        self.nombre = nombre

        self.empresas: dict[str, Company] = {}
        self.modelos: dict[str, Model] = {}
        self.conections: dict[str, Conection] = {}

    def agregar_modelo(self, modelo: Model):
        self.modelos[modelo.id] = modelo

    def obtener_modelo(self, modelo_id: str) -> Model:
        return self.modelos.get(modelo_id)
    
    def obtener_modelos(self) -> list[Model]:
        return self.modelos
    
    def agregar_empresa(self, empresa: Company):
        self.empresas[empresa.id_emp] = empresa

    def agregar_conexion(self, conexion: Conection):
        self.conections[conexion.id] = conexion
    

    
