@echo off
echo ============================================================
echo  Venice AI - Web Interface
echo ============================================================
echo.

REM Check if Python is installed
python\python.exe --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

REM Check if requirements are installed
echo Checking dependencies...
python\python.exe -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo.
    echo Installing dependencies...
    python\python.exe -m pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
)

echo.
echo Starting Venice AI Web Interface...
echo.
echo Open your browser to: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

REM Run the application
python\python.exe start.py

pause
