@echo off

title PythoRNG - Starting...

docker --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Docker is not installed or not in PATH
    echo.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   PythoRNG - Starting Game
echo ========================================
echo.
echo Docker found! Building and starting...
echo.

cd /d "%%~dp0" 2>nul || cd /d "%~dp0"

docker-compose -f "%~dp0docker-compose.yml" up --build
if errorlevel 1 (
    echo.
    echo ERROR: Game failed to start
    echo Check that Docker Desktop is running and the compose file exists
    echo.
    pause
    exit /b 1
)

echo.
echo Game started successfully.
pause
exit /b 0
