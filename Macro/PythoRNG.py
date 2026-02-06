import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import sys
import os
import time
import requests
import json
import socket
from pathlib import Path

WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")  # Set your Discord webhook URL in environment variable for security

BASE_DIR = Path(__file__).parent.parent
GAME_FOLDER = BASE_DIR / "Game" / "Game Making" / "PythoRNG"
DATA_FILE = GAME_FOLDER / "pythorng_data.json"
BACKUP_FILE = GAME_FOLDER / "pythorng_backup.json"

GAME_FOLDER.mkdir(parents=True, exist_ok=True)

COLORS = {
    "bg_dark": "#0a0a0f",
    "bg_header": "#1a1a2e",
    "bg_panel": "#16213e",
    "bg_display": "#0f0f15",
    "border": "#2a3a5e",
    "text_primary": "#00d4ff",
    "text_secondary": "#888888",
    "text_success": "#00ff99",
    "text_error": "#ff3333",
    "text_warning": "#ffaa00",
    "text_light": "#ffffff"
}

class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Pytho-RNG Dashboard")
        self.root.geometry("600x700")
        self.root.configure(bg=COLORS["bg_dark"])
        
        self.process = None
        self.total_rolls = 0
        self.session_rolls = 0
        self.rare_finds = []
        self.is_online = True
        self.load_total_rolls()
        self.setup_gui()
        self.check_connectivity_loop()
    
    def setup_gui(self):
        header = tk.Frame(self.root, bg=COLORS["bg_header"], height=80)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="PYTHO-RNG DASHBOARD", font=("Impact", 28), bg=COLORS["bg_header"], fg=COLORS["text_primary"])
        title_label.pack(pady=15)
        
        btn_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        btn_frame.pack(pady=15)
        
        self.btn_launch = tk.Button(btn_frame, text="LAUNCH GAME", command=self.launch_game, font=("Arial", 14, "bold"), bg="#00d4ff", fg="black", width=25, height=2, cursor="hand2", relief="raised", bd=3)
        self.btn_launch.pack()
        
        tracker_frame = tk.Frame(self.root, bg=COLORS["bg_panel"], bd=2, relief="ridge", highlightbackground=COLORS["border"], highlightthickness=2)
        tracker_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        tracker_title = tk.Label(tracker_frame, text="LIVE TRACKER", font=("Verdana", 13, "bold"), bg=COLORS["bg_panel"], fg=COLORS["text_primary"])
        tracker_title.pack(pady=10)
        
        stats_frame = tk.Frame(tracker_frame, bg=COLORS["bg_panel"])
        stats_frame.pack(pady=10, padx=10, fill="x")
        
        self.lbl_bio = tk.Label(stats_frame, text="Biome: Waiting", font=("Arial", 14, "bold"), bg=COLORS["bg_panel"], fg=COLORS["text_light"], width=25, anchor="center", relief="sunken", bd=2)
        self.lbl_bio.pack(pady=5)
        
        self.lbl_rolls = tk.Label(stats_frame, text="Total: 0 | Session: 0", font=("Arial", 12, "bold"), bg=COLORS["bg_panel"], fg=COLORS["text_secondary"], anchor="center")
        self.lbl_rolls.pack(pady=5)
        
        self.lbl_last_roll = tk.Label(tracker_frame, text="Last Roll: None", font=("Arial", 14, "bold"), bg=COLORS["bg_display"], fg=COLORS["text_success"], width=40, height=2, relief="sunken", bd=2, anchor="center")
        self.lbl_last_roll.pack(pady=10, padx=10)
        
        activity_title = tk.Label(tracker_frame, text="ACTIVITY LOG", font=("Verdana", 11, "bold"), bg=COLORS["bg_panel"], fg=COLORS["text_secondary"])
        activity_title.pack(pady=5)
        
        self.log_box = scrolledtext.ScrolledText(tracker_frame, height=13, bg=COLORS["bg_display"], fg=COLORS["text_success"], font=("Consolas", 9), state="disabled", wrap="word", relief="sunken", bd=2)
        self.log_box.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.connection_frame = tk.Frame(self.root, bg=COLORS["bg_header"], height=30)
        self.connection_frame.pack(side="bottom", fill="x")
        self.connection_frame.pack_propagate(False)
        
        self.connection_label = tk.Label(self.connection_frame, text="Status: Checking", font=("Arial", 10, "bold"), bg=COLORS["bg_header"], fg=COLORS["text_warning"], anchor="w")
        self.connection_label.pack(side="left", padx=12, pady=5)
        
        self.status_bar = tk.Label(self.root, text="Ready", font=("Arial", 9), bg=COLORS["bg_header"], fg=COLORS["text_secondary"], anchor="w")
        self.status_bar.pack(side="bottom", fill="x", padx=5, pady=3)
    
    def launch_game(self):
        if self.process:
            self.log_msg("GAME ALREADY RUNNING")
            return
        
        self.session_rolls = 0
        self.btn_launch.config(state="disabled", text="RUNNING", bg=COLORS["text_secondary"])
        self.status_bar.config(text="Launching game", fg=COLORS["text_primary"])
        
        game_path = GAME_FOLDER / "main.py"
        
        if not game_path.exists():
            self.log_msg(f"ERROR: Game file not found at {game_path}")
            self.btn_launch.config(state="normal", text="LAUNCH GAME", bg="#00d4ff")
            return
        
        cmd = [sys.executable, "-u", str(game_path)]
        
        try:
            self.process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE, 
                creationflags=subprocess.CREATE_NEW_CONSOLE,
                text=True,
                bufsize=1
            )
            
            self.log_msg("Game launched successfully")
            self.status_bar.config(text="Game running", fg=COLORS["text_success"])
            
            threading.Thread(target=self.monitor_game, daemon=True).start()
        except Exception as e:
            self.log_msg(f"ERROR launching: {str(e)}")
            self.btn_launch.config(state="normal", text="LAUNCH GAME", bg="#00d4ff")
    
    def monitor_game(self):
        while self.process and self.process.poll() is None:
            line = self.process.stdout.readline()
            if not line:
                break
            line = line.strip()
            if line:
                self.parse_data(line)
        
        self.on_game_closed()
    
    def parse_data(self, line):
        if line.startswith("BIOME_UPDATE:"):
            biome = line.split(":")[1]
            self.lbl_bio.config(text=f"Biome: {biome}")
            
            if biome == "Glitch":
                self.lbl_bio.config(fg="#ff00ff")
                self.log_msg("RARE BIOME DETECTED: Glitch")
                threading.Thread(target=self.send_biome_webhook, args=(biome,), daemon=True).start()
            elif biome == "Hell":
                self.lbl_bio.config(fg="#ff3333")
                self.log_msg("SPECIAL BIOME: Hell")
                threading.Thread(target=self.send_biome_webhook, args=(biome,), daemon=True).start()
            elif biome == "Corruption":
                self.lbl_bio.config(fg="#bb44ff")
                self.log_msg("SPECIAL BIOME: Corruption")
                threading.Thread(target=self.send_biome_webhook, args=(biome,), daemon=True).start()
            else:
                self.lbl_bio.config(fg=COLORS["text_light"])
            
        elif line.startswith("ROLL:"):
            parts = line.split(":")
            if len(parts) >= 3:
                name = parts[1]
                rarity = parts[2]
                
                self.total_rolls += 1
                self.session_rolls += 1
                self.lbl_rolls.config(text=f"Total: {self.total_rolls} | Session: {self.session_rolls}")
                self.lbl_last_roll.config(text=f"{name} (1/{rarity})")
                
                rarity_val = int(rarity)
                if rarity_val >= 1000:
                    self.lbl_last_roll.config(fg="#ffdd00")
                    self.log_msg(f"DIVINE DROP: {name} (1/{rarity})")
                    self.rare_finds.append(name)
                    threading.Thread(target=self.send_aura_webhook, args=(name, rarity, "Divine"), daemon=True).start()
                elif rarity_val >= 500:
                    self.lbl_last_roll.config(fg="#ff6600")
                    self.log_msg(f"MYTHIC DROP: {name} (1/{rarity})")
                    self.rare_finds.append(name)
                    threading.Thread(target=self.send_aura_webhook, args=(name, rarity, "Mythic"), daemon=True).start()
                elif rarity_val >= 250:
                    self.lbl_last_roll.config(fg="#ff0066")
                    self.log_msg(f"LEGENDARY: {name} (1/{rarity})")
                    threading.Thread(target=self.send_aura_webhook, args=(name, rarity, "Legendary"), daemon=True).start()
                elif rarity_val >= 100:
                    self.lbl_last_roll.config(fg="#9933ff")
                    self.log_msg(f"Epic: {name}")
                else:
                    self.lbl_last_roll.config(fg=COLORS["text_success"])
        
        elif line.startswith("WEBHOOK_SUCCESS:"):
            aura = line.split(":")[1]
            self.log_msg(f"Discord notification sent")
        
        elif line.startswith("WEBHOOK_FAILED:"):
            self.log_msg(f"Webhook notification failed")
        
        elif line.startswith("WEBHOOK_ERROR:"):
            error = line.split(":")[1]
            self.log_msg(f"Webhook error occurred")
    
    def log_msg(self, msg):
        timestamp = time.strftime("%H:%M:%S")
        self.log_box.config(state="normal")
        self.log_box.insert("end", f"[{timestamp}] {msg}\n")
        self.log_box.see("end")
        self.log_box.config(state="disabled")
    
    def check_connectivity(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except (socket.timeout, socket.error):
            return False
    
    def check_connectivity_loop(self):
        was_online = self.is_online
        self.is_online = self.check_connectivity()
        
        if was_online and not self.is_online:
            self.log_msg("OFFLINE - Webhooks disabled")
            self.connection_label.config(text="Status: OFFLINE", fg=COLORS["text_error"])
        elif not was_online and self.is_online:
            self.log_msg("ONLINE - Webhooks enabled")
            self.connection_label.config(text="Status: ONLINE", fg=COLORS["text_success"])
        elif self.is_online:
            self.connection_label.config(text="Status: ONLINE", fg=COLORS["text_success"])
        else:
            self.connection_label.config(text="Status: OFFLINE", fg=COLORS["text_error"])
        
        self.root.after(5000, self.check_connectivity_loop)
    
    def load_total_rolls(self):
        try:
            if DATA_FILE.exists():
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.total_rolls = data.get("total_rolls", 0)
                    print(f"Loaded {self.total_rolls} total rolls")
        except Exception as e:
            print(f"Error loading rolls (trying backup): {e}")
            try:
                if BACKUP_FILE.exists():
                    with open(BACKUP_FILE, 'r') as f:
                        data = json.load(f)
                        self.total_rolls = data.get("total_rolls", 0)
                        print(f"Loaded from backup: {self.total_rolls} total rolls")
            except Exception as e2:
                print(f"Error loading backup: {e2}")
                self.total_rolls = 0
    
    def send_biome_webhook(self, biome):
        if not self.is_online:
            self.log_msg("Webhook skipped: offline")
            return
        try:
            data = {"content": f"BIOME ALERT: {biome} biome detected!"}
            requests.post(WEBHOOK_URL, json=data, timeout=5)
        except Exception as e:
            print(f"Biome webhook error: {e}")
    
    def send_aura_webhook(self, name, rarity, rarity_type):
        if not self.is_online:
            self.log_msg("Webhook skipped: offline")
            return
        try:
            data = {"content": f"{rarity_type.upper()} AURA: {name} (1/{rarity})"}
            requests.post(WEBHOOK_URL, json=data, timeout=5)
        except Exception as e:
            print(f"Aura webhook error: {e}")
    
    def on_game_closed(self):
        self.process = None
        self.btn_launch.config(state="normal", text="LAUNCH GAME", bg="#00d4ff")
        self.status_bar.config(text="Game closed", fg=COLORS["text_warning"])
        self.log_msg(f"Session ended. Rolls: {self.session_rolls} | Rare finds: {len(self.rare_finds)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()
