from pydantic import BaseModel, EmailStr
from enum import Enum

class User:
    def __init__(self, id: int, name: str, email: EmailStr, password: str, level: int):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.level = level
        self.habilitado = True
    
    def get_id(self) -> int:
        return self.id
    
    def get_name(self) -> str:
        return self.name
    
    def get_email(self) -> EmailStr:
        return self.email

    def get_password(self) -> str:
        return self.password

    def set_password(self, password: str):
        self.password = password

    def get_level(self) -> int:
        return self.level

    def set_level(self, level: int):
        self.level = level

    def get_id_emp(self) -> str:
        return self.id_emp

    def set_id_emp(self, id_emp: str):
        self.id_emp = id_emp

    def habilitado(self) -> bool:
        return self.habilitado
    
class Empleado(User):
    def __init__(self, id: int, name: str, email: EmailStr, password: str, level: int, id_emp: str):
        super().__init__(id, name, email, password, level)
        self.id_emp = id_emp
    
    def get_id_emp(self) -> str:
        return self.id_emp
    
    def set_id_emp(self, id_emp: str):
        self.id_emp = id_emp

    def is_admin(self) -> bool:
        return False
    
class Admin(User):
    def __init__(self, id: int, name: str, email: EmailStr, password: str, level: int):
        super().__init__(id, name, email, password, level)
    
    def is_admin(self) -> bool:
        return True
