@echo off
echo 🚀 Iniciando servidor frontend para CZiber...
echo.

REM Verificar si Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado o no está en el PATH
    echo Por favor instala Python desde: https://python.org
    pause
    exit /b 1
)

echo ✅ Python encontrado
echo 📁 Directorio: %~dp0
echo 🌐 Servidor iniciará en: http://localhost:3000
echo 🛑 Presiona Ctrl+C para detener el servidor
echo.

REM Cambiar al directorio del script
cd /d "%~dp0"

REM Iniciar servidor Python
python server.py

echo.
echo 🛑 Servidor detenido
pause
