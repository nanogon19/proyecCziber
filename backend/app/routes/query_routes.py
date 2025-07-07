from flask import Blueprint, request, jsonify

query_bp = Blueprint("query", __name__)

@query_bp.route("/ask", methods=["POST"])
def query_ai():
    data = request.get_json()
    prompt = data.get("prompt")

    # logica a implementar:
    # -> determinar a que app-model pertenece el usuario
    # -> generar la MS SQL con la IA
    # -> ejecutar la sql
    # -> devolver el resultado (PDF o .xslx)

    return jsonify({"message": "Consulta procesada"}), 200
