#!/bin/bash
# PythoRNG - One-Click Game Launcher for Mac/Linux

echo ""
echo "========================================"
echo "  PythoRNG - Starting Game"
echo "========================================"
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker is not installed"
    echo ""
    echo "Please install Docker Desktop from:"
    echo "https://www.docker.com/products/docker-desktop"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Docker found! Building and starting..."
echo ""

# Build and start the containers
docker compose up --build

# If we get here, something went wrong
echo ""
echo "ERROR: Game failed to start"
read -p "Press Enter to exit..."
exit 1
