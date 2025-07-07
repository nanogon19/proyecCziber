from flask import Blueprint, request, jsonify
from app.models.empresa import Empresa
from app.models.usuario import Admin

empresa_bp = Blueprint("empresa", __name__)

empresa_db = {
    "emp1": Empresa("emp1", "Empresa Uno", "123456789", "logo1.png"),
    "emp2": Empresa("emp2", "Empresa Dos", "987654321", "logo2.png")
}

@empresa_bp.route("/registrar_empresa", methods=["POST"])
def registrar_empresa():
    data = request.json

    try:
        id_empresa = data["id"]
        nombre = data["nombre"]
        rut = data["rut"]
        logo = data.get("logo", "")

        admin_data = data["admin"]
        admin = Admin(
            id=admin_data["id"],
            nombre=admin_data["nombre"],
            email=admin_data["email"],
            empresa_id=id_empresa
        )

        nueva_empresa = Empresa(
            id=id_empresa,
            nombre=nombre,
            rut=rut,
            logo=logo
        )
        nueva_empresa.agregar_admin(admin)
        empresa_db.add = nueva_empresa

        return jsonify({"message": "empresa registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error"}), 400
    
@empresa_bp.route("/listar_empresas", methods=["GET"])
def listar_empresas():
    empresas = {
        eid: {
            "nombre": e.nombre,
            "rut": e.rut,
        } for eid, e in empresa_db.items()
    }
    return jsonify(empresas)