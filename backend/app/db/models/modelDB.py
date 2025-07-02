from sqlalchemy import Column, String, ForeignKey
from app.db.database import Base

class modelDB(Base):
    __tablename__ = "Modelo_Datos"

    idEmpresa = Column(String, primary_key= True, index = True, nullable = False)
    idModelo = Column(String, primary_key= True, index = True, nullable = False)
    nombreModelo = Column(String, nullable = False)
    password = Column(String, nullable = False)
    contexto = Column(String, nullable = True)

    def __repr__(self):
        return f"<modelDB(idEmpresa={self.idEmpresa}, idModelo={self.idModelo}, nombreModelo={self.nombreModelo}, password={self.password}, contexto={self.contexto})>"