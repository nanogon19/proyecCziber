from flask import Blueprint, request, jsonify
from uuid import uuid4

from backend.app.models.aplication import Aplication
from backend.app.models.company import Company
from backend.app.models.model import Model
from backend.app.models.conection import Conection  

cziber_bp = Blueprint("cziber", __name__)
companies_db = {}
app_db = {}
modelos_db = {}

@cziber_bp.route("/registrar_empresa", methods=["POST"])
def registrar_empresa():
    data = request.json

    try:
        id_emp = data["id_emp"]
        name = data["name"]
        rut = data["rut"]
        logo = data["logo"]

        mail = data["mail"]
        clave = data["clave"]
        recover = data["recover"]
        new_company = Company(
            id_emp=id_emp,
            name=name,
            rut=rut,
            logo=logo,
            mail=mail,
            clave=clave,
            recover=recover
        )

        # agregar company to the database
        companies_db[id_emp] = new_company

        return jsonify({"message": "Empresa registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error"}), 400
    
@cziber_bp.route("/listar_empresas", methods=["GET"])
def listar_empresas():
    empresas = {
        id_emp: {
            "name": company.name,
            "rut": company.rut,
            "logo": company.logo
        } for id_emp, company in companies_db.items()
    }
    return jsonify(empresas), 200

@cziber_bp.route("/registrar_aplicacion", methods=["POST"])
def registrar_aplicacion():
    data = request.json

    try:
        id_app = data["id"] 
        nombre = data["nombre"]

        nueva_aplicacion = Aplication(
            id=id_app,
            nombre=nombre
        )

        app_db[id_app] = nueva_aplicacion      

        return jsonify({"message": "Aplicación registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {str(e)}"}), 400
    
@cziber_bp.route("/asociar_empresa_aplicacion", methods=["POST"])
def asociar_empresa_aplicacion():
    data = request.json

    try:
        id_emp = data["id_emp"]
        id_app = data["id_app"]

        company = companies_db.get(id_emp)
        app = app_db.get(id_app)

        if not company:
            return jsonify({"error": "Empresa no encontrada"}), 404
        
        if not app:
            return jsonify({"error": "Aplicación no encontrada"}), 404

        company.agregar_aplicacion(app)
        app.agregar_empresa(company)

        return jsonify({"message": "Empresa y aplicación asociadas"}), 200
    
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {str(e)}"}), 400
    
@cziber_bp.route("/registrar_modelo", methods=["POST"])
def registrar_modelo():
    data = request.json

    try:
        id_modelo = data["id"]
        nombre = data["nombre"]
        documentacion = data["documentacion"]
        version = data["version"]

        emp_id = data["id_emp"]
        id_app = data["id_app"]
        emp = companies_db.get(emp_id)
        app = app_db.get(id_app)

        if not emp:
            return jsonify({"error": "Empresa no encontrada"}), 404
        
        if not app:
            return jsonify({"error": "Aplicación no encontrada"}), 404

        nuevo_modelo = Model(
            id=id_modelo,
            nombre=nombre,
            descripcion=documentacion,
            version=version
        )

        emp.agregar_modelo(nuevo_modelo)
        app.agregar_modelo(nuevo_modelo)
        modelos_db[id_modelo] = nuevo_modelo

        return jsonify({"message": "Modelo registrado"}), 201
    
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {str(e)}"}), 400
    
@cziber_bp.route("/registrar_conexion", methods=["POST"])
def registrar_conexion():
    data = request.json

    try:
        id_conexion = data["id"]
        ip = data["ip"]
        puerto = data["puerto"]
        usuario = data["usuario"]
        clave = data["clave"]

        emp_id = data["emp_id"]
        app_id = data["app_id"]
        model_id = data["model_id"]
        emp = companies_db.get(emp_id)
        app = app_db.get(app_id)
        model = modelos_db.get(model_id)

        if not emp:
            return jsonify({"error": "Empresa no encontrada"}), 404
        
        if not app:
            return jsonify({"error": "Aplicación no encontrada"}), 404
        
        if not model:
            return jsonify({"error": "Modelo no encontrado"}), 404

        nueva_conexion = Conection(
            id=id_conexion,
            ip=ip,
            port=puerto,
            user=usuario,
            password=clave,
            app_id=app_id,
            emp_id=emp_id,
            model_id=model_id   
        )

        emp.agregar_conexion(nueva_conexion)
        app.agregar_conexion(nueva_conexion)
        model.agregar_conexion(nueva_conexion)

        return jsonify({"message": "Conexión registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {str(e)}"}), 400
    
@cziber_bp.route("/listar_modelos", methods=["GET"])
def listar_modelos():  
    emp_id = request.args.get("emp_id")
    app_id = request.args.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Missing emp_id or app_id parameter"}), 400

    emp = companies_db.get(emp_id)
    app = app_db.get(app_id)

    if not emp:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    if not app:
        return jsonify({"error": "Aplicación no encontrada"}), 404

    modelos = [model.to_dict() for model in emp.obtener_modelos().values() if model.app_id == app_id]
    
    return jsonify({"modelos": modelos}), 200

@cziber_bp.route("/listar_conexiones", methods=["GET"])
def listar_conexiones():
    emp_id = request.args.get("emp_id")
    app_id = request.args.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Missing emp_id or app_id parameter"}), 400

    emp = companies_db.get(emp_id)
    app = app_db.get(app_id)

    if not emp:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    if not app:
        return jsonify({"error": "Aplicación no encontrada"}), 404

    conexiones = [con.to_dict() for con in emp.obtener_conexiones().values() if con.app_id == app_id]
    
    return jsonify({"conexiones": conexiones}), 200

@cziber_bp.route("/get_tokens_from_company", methods=["GET"])
def get_tokens_from_company():
    emp_id = request.args.get("emp_id")
    if not emp_id:
        return jsonify({"error": "Missing emp_id parameter"}), 400

    emp = companies_db.get(emp_id)
    if not emp:
        return jsonify({"error": "Empresa no encontrada"}), 404

    tokens = emp.get_tokens()
    
    return jsonify({"tokens": tokens}), 200


