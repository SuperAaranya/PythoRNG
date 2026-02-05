@echo off
REM PythoRNG - One-Click Game Launcher for Windows

title PythoRNG - Starting...

REM Check if Docker is installed
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

REM Build and start the containers
docker-compose up --build

REM If we get here, something went wrong
echo.
echo ERROR: Game failed to start
pause
exit /b 1
