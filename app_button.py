from tkinter import *
from PIL import Image, ImageTk


class LabelButton:

    def __init__(self, x, y, width, height, button_name, master, label):

        self.win_open = True
        self.state = "inactive"

        self.master = master
        self.button_name = button_name
        self.images = {
            "inactive": ImageTk.PhotoImage(Image.open("Rubikon_VX2/{}_inactive.png".format(button_name))),
            "active": ImageTk.PhotoImage(Image.open("Rubikon_VX2/{}_active.png".format(button_name))),
            "clic": ImageTk.PhotoImage(Image.open("Rubikon_VX2/{}_clic.png".format(button_name))),
            "unclic": ImageTk.PhotoImage(Image.open("Rubikon_VX2/{}_active.png".format(button_name)))
        }

        self.label = label
        self.label.configure(image=self.images[self.state])
        self.label.place(x=x, y=y, width=width, height=height)
        self.bind_events()

    def bind_events(self):
        self.label.bind("<Enter>", lambda event: self.change_state("active"))
        self.label.bind("<Leave>", lambda event: self.change_state("inactive"))
        self.label.bind("<ButtonPress>", lambda event: self.change_state("clic"))
        self.label.bind("<ButtonRelease>", self.on_button_release)

    def on_button_release(self, event):

        self.change_state("unclic")

        button_functions = {
            "exit": self.master.on_exit,
            "mini": self.master.on_minimize,
            "logo": self.master.logo_unclic,
            "colorpicker": self.master.colorpicker_unclic,
            "screenruler": self.master.screenruler_unclic,
            "folder": self.master.load_music,
            "back": self.master.load_random_music,
            "play": self.master.pause_music,
            "pause": self.master.pause_music,
            "next": self.master.load_random_music,
            "stop": self.master.stop_music,
            "dl": self.master.music_unclic,
        }

        if self.button_name in button_functions:
            self.master.after(50, button_functions[self.button_name])

    def change_state(self, new_state):
        self.state = new_state
        self.label.configure(image=self.images[self.state])
