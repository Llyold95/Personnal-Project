import tkinter as tk
from PIL import Image, ImageTk
from pystray import MenuItem as Item
from pynput.mouse import Listener, Button
import pystray
import threading


class BasicButton:

    def __init__(self, master, canvas, x, y, width, height, button_name):

        self.win_open = True
        self.state = "inactive"
        self.master = master
        self.canvas = canvas
        self.button_name = button_name

        self.get_pos = self.get_pos
        self.on_minimize = self.on_minimize

        self.images = {
            "inactive": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_inactive.png".format(button_name))),
            "active": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_active.png".format(button_name))),
            "clic": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_clic.png".format(button_name))),
            "unclic": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_active.png".format(button_name)))
        }
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.images[self.state])
        self.bind_events()

    def bind_events(self):
        self.canvas.bind("<Enter>", lambda event: self.change_state("active"))
        self.canvas.bind("<Leave>", lambda event: self.change_state("inactive"))
        self.canvas.bind("<ButtonPress>", lambda event: self.change_state("clic"))
        self.canvas.bind("<ButtonRelease>", lambda event: self.change_state("unclic"))

    def change_state(self, new_state):
        self.state = new_state
        self.canvas.itemconfig(self.image_item, image=self.images[self.state])

        if new_state == "unclic":
            if self.button_name == "logo":
                pass
                #self.master.geometry("1280x720+600+300")
            elif self.button_name == "mini":
                self.master.withdraw()
                self.on_minimize()
            elif self.button_name == "exit":
                self.master.destroy()

    def on_minimize(self):

        self.win_open = False
        image = Image.open("Rubikon_png/icon_rubikon_32.ico")
        menu = (Item('Open', lambda: self.on_open()),
                Item('Exit', lambda: self.on_exit()))

        self.icon = pystray.Icon("name", image, "Rubikon_VX1", menu)
        self.listener = Listener(on_click=self.on_click)
        self.listener.start()

        self.icon.run()

    def on_click(self, x, y, button, pressed):
        if not pressed and button == Button.left:
            if self.check_coordinates(x, y):
                threading.Timer(0.1, self.on_open).start()

    @staticmethod
    def check_coordinates(x, y):
        return 2337 <= x <= 2353 and 1404 <= y <= 1437

    def on_open(self):

        self.win_open = True
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.icon.stop()
        self.master.deiconify()

    def on_exit(self):

        self.icon.stop()
        self.master.destroy()

    def get_pos(self, event):

        self.start_x = event.x_root
        self.start_y = event.y_root
        self.x_win = self.master.winfo_x()
        self.y_win = self.master.winfo_y()

    def move_window(self, event):

        self.master.geometry("+%s+%s" % (event.x_root - self.start_x + self.x_win,
                                         event.y_root - self.start_y + self.y_win))


class ReduceButton:

    def __init__(self, master, canvas, x, y, width, height, button_name):

        self.win_open = True
        self.logo_open = False
        self.state = "inactive"
        self.master = master
        self.canvas = canvas
        self.button_name = button_name

        self.get_pos = self.get_pos
        self.on_minimize = self.on_minimize

        self.images = {
            "inactive": ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/{}_inactive.png".format(button_name))),
            "active": ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/{}_active.png".format(button_name))),
            "clic": ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/{}_clic.png".format(button_name))),
            "unclic": ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/{}_active.png".format(button_name)))
        }
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.images[self.state])
        self.bind_events()

    def bind_events(self):
        self.canvas.bind("<Enter>", lambda event: self.change_state("active"))
        self.canvas.bind("<Leave>", lambda event: self.change_state("inactive"))
        self.canvas.bind("<ButtonPress>", lambda event: self.change_state("clic"))
        self.canvas.bind("<ButtonRelease>", lambda event: self.change_state("unclic"))

    def change_state(self, new_state):
        self.state = new_state
        self.canvas.itemconfig(self.image_item, image=self.images[self.state])

        if new_state == "unclic":
            if self.button_name == "logo":
                pass
            elif self.button_name == "mini":
                self.master.withdraw()
                self.on_minimize()
            elif self.button_name == "exit":
                self.master.destroy()

    def on_minimize(self):

        self.win_open = False
        image = Image.open("Rubikon_png/icon_rubikon_32.ico")
        menu = (Item('Open', lambda: self.on_open()),
                Item('Exit', lambda: self.on_exit()))

        self.icon = pystray.Icon("name", image, "Rubikon_VX1", menu)
        self.listener = Listener(on_click=self.on_click)
        self.listener.start()

        self.icon.run()

    def on_click(self, x, y, button, pressed):
        if not pressed and button == Button.left:
            if self.check_coordinates(x, y):
                threading.Timer(0.1, self.on_open).start()

    @staticmethod
    def check_coordinates(x, y):
        return 2337 <= x <= 2353 and 1404 <= y <= 1437

    def on_open(self):

        self.win_open = True
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.icon.stop()
        self.master.deiconify()

    def on_exit(self):

        self.icon.stop()
        self.master.destroy()

    def get_pos(self, event):

        self.start_x = event.x_root
        self.start_y = event.y_root
        self.x_win = self.master.winfo_x()
        self.y_win = self.master.winfo_y()

    def move_window(self, event):

        self.master.geometry("+%s+%s" % (event.x_root - self.start_x + self.x_win,
                                         event.y_root - self.start_y + self.y_win))


class SpecialButton:

    def __init__(self, master, canvas, x, y, width, height, button_name):

        self.win_open = True
        self.state = "inactive"
        self.master = master
        self.canvas = canvas
        self.button_name = button_name

        self.images = {
            "inactive": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_inactive.png".format(button_name))),
            "active": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_active.png".format(button_name))),
            "clic": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_clic.png".format(button_name))),
            "unclic": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_active.png".format(button_name))),
            "on_play": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_active.png".format(button_name))),
            "on_pause": ImageTk.PhotoImage(Image.open("Rubikon_png/{}_active.png".format(button_name)))
        }
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.images[self.state])
        self.bind_events()

    def bind_events(self):
        self.canvas.bind("<Enter>", lambda event: self.change_state("active"))
        self.canvas.bind("<Leave>", lambda event: self.change_state("inactive"))
        self.canvas.bind("<ButtonPress>", lambda event: self.change_state("clic"))

    def change_state(self, new_state):
        self.state = new_state
        self.canvas.itemconfig(self.image_item, image=self.images[self.state])


class ReduceSpecialButton:

    def __init__(self, master, canvas, x, y, width, height, button_name, state):

        self.win_open = True
        self.state = "inactive"
        self.master = master
        self.canvas = canvas
        self.button_name = button_name

        self.images = {
            "inactive": ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/{}_inactive.png".format(button_name))),
            "active": ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/{}_active.png".format(button_name))),
            "clic": ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/{}_clic.png".format(button_name))),
            "unclic": ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/{}_active.png".format(button_name)))
        }
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.image_item = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.images[self.state])
        self.bind_events()

    def bind_events(self):
        self.canvas.bind("<Enter>", lambda event: self.change_state("active"))
        self.canvas.bind("<Leave>", lambda event: self.change_state("inactive"))
        self.canvas.bind("<ButtonPress>", lambda event: self.change_state("clic"))

    def change_state(self, new_state):
        self.state = new_state
        self.canvas.itemconfig(self.image_item, image=self.images[self.state])

    def on_minimize(self):

        self.win_open = False
        image = Image.open("Rubikon_png/icon_rubikon_32.ico")
        menu = (Item('Open', lambda: self.on_open()),
                Item('Exit', lambda: self.on_exit()))

        self.icon = pystray.Icon("name", image, "Rubikon_VX1", menu)
        self.listener = Listener(on_click=self.on_click)
        self.listener.start()

        self.icon.run()

    def on_click(self, x, y, button, pressed):
        if not pressed and button == Button.left:
            if self.check_coordinates(x, y):
                threading.Timer(0.1, self.on_open).start()

    @staticmethod
    def check_coordinates(x, y):
        return 2337 <= x <= 2353 and 1404 <= y <= 1437

    def on_open(self):

        self.win_open = True
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.icon.stop()
        self.master.deiconify()

    def on_exit(self):

        self.icon.stop()
        self.master.destroy()

    def get_pos(self, event):

        self.start_x = event.x_root
        self.start_y = event.y_root
        self.x_win = self.master.winfo_x()
        self.y_win = self.master.winfo_y()

    def move_window(self, event):

        self.master.geometry("+%s+%s" % (event.x_root - self.start_x + self.x_win,
                                         event.y_root - self.start_y + self.y_win))

