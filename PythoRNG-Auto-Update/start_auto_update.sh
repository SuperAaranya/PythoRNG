#!/bin/bash
# PythoRNG Auto-Update - Mac/Linux Launcher

echo ""
echo "========================================"
echo "  PythoRNG - Auto-Update Launcher"
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

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "ERROR: .env file not found!"
    echo ""
    echo "Steps:"
    echo "1. Run: bash setup.sh"
    echo "2. Edit .env with your GitHub details"
    echo "3. Run this script again"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "Loading configuration..."
echo ""

# Source .env (skip comments and empty lines)
export $(grep -v '^#' .env | xargs)

echo "Repository: $GITHUB_USERNAME/$GITHUB_REPO"
echo "Branch: ${GITHUB_BRANCH:-main}"
echo ""

# Start with auto-update
docker compose -f docker-compose.yml up --build

read -p "Press Enter to exit..."
