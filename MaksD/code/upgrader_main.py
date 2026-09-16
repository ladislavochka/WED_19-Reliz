import customtkinter as ctk
from PIL import Image


class VisualMG:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("MusorGrade")
        self.window.geometry("1500x1000")
        self.window.resizable(False, False)

        try:
            self.window.iconbitmap("WED_19-Reliz/MaksD/code/icon.ico")
        except Exception:
            pass

        ctk.set_appearance_mode("dark")

        pil_img = Image.open("WED_19-Reliz/MaksD/code/musorgrade.png")
        self.img = ctk.CTkImage(
            light_image=pil_img,
            dark_image=pil_img,
            size=(150, 150)
        )

        self.image_label = ctk.CTkLabel(
            self.window,
            image=self.img,
            text=""
        )

        self.image_label.place(x=0, y=0)

        self.image_label = ctk.CTkLabel(
            self.window,
            image=self.img,
            text="U P G R A D E R",
            font=("Arial", 20, "bold"),
            text_color="white",
            compound="top",
            padx=10,
            pady=10
        )

        self.image_label.place(x=700, y=50)

        self.window.mainloop()


mg = VisualMG()