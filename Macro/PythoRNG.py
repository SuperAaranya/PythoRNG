import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
import subprocess
import threading
import sys
import os
import time
import requests
import json
import socket
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_file = Path.home() / ".pythorng_launcher_config.json"
        self.config = self.load_config()
    
    def load_config(self):
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def save_config(self):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            print(f"Failed to save config: {e}")
            return False
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()

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
    "text_light": "#ffffff",
    "accent_purple": "#bb44ff",
    "accent_gold": "#ffdd00"
}

class Launcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Pytho-RNG Dashboard & Launcher v2.0")
        self.root.geometry("700x800")
        self.root.configure(bg=COLORS["bg_dark"])
        
        self.config_manager = ConfigManager()
        self.process = None
        self.total_rolls = 0
        self.session_rolls = 0
        self.rare_finds = []
        self.is_online = True
        self.session_start_time = None
        
        if not self.check_configuration():
            self.show_setup_wizard()
        else:
            self.initialize_launcher()
    
    def check_configuration(self):
        game_folder = self.config_manager.get("game_folder")
        webhook_url = self.config_manager.get("webhook_url")
        
        if not game_folder:
            return False
        
        game_path = Path(game_folder) / "main.py"
        if not game_path.exists():
            return False
        
        return True
    
    def show_setup_wizard(self):
        setup_window = tk.Toplevel(self.root)
        setup_window.title("Launcher Setup")
        setup_window.geometry("550x450")
        setup_window.configure(bg=COLORS["bg_panel"])
        setup_window.transient(self.root)
        setup_window.grab_set()
        
        tk.Label(setup_window, text="Pytho-RNG Launcher Setup", 
                font=("Impact", 20), bg=COLORS["bg_panel"], 
                fg=COLORS["text_primary"]).pack(pady=20)
        
        tk.Label(setup_window, text="Configure launcher settings:", 
                font=("Arial", 12), bg=COLORS["bg_panel"], 
                fg=COLORS["text_light"]).pack(pady=10)
        
        folder_frame = tk.Frame(setup_window, bg=COLORS["bg_panel"])
        folder_frame.pack(pady=15, padx=20, fill="x")
        
        tk.Label(folder_frame, text="Game Folder (containing main.py):", 
                font=("Arial", 11, "bold"),
                bg=COLORS["bg_panel"], fg=COLORS["text_light"]).pack(anchor="w")
        
        folder_entry = tk.Entry(folder_frame, font=("Arial", 10), width=45,
                               bg=COLORS["bg_display"], fg=COLORS["text_light"],
                               insertbackground=COLORS["text_primary"])
        folder_entry.pack(side="left", padx=(0, 5), pady=5)
        
        def browse_folder():
            folder = filedialog.askdirectory(title="Select Game Folder")
            if folder:
                folder_entry.delete(0, tk.END)
                folder_entry.insert(0, folder)
        
        tk.Button(folder_frame, text="Browse", command=browse_folder,
                 bg=COLORS["text_primary"], fg="black", 
                 font=("Arial", 9, "bold")).pack()
        
        webhook_frame = tk.Frame(setup_window, bg=COLORS["bg_panel"])
        webhook_frame.pack(pady=15, padx=20, fill="x")
        
        tk.Label(webhook_frame, text="Discord Webhook URL (optional):", 
                font=("Arial", 11, "bold"),
                bg=COLORS["bg_panel"], fg=COLORS["text_light"]).pack(anchor="w")
        
        webhook_entry = tk.Entry(webhook_frame, font=("Arial", 10), width=55,
                                bg=COLORS["bg_display"], fg=COLORS["text_light"],
                                insertbackground=COLORS["text_primary"])
        webhook_entry.pack(pady=5)
        
        threshold_frame = tk.Frame(setup_window, bg=COLORS["bg_panel"])
        threshold_frame.pack(pady=10, padx=20, fill="x")
        
        tk.Label(threshold_frame, text="Notification Rarity Threshold:", 
                font=("Arial", 11, "bold"),
                bg=COLORS["bg_panel"], fg=COLORS["text_light"]).pack(anchor="w")
        
        threshold_entry = tk.Entry(threshold_frame, font=("Arial", 10), width=15,
                                  bg=COLORS["bg_display"], fg=COLORS["text_light"],
                                  insertbackground=COLORS["text_primary"])
        threshold_entry.insert(0, "500")
        threshold_entry.pack(anchor="w", pady=5)
        
        tk.Label(setup_window, 
                text="Webhook sends notifications for rare drops above threshold",
                font=("Arial", 8), bg=COLORS["bg_panel"], 
                fg=COLORS["text_secondary"]).pack(pady=5)
        
        def save_and_continue():
            game_folder = folder_entry.get().strip()
            webhook_url = webhook_entry.get().strip()
            threshold = threshold_entry.get().strip()
            
            if not game_folder:
                messagebox.showerror("Error", "Please select a game folder!")
                return
            
            game_path = Path(game_folder) / "main.py"
            if not game_path.exists():
                messagebox.showerror("Error", f"main.py not found in {game_folder}")
                return
            
            try:
                threshold_val = int(threshold) if threshold else 500
            except:
                threshold_val = 500
            
            self.config_manager.set("game_folder", game_folder)
            self.config_manager.set("webhook_url", webhook_url)
            self.config_manager.set("notification_threshold", threshold_val)
            
            setup_window.destroy()
            self.initialize_launcher()
        
        tk.Button(setup_window, text="Save & Continue", command=save_and_continue,
                 font=("Arial", 14, "bold"), bg=COLORS["text_success"],
                 fg="black", width=20, height=2, cursor="hand2").pack(pady=30)
    
    def initialize_launcher(self):
        self.game_folder = Path(self.config_manager.get("game_folder"))
        self.webhook_url = self.config_manager.get("webhook_url", "")
        self.notification_threshold = self.config_manager.get("notification_threshold", 500)
        
        self.data_file = self.game_folder / "pythorng_data.json"
        self.backup_file = self.game_folder / "pythorng_backup.json"
        
        self.load_total_rolls()
        self.setup_gui()
        self.check_connectivity_loop()
        self.update_session_time()
    
    def setup_gui(self):
        header = tk.Frame(self.root, bg=COLORS["bg_header"], height=90)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        title_label = tk.Label(header, text="PYTHO-RNG LAUNCHER", 
                              font=("Impact", 32), bg=COLORS["bg_header"], 
                              fg=COLORS["text_primary"])
        title_label.pack(pady=10)
        
        subtitle = tk.Label(header, text="Game Monitoring & Webhook Dashboard", 
                           font=("Arial", 10), bg=COLORS["bg_header"], 
                           fg=COLORS["text_secondary"])
        subtitle.pack()
        
        control_frame = tk.Frame(self.root, bg=COLORS["bg_dark"])
        control_frame.pack(pady=15)
        
        self.btn_launch = tk.Button(control_frame, text="LAUNCH GAME", 
                                    command=self.launch_game, 
                                    font=("Arial", 14, "bold"), 
                                    bg="#00d4ff", fg="black", width=20, height=2, 
                                    cursor="hand2", relief="raised", bd=3)
        self.btn_launch.grid(row=0, column=0, padx=5)
        
        self.btn_settings = tk.Button(control_frame, text="SETTINGS", 
                                      command=self.show_settings,
                                      font=("Arial", 14, "bold"),
                                      bg=COLORS["text_warning"], fg="black", 
                                      width=15, height=2, cursor="hand2", 
                                      relief="raised", bd=3)
        self.btn_settings.grid(row=0, column=1, padx=5)
        
        stats_container = tk.Frame(self.root, bg=COLORS["bg_dark"])
        stats_container.pack(fill="x", padx=15, pady=10)
        
        session_frame = tk.Frame(stats_container, bg=COLORS["bg_panel"], 
                                bd=2, relief="ridge")
        session_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(session_frame, text="SESSION INFO", font=("Verdana", 10, "bold"),
                bg=COLORS["bg_panel"], fg=COLORS["text_primary"]).pack(pady=5)
        
        self.lbl_session_time = tk.Label(session_frame, text="Duration: 00:00:00",
                                        font=("Arial", 11), bg=COLORS["bg_panel"],
                                        fg=COLORS["text_light"])
        self.lbl_session_time.pack(pady=3)
        
        self.lbl_session_rolls = tk.Label(session_frame, text="Session Rolls: 0",
                                         font=("Arial", 11), bg=COLORS["bg_panel"],
                                         fg=COLORS["text_light"])
        self.lbl_session_rolls.pack(pady=3)
        
        self.lbl_rolls_per_min = tk.Label(session_frame, text="Rate: 0/min",
                                         font=("Arial", 11), bg=COLORS["bg_panel"],
                                         fg=COLORS["text_light"])
        self.lbl_rolls_per_min.pack(pady=3)
        
        total_frame = tk.Frame(stats_container, bg=COLORS["bg_panel"], 
                              bd=2, relief="ridge")
        total_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        tk.Label(total_frame, text="TOTAL STATS", font=("Verdana", 10, "bold"),
                bg=COLORS["bg_panel"], fg=COLORS["text_primary"]).pack(pady=5)
        
        self.lbl_total_rolls = tk.Label(total_frame, text=f"Total Rolls: {self.total_rolls}",
                                       font=("Arial", 11), bg=COLORS["bg_panel"],
                                       fg=COLORS["text_light"])
        self.lbl_total_rolls.pack(pady=3)
        
        self.lbl_rare_count = tk.Label(total_frame, text="Rare Finds: 0",
                                      font=("Arial", 11), bg=COLORS["bg_panel"],
                                      fg=COLORS["accent_gold"])
        self.lbl_rare_count.pack(pady=3)
        
        tracker_frame = tk.Frame(self.root, bg=COLORS["bg_panel"], 
                                bd=3, relief="ridge", 
                                highlightbackground=COLORS["border"], 
                                highlightthickness=2)
        tracker_frame.pack(fill="both", expand=True, padx=15, pady=10)
        
        tracker_title = tk.Label(tracker_frame, text="LIVE TRACKER", 
                                font=("Verdana", 13, "bold"), 
                                bg=COLORS["bg_panel"], fg=COLORS["text_primary"])
        tracker_title.pack(pady=10)
        
        current_frame = tk.Frame(tracker_frame, bg=COLORS["bg_panel"])
        current_frame.pack(pady=10, padx=10, fill="x")
        
        self.lbl_biome = tk.Label(current_frame, text="Biome: Waiting", 
                                 font=("Arial", 14, "bold"), 
                                 bg=COLORS["bg_display"], fg=COLORS["text_light"], 
                                 width=30, anchor="center", relief="sunken", bd=2)
        self.lbl_biome.pack(pady=5)
        
        self.lbl_last_roll = tk.Label(tracker_frame, text="Last Roll: None", 
                                     font=("Arial", 15, "bold"), 
                                     bg=COLORS["bg_display"], 
                                     fg=COLORS["text_success"], 
                                     width=45, height=2, relief="sunken", 
                                     bd=2, anchor="center")
        self.lbl_last_roll.pack(pady=10, padx=10)
        
        activity_title = tk.Label(tracker_frame, text="ACTIVITY LOG", 
                                 font=("Verdana", 11, "bold"), 
                                 bg=COLORS["bg_panel"], fg=COLORS["text_secondary"])
        activity_title.pack(pady=5)
        
        self.log_box = scrolledtext.ScrolledText(tracker_frame, height=10, 
                                                 bg=COLORS["bg_display"], 
                                                 fg=COLORS["text_success"], 
                                                 font=("Consolas", 9), 
                                                 state="disabled", wrap="word", 
                                                 relief="sunken", bd=2)
        self.log_box.pack(padx=10, pady=10, fill="both", expand=True)
        
        footer = tk.Frame(self.root, bg=COLORS["bg_header"], height=40)
        footer.pack(side="bottom", fill="x")
        footer.pack_propagate(False)
        
        self.connection_label = tk.Label(footer, text="Status: Checking", 
                                        font=("Arial", 10, "bold"), 
                                        bg=COLORS["bg_header"], 
                                        fg=COLORS["text_warning"], anchor="w")
        self.connection_label.pack(side="left", padx=15, pady=5)
        
        webhook_status = "Webhook: ON" if self.webhook_url else "Webhook: OFF"
        self.webhook_status_label = tk.Label(footer, text=webhook_status, 
                                             font=("Arial", 10, "bold"), 
                                             bg=COLORS["bg_header"], 
                                             fg=COLORS["text_success"] if self.webhook_url else COLORS["text_secondary"], 
                                             anchor="center")
        self.webhook_status_label.pack(side="left", padx=15, pady=5)
        
        self.status_bar = tk.Label(footer, text="Ready to launch", 
                                  font=("Arial", 9), bg=COLORS["bg_header"], 
                                  fg=COLORS["text_secondary"], anchor="e")
        self.status_bar.pack(side="right", padx=15, pady=5)
    
    def show_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Launcher Settings")
        settings_window.geometry("550x400")
        settings_window.configure(bg=COLORS["bg_panel"])
        settings_window.transient(self.root)
        
        tk.Label(settings_window, text="LAUNCHER SETTINGS", font=("Impact", 24),
                bg=COLORS["bg_panel"], fg=COLORS["text_primary"]).pack(pady=20)
        
        info_frame = tk.Frame(settings_window, bg=COLORS["bg_panel"])
        info_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(info_frame, text="Game Folder:", font=("Arial", 10, "bold"),
                bg=COLORS["bg_panel"], fg=COLORS["text_light"]).pack(anchor="w")
        tk.Label(info_frame, text=str(self.game_folder), font=("Arial", 9),
                bg=COLORS["bg_panel"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(0, 10))
        
        webhook_status = "Configured" if self.webhook_url else "Not Set"
        tk.Label(info_frame, text=f"Webhook Status: {webhook_status}", 
                font=("Arial", 10, "bold"),
                bg=COLORS["bg_panel"], fg=COLORS["text_light"]).pack(anchor="w")
        
        if self.webhook_url:
            tk.Label(info_frame, text=f"URL: {self.webhook_url[:50]}...", 
                    font=("Arial", 8),
                    bg=COLORS["bg_panel"], fg=COLORS["text_secondary"]).pack(anchor="w", pady=(0, 10))
        
        tk.Label(info_frame, text=f"Notification Threshold: 1/{self.notification_threshold}", 
                font=("Arial", 10, "bold"),
                bg=COLORS["bg_panel"], fg=COLORS["text_light"]).pack(anchor="w")
        
        btn_frame = tk.Frame(settings_window, bg=COLORS["bg_panel"])
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, text="Reconfigure", 
                 command=lambda: [settings_window.destroy(), self.show_setup_wizard()],
                 font=("Arial", 12, "bold"), bg=COLORS["text_warning"],
                 fg="black", width=15, cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="Close", command=settings_window.destroy,
                 font=("Arial", 12, "bold"), bg=COLORS["text_secondary"],
                 fg="white", width=15, cursor="hand2").pack(side="left", padx=5)
    
    def launch_game(self):
        if self.process:
            self.log_msg("WARNING: GAME ALREADY RUNNING")
            return
        
        self.session_rolls = 0
        self.session_start_time = time.time()
        self.rare_finds = []
        
        self.btn_launch.config(state="disabled", text="RUNNING", 
                              bg=COLORS["text_secondary"])
        self.status_bar.config(text="Launching game...", fg=COLORS["text_primary"])
        
        game_path = self.game_folder / "main.py"
        
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
                creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0,
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
            biome = line.split(":", 1)[1]
            self.lbl_biome.config(text=f"Biome: {biome}")
            
            if biome == "Glitch":
                self.lbl_biome.config(fg="#ff00ff")
                self.log_msg("RARE BIOME DETECTED: Glitch")
            elif biome == "Hell":
                self.lbl_biome.config(fg="#ff3333")
                self.log_msg("SPECIAL BIOME: Hell")
            elif biome == "Corruption":
                self.lbl_biome.config(fg="#bb44ff")
                self.log_msg("SPECIAL BIOME: Corruption")
            else:
                self.lbl_biome.config(fg=COLORS["text_light"])
            
        elif line.startswith("ROLL:"):
            parts = line.split(":")
            if len(parts) >= 3:
                name = parts[1]
                rarity = parts[2]
                
                self.total_rolls += 1
                self.session_rolls += 1
                
                self.lbl_total_rolls.config(text=f"Total Rolls: {self.total_rolls}")
                self.lbl_session_rolls.config(text=f"Session Rolls: {self.session_rolls}")
                self.lbl_last_roll.config(text=f"{name} (1/{rarity})")
                
                rarity_val = int(rarity)
                if rarity_val >= 2500:
                    self.lbl_last_roll.config(fg="#ff00ff")
                    self.log_msg(f"CELESTIAL: {name} (1/{rarity})")
                    self.rare_finds.append(name)
                    if self.webhook_url and rarity_val >= self.notification_threshold:
                        threading.Thread(target=self.send_webhook, args=(name, rarity, "CELESTIAL"), daemon=True).start()
                elif rarity_val >= 1000:
                    self.lbl_last_roll.config(fg="#ffdd00")
                    self.log_msg(f"DIVINE DROP: {name} (1/{rarity})")
                    self.rare_finds.append(name)
                    if self.webhook_url and rarity_val >= self.notification_threshold:
                        threading.Thread(target=self.send_webhook, args=(name, rarity, "DIVINE"), daemon=True).start()
                elif rarity_val >= 500:
                    self.lbl_last_roll.config(fg="#ff6600")
                    self.log_msg(f"MYTHIC DROP: {name} (1/{rarity})")
                    self.rare_finds.append(name)
                    if self.webhook_url and rarity_val >= self.notification_threshold:
                        threading.Thread(target=self.send_webhook, args=(name, rarity, "MYTHIC"), daemon=True).start()
                elif rarity_val >= 250:
                    self.lbl_last_roll.config(fg="#ff0066")
                    self.log_msg(f"LEGENDARY: {name} (1/{rarity})")
                    self.rare_finds.append(name)
                    if self.webhook_url and rarity_val >= self.notification_threshold:
                        threading.Thread(target=self.send_webhook, args=(name, rarity, "LEGENDARY"), daemon=True).start()
                elif rarity_val >= 100:
                    self.lbl_last_roll.config(fg="#9933ff")
                    self.log_msg(f"Epic: {name}")
                else:
                    self.lbl_last_roll.config(fg=COLORS["text_success"])
                
                self.lbl_rare_count.config(text=f"Rare Finds: {len(self.rare_finds)}")
    
    def send_webhook(self, name, rarity, tier):
        if not self.is_online:
            self.log_msg("Webhook skipped: offline")
            return
        
        rarity_val = int(rarity)
        rarity_display = f"1:{rarity_val:,}"
        
        if tier == "CELESTIAL":
            embed_color = 0xFF00FF
        elif tier == "DIVINE":
            embed_color = 0xFFD700
        elif tier == "MYTHIC":
            embed_color = 0xFF6600
        else:
            embed_color = 0xFF0066
        
        current_biome = self.lbl_biome.cget("text").replace("Biome: ", "")
        
        description_lines = [
            f"════════════════════════",
            f"    **{name.upper()}**",
            f"════════════════════════",
            "",
            f"An incredibly rare {tier} tier aura has manifested!",
            "",
            f"━━━━━━━━━━━━━━━━━━━━━━"
        ]
        
        embed = {
            "embeds": [{
                "title": f"⚡ {tier} AURA OBTAINED ⚡",
                "description": "\n".join(description_lines),
                "color": embed_color,
                "fields": [
                    {
                        "name": "💎 Aura Name",
                        "value": f"```fix\n{name}\n```",
                        "inline": True
                    },
                    {
                        "name": "🎲 Rarity Odds",
                        "value": f"```yaml\n{rarity_display}\n```",
                        "inline": True
                    },
                    {
                        "name": "🌍 Biome",
                        "value": f"```css\n{current_biome}\n```",
                        "inline": True
                    },
                    {
                        "name": "📊 Total Rolls",
                        "value": f"```apache\n{self.total_rolls:,}\n```",
                        "inline": True
                    },
                    {
                        "name": "⏱️ Timestamp",
                        "value": f"```{time.strftime('%Y-%m-%d %H:%M:%S')}```",
                        "inline": True
                    },
                    {
                        "name": "🎯 Tier",
                        "value": f"```diff\n+ {tier} TIER\n```",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": f"Pytho-RNG Launcher • Powered by Divine RNG"
                },
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }],
            "username": "Pytho-RNG Bot"
        }
        
        try:
            response = requests.post(self.webhook_url, json=embed, timeout=5)
            if response.status_code == 204:
                self.log_msg(f"Webhook sent: {name}")
            else:
                self.log_msg(f"Webhook failed: {response.status_code}")
        except Exception as e:
            self.log_msg(f"Webhook error: {str(e)}")
    
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
    
    def update_session_time(self):
        if self.session_start_time:
            elapsed = int(time.time() - self.session_start_time)
            hours = elapsed // 3600
            minutes = (elapsed % 3600) // 60
            seconds = elapsed % 60
            
            self.lbl_session_time.config(text=f"Duration: {hours:02d}:{minutes:02d}:{seconds:02d}")
            
            if elapsed > 0:
                rolls_per_min = (self.session_rolls / elapsed) * 60
                self.lbl_rolls_per_min.config(text=f"Rate: {rolls_per_min:.1f}/min")
        
        self.root.after(1000, self.update_session_time)
    
    def load_total_rolls(self):
        try:
            if self.data_file.exists():
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.total_rolls = data.get("total_rolls", 0)
                    print(f"Loaded {self.total_rolls} total rolls")
        except Exception as e:
            print(f"Error loading rolls (trying backup): {e}")
            try:
                if self.backup_file.exists():
                    with open(self.backup_file, 'r') as f:
                        data = json.load(f)
                        self.total_rolls = data.get("total_rolls", 0)
                        print(f"Loaded from backup: {self.total_rolls} total rolls")
            except Exception as e2:
                print(f"Error loading backup: {e2}")
                self.total_rolls = 0
    
    def on_game_closed(self):
        self.process = None
        self.btn_launch.config(state="normal", text="LAUNCH GAME", bg="#00d4ff")
        self.status_bar.config(text="Game closed", fg=COLORS["text_warning"])
        
        if self.session_start_time:
            elapsed = int(time.time() - self.session_start_time)
            self.log_msg(f"Session ended. Duration: {elapsed//60}m | Rolls: {self.session_rolls} | Rare: {len(self.rare_finds)}")
            self.session_start_time = None

if __name__ == "__main__":
    root = tk.Tk()
    app = Launcher(root)
    root.mainloop()