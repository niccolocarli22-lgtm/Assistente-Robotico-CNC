import pyautogui
import time
import pyperclip

class RobotAutomator:
    def __init__(self, coords: dict):
        self.coords = coords
        pyautogui.FAILSAFE = True

    def run_automation(self, dxf_path: str, nome: str, spessore: float):
        try:
            # Import DXF
            if "menu_import" in self.coords:
                pyautogui.click(self.coords["menu_import"][0], self.coords["menu_import"][1])
                time.sleep(1.5)

            pyperclip.copy(str(dxf_path))
            pyautogui.hotkey("ctrl", "v")
            time.sleep(0.8)
            pyautogui.press("enter")
            time.sleep(2.0)

            # Nome Pezzo
            if "campo_nome" in self.coords:
                pyautogui.click(self.coords["campo_nome"][0], self.coords["campo_nome"][1])
                time.sleep(0.6)
                pyautogui.write(nome)

            # Spessore
            if "campo_spessore" in self.coords:
                pyautogui.click(self.coords["campo_spessore"][0], self.coords["campo_spessore"][1])
                time.sleep(0.6)
                pyautogui.write(str(spessore))

            # Calcola Sequenza
            if "btn_calcola" in self.coords:
                pyautogui.click(self.coords["btn_calcola"][0], self.coords["btn_calcola"][1])

            print("✅ Automazione RPA completata.")
        except Exception as e:
            print(f"Errore automazione: {e}")
