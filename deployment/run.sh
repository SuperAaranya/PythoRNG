#!/bin/bash

# Build and run Pytho-RNG

echo "Building Pytho-RNG Docker image..."
docker build -t pythorng:latest .

echo "Starting Pytho-RNG..."
docker-compose up

echo "Done! Press Ctrl+C to stop."
