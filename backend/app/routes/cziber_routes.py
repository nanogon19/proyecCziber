from flask import Blueprint, request, jsonify, send_file
from uuid import uuid4
from datetime import datetime
import os
import openai
from openai import OpenAI
import matplotlib.pyplot as plt
import pandas as pd
import re
from sqlalchemy import inspect, text, create_engine
from backend.app.extensions import db
import fitz

from backend.app.extensions import db

from backend.app.models.application import Application
from backend.app.models.company import Company
from backend.app.models.model import Model
from backend.app.models.conection import Conection  
from backend.app.models.query import Query

cziber_bp = Blueprint("cziber", __name__)


@cziber_bp.route("/registrar_empresa", methods=["POST"])
def registrar_empresa():
    data = request.json

    try:
        new_company = Company(
            name=data["name"],
            rut=data.get("rut"),
            logo=data.get("logo")
        )
        
        db.session.add(new_company)
        db.session.commit()

        return jsonify({"message": "Empresa registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error"}), 400
    
@cziber_bp.route("/listar_empresas_id", methods=["GET"])
def listar_empresas():

    empresas = Company.query.all()
    result = {
        empresa.id_emp: {
            "name": empresa.name,
            "id_emp" : empresa.id_emp, 
        } for empresa in empresas
    }
    return jsonify(result), 200

@cziber_bp.route("/registrar_aplicacion", methods=["POST"])
def registrar_aplicacion():
    data = request.json

    try:
        nombre = data["nombre"]

        nueva_aplicacion = Application(
            nombre=nombre
        )

        db.session.add(nueva_aplicacion)
        db.session.commit()

        return jsonify({"message": "Aplicación registrada"}), 201
    
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {str(e)}"}), 400
    
@cziber_bp.route("/asociar_empresa_aplicacion", methods=["POST"])
def asociar_empresa_aplicacion():
    data = request.json
    emp_id = data.get("emp_id")
    app_id = data.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Missing emp_id or app_id parameter"}), 400
    
    company = Company.query.get(emp_id)
    app = Application.query.get(app_id)

    if not company:
        return jsonify({"error": "Empresa no encontrada"}), 404
    if not app: 
        return jsonify({"error": "Aplicación no encontrada"}), 404
    
    company.agregar_aplicacion(app)
    app.agregar_empresa(company)

    db.session.commit()
    return jsonify({"message": "Empresa y aplicación asociadas"}), 200
    
@cziber_bp.route("/registrar_modelo", methods=["POST"])
def registrar_modelo():
    data = request.json

    nombre = data.get("nombre")
    documentacion = data.get("documentacion")
    version = data.get("version")
    emp_id = data.get("emp_id")
    app_id = data.get("app_id")

    if not all([nombre, emp_id, app_id]):
        return jsonify({"error": "Missing required fields"}), 400
    
    emp = Company.query.get(emp_id)
    app = Application.query.get(app_id)

    if not emp:
        return jsonify({"error": "Empresa no encontrada"}), 404
    if not app:
        return jsonify({"error": "Aplicación no encontrada"}), 404
    
    nuevo_modelo = Model(
        nombre=nombre,
        documentacion=documentacion,
        version=version,
        emp_id=emp_id,
        app_id=app_id
    )

    emp.agregar_modelo(nuevo_modelo)
    app.agregar_modelo(nuevo_modelo)

    db.session.add(nuevo_modelo)
    db.session.commit()
    
@cziber_bp.route("/registrar_conexion", methods=["POST"])
def registrar_conexion():
    data = request.json

    ip = data.get("ip")
    puerto = data.get("puerto")
    usuario = data.get("usuario")
    clave = data.get("clave")
    emp_id = data.get("emp_id")
    app_id = data.get("app_id")
    model_id = data.get("model_id")

    if not all([ip, puerto, usuario, clave, emp_id, app_id, model_id]):
        return jsonify({"error": "Missing required fields"}), 400
    
    emp = Company.query.get(emp_id)
    app = Application.query.get(app_id)
    model = Model.query.get(model_id)

    if not emp:
        return jsonify({"error": "Empresa no encontrada"}), 404
    
    if not app:
        return jsonify({"error": "Aplicación no encontrada"}), 404
    
    if not model:
        return jsonify({"error": "Modelo no encontrado"}), 404
    
    new_conection = Conection(
        ip=ip,
        port=puerto,
        user=usuario,
        password=clave,
        app_id=app_id,
        emp_id=emp_id,
        model_id=model_id
    )    

    emp.agregar_conexion(new_conection)
    app.agregar_conexion(new_conection)
    model.agregar_conexion(new_conection)

    db.session.add(new_conection)
    db.session.commit()
    
@cziber_bp.route("/listar_modelos", methods=["GET"])
def listar_modelos():  
    emp_id = request.args.get("emp_id")
    app_id = request.args.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Missing emp_id or app_id parameter"}), 400

    modelos = Model.query.filter_by(empresa_id=emp_id, app_id=app_id).all()

    modelos_serializados = [{
        "id_model": m.id_model,
        "nombre": m.nombre,
        "version": m.version,
        "documentacion": m.documentacion
    } for m in modelos]

    return jsonify({"modelos": modelos_serializados}), 200


@cziber_bp.route("/listar_conexiones", methods=["GET"])
def listar_conexiones():
    emp_id = request.args.get("emp_id")
    app_id = request.args.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Faltan parámetros emp_id o app_id"}), 400

    conexiones = Conection.query.filter_by(emp_id=emp_id, app_id=app_id).all()

    conexiones_serializadas = []
    for con in conexiones:
        conexiones_serializadas.append({
            "id_conn": con.id_conn,
            "ip": con.obtener_ip(),
            "puerto": con.obtener_port(),
            "usuario": con.obtener_usuario(),
            "clave": con.obtener_clave(),
            "modelo_id": con.model_id
        })

    return jsonify({"conexiones": conexiones_serializadas}), 200

@cziber_bp.route("/get_tokens_from_company", methods=["GET"])
def get_tokens_from_company():
    emp_id = request.args.get("emp_id")
    if not emp_id:
        return jsonify({"error": "Falta el parámetro emp_id"}), 400

    empresa = Company.query.get(emp_id)
    if not empresa:
        return jsonify({"error": "Empresa no encontrada"}), 404

    total_tokens = empresa.get_tokens()  # Este método ya está definido en el modelo

    return jsonify({"emp_id": emp_id, "tokens": total_tokens}), 200

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

@cziber_bp.route("/consultar", methods=["POST"])
def consultar():
    engine = db.engine

    connection_string = (
        "mssql+pyodbc://igonzalez:Zig1-Red6{Voc1@192.168.0.5,1433/Gamma_CZ"
        "?driver=ODBC+Driver+18+for+SQL+Server"
        "&TrustServerCertificate=yes"
        "&Encrypt=no"
    )
    engine_consultas = create_engine(connection_string, connect_args={"timeout": 5})


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
        with engine_consultas.connect() as conn:
            resultado = conn.execute(text(sql_generado))
            print(f"Resultados obtenidos: {resultado.rowcount} filas")

            df = pd.DataFrame(resultado.fetchall(), columns=resultado.keys())

            if df.empty:
                return {"sql": sql_generado, "mensaje": "⚠️ Consulta válida, pero sin resultados."}
            
            else:
                # Agregar la consulta a la base de datos
                # query = Query(
                #     prompt = prompt_usuario,
                #     res_SQL = sql_generado,
                #     tokens_in = tokens_in,
                #     tokens_out = tokens_out,
                #     user_id = data.get("user_id"),
                #     model_id = data.get("model_id")
                # )
                # db.session.add(query)
                # db.session.commit()

                generar_pdf_tabla(df, ruta_salida=title_res)
                return send_file(
                    title_res,
                    mimetype="application/pdf",
                    download_name=title_res,  # Opcional, muestra ese nombre en el visor del navegador
                    as_attachment=False       # ✅ Clave: NO forzar descarga
                )   

    except Exception as e:
        return {"error": str(e), "sql": sql_generado}
