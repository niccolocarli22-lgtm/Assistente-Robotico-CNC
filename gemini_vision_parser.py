import google.generativeai as genai
import json
import re
from PIL import Image
import logging

class GeminiVisionParser:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def analizza_immagine(self, image_path: str) -> dict:
        try:
            image = Image.open(image_path)
            prompt = """
Sei un esperto di piegatura lamiera CNC. Analizza il disegno e restituisci SOLO un JSON valido:

{
  "segmenti": [
    {"tipo": "linea", "lunghezza": 150.0},
    {"tipo": "piega", "angolo": 90, "raggio": 2.0},
    {"tipo": "linea", "lunghezza": 80.0}
  ]
}
"""
            response = self.model.generate_content([prompt, image])
            text = re.sub(r'```json|```', '', response.text).strip()
            return json.loads(text)
        except Exception as e:
            logging.error(f"Errore Gemini: {e}")
            raise
