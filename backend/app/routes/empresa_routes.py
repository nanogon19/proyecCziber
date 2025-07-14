from flask import Blueprint, request, jsonify
from uuid import uuid4

from backend.app.extensions import db
from backend.app.models.company import Company
from backend.app.models.user import User
from backend.app.models.model import Model

empresa_bp = Blueprint("empresa", __name__)

@empresa_bp.route("/registrar_empleado", methods=["POST"])
def registrar_empleado():
    data = request.json

    try:
        empresa = Company.query.get(data["empresa_id"])
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404
        
        nuevo_empleado = User(
            name=data["name"],
            email=data["email"],
            password=data["password"],
            recover=data.get("recover"),
            level=data.get("level", "1"),
            active=data.get("active", True),
            isAdmin=data.get("isAdmin", False),
            company_id=empresa.id_emp
        )

        db.session.add(nuevo_empleado)
        db.session.commit()
        
        return jsonify({"message": "empleado registrado"}), 201
    
    except KeyError as e:
        return jsonify({"error": "Datos incompletos"}), 400

@empresa_bp.route("/listar_empleados", methods=["GET"])
def listar_empleados():

    empresa_id = request.args.get("empresa_id")
    empresa = Company.query.get(empresa_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    empleados = [{
        "id": empleado.id_user,
        "name": empleado.name,
        "email": empleado.email,
        "level": empleado.level,
        "isAdmin": empleado.isAdmin
    } for empleado in empresa.empleados if not empleado.isAdmin]
    return jsonify(empleados), 200

@empresa_bp.route("/listar_admins", methods=["GET"])
def listar_admins():
    empresa_id = request.args.get("empresa_id")
    empresa = Company.query.get(empresa_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    admins = [{
        "id": empleado.id_user,
        "name": empleado.name,
        "email": empleado.email
    } for empleado in empresa.empleados if empleado.isAdmin]
    
    return jsonify(admins), 200

@empresa_bp.route("/eliminar_empleado", methods=["DELETE"])
def eliminar_empleado():
    data = request.json
    empleado = User.query.get(data["id_user"])
    if not empleado:
        return jsonify({"error": "Empleado no encontrado"}), 404
    
    db.session.delete(empleado)
    db.session.commit()
    return jsonify({"message": "Empleado eliminado"}), 200

@empresa_bp.route("/obtener_consultas_empleados", methods=["GET"])
def obtener_consultas_empleados():
    emp_id = request.args.get("emp_id")
    empresa = Company.query.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    consultas = [q.to_dict() for u in empresa.empleados for q in u.consultas]
    return jsonify(consultas), 200

@empresa_bp.route("/obtener_total_tokens", methods=["GET"])
def obtener_total_tokens():
    emp_id = request.args.get("emp_id")
    empresa = Company.query.get(emp_id)

    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    total_tokens = empresa.get_tokens()
    return jsonify({"total_tokens": total_tokens}), 200

# agrega contexto a un modelo de una base de datos
# si ya lo tiene lo actualiza
@empresa_bp.route("/agregar_contexto_modelo", methods=["POST"])
def agregar_contexto_modelo():
    data = request.json
    modelo = Model.query.filter_by(id_model=data.get("model_id"), empresa_id=data.get("emp_id")).first()

    if not modelo:
        return jsonify({"error": "Modelo no encontrado"}), 404

    modelo.context = data.get("context")
    db.session.commit()
    return jsonify({"message": "Contexto agregado al modelo"}), 200    

@empresa_bp.route("/obtener_aplicaciones", methods=["GET"])
def obtener_aplicaciones():
    emp_id = request.args.get("emp_id")
    empresa = Company.query.get(emp_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    apps =[{
        "id": app.id,
        "name": app.name,
        } for app in empresa.aplicaciones]
    
    return jsonify(apps), 200