from tkinter import *
from button_app_V2 import *


class LoginPage:

    def __init__(self, master):

        self.master = master
        self.win_open = True
        # windows bg
        self.login_page_png = ImageTk.PhotoImage(Image.open("Rubikon_png/login_bg.png"))
        self.login_page_canvas = Canvas(self.master, bd=0, highlightthickness=0)
        self.login_page_canvas.place(x=0, y=0, width=1280, height=720)
        self.login_page_canvas.create_image(0, 0, anchor=tk.NW,  image=self.login_page_png)
        # windows settings
        self.master.title("Login")
        self.master.geometry("1280x720+600+300")
        self.master.attributes("-topmost", True)
        self.master.attributes("-alpha", 0.9)
        self.master.overrideredirect(True)
        self.master.attributes("-transparentcolor", '#ffaec8')
        self.master.config(bg="#ffaec8")
        # barre move
        self.move_png = ImageTk.PhotoImage(Image.open("Rubikon_png/move_bar.png"))
        self.move_canvas = Canvas(self.master, bd=0, highlightthickness=0)
        self.move_canvas.place(x=0, y=0, width=1280, height=40)
        self.move_canvas.create_image(0, 0, anchor=tk.NW,  image=self.move_png)
        self.move_canvas.bind("<Button-1>", lambda event: self.logo_button.get_pos(event))
        self.move_canvas.bind("<B1-Motion>", lambda event: self.logo_button.move_window(event))
        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None
        # btn logo
        self.logo_button_canvas = Canvas(self.move_canvas, bd=0, highlightthickness=0)
        self.logo_button = BasicButton(master=self.master, canvas=self.logo_button_canvas,
                                       x=0, y=0, width=40, height=40,
                                       button_name="logo")
        # btn mini
        self.mini_button_canvas = Canvas(self.move_canvas, bd=0, highlightthickness=0)
        self.mini_button = BasicButton(master=self.master, canvas=self.mini_button_canvas,
                                       x=1200, y=0, width=40, height=40,
                                       button_name="mini")
        # btn exit
        self.exit_button_canvas = Canvas(self.move_canvas, bd=0, highlightthickness=0)
        self.exit_button = BasicButton(master=self.master, canvas=self.exit_button_canvas,
                                       x=1240, y=0, width=40, height=40,
                                       button_name="exit")
        self.login()

    def login(self):

        # login zone bg
        self.login_zone_png = ImageTk.PhotoImage(Image.open("Rubikon_png/fond_login.png"))
        self.login_zone_canvas = Canvas(self.master, bd=0, highlightthickness=0)
        self.login_zone_canvas.place(x=460, y=460, width=360, height=230)
        self.login_zone_canvas.create_image(0, 0, anchor=tk.NW,  image=self.login_zone_png)

        # Label pour afficher le message d'erreur du nom d'utilisateur
        self.username_error_label = Label(self.master, text="", bg='#11212d', fg="red")
        self.username_error_label.place(x=490, y=465, width=300, height=20)

        # username entry
        self.username_entry = Entry(self.master, bd=0, bg='#253745', font=('Arial', 16), justify='center', fg='#838B8B')
        self.username_entry.place(x=490, y=490, width=300, height=40)
        self.username_entry.insert(0, "Username")
        self.username_entry.bind("<FocusIn>", self.on_username_entry_focus_in)
        self.username_entry.bind("<FocusOut>", self.on_username_entry_focus_out)
        self.username_entry.bind("<Return>", self.perform_login)

        # password entry
        self.password_entry = Entry(self.master, bd=0, bg='#253745', font=('Arial', 16), show='*', justify='center', fg='#838B8B')
        self.password_entry.place(x=490, y=540, width=300, height=40)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", self.on_password_entry_focus_in)
        self.password_entry.bind("<FocusOut>", self.on_password_entry_focus_out)
        self.password_entry.bind("<Return>", self.perform_login)

        # btn login
        self.login_button_canvas = Canvas(self.master, bd=0, highlightthickness=0)
        self.login_button = SpecialButton(master=self.master, canvas=self.login_button_canvas,
                                        x=550, y=620, width=180, height=40,
                                        button_name="login")
        self.login_button_canvas.bind("<ButtonRelease>", self.perform_login)

    def perform_login(self, event=None):

        username = self.username_entry.get()

        if not username == "1":
            self.username_error_label.config(text="Veuillez saisir un nom d'utilisateur valide", fg="red")
            self.master.after(2000, self.clear_username_error)
            return
        else:
            self.clear_username_error()

        # Vérification du mot de passe
        password = self.password_entry.get()

        if not password == "1":
            self.username_error_label.config(text="Mot de passe incorrect", fg="red")
            self.master.after(2000, self.clear_username_error)
            return
        else:
            self.clear_username_error()

        if username == "1" and password == "1":

            from home_page import HomePage

            self.master.destroy()
            root = tk.Tk()
            HomePage(root)
            root.mainloop()

        else:
            print("Échec de la connexion !")

    def on_username_entry_focus_in(self, event):
        if self.username_entry.get() == "Username":
            self.username_entry.delete(0, END)

    def on_username_entry_focus_out(self, event):
        if not self.username_entry.get():
            self.username_entry.insert(0, "Username")

    def on_password_entry_focus_in(self, event):
        if self.password_entry.get() == "Password":
            self.password_entry.delete(0, END)
            self.password_entry.config(show="*")

    def on_password_entry_focus_out(self, event):
        if not self.password_entry.get():
            self.password_entry.insert(0, "Password")
            self.password_entry.config(show="*")

    def clear_username_error(self):
        self.username_error_label.config(text="")
