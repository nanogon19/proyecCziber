from flask import Blueprint, request, jsonify

from uuid import uuid4
from datetime import datetime

from backend.app.extensions import db

from backend.app.models.query import Query
from backend.app.models.user import User

usr_bp = Blueprint("usr", __name__)

@usr_bp.route("/registrar_query", methods=["POST"])
def create_query():
    data = request.json

    user_id = data.get("user_id")
    model_id = data.get("model_id")
    prompt = data.get("prompt")
    result_sql = data.get("result_sql")
    tokens_in = data.get("tokens_in", 0)
    tokens_out = data.get("tokens_out", 0)

    if not user_id or not model_id or not prompt:
        return jsonify({"error": "Missing required parameters"}), 400

    new_query = Query(
        user_id=user_id,
        model_id=model_id,
        prompt=prompt,
        res_SQL=result_sql,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        fecha=datetime.now()
    )

    db.session.add(new_query)
    db.session.commit()

    return jsonify({"message": "Query created successfully"}), 201

@usr_bp.route("/get_queries", methods=["GET"])
def get_queries():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    queries = Query.query.filter_by(user_id=user_id).all()
    return jsonify({"queries": [q.to_dict() for q in queries]}), 200

@usr_bp.route("/get_query/<query_id>", methods=["GET"])
def get_query(query_id):
    query = Query.query.get(query_id)
    if not query:
        return jsonify({"error": "Query not found"}), 404

    return jsonify(query.to_dict()), 200

@usr_bp.route("/delete_query/<query_id>", methods=["DELETE"])
def delete_query(query_id):
    query = Query.query.get(query_id)
    if not query:
        return jsonify({"error": "Query not found"}), 404

    db.session.delete(query)
    db.session.commit()
    return jsonify({"message": "Query deleted successfully"}), 200

@usr_bp.route("/get_models", methods=["GET"])
def get_models():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id parameter"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    models = user.get_models()  # ya definido en el modelo
    return jsonify({"model_ids": models}), 200