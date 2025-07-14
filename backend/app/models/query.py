from datetime import datetime
from backend.app.extensions import db
import uuid

class Query(db.Model):
    __tablename__ = "queries"

    id_query = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    prompt = db.Column(db.String, nullable=False)
    res_SQL = db.Column(db.Text)
    tokens_in = db.Column(db.Integer, default=0)
    tokens_out = db.Column(db.Integer, default=0)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    # Claves foráneas
    user_id = db.Column(db.String, db.ForeignKey("users.id_user"), nullable=False)
    model_id = db.Column(db.String, db.ForeignKey("models.id_model"), nullable=False)

    # Relaciones 
    usuario = db.relationship("User",   back_populates="consultas")   # many-to-one
    model  = db.relationship("Model",  back_populates="consultas")

    # Métodos de acceso
    def obtener_prompt(self) -> str:
        return self.prompt    

    def obtener_res_SQL(self) -> str:
        return self.res_SQL

    def obtener_fecha(self) -> datetime:
        return self.fecha

    def total_tokens(self) -> int:
        return (self.tokens_in or 0) + (self.tokens_out or 0)

    def obtener_usuario(self) -> str:
        return self.user_id

    def obtener_modelo(self) -> str:
        return self.model_id

    def to_dict(self) -> dict:
        return {
            "id_query": self.id_query,
            "prompt": self.prompt,
            "res_SQL": self.res_SQL,
            "tokens_in": self.tokens_in,
            "tokens_out": self.tokens_out,
            "fecha": self.fecha.isoformat(),
            "user_id": self.user_id,
            "model_id": self.model_id
        }