import os
import itertools
import time
import pikepdf
from tqdm import tqdm
from PyPDF2 import PdfWriter, PdfReader

def encrypt_pdf():
    input_path = input("Enter path to input PDF: ")
    output_path = input("Enter path to save encrypted PDF: ")
    password = input("Enter password to encrypt the PDF: ")

    if not os.path.exists(input_path):
        print("[!] Input file does not exist.")
        return

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            writer.add_page(page)

        writer.encrypt(password)

        with open(output_path, 'wb') as f:
            writer.write(f)

        print("[✓] PDF encrypted successfully.")

    except Exception as e:
        print(f"[!] Encryption failed: {e}")

def crack_pdf():
    pdf_path = input("Enter path to password-protected PDF: ")
    if not os.path.exists(pdf_path):
        print("[!] File not found.")
        return

    method = input("Choose method - 1 for Wordlist, 2 for Brute-force: ")

    if method == '1':
        wordlist_path = input("Enter path to wordlist file: ")
        if not os.path.exists(wordlist_path):
            print("[!] Wordlist not found.")
            return

        with open(wordlist_path, "r") as f:
            passwords = [line.strip() for line in f]
    elif method == '2':
        charset = input("Enter charset (e.g., 0123456789 or abcdef): ")
        min_len = int(input("Enter min password length: "))
        max_len = int(input("Enter max password length: "))
        passwords = [
            ''.join(candidate)
            for length in range(min_len, max_len + 1)
            for candidate in itertools.product(charset, repeat=length)
        ]
    else:
        print("[!] Invalid method choice.")
        return

    print("\n🔐 Cracking PDF... Please wait.\n")
    found = False

    for pwd in tqdm(passwords, desc="Trying passwords", unit="password", dynamic_ncols=True):
        try:
            with pikepdf.open(pdf_path, password=pwd) as pdf:
                print(f"\n[+] Password found: {pwd}")

                # Save decrypted PDF
                output_file = os.path.splitext(pdf_path)[0] + "_decrypted.pdf"
                pdf.save(output_file)

                # Show decryption progress bar
                for _ in tqdm(range(100), desc="Decrypting PDF", unit="%", leave=False):
                    time.sleep(0.01)

                print()  # Ensure clean line after progress bar
                print(f"[✓] PDF decrypted successfully with password: {pwd}")
                found = True
                break
        except pikepdf._core.PasswordError:
            continue

    if not found:
        print("\n[✗] Password not found.")

def main():
    while True:
        print("\n====== PDF SECURITY TOOL ======")
        print("1. Encrypt a PDF")
        print("2. Crack a PDF")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            encrypt_pdf()
        elif choice == '2':
            crack_pdf()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("[!] Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()