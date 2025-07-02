from sqlalchemy import Column, String, Enum
from app.db.database import Base

class User(Base):   
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_admin = Column(Enum("admin", "employee", name="user_role"), default="employee")
    nivel = Column(Enum(name = "user_level",  nullable = True))

    def __repr__(self):
        return f"<User(id={self.id}, name={self.name}, email={self.email}, is_admin={self.is_admin})>"