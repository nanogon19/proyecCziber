import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

class EncryptionManager:
    def __init__(self):
        key = os.getenv("ENC_KEY")
        if not key:
            raise ValueError("No ENC_KEY found in environment variables.")
        self.fernet = Fernet(key.encode())

    def encrypt_data(self, data: str) -> str:
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt_data(self, encrypted_data: str) -> str:
        return self.fernet.decrypt(encrypted_data.encode()).decode()
    