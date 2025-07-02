from datetime import datetime

class Consulta:
    def __init__(self, id: str, usuario_id: str, modelo_id: str, fecha: datetime, resultado: str, tokens_ent: int, tokens_sal: int):
        self.id = id
        self.usuario_id = usuario_id
        self.modelo_id = modelo_id
        self.fecha = fecha
        self.resultado = resultado
        self.tokens_ent = tokens_ent
        self.tokens_sal = tokens_sal

    def total_tokens(self) -> int:
        return self.tokens_ent + self.tokens_sal