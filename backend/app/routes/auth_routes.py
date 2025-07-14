from flask import Blueprint, request, jsonify

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Faltan datos de autenticación"}), 400
    
    return jsonify({"mensaje": "Login exitoso"})
