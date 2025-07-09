from typing import List
from .user import User
from .aplication import Aplication

class Company:
    def __init__(self, id_emp: str, name: str, rut: str, logo: str, mail: str, clave: str, recover: str):
        self.id_emp = id_emp
        self.name = name
        self.rut = rut
        self.logo = logo # ver la forma de implementar el logo

        # para el admin
        self.mail = mail
        self.clave = clave
        self.recover = recover

        self.empleados: dict[str, User] = []
        self.aplicaciones: dict[str, Aplication] = {}

    def agregar_empleado(self, empleado: User):
        self.empleados.append(empleado)

    def agregar_aplicacion(self, app: Aplication):
        self.aplicaciones[app.codigo] = app
    
    def obtener_empleados(self) -> List[str]:
        return list(self.empleados.keys())
    
    def obtener_empleado(self, id: str) -> User | None:
        return self.empleados.get(id)
    
    def obtener_aplicaciones(self) -> List[Aplication]:
        return list(self.aplicaciones.keys())
    
    def obtener_aplicacion(self, codigo: str) -> Aplication | None:
        return self.aplicaciones.get(codigo)
    
    def get_tokens(self) -> int:
        return sum(empleado.get_total_tokens() for empleado in self.empleados.values())