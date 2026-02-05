# 🔄 PythoRNG Auto-Update System - Complete Setup

## What This Does

✅ **You edit code** → Push to GitHub  
✅ **Friend launches game** → Automatically gets your latest code  
✅ **No manual updates** → They never have to do anything!

---

## 🚀 Quick Start (3 Steps)

### Step 1: Create a GitHub Repository

1. Go to https://github.com/new
2. Create a **private** repository named `pythorng`
3. Clone it locally:
```bash
git clone https://github.com/YOUR_USERNAME/pythorng.git
cd pythorng
```

4. Copy your code into it:
```bash
# Copy the PythoRNG and Macro folders into the cloned repo
# So you have:
# pythorng/
#   ├── PythoRNG/
#   ├── Macro/
#   └── .git/
```

5. Push to GitHub:
```bash
git add .
git commit -m "Initial PythoRNG setup"
git push origin main
```

### Step 2: Set Up Auto-Update System

1. Go to `Extra/PythoRNG-Auto-Update/`
2. Run:
   - **Windows**: `setup.bat`
   - **Mac/Linux**: `bash setup.sh`
3. Edit the `.env` file that appears with your GitHub details:
```
GITHUB_USERNAME=your_username
GITHUB_REPO=pythorng
GITHUB_BRANCH=main
```

### Step 3: Test It!

Run:
- **Windows**: `start_auto_update.bat`
- **Mac/Linux**: `bash start_auto_update.sh`

The system will automatically clone your repo and start the game!

---

## 📋 For Your Friend

Once you've set everything up, just give them **one thing**:

### Option A: Docker Image Link
```
"Download and install Docker"
"Then run: docker pull YOUR_USERNAME/pythorng:latest"
"Then: docker run -it YOUR_USERNAME/pythorng:latest"
```

### Option B: GitHub Link
```
"Install Docker"
"Then clone: git clone https://github.com/YOUR_USERNAME/pythorng.git"
"Then run: bash start_auto_update.sh"
```

### Option C: Pre-Packaged Executable
(We can create a single .exe that handles everything!)

---

## 🔧 How Auto-Updates Work

When your friend runs the game:

```
1. Docker container starts
2. Entrypoint script runs
3. Script checks: "Is there a .git folder?"
   └─ NO? Clone from GitHub for first time
   └─ YES? Pull latest code from GitHub
4. Game launches with your latest code
5. Friend plays!
```

**Result**: Every time they launch, they get your newest updates automatically!

---

## ✏️ Your Workflow (After Setup)

1. **Edit code locally**
```bash
cd pythorng/PythoRNG
# Edit main.py, config.py, etc.
```

2. **Test locally** (optional)
```bash
python main.py
```

3. **Commit and push**
```bash
cd ..  # Go back to pythorng root
git add .
git commit -m "Fix bug: make auras more colorful"
git push origin main
```

4. **Your friend automatically gets it** ✅
   - Next time they launch the game, they'll have your changes!

---

## 🔐 GitHub Token Setup (Optional, For Private Repos)

If you want auto-authentication (no password prompt):

1. Go to https://github.com/settings/tokens
2. Click "Generate new token"
3. Select scopes: `repo` (full control of private repos)
4. Copy the token
5. Add to `.env`:
```
GITHUB_TOKEN=ghp_xxxxxxxxxxxxx
```

---

## 📦 Testing Before Sharing

### Test Folder: `PythoRNG-Test`
This folder is SEPARATE from your live repo - use it to test without affecting GitHub:

1. Copy your current code to `Extra/PythoRNG-Test/`
2. Test locally without pushing
3. Once you're happy, push to GitHub
4. Remove the test folder

---

## 🎯 Full Setup Checklist

- [ ] Create GitHub repository named `pythorng`
- [ ] Push your PythoRNG + Macro folders to GitHub
- [ ] Go to `Extra/PythoRNG-Auto-Update/`
- [ ] Run `setup.bat` (Windows) or `bash setup.sh` (Mac/Linux)
- [ ] Edit `.env` with your GitHub username and repo
- [ ] Run `start_auto_update.bat` or `bash start_auto_update.sh`
- [ ] Confirm both launcher and game start
- [ ] Make a test edit, push to GitHub
- [ ] Verify your friend gets the update automatically

---

## 🆘 Troubleshooting

### "Docker says permission denied"
**Windows**: Run Command Prompt as Administrator
**Mac/Linux**: Add your user to docker group: `sudo usermod -aG docker $USER`

### ".env file won't load"
Make sure:
- No spaces around `=` signs: `GITHUB_USERNAME=john` ✅ not `GITHUB_USERNAME = john` ❌
- No quotes around values: `GITHUB_REPO=pythorng` ✅ not `GITHUB_REPO="pythorng"` ❌

### "Git authentication fails"
If you're using a private repo, set `GITHUB_TOKEN` in `.env` with your personal access token

### "Code isn't updating"
1. Push your changes to GitHub: `git push origin main`
2. Kill the running Docker container
3. Restart with `start_auto_update.bat` or `bash start_auto_update.sh`
4. Docker will pull the latest code

---

## 🚀 Production Deployment

Once you're confident, you can:

### Build a Docker Image
```bash
cd Extra/PythoRNG-Auto-Update
docker build -f Dockerfile.auto-update -t YOUR_USERNAME/pythorng:latest .
docker push YOUR_USERNAME/pythorng:latest
```

Then your friend just runs:
```bash
docker run -it YOUR_USERNAME/pythorng:latest
```

---

## 📊 Architecture

```
Your Computer
    ↓
Git Push to GitHub
    ↓
Friend's Computer
    ↓
docker-compose up
    ↓
entrypoint.sh runs
    ↓
Git Clone/Pull Latest Code
    ↓
Game & Launcher Start
    ↓
Friend Plays with Latest Version ✅
```

---

## ✨ Summary

**You:**
- Edit code, run `git push`
- Done!

**Your Friend:**
- Installs Docker (once)
- Runs the start script
- Always gets your latest updates
- Done!

**No manual syncing. No version confusion. Just updates.** 🎉

---

Next Steps: Configure `.env` and test with `start_auto_update.bat` or `bash start_auto_update.sh`!
