from backend.app import create_app
from backend.app.extensions import db
from flask_migrate import Migrate
from backend.app.models import User, Company, Application, Model, Query

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
        "Aplication": Application,
        "Model": Model,
        "Query": Query
    }

if __name__ == "__main__":
    # Crear datos de prueba al iniciar
    crear_datos_prueba()
    app.run(debug=True)

