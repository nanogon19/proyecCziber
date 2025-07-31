"""
Script simple para crear datos de prueba
"""
print("Iniciando script...")

try:
    print("Importando módulos...")
    import sys
    import os
    
    # Agregar backend al path
    backend_path = os.path.join(os.path.dirname(__file__), 'backend')
    if backend_path not in sys.path:
        sys.path.insert(0, backend_path)
    
    print(f"Backend path: {backend_path}")
    
    # Verificar que los archivos existen
    files_to_check = [
        os.path.join(backend_path, 'app', '__init__.py'),
        os.path.join(backend_path, 'app', 'models', 'company.py'),
        os.path.join(backend_path, 'app', 'models', 'application.py'),
        os.path.join(backend_path, 'app', 'models', 'model.py')
    ]
    
    for file_path in files_to_check:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
    
    print("Intentando importar la aplicación...")
    from app import create_app
    print("✅ create_app importado")
    
    from app.extensions import db
    print("✅ db importado")
    
    from app.models.company import Company
    from app.models.application import Application  
    from app.models.model import Model
    print("✅ Modelos importados")
    
    print("Creando aplicación...")
    app = create_app()
    print("✅ Aplicación creada")
    
    with app.app_context():
        print("Creando tablas...")
        db.create_all()
        print("✅ Tablas creadas")
        
        # Contar registros existentes
        empresas_count = Company.query.count()
        apps_count = Application.query.count()
        models_count = Model.query.count()
        
        print(f"Empresas existentes: {empresas_count}")
        print(f"Aplicaciones existentes: {apps_count}")
        print(f"Modelos existentes: {models_count}")
        
        # Crear datos si no existen
        if empresas_count == 0:
            print("Creando empresas...")
            empresa1 = Company(name="Gamma Consultores")
            empresa2 = Company(name="Tech Solutions")
            db.session.add(empresa1)
            db.session.add(empresa2)
            db.session.commit()
            print("✅ Empresas creadas")
        
        if apps_count == 0:
            print("Creando aplicaciones...")
            app1 = Application(nombre="DataSage")
            app2 = Application(nombre="Business Intelligence")
            db.session.add(app1)
            db.session.add(app2)
            db.session.commit()
            print("✅ Aplicaciones creadas")
        
        if models_count == 0:
            print("Creando modelos...")
            primera_app = Application.query.first()
            if primera_app:
                model1 = Model(nombre="GPT-4", version="1.0", app_id=primera_app.id_app)
                model2 = Model(nombre="Claude", version="2.1", app_id=primera_app.id_app)
                db.session.add(model1)
                db.session.add(model2)
                db.session.commit()
                print("✅ Modelos creados")
        
        # Verificar conteos finales
        print(f"\n=== RESULTADO FINAL ===")
        print(f"Empresas: {Company.query.count()}")
        print(f"Aplicaciones: {Application.query.count()}")
        print(f"Modelos: {Model.query.count()}")
        
    print("🎉 Script completado exitosamente!")

except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
