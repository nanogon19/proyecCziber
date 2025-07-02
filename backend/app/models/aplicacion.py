from typing import Dict
from app.models.modelo_de_datos import ModelDB
from app.utils.security import EncryptionManager

encryptor = EncryptionManager()

class Aplicacion:
    def __init__(self, id: str, nombre: str, conexion: str, usuario: str, clave: str):
        self.id = id
        self.nombre = nombre
        self.conexion = encryptor.encrypt(conexion)
        self.usuario = encryptor.encrypt(usuario)
        self.clave = encryptor.encrypt(clave)

        self.modelos: Dict[str, ModelDB] = {}

    def agregar_modelo(self, modelo: ModelDB):
        self.modelos[modelo.id] = modelo

    def obtener_modelo(self, modelo_id: str) -> ModelDB:
        return self.modelos.get(modelo_id)
    
    def obtener_modelos(self) -> list[ModelDB]:
        return self.modelos
    
    def get_usuario(self) -> str:
        return encryptor.decrypt(self.usuario)
    
    def get_clave(self) -> str:
        return encryptor.decrypt(self.clave)
    
    def get_conexion(self) -> str:
        return encryptor.decrypt(self.conexion)
    
