# Pytho-RNG Distribution Guide

## For End Users

### Option 1: Docker (Recommended - Works on any PC)

**Requirements:** Docker and Docker Compose installed

**Steps:**
1. Download the project folder
2. Open terminal in the project directory
3. Run:
   ```bash
   docker-compose up
   ```
   This will start both the game and launcher automatically

**To stop:**
   ```bash
   docker-compose down
   ```

---

### Option 2: Local Python Installation

**Requirements:** Python 3.11+

**Steps:**
1. Download the project folder
2. Open terminal in the project directory
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the game:
   ```bash
   python main.py
   ```
5. Or run the launcher (from Macro folder):
   ```bash
   python PythoRNG.py
   ```

---

### Option 3: Standalone Executable (Windows)

**Steps:**
1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```
2. Navigate to project folder
3. Create executable:
   ```bash
   pyinstaller --onefile --windowed --add-data "pythorng_data.json:." main.py
   ```
4. Find executable in `dist/` folder

---

## For Developers

### Project Structure
```
PythoRNG/
├── main.py                 (Game client)
├── config.py              (Configuration)
├── requirements.txt       (Python dependencies)
├── Dockerfile            (Docker image)
├── docker-compose.yml    (Multi-container setup)
├── .dockerignore         (Docker exclusions)
├── pythorng_data.json    (Game data - auto-created)
└── pythorng_backup.json  (Backup data - auto-created)
```

### Environment Variables
Set these before running:
- `WEBHOOK_URL` - Discord webhook URL
- `DISPLAY` - X11 display (Linux/Mac only)

### Building Docker Image
```bash
docker build -t pythorng:latest .
```

### Running Docker Container
```bash
docker run -it pythorng:latest
```

### Customizing for Your PC
Edit `config.py` to change paths or settings without modifying main.py

---

## Troubleshooting

**"Module not found" error:**
- Run: `pip install -r requirements.txt`

**Data not persisting in Docker:**
- Ensure volumes are mounted in docker-compose.yml

**Can't see GUI in Docker (Linux):**
- Install X11 forwarding
- Run: `xhost +local:docker`

**Wrong paths on different PC:**
- All paths are now relative to script location
- Config.py handles all path resolution
