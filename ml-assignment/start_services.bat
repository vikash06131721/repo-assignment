@echo off
title ML Feature Engineering API & Documentation Setup
color 0B

echo.
echo ================================================
echo 🚀 ML Feature Engineering API ^& Documentation Setup
echo ================================================
echo.

:: Function to check if a command exists
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    pause
    exit /b 1
)

where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed or not in PATH
    echo    Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

where npm >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm is not installed or not in PATH
    pause
    exit /b 1
)

echo 📡 Starting FastAPI Server...
start "FastAPI Server" cmd /c "python main.py"

echo 📚 Starting Documentation Server...
if not exist "docs" (
    echo ❌ docs directory not found
    pause
    exit /b 1
)

cd docs

if not exist "node_modules" (
    echo 📦 Installing dependencies...
    npm install
)

start "Documentation Server" cmd /c "npm start"
cd ..

echo.
echo ⏳ Waiting for services to start...
timeout /t 5 /nobreak >nul

echo.
echo ================================================
echo 🎉 Services are running!
echo ================================================
echo.
echo 📊 API Server:
echo    🔗 Main API: http://localhost:8000
echo    🔗 Health Check: http://localhost:8000/health
echo    🔗 FastAPI Docs: http://localhost:8000/docs
echo    🔗 ReDoc: http://localhost:8000/redoc
echo.
echo 📚 Documentation:
echo    🔗 Beautiful Docs: http://localhost:5002/docs
echo    🔗 Interactive API Tester: http://localhost:5002/docs#testing
echo    🔗 Code Examples: http://localhost:5002/docs#examples
echo.
echo 💡 Tips:
echo    • Use the interactive tester at http://localhost:5002/docs#testing
echo    • Copy code examples from the documentation
echo    • Monitor server status in real-time
echo    • Close the terminal windows to stop the services
echo.
echo ================================================

:: Open the documentation in default browser
start http://localhost:5002/docs

echo Press any key to exit...
pause >nul 