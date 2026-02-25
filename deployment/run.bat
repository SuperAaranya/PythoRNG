@echo off
REM Build and run Pytho-RNG on Windows

cd /d "%~dp0"

echo Starting Pytho-RNG with Docker Compose...
docker compose -f docker-compose.yml up --build

echo Done! Press Ctrl+C to stop.
pause
