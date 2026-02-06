# 🚀 Quick Setup Guide for Docker

## Prerequisites
- Docker Desktop installed and running
- Docker Compose (included with Docker Desktop)

## Quick Start

### 1. Navigate to deployment folder
```bash
cd deployment
```

### 2. Create environment file
```bash
cp ../.env.example .env
```

### 3. (Optional) Configure Discord Webhook
Edit `.env` and add your Discord webhook URL:
```env
WEBHOOK_URL=https://discord.com/api/webhooks/YOUR_WEBHOOK_ID/YOUR_TOKEN
```

### 4. Build and Start Services
```bash
docker-compose up -d --build
```

### 5. Verify Services are Running
```bash
docker-compose ps
docker-compose logs -f pythorng-game
```

### 6. Stop Services
```bash
docker-compose down
```

## Troubleshooting

### Images won't build
```bash
# Clean everything and rebuild
docker-compose down
docker system prune -a
docker-compose up -d --build
```

### Data not persisting
The `pythorng_data.json` is stored in a Docker volume named `game-data`.
View it with:
```bash
docker volume ls
docker volume inspect deployment_game-data
```

### View logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f pythorng-game
docker-compose logs -f pythorng-launcher
```

## Files & Volumes

- **Config**: `.env` - Environment variables
- **Data Volume**: `game-data` - Persists `pythorng_data.json` between runs
- **Network**: `pythorng-net` - Bridges pythorng-game and pythorng-launcher services

## Security Notes

✅ **DO**: Use `.env` file for secrets  
✅ **DO**: Keep `.env` in `.gitignore`  
⚠️ **DON'T**: Commit `.env` to repository  
⚠️ **DON'T**: Put webhook URLs in code  

For more details, see [DOCKER_AND_GIT_FIXES.md](../DOCKER_AND_GIT_FIXES.md)
