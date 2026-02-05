# 🎮 PythoRNG - Friend Setup Guide (Ultra Simple!)

**Read this if someone gave you PythoRNG and you have NO idea what's happening.**

---

## Step 1️⃣: Get Docker (One-Time Setup)

### Windows:
1. Go to: https://www.docker.com/products/docker-desktop
2. Click the big **Download** button (Windows version)
3. Run the installer (the `.exe` file you downloaded)
4. Click **Install** and follow the prompts
5. Restart your computer when it finishes
6. Look for the Docker icon (whale logo) in your taskbar - if it's there, you're done! ✅

### Mac:
1. Go to: https://www.docker.com/products/docker-desktop
2. Choose **Apple Silicon** OR **Intel** (if you don't know, Apple Silicon is newer)
3. Run the installer (the `.dmg` file)
4. Drag Docker to Applications folder
5. Open Applications → Docker.app
6. Docker is ready when you see the whale icon in the menu bar! ✅

### Linux:
```bash
sudo apt update
sudo apt install docker.io docker-compose
sudo usermod -aG docker $USER
```
Restart your terminal and you're ready! ✅

---

## Step 2️⃣: Start the Game (Every Time)

### Windows - The Easiest Way:
1. Find the folder with all the game files
2. Look for **`start_game.bat`** (the file with a gear icon)
3. **Double-click it** 🎮
4. A black window will appear - this is normal!
5. Wait 30 seconds on first run (it downloads the game)
6. The game window will pop up automatically!

### Mac/Linux - Also Easy:
1. Open Terminal
2. Drag the PythoRNG folder into Terminal (this sets the location)
3. Type: `bash start_game.sh`
4. Press Enter
5. Wait 30 seconds on first run
6. Game appears automatically!

---

## 📊 When the Game Opens

You'll see TWO windows:

### Window 1: Dashboard (small one on left)
- Shows your total rolls
- Shows your current biome
- Shows recent aura drops
- Has a **"Launch Game"** button

### Window 2: Game (bigger one on right)
- The actual gacha game!
- Click **"ROLL"** button to try your luck
- See the aura you got with cool animation
- Your stats update in the dashboard automatically

---

## 🎯 How to Play

1. **Click ROLL** → Spin the lottery
2. **See what you got** → Watch the animation
3. **Check your stats** → Dashboard updates automatically
4. **Keep rolling** → Try to get rare ones!

### Rarity Levels (Easiest to Hardest):
- 🟢 Common (easy, usually get this)
- 🔵 Uncommon
- 🟣 Rare
- 🟠 Epic
- 🌟 Legendary
- ✨ Mythic (very rare!)
- 👑 Divine (SUPER RARE!)

---

## 🆘 Something Went Wrong?

### "I double-clicked start_game.bat but nothing happened"
- Make sure Docker is running (look for the whale icon in your taskbar)
- Right-click `start_game.bat` → Run as Administrator
- Wait another minute

### "Docker icon won't appear"
- Restart your computer
- Run Docker again from Applications (Mac) or Start Menu (Windows)
- Wait for it to fully load (5-10 minutes first time)

### "The game window appears but is blank/frozen"
- Wait 30 more seconds (first run takes longer)
- Close and try again

### "It says 'Port already in use'"
- This means you ran it twice
- Close all open game windows
- Try again

### "Still not working?"
- Contact the person who gave you PythoRNG with:
  - What you were doing
  - What error message you got
  - Your operating system (Windows 10/11, Mac, or Linux)

---

## 💾 Where's My Data?

Your progress is **automatically saved**! 

When you close the game:
- ✅ Your rolls are saved
- ✅ Your biome is saved
- ✅ Your rare auras are saved
- ✅ Everything comes back when you reopen the game

**There's a backup too** - even if something goes wrong, your data is safe!

---

## 🔄 Running Again Tomorrow

**Just repeat Step 2!**
- Windows: Double-click `start_game.bat`
- Mac/Linux: `bash start_game.sh`

That's it! Docker handles everything else.

---

## 🎁 Pro Tips

- **More rolls = better chances** at rare auras
- **Different biomes = different rewards** - try switching!
- **Close and reopen anytime** - your progress is always saved
- **Check the dashboard** for cool stats about your rolls

---

## ✨ Enjoy!

You're now playing! Have fun rolling and good luck getting those Divine auras! 🍀

**Questions?** Ask the person who gave you this!

---

*P.S. If you're feeling brave, you can also read `README.md` for more technical details. But honestly, you don't need to!*
