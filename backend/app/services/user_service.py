from app.schemas.user import Usuario
from app.schemas.empresa import Empresa

class UserService:
    def add_user(self, user: Usuario, empresa: Empresa):
        if user.get_id() in empresa.empleados:
            raise ValueError(f"User with ID {user.get_id()} already exists in empresa {empresa.get_name()}.")
        
        if user.get_email() in empresa.empleados:
            raise ValueError(f"User with email {user.get_email()} already exists.")
        
        empresa.add_empleado(user)

    def remove_user(self, user_id: str, empresa: Empresa):
        if user_id not in empresa.empleados:
            raise ValueError(f"User with ID {user_id} does not exist in empresa {empresa.get_name()}.")
        
        empresa.remove_empleado(user_id)

    def update_user_level(self, user: Usuario, empresa: Empresa, level: int):
        if user.get_id() not in empresa.empleados:
            raise ValueError(f"User with ID {user.get_id()} does not exist in empresa {empresa.get_name()}.")
        
        user.set_level(level)
        empresa.empleados[user.get_id()] = user

    def get_user_by_id(self, user_id: str, empresa: Empresa) -> Usuario:
        if user_id not in empresa.empleados:
            raise ValueError(f"User with ID {user_id} does not exist in empresa {empresa.get_name()}.")
        
        return empresa.empleados[user_id]
    
    def get_all_users(self, empresa: Empresa) -> list[Usuario]:
        return list(empresa.empleados.values())
    
    def get_users_by_level(self, level: int, empresa: Empresa) -> list[str]:
        return [user.name for user in empresa.empleados.values() if user.get_level() == level]

    def get_user_by_email(self, email: str, empresa: Empresa) -> Usuario:
        for user in empresa.empleados.values():
            if user.get_email() == email:
                return user
        raise ValueError(f"User with email {email} does not exist in empresa {empresa.get_name()}.")

    def is_user_active(self, user: Usuario) -> bool:
        return user.habilitado()

    def set_user_active(self, user: Usuario, active: bool):
        if user.habilitado() == active:
            return "User is already {'active' if active else 'inactive'}."
        else:
            user.set_is_active(active)
            return f"User has been set to {'active' if active else 'inactive'}."
    
    def change_user_password(self, user: Usuario, new_password: str):
        if user.get_password() == new_password:
            return "New password cannot be the same as the old password."
        else:
            user.set_password(new_password)
            return "Password has been changed successfully."
    
    def get_user_level(self, user: Usuario) -> int:
        return user.get_level()
    
    def set_user_level(self, user: Usuario, level: int):
        if user.get_level() == level:
            return "User is already at this level."
        else:
            user.set_level(level)
            return f"User level has been set to {level}."
        
    def get_user_id(self, user: Usuario) -> str:
        return user.get_id()
    
    def get_user_name(self, user: Usuario) -> str:
        return user.get_name()
    
    def get_user_email(self, user: Usuario) -> str:
        return user.get_email()
    
    def get_user_password(self, user: Usuario) -> str:  
        return user.get_password()
    
    