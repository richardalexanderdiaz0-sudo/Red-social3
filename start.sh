#!/bin/bash
# Script para iniciar la Red Social

echo "🚀 Iniciando Red Social..."
echo ""

# Verificar si Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 no está instalado"
    exit 1
fi

# Verificar si las dependencias están instaladas
if ! python3 -c "import flask" 2>/dev/null; then
    echo "📦 Instalando dependencias..."
    python3 -m pip install --user -r requirements.txt
    echo ""
fi

# Iniciar la aplicación
echo "✅ Iniciando servidor en http://localhost:5000"
echo "📝 Presiona Ctrl+C para detener el servidor"
echo ""
python3 app.py

