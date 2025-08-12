import pyodbc

driver = "ODBC Driver 18 for SQL Server"  # usa "17" si ese tenés
server = "192.168.0.5,1433"               # o 192.168.0.5\INSTANCIA si aplica
database = "Gamma_CZ"
user = "igonzalez"
pwd = "Zig1-Red6{Voc1"

cn = pyodbc.connect(
    f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={user};PWD={pwd};"
    "Encrypt=yes;TrustServerCertificate=yes;Connection Timeout=5;"
)
print(cn.cursor().execute("SELECT 1").fetchone())
