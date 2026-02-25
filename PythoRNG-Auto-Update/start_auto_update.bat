@echo off
REM PythoRNG Auto-Update - Windows Launcher

title PythoRNG - Auto Update Mode

echo.
echo ========================================
echo   PythoRNG - Auto-Update Launcher
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo.
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    echo.
    pause
    exit /b 1
)

REM Check if .env exists
if not exist ".env" (
    echo ERROR: .env file not found!
    echo.
    echo Steps:
    echo 1. Run: setup.bat
    echo 2. Edit the .env file with your GitHub username and repo
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo Loading configuration from .env...
echo.

REM Load .env (basic parsing for Windows)
for /f "tokens=1,2 delims==" %%A in (.env) do (
    if not "%%A"=="" (
        if not "%%A:~0,1%"=="#" (
            set %%A=%%B
        )
    )
)

echo Repository: %GITHUB_USERNAME%/%GITHUB_REPO%
echo Branch: %GITHUB_BRANCH%
echo.

REM Build and start with auto-update
docker compose -f docker-compose.yml up --build

pause
