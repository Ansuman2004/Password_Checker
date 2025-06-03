import requests
from bs4 import BeautifulSoup
import re

headers = {
    'User-Agent': 'Mozilla/5.0'
}

def is_vulnerable_to_sqli(url):
    payload = "' OR '1'='1"
    try:
        r = requests.get(url + payload, headers=headers, timeout=5)
        if "sql" in r.text.lower() or "mysql" in r.text.lower() or "syntax" in r.text.lower():
            return True
    except:
        pass
    return False

def is_vulnerable_to_xss(url):
    xss_test = "<script>alert(1)</script>"
    try:
        r = requests.get(url + xss_test, headers=headers, timeout=5)
        if xss_test in r.text:
            return True
    except:
        pass
    return False

def check_insecure_headers(url):
    try:
        r = requests.get(url, headers=headers)
        issues = []
        if 'X-Frame-Options' not in r.headers:
            issues.append('Missing X-Frame-Options')
        if 'Content-Security-Policy' not in r.headers:
            issues.append('Missing Content-Security-Policy')
        if 'X-XSS-Protection' not in r.headers:
            issues.append('Missing X-XSS-Protection')
        return issues
    except:
        return ['Unable to fetch headers']

def find_admin_panels(base_url):
    common_admin_paths = ['admin', 'admin/login', 'administrator', 'admin123']
    found = []
    for path in common_admin_paths:
        test_url = base_url.rstrip('/') + '/' + path
        try:
            r = requests.get(test_url, headers=headers, timeout=5)
            if r.status_code == 200:
                found.append(test_url)
        except:
            pass
    return found

def crawl_website(url):
    visited = set()
    to_visit = [url]

    while to_visit:
        current_url = to_visit.pop()
        if current_url in visited:
            continue
        visited.add(current_url)
        try:
            r = requests.get(current_url, headers=headers, timeout=5)
            soup = BeautifulSoup(r.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith('/'):
                    href = url.rstrip('/') + href
                if href.startswith(url):
                    to_visit.append(href)
        except:
            pass
    return visited

def main():
    base_url = input("Enter target URL (e.g., https://example.com): ").strip()
    report = {}

    print("\n[+] Crawling website...")
    urls = crawl_website(base_url)
    print(f"[+] {len(urls)} URLs found.")

    for url in urls:
        print(f"\nScanning: {url}")
        report[url] = {
            'SQL Injection': is_vulnerable_to_sqli(url),
            'XSS': is_vulnerable_to_xss(url),
            'Insecure Headers': check_insecure_headers(url)
        }

    admin_urls = find_admin_panels(base_url)
    report['Admin Panels'] = admin_urls

    print("\n[+] Scan complete. Generating report...\n")
    with open("scan_report.txt", "w") as f:
        for url, issues in report.items():
            f.write(f"\nURL: {url}\n")
            if isinstance(issues, dict):
                for key, val in issues.items():
                    f.write(f"  {key}: {val}\n")
            else:
                f.write(f"  {issues}\n")

    print("[✓] Report saved to scan_report.txt")

if __name__ == "__main__":
    main()
