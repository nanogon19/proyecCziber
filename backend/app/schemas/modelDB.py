
# from typing import Optional

# class ModelDB:
#     def __init__(self, id: str, name: str, context: Optional[str], empresa_id: str):
#         self.id = id
#         self.name = name
#         self.context = context

#         self.empresa_id = empresa_id

from pydantic import BaseModel

class ModelDBCreate(BaseModel):
    id: str
    nombre: str
    descripcion: str
    id_empresa: str
    archivo: str  # ruta o nombre del archivo PDF


class ModelDBOut(BaseModel):
    id: str
    nombre: str
    descripcion: str
    id_empresa: str
    archivo: str
