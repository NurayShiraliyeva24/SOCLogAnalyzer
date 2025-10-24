@echo off
echo 🛡️  Security Analysis Dashboard
echo ================================
echo.
echo Starting GUI application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import matplotlib, pandas, tkinter" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install -r requirements_gui.txt
    if errorlevel 1 (
        echo ❌ Failed to install required packages
        pause
        exit /b 1
    )
)

REM Launch the GUI application
echo 🚀 Launching Security Analysis Dashboard...
python gui_app.py

if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error
    pause
)
