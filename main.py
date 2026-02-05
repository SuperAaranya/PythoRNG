import tkinter as tk
from tkinter import Canvas
import random
import requests
import threading
import sys
import time
import json
import os
import socket
from config import Config

Config.ensure_directories()

WEBHOOK_URL = Config.WEBHOOK_URL
DATA_FILE = Config.DATA_FILE
BACKUP_FILE = Config.BACKUP_FILE

COLOR_SCHEME = {
    "bg_dark": "#0a0a0f",
    "bg_header": "#1a1a2e",
    "bg_panel": "#16213e",
    "bg_display": "#0f0f15",
    "border": "#16213e",
    "text_primary": "#00ffcc",
    "text_secondary": "#888888",
    "text_light": "#ffffff"
}

BIOME_COLORS = {
    "Normal": {"bg": "#0a0a0f", "text": "#ffffff", "accent": "#00ffcc"},
    "Glitch": {"bg": "#0f000f", "text": "#ff00ff", "accent": "#ff00ff"},
    "Hell": {"bg": "#1a0000", "text": "#ff4444", "accent": "#ff3333"},
    "Corruption": {"bg": "#0f0520", "text": "#bb44ff", "accent": "#bb44ff"}
}

BIOME_DIVISORS = {
    "Normal": 10,      
    "Glitch": 1,    
    "Hell": 1,        
    "Corruption": 1   
}

class PythoRNG:
    def __init__(self, root):
        self.root = root
        self.root.title("Pytho-RNG: Game Client")
        self.root.geometry("700x650")
        self.root.configure(bg=COLOR_SCHEME["bg_dark"])
        
        self.auto_rolling = False
        self.current_biome = "Normal"
        self.roll_count = 0
        self.animation_running = False
        self.is_online = True
        
        self.auras = []
        self.setup_auras()
        self.load_data()
        self.setup_ui()
        self.biome_tick()
        self.check_connectivity_loop()

    def setup_auras(self):
        self.add_aura("Common", 2, None)
        self.add_aura("Uncommon", 4, None)
        self.add_aura("Rare", 8, None)
        self.add_aura("Epic", 100, None)
        self.add_aura("Legendary", 250, None)
        self.add_aura("Mythic", 500, None)
        self.add_aura("Divine", 1000, None)
        
        self.add_aura("Celestial", 2500, "Glitch")
        self.add_aura("Infernal", 1500, "Hell")
        self.add_aura("Corrupted", 1200, "Corruption")

    def add_aura(self, name, rarity, bio):
        self.auras.append({"name": name, "rarity": rarity, "bio": bio})

    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.roll_count = data.get("total_rolls", 0)
                    print(f"Data loaded: {self.roll_count} total rolls")
        except Exception as e:
            print(f"Error loading data (trying backup): {e}")
            self.load_backup_data()

    def load_backup_data(self):
        try:
            if os.path.exists(BACKUP_FILE):
                with open(BACKUP_FILE, 'r') as f:
                    data = json.load(f)
                    self.roll_count = data.get("total_rolls", 0)
                    print(f"Backup data restored: {self.roll_count} total rolls")
        except Exception as e:
            print(f"Error loading backup data: {e}")
            self.roll_count = 0

    def save_data(self):
        try:
            data = {
                "total_rolls": self.roll_count,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": 2
            }
            
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, 'r') as f:
                        old_data = json.load(f)
                    with open(BACKUP_FILE, 'w') as f:
                        json.dump(old_data, f, indent=2)
                except:
                    pass
            
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Data saved: {self.roll_count} rolls")
        except Exception as e:
            print(f"Critical error saving data: {e}")

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg=COLOR_SCHEME["bg_header"], height=90)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_frame = tk.Frame(header_frame, bg=COLOR_SCHEME["bg_header"])
        title_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.lbl_title = tk.Label(title_frame, text="PYTHO-RNG", font=("Impact", 40), bg=COLOR_SCHEME["bg_header"], fg=COLOR_SCHEME["text_primary"])
        self.lbl_title.pack(side="left")
        
        stats_label = tk.Label(title_frame, text=f"Rolls: {self.roll_count}", font=("Arial", 12), bg=COLOR_SCHEME["bg_header"], fg=COLOR_SCHEME["text_secondary"])
        stats_label.pack(side="right", padx=10)
        self.lbl_stats_header = stats_label

        self.lbl_biome = tk.Label(self.root, text="Biome: Normal", font=("Verdana", 18, "bold"), bg=COLOR_SCHEME["bg_dark"], fg=COLOR_SCHEME["text_light"], anchor="center")
        self.lbl_biome.pack(pady=15)

        self.canvas = Canvas(self.root, width=650, height=140, bg=COLOR_SCHEME["bg_display"], highlightthickness=2, highlightbackground=COLOR_SCHEME["border"])
        self.canvas.pack(pady=10, padx=10)
        
        self.lbl_res = tk.Label(self.root, text="Press ROLL to begin", font=("Arial", 20, "bold"), bg=COLOR_SCHEME["bg_panel"], fg=COLOR_SCHEME["text_secondary"], width=40, height=3, relief="ridge", bd=3, anchor="center")
        self.lbl_res.pack(pady=15)

        self.lbl_count = tk.Label(self.root, text="Rolls: 0", font=("Arial", 14, "bold"), bg=COLOR_SCHEME["bg_dark"], fg=COLOR_SCHEME["text_primary"], anchor="center")
        self.lbl_count.pack(pady=8)
        
        self.connection_label = tk.Label(self.root, text="Status: CHECKING...", font=("Arial", 10, "bold"), bg=COLOR_SCHEME["bg_dark"], fg="#ffaa00", anchor="center")
        self.connection_label.pack(pady=5)

        btn_frame = tk.Frame(self.root, bg=COLOR_SCHEME["bg_dark"])
        btn_frame.pack(pady=12)

        self.btn_roll = tk.Button(btn_frame, text="ROLL", command=self.manual_roll, font=("Arial", 16, "bold"), bg="#0066ff", fg="white", activebackground="#0044aa", width=14, height=2, cursor="hand2", relief="raised", bd=3)
        self.btn_roll.grid(row=0, column=0, padx=8)

        self.btn_auto = tk.Button(btn_frame, text="AUTO: OFF", command=self.toggle_auto, font=("Arial", 14, "bold"), bg="#ff3333", fg="white", width=14, height=2, cursor="hand2", relief="raised", bd=3)
        self.btn_auto.grid(row=0, column=1, padx=8)

    def biome_tick(self):
        rng = random.randint(1, 1000)
        
        if rng == 1: 
            self.current_biome = "Glitch"
        elif rng <= 10: 
            self.current_biome = "Hell"
        elif rng <= 30: 
            self.current_biome = "Corruption"
        else: 
            self.current_biome = "Normal"

        colors = BIOME_COLORS[self.current_biome]
        self.root.configure(bg=colors["bg"])
        self.lbl_biome.config(text=f"Biome: {self.current_biome}", fg=colors["text"])

        self.lbl_biome.config(text=f"Biome: {self.current_biome}")
        print(f"BIOME_UPDATE:{self.current_biome}")
        sys.stdout.flush()
        
        if self.current_biome == "Glitch":
            duration = random.randint(90000, 150000)
        elif self.current_biome == "Hell":
            duration = random.randint(120000, 240000)
        elif self.current_biome == "Corruption":
            duration = random.randint(150000, 240000)
        else:
            duration = random.randint(180000, 300000)
        
        self.root.after(duration, self.biome_tick)

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
            print("OFFLINE_DETECTED:Webhooks disabled")
            self.connection_label.config(text="Status: OFFLINE", fg="#ff0000")
            sys.stdout.flush()
        elif not was_online and self.is_online:
            print("ONLINE_DETECTED:Webhooks enabled")
            self.connection_label.config(text="Status: ONLINE", fg="#00ff00")
            sys.stdout.flush()
        
        self.root.after(5000, self.check_connectivity_loop)

    def manual_roll(self):
        if not self.animation_running:
            self.roll()

    def toggle_auto(self):
        self.auto_rolling = not self.auto_rolling
        color = "#00cc44" if self.auto_rolling else "#ff3333"
        state = "ON" if self.auto_rolling else "OFF"
        self.btn_auto.config(text=f"AUTO: {state}", bg=color)
        if self.auto_rolling:
            self.auto_loop()

    def auto_loop(self):
        if self.auto_rolling:
            if not self.animation_running:
                self.roll()
            self.root.after(150, self.auto_loop)

    def roll(self):
        self.roll_count += 1
        self.lbl_count.config(text=f"Rolls: {self.roll_count}")
        self.save_data()
        
        applicable = []
        for aura in self.auras:
            if aura["bio"] is None:
                applicable.append(aura)
            elif aura["bio"] == self.current_biome:
                applicable.append(aura)
            else:
                applicable.append({**aura, "rarity": aura["rarity"] * 100})
        
        applicable.sort(key=lambda x: x["rarity"], reverse=True)
        
        found = applicable[-1]
        
        for a in applicable:
            if random.randint(1, a["rarity"]) == 1:
                found = a
                break
        
        self.animate_roll(found)
        print(f"ROLL:{found['name']}:{found['rarity']}")
        sys.stdout.flush()

        if found["rarity"] >= 500:
            threading.Thread(target=self.send_webhook, args=(found,), daemon=True).start()

    def animate_roll(self, final_aura):
        self.animation_running = True
        self.canvas.delete("all")
        
        rarity = final_aura["rarity"]
        if rarity >= 2500:
            color = "#ff00ff"
        elif rarity >= 1000:
            color = "#ffdd00"
        elif rarity >= 500:
            color = "#ff6600"
        elif rarity >= 250:
            color = "#ff0066"
        elif rarity >= 100:
            color = "#9933ff"
        elif rarity >= 50:
            color = "#0099ff"
        else:
            color = "#aaaaaa"
        
        self.lbl_res.config(text=f"{final_aura['name']} (1/{final_aura['rarity']})", fg=color, bg=COLOR_SCHEME["bg_panel"])
        self.lbl_res.place(relx=0.5, y=-100, anchor="center")
        
        def slide_down(current_y=-100, target_y=210):
            if current_y < target_y:
                self.lbl_res.place(relx=0.5, y=current_y, anchor="center")
                self.root.after(10, lambda: slide_down(current_y + 8, target_y))
            else:
                self.lbl_res.place(relx=0.5, y=210, anchor="center")
                self.draw_particles(final_aura)
                self.animation_running = False
        
        slide_down()

    def draw_particles(self, aura):
        rarity = aura["rarity"]
        particle_count = min(60, rarity // 15)
        
        for _ in range(particle_count):
            x = random.randint(50, 600)
            y = random.randint(10, 130)
            size = random.randint(2, 8)
            
            if rarity >= 1000:
                color = random.choice(["#ffdd00", "#ff00ff", "#00ffff", "#ffff00"])
            elif rarity >= 500:
                color = random.choice(["#ff6600", "#ffdd00", "#ff8800"])
            elif rarity >= 250:
                color = random.choice(["#ff0066", "#ff33cc", "#ff6699"])
            elif rarity >= 100:
                color = random.choice(["#9933ff", "#aa44ff", "#bb55ff"])
            else:
                color = random.choice(["#aaaaaa", "#bbbbbb", "#cccccc"])
            
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")

    def send_webhook(self, aura):
        if not self.is_online:
            print(f"WEBHOOK_SKIPPED:Offline")
            sys.stdout.flush()
            return
        
        embed = {
            "embeds": [{
                "title": "LEGENDARY DROP",
                "description": f"{aura['name']} has been obtained!",
                "color": 0x00ffcc,
                "fields": [
                    {"name": "Rarity", "value": f"1/{aura['rarity']}", "inline": True},
                    {"name": "Biome", "value": self.current_biome, "inline": True},
                    {"name": "Total Rolls", "value": str(self.roll_count), "inline": True}
                ],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }]
        }
        
        try:
            response = requests.post(WEBHOOK_URL, json=embed, timeout=5)
            if response.status_code == 204:
                print(f"WEBHOOK_SUCCESS:{aura['name']}")
            else:
                print(f"WEBHOOK_FAILED:{response.status_code}")
            sys.stdout.flush()
        except Exception as e:
            print(f"WEBHOOK_ERROR:{str(e)}")
            sys.stdout.flush()

if __name__ == "__main__":
    root = tk.Tk()
    app = PythoRNG(root)
    root.mainloop()

class PythoRNG:
    def __init__(self, root):
        self.root = root
        self.root.title("Pytho-RNG: Game Client")
        self.root.geometry("600x500")
        self.root.configure(bg="#0a0a0f")
        
        self.auto_rolling = False
        self.current_biome = "Normal"
        self.roll_count = 0
        self.animation_running = False
        self.is_online = True
        
        self.auras = []
        self.setup_auras()
        self.load_data()
        self.setup_ui()
        self.biome_tick()
        self.check_connectivity_loop()

    def setup_auras(self):
        self.add_aura("Common", 2, None)
        self.add_aura("Uncommon", 4, None)
        self.add_aura("Rare", 8, None)
        self.add_aura("Epic", 100, None)
        self.add_aura("Legendary", 250, None)
        self.add_aura("Mythic", 500, None)
        self.add_aura("Divine", 1000, None)
        
        self.add_aura("Celestial", 2500, "Glitch")
        self.add_aura("Infernal", 1500, "Hell")
        self.add_aura("Corrupted", 1200, "Corruption")

    def add_aura(self, name, rarity, bio):
        self.auras.append({"name": name, "rarity": rarity, "bio": bio})

    def load_data(self):
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.roll_count = data.get("total_rolls", 0)
                    print(f"Data loaded: {self.roll_count} total rolls")
        except Exception as e:
            print(f"Error loading data (trying backup): {e}")
            self.load_backup_data()

    def load_backup_data(self):
        try:
            if os.path.exists(BACKUP_FILE):
                with open(BACKUP_FILE, 'r') as f:
                    data = json.load(f)
                    self.roll_count = data.get("total_rolls", 0)
                    print(f"Backup data restored: {self.roll_count} total rolls")
        except Exception as e:
            print(f"Error loading backup data: {e}")
            self.roll_count = 0

    def save_data(self):
        try:
            data = {
                "total_rolls": self.roll_count,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": 2
            }
            
            if os.path.exists(DATA_FILE):
                try:
                    with open(DATA_FILE, 'r') as f:
                        old_data = json.load(f)
                    with open(BACKUP_FILE, 'w') as f:
                        json.dump(old_data, f, indent=2)
                except:
                    pass
            
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"Data saved: {self.roll_count} rolls")
        except Exception as e:
            print(f"Critical error saving data: {e}")

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg="#1a1a2e", height=80)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        self.lbl_title = tk.Label(header_frame, text="PYTHO-RNG", font=("Impact", 32), bg="#1a1a2e", fg="#00ffcc")
        self.lbl_title.pack(pady=20)

        self.lbl_biome = tk.Label(self.root, text="Biome: Normal", font=("Verdana", 16, "bold"), bg="#0a0a0f", fg="#ffffff", anchor="center")
        self.lbl_biome.pack(pady=15)

        self.canvas = Canvas(self.root, width=500, height=120, bg="#0a0a0f", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        self.lbl_res = tk.Label(self.root, text="Press ROLL to begin", font=("Arial", 18, "bold"), bg="#1e1e2e", fg="#aaaaaa", width=35, height=3, relief="ridge", bd=3, anchor="center")
        self.lbl_res.pack(pady=20)

        self.lbl_count = tk.Label(self.root, text="Rolls: 0", font=("Arial", 12), bg="#0a0a0f", fg="#888888", anchor="center")
        self.lbl_count.pack(pady=5)
        
        self.connection_label = tk.Label(self.root, text="Status: ONLINE", font=("Arial", 9), bg="#0a0a0f", fg="#00ff99", anchor="center")
        self.connection_label.pack(pady=5)

        btn_frame = tk.Frame(self.root, bg="#0a0a0f")
        btn_frame.pack(pady=10)

        self.btn_roll = tk.Button(btn_frame, text="ROLL", command=self.manual_roll, font=("Arial", 16, "bold"), bg="#0066ff", fg="white", activebackground="#0044aa", width=12, height=2, cursor="hand2")
        self.btn_roll.grid(row=0, column=0, padx=10)

        self.btn_auto = tk.Button(btn_frame, text="AUTO: OFF", command=self.toggle_auto, font=("Arial", 14, "bold"), bg="#ff3333", fg="white", width=12, height=2, cursor="hand2")
        self.btn_auto.grid(row=0, column=1, padx=10)

    def biome_tick(self):
        rng = random.randint(1, 1000)
        
        if rng == 1: 
            self.current_biome = "Glitch" 
            self.root.configure(bg="#0f000f")
            self.lbl_biome.config(fg="#ff00ff")
        elif rng <= 10: 
            self.current_biome = "Hell" 
            self.root.configure(bg="#1a0000")
            self.lbl_biome.config(fg="#ff4444")
        elif rng <= 30: 
            self.current_biome = "Corruption" 
            self.root.configure(bg="#0f0520")
            self.lbl_biome.config(fg="#bb44ff")
        else: 
            self.current_biome = "Normal"
            self.root.configure(bg="#0a0a0f")
            self.lbl_biome.config(fg="#ffffff")

        self.lbl_biome.config(text=f"Biome: {self.current_biome}")
        print(f"BIOME_UPDATE:{self.current_biome}")
        sys.stdout.flush()
        
        if self.current_biome == "Glitch":
            duration = random.randint(90000, 150000)
        elif self.current_biome == "Hell":
            duration = random.randint(120000, 240000)
        elif self.current_biome == "Corruption":
            duration = random.randint(150000, 240000)
        else:
            duration = random.randint(180000, 300000)
        
        self.root.after(duration, self.biome_tick)

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
            print("OFFLINE_DETECTED:Webhooks disabled")
            self.connection_label.config(text="Status: OFFLINE - Webhooks Disabled", fg="#ff3333")
            sys.stdout.flush()
        elif not was_online and self.is_online:
            print("ONLINE_DETECTED:Webhooks enabled")
            self.connection_label.config(text="Status: ONLINE - Webhooks Enabled", fg="#00ff99")
            sys.stdout.flush()
        
        self.root.after(5000, self.check_connectivity_loop)

    def manual_roll(self):
        if not self.animation_running:
            self.roll()

    def toggle_auto(self):
        self.auto_rolling = not self.auto_rolling
        color = "#00cc44" if self.auto_rolling else "#ff3333"
        state = "ON" if self.auto_rolling else "OFF"
        self.btn_auto.config(text=f"AUTO: {state}", bg=color)
        if self.auto_rolling:
            self.auto_loop()

    def auto_loop(self):
        if self.auto_rolling:
            if not self.animation_running:
                self.roll()
            self.root.after(150, self.auto_loop)

    def roll(self):
        self.roll_count += 1
        self.lbl_count.config(text=f"Rolls: {self.roll_count}")
        self.save_data()
        
        applicable = []
        for aura in self.auras:
            if aura["bio"] is None:
                applicable.append(aura)
            elif aura["bio"] == self.current_biome:
                applicable.append(aura)
            else:
                applicable.append({**aura, "rarity": aura["rarity"] * 100})
        
        applicable.sort(key=lambda x: x["rarity"], reverse=True)
        
        found = applicable[-1]
        
        for a in applicable:
            if random.randint(1, a["rarity"]) == 1:
                found = a
                break
        
        self.animate_roll(found)
        print(f"ROLL:{found['name']}:{found['rarity']}")
        sys.stdout.flush()

        if found["rarity"] >= 500:
            threading.Thread(target=self.send_webhook, args=(found,), daemon=True).start()

    def animate_roll(self, final_aura):
        self.animation_running = True
        self.canvas.delete("all")
        
        rarity = final_aura["rarity"]
        if rarity >= 2500:
            color = "#ff00ff"
        elif rarity >= 1000:
            color = "#ffdd00"
        elif rarity >= 500:
            color = "#ff6600"
        elif rarity >= 250:
            color = "#ff0066"
        elif rarity >= 100:
            color = "#9933ff"
        elif rarity >= 50:
            color = "#0099ff"
        else:
            color = "#aaaaaa"
        
        self.lbl_res.config(text=f"{final_aura['name']} (1/{final_aura['rarity']})", fg=color, bg="#1e1e2e")
        self.lbl_res.place(relx=0.5, y=-100, anchor="center")
        
        def slide_down(current_y=-100, target_y=210):
            if current_y < target_y:
                self.lbl_res.place(relx=0.5, y=current_y, anchor="center")
                self.root.after(10, lambda: slide_down(current_y + 8, target_y))
            else:
                self.lbl_res.place(relx=0.5, y=210, anchor="center")
                self.draw_particles(final_aura)
                self.animation_running = False
        
        slide_down()

    def draw_particles(self, aura):
        rarity = aura["rarity"]
        particle_count = min(50, rarity // 20)
        
        for _ in range(particle_count):
            x = random.randint(50, 450)
            y = random.randint(10, 110)
            size = random.randint(2, 6)
            
            if rarity >= 1000:
                color = random.choice(["#ffdd00", "#ff00ff", "#00ffff"])
            elif rarity >= 500:
                color = random.choice(["#ff6600", "#ffdd00"])
            elif rarity >= 100:
                color = random.choice(["#9933ff", "#ff0066"])
            else:
                color = "#aaaaaa"
            
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")

    def send_webhook(self, aura):
        if not self.is_online:
            print(f"WEBHOOK_SKIPPED:Offline")
            sys.stdout.flush()
            return
        
        embed = {
            "embeds": [{
                "title": "LEGENDARY DROP",
                "description": f"**{aura['name']}** has been obtained!",
                "color": 0x00ffcc,
                "fields": [
                    {"name": "Rarity", "value": f"1/{aura['rarity']}", "inline": True},
                    {"name": "Biome", "value": self.current_biome, "inline": True},
                    {"name": "Total Rolls", "value": str(self.roll_count), "inline": True}
                ],
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            }]
        }
        
        try:
            response = requests.post(WEBHOOK_URL, json=embed, timeout=5)
            if response.status_code == 204:
                print(f"WEBHOOK_SUCCESS:{aura['name']}")
            else:
                print(f"WEBHOOK_FAILED:{response.status_code}")
            sys.stdout.flush()
        except Exception as e:
            print(f"WEBHOOK_ERROR:{str(e)}")
            sys.stdout.flush()

if __name__ == "__main__":
    root = tk.Tk()
    app = PythoRNG(root)
    root.mainloop()