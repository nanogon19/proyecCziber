from app.schemas.empresa import Empresa
from app.schemas.modelDB import ModelDB
from app.schemas.user import Usuario

class EmpresaService:
    def add_empleado(self, empleado: Usuario):
        if empleado.get_id() in self.empleados:
            raise ValueError(f"Empleado with ID {empleado.get_id()} already exists in empresa {self.name}.")
        self.empleados[empleado.get_id()] = empleado
    
    def remove_empleado(self, empleado_id: str):
        if empleado_id not in self.empleados:
            raise ValueError(f"Empleado with ID {empleado_id} does not exist in empresa {self.name}.")
        del self.empleados[empleado_id]

    def add_modelo(self, modelo: ModelDB):
        if modelo.get_id() in self.modelos:
            raise ValueError(f"Modelo with ID {modelo.get_id()} already exists in empresa {self.name}.")
        self.modelos[modelo.get_id()] = modelo  

    def remove_modelo(self, modelo_id: str):
        if modelo_id not in self.modelos:
            raise ValueError(f"Modelo with ID {modelo_id} does not exist in empresa {self.name}.")
        del self.modelos[modelo_id]

    def get_empleado(self, empleado_id: str) -> Usuario:
        if empleado_id not in self.empleados:
            raise ValueError(f"Empleado with ID {empleado_id} does not exist in empresa {self.name}.")
        return self.empleados[empleado_id]
    
    def get_modelo(self, modelo_id: str) -> ModelDB:
        if modelo_id not in self.modelos:
            raise ValueError(f"Modelo with ID {modelo_id} does not exist in empresa {self.name}.")
        return self.modelos[modelo_id]
    
    def get_all_empleados(self) -> list[Usuario]:
        return list(self.empleados.values())
    
    def get_all_modelos(self) -> list[ModelDB]:
        return list(self.modelos.values())
    
    def get_empleados_by_level(self, level: int) -> list[Usuario]:
        return [empleado for empleado in self.empleados.values() if empleado.get_level() == level]
    
#    def get_modelos_by_context(self, context: str) -> list[ModelDB]:
#        return [modelo for modelo in self.modelos.values() if modelo.get_context() == context]  
    
    def get_empleado_by_email(self, email: str) -> Usuario:
        for empleado in self.empleados.values():
            if empleado.get_email() == email:
                return empleado
        raise ValueError(f"Empleado with email {email} does not exist in empresa {self.name}.")
    
    def is_empleado_active(self, empleado: Usuario) -> bool:
        return empleado.habilitado()
    
    def set_empleado_active(self, empleado: Usuario, active: bool):
        if empleado.habilitado() == active:
            return f"Empleado is already {'active' if active else 'inactive'}."
        else:
            empleado.set_is_active(active)
            return f"Empleado has been set to {'active' if active else 'inactive'}."
    
    