@echo off
echo 🛡️  Modern Security Analysis Dashboard
echo =====================================
echo.
echo Starting modern GUI application...
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    pause
    exit /b 1
)

REM Launch the modern GUI application
echo 🚀 Launching Modern Security Analysis Dashboard...
python modern_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Application encountered an error
    pause
)
