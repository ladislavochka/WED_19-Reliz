import customtkinter as ctk
import subprocess
import sys

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

PRESETS = {
    "Small": (600, 120),
    "Medium": (800, 200),
    "Large": (1600, 300),
}

root = ctk.CTk()
root.geometry("480x360")
root.title("Game Menu")

selected = ctk.StringVar(value="Medium")

label = ctk.CTkLabel(root, text="Main Menu", font=ctk.CTkFont(size=28, weight="bold"))
label.pack(pady=18)

def on_start():
    choice = selected.get()
    w, h = PRESETS.get(choice, PRESETS["Medium"])
    root.destroy()
    cmd = [sys.executable, "main.py", str(w), str(h)]
    subprocess.run(cmd)

start_btn = ctk.CTkButton(root, text="Start", command=on_start, width=200)
start_btn.pack(pady=8)

frame = ctk.CTkFrame(root)
frame.pack(pady=12, padx=12, fill="x")

opt_label = ctk.CTkLabel(frame, text="World Size:")
opt_label.pack(anchor="w", padx=8, pady=(6, 0))

for name in ("Small", "Medium", "Large"):
    rb = ctk.CTkRadioButton(frame, text=name, variable=selected, value=name)
    rb.pack(anchor="w", padx=20, pady=4)

exit_btn = ctk.CTkButton(root, text="Exit", command=root.destroy, width=200)
exit_btn.pack(pady=8)

root.mainloop()
