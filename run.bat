@echo off
REM CyberSense Local Development Script for Windows
REM This script helps you run the project locally on Windows

setlocal EnableDelayedExpansion

echo.
echo ========================================
echo   CyberSense - Local Development
echo ========================================
echo.

REM Check Python
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.9 or higher
    pause
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo [OK] Python %PYTHON_VERSION% found
echo.

:MENU
echo.
echo What would you like to do?
echo.
echo 1. Setup backend (first time only)
echo 2. Run backend server
echo 3. Run frontend server
echo 4. Run both (backend + frontend)
echo 5. Run tests
echo 6. Exit
echo.
set /p choice="Enter choice [1-6]: "

if "%choice%"=="1" goto SETUP
if "%choice%"=="2" goto BACKEND
if "%choice%"=="3" goto FRONTEND
if "%choice%"=="4" goto BOTH
if "%choice%"=="5" goto TESTS
if "%choice%"=="6" goto EXIT
echo [ERROR] Invalid choice
goto MENU

:SETUP
echo.
echo Setting up backend...
cd backend

if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

echo Downloading NLTK data...
python -c "import nltk; nltk.download('stopwords', quiet=True); nltk.download('wordnet', quiet=True); nltk.download('omw-1.4', quiet=True)"

echo.
echo [OK] Backend setup complete
cd ..
goto MENU

:BACKEND
echo.
echo Starting backend server...
cd backend
call venv\Scripts\activate.bat

if not exist "models\best_model.joblib" (
    echo [WARNING] Models not found - running in DEMO MODE
    echo            To use ML models, train them using notebooks/Main.ipynb
    echo.
)

echo Backend running at: http://localhost:5000
echo Press Ctrl+C to stop
echo.

python app\main.py
cd ..
goto END

:FRONTEND
echo.
echo Starting frontend server...
cd frontend

echo Frontend running at: http://localhost:3000
echo Press Ctrl+C to stop
echo.

python -m http.server 3000 --directory public
cd ..
goto END

:BOTH
echo.
echo Starting both servers...
echo Backend will run in a new window
echo.

start "CyberSense Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python app\main.py"

timeout /t 3 /nobreak >nul

echo [OK] Backend started in new window
echo.
goto FRONTEND

:TESTS
echo.
echo Running tests...
cd backend
call venv\Scripts\activate.bat

echo Installing test dependencies...
pip install --quiet pytest pytest-cov

echo.
echo Running pytest...
python -m pytest tests\ -v

cd ..
pause
goto MENU

:EXIT
echo.
echo Goodbye!
goto END

:END
endlocal
