class Usuario:
    def __init__(self, id: str, name: str, password: str, email: str, empresa_id: str):
        self.id = id
        self.name = name
        self.password = password
        self.email = email
        self.empresa_id = empresa_id

class Admin(Usuario):
    def __init__(self, id: str, name: str, password: str, email: str, empresa_id: str):
        super().__init__(id, name, password, email, empresa_id)
        self.is_admin = True

class Empleado(Usuario):
    def __init__(self, id: str, name: str, password: str, email: str, empresa_id: str, level_Access: int):
        super().__init__(id, name, password, email, empresa_id)
        self.is_admin = False
        self.level_Access = level_Access
