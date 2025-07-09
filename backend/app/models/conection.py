from utils.security import EncryptionManager
encryptor = EncryptionManager()

class Conection:
    def __init__(self, id: str, ip: str, port: int, user: str, password: str, app_id: str, emp_id: str, model_id: str):
        self.id = id
        self.ip = encryptor.encrypt_data(ip)
        self.port = encryptor.encrypt_data(port)
        self.user = encryptor.encrypt_data(user)
        self.password = encryptor.encrypt_data(password)   

        self.app_id = app_id
        self.emp_id = emp_id
        self.model_id = model_id

    def obtener_ip(self) -> str:
        return encryptor.decrypt(self.ip)
    
    def obtener_port(self) -> int:
        return encryptor.decrypt(self.port)

    def obtener_usuario(self) -> str:
        return encryptor.decrypt(self.usuario)
    
    def obtener_clave(self) -> str:
        return encryptor.decrypt(self.clave)
    
    
    