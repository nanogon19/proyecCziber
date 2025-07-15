from flask import Blueprint, request, jsonify, send_file

from uuid import uuid4
from datetime import datetime
import os
import openai
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd
import re
from sqlalchemy import inspect, text
import fitz  # PyMuPDF for PDF text extraction

from backend.app.extensions import db, engine

from backend.app.models.query import Query
from backend.app.models.user import User

usr_bp = Blueprint("usr", __name__)
openai.api_key = os.getenv("OPENAI_KEY")

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

def obtener_esquema_ligero(prompt_usuario, engine):
    inspector = inspect(engine)
    esquema = ""
    for tabla in inspector.get_table_names():
        if tabla.lower() in prompt_usuario.lower():
            columnas = inspector.get_columns(tabla)
            cols = ", ".join([f"{col['name']} ({col['type']})" for col in columnas])
            esquema += f"Tabla: {tabla} | Columnas: {cols}\n"
    return esquema.strip()

def extraer_texto_de_pdfs(directorio):
    texto_total = ""
    for archivo in os.listdir(directorio):
        if archivo.lower().endswith(".pdf"):
            ruta = os.path.join(directorio, archivo)
            with fitz.open(ruta) as doc:
                for pagina in doc:
                    texto_total += pagina.get_text()
            texto_total += "\n\n"
    return texto_total.strip()

def generar_pdf_tabla(df, ruta_salida="resultado.pdf"):
    fig, ax = plt.subplots(figsize=(len(df.columns) * 1.5, len(df) * 0.5 + 1))
    ax.axis('tight')
    ax.axis('off')
    tabla = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        loc='center',
        cellLoc='center'
    )
    tabla.auto_set_font_size(False)
    tabla.set_fontsize(8)
    tabla.scale(1.2, 1.2)
    plt.savefig(ruta_salida, bbox_inches='tight')
    plt.close()

@usr_bp.route("/consultar", methods=["POST"])
async def consultar():
    data = request.get_json()
    prompt_usuario = data["prompt"]
    esquema = obtener_esquema_ligero(prompt_usuario, engine)
    ruta_documentacion = r"C:\Users\nanog\OneDrive\Desktop\Cziber\proySQL-IA\contexto"
    contexto_pdf = extraer_texto_de_pdfs(ruta_documentacion)

    prompt_completo = f"""
    Documentación adicional:
    {contexto_pdf}
    Base de datos:
    {esquema}
    Usuario dice: {prompt_usuario}
    Si la consulta es válida, devuelve la consulta MS SQL completa, sin ninguna explicacion.
    En caso de que la consulta no sea válida, devuelve el siguiente mensaje de error: Consulta inválida, por favor intente nuevamente.
    """

    # Llamada a OpenAI
    client = OpenAI(api_key=openai.api_key)

    response = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Sos un asistente que genera MS SQL válido basado en el esquema provisto."},
            {"role": "user", "content": prompt_completo}
        ]
    )

    sql_generado = response.choices[0].message.content.strip()

    # Limpieza de delimitadores ```sql
    if sql_generado.startswith("```"):
        sql_generado = sql_generado.strip("`").strip()
        if sql_generado.lower().startswith("sql"):
            sql_generado = sql_generado[3:].strip()
    print(f"SQL Generada: {sql_generado}")

    prompt_titulo = f"""
    Basado en este pedido del usuario:
    \"{prompt_usuario}\"
    Genera un titulo descriptivo para el PDF de maximo 5 palabras.
    """
    response_title = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Sos un asistente que genera nombres de archivos descriptivos."},
            {"role": "user", "content": prompt_titulo}
        ]
    )

    print("Tokens usados:", response.usage.total_tokens + response_title.usage.total_tokens)
    print("Prompt tokens:", response.usage.prompt_tokens + response_title.usage.prompt_tokens)
    print("Completion tokens:", response.usage.completion_tokens + response_title.usage.completion_tokens)

    title_pdf = response_title.choices[0].message.content.strip()
    title_pdf = re.sub(r'[\\/*?:<>|\"\'\n]', '', title_pdf)
    title_pdf = title_pdf.replace(" ", "_")
    title_pdf = title_pdf.lower()
    title_res = f"{title_pdf}.pdf"
    # 📦 Ejecutar la consulta SQL y generar PDF si hay resultados
    tokens_in  = response.usage.prompt_tokens + response_title.usage.prompt_tokens
    tokens_out = response.usage.completion_tokens + response_title.usage.completion_tokens

    try:
        with engine.connect() as conn:
            resultado = conn.execute(text(sql_generado))
            print(f"Resultados obtenidos: {resultado.rowcount} filas")

            df = pd.DataFrame(resultado.fetchall(), columns=resultado.keys())

            if df.empty:
                return {"sql": sql_generado, "mensaje": "⚠️ Consulta válida, pero sin resultados."}
            
            else:
                # Agregar la consulta a la base de datos
                query = Query(
                    prompt = prompt_usuario,
                    res_SQL = sql_generado,
                    tokens_in = tokens_in,
                    tokens_out = tokens_out,
                    user_id = data.get("user_id"),
                    model_id = data.get("model_id")
                )
                db.session.add(query)
                db.session.commit()

                generar_pdf_tabla(df, ruta_salida=title_res)
                return send_file(title_res, media_type="application/pdf", filename=title_res)

    except Exception as e:
        return {"error": str(e), "sql": sql_generado}
