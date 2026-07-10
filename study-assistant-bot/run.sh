#!/bin/bash

# Study Assistant Bot Startup Script

set -e

echo "================================"
echo "Study Assistant Bot"
echo "================================"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✓ Python $python_version"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "📦 Creating virtual environment..."
    python -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "✓ Virtual environment activated"

# Check if requirements are installed
echo ""
echo "📚 Checking dependencies..."
if ! python -c "import telegram" 2>/dev/null; then
    echo "⚙️  Installing dependencies..."
    pip install -q -r requirements.txt
    echo "✓ Dependencies installed"
else
    echo "✓ Dependencies already installed"
fi

# Check if .env exists
echo ""
echo "⚙️  Checking configuration..."
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found"
    echo "Creating from template..."
    cp .env.example .env
    echo "❌ Please edit .env with your API keys"
    echo "   Edit: nano .env"
    echo "   Then run: bash run.sh"
    exit 1
else
    echo "✓ Configuration file found"
fi

# Check if database is initialized
echo ""
echo "🗄️  Checking database..."
if [ ! -f "study_assistant.db" ] && [ ! -d "study_assistant_db" ]; then
    echo "Initializing database..."
    python -c "from database import init_db; init_db()"
    echo "✓ Database initialized"
else
    echo "✓ Database exists"
fi

# Create logs and storage directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p logs storage/uploads storage/generated
echo "✓ Directories ready"

# Start the bot
echo ""
echo "================================"
echo "🚀 Starting Study Assistant Bot"
echo "================================"
echo ""

python bot.py
