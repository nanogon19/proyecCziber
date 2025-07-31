import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.app import create_app
from backend.app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Verificar si existe la columna
        print("Verificando columnas existentes...")
        result = db.engine.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'conections'"))
        columns = [row[0] for row in result]
        print(f"Columnas encontradas: {columns}")
        
        if 'database_name' not in columns:
            print('Columna database_name no existe, agregándola...')
            db.engine.execute(text('ALTER TABLE conections ADD COLUMN database_name VARCHAR(255)'))
            print('Columna agregada exitosamente')
        else:
            print('La columna database_name ya existe')
            
        # Verificar conexiones existentes
        print("\nVerificando conexiones existentes...")
        result = db.engine.execute(text("SELECT id_conn, database_name FROM conections"))
        conexiones = result.fetchall()
        print(f"Conexiones encontradas: {len(conexiones)}")
        
        for conn in conexiones:
            print(f"  - ID: {conn[0]}, Database: {conn[1]}")
            
    except Exception as e:
        print(f'Error: {e}')
        import traceback
        traceback.print_exc()
