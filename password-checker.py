import re
import tkinter as tk
from tkinter import messagebox

# Common weak passwords
COMMON = {"password","123456","123456789","qwerty","admin","letmein","welcome","iloveyou"}
# Regex tests
TESTS  = {"lowercase":r"[a-z]","uppercase":r"[A-Z]","number":r"\d","special":r"[^\w\s]"}

def check_password(pw, user=None):
    score, tips, kinds = min(len(pw)*4,40), [], 0
    if len(pw)<12: tips.append("There should be 12–16+ characters")
    for name,pat in TESTS.items():
        if re.search(pat,pw): score+=10; kinds+=1
        else: tips.append(f"add {name}")
    score += (5 if kinds>=3 else 0)+(5 if kinds==4 else 0)

    if pw.isalpha() or pw.isdigit(): score-=10; tips.append("avoid only letters/numbers")
    if re.search(r"(.)\1{2,}",pw): score-=10; tips.append("avoid repeats like 'aaa'")
    if any(w in pw.lower() for w in COMMON): score-=15; tips.append("avoid common words")
    if user and user.lower() in pw.lower(): score-=10; tips.append("don't include username")

    score = max(0,min(score,100))
    rating = ["Very Weak","Weak","Strong","Very Strong"][(score>25)+(score>50)+(score>75)]
    return score,rating,sorted(set(tips))

# GUI App
def analyze():
    pw = password_entry.get()
    user = username_entry.get().strip() or None
    if not pw:
        messagebox.showwarning("Error","Please enter a password")
        return
    score,rating,tips = check_password(pw,user)
    result_var.set(f"Score: {score}/100 → {rating}")
    if tips:
        tips_text.set("\n".join("• "+t for t in tips))
    else:
        tips_text.set("Looks good! ✅")

# Create window
root = tk.Tk()
root.title("Password Complexity Checker")
root.geometry("400x300")
root.config(bg="#1e1e2f")

# Widgets
tk.Label(root,text="Username (optional):",bg="#1e1e2f",fg="white").pack(anchor="w",padx=10,pady=5)
username_entry = tk.Entry(root,width=30)
username_entry.pack(padx=10,pady=2)

tk.Label(root,text="Password:",bg="#1e1e2f",fg="white").pack(anchor="w",padx=10,pady=5)
password_entry = tk.Entry(root,show="*",width=30)
password_entry.pack(padx=10,pady=2)

tk.Button(root,text="Check Strength",command=analyze,bg="#3b82f6",fg="white").pack(pady=10)

result_var = tk.StringVar()
tk.Label(root,textvariable=result_var,bg="#1e1e2f",fg="cyan",font=("Arial",12,"bold")).pack(pady=5)

tips_text = tk.StringVar()
tk.Label(root,textvariable=tips_text,bg="#1e1e2f",fg="orange",justify="left",wraplength=380).pack(padx=10,pady=10)

root.mainloop()
