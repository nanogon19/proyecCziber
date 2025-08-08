#!/usr/bin/env python3
"""
Servidor web simple para servir archivos estáticos del frontend
Ideal para desarrollo y pruebas locales
"""
import http.server
import socketserver
import os
import webbrowser
from pathlib import Path

# Configuración del servidor
PORT = 3000
DIRECTORY = Path(__file__).parent

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Agregar headers CORS para desarrollo
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_GET(self):
        # Redirigir la raíz a datasage-home-fixed.html
        if self.path == '/':
            self.path = '/pages/datasage-home-fixed.html'
        return super().do_GET()

def start_server():
    """Inicia el servidor web"""
    try:
        with socketserver.TCPServer(("", PORT), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Servidor iniciado en: http://localhost:{PORT}")
            print(f"📁 Sirviendo archivos desde: {DIRECTORY}")
            print(f"🌐 Página principal: http://localhost:{PORT}")
            print("📋 Páginas disponibles:")
            print(f"   - Home: http://localhost:{PORT}/pages/datasage-home-fixed.html")
            print(f"   - Login: http://localhost:{PORT}/pages/login.html")
            print(f"   - Register: http://localhost:{PORT}/pages/register.html")
            print("\n🛑 Presiona Ctrl+C para detener el servidor\n")
            
            # Abrir automáticamente en el navegador
            webbrowser.open(f'http://localhost:{PORT}')
            
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido")
    except OSError as e:
        if e.errno == 10048:  # Puerto en uso
            print(f"❌ Error: El puerto {PORT} ya está en uso")
            print("Intenta cambiar el puerto o cerrar otros servidores")
        else:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    start_server()
