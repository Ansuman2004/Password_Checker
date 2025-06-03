import os
import sqlite3
import time
import shutil
import pandas as pd
import requests
from urllib.parse import urlparse
from tqdm import tqdm

# Constants
CHROME_HISTORY_PATH = os.path.expanduser(
    r"~\AppData\Local\Google\Chrome\User Data\Default\History"
)
PHISHTANK_FEED = "https://data.phishtank.com/data/online-valid.json"

def copy_history_file():
    temp_path = "chrome_history_copy"
    try:
        shutil.copy2(CHROME_HISTORY_PATH, temp_path)
        return temp_path
    except Exception as e:
        print("[!] Error copying Chrome history:", e)
        return None

def extract_history(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT url, title, last_visit_time FROM urls ORDER BY last_visit_time DESC")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        print("[!] Failed to read history:", e)
        return []

def load_phishtank_domains():
    try:
        print("[*] Downloading phishing domain list...")
        response = requests.get(PHISHTANK_FEED)
        if response.status_code == 200:
            data = response.json()
            domains = set(urlparse(entry["url"]).netloc for entry in data)
            print(f"[+] Loaded {len(domains)} phishing domains from PhishTank.")
            return domains
        else:
            print("[!] Failed to fetch PhishTank feed.")
            return set()
    except Exception as e:
        print("[!] Error fetching PhishTank feed:", e)
        return set()

def analyze_urls(history, phishing_domains):
    print("\n🔍 Analyzing browser history for hijacks and phishing...")
    hijack_suspects = []
    for url, title, timestamp in tqdm(history[:500]):  # Limit to latest 500 for speed
        domain = urlparse(url).netloc
        if any(keyword in url.lower() for keyword in ['login', 'redirect', 'verify', 'auth']):
            if domain in phishing_domains:
                hijack_suspects.append((url, title, domain))
    return hijack_suspects

def generate_report(suspects):
    if not suspects:
        print("\n✅ No hijacks or phishing detected in recent history.")
        return
    print("\n🚨 Potential Hijack/Phishing URLs Detected:")
    for i, (url, title, domain) in enumerate(suspects, 1):
        print(f"{i}. {url} | Title: {title} | Domain: {domain}")
    df = pd.DataFrame(suspects, columns=["URL", "Title", "Domain"])
    df.to_csv("hijack_report.csv", index=False)
    print("\n[✓] Report saved as 'hijack_report.csv'")

def main():
    print("=== Browser History Hijack Detector ===\n")
    db_path = copy_history_file()
    if not db_path:
        return

    history = extract_history(db_path)
    if not history:
        print("[!] No history data found.")
        return

    phishing_domains = load_phishtank_domains()
    suspects = analyze_urls(history, phishing_domains)
    generate_report(suspects)

    # Cleanup
    os.remove(db_path)

if __name__ == "__main__":
    main()
