#!/usr/bin/env python3
"""
Script para verificar si hay datos en las tablas de empresas, aplicaciones y modelos
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import create_app
from backend.app.models.company import Company
from backend.app.models.application import Application
from backend.app.models.model import Model

def check_dropdown_data():
    app = create_app()
    
    with app.app_context():
        print("=== Verificando datos para dropdowns ===")
        
        # Verificar empresas
        print("\n--- EMPRESAS ---")
        empresas = Company.query.all()
        if empresas:
            print(f"Encontradas {len(empresas)} empresas:")
            for emp in empresas:
                print(f"  - ID: {emp.id_emp}, Nombre: {emp.name}")
        else:
            print("❌ No hay empresas registradas")
            print("Creando empresa de prueba...")
            try:
                nueva_empresa = Company(name="Empresa Demo")
                from backend.app.extensions import db
                db.session.add(nueva_empresa)
                db.session.commit()
                print("✅ Empresa de prueba creada")
            except Exception as e:
                print(f"Error creando empresa: {e}")
        
        # Verificar aplicaciones
        print("\n--- APLICACIONES ---")
        aplicaciones = Application.query.all()
        if aplicaciones:
            print(f"Encontradas {len(aplicaciones)} aplicaciones:")
            for app in aplicaciones:
                print(f"  - ID: {app.id_app}, Nombre: {app.nombre}")
        else:
            print("❌ No hay aplicaciones registradas")
            print("Creando aplicación de prueba...")
            try:
                nueva_app = Application(nombre="DataSage Demo")
                from backend.app.extensions import db
                db.session.add(nueva_app)
                db.session.commit()
                print("✅ Aplicación de prueba creada")
            except Exception as e:
                print(f"Error creando aplicación: {e}")
        
        # Verificar modelos
        print("\n--- MODELOS ---")
        modelos = Model.query.all()
        if modelos:
            print(f"Encontrados {len(modelos)} modelos:")
            for model in modelos:
                print(f"  - ID: {model.id_model}, Nombre: {model.nombre}, Versión: {model.version}")
        else:
            print("❌ No hay modelos registrados")
            print("Creando modelo de prueba...")
            try:
                nuevo_modelo = Model(nombre="GPT Demo", version="1.0")
                from backend.app.extensions import db
                db.session.add(nuevo_modelo)
                db.session.commit()
                print("✅ Modelo de prueba creado")
            except Exception as e:
                print(f"Error creando modelo: {e}")

if __name__ == "__main__":
    check_dropdown_data()
