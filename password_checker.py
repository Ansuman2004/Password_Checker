import tkinter as tk
from tkinter import messagebox
import re
import math
import hashlib
import requests
from datetime import datetime

history_file = "password_history.txt"

def calculate_entropy(password):
    charset = 0
    if re.search(r'[a-z]', password):
        charset += 26
    if re.search(r'[A-Z]', password):
        charset += 26
    if re.search(r'[0-9]', password):
        charset += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset += 32
    if charset == 0:
        return 0
    return round(len(password) * math.log2(charset), 2)

def check_breached(password):
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        res = requests.get(url)
        if suffix in res.text:
            return True
        return False
    except:
        return None  # API failed

def evaluate_password(password):
    score = 0
    feedback = []

    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Too short (min 8 characters).")

    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters.")

    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters.")

    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Add digits.")

    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add special characters.")

    if score == 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    entropy = calculate_entropy(password)
    breached = check_breached(password)

    return strength, entropy, feedback, breached

def update_feedback(event=None):
    password = entry.get()
    strength, entropy, feedback, breached = evaluate_password(password)
    result_var.set(f"Strength: {strength} | Entropy: {entropy}")
    suggestions.delete(0, tk.END)
    for fb in feedback:
        suggestions.insert(tk.END, fb)
    if breached is True:
        breach_label.config(text="⚠️ This password has been breached!", fg="red")
    elif breached is False:
        breach_label.config(text="✅ Not found in breaches.", fg="green")
    else:
        breach_label.config(text="🔄 Could not verify breach status.", fg="gray")

    with open(history_file, "a") as file:
        file.write(f"{datetime.now()}: {password} ({strength}, Entropy: {entropy})\\n")

app = tk.Tk()
app.title("Password Strength Checker")
app.geometry("500x400")

tk.Label(app, text="Enter Password:").pack(pady=5)
entry = tk.Entry(app, show="*", width=40)
entry.pack(pady=5)
entry.bind("<KeyRelease>", update_feedback)

result_var = tk.StringVar()
tk.Label(app, textvariable=result_var, font=("Helvetica", 12)).pack(pady=10)

breach_label = tk.Label(app, text="", font=("Helvetica", 10))
breach_label.pack()

tk.Label(app, text="Suggestions:").pack()
suggestions = tk.Listbox(app, width=50, height=6)
suggestions.pack(pady=5)

app.mainloop()
