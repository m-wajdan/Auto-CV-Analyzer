@echo off
echo ================================================
echo   Intelligent CV Analyzer - Setup
echo ================================================
echo.

echo Installing required Python packages...
echo.

pip install -r requirements.txt

echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To run the application, execute: run.bat
echo Or use: streamlit run app.py
echo.

pause
