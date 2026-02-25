#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "Starting Pytho-RNG with Docker Compose..."
docker compose -f docker-compose.yml up --build

echo "Done! Press Ctrl+C to stop."
