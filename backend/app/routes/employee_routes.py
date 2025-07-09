from flask import Blueprint, request, jsonify
from uuid import uuid4
from datetime import datetime

from backend.app.models.user import Empleado
from backend.app.models.company import Empresa
from backend.app.models.query import Consulta

from app.routes.empresa_routes import empresa_db

empleados_db = {} # simula base de datos de empleados
empleado_bp = Blueprint("empleado", __name__)

@empleado_bp.route("/applications", methods=["GET"])
def list_applications():
    #devolver aplicaciones asociadas al empleado
    return jsonify({"applications": []})

@empleado_bp.route("/models/<app_id>", methods=["GET"])
def list_models(app_id):
    # devolver modelos para una aplicacion especifica
    return jsonify({"models": []})

    
@empleado_bp.route("/obtener_empresa", methods=["GET"])
def obtener_empresa():
    emp_id = request.args.get("emp_id")
    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    return jsonify({
        "id": empresa.id,
        "name": empresa.name,
        "rut": empresa.rut,
        "logo": empresa.logo
    })
    
@empleado_bp.route("/obtener_consultas", methods=["GET"])
def obtener_consultas():
    emp_id = request.args.get("emp_id")
    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    consultas = []

@empleado_bp.route("/crear_consulta", methods=["POST"])
def crear_consulta():
    data = request.json
    emp_id = data.get("emp_id")
    usuario_id = data.get("usuario_id")
    modelo_id = data.get("modelo_id")
    prompt = data.get("prompt")
    resultado = data.get("resultado-sql")
    tokens_ent = data.get("tokens_ent", 0)
    tokens_sal = data.get("tokens_sal", 0)

    empleado = empleados_db.get(usuario_id)
    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    consulta = Consulta(
        id=str(uuid4()),  # Placeholder, generate a unique ID
        usuario_id=usuario_id,
        modelo_id=modelo_id,
        fecha=datetime.now().isoformat(),  # Placeholder, use actual datetime
        prompt=prompt,
        resultado=resultado,
        tokens_ent=tokens_ent,
        tokens_sal=tokens_sal
    )
    empleado.consultas[consulta.id] = consulta

    # Aquí deberías agregar la lógica para almacenar la consulta en la base de datos
    return jsonify({"message": "Consulta creada", "consulta": consulta.to_dict()}), 201

@empleado_bp.route("/obtener_modelos", methods=["GET"])
def obtener_modelos():
    emp_id = request.args.get("emp_id")
    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    modelos = []
    for app in empresa.obtener_aplicaciones().values():
        modelos.extend(app.modelos)

