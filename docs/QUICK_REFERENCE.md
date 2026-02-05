# 📋 Quick Reference Card

## For You (Developer)

### Daily Workflow
```bash
# Edit code
code Extra/Game/Game\ Making/PythoRNG/main.py

# Test locally (optional)
python Extra/Game/Game\ Making/PythoRNG/main.py

# Push to GitHub when ready
cd ~/pythorng
git add .
git commit -m "Your message"
git push origin main

# DONE! Your friend gets it automatically next launch! ✅
```

### One-Time Setup
```bash
# Create GitHub repo
# Go to: https://github.com/new → create "pythorng"

# Clone it
git clone https://github.com/YOUR_USERNAME/pythorng.git
cd pythorng

# Copy your code
# Add PythoRNG/ and Macro/ folders

# Push
git add .
git commit -m "Initial"
git push origin main

# Configure auto-update
cd Extra/PythoRNG-Auto-Update
setup.bat              # Windows
# OR
bash setup.sh          # Mac/Linux

# Edit .env file with GitHub username + repo name
```

---

## For Your Friend

### First Time
1. Install Docker → https://docker.com/products/docker-desktop
2. Clone the repo
3. Run `start_auto_update.bat` or `bash start_auto_update.sh`
4. Play!

### Every Other Time
Just run the start script - they automatically get your updates!

---

## Three Folders Explained

| Folder | Purpose | For Whom |
|--------|---------|----------|
| `Extra/Game/Game Making/PythoRNG/` | Original code | You (dev) |
| `Extra/PythoRNG-Test/` | Testing space | You (before pushing) |
| `Extra/PythoRNG-Auto-Update/` | Production setup | Your friend |

---

## Commands Cheat Sheet

### Setup (One-Time)
```bash
# Windows
cd Extra/PythoRNG-Auto-Update
setup.bat

# Mac/Linux
cd Extra/PythoRNG-Auto-Update
bash setup.sh
```

### Push Updates
```bash
cd ~/pythorng
git add .
git commit -m "Update message"
git push origin main
```

### Run Auto-Update
```bash
# Windows
cd Extra/PythoRNG-Auto-Update
start_auto_update.bat

# Mac/Linux
cd Extra/PythoRNG-Auto-Update
bash start_auto_update.sh
```

### Emergency Cleanup
```bash
# Reset Docker (if something breaks)
docker system prune -a

# Delete test folder (always safe)
rm -rf Extra/PythoRNG-Test/
```

---

## What Your Friend Sees

```
Friend installs Docker
         ↓
Runs start_auto_update script
         ↓
Docker pulls your code from GitHub
         ↓
Game launches
         ↓
They play! ✅
         ↓
Next week, they run it again...
         ↓
Docker pulls your NEW code
         ↓
They automatically have your updates! ✅✅✅
```

**No manual updates. No "get the latest version." Just automatic!**

---

## Remember

- 📁 Edit in: `Extra/Game/Game Making/PythoRNG/`
- 🧪 Test in: `Extra/PythoRNG-Test/`
- 🚀 Deploy with: `Extra/PythoRNG-Auto-Update/`
- ☁️ Store in: GitHub repository
- 👥 Friend uses: Auto-update system (automatic!)

---

## 📞 Quick Troubleshooting

**"Docker won't start?"**
- Install Docker Desktop
- Restart your computer
- Make sure Docker is running (check taskbar/menu bar)

**"Git won't push?"**
- Make sure you have internet
- Verify GitHub username and repo name in `.env`
- Use personal access token if using 2FA

**"Test folder got messed up?"**
- Delete it - it's safe to delete!
- `rm -rf Extra/PythoRNG-Test/`
- Copy fresh and try again

**"Friend says they're not getting updates?"**
- Make sure you pushed to GitHub: `git log`
- They need to restart their Docker container
- Next launch will have updates

---

## ✨ That's It!

You now have a complete, automated, friend-friendly game distribution system.

Enjoy! 🎮
