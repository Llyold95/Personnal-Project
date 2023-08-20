from io import BytesIO
from tkinter import *
import datetime
import requests
import locale
from button_app_V2 import *


class HomePage:

    def __init__(self, master):

        self.master = master
        self.win_open = True
        # windows bg
        self.home_page_png = ImageTk.PhotoImage(Image.open("Rubikon_png/home_bg.png"))
        self.home_page_canvas = Canvas(self.master, bd=0, highlightthickness=0)
        self.home_page_canvas.place(x=0, y=0, width=1280, height=720)
        self.home_page_canvas.create_image(0, 0, anchor=tk.NW,  image=self.home_page_png)
        # windows settings
        self.master.title("Home")
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
        # btn reduce
        self.reduce_button_canvas = Canvas(self.move_canvas, bd=0, highlightthickness=0)
        self.reduce_button = SpecialButton(master=self.master, canvas=self.reduce_button_canvas,
                                        x=40, y=0, width=40, height=40,
                                        button_name="reduce")
        self.reduce_button_canvas.bind("<ButtonRelease>", self.reduce_unclic)
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

        self.home()
        locale.setlocale(locale.LC_TIME, "fr_FR")
        self.update_time()
        self.update_temperature()

    def home(self):

        # page menu principale
        self.main_menu_png = ImageTk.PhotoImage(Image.open("Rubikon_png/menu_principale_fond.png"))
        self.canvas_main_menu = Canvas(self.master, bg='#11212d', bd=0, highlightthickness=0)
        self.canvas_main_menu.place(x=0, y=40, width=300, height=680)
        self.canvas_main_menu.create_image(0, 0, anchor=tk.NW, image=self.main_menu_png)

        # menu date et heure et température
        self.date_label = Label(self.master, text="", bg='#06141b', fg='#ccd0cf', font=('Arial', 14, 'bold'))
        self.date_label.place(x=850, y=6, anchor='nw')
        self.date_label.bind("<Button-1>", lambda event: self.logo_button.get_pos(event))
        self.date_label.bind("<B1-Motion>", lambda event: self.logo_button.move_window(event))

        self.time_label = Label(self.master, text="", bg='#06141b', fg='#ccd0cf', font=('Arial', 14, 'bold'))
        self.time_label.place(x=120, y=6, anchor='nw')
        self.time_label.bind("<Button-1>", lambda event: self.logo_button.get_pos(event))
        self.time_label.bind("<B1-Motion>", lambda event: self.logo_button.move_window(event))

        self.temperature_label = Label(self.master, text="", bg='#06141b', fg='#ccd0cf',
                                       font=('Arial', 14, 'bold'))
        self.temperature_label.place(x=1095, y=6, anchor='n')
        self.temperature_label.bind("<Button-1>", lambda event: self.logo_button.get_pos(event))
        self.temperature_label.bind("<B1-Motion>", lambda event: self.logo_button.move_window(event))

        # icone météo
        self.canvas_meteo_png = Canvas(self.master, bg='#06141b', bd=0, highlightthickness=0)
        self.canvas_meteo_png.place(x=1110, y=0, width=40, height=40)
        self.canvas_meteo_png.bind("<Button-1>", lambda event: self.logo_button.get_pos(event))
        self.canvas_meteo_png.bind("<B1-Motion>", lambda event: self.logo_button.move_window(event))

    def start_updates(self):

        self.callback_id_time = self.master.after(1000, self.update_time)
        self.callback_id_temperature = self.master.after(1000, self.update_temperature)

    def stop_updates(self):

        if self.callback_id_time is not None:
            self.master.after_cancel(self.callback_id_time)
            self.callback_id_time = None

        if self.callback_id_temperature is not None:
            self.master.after_cancel(self.callback_id_temperature)
            self.callback_id_temperature = None

    def reduce_unclic(self, args):

        from home_page_reduce import HomePageReduce

        self.stop_updates()
        self.master.destroy()
        root = tk.Tk()
        HomePageReduce(root)
        root.mainloop()

    def update_time(self):

        now = datetime.datetime.now()
        current_date = now.strftime("%A %d %B %Y")
        current_time = now.strftime("%H:%M")

        self.date_label.config(text=current_date)
        self.time_label.config(text=current_time)
        self.callback_id_time = self.master.after(1000, self.update_time)

    def update_temperature(self):

        api_key = 'c51b77924149bad4a69badb05ecc681c'

        city = "Geneva"
        country_code = "CH"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&appid={api_key}"

        try:

            self.response = requests.get(url)

            if self.response.status_code == 200:

                self.data = self.response.json()
                self.temperature = self.data['main']['temp']
                self.temperature_int = int(self.temperature)
                self.temperature_celsius = self.temperature - 273.15
                self.temperature_label.config(text=f"{self.temperature_celsius:.0f}°")

                self.icon_code = self.data['weather'][0]['icon']
                self.icon_url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=self.icon_code)
                self.response = requests.get(self.icon_url, stream=True)
                self.image_data = self.response.content
                self.image = Image.open(BytesIO(self.image_data))

                self.image = self.image.resize((40, 40))
                self.icon_image = ImageTk.PhotoImage(self.image)

                self.canvas_meteo_png.create_image(0, 0, anchor=tk.NW, image=self.icon_image)

            else:
                print("Erreur lors de la récupération des données de météo.")
        except requests.RequestException as e:
            print("Une erreur s'est produite lors de la requête :", e)

        self.callback_id_temperature = self.master.after(30000, self.update_temperature)

