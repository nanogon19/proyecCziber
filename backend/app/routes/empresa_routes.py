from flask import Blueprint, request, jsonify

from backend.app.models.company import Empresa
from backend.app.models.user import Admin
from backend.app.models.user import Empleado
from backend.app.models.aplication import Aplicacion
from backend.app.models.model import Modelo

empresa_bp = Blueprint("empresa", __name__)
empresa_db = {}  # Simulando una base de datos en memoria

@empresa_bp.route("/registrar_empresa", methods=["POST"])
def registrar_empresa():
    data = request.json

    try:
        id_empresa = data["id"]
        name = data["name"]
        rut = data["rut"]
        logo = data.get("logo", "")

        admin_data = data["admin"]
        admin = Admin(
            id=admin_data["id"],
            name=admin_data["name"],
            password=admin_data["password"],
            email=admin_data["email"],
            empresa_id=id_empresa
        )

        nueva_empresa = Empresa(
            id=id_empresa,
            name=name,
            rut=rut,
            logo=logo
        )
        nueva_empresa.agregar_admin(admin)
        empresa_db[id_empresa] = nueva_empresa

        return jsonify({"message": "empresa registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error"}), 400
    
@empresa_bp.route("/listar_empresas", methods=["GET"])
def listar_empresas():
    empresas = {
        eid: {
            "name": e.name,
            "rut": e.rut,
        } for eid, e in empresa_db.items()
    }
    return jsonify(empresas)

@empresa_bp.route("/listar_empleados", methods=["GET"])
def listar_empleados():
    emp_id = request.args.get("emp_id")
    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    empleados = [empleado.__dict__ for empleado in empresa.obtener_empleados()]
    return jsonify(empleados)

@empresa_bp.route("/registrar_empleado", methods=["POST"])
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
        empresa = empresa_db.get(emp_id)
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404

        empresa.agregar_empleado(nuevo_empleado)
        
        return jsonify({"message": "empleado registrado"}), 201
    
    except KeyError as e:
        return jsonify({"error": "Datos incompletos"}), 400

@empresa_bp.route("/eliminar_empleado", methods=["DELETE"])
def eliminar_empleado():
    data = request.json
    emp_id = data.get("emp_id")
    empleado_id = data.get("empleado_id")

    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    empleados = empresa.obtener_empleados()
    empleado = next((e for e in empleados if e.id == empleado_id), None)
    
    if not empleado:
        return jsonify({"error": "Empleado no encontrado"}), 404
    
    empresa.empleados.remove(empleado)
    return jsonify({"message": "Empleado eliminado"}), 200

@empresa_bp.route("/obtener_consultas_empleados", methods=["GET"])
def obtener_consultas_empleados():
    emp_id = request.args.get("emp_id")
    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    consultas = []
    for empleado in empresa.obtener_empleados():
        consultas.extend(empleado.consultas.values())
    
    return jsonify([consulta.__dict__ for consulta in consultas])

@empresa_bp.route("/obtener_total_tokens", methods=["GET"])
def obtener_total_tokens():
    emp_id = request.args.get("emp_id")
    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    total_tokens = sum(empleado.total_tokens() for empleado in empresa.obtener_empleados())
    return jsonify({"total_tokens": total_tokens})

# agrega contexto a un modelo de una base de datos
# si ya lo tiene lo actualiza
@empresa_bp.route("/agregar_contexto_modelo", methods=["POST"])
def agregar_contexto_modelo():
    data = request.json
    emp_id = data.get("emp_id")
    modelo_id = data.get("modelo_id")
    contexto = data.get("contexto")

    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    app = empresa.obtener_aplicacion(modelo_id)
    model = modelo.obtener_modelo(modelo_id)
    if not app:
        return jsonify({"error": "Aplicación no encontrada"}), 404
    
    app.agregar_contexto(contexto)
    
    return jsonify({"message": "Contexto agregado al modelo"}), 200

@empresa_bp.route("/obtener_aplicaciones", methods=["GET"])
def obtener_aplicaciones():
    emp_id = request.args.get("emp_id")
    empresa = empresa_db.get(emp_id)
    
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    aplicaciones = [app.__dict__ for app in empresa.obtener_aplicaciones()]
    return jsonify(aplicaciones)