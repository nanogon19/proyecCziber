from sqlalchemy import Column, String
from app.db.database import Base

class Empresa(Base):
    __tablename__ = "empresas"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    codRut = Column(String, nullable=False, unique=True)
    # logo = Column(String)  # Uncomment if you want to handle image uploads later

    def __repr__(self):
        return f"<Empresa(id={self.id}, name={self.name}, codRut={self.codRut})>"