from typing import Dict
from backend.app.models.query import Query

class Model:
    def __init__(self, id: str, nombre: str, documentacion: str, version: str, empresa_id: str, app_id: str):
        self.id = id
        self.nombre = nombre
        self.documentacion = documentacion
        self.version = version

        self.empresa_id = empresa_id
        self.app_id = app_id
        self.consultas = dict[str, Query] = {}

    def obtener_contexto(self) -> str:
        return self.documentacion
    
    def set_contexto(self, contexto: str, version: str):
        self.documentacion = contexto
        self.version = version

