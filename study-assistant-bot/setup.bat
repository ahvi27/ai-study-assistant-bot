@echo off
REM Study Assistant Bot - Windows Setup Script

echo.
echo ==========================================
echo Study Assistant Bot - Setup
echo ==========================================
echo.

echo Checking Python version...
python --version

echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating necessary directories...
if not exist "data\uploads" mkdir data\uploads
if not exist "data\vectors" mkdir data\vectors
if not exist "logs" mkdir logs

echo.
echo ==========================================
echo Setup Complete!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your OPENAI_API_KEY
echo 2. Run: venv\Scripts\activate.bat
echo 3. Run: python bot.py
echo.
echo Your bot token is already configured in .env
echo.
pause
