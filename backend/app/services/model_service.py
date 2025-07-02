from app.schemas.empresa import Empresa
from app.schemas.modelDB import ModelDB

class ModelService:
    def add_model(self, model: ModelDB, empresa: Empresa):
        if model.id in empresa.modelos:
            raise ValueError(f"Model with ID {model.id} already exists in empresa {empresa.get_name()}.")
        
        empresa.add_modelo(model)

    def remove_model(self, model_id: str, empresa: Empresa):
        if model_id not in empresa.modelos:
            raise ValueError(f"Model with ID {model_id} does not exist in empresa {empresa.get_name()}.")
        
        empresa.remove_modelo(model_id)

    def get_model_by_id(self, model_id: str, empresa: Empresa) -> ModelDB:
        if model_id not in empresa.modelos:
            raise ValueError(f"Model with ID {model_id} does not exist in empresa {empresa.get_name()}.")
        
        return empresa.get_modelo(model_id)
    
    def get_all_models(self, empresa: Empresa) -> list[ModelDB]:
        return list(empresa.modelos.values())