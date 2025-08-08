# Script PowerShell para iniciar el servidor frontend
# Ejecuta: .\start-frontend.ps1

Write-Host "🚀 Iniciando servidor frontend para CZiber..." -ForegroundColor Green

# Verificar si Python está instalado
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python encontrado" -ForegroundColor Green
    
    # Cambiar al directorio del frontend
    Set-Location $PSScriptRoot
    
    Write-Host "📁 Directorio actual: $(Get-Location)" -ForegroundColor Cyan
    Write-Host "🌐 Iniciando servidor en http://localhost:3000" -ForegroundColor Yellow
    Write-Host "🛑 Presiona Ctrl+C para detener el servidor" -ForegroundColor Red
    Write-Host ""
    
    # Iniciar servidor Python
    python server.py
} else {
    Write-Host "❌ Python no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Por favor instala Python desde: https://python.org" -ForegroundColor Yellow
}

Write-Host "🛑 Servidor detenido" -ForegroundColor Red
