from tkinter import *
from tkinter.font import BOLD
from PIL import Image, ImageTk
import pygame
from game import game
import webbrowser

class __gui__(Tk):

    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        pygame.mixer.music.load("Sounds/first_music.mp3")
        pygame.mixer.music.play(-1)
        self.back_color = "#01527a"
        self.title("Snake Game By Prathamesh Dhande")
        self.geometry("700x353")
        self.resizable(False, False)
        self.iconbitmap("Images/icon_gui.ico")
        self.gif_file = Image.open("Images/game_start_animation.gif")
        self.frames = self.gif_file.n_frames
        self.count = 0
        self.im = [PhotoImage(file="Images/game_start_animation.gif",
                              format=f"gif -index {i}") for i in range(self.frames)]
        self.anim = None
        self.configure(background=self.back_color)
        # threading.Thread(target=self.p_gui).start()
        self.p_gui()
        self.is_music_set = False
        self.is_gmusic_set = False
        self.mvalue = IntVar()
        self.mvalue.set(1)
        self.gvalue = IntVar()
        self.gvalue.set(1)
        self.m_volume = IntVar()
        self.g_volume = IntVar()
        self.m_volume.set(7)
        self.g_volume.set(7)
        self.gv = 7
        self.gm = 7
        self.fps = 0

    def p_gui(self):
        self.gif_label = Label(self, image="", background=self.back_color)
        self.gif_label.place(x=5, y=5)
        self.animation()
        Label(self, text="Game Made By Prathamesh Dhande", font=("Times New Roman", 12),
              background=self.back_color, foreground="White").place(x=5, y=330)
        self.img1 = Image.open("Images/play.png").resize(size=(140, 50))
        self.img2 = Image.open("Images/exit.png").resize(size=(70, 70))
        self.img3 = Image.open("Images/github.png").resize(size=(40, 40))
        self.img4 = Image.open("Images/setting.png").resize(size=(50, 50))
        self.img1 = ImageTk.PhotoImage(image=self.img1)
        self.img2 = ImageTk.PhotoImage(image=self.img2)
        self.img3 = ImageTk.PhotoImage(image=self.img3)
        self.img4 = ImageTk.PhotoImage(image=self.img4)
        Button(self, image=self.img1, background=self.back_color, activebackground=self.back_color,
               relief="flat", command=self.set_difficulty_level).place(x=525, y=30)
        Button(self, image=self.img2, background=self.back_color, activebackground=self.back_color,
               relief="flat", command=self.destroy).place(x=560, y=190)
        Button(self, image=self.img3, background=self.back_color, activebackground=self.back_color, relief="flat",
               command=lambda: webbrowser.open_new_tab("https://github.com/PrathameshDhande22/Snake-Game-in-Pygame.git")).place(x=650, y=305)
        Button(self, image=self.img4, background=self.back_color, activebackground=self.back_color,
               command=self.setting, relief="flat").place(x=570, y=110)

    def setting(self):
        self.img5 = Image.open("Images/back_btn.png").resize(size=(40, 30))
        self.img5 = ImageTk.PhotoImage(image=self.img5)
        self.setting_frame = Frame(
            self, background="White", width=200, height=353)
        self.setting_frame.place(x=500, y=0)
        Button(self.setting_frame, image=self.img5, relief="ridge", background="white",
               command=lambda: self.setting_frame.place_forget(), activebackground="White").place(x=5, y=5)
        Label(self.setting_frame, text="Settings", background="White",
              font=("Calibri", 19, BOLD)).place(x=70, y=2)

        self.music_btn = Checkbutton(self.setting_frame, text="Background Music", variable=self.mvalue, font=(
            "Times New Roman", 14), background="White")
        self.music_btn.place(x=10, y=60)

        Label(self.setting_frame, text="Set the Music Volume",
              font="Calibri 10", background="white", border=0).place(x=10, y=88)
        Label(self.setting_frame, text="Set the Game Volume",
              font="Calibri 10", background="white", border=0).place(x=10, y=198)

        self.game_btn = Checkbutton(self.setting_frame, text="Game Music", variable=self.gvalue, font=(
            "Times New Roman", 14), background="White")
        self.game_btn.place(x=10, y=170)

        self.music_volume = Scale(self.setting_frame, variable=self.m_volume, from_=0, to=10, border=0,
                                  orient="horizontal", background='white', font=("Calibri", 10), tickinterval=1, length=180)
        self.music_volume.place(x=10, y=106)

        self.game_volume = Scale(self.setting_frame, from_=0, to=10, border=0, variable=self.g_volume,
                                 orient="horizontal", background='white', font=("Calibri", 10), tickinterval=1, length=180)
        self.game_volume.place(x=10, y=215)

        self.music_btn.bind("<Button-1>", self.set_music)
        self.game_btn.bind("<Button-1>", self.set_game_music)
        self.game_volume.bind("<Button-1>", self.set_game_volume)
        self.music_volume.bind("<Button-1>", self.set_game_volume)

    def set_music(self, event):
        if self.mvalue.get() == 1:
            pygame.mixer.music.stop()
            self.is_music_set = True

        elif self.mvalue.get() == 0:
            self.is_music_set = False
            pygame.mixer.init()
            pygame.mixer.music.load("Sounds/first_music.mp3")
            pygame.mixer.music.play(-1)

    def set_game_music(self, event):
        if self.gvalue.get() == 1:
            self.is_gmusic_set = True
        elif self.gvalue.get() == 0:
            self.is_gmusic_set = False

    def play_game(self, fps):
        self.destroy()
        pygame.mixer.music.stop()
        c = game(self.is_music_set, self.is_gmusic_set, self.gv, self.gm, fps)

    def animation(self):
        im2 = self.im[self.count]
        self.gif_label.configure(image=im2)
        self.count += 1
        if self.count == self.frames:
            self.count = 0
        self.anim = self.after(35, self.animation)

    def set_game_volume(self, event):
        self.gv = self.game_volume.get()
        self.gm = self.music_volume.get()

    def set_difficulty_level(self):
        self.difficulty_frame = Frame(
            self, background=self.back_color, width=200, height=353)
        self.difficulty_frame.place(x=500, y=0)

        self.img5 = Image.open("Images/back_btn.png").resize(size=(40, 30))
        self.img5 = ImageTk.PhotoImage(image=self.img5)
        Button(self.difficulty_frame, image=self.img5, relief="raised", background="yellow",
               command=lambda: self.difficulty_frame.place_forget(), activebackground=self.back_color).place(x=5, y=5)

        Label(self.difficulty_frame, text="Set The Difficulty Level", font=(
            "Lucida Bright", 12, BOLD), background=self.back_color, foreground="white").place(x=3, y=50)

        Button(self.difficulty_frame, text="EASY", background="Yellow", font=("Arial Black", 15),
               activebackground="Red", relief="groove", bd=3, width=9, command=lambda: self.play_game(30)).place(x=30, y=100)
        Button(self.difficulty_frame, text="MEDIUM", background="Yellow", font=("Arial Black", 15),
               activebackground="Red", relief="groove", bd=3, width=9, command=lambda: self.play_game(60)).place(x=30, y=170)
        Button(self.difficulty_frame, text="HARD", background="Yellow", font=("Arial Black", 15),
               activebackground="Red", relief="groove", bd=3, width=9, command=lambda: self.play_game(70)).place(x=30, y=240)


if __name__ == "__main__":
    b = __gui__()
    b.mainloop()
