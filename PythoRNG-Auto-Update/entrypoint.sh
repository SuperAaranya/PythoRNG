#!/bin/bash
# PythoRNG Auto-Update Entrypoint
# Handles pulling latest code from GitHub before running the application

set -e

echo "=========================================="
echo "  PythoRNG - Auto-Update Launcher"
echo "=========================================="
echo ""

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
    echo "✓ Configuration loaded from .env"
else
    echo "⚠ No .env file found - using defaults"
    GITHUB_BRANCH=${GITHUB_BRANCH:-main}
    UPDATE_CHECK_INTERVAL=${UPDATE_CHECK_INTERVAL:-0}
fi

# Validate required variables
if [ -z "$GITHUB_USERNAME" ] || [ -z "$GITHUB_REPO" ]; then
    echo "❌ ERROR: GITHUB_USERNAME and GITHUB_REPO must be set in .env"
    echo ""
    echo "Steps:"
    echo "1. Copy .env.example to .env"
    echo "2. Edit .env and fill in your GitHub username and repo name"
    echo "3. Run this script again"
    exit 1
fi

GITHUB_REPO_URL="https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}.git"
BRANCH=${GITHUB_BRANCH:-main}

echo "Repository: $GITHUB_REPO_URL"
echo "Branch: $BRANCH"
echo ""

# Function to pull from GitHub
pull_from_github() {
    echo "⬇️  Checking for updates from GitHub..."
    
    if [ -d ".git" ]; then
        echo "Repository already exists, pulling latest..."
        git fetch origin
        git checkout $BRANCH
        git pull origin $BRANCH
    else
        echo "First-time setup: Cloning repository..."
        git clone --branch $BRANCH $GITHUB_REPO_URL .
    fi
    
    echo "✓ Repository updated"
    echo ""
}

# Pull initial code
pull_from_github

# Start the application in background
echo "🎮 Starting application..."
echo ""

cd PythoRNG
python main.py &
MAIN_PID=$!

cd ../Macro
python PythoRNG.py &
LAUNCHER_PID=$!

# Wait for both processes
wait $MAIN_PID $LAUNCHER_PID
