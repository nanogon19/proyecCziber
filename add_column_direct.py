import psycopg2
import os

# Configuración de la base de datos (ajusta estos valores según tu configuración)
DB_CONFIG = {
    'host': '192.168.0.5',
    'port': 1433,
    'database': 'Gamma_CZ',
    'user': 'igonzalez',
    'password': 'Zig1-Red6{Voc1'
}

try:
    # Conectar a la base de datos
    print("Conectando a la base de datos...")
    
    # Para SQL Server necesitamos usar pyodbc, no psycopg2
    import pyodbc
    
    connection_string = f"DRIVER={{ODBC Driver 18 for SQL Server}};SERVER={DB_CONFIG['host']},{DB_CONFIG['port']};DATABASE={DB_CONFIG['database']};UID={DB_CONFIG['user']};PWD={DB_CONFIG['password']};TrustServerCertificate=yes;Encrypt=no"
    
    conn = pyodbc.connect(connection_string)
    cursor = conn.cursor()
    
    # Verificar si la columna existe
    print("Verificando si la columna database_name existe...")
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'conections' AND COLUMN_NAME = 'database_name'
    """)
    
    result = cursor.fetchone()
    
    if result:
        print("La columna database_name ya existe")
    else:
        print("La columna database_name no existe, agregándola...")
        
        # Agregar la columna
        cursor.execute("ALTER TABLE conections ADD database_name VARCHAR(255)")
        conn.commit()
        print("Columna database_name agregada exitosamente")
    
    # Verificar todas las columnas de la tabla
    print("\nColumnas en la tabla conections:")
    cursor.execute("""
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = 'conections'
        ORDER BY ORDINAL_POSITION
    """)
    
    columns = cursor.fetchall()
    for col in columns:
        print(f"  - {col[0]} ({col[1]})")
    
    cursor.close()
    conn.close()
    print("\nOperación completada exitosamente")
    
except Exception as e:
    print(f"Error: {e}")
    print("\nSi tienes problemas de conexión, verifica:")
    print("1. Que el servidor SQL Server esté ejecutándose")
    print("2. Que las credenciales sean correctas")
    print("3. Que el driver ODBC esté instalado")
