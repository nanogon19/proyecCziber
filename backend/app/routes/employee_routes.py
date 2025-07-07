from flask import Blueprint, request, jsonify
from app.models.usuario import Empleado

employee_bp = Blueprint("employee", __name__)

@employee_bp.route("/applications", methods=["GET"])
def list_applications():
    #devolver aplicaciones asociadas al empleado
    return jsonify({"applications": []})

@employee_bp.route("/modeles/<app_id>", methods=["GET"])
def list_models(app_id):
    # devolver modelos para una aplicacion especifica
    return jsonify({"models": []})

@employee_bp.route("/registrar_empleado", methods=["POST"])
def registrar_empleado():
    data = request.json

    try:
        id_empleado = data["id"]
        name = data["name"]
        password = data["password"]
        email = data["email"]

        emp_id = data["emp_id"]
        level_access = data["level"]

        nuevo_empleado = Empleado(
            id=id_empleado,
            name=name,
            password=password,
            email=email,
            empresa_id=emp_id,
            level_Access=level_access
        )

        # falta agregar el empleado a la empresa
        # empresa a la base de datos
        # empresa a la aplicacion que tiene acceso
        
        return jsonify({"message": "empleado registrado"})
    
    except KeyError as e:
        return jsonify({"error"}), 400
    
#@employee_bp.route("/listar_aplicaciones", methods=["GET"])
#def listar_aplicaciones():
