# Docker and Git Compatibility Fixes

## Summary of Changes

This document outlines all the fixes applied to make PythoRNG fully Docker and Git compatible.

### ✅ Completed Fixes

#### 1. **Git Compatibility**

##### Added `.gitignore` file
- Properly ignores Python cache files (`__pycache__/`, `*.pyc`)
- Excludes virtual environment directories (`venv/`, `env/`)
- Prevents committing generated data files (`pythorng_data.json`, `pythorng_backup.json`)
- Excludes environment variable files (`.env*`)
- Ignores IDE configuration files (`.vscode/`, `.idea/`)
- Avoids committing sensitive logs and OS files

##### Created `.env.example` file
- Template file showing required environment variables
- Allows secure setup without exposing secrets
- Documents `WEBHOOK_URL` requirement for Discord integration

##### Removed Hardcoded Secrets
- **Fixed [config/config.py](config/config.py)**: Changed webhook URL from hardcoded string to environment variable only
  - ⚠️ **Security Issue Fixed**: Discord webhook URL is no longer exposed in source code
  - Users must set `WEBHOOK_URL` environment variable or leave it empty

#### 2. **Docker Compatibility**

##### Fixed Docker Build Contexts
- **[deployment/docker-compose.yml](deployment/docker-compose.yml)**: 
  - Corrected `pythorng-game` build to use correct Dockerfile path
  - Fixed `pythorng-launcher` build context from invalid `../../PythoRNG/Macro` to `../Macro`
  - Changed from file-based volumes to named volume `game-data` for better portability
  - Added environment variable support for `WEBHOOK_URL`

- **[deployment/Dockerfile](deployment/Dockerfile)**:
  - Fixed requirements.txt path from `requirements.txt` to `config/requirements.txt`
  - Added proper labels for Docker Hub integration
  - Improved documentation

- **[Macro/Dockerfile](Macro/Dockerfile)**:
  - Simplified WORKDIR to `/app` (was `/app/launcher`)
  - Fixed COPY commands that had issues with spaces in paths
  - Properly creates data directory for volume mounting
  - Removed problematic DISPLAY environment variable for cross-platform compatibility

##### Updated Requirements Files
- **[config/requirements.txt](config/requirements.txt)**: Added Pillow for image support
- **[Macro/requirements.txt](Macro/requirements.txt)**: Added Pillow for image support
- Both files now have proper newline separation between packages

##### Created `.dockerignore` Files
- **[.dockerignore](.dockerignore)**: Excludes unnecessary files from main Docker image
  - Reduces image size by excluding .git, docs, .md files
  - Prevents secrets from being baked into image
  
- **[Macro/.dockerignore](Macro/.dockerignore)**: Optimizes Macro service image

#### 3. **Configuration Fixes**

##### [config/config.py](config/config.py) Improvements
- Fixed `BASE_DIR` calculation to properly resolve parent directory
- Changed from relative to absolute path resolution for Docker compatibility
- Removed default webhook URL to prevent accidental secret exposure
- Proper environment variable handling with empty string fallback

### 🚀 How to Use

#### Setting Up Locally
```bash
# Clone the repository
git clone https://github.com/SuperAaranya/PythoRNG.git
cd PythoRNG

# Create .env file (copy from .env.example)
cp .env.example .env

# Edit .env and add your Discord webhook URL (optional)
# WEBHOOK_URL=your_webhook_url_here
```

#### Docker Setup
```bash
# Navigate to deployment directory
cd deployment

# Create .env file
cp ../.env.example .env

# Edit .env with your settings
# vim .env

# Build and run
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### 🔒 Security Improvements

1. **No Hardcoded Secrets**: All sensitive information is now environment-variable based
2. **Git Safe**: Data files and .env files are properly ignored
3. **Docker Safe**: Secrets are not baked into Docker images
4. **Template Provided**: `.env.example` shows required configuration without exposing data

### 📋 Files Changed

- ✅ `.gitignore` - Created
- ✅ `.env.example` - Created
- ✅ `.dockerignore` - Created
- ✅ `Macro/.dockerignore` - Created
- ✅ `config/config.py` - Fixed paths and removed hardcoded secrets
- ✅ `config/requirements.txt` - Added Pillow, fixed formatting
- ✅ `Macro/requirements.txt` - Added Pillow, fixed formatting
- ✅ `Macro/Dockerfile` - Fixed build paths and directory structure
- ✅ `deployment/Dockerfile` - Fixed requirements.txt path
- ✅ `deployment/docker-compose.yml` - Fixed build contexts and volume mounts

### ✨ Testing

Docker build has been tested and verified:
```
✔ Image deployment-pythorng-game     Built          8.3s
✔ Image deployment-pythorng-launcher Built          8.3s
```

Both services build successfully with all dependencies installed.

### 📝 Next Steps

1. Review the `.env.example` file and configure your environment
2. Run `docker-compose up -d --build` to start the services
3. Check logs with `docker-compose logs -f`
4. Commit changes with confidence knowing secrets are secure

### 🚨 Important Notes

- Always use `.env` files locally (never commit them)
- Keep `.env.example` updated as new config options are added
- Use `WEBHOOK_URL` environment variable for Discord integration
- Data files are volume-mounted, persisting across container restarts
