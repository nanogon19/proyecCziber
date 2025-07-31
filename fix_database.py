from backend.app import create_app
from backend.app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        # Verificar si existe la columna
        result = db.engine.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'conections' AND column_name = 'database_name'"))
        exists = result.fetchone()
        
        if not exists:
            print('Columna database_name no existe, agregándola...')
            db.engine.execute(text('ALTER TABLE conections ADD COLUMN database_name VARCHAR(255)'))
            print('Columna agregada exitosamente')
        else:
            print('La columna database_name ya existe')
            
        # Verificar las columnas existentes
        print('\nColumnas en la tabla conections:')
        result = db.engine.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'conections'"))
        for row in result:
            print(f"  - {row[0]}")
            
    except Exception as e:
        print(f'Error: {e}')
