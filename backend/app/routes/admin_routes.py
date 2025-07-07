from flask import Blueprint, request, jsonify

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("register_company", methods=["POST"])
def register_company():
    # logica para registrar compania
    return jsonify({"message": "Empresa registrada exitosamente"}), 201


@admin_bp.route("register_employee", methods=["POST"])
def register_employee():
    # logica para registrar empleado
    return jsonify({"message": "Empleado registrada exitosamente"}), 201