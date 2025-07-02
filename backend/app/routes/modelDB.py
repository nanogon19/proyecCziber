from fastapi import APIRouter, HTTPException
from app.schemas.modelDB import ModelDBCreate, ModelDBOut
from app.services.model_service import ModelDBService

router = APIRouter()
model_service = ModelDBService()

@router.post("/modelos", response_model=ModelDBOut)
def crear_modelo(modelo: ModelDBCreate):
    try:
        nuevo = model_service.crear_modelo(modelo)
        return ModelDBOut(
            id=nuevo.id,
            nombre=nuevo.nombre,
            descripcion=nuevo.descripcion,
            id_empresa=nuevo.id_empresa,
            archivo=nuevo.archivo
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/modelos", response_model=list[ModelDBOut])
def listar_modelos():
    return [
        ModelDBOut(
            id=m.id,
            nombre=m.nombre,
            descripcion=m.descripcion,
            id_empresa=m.id_empresa,
            archivo=m.archivo
        )
        for m in model_service.listar_modelos()
    ]
