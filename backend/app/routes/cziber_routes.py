from flask import Blueprint, request, jsonify
from uuid import uuid4

from backend.app.extensions import db

from backend.app.models.application import Application
from backend.app.models.company import Company
from backend.app.models.model import Model
from backend.app.models.conection import Conection  

cziber_bp = Blueprint("cziber", __name__)


@cziber_bp.route("/registrar_empresa", methods=["POST"])
def registrar_empresa():
    data = request.json

    try:
        new_company = Company(
            name=data["name"],
            rut=data.get("rut"),
            logo=data.get("logo")
        )
        
        db.session.add(new_company)
        db.session.commit()

        return jsonify({"message": "Empresa registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error"}), 400
    
@cziber_bp.route("/listar_empresas_id", methods=["GET"])
def listar_empresas():

    empresas = Company.query.all()
    result = {
        empresa.id_emp: {
            "name": empresa.name,
            "id_emp" : empresa.id_emp, 
        } for empresa in empresas
    }
    return jsonify(result), 200

@cziber_bp.route("/registrar_aplicacion", methods=["POST"])
def registrar_aplicacion():
    data = request.json

    try:
        nombre = data["nombre"]

        nueva_aplicacion = Application(
            nombre=nombre
        )

        db.session.add(nueva_aplicacion)
        db.session.commit()

        return jsonify({"message": "Aplicación registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {str(e)}"}), 400
    
@cziber_bp.route("/asociar_empresa_aplicacion", methods=["POST"])
def asociar_empresa_aplicacion():
    data = request.json
    emp_id = data.get("emp_id")
    app_id = data.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Missing emp_id or app_id parameter"}), 400
    
    company = Company.query.get(emp_id)
    app = Application.query.get(app_id)

    if not company:
        return jsonify({"error": "Empresa no encontrada"}), 404
    if not app: 
        return jsonify({"error": "Aplicación no encontrada"}), 404
    
    company.agregar_aplicacion(app)
    app.agregar_empresa(company)

    db.session.commit()
    return jsonify({"message": "Empresa y aplicación asociadas"}), 200
    
@cziber_bp.route("/registrar_modelo", methods=["POST"])
def registrar_modelo():
    data = request.json

    nombre = data.get("nombre")
    documentacion = data.get("documentacion")
    version = data.get("version")
    emp_id = data.get("emp_id")
    app_id = data.get("app_id")

    if not all([nombre, emp_id, app_id]):
        return jsonify({"error": "Missing required fields"}), 400
    
    emp = Company.query.get(emp_id)
    app = Application.query.get(app_id)

    if not emp:
        return jsonify({"error": "Empresa no encontrada"}), 404
    if not app:
        return jsonify({"error": "Aplicación no encontrada"}), 404
    
    nuevo_modelo = Model(
        nombre=nombre,
        documentacion=documentacion,
        version=version,
        emp_id=emp_id,
        app_id=app_id
    )

    emp.agregar_modelo(nuevo_modelo)
    app.agregar_modelo(nuevo_modelo)

    db.session.add(nuevo_modelo)
    db.session.commit()
    
@cziber_bp.route("/registrar_conexion", methods=["POST"])
def registrar_conexion():
    data = request.json

    ip = data.get("ip")
    puerto = data.get("puerto")
    usuario = data.get("usuario")
    clave = data.get("clave")
    emp_id = data.get("emp_id")
    app_id = data.get("app_id")
    model_id = data.get("model_id")

    if not all([ip, puerto, usuario, clave, emp_id, app_id, model_id]):
        return jsonify({"error": "Missing required fields"}), 400
    
    emp = Company.query.get(emp_id)
    app = Application.query.get(app_id)
    model = Model.query.get(model_id)

    if not emp:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    if not app:
        return jsonify({"error": "Aplicación no encontrada"}), 404
    
    if not model:
        return jsonify({"error": "Modelo no encontrado"}), 404
    
    new_conection = Conection(
        ip=ip,
        port=puerto,
        user=usuario,
        password=clave,
        app_id=app_id,
        emp_id=emp_id,
        model_id=model_id
    )    

    emp.agregar_conexion(new_conection)
    app.agregar_conexion(new_conection)
    model.agregar_conexion(new_conection)

    db.session.add(new_conection)
    db.session.commit()
    
@cziber_bp.route("/listar_modelos", methods=["GET"])
def listar_modelos():  
    emp_id = request.args.get("emp_id")
    app_id = request.args.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Missing emp_id or app_id parameter"}), 400

    modelos = Model.query.filter_by(empresa_id=emp_id, app_id=app_id).all()

    modelos_serializados = [{
        "id_model": m.id_model,
        "nombre": m.nombre,
        "version": m.version,
        "documentacion": m.documentacion
    } for m in modelos]

    return jsonify({"modelos": modelos_serializados}), 200


@cziber_bp.route("/listar_conexiones", methods=["GET"])
def listar_conexiones():
    emp_id = request.args.get("emp_id")
    app_id = request.args.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Faltan parámetros emp_id o app_id"}), 400

    conexiones = Conection.query.filter_by(emp_id=emp_id, app_id=app_id).all()

    conexiones_serializadas = []
    for con in conexiones:
        conexiones_serializadas.append({
            "id_conn": con.id_conn,
            "ip": con.obtener_ip(),
            "puerto": con.obtener_port(),
            "usuario": con.obtener_usuario(),
            "clave": con.obtener_clave(),
            "modelo_id": con.model_id
        })

    return jsonify({"conexiones": conexiones_serializadas}), 200

@cziber_bp.route("/get_tokens_from_company", methods=["GET"])
def get_tokens_from_company():
    emp_id = request.args.get("emp_id")
    if not emp_id:
        return jsonify({"error": "Falta el parámetro emp_id"}), 400

    empresa = Company.query.get(emp_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    total_tokens = empresa.get_tokens()  # Este método ya está definido en el modelo

    return jsonify({"emp_id": emp_id, "tokens": total_tokens}), 200


