import tkinter as tk
from tkinter import ttk
import re
import math

# ---------------- Common Passwords ---------------- #
common_passwords = ["123456", "password", "12345678", "qwerty", "abc123"]

# ---------------- Password Strength ---------------- #
def check_password():
    password = entry.get()

    score = 0
    missing = []

    # Common password check
    if password.lower() in common_passwords:
        result_label.config(text="Very Weak ❌", fg="red")
        missing_label.config(text="Common password detected!")
        progress['value'] = 10
        entropy_label.config(text="Entropy: Low")
        crack_label.config(text="Crack Time: Instantly")
        return

    if len(password) >= 8:
        score += 1
    else:
        missing.append("Min 8 chars")

    if re.search(r"[A-Z]", password):
        score += 1
    else:
        missing.append("Uppercase")

    if re.search(r"[0-9]", password):
        score += 1
    else:
        missing.append("Number")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 1
    else:
        missing.append("Special char")

    # Strength levels
    if score == 4:
        strength = "Strong 💪"
        color = "#00c853"
        progress['value'] = 100
    elif score == 3:
        strength = "Medium ⚠"
        color = "#ff9800"
        progress['value'] = 70
    else:
        strength = "Weak ❌"
        color = "#ff1744"
        progress['value'] = 30

    result_label.config(text=strength, fg=color)

    if missing:
        missing_label.config(text="Missing: " + ", ".join(missing))
    else:
        missing_label.config(text="All requirements met ✅")

    # Entropy + Crack Time
    entropy = calculate_entropy(password)
    crack_time = estimate_crack_time(entropy)

    entropy_label.config(text=f"Entropy: {entropy} bits")
    crack_label.config(text=f"Crack Time: {crack_time}")


# ---------------- Entropy ---------------- #
def calculate_entropy(password):
    pool = 0

    if re.search(r"[a-z]", password):
        pool += 26
    if re.search(r"[A-Z]", password):
        pool += 26
    if re.search(r"[0-9]", password):
        pool += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        pool += 32

    if pool == 0:
        return 0

    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)


# ---------------- Crack Time ---------------- #
def estimate_crack_time(entropy):
    guesses_per_second = 1e9
    seconds = 2 ** entropy / guesses_per_second

    if seconds < 60:
        return f"{seconds:.2f} sec"
    elif seconds < 3600:
        return f"{seconds/60:.2f} min"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hrs"
    elif seconds < 31536000:
        return f"{seconds/86400:.2f} days"
    else:
        return f"{seconds/31536000:.2f} years"


# ---------------- Toggle Password ---------------- #
def toggle_password():
    if entry.cget('show') == '*':
        entry.config(show='')
        toggle_btn.config(text="Hide 👁️")
    else:
        entry.config(show='*')
        toggle_btn.config(text="Show 👁️")


# ---------------- GUI Setup ---------------- #
root = tk.Tk()
root.title("🔐 Password Security Analyzer")
root.geometry("450x420")
root.config(bg="#121212")

title = tk.Label(root, text="Password Security Analyzer",
                 font=("Arial", 16, "bold"),
                 bg="#121212", fg="white")
title.pack(pady=15)

entry = tk.Entry(root, show="*", width=30,
                 font=("Arial", 12),
                 bg="#1e1e1e", fg="white",
                 insertbackground="white")
entry.pack(pady=10)

toggle_btn = tk.Button(root, text="Show 👁️",
                       command=toggle_password,
                       bg="#333", fg="white")
toggle_btn.pack()

check_btn = tk.Button(root, text="Analyze Password",
                      command=check_password,
                      bg="#2962ff", fg="white",
                      font=("Arial", 11, "bold"),
                      padx=10, pady=5)
check_btn.pack(pady=15)

# Strength Label
result_label = tk.Label(root, text="",
                        font=("Arial", 14, "bold"),
                        bg="#121212")
result_label.pack()

# Progress Bar 🔥
progress = ttk.Progressbar(root, length=300, mode='determinate')
progress.pack(pady=10)

# Missing
missing_label = tk.Label(root, text="",
                         font=("Arial", 10),
                         bg="#121212", fg="#bbbbbb")
missing_label.pack()

# Entropy
entropy_label = tk.Label(root, text="",
                         font=("Arial", 11),
                         bg="#121212", fg="#00e5ff")
entropy_label.pack(pady=5)

# Crack Time
crack_label = tk.Label(root, text="",
                       font=("Arial", 11),
                       bg="#121212", fg="#ffd600")
crack_label.pack()

root.mainloop()