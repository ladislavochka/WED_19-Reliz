import customtkinter as ctk
from pygame import mixer
from PIL import Image

mixer.init()

app = ctk.CTk()
app.title("Filine")
app.geometry("1300x800")

center_frame = ctk.CTkFrame(app, fg_color="transparent")
center_frame.pack(expand=True)
th_label = ctk.CTkLabel(center_frame, text="")
th_label.pack(expand=True)

def three():
    try:
        trhe = Image.open("WED_19-Reliz/Vlad/CU.png")
        trhe_image = ctk.CTkImage(light_image=trhe, dark_image=trhe,size=(500, 500))
        th_label.configure(image=trhe_image)
        th_label.image = trhe_image
        mixer.music.load("WED_19-Reliz/Vlad/Sounds/Cult_Member_-_three_(SkySound7.com).mp3")
        mixer.music.play()
    except:
        pass

def RAC():
    try:
        RA = Image.open("WED_19-Reliz/Vlad/WO.png")
        RA_image = ctk.CTkImage(light_image=RA, dark_image=RA, size=(500, 500))
        th_label.configure(image=RA_image)
        th_label.image = RA_image
        mixer.music.load("WED_19-Reliz/Vlad/Sounds/SEMATARY - RAGING WOLF.mp3")
        mixer.music.play()
    except:
        pass

def magic():
    try:
        mag = Image.open("WED_19-Reliz/Vlad/IK.png")
        mag_image = ctk.CTkImage(light_image=mag, dark_image=mag, size=(500, 500))
        th_label.configure(image=mag_image)
        th_label.image = mag_image
        mixer.music.load("WED_19-Reliz/Vlad/Sounds/Medasin-magic-spaces.im.mp3")
        mixer.music.play()
    except:
        pass

def pause_music():
    mixer.music.pause()
    th_label.configure(image="")  # Убираем картинку с экрана
    th_label.image = None


# ---ПЛЕЙЛІСТ (ФРЕЙМ)---
playlist = ctk.CTkFrame(app, width=300, corner_radius=0)
playlist.pack(side="left", fill="y")

title_name = ctk.CTkLabel(playlist, text="Filine", font=("Arial", 30, "bold"))
title_name.pack(padx=20, pady=20, anchor="w")


#------PIP IMAGE------
photo_frame = ctk.CTkFrame(app, width=300, corner_radius=0)
photo_frame.pack(side="right", fill="y")

filine_avatar = Image.open("WED_19-Reliz/Vlad/filine.jpg")

my_image = ctk.CTkImage(light_image=filine_avatar,dark_image=filine_avatar,size=(300, 300))

photo_avatar_label = ctk.CTkLabel(photo_frame, image=my_image, text="")
photo_avatar_label.pack(padx=20, pady=10, anchor="w")

#------ПЛЕЙЛІСТ(КНОПКИ)------

cult = ctk.CTkButton(playlist, text="Three-Cult_Member", width=200, command=three)
cult.pack(padx=20, pady=10, anchor="w")

wolf = ctk.CTkButton(playlist, text="SEMATARY - RAGING WOLF", width=200, command=RAC)
wolf.pack(padx=20, pady=10, anchor="w")

magik = ctk.CTkButton(playlist, text="Medasin-magic", width=200, command=magic)
magik.pack(padx=20, pady=10, anchor="w")

#--------КНОПКА ПАУЗА--------

button_area = ctk.CTkFrame(app, fg_color="transparent")
button_area.pack(side="right", fill="both", padx=20, pady=20)

knopka_frame = ctk.CTkFrame(button_area, fg_color="transparent")
knopka_frame.pack(side="bottom", fill="x", pady=20)

pause_button = ctk.CTkButton(knopka_frame, text="⏸ Стоп", width=150, command=pause_music)
pause_button.pack(side="left", padx=10)

app.mainloop()