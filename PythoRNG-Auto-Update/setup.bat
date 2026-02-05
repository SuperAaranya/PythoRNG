@echo off
REM PythoRNG Auto-Update - Windows Setup

echo.
echo ========================================
echo   PythoRNG Auto-Update Setup
echo ========================================
echo.

REM Check if .env exists
if not exist ".env" (
    echo Creating .env file...
    copy .env.example .env
    echo.
    echo ✓ .env file created
    echo.
    echo NEXT STEPS:
    echo 1. Open .env in a text editor
    echo 2. Fill in your GitHub username and repo name
    echo 3. Run: start_auto_update.bat
    echo.
    pause
    start notepad .env
) else (
    echo .env already exists
    echo.
    echo Ready to run! Type: start_auto_update.bat
    echo.
    pause
)
