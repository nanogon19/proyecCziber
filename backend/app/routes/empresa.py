from fastapi import APIRouter, HTTPException
from app.schemas.empresa import EmpresaCreate, EmpresaOut
from app.services.empresa_service import EmpresaService

router = APIRouter()
empresa_service = EmpresaService()

@router.post("/empresas", response_model=EmpresaOut)
def crear_empresa(empresa: EmpresaCreate):
    try:
        nueva = empresa_service.crear_empresa(empresa)
        return EmpresaOut(id=nueva.id, name=nueva.name, is_active=nueva.is_active)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/empresas", response_model=list[EmpresaOut])
def listar_empresas():
    return [
        EmpresaOut(id=e.id, name=e.name, is_active=e.is_active)
        for e in empresa_service.listar_empresas()
    ]
