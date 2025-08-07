"""
Script de prueba para el endpoint /consultar
Ejecuta este script después de iniciar el servidor Flask para probar el endpoint
"""

import requests
import json

# Configuración
BASE_URL = "http://localhost:5000"
ENDPOINT = "/cziber/consultar"

def test_consultar_endpoint():
    """Prueba el endpoint /consultar con diferentes escenarios"""
    
    print("=== PRUEBA DEL ENDPOINT /CONSULTAR ===\n")
    
    # Datos de prueba
    test_data = {
        "prompt": "SELECT * FROM usuarios LIMIT 5",
        "connection_string": "mssql+pyodbc://username:password@server:port/database?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes&Encrypt=no"
    }
    
    try:
        print("Enviando solicitud al endpoint...")
        print(f"URL: {BASE_URL}{ENDPOINT}")
        print(f"Datos: {json.dumps(test_data, indent=2)}\n")
        
        response = requests.post(
            f"{BASE_URL}{ENDPOINT}",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=30
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("\n✅ RESPUESTA EXITOSA:")
            print(f"SQL Generado: {data.get('sql', 'No disponible')}")
            print(f"Columnas: {data.get('columns', [])}")
            print(f"Filas de datos: {len(data.get('data', []))}")
            print(f"Tokens utilizados: {data.get('tokens_used', 'No disponible')}")
            print(f"Mensaje: {data.get('message_info', 'No disponible')}")
        else:
            print(f"\n❌ ERROR {response.status_code}:")
            try:
                error_data = response.json()
                print(json.dumps(error_data, indent=2))
            except:
                print(response.text)
                
    except requests.exceptions.ConnectionError:
        print("❌ ERROR: No se pudo conectar al servidor.")
        print("Asegúrate de que el servidor Flask esté ejecutándose en http://localhost:5000")
    except requests.exceptions.Timeout:
        print("❌ ERROR: Timeout - la solicitud tardó demasiado")
    except Exception as e:
        print(f"❌ ERROR inesperado: {e}")

def test_sin_openai():
    """Prueba básica sin OpenAI para verificar la estructura del endpoint"""
    
    print("\n=== PRUEBA BÁSICA (estructura del endpoint) ===\n")
    
    # Datos incompletos para probar validación
    test_data = {
        "prompt": "test query"
        # Sin connection_string ni credenciales
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}{ENDPOINT}",
            headers={"Content-Type": "application/json"},
            json=test_data,
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 400:
            data = response.json()
            print("✅ Validación funcionando correctamente:")
            print(f"Error esperado: {data.get('error')}")
        else:
            print(f"Respuesta: {response.text}")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    print("Iniciando pruebas del endpoint /consultar...")
    print("Asegúrate de tener el servidor Flask ejecutándose en http://localhost:5000\n")
    
    # Prueba básica primero
    test_sin_openai()
    
    # Pregunta si continuar con la prueba completa
    continuar = input("\n¿Deseas continuar con la prueba completa? (requiere OpenAI configurado) [y/N]: ")
    if continuar.lower() in ['y', 'yes', 's', 'si']:
        test_consultar_endpoint()
    
    print("\n=== FIN DE LAS PRUEBAS ===")
