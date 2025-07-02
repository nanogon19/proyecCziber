from typing import List
from .usuario import Admin, Empleado
from .aplicacion import Aplicacion

class Empresa:
    def __init__(self, id: str, nombre: str, rut: str, logo: str):
        self.id = id
        self.nombre = nombre
        self.rut = rut
        self.logo = logo # ver la forma de implementar el logo

        self.admins: List[Admin] = []
        self.empleados: List[Empleado] = []
        self.aplicaciones= List[Aplicacion] = {}

    def agregar_admin(self, admin: Admin):
        self.admins.append(admin)

    def agregar_empleado(self, empleado: Empleado):
        self.empleados.append(empleado)

    def agregar_aplicacion(self, app: Aplicacion):
        self.aplicaciones[app.codigo] = app

    def obtener_admins(self) -> List[Admin]:
        return self.admins
    
    def obtener_empleados(self) -> List[Empleado]:
        return self.empleados
    
    def obtener_aplicaciones(self) -> List[Aplicacion]:
        return list(self.aplicaciones.values())
    
    def obtener_aplicacion(self, codigo: str) -> Aplicacion | None:
        return self.aplicaciones.get(codigo)