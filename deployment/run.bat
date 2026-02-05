@echo off
REM Build and run Pytho-RNG on Windows

echo Building Pytho-RNG Docker image...
docker build -t pythorng:latest .

echo Starting Pytho-RNG with Docker Compose...
docker-compose up

echo Done! Press Ctrl+C to stop.
pause
