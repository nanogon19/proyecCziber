# from app.schemas.modelDB import ModelDB
# from app.schemas.user import User 

# class Empresa:
#     def __init__(self, id: str, name: str):
#         self.id = id
#         self.name = name

#         self.isActive = True
#         self.empleados: dict[str, User] = {}
#         self.modelos: dict[str, ModelDB] = {}

#     def get_id(self) -> str:
#         return self.id  

#     def get_name(self) -> str:
#         return self.name
    
#     def set_name(self, name: str):
#         self.name = name

#     def get_is_active(self) -> bool:
#         return self.isActive
    
#     def set_is_active(self, active: bool):
#         self.isActive = active
    
from pydantic import BaseModel
from typing import Dict
from app.schemas.user import UsuarioOut
from app.schemas.modelDB import ModelDBOut


class EmpresaCreate(BaseModel):
    id: str
    name: str


class EmpresaOut(BaseModel):
    id: str
    name: str
    is_active: bool
    empleados: Dict[str, UsuarioOut] = {}
    modelos: Dict[str, ModelDBOut] = {}
