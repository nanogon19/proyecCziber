from datetime import datetime

class Query:
    def __init__(self, id_query: str, prompt: str, result: str, res_SQL: str ,tokens_in: int, tokens_out: int, fecha: datetime, user_id = str, model_id = str):
        self.id_query = id_query
        self.prompt = prompt
        self.result = result
        self.res_SQL = res_SQL
        self.tokens_in = tokens_in
        self.tokens_out = tokens_out
        self.fecha = fecha

        self.user_id = user_id
        self.model_id = model_id
    
    def obtener_prompt(self) -> str:
        return self.prompt
    
    def obtener_resultado(self) -> str:
        return self.result      
    
    def obtener_res_SQL(self) -> str:
        return self.res_SQL
    
    def obtener_fecha(self) -> datetime:
        return self.fecha
    
    def total_tokens(self) -> int:
        return self.tokens_ent + self.tokens_sal
    
    def obtener_usuario(self) -> str:
        return self.user_id
    
    def obtener_modelo(self) -> str:
        return self.model_id