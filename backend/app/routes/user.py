from fastapi import APIRouter, HTTPException
from app.schemas.user import Usuario, UserCreate, UserOut
from app.services.user_service import UserService

router = APIRouter()
usuario_service = UserService()

@router.post("/usuarios/", response_model=UserOut)
def create_usuario(usuario: UserCreate):
    try:
        new_usuario = usuario_service.add_user(usuario)
        return new_usuario
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    