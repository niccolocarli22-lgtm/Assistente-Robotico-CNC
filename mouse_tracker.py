import pyautogui
import time

print("🖱️ Mouse Tracker avviato - Muovi il mouse sui punti del software CNC")
print("Premi CTRL + C per fermare\n")

try:
    while True:
        x, y = pyautogui.position()
        print(f"X: {x:4} | Y: {y:4}", end="\r")
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n\nTracker terminato.")
