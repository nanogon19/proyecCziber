from flask import Blueprint, request, jsonify, send_file
from uuid import uuid4
from datetime import datetime
import os
import openai
from openai import OpenAI
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Evita problemas con el backend de matplotlib en servidores sin GUI
import pandas as pd
import re
from sqlalchemy import inspect, text, create_engine
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
        company_id=emp_id,
        app_id=app_id
    )

    emp.agregar_modelo(nuevo_modelo)
    app.agregar_modelo(nuevo_modelo)

    db.session.add(nuevo_modelo)
    db.session.commit()
    
    return jsonify({"message": "Modelo registrado exitosamente", "id_model": nuevo_modelo.id_model}), 201
    
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
        company_id=emp_id,
        model_id=model_id
    )    

    emp.agregar_conexion(new_conection)
    app.agregar_conexion(new_conection)
    model.agregar_conexion(new_conection)

    db.session.add(new_conection)
    db.session.commit()
    
    return jsonify({"message": "Conexión registrada exitosamente", "id_conn": new_conection.id_conn}), 201
    
@cziber_bp.route("/listar_modelos", methods=["GET"])
def listar_modelos():  
    emp_id = request.args.get("emp_id")
    app_id = request.args.get("app_id")

    if not emp_id or not app_id:
        return jsonify({"error": "Missing emp_id or app_id parameter"}), 400

    modelos = Model.query.filter_by(company_id=emp_id, app_id=app_id).all()

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

    # Si no se proporciona emp_id, error
    if not emp_id:
        return jsonify({"error": "Falta el parámetro emp_id"}), 400

    # Si se proporciona app_id, filtrar por empresa y aplicación
    if app_id:
        conexiones = Conection.query.filter_by(company_id=emp_id, app_id=app_id).all()
    else:
        # Si no se proporciona app_id, listar todas las conexiones de la empresa
        conexiones = Conection.query.filter_by(company_id=emp_id).all()

    conexiones_serializadas = []
    for con in conexiones:
        # Obtener información del modelo asociado
        modelo = Model.query.get(con.model_id)
        aplicacion = Application.query.get(con.app_id)
        
        conexion_data = {
            "id_conn": con.id_conn,
            "ip": con.obtener_ip(),
            "puerto": con.obtener_port(),
            "usuario": con.obtener_usuario(),
            "clave": con.obtener_clave(),
            "modelo_id": con.model_id,
            "app_id": con.app_id,
            "company_id": con.company_id
        }
        
        # Agregar información del modelo si existe
        if modelo:
            conexion_data["modelo_nombre"] = modelo.nombre
            conexion_data["modelo_version"] = modelo.version
        
        # Agregar información de la aplicación si existe
        if aplicacion:
            conexion_data["aplicacion_nombre"] = aplicacion.nombre
            
        conexiones_serializadas.append(conexion_data)

    return jsonify({"conexiones": conexiones_serializadas}), 200

@cziber_bp.route("/listar_todas_conexiones", methods=["GET"])
def listar_todas_conexiones():
    """
    Lista todas las conexiones disponibles en el sistema
    """
    try:
        conexiones = Conection.query.all()
        
        conexiones_serializadas = []
        for con in conexiones:
            # Obtener información relacionada
            modelo = Model.query.get(con.model_id)
            aplicacion = Application.query.get(con.app_id)
            empresa = Company.query.get(con.company_id)
            
            conexion_data = {
                "id_conn": con.id_conn,
                "ip": con.obtener_ip(),
                "puerto": con.obtener_port(),
                "usuario": con.obtener_usuario(),
                "clave": con.obtener_clave(),
                "modelo_id": con.model_id,
                "app_id": con.app_id,
                "company_id": con.company_id
            }
            
            # Agregar información del modelo si existe
            if modelo:
                conexion_data["modelo_nombre"] = modelo.nombre
                conexion_data["modelo_version"] = modelo.version
            
            # Agregar información de la aplicación si existe
            if aplicacion:
                conexion_data["aplicacion_nombre"] = aplicacion.nombre
                
            # Agregar información de la empresa si existe
            if empresa:
                conexion_data["empresa_nombre"] = empresa.name
                
            conexiones_serializadas.append(conexion_data)

        return jsonify({
            "conexiones": conexiones_serializadas,
            "total": len(conexiones_serializadas)
        }), 200
        
    except Exception as e:
        return jsonify({"error": f"Error al obtener conexiones: {str(e)}"}), 500

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
    Si la consulta es válida, devuelve la consulta MS SQL completa, sin ninguna explicacion. No inventes relaciones ni tablas ni columnas que no existan.
    En caso de que la consulta no sea válida, devuelve el siguiente mensaje de error: Consulta inválida, por favor intente nuevamente.
    """

    # Llamada a OpenAI
    client = OpenAI(api_key=openai.api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Sos un asistente que genera MS SQL válido basado en el esquema provisto. No inventes relaciones ni tablas ni columnas que no existan."},
            {"role": "user", "content": prompt_completo}
        ]
    )

    sql_generado = response.choices[0].message.content.strip()

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
   
    tokens_in  = response.usage.prompt_tokens + response_title.usage.prompt_tokens
    tokens_out = response.usage.completion_tokens + response_title.usage.completion_tokens

    try:
        with engine_consultas.connect() as conn:
            resultado = conn.execute(text(sql_generado))
            print(f"Resultados obtenidos: {resultado.rowcount} filas")

            rows = resultado.fetchall()
            columns = list(resultado.keys())
            data = [list(row) for row in rows]

            print(f"Columnas obtenidas: {columns}")
            print(f"Datos obtenidos: {data}")

            if not rows:
                return {"sql": sql_generado, "mensaje": "Consulta válida, pero sin resultados."}
            
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

                return jsonify({
                    "columns": columns,
                    "data": data
                })  


    except Exception as e:
        return jsonify({
            "error": str(e),
            "sql": sql_generado
        }), 500

@cziber_bp.route("/listar_aplicaciones", methods=["GET"])
def listar_aplicaciones():
    try:
        engine = db.engine
        with engine.connect() as conn:
            resultado = conn.execute(text("SELECT * FROM applications"))
            rows = resultado.fetchall()
            columns = list(resultado.keys())
            data = [list(row) for row in rows]

            return jsonify({
                "columns": columns,
                "data": data
            })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500

@cziber_bp.route("/agregar_conexion", methods=["POST"])
def agregar_conexion():
    """
    Crear una nueva conexión en el sistema
    """
    try:
        data = request.json
        
        # Validar datos requeridos
        required_fields = ["ip", "port", "user", "password", "app_id", "company_id", "model_id"]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo requerido faltante: {field}"}), 400
        
        # Verificar que las relaciones existan
        app = Application.query.get(data["app_id"])
        if not app:
            return jsonify({"error": "Aplicación no encontrada"}), 404
            
        company = Company.query.get(data["company_id"])
        if not company:
            return jsonify({"error": "Empresa no encontrada"}), 404
            
        model = Model.query.get(data["model_id"])
        if not model:
            return jsonify({"error": "Modelo no encontrado"}), 404
        
        # Crear nueva conexión
        nueva_conexion = Conection(
            ip=data["ip"],
            port=data["port"],
            user=data["user"],
            password=data["password"],
            app_id=data["app_id"],
            company_id=data["company_id"],
            model_id=data["model_id"]
        )
        
        db.session.add(nueva_conexion)
        db.session.commit()
        
        return jsonify({
            "message": "Conexión creada exitosamente",
            "id_conn": nueva_conexion.id_conn
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Error al crear conexión: {str(e)}"}), 500

@cziber_bp.route("/listar_empresas_dropdown", methods=["GET"])
def listar_empresas_dropdown():
    """
    Lista empresas para dropdown del formulario
    """
    try:
        empresas = Company.query.all()
        empresas_list = [{"id": emp.id_emp, "name": emp.name} for emp in empresas]
        return jsonify({"empresas": empresas_list}), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener empresas: {str(e)}"}), 500

@cziber_bp.route("/listar_aplicaciones_dropdown", methods=["GET"])
def listar_aplicaciones_dropdown():
    """
    Lista aplicaciones para dropdown del formulario
    """
    try:
        aplicaciones = Application.query.all()
        apps_list = [{"id": app.id_app, "name": app.nombre} for app in aplicaciones]
        return jsonify({"aplicaciones": apps_list}), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener aplicaciones: {str(e)}"}), 500

@cziber_bp.route("/listar_modelos_dropdown", methods=["GET"])
def listar_modelos_dropdown():
    """
    Lista modelos para dropdown del formulario
    """
    try:
        modelos = Model.query.all()
        modelos_list = [{"id": model.id_model, "name": model.nombre, "version": model.version} for model in modelos]
        return jsonify({"modelos": modelos_list}), 200
    except Exception as e:
        return jsonify({"error": f"Error al obtener modelos: {str(e)}"}), 500