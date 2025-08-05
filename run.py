from backend.app import create_app
from backend.app.extensions import db
from flask_migrate import Migrate
from backend.app.models import User, Company, Application, Model, Query
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

app = create_app()
migrate = Migrate(app, db)

def crear_datos_prueba():
    """Crear datos de prueba si no existen"""
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        
        # Verificar si ya hay datos
        if Company.query.count() == 0:
            print("Creando empresas de prueba...")
            empresas = [
                Company(name="Gamma Consultores"),
                Company(name="Tech Solutions"), 
                Company(name="Data Analytics Inc")
            ]
            for empresa in empresas:
                db.session.add(empresa)
            db.session.commit()
            print("✅ Empresas creadas")
        
        if Application.query.count() == 0:
            print("Creando aplicaciones de prueba...")
            apps = [
                Application(nombre="DataSage"),
                Application(nombre="Business Intelligence"),
                Application(nombre="Customer Analytics")
            ]
            for app in apps:
                db.session.add(app)
            db.session.commit()
            print("✅ Aplicaciones creadas")
        
        if Model.query.count() == 0:
            print("Creando modelos de prueba...")
            primera_app = Application.query.first()
            if primera_app:
                modelos = [
                    Model(nombre="GPT-4", version="1.0", app_id=primera_app.id_app),
                    Model(nombre="Claude", version="2.1", app_id=primera_app.id_app),
                    Model(nombre="Llama", version="3.0", app_id=primera_app.id_app)
                ]
                for modelo in modelos:
                    db.session.add(modelo)
                db.session.commit()
                print("✅ Modelos creados")

@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Company": Company,
        "Application": Application,
        "Model": Model,
        "Query": Query
    }

def run_server():
    """Función para ejecutar el servidor desde línea de comandos"""
    print("🚀 Iniciando DataSage...")
    print("📊 Sistema de análisis de datos con IA")
    print("🌐 Servidor disponible en: http://localhost:5000")
    print("✨ ¡Listo para consultas inteligentes!")
    
    # Crear datos de prueba al iniciar
    crear_datos_prueba()
    
    # Configurar puerto desde variable de entorno o usar 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    )

def main():
    """Función principal para el punto de entrada del paquete"""
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'server':
            run_server()
        elif command == 'init-db':
            with app.app_context():
                db.create_all()
                crear_datos_prueba()
                print("✅ Base de datos inicializada")
        elif command == 'shell':
            with app.app_context():
                import IPython
                IPython.embed()
        else:
            print(f"Comando desconocido: {command}")
            print("Comandos disponibles: server, init-db, shell")
    else:
        run_server()

if __name__ == "__main__":
    main()

