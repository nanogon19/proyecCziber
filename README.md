REQUISITOS:
- Tener Python 3 instalado
- Tener un driver ODBC para SQL Server (Driver 18 recomendado)
- Tener conexión a la misma base de datos (o acceso al entorno de prueba)

PASOS:
1. Abrir terminal en la carpeta backend/
2. Crear entorno virtual (opcional):
   python -m venv venv
   venv\Scripts\activate   (Windows)
3. Instalar dependencias:
   pip install -r requirements.txt
4. Ejecutar el servidor:
   python app.py
5. Abrir el archivo frontend/ver_consulta.html con un navegador

NOTA:
- Modificar en app.py la cadena de conexión si es necesario
