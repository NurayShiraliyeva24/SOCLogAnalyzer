@echo off
echo 🛡️  Advanced Security Intelligence Platform
echo ==========================================
echo.
echo Starting Streamlit web application...
echo The application will open in your default web browser
echo URL: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo.

python -m streamlit run streamlit_app.py --server.port 8501

pause
