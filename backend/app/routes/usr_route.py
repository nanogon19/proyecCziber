from flask import Blueprint, request, jsonify

from uuid import uuid4
from datetime import datetime

from backend.app.models.user import User
from backend.app.models.company import Company
from backend.app.models.query import Query

usr_bp = Blueprint("usr", __name__)
usr_db = {}  # Simula base de datos de usuarios

@usr_bp.route("/create_query", methods = ["POST"])
def create_query():
    data = request.json
    user_id = data.get("user_id")
    company_id = data.get("company_id")
    model_id = data.get("model_id")
    prompt = data.get("prompt")
    result_sql = data.get("result_sql", "")
    tokens_in = data.get("tokens_in")
    tokens_out = data.get("tokens_out")

    if not user_id or not company_id or not model_id or not prompt:
        return jsonify({"error": "Missing required fields"}), 400

    query_id = str(uuid4())
    new_query = Query(
        id=query_id,
        user_id=user_id,
        company_id=company_id,
        model_id=model_id,
        prompt=prompt,
        result_sql=result_sql,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        created_at=datetime.now()
    )

    usr_db[query_id] = new_query
    return jsonify({"message": "Query created successfully", "query_id": query_id}), 201

@usr_bp.route("/get_queries", methods=["GET"])
def get_queries():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    queries = [query.to_dict() for query in usr_db.values() if query.user_id == user_id]
    return jsonify({"queries": queries}), 200

@usr_bp.route("/get_query/<query_id>", methods=["GET"])
def get_query(query_id):
    query = usr_db.get(query_id)
    if not query:
        return jsonify({"error": "Query not found"}), 404

    return jsonify(query.to_dict()), 200

@usr_bp.route("/delete_query/<query_id>", methods=["DELETE"])
def delete_query(query_id):
    if query_id not in usr_db:
        return jsonify({"error": "Query not found"}), 404

    del usr_db[query_id]
    return jsonify({"message": "Query deleted successfully"}), 200

@usr_bp.route("/get_models", methods=["GET"])
def get_models():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    user = usr_db.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    models = user.get_models()