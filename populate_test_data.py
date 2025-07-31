"""
Script para poblar la base de datos con datos de prueba
"""
import sys
import os

# Agregar el directorio backend al path
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

try:
    from app import create_app
    from app.extensions import db
    from app.models.company import Company
    from app.models.application import Application
    from app.models.model import Model
    
    print("Creando aplicación Flask...")
    app = create_app()
    
    with app.app_context():
        print("Creando tablas si no existen...")
        db.create_all()
        
        # Verificar y crear empresas
        print("\n=== EMPRESAS ===")
        empresas_existentes = Company.query.count()
        print(f"Empresas existentes: {empresas_existentes}")
        
        if empresas_existentes == 0:
            print("Creando empresas de prueba...")
            empresas_prueba = [
                Company(name="Gamma Consultores"),
                Company(name="Tech Solutions"),
                Company(name="Data Analytics Inc")
            ]
            
            for empresa in empresas_prueba:
                db.session.add(empresa)
            
            db.session.commit()
            print("✅ Empresas creadas exitosamente")
        else:
            print("Ya existen empresas en la base de datos")
        
        # Verificar y crear aplicaciones
        print("\n=== APLICACIONES ===")
        apps_existentes = Application.query.count()
        print(f"Aplicaciones existentes: {apps_existentes}")
        
        if apps_existentes == 0:
            print("Creando aplicaciones de prueba...")
            apps_prueba = [
                Application(nombre="DataSage"),
                Application(nombre="Business Intelligence"),
                Application(nombre="Customer Analytics")
            ]
            
            for app in apps_prueba:
                db.session.add(app)
            
            db.session.commit()
            print("✅ Aplicaciones creadas exitosamente")
        else:
            print("Ya existen aplicaciones en la base de datos")
        
        # Verificar y crear modelos
        print("\n=== MODELOS ===")
        modelos_existentes = Model.query.count()
        print(f"Modelos existentes: {modelos_existentes}")
        
        if modelos_existentes == 0:
            print("Creando modelos de prueba...")
            # Obtener la primera aplicación para asociar los modelos
            primera_app = Application.query.first()
            
            if primera_app:
                modelos_prueba = [
                    Model(nombre="GPT-4", version="1.0", app_id=primera_app.id_app),
                    Model(nombre="Claude", version="2.1", app_id=primera_app.id_app),
                    Model(nombre="Llama", version="3.0", app_id=primera_app.id_app)
                ]
                
                for modelo in modelos_prueba:
                    db.session.add(modelo)
                
                db.session.commit()
                print("✅ Modelos creados exitosamente")
            else:
                print("❌ No se encontró ninguna aplicación para asociar los modelos")
        else:
            print("Ya existen modelos en la base de datos")
        
        # Mostrar resumen final
        print("\n=== RESUMEN FINAL ===")
        print(f"Empresas: {Company.query.count()}")
        print(f"Aplicaciones: {Application.query.count()}")
        print(f"Modelos: {Model.query.count()}")
        
        print("\n✅ Script completado exitosamente")

except ImportError as e:
    print(f"Error de importación: {e}")
    print("Asegúrate de que el backend esté configurado correctamente")
except Exception as e:
    print(f"Error inesperado: {e}")
    import traceback
    traceback.print_exc()
