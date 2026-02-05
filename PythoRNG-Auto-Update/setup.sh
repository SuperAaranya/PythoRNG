#!/bin/bash
# PythoRNG Auto-Update - Mac/Linux Setup

echo ""
echo "========================================"
echo "  PythoRNG Auto-Update Setup"
echo "========================================"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo ""
    echo "✓ .env file created"
    echo ""
    echo "NEXT STEPS:"
    echo "1. Edit .env with your favorite editor:"
    echo "   nano .env"
    echo "2. Fill in your GitHub username and repo name"
    echo "3. Save and run:"
    echo "   bash start_auto_update.sh"
    echo ""
else
    echo "✓ .env already exists"
    echo ""
    echo "Ready to run!"
    echo "Type: bash start_auto_update.sh"
    echo ""
fi

read -p "Press Enter to continue..."
