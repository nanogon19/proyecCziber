from typing import Dict

import backend.app.models.query as Query
import models.model as Model

class User:
    def __init__(self, id_user: str, name: str, email: str, password: str, recover: str, level: int, active: bool, empresa_id: str):
        self.id_user = id
        self.name = name
        self.email = email
        self.password = password
        self.recover = recover
        self.level = level
        self.active = active

        self.models = dict(str, Model) = {}
        self.consultas = dict(str, Query) = {}
        self.empresa_id = empresa_id

    def add_model(self, model: Model):
        self.models[model.id] = model

    def get_model(self, model_id: str) -> Model:
        return self.models.get(model_id)
    
    def get_models(self) -> list[str]:
        return list(self.models.keys())
    
    def add_consulta(self, consulta: Query):
        self.consultas[consulta.id] = consulta

    def get_consulta(self, consulta_id: str) -> Query:
        return self.consultas.get(consulta_id)
    
    def get_consultas(self) -> list[str]:
        return list(self.consultas.keys())
    
    def get_empresa_id(self) -> str:
        return self.empresa_id
    
    def set_password(self, new_password: str):
        self.password = new_password

    def get_total_tokens(self) -> int:
        total_tokens = 0
        for model in self.models.values():
            total_tokens += model.get_total_tokens()
        return total_tokens