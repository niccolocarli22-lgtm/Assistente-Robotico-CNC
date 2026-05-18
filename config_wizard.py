import customtkinter as ctk
import json
from pathlib import Path
import pyautogui
import time

class ConfigWizard(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("⚙️ Configurazione Iniziale - Assistente CNC")
        self.geometry("1050x750")
        self.config_path = Path("config.json")
        self.config = self.load_config()
        self.create_widgets()

    def load_config(self):
        if self.config_path.exists():
            with open(self.config_path, encoding="utf-8") as f:
                return json.load(f)
        return {"api_key": "", "coords": {}}

    def create_widgets(self):
        ctk.CTkLabel(self, text="Configurazione Iniziale", font=ctk.CTkFont(size=24, weight="bold")).pack(pady=15)

        # API Key
        api_frame = ctk.CTkFrame(self)
        api_frame.pack(pady=10, padx=30, fill="x")
        ctk.CTkLabel(api_frame, text="Google Gemini API Key", font=ctk.CTkFont(weight="bold")).pack(anchor="w", padx=20, pady=5)
        self.api_entry = ctk.CTkEntry(api_frame, width=720, height=40)
        self.api_entry.insert(0, self.config.get("api_key", ""))
        self.api_entry.pack(padx=20, pady=5)

        # Coordinate
        ctk.CTkLabel(self, text="Coordinate del Software CNC", font=ctk.CTkFont(size=18, weight="bold")).pack(pady=20)

        self.fields = {
            "menu_import": "1. Pulsante 'Importa' o 'File → Import DXF'",
            "campo_nome": "2. Campo Nome Pezzo",
            "campo_spessore": "3. Campo Spessore Lamiera",
            "btn_calcola": "4. Pulsante Calcola Sequenza Pieghe",
            "btn_conferma": "5. Pulsante Conferma / OK (se presente)"
        }

        self.coord_entries = {}
        for key, desc in self.fields.items():
            frame = ctk.CTkFrame(self)
            frame.pack(pady=8, padx=30, fill="x")
            ctk.CTkLabel(frame, text=desc, anchor="w").pack(side="left", padx=15, fill="x", expand=True)
            
            self.coord_entries[key] = ctk.CTkEntry(frame, width=220)
            self.coord_entries[key].pack(side="right", padx=10)
            
            ctk.CTkButton(frame, text="📍 Cattura", width=110,
                         command=lambda k=key: self.capture(k)).pack(side="right", padx=10)

        ctk.CTkButton(self, text="💾 SALVA CONFIGURAZIONE", height=50, fg_color="green",
                     font=ctk.CTkFont(size=16, weight="bold"),
                     command=self.save_config).pack(pady=30)

    def capture(self, key):
        self.iconify()
        time.sleep(1.8)
        x, y = pyautogui.position()
        self.config["coords"][key] = [x, y]
        self.coord_entries[key].delete(0, "end")
        self.coord_entries[key].insert(0, f"({x}, {y})")
        self.deiconify()

    def save_config(self):
        self.config["api_key"] = self.api_entry.get().strip()
        with open(self.config_path, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)
        ctk.CTkLabel(self, text="✅ Salvato con successo!", text_color="lime").pack(pady=10)
