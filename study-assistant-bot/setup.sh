#!/bin/bash

# Study Assistant Bot - Local Setup Script
# This script prepares your environment for local testing

set -e

echo "=========================================="
echo "Study Assistant Bot - Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"

required_version="3.11"
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 11) else 1)"; then
    echo "Warning: Python 3.11+ is recommended. You have $python_version"
fi

echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate

echo ""
echo "Upgrading pip..."
pip install --upgrade pip

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Creating necessary directories..."
mkdir -p data/uploads data/vectors logs

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and add your OPENAI_API_KEY"
echo "2. Run: source venv/bin/activate (or venv\\Scripts\\activate on Windows)"
echo "3. Run: python bot.py"
echo ""
echo "Your bot token is already configured in .env"
echo ""
