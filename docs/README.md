# PythoRNG - Gacha Game Launcher 🎮

A fun, interactive gacha-style RNG game with Discord integration, biome-specific rewards, and smooth animations.

## 🚀 Quick Start (Easiest Way!)

### I'm completely new to programming:
1. **[Read EASY_SETUP.md](EASY_SETUP.md)** - 2-minute setup for non-programmers
2. Double-click `start_game.bat` (Windows) or run `bash start_game.sh` (Mac/Linux)
3. Play!

### I'm familiar with Docker:
```bash
docker-compose up --build
```

### I want to run without Docker:
```bash
# Install Python 3.11+ and dependencies
pip install requests

# Run the launcher
python ../../Macro/PythoRNG.py
```

---

## 📋 What's Inside

- **PythoRNG.py** - Dashboard/Launcher that monitors your game
- **main.py** - The actual gacha game with beautiful animations
- **config.py** - Centralized configuration
- **requirements.txt** - All dependencies

---

## 🎮 How to Play

1. **Start the Launcher** - See your roll history and biome
2. **Click "Launch Game"** - Open the main game window
3. **Click "ROLL"** - Try your luck getting rare auras!
4. **Track Progress** - Launcher shows your stats in real-time

### Biomes
- **Normal** - Easy, common rewards
- **Glitch** - Rare special auras (2500+ Celestial)
- **Hell** - Rare special auras (1500+ Infernal)
- **Corruption** - Rare special auras (1200+ Corrupted)

### Aura Rarities
- Common (Rarity: 1-100)
- Uncommon (Rarity: 101-300)
- Rare (Rarity: 301-800)
- Epic (Rarity: 801-1500)
- Legendary (Rarity: 1501-2500)
- Mythic (Rarity: 2501-5000)
- Divine (Rarity: 5001+)

---

## 🔧 Features

✅ Biome-specific aura rarity system  
✅ Beautiful particle animations  
✅ Discord webhook integration (notify on rare drops)  
✅ Automatic data backup  
✅ Cross-platform (Windows, Mac, Linux)  
✅ Docker support for easy distribution  
✅ Relative paths (works on any computer)  

---

## 📊 Data & Backups

Your game data is saved in:
- `pythorng_data.json` - Main game data
- `pythorng_backup.json` - Automatic backup

Both files are created automatically on first run.

---

## 🐳 Docker (Recommended)

Everything runs in isolated Docker containers, no installation conflicts!

### First Time:
```bash
./start_game.bat          # Windows
bash start_game.sh        # Mac/Linux
```

### Later:
```bash
docker-compose up
```

### Stop Game:
Press `Ctrl+C` in the terminal

---

## 🔗 Discord Integration

To get rare drop notifications on Discord:

1. Create a Discord webhook
2. Set environment variable: `WEBHOOK_URL=your_webhook_url_here`
3. Run the game
4. Get notified on Discord when you roll rare auras (500+ rarity)!

---

## 🐛 Troubleshooting

**Windows: "Docker is not installed"**
- Download from: https://www.docker.com/products/docker-desktop
- Restart your computer after install
- Try `start_game.bat` again

**Mac/Linux: "Permission denied"**
- Run: `chmod +x start_game.sh`
- Then: `bash start_game.sh`

**"Port already in use"**
- Another instance is running
- Close other PythoRNG windows
- Wait 10 seconds and try again

**Game window won't appear**
- Make sure Docker Desktop is running
- Check if a window opened behind other windows
- Try restarting Docker Desktop

---

## 📦 System Requirements

- **Windows**: Docker Desktop
- **Mac**: Docker Desktop (Intel or Apple Silicon)
- **Linux**: Docker (and Docker Compose)

No Python installation needed if using Docker!

---

## 💡 Tips & Tricks

- Your total roll count is saved forever
- Each biome has different aura distributions
- More rolls = better chance at rare auras
- Check the launcher dashboard for live stats
- Data automatically backs up after each save

---

## 📝 License

[Add your license here]

---

## 🆘 Need Help?

1. Check **EASY_SETUP.md** for beginner-friendly guide
2. Read troubleshooting section above
3. Check Docker container logs: `docker-compose logs`
4. Contact the developer with error messages

---

**Enjoy the game! 🎮✨**
