from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    #hay que hacer la logica de autenticacion
    return jsonify({"mensaje": "Login exitoso"})
