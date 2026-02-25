import tkinter as tk
from tkinter import Canvas, messagebox
import random
import sys
import time
import json
from pathlib import Path
from json import JSONDecodeError

DEFAULT_SETTINGS = {
    "auto_roll_speed": 150,
    "animation_speed": 10,
    "particle_count_multiplier": 1.0,
    "biome_change_min": 180000,
    "biome_change_max": 300000,
    "notification_threshold": 500,
    "window_width": 750,
    "window_height": 700,
    "show_particle_effects": True,
    "canvas_width": 680,
    "canvas_height": 150,
    "glitch_biome_duration_min": 90000,
    "glitch_biome_duration_max": 150000,
    "hell_biome_duration_min": 120000,
    "hell_biome_duration_max": 240000,
    "corruption_biome_duration_min": 150000,
    "corruption_biome_duration_max": 240000
}

class ConfigManager:
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.config_file = self.base_dir / "game_config.json"
        self.data_file = self.base_dir / "pythorng_data.json"
        self.backup_file = self.base_dir / "pythorng_backup.json"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        
        self.settings = self.load_settings()
    
    def load_settings(self):
        default_settings = DEFAULT_SETTINGS.copy()
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    loaded = json.load(f)
                    default_settings.update(loaded)
            except (OSError, JSONDecodeError):
                pass
        
        return self.sanitize_settings(default_settings)
    
    def save_settings(self, settings):
        try:
            settings = self.sanitize_settings(settings)
            with open(self.config_file, 'w') as f:
                json.dump(settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def sanitize_settings(self, settings):
        cleaned = DEFAULT_SETTINGS.copy()
        cleaned.update(settings)

        int_keys = [
            "auto_roll_speed", "animation_speed", "biome_change_min", "biome_change_max",
            "notification_threshold", "window_width", "window_height", "canvas_width",
            "canvas_height", "glitch_biome_duration_min", "glitch_biome_duration_max",
            "hell_biome_duration_min", "hell_biome_duration_max",
            "corruption_biome_duration_min", "corruption_biome_duration_max",
        ]
        for key in int_keys:
            try:
                cleaned[key] = int(cleaned[key])
            except (TypeError, ValueError):
                cleaned[key] = int(DEFAULT_SETTINGS[key])

        try:
            cleaned["particle_count_multiplier"] = float(cleaned["particle_count_multiplier"])
        except (TypeError, ValueError):
            cleaned["particle_count_multiplier"] = DEFAULT_SETTINGS["particle_count_multiplier"]

        cleaned["show_particle_effects"] = bool(cleaned["show_particle_effects"])

        cleaned["auto_roll_speed"] = max(1, cleaned["auto_roll_speed"])
        cleaned["animation_speed"] = max(1, cleaned["animation_speed"])
        cleaned["notification_threshold"] = max(1, cleaned["notification_threshold"])
        cleaned["window_width"] = max(500, cleaned["window_width"])
        cleaned["window_height"] = max(500, cleaned["window_height"])
        cleaned["canvas_width"] = max(140, cleaned["canvas_width"])
        cleaned["canvas_height"] = max(40, cleaned["canvas_height"])
        cleaned["particle_count_multiplier"] = max(0.0, cleaned["particle_count_multiplier"])

        duration_pairs = [
            ("biome_change_min", "biome_change_max"),
            ("glitch_biome_duration_min", "glitch_biome_duration_max"),
            ("hell_biome_duration_min", "hell_biome_duration_max"),
            ("corruption_biome_duration_min", "corruption_biome_duration_max"),
        ]
        for min_key, max_key in duration_pairs:
            cleaned[min_key] = max(1000, cleaned[min_key])
            cleaned[max_key] = max(1000, cleaned[max_key])
            if cleaned[min_key] > cleaned[max_key]:
                cleaned[min_key], cleaned[max_key] = cleaned[max_key], cleaned[min_key]

        return cleaned

config_manager = ConfigManager()
DATA_FILE = config_manager.data_file
BACKUP_FILE = config_manager.backup_file

COLOR_SCHEME = {
    "bg_dark": "#0a0a0f",
    "bg_header": "#1a1a2e",
    "bg_panel": "#16213e",
    "bg_display": "#0f0f15",
    "border": "#16213e",
    "text_primary": "#00ffcc",
    "text_secondary": "#888888",
    "text_light": "#ffffff",
    "text_success": "#00ff99",
    "text_warning": "#ffaa00",
    "text_error": "#ff3333",
    "accent_gold": "#ffdd00",
    "accent_purple": "#bb44ff",
    "accent_red": "#ff3333"
}

BIOME_COLORS = {
    "Normal": {"bg": "#0a0a0f", "text": "#ffffff", "accent": "#00ffcc"},
    "Glitch": {"bg": "#0f000f", "text": "#ff00ff", "accent": "#ff00ff"},
    "Hell": {"bg": "#1a0000", "text": "#ff4444", "accent": "#ff3333"},
    "Corruption": {"bg": "#0f0520", "text": "#bb44ff", "accent": "#bb44ff"}
}

class AuraDatabase:
    def __init__(self):
        self.auras = []
        self.setup_auras()
    
    def setup_auras(self):
        self.add_aura("Common", 2, None)
        self.add_aura("Uncommon", 4, None)
        self.add_aura("Rare", 8, None)
        self.add_aura("Super Rare", 25, None)
        self.add_aura("Epic", 100, None)
        self.add_aura("Legendary", 250, None)
        self.add_aura("Mythic", 500, None)
        self.add_aura("Divine", 1000, None)
        self.add_aura("Ascended", 1750, None)
        
        self.add_aura("Celestial", 2500, "Glitch")
        self.add_aura("Void Walker", 3000, "Glitch")
        
        self.add_aura("Infernal", 1500, "Hell")
        self.add_aura("Demon Lord", 2000, "Hell")
        
        self.add_aura("Corrupted", 1200, "Corruption")
        self.add_aura("Eldritch", 1800, "Corruption")
    
    def add_aura(self, name, rarity, biome):
        self.auras.append({"name": name, "rarity": rarity, "bio": biome})
    
    def get_applicable_auras(self, current_biome):
        applicable = []
        for aura in self.auras:
            if aura["bio"] is None:
                applicable.append(aura.copy())
            elif aura["bio"] == current_biome:
                applicable.append(aura.copy())
            else:
                modified_aura = aura.copy()
                modified_aura["rarity"] = aura["rarity"] * 100
                applicable.append(modified_aura)
        return applicable

class PythoRNG:
    def __init__(self, root):
        self.root = root
        self.settings = config_manager.settings
        
        self.root.title("Pytho-RNG: Game Client v2.0")
        self.root.geometry(f"{self.settings['window_width']}x{self.settings['window_height']}")
        self.root.configure(bg=COLOR_SCHEME["bg_dark"])
        
        self.auto_rolling = False
        self.current_biome = "Normal"
        self.total_rolls = 0
        self.session_rolls = 0
        self.animation_running = False
        
        self.aura_db = AuraDatabase()
        self.load_data()
        self.setup_ui()
        self.biome_tick()

    def load_data(self):
        try:
            if DATA_FILE.exists():
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.total_rolls = int(data.get("total_rolls", 0))
                    print(f"Data loaded: {self.total_rolls} total rolls")
        except Exception as e:
            print(f"Error loading data (trying backup): {e}")
            self.load_backup_data()

    def load_backup_data(self):
        try:
            if BACKUP_FILE.exists():
                with open(BACKUP_FILE, 'r') as f:
                    data = json.load(f)
                    self.total_rolls = int(data.get("total_rolls", 0))
                    print(f"Backup data restored: {self.total_rolls} total rolls")
        except Exception as e:
            print(f"Error loading backup data: {e}")
            self.total_rolls = 0

    def save_data(self):
        try:
            data = {
                "total_rolls": self.total_rolls,
                "last_updated": time.strftime("%Y-%m-%d %H:%M:%S"),
                "version": 2
            }
            
            if DATA_FILE.exists():
                try:
                    with open(DATA_FILE, 'r') as f:
                        old_data = json.load(f)
                    with open(BACKUP_FILE, 'w') as f:
                        json.dump(old_data, f, indent=2)
                except (OSError, json.JSONDecodeError):
                    pass
            
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            
        except Exception as e:
            print(f"Critical error saving data: {e}")

    def setup_ui(self):
        header_frame = tk.Frame(self.root, bg=COLOR_SCHEME["bg_header"], height=100)
        header_frame.pack(fill="x")
        header_frame.pack_propagate(False)
        
        title_container = tk.Frame(header_frame, bg=COLOR_SCHEME["bg_header"])
        title_container.pack(fill="both", expand=True, padx=15, pady=15)
        
        self.lbl_title = tk.Label(title_container, 
                                  text="PYTHO-RNG", 
                                  font=("Impact", 44), 
                                  bg=COLOR_SCHEME["bg_header"], 
                                  fg=COLOR_SCHEME["text_primary"])
        self.lbl_title.pack(side="left")
        
        stats_container = tk.Frame(title_container, bg=COLOR_SCHEME["bg_header"])
        stats_container.pack(side="right")
        
        self.lbl_stats_header = tk.Label(stats_container, 
                                         text=f"Total Rolls: {self.total_rolls}", 
                                         font=("Arial", 13, "bold"), 
                                         bg=COLOR_SCHEME["bg_header"], 
                                         fg=COLOR_SCHEME["text_secondary"])
        self.lbl_stats_header.pack(anchor="e")

        self.lbl_biome = tk.Label(self.root, 
                                 text="Biome: Normal", 
                                 font=("Verdana", 19, "bold"), 
                                 bg=COLOR_SCHEME["bg_dark"], 
                                 fg=COLOR_SCHEME["text_light"], 
                                 anchor="center")
        self.lbl_biome.pack(pady=18)

        self.canvas = Canvas(self.root, 
                            width=self.settings["canvas_width"], 
                            height=self.settings["canvas_height"], 
                            bg=COLOR_SCHEME["bg_display"], 
                            highlightthickness=3, 
                            highlightbackground=COLOR_SCHEME["border"])
        self.canvas.pack(pady=12, padx=15)
        
        self.lbl_res = tk.Label(self.root, 
                               text="Press ROLL to begin", 
                               font=("Arial", 22, "bold"), 
                               bg=COLOR_SCHEME["bg_panel"], 
                               fg=COLOR_SCHEME["text_secondary"], 
                               width=38, 
                               height=3, 
                               relief="ridge", 
                               bd=4, 
                               anchor="center")
        self.lbl_res.pack(pady=18)

        info_frame = tk.Frame(self.root, bg=COLOR_SCHEME["bg_dark"])
        info_frame.pack(pady=10)
        
        self.lbl_count = tk.Label(info_frame, 
                                 text="Session Rolls: 0", 
                                 font=("Arial", 14, "bold"), 
                                 bg=COLOR_SCHEME["bg_dark"], 
                                 fg=COLOR_SCHEME["text_primary"], 
                                 anchor="center")
        self.lbl_count.pack(side="left", padx=15)

        btn_frame = tk.Frame(self.root, bg=COLOR_SCHEME["bg_dark"])
        btn_frame.pack(pady=15)

        self.btn_roll = tk.Button(btn_frame, 
                                  text="ROLL", 
                                  command=self.manual_roll, 
                                  font=("Arial", 17, "bold"), 
                                  bg="#0066ff", 
                                  fg="white", 
                                  activebackground="#0044aa", 
                                  width=16, 
                                  height=2, 
                                  cursor="hand2", 
                                  relief="raised", 
                                  bd=4)
        self.btn_roll.grid(row=0, column=0, padx=10)

        self.btn_auto = tk.Button(btn_frame, 
                                  text="AUTO: OFF", 
                                  command=self.toggle_auto, 
                                  font=("Arial", 15, "bold"), 
                                  bg=COLOR_SCHEME["accent_red"], 
                                  fg="white", 
                                  width=16, 
                                  height=2, 
                                  cursor="hand2", 
                                  relief="raised", 
                                  bd=4)
        self.btn_auto.grid(row=0, column=1, padx=10)
        
        self.btn_settings = tk.Button(btn_frame, 
                                      text="SETTINGS", 
                                      command=self.open_settings, 
                                      font=("Arial", 15, "bold"), 
                                      bg="#ffaa00", 
                                      fg="black", 
                                      width=16, 
                                      height=2, 
                                      cursor="hand2", 
                                      relief="raised", 
                                      bd=4)
        self.btn_settings.grid(row=0, column=2, padx=10)

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Game Settings")
        settings_window.geometry("600x700")
        settings_window.configure(bg=COLOR_SCHEME["bg_panel"])
        settings_window.transient(self.root)
        
        tk.Label(settings_window, 
                text="GAME SETTINGS", 
                font=("Impact", 26),
                bg=COLOR_SCHEME["bg_panel"], 
                fg=COLOR_SCHEME["text_primary"]).pack(pady=15)
        
        canvas = tk.Canvas(settings_window, bg=COLOR_SCHEME["bg_panel"], highlightthickness=0)
        scrollbar = tk.Scrollbar(settings_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=COLOR_SCHEME["bg_panel"])
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        settings_vars = {}
        
        def create_setting(parent, label_text, setting_key, setting_type="int", min_val=None, max_val=None):
            frame = tk.Frame(parent, bg=COLOR_SCHEME["bg_panel"])
            frame.pack(pady=8, padx=20, fill="x")
            
            tk.Label(frame, 
                    text=label_text, 
                    font=("Arial", 11, "bold"),
                    bg=COLOR_SCHEME["bg_panel"], 
                    fg=COLOR_SCHEME["text_light"],
                    anchor="w").pack(side="left", fill="x", expand=True)
            
            if setting_type == "bool":
                var = tk.BooleanVar(value=self.settings[setting_key])
                cb = tk.Checkbutton(frame, 
                                   variable=var,
                                   bg=COLOR_SCHEME["bg_panel"],
                                   activebackground=COLOR_SCHEME["bg_panel"],
                                   selectcolor=COLOR_SCHEME["bg_display"])
                cb.pack(side="right")
            else:
                var = tk.StringVar(value=str(self.settings[setting_key]))
                entry = tk.Entry(frame, 
                               textvariable=var,
                               font=("Arial", 10),
                               width=15,
                               bg=COLOR_SCHEME["bg_display"],
                               fg=COLOR_SCHEME["text_light"],
                               insertbackground=COLOR_SCHEME["text_primary"])
                entry.pack(side="right")
            
            settings_vars[setting_key] = (var, setting_type)
        
        tk.Label(scrollable_frame, 
                text="Performance Settings", 
                font=("Arial", 13, "bold"),
                bg=COLOR_SCHEME["bg_panel"], 
                fg=COLOR_SCHEME["accent_gold"]).pack(pady=(10, 5), anchor="w", padx=20)
        
        create_setting(scrollable_frame, "Auto Roll Speed (ms)", "auto_roll_speed", "int")
        create_setting(scrollable_frame, "Animation Speed (ms)", "animation_speed", "int")
        create_setting(scrollable_frame, "Particle Multiplier", "particle_count_multiplier", "float")
        create_setting(scrollable_frame, "Show Particle Effects", "show_particle_effects", "bool")
        
        tk.Label(scrollable_frame, 
                text="Biome Settings", 
                font=("Arial", 13, "bold"),
                bg=COLOR_SCHEME["bg_panel"], 
                fg=COLOR_SCHEME["accent_gold"]).pack(pady=(15, 5), anchor="w", padx=20)
        
        create_setting(scrollable_frame, "Normal Biome Min Duration (ms)", "biome_change_min", "int")
        create_setting(scrollable_frame, "Normal Biome Max Duration (ms)", "biome_change_max", "int")
        create_setting(scrollable_frame, "Glitch Biome Min Duration (ms)", "glitch_biome_duration_min", "int")
        create_setting(scrollable_frame, "Glitch Biome Max Duration (ms)", "glitch_biome_duration_max", "int")
        create_setting(scrollable_frame, "Hell Biome Min Duration (ms)", "hell_biome_duration_min", "int")
        create_setting(scrollable_frame, "Hell Biome Max Duration (ms)", "hell_biome_duration_max", "int")
        create_setting(scrollable_frame, "Corruption Biome Min Duration (ms)", "corruption_biome_duration_min", "int")
        create_setting(scrollable_frame, "Corruption Biome Max Duration (ms)", "corruption_biome_duration_max", "int")
        
        tk.Label(scrollable_frame, 
                text="Display Settings", 
                font=("Arial", 13, "bold"),
                bg=COLOR_SCHEME["bg_panel"], 
                fg=COLOR_SCHEME["accent_gold"]).pack(pady=(15, 5), anchor="w", padx=20)
        
        create_setting(scrollable_frame, "Window Width", "window_width", "int")
        create_setting(scrollable_frame, "Window Height", "window_height", "int")
        create_setting(scrollable_frame, "Canvas Width", "canvas_width", "int")
        create_setting(scrollable_frame, "Canvas Height", "canvas_height", "int")
        
        def save_settings():
            try:
                for key, (var, var_type) in settings_vars.items():
                    if var_type == "int":
                        self.settings[key] = int(var.get())
                    elif var_type == "float":
                        self.settings[key] = float(var.get())
                    elif var_type == "bool":
                        self.settings[key] = var.get()
                    else:
                        self.settings[key] = var.get()
                
                self.settings = config_manager.sanitize_settings(self.settings)
                config_manager.save_settings(self.settings)
                
                messagebox.showinfo("Success", "Settings saved! Restart the game for all changes to take effect.")
                settings_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save settings: {str(e)}")
        
        def reset_defaults():
            if messagebox.askyesno("Reset Settings", "Are you sure you want to reset all settings to defaults?"):
                default_settings = DEFAULT_SETTINGS
                
                for key, (var, var_type) in settings_vars.items():
                    if key in default_settings:
                        if var_type == "bool":
                            var.set(default_settings[key])
                        else:
                            var.set(str(default_settings[key]))
        
        btn_frame = tk.Frame(scrollable_frame, bg=COLOR_SCHEME["bg_panel"])
        btn_frame.pack(pady=20)
        
        tk.Button(btn_frame, 
                 text="Save Settings", 
                 command=save_settings,
                 font=("Arial", 13, "bold"),
                 bg=COLOR_SCHEME["text_success"],
                 fg="black",
                 width=15,
                 cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, 
                 text="Reset to Defaults", 
                 command=reset_defaults,
                 font=("Arial", 13, "bold"),
                 bg=COLOR_SCHEME["text_warning"],
                 fg="black",
                 width=15,
                 cursor="hand2").pack(side="left", padx=5)
        
        tk.Button(btn_frame, 
                 text="Close", 
                 command=settings_window.destroy,
                 font=("Arial", 13, "bold"),
                 bg=COLOR_SCHEME["text_secondary"],
                 fg="white",
                 width=15,
                 cursor="hand2").pack(side="left", padx=5)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y")

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
        self.lbl_biome.config(fg=colors["text"])
        
        self.lbl_biome.config(text=f"Biome: {self.current_biome}")
        print(f"BIOME_UPDATE:{self.current_biome}")
        sys.stdout.flush()
        
        if self.current_biome == "Glitch":
            duration = random.randint(
                self.settings["glitch_biome_duration_min"],
                self.settings["glitch_biome_duration_max"]
            )
        elif self.current_biome == "Hell":
            duration = random.randint(
                self.settings["hell_biome_duration_min"],
                self.settings["hell_biome_duration_max"]
            )
        elif self.current_biome == "Corruption":
            duration = random.randint(
                self.settings["corruption_biome_duration_min"],
                self.settings["corruption_biome_duration_max"]
            )
        else:
            duration = random.randint(
                self.settings["biome_change_min"],
                self.settings["biome_change_max"]
            )
        
        self.root.after(duration, self.biome_tick)

    def manual_roll(self):
        if not self.animation_running:
            self.roll()

    def toggle_auto(self):
        self.auto_rolling = not self.auto_rolling
        color = "#00cc44" if self.auto_rolling else COLOR_SCHEME["accent_red"]
        state = "ON" if self.auto_rolling else "OFF"
        self.btn_auto.config(text=f"AUTO: {state}", bg=color)
        if self.auto_rolling:
            self.auto_loop()

    def auto_loop(self):
        if self.auto_rolling:
            if not self.animation_running:
                self.roll()
            self.root.after(self.settings["auto_roll_speed"], self.auto_loop)

    def roll(self):
        self.session_rolls += 1
        self.total_rolls += 1
        self.lbl_count.config(text=f"Session Rolls: {self.session_rolls}")
        self.lbl_stats_header.config(text=f"Total Rolls: {self.total_rolls}")
        self.save_data()
        
        applicable = self.aura_db.get_applicable_auras(self.current_biome)
        applicable.sort(key=lambda x: x["rarity"], reverse=True)
        
        found = applicable[-1]
        
        for aura in applicable:
            if random.randint(1, aura["rarity"]) == 1:
                found = aura
                break
        
        self.animate_roll(found)
        print(f"ROLL:{found['name']}:{found['rarity']}")
        sys.stdout.flush()

    def animate_roll(self, final_aura):
        self.animation_running = True
        self.canvas.delete("all")
        
        rarity = final_aura["rarity"]
        
        if rarity >= 3000:
            color = "#00ffff"
        elif rarity >= 2500:
            color = "#ff00ff"
        elif rarity >= 2000:
            color = "#ff1a1a"
        elif rarity >= 1500:
            color = "#ffaa00"
        elif rarity >= 1000:
            color = COLOR_SCHEME["accent_gold"]
        elif rarity >= 500:
            color = "#ff6600"
        elif rarity >= 250:
            color = "#ff0066"
        elif rarity >= 100:
            color = "#9933ff"
        elif rarity >= 25:
            color = "#0099ff"
        else:
            color = "#aaaaaa"
        
        self.lbl_res.config(text=f"{final_aura['name']} (1/{final_aura['rarity']})", 
                           fg=color, 
                           bg=COLOR_SCHEME["bg_panel"])
        self.lbl_res.place(relx=0.5, y=-100, anchor="center")
        
        def slide_down(current_y=-100, target_y=230):
            if current_y < target_y:
                self.lbl_res.place(relx=0.5, y=current_y, anchor="center")
                self.root.after(self.settings["animation_speed"], lambda: slide_down(current_y + 9, target_y))
            else:
                self.lbl_res.place(relx=0.5, y=230, anchor="center")
                if self.settings["show_particle_effects"]:
                    self.draw_particles(final_aura)
                self.animation_running = False
        
        slide_down()

    def draw_particles(self, aura):
        rarity = aura["rarity"]
        base_count = min(80, max(20, rarity // 12))
        particle_count = int(base_count * self.settings["particle_count_multiplier"])
        canvas_width = max(140, int(self.settings["canvas_width"]))
        canvas_height = max(40, int(self.settings["canvas_height"]))
        
        for _ in range(particle_count):
            x = random.randint(10, canvas_width - 10)
            y = random.randint(5, canvas_height - 5)
            size = random.randint(3, 10)
            
            if rarity >= 2500:
                color = random.choice(["#ff00ff", "#00ffff", "#ffff00", "#ff00ff"])
            elif rarity >= 1000:
                color = random.choice([COLOR_SCHEME["accent_gold"], "#ffff00", "#ff00ff", "#00ffff"])
            elif rarity >= 500:
                color = random.choice(["#ff6600", COLOR_SCHEME["accent_gold"], "#ff8800"])
            elif rarity >= 250:
                color = random.choice(["#ff0066", "#ff33cc", "#ff6699"])
            elif rarity >= 100:
                color = random.choice(["#9933ff", "#aa44ff", "#bb55ff"])
            else:
                color = random.choice(["#aaaaaa", "#bbbbbb", "#cccccc"])
            
            self.canvas.create_oval(x, y, x+size, y+size, fill=color, outline="")
            
            if rarity >= 1000 and random.random() < 0.3:
                star_size = random.randint(1, 3)
                star_char = random.choice(["*", "+", "x"])
                self.canvas.create_text(x, y, text=star_char, fill=color, font=("Arial", star_size*5))

if __name__ == "__main__":
    root = tk.Tk()
    app = PythoRNG(root)
    root.mainloop()
