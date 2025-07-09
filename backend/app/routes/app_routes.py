from flask import Blueprint, request, jsonify

from backend.app.models.aplication import Aplication
from app.routes.empresa_routes import empresa_db

app_bp = Blueprint("app", __name__)

@app_bp.route("/registrar_aplicacion", methods=["POST"])
def registrar_aplicacion():
    data = request.json

    try:
        emp_id = data["emp_id"]
        id_app = data["id"] 
        nombre = data["nombre"]
        typebd = data["typebd"]  #encriptar
        conexion = data["conexion"]  #encriptar
        usuario = data["usuario"]  #encriptar
        clave = data["clave"]  #encriptar

        nueva_aplicacion = Aplicacion(
            id=id_app,
            nombre=nombre,
            typebd=typebd,
            conexion=conexion,
            usuario=usuario,
            clave=clave
        )

        empresa = empresa_db.get(emp_id)
        if not empresa:
            return jsonify({"error": "Empresa no encontrada"}), 404
        
        empresa.agregar_aplicacion(nueva_aplicacion) #agregar aplicacion a la empresa
        # empresa a la base de datos
        # empresa a la aplicacion que tiene acceso  
        return jsonify({"message": "Aplicación registrada"}), 201
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {str(e)}"}), 400  
    

