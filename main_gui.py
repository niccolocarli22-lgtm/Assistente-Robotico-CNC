import customtkinter as ctk
from tkinter import filedialog
import json
from pathlib import Path
import logging

from gemini_vision_parser import GeminiVisionParser
from dxf_builder import DXFBuilder
from robot_automator import RobotAutomator
from config_wizard import ConfigWizard

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AssistenteCNC(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🤖 Assistente Robotico CNC - Pressa Piegatrice")
        self.geometry("1150x780")
        self.config_path = Path("config.json")
        self.setup_logging()
        self.create_widgets()

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    def create_widgets(self):
        ctk.CTkLabel(self, text="Assistente Robotico CNC", font=ctk.CTkFont(size=28, weight="bold")).pack(pady=20)

        ctk.CTkButton(self, text="⚙️ Configurazione Iniziale (API + Coordinate)", 
                     height=40, command=self.open_config).pack(pady=10)

        # Carica Immagine
        self.img_var = ctk.StringVar()
        ctk.CTkButton(self, text="📁 Carica Immagine del Disegno", 
                     command=self.load_image).pack(pady=12)

        self.lbl_img = ctk.CTkLabel(self, text="Nessuna immagine caricata")
        self.lbl_img.pack(pady=5)

        # Parametri
        frame = ctk.CTkFrame(self)
        frame.pack(pady=15, padx=30, fill="x")
        ctk.CTkLabel(frame, text="Nome Pezzo:").grid(row=0, column=0, padx=10, pady=8)
        self.nome_entry = ctk.CTkEntry(frame, width=250)
        self.nome_entry.grid(row=0, column=1, padx=10, pady=8)

        ctk.CTkLabel(frame, text="Spessore (mm):").grid(row=1, column=0, padx=10, pady=8)
        self.spess_entry = ctk.CTkEntry(frame, width=100)
        self.spess_entry.insert(0, "2.0")
        self.spess_entry.grid(row=1, column=1, padx=10, pady=8)

        # Bottone Avvio
        self.start_btn = ctk.CTkButton(self, text="🚀 GENERA DXF E AVVIA AUTOMAZIONE", 
                                      height=60, font=ctk.CTkFont(size=18, weight="bold"),
                                      command=self.start_process)
        self.start_btn.pack(pady=25)

        # Log
        self.log_box = ctk.CTkTextbox(self, height=280)
        self.log_box.pack(padx=25, pady=10, fill="both", expand=True)

    def open_config(self):
        ConfigWizard(self)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Immagini", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            self.img_var.set(path)
            self.lbl_img.configure(text=Path(path).name)

    def log(self, text):
        self.log_box.insert("end", text + "\n")
        self.log_box.see("end")
        logging.info(text)

    def start_process(self):
        try:
            if not self.img_var.get():
                self.log("❌ Carica prima un'immagine!")
                return

            with open(self.config_path, encoding='utf-8') as f:
                config = json.load(f)

            if not config.get("api_key"):
                self.log("❌ Inserisci l'API Key di Gemini nella configurazione!")
                return

            self.log("🔄 Analisi immagine con Gemini...")
            parser = GeminiVisionParser(config["api_key"])
            data = parser.analizza_immagine(self.img_var.get())

            self.log("📐 Generazione file DXF...")
            builder = DXFBuilder()
            dxf_path = builder.build_dxf(data, self.nome_entry.get() or "Pezzo")

            self.log("🤖 Avvio automazione RPA...")
            robot = RobotAutomator(config.get("coords", {}))
            robot.import_dxf(dxf_path)
            robot.set_parameters(self.nome_entry.get() or "Pezzo", float(self.spess_entry.get()))

            self.log("✅ OPERAZIONE COMPLETATA CON SUCCESSO!")

        except Exception as e:
            self.log(f"❌ ERRORE: {str(e)}")

if __name__ == "__main__":
    app = AssistenteCNC()
    app.mainloop()
