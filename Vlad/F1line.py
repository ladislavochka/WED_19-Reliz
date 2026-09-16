import customtkinter as ctk

app = ctk.CTk()
app.title("Filine")
app.geometry("1300x800")

# Заголовок
title_name = ctk.CTkLabel(app, text="Filine", font=("arial", 30))
title_name.pack(anchor="e", padx=20, pady=20)

#!!ВСЯ КООРДИНАТА Х ОТ НАЧАЛА ДО КОНЦА ОКНА ПО ОСИ У ОТ СЛАЙДЕРА ДО КНОПОК
knopki_frame = ctk.CTkFrame(app, fg_color="transparent")

knopki_frame.pack(side="bottom", fill="x", pady=40)

#!!ПЛАТФОРМА В КОТОРОЙ КНОПКИ БЕЗ СЛАЙДЕРА!!
buttons_frame = ctk.CTkFrame(knopki_frame, fg_color="transparent")
buttons_frame.pack(pady=10)


remote_button = ctk.CTkButton(buttons_frame, text="Минулий трек", width=120)
remote_button.pack(side="left", padx=10)

play_button = ctk.CTkButton(buttons_frame, text="▶Почати", width=80)
play_button.pack(side="left", padx=10)

pause_button = ctk.CTkButton(buttons_frame, text="⏸Пауза", width=80)
pause_button.pack(side="left", padx=10)

rewind_button = ctk.CTkButton(buttons_frame, text="Наступний трек", width=120)
rewind_button.pack(side="left", padx=10)

playlist = ctk.CTkFrame(app, fg_color="transparent")
playlist.pack()
playlist.place(relwidth=0.5, relheight=1)
cult = ctk.CTkButton(playlist, text="Three-Cult_Member", width=175)
cult.pack(anchor="w",pady=45)
wolf = ctk.CTkButton(playlist, text="SEMATARY - RAGING WOLF", width=150)
wolf.pack(anchor="w",pady=45)
magik = ctk.CTkButton(playlist, text="Medasin-magic", width=175)
magik.pack(anchor="w",pady=45)









app.mainloop()