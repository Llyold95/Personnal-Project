from tkinter import *
import datetime
import locale
from tkinter import filedialog
from tkinter import ttk
import requests
from io import BytesIO
from pytube import YouTube
import subprocess
import os
import re
import pyautogui
from button_app_V2 import *
import vlc
import time
import random
import psutil
import wmi
import py3nvml
from py3nvml.py3nvml import *


wmi = wmi.WMI()
processors = wmi.Win32_Processor()

py3nvml.nvidia_smi.nvmlInit()
deviceCount = py3nvml.nvidia_smi.nvmlDeviceGetCount()


# color btn
# inactive = bg=#06141b / fg=#4a5c6a
# active = bg=#11212b / fg=#00557b
# clic = bg=#253745 / fg=#00557b


class HomePageReduce:

    def __init__(self, master):

        self.master = master

        self.win_open = False

        # main windows settings
        self.master.title("Reduce Home")
        self.master.geometry("300x1000+5+5")
        self.master.attributes("-topmost", True)
        self.master.attributes("-alpha", 0.8)
        self.master.overrideredirect(True)
        self.master.attributes("-transparentcolor", '#ffaec8')
        self.master.config(bg="#ffaec8")
        # main windows bg
        self.home_page_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/menu_bg.png"))
        self.home_page_canvas = Canvas(self.master, bd=0, highlightthickness=0, bg='#ffaec8')
        self.home_page_canvas.place(x=0, y=0, width=300, height=1000)
        self.home_page_canvas.create_image(0, 0, anchor=tk.NW,  image=self.home_page_png)
        # main barre move
        self.move_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/menu_bg.png"))
        self.move_canvas = Canvas(self.home_page_canvas, bd=0, highlightthickness=0)
        self.move_canvas.place(x=0, y=0, width=300, height=40)
        self.move_canvas.create_image(0, 0, anchor=tk.NW,  image=self.move_png)
        self.move_canvas.bind("<Button-1>", lambda event: self.logo_button.get_pos(event))
        self.move_canvas.bind("<B1-Motion>", lambda event: self.logo_button.move_window(event))
        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None
        # btn logo
        self.logo_button_canvas = Canvas(self.move_canvas, bd=0, highlightthickness=0)
        self.logo_button = ReduceSpecialButton(master=self.master, canvas=self.logo_button_canvas,
                                               x=0, y=0, width=40, height=40,
                                               button_name="logo",
                                               state="inactive")
        self.logo_button_canvas.bind("<ButtonRelease>", self.logo_unclic)
        # btn reduce
        self.reduce_button_canvas = Canvas(self.move_canvas, bd=0, highlightthickness=0)
        self.reduce_button = ReduceButton(master=self.master, canvas=self.reduce_button_canvas,
                                          x=40, y=0, width=40, height=40,
                                          button_name="reduce")
        self.reduce_button_canvas.bind("<ButtonRelease>", self.reduce_unclic)
        # btn mini
        self.mini_button_canvas = Canvas(self.move_canvas, bd=0, highlightthickness=0)
        self.mini_button = ReduceButton(master=self.master, canvas=self.mini_button_canvas,
                                        x=220, y=0, width=40, height=40,
                                        button_name="mini")
        # btn exit
        self.exit_button_canvas = Canvas(self.move_canvas, bd=0, highlightthickness=0)
        self.exit_button = ReduceButton(master=self.master, canvas=self.exit_button_canvas,
                                        x=260, y=0, width=40, height=40,
                                        button_name="exit")

        self.after_on = True
        self.logo_open = False
        self.powertoys_open = True
        self.music_open = False
        self.btn_menu_active = False
        self.callback_id_time = None
        self.callback_id_temperature = None

        locale.setlocale(locale.LC_TIME, "fr_FR")

        self.time()
        self.time_update()

        self.date()
        self.date_update()

        self.weather()
        self.weather_update()

        self.powertoys()

        self.playing_music = None
        self.audio_choose = None
        self.audio_random = None
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        self.player.audio_set_volume(50)

        volume = 50

        self.duration = 0

        self.music_folder = "C:/DATA/PROJET_X/Rubikon_png/music_dl"

        self.music()
        self.btn_music(volume)

        self.setup_cpu()
        self.setup_cpu_update()

        self.setup_gpu()
        self.setup_gpu_update()

    # Fonction pour afficher l'heure
    def time(self):
        # time
        self.time_label = Label(self.master, text="", bg='#06141b', fg='#ccd0cf', font=('Arial', 14, 'bold'))
        self.time_label.place(x=120, y=6, anchor='nw')
        self.time_label.bind("<Button-1>", lambda event: self.logo_button.get_pos(event))
        self.time_label.bind("<B1-Motion>", lambda event: self.logo_button.move_window(event))

    # Fonction pour rafraîchir l'affichage de l'heure
    def time_update(self):

        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")

        self.time_label.config(text=current_time)

        threading.Timer(2, self.time_update).start()

    # Fonction pour afficher la date
    def date(self):
        # date canvas
        self.date_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/date_bg.png"))
        self.date_canvas = Canvas(self.home_page_canvas, bd=0, highlightthickness=0)
        self.date_canvas.place(x=0, y=50, width=80, height=80)
        self.date_canvas.create_image(0, 0, anchor=tk.NW,  image=self.date_png)

        self.date_label_n = Label(self.date_canvas, text="", bg='#06141b', fg='#ccd0cf',
                                  font=('Arial', 24, 'bold'), justify='center')
        self.date_label_n.place(x=5, y=0, width=70, height=50)

        self.date_label_t = Label(self.date_canvas, text="", bg='#06141b', fg='#ccd0cf',
                                  font=('Arial', 14, 'bold'), justify='center')
        self.date_label_t.place(x=5, y=45, width=70, height=25)

    # Fonction pour rafraîchir l'affichage de la date
    def date_update(self):

        now = datetime.datetime.now()

        current_date_n = now.strftime("%d")
        self.date_label_n.config(text=current_date_n)

        current_date_t = now.strftime("%b")
        self.date_label_t.config(text=current_date_t[:4])

        threading.Timer(2, self.date_update).start()

    # Fonction pour afficher l'îcone de la météo, la température et la description
    def weather(self):
        # weather canvas
        self.weather_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/weather_bg.png"))
        self.weather_canvas = Canvas(self.home_page_canvas, bd=0, highlightthickness=0)
        self.weather_canvas.place(x=90, y=50, width=210, height=80)
        self.weather_canvas.create_image(0, 0, anchor=tk.NW,  image=self.weather_png)

        self.weather_icon_canvas = Canvas(self.weather_canvas, bg='#06141b', bd=0, highlightthickness=0)
        self.weather_icon_canvas.place(x=23, y=5, width=70, height=70)

        self.weather_temp_label = Label(self.weather_canvas, text="", bg='#06141b', fg='#ccd0cf',
                                       font=('Arial', 14, 'bold'))
        self.weather_temp_label.place(x=160, y=5, anchor='n')

        self.weather_desc_label = Label(self.weather_canvas, text="", bg='#06141b', fg='#ccd0cf',
                                       font=('Arial', 10, 'bold'))
        self.weather_desc_label.place(x=160, y=33, anchor='n')

    # Fonction pour rafraîchir l'affichage des widget de la météo
    def weather_update(self):

        api_key = 'YourWeatherApiKey'
        city = "Geneva"
        country_code = "CH"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&lang=fr&appid={api_key}"

        try:
            self.response = requests.get(url)

            if self.response.status_code == 200:
                self.data = self.response.json()

                self.icon_code = self.data['weather'][0]['icon']
                self.icon_url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=self.icon_code)
                self.response = requests.get(self.icon_url, stream=True)
                self.image_data = self.response.content
                self.image = Image.open(BytesIO(self.image_data))

                self.image = self.image.resize((70, 70))
                self.icon_image = ImageTk.PhotoImage(self.image)
                self.weather_icon_canvas.create_image(0, 0, anchor=tk.NW, image=self.icon_image)

                self.temperature = self.data['main']['temp']
                self.temperature_int = int(self.temperature)
                self.temperature_celsius = self.temperature - 273.15
                self.weather_temp_label.config(text=f"{self.temperature_celsius:.0f}°C")

                self.weather_description = self.data['weather'][0]['description']
                description_words = self.weather_description.split()
                if len(description_words) >= 2:
                    first_word = description_words[0]
                    second_word = description_words[1]
                    self.weather_desc_label.config(text=f"{first_word}\n{second_word}")
                else:
                    self.weather_desc_label.config(text=self.weather_description)

            else:
                print("Erreur lors de la récupération des données de météo.")
        except requests.RequestException as e:
            print("Une erreur s'est produite lors de la requête :", e)

        threading.Timer(60, self.weather_update).start()

    def powertoys(self):
        # powertoys canvas
        self.powertoys_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/tool_bg.png"))
        self.canvas_powertoys_bg = Canvas(self.home_page_canvas, bd=0, highlightthickness=0)
        self.canvas_powertoys_bg.place(x=0, y=140, width=300, height=40)
        self.canvas_powertoys_bg.create_image(0, 0, anchor=tk.NW,  image=self.powertoys_png)
        # btn powertoys
        self.powertoys_button_canvas = Canvas(self.canvas_powertoys_bg, bd=0, highlightthickness=0)
        self.powertoys_button = ReduceSpecialButton(master=self.master, canvas=self.powertoys_button_canvas,
                                                    x=0, y=0, width=40, height=40,
                                                    button_name="PowerToys",
                                                    state="inactive")
        self.powertoys_button_canvas.bind("<ButtonRelease>", self.powertoys_unclic)
        # btn colorpicker
        self.colorpicker_button_canvas = Canvas(self.canvas_powertoys_bg, bd=0, highlightthickness=0)
        self.colorpicker_button = ReduceSpecialButton(master=self.master, canvas=self.colorpicker_button_canvas,
                                                      x=43, y=0, width=40, height=40,
                                                      button_name="ColorPicker",
                                                      state="inactive")
        self.colorpicker_button_canvas.bind("<ButtonRelease>", self.colorpicker_unclic)
        # btn screenruler
        self.screenruler_button_canvas = Canvas(self.canvas_powertoys_bg, bd=0, highlightthickness=0)
        self.screenruler_button = ReduceSpecialButton(master=self.master, canvas=self.screenruler_button_canvas,
                                                      x=83, y=0, width=40, height=40,
                                                      button_name="ScreenRuler",
                                                      state="inactive")
        self.screenruler_button_canvas.bind("<ButtonRelease>", self.screenruler_unclic)

    # Fonction pour afficher la vidéo du MusicPlayer
    def music(self):


        self.volume_scale = self.player.audio_set_volume(50)

        # music canvas
        self.music_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/video_player_bg.png"))
        self.music_canvas = Canvas(self.home_page_canvas, bd=0, highlightthickness=0)
        self.music_canvas.place(x=0, y=190, width=300, height=210)
        self.music_canvas.create_image(0, 0, anchor=tk.NW,  image=self.music_png)

        # video canvas
        self.video_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/video_off.png"))
        self.video_canvas = Canvas(self.music_canvas, bd=0, highlightthickness=0)
        self.video_canvas.place(x=3, y=3, width=294, height=164)
        self.video_canvas.create_image(0, 0, anchor=tk.NW,  image=self.video_png)
        self.video_canvas.bind("<ButtonRelease>", self.pause_music)

        self.video_label = LabelFrame(self.video_canvas, bd=0, width=70, height=70, bg="#06141b")
        self.video_label.place_forget()
        self.video_label.bind("<ButtonRelease>", self.pause_music)

        self.video_title_label = Label(self.music_canvas, text="",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'))
        self.video_title_label.place(x=5, y=170, width=250, height=40)

        self.video_time_label = Label(self.music_canvas, text="",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.video_time_label.place(x=250, y=170, width=45, height=40)

        # player btn canvas
        self.player_btn_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/player_btn_bg.png"))
        self.player_btn_canvas = Canvas(self.home_page_canvas, bd=0, highlightthickness=0)
        self.player_btn_canvas.place(x=0, y=410, width=300, height=80)
        self.player_btn_canvas.create_image(0, 0, anchor=tk.NW,  image=self.player_btn_png)
        pass

    def btn_music(self, volume):

        # btn volume
        self.volume_button_canvas = Canvas(self.player_btn_canvas, bd=0, highlightthickness=0)
        self.volume_button = ReduceSpecialButton(master=self.master, canvas=self.volume_button_canvas,
                                                 x=0, y=0, width=40, height=40,
                                                 button_name="volume",
                                                 state="inactive")

        # scale volume
        self.volume_scale = Scale(self.player_btn_canvas, from_=0, to=100, orient=tk.HORIZONTAL,
                                  bg="#4a5c6a", # couleur "canvas" et du bouton
                                  fg="#ccd0cf", # couleur des numéro
                                  relief="flat", # "raised" "sunken" "flat" "ridge" "solid" "groove"
                                  showvalue="0",
                                  bd=0,
                                  width=12,
                                  troughcolor="#0b2532", #couleur du rail
                                  activebackground="#00557b", # couleur du bouton quand actif
                                  highlightbackground="#06141b", # couleur des bordure du canvas
                                  highlightcolor="#253745", # ?
                                  sliderrelief="flat", sliderlength=20)
        self.volume_scale.place(x=50, y=12, width=200, height=16)

        self.volume_scale.set(volume)

        # label volume percent
        self.volume_percent = Label(self.player_btn_canvas, text="50%",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.volume_percent.place(x=255, y=0, width=40, height=40)

        # btn folder
        self.folder_button_canvas = Canvas(self.player_btn_canvas, bd=0, highlightthickness=0)
        self.folder_button = ReduceSpecialButton(master=self.master, canvas=self.folder_button_canvas,
                                                 x=45, y=40, width=40, height=40,
                                                 button_name="folder",
                                                 state="inactive")
        self.folder_button_canvas.bind("<ButtonRelease>", self.load_music)

        # btn back
        self.back_button_canvas = Canvas(self.player_btn_canvas, bd=0, highlightthickness=0)
        self.back_button = ReduceSpecialButton(master=self.master, canvas=self.back_button_canvas,
                                               x=90, y=40, width=40, height=40,
                                               button_name="back",
                                               state="inactive")

        # btn pause / play
        self.pause_play_button_canvas = Canvas(self.player_btn_canvas, bd=0, highlightthickness=0)

        if self.playing_music is None:
            pause_button_name = "play"
        elif self.playing_music is False:
            pause_button_name = "play"
        else:
            pause_button_name = "pause"

        self.pause_button = ReduceSpecialButton(master=self.master, canvas=self.pause_play_button_canvas,
                                                x=130, y=40, width=40, height=40,
                                                button_name=pause_button_name,
                                                state="inactive")
        self.pause_play_button_canvas.bind("<ButtonRelease>", self.pause_music)

        # btn next
        self.next_button_canvas = Canvas(self.player_btn_canvas, bd=0, highlightthickness=0)
        self.next_button = ReduceSpecialButton(master=self.master, canvas=self.next_button_canvas,
                                               x=170, y=40, width=40, height=40,
                                               button_name="next",
                                               state="inactive")
        self.next_button_canvas.bind("<ButtonRelease>", self.on_music_end)

        # btn stop
        self.stop_button_canvas = Canvas(self.player_btn_canvas, bd=0, highlightthickness=0)
        self.stop_button = ReduceSpecialButton(master=self.master, canvas=self.stop_button_canvas,
                                               x=215, y=40, width=40, height=40,
                                               button_name="stop",
                                               state="inactive")
        self.stop_button_canvas.bind("<ButtonRelease>", self.stop_music)

        # download canvas
        self.music_dl_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/music_dl.png"))
        self.music_dl_canvas = Canvas(self.player_btn_canvas, bd=0, highlightthickness=0)
        self.music_dl_canvas.place(x=0, y=40, width=40, height=40)
        self.music_dl_canvas.create_image(0, 0, anchor=tk.NW,  image=self.music_dl_png)

        # btn download
        self.music_button_canvas = Canvas(self.music_dl_canvas, bd=0, highlightthickness=0)
        self.music_button = ReduceSpecialButton(master=self.master, canvas=self.music_button_canvas,
                                                x=0, y=0, width=40, height=40,
                                                button_name="dl",
                                                state="inactive")
        self.music_button_canvas.bind("<ButtonRelease>", self.music_unclic)

        # url download
        self.url_entry = Entry(self.music_dl_canvas, bd=0, bg='#11212d', font=('Arial', 10), justify='center',
                               fg='#ccd0cf')
        self.url_entry.place(x=47, y=4, width=248, height=32)

        self.url_entry.bind("<FocusIn>", self.on_url_entry_focus_in)
        # self.url_entry.bind("<FocusOut>", self.on_url_entry_focus_out)
        self.url_entry.bind("<Return>", self.perform_dl)

    def setup_cpu(self):


        # setup canvas
        self.cpu_setup_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/setup_bg.png"))
        self.cpu_setup_canvas = Canvas(self.home_page_canvas, bd=0, highlightthickness=0)
        self.cpu_setup_canvas.place(x=0, y=500, width=300, height=120)
        self.cpu_setup_canvas.create_image(0, 0, anchor=tk.NW,  image=self.cpu_setup_png)
        # label cpu name
        self.cpu_name_label = Label(self.cpu_setup_canvas, text="device name",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'))
        self.cpu_name_label.place(x=5, y=3, width=295, height=40)
        # btn cpu
        self.cpu_button_canvas = Canvas(self.cpu_setup_canvas, bd=0, highlightthickness=0)
        self.cpu_button = ReduceSpecialButton(master=self.master, canvas=self.cpu_button_canvas,
                                                 x=0, y=40, width=40, height=40,
                                                 button_name="cpu",
                                                 state="inactive")
        # cpu load progressbar
        style_blue = ttk.Style()
        style_blue.theme_use('alt')
        ttk.Style().configure("Bluec.Horizontal.TProgressbar",
                              theme_use='alt',
                              thickness=10,
                              borderwidth=0,
                              troughcolor='#0b2532',
                              background="#10bce7",
                              darkcolor="#283747",
                              lightcolor="#283747",
                              bordercolor="#283747",
                              maximum=100,
                              troughrelief='flat')
        ttk.Style().map('Bluec.Horizontal.TProgressbar')

        self.cpu_load_bar = ttk.Progressbar(self.cpu_setup_canvas,
                                           style="Bluec.Horizontal.TProgressbar",
                                           orient="horizontal",
                                           length=170,
                                           mode="determinate",
                                           maximum=100)
        self.cpu_load_bar.place(x=50, y=54, width=200, height=12)
        # label cpu load current
        self.cpu_load_percent = Label(self.cpu_setup_canvas, text="100",
                                    bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.cpu_load_percent.place(x=255, y=40, width=40, height=40)
        # label cpu load minimal
        self.cpu_min_percent = Label(self.cpu_setup_canvas, text="min",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.cpu_min_percent.place(x=5, y=80, width=90, height=40)
        # label cpu load average
        self.cpu_avg_percent = Label(self.cpu_setup_canvas, text="avg",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.cpu_avg_percent.place(x=105, y=80, width=91, height=40)
        # label cpu load maximal
        self.cpu_max_percent = Label(self.cpu_setup_canvas, text="max",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.cpu_max_percent.place(x=206, y=80, width=90, height=40)

        self.cpu_percent_list = []

    def setup_cpu_update(self):

        cpu_name = processors[0].Name

        self.cpu_name_label.config(text=cpu_name)

        cpu_percent = psutil.cpu_percent(interval=1)
        self.cpu_percent_list.append(cpu_percent)

        min_percent = min(self.cpu_percent_list)
        avg_percent = sum(self.cpu_percent_list) / len(self.cpu_percent_list)
        max_percent = max(self.cpu_percent_list)

        self.cpu_load_percent.config(text=f"{cpu_percent:.1f}%")
        self.cpu_load_bar["value"] = cpu_percent

        self.cpu_min_percent.config(text=f"Min: {min_percent:.1f}%")
        self.cpu_avg_percent.config(text=f"Avg: {avg_percent:.1f}%")
        self.cpu_max_percent.config(text=f"Max: {max_percent:.1f}%")

        threading.Timer(0.5, self.setup_cpu_update).start()

    def setup_gpu(self):

        # setup canvas
        self.gpu_setup_png = ImageTk.PhotoImage(Image.open("Rubikon_png/reduce_mode/setup_gpu_bg.png"))
        self.gpu_setup_canvas = Canvas(self.home_page_canvas, bd=0, highlightthickness=0)
        self.gpu_setup_canvas.place(x=0, y=630, width=300, height=280)
        self.gpu_setup_canvas.create_image(0, 0, anchor=tk.NW,  image=self.gpu_setup_png)
        # label gpu name
        self.gpu_name_label = Label(self.gpu_setup_canvas, text="",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'))
        self.gpu_name_label.place(x=5, y=3, width=295, height=40)
        # btn gpu
        self.gpu_button_canvas = Canvas(self.gpu_setup_canvas, bd=0, highlightthickness=0)
        self.gpu_button = ReduceSpecialButton(master=self.master, canvas=self.gpu_button_canvas,
                                                 x=0, y=40, width=40, height=40,
                                                 button_name="cpu",
                                                 state="inactive")
        # gpu load progressbar
        style_blue = ttk.Style()
        style_blue.theme_use('alt')
        ttk.Style().configure("Bluec.Horizontal.TProgressbar",
                              theme_use='alt',
                              thickness=10,
                              borderwidth=0,
                              troughcolor='#0b2532',
                              background="#10bce7",
                              darkcolor="#283747",
                              lightcolor="#283747",
                              bordercolor="#283747",
                              maximum=100,
                              troughrelief='flat')
        ttk.Style().map('Bluec.Horizontal.TProgressbar')

        self.gpu_load_bar = ttk.Progressbar(self.gpu_setup_canvas,
                                           style="Bluec.Horizontal.TProgressbar",
                                           orient="horizontal",
                                           length=170,
                                           mode="determinate",
                                           maximum=100)
        self.gpu_load_bar.place(x=50, y=54, width=200, height=12)
        # label cpu load current
        self.gpu_load_percent = Label(self.gpu_setup_canvas, text="100",
                                    bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.gpu_load_percent.place(x=255, y=40, width=40, height=40)
        # label cpu load minimal
        self.gpu_min_percent = Label(self.gpu_setup_canvas, text="min",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.gpu_min_percent.place(x=5, y=80, width=90, height=40)
        # label cpu load average
        self.gpu_avg_percent = Label(self.gpu_setup_canvas, text="avg",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.gpu_avg_percent.place(x=105, y=80, width=91, height=40)
        # label cpu load maximal
        self.gpu_max_percent = Label(self.gpu_setup_canvas, text="max",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.gpu_max_percent.place(x=206, y=80, width=90, height=40)

        self.gpu_percent_list = []

        # btn gpu
        self.mem_button_canvas = Canvas(self.gpu_setup_canvas, bd=0, highlightthickness=0)
        self.mem_button = ReduceSpecialButton(master=self.master, canvas=self.mem_button_canvas,
                                                 x=0, y=120, width=40, height=40,
                                                 button_name="cpu",
                                                 state="inactive")
        # gpu load progressbar
        style_blue = ttk.Style()
        style_blue.theme_use('alt')
        ttk.Style().configure("Bluec.Horizontal.TProgressbar",
                              theme_use='alt',
                              thickness=10,
                              borderwidth=0,
                              troughcolor='#0b2532',
                              background="#10bce7",
                              darkcolor="#283747",
                              lightcolor="#283747",
                              bordercolor="#283747",
                              maximum=100,
                              troughrelief='flat')
        ttk.Style().map('Bluec.Horizontal.TProgressbar')

        self.mem_load_bar = ttk.Progressbar(self.gpu_setup_canvas,
                                           style="Bluec.Horizontal.TProgressbar",
                                           orient="horizontal",
                                           length=170,
                                           mode="determinate",
                                           maximum=100)
        self.mem_load_bar.place(x=50, y=134, width=200, height=12)
        # label cpu load current
        self.mem_load_percent = Label(self.gpu_setup_canvas, text="100",
                                    bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.mem_load_percent.place(x=255, y=120, width=40, height=40)
        # label cpu load minimal
        self.mem_min_percent = Label(self.gpu_setup_canvas, text="min",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.mem_min_percent.place(x=5, y=160, width=90, height=40)
        # label cpu load average
        self.mem_avg_percent = Label(self.gpu_setup_canvas, text="avg",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.mem_avg_percent.place(x=105, y=160, width=91, height=40)
        # label cpu load maximal
        self.mem_max_percent = Label(self.gpu_setup_canvas, text="max",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.mem_max_percent.place(x=206, y=160, width=90, height=40)

        self.mem_percent_list = []

        # btn gpu
        self.tem_button_canvas = Canvas(self.gpu_setup_canvas, bd=0, highlightthickness=0)
        self.tem_button = ReduceSpecialButton(master=self.master, canvas=self.tem_button_canvas,
                                                 x=0, y=200, width=40, height=40,
                                                 button_name="cpu",
                                                 state="inactive")
        # gpu load progressbar
        style_blue = ttk.Style()
        style_blue.theme_use('alt')
        ttk.Style().configure("Red.Horizontal.TProgressbar",
                              theme_use='alt',
                              thickness=10,
                              borderwidth=0,
                              troughcolor='#173750',
                              background="#CD2626",
                              darkcolor="#283747",
                              lightcolor="#283747",
                              bordercolor="#283747",
                              maximum=100,
                              troughrelief='flat')
        ttk.Style().map('Red.Horizontal.TProgressbar')

        self.tem_load_bar = ttk.Progressbar(self.gpu_setup_canvas,
                                           style="Red.Horizontal.TProgressbar",
                                           orient="horizontal",
                                           length=170,
                                           mode="determinate",
                                           maximum=100)
        self.tem_load_bar.place(x=50, y=214, width=200, height=12)
        # label cpu load current
        self.tem_load_percent = Label(self.gpu_setup_canvas, text="100",
                                    bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.tem_load_percent.place(x=255, y=200, width=40, height=40)
        # label cpu load minimal
        self.tem_min_percent = Label(self.gpu_setup_canvas, text="min",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.tem_min_percent.place(x=5, y=240, width=90, height=40)
        # label cpu load average
        self.tem_avg_percent = Label(self.gpu_setup_canvas, text="avg",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.tem_avg_percent.place(x=105, y=240, width=91, height=40)
        # label cpu load maximal
        self.tem_max_percent = Label(self.gpu_setup_canvas, text="max",
                                    bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                    justify='center')
        self.tem_max_percent.place(x=206, y=240, width=90, height=40)

        self.tem_percent_list = []

    def setup_gpu_update(self):

        for i in range(0, deviceCount):
            handle = py3nvml.nvidia_smi.nvmlDeviceGetHandleByIndex(i)
            pci_info = py3nvml.nvidia_smi.nvmlDeviceGetPciInfo(handle)
            brand_names = {NVML_BRAND_UNKNOWN: "Unknown",
                           NVML_BRAND_QUADRO: "Quadro",
                           NVML_BRAND_TESLA: "Tesla",
                           NVML_BRAND_NVS: "NVS",
                           NVML_BRAND_GRID: "Grid",
                           NVML_BRAND_GEFORCE: "GeForce",
                           }
            # gpu name
            name = py3nvml.nvidia_smi.nvmlDeviceGetName(handle)
            self.gpu_name_label.config(text=name)
            # gpu current load
            util = py3nvml.nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
            gpu_util = util.gpu

            self.gpu_percent_list.append(gpu_util)

            gpu_min_percent = min(self.gpu_percent_list)
            gpu_avg_percent = sum(self.gpu_percent_list) / len(self.gpu_percent_list)
            gpu_max_percent = max(self.gpu_percent_list)

            # update load label %
            self.gpu_load_percent.config(text=f"{gpu_util:.1f}%")
            # update load progressbar
            self.gpu_load_bar["value"] = gpu_util

            self.gpu_min_percent.config(text=f"Min: {gpu_min_percent:.1f}%")
            self.gpu_avg_percent.config(text=f"Avg: {gpu_avg_percent:.1f}%")
            self.gpu_max_percent.config(text=f"Max: {gpu_max_percent:.1f}%")

            # mem current load
            mem_util = util.memory

            self.mem_percent_list.append(mem_util)

            mem_min_percent = min(self.mem_percent_list)
            mem_avg_percent = sum(self.mem_percent_list) / len(self.mem_percent_list)
            mem_max_percent = max(self.mem_percent_list)

            # update mem label %
            self.mem_load_percent.config(text=f"{mem_util:.1f}%")
            # update mem progressbar
            self.mem_load_bar["value"] = mem_util

            self.mem_min_percent.config(text=f"Min: {mem_min_percent:.1f}%")
            self.mem_avg_percent.config(text=f"Avg: {mem_avg_percent:.1f}%")
            self.mem_max_percent.config(text=f"Max: {mem_max_percent:.1f}%")

            # tem current load
            tem = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)

            self.tem_percent_list.append(tem)

            tem_min_percent = min(self.tem_percent_list)
            tem_avg_percent = sum(self.tem_percent_list) / len(self.tem_percent_list)
            tem_max_percent = max(self.tem_percent_list)

            # update tem label %
            self.tem_load_percent.config(text=f"{tem:.1f}%")
            # update tem progressbar
            self.tem_load_bar["value"] = tem

            self.tem_min_percent.config(text=f"Min: {tem_min_percent:.1f}%")
            self.tem_avg_percent.config(text=f"Avg: {tem_avg_percent:.1f}%")
            self.tem_max_percent.config(text=f"Max: {tem_max_percent:.1f}%")

            threading.Timer(0.5, self.setup_gpu_update).start()

    def load_music(self, args):
        self.stop_music(self)
        self.audio_choose = True
        self.audio_path = filedialog.askopenfilename(initialdir=self.music_folder,
                                                     filetypes=[("Audio files", "*.mp3 *.mp4 *.wav")])

        if self.audio_path:
            title_song = os.path.basename(self.audio_path).replace(".mp4", "")
            self.video_title_label.config(text=title_song)
            print(title_song)

            self.play_music(args)

    def play_random_music(self, args):
        self.stop_music(self)
        self.audio_random = True
        self.audio_rdm = [f for f in os.listdir(self.music_folder) if f.endswith(".mp4") or f.endswith(".wav")]

        if self.audio_rdm:
            random_music = random.choice(self.audio_rdm)
            title_song = os.path.basename(random_music).replace(".mp4", "")
            self.audio_rdm = os.path.join(self.music_folder, random_music)

            self.video_title_label.config(text=title_song)
            print(title_song)

            self.play_music(args)

    def on_music_end(self, args):

        self.video_title_label.config(text="")
        self.video_time_label.config(text="")
        self.video_label.place_forget()

        self.playing_music = None
        self.play_random_music(args)

    def play_music(self, args):

        if self.audio_choose:

            if self.playing_music is None:
                print('play choose')
                self.playing_music = True
                volume = self.volume_scale.get()
                self.btn_music(volume=volume)
                media = self.Instance.media_new(self.audio_path)
                self.duration = media.get_duration() // 1000
                self.player.set_media(media)

                self.video_label.place_forget()
                self.video_label.place(x=0, y=0, width=295, height=166)
                self.player.set_hwnd(self.video_label.winfo_id())

                self.player.play()
                threading.Timer(1, self.update_time_label).start()

            elif self.playing_music:
                print('play new choose')
                self.playing_music = True
                volume = self.volume_scale.get()
                self.btn_music(volume=volume)
                media = self.Instance.media_new(self.audio_path)
                self.duration = media.get_duration() // 1000
                self.player.set_media(media)

                self.video_label.place_forget()
                self.video_label.place(x=0, y=0, width=295, height=166)
                self.player.set_hwnd(self.video_label.winfo_id())

                self.player.play()
                threading.Timer(1, self.update_time_label).start()

        elif self.audio_random:
            print('play random')
            self.playing_music = True
            volume = self.volume_scale.get()
            self.btn_music(volume=volume)

            media = self.Instance.media_new(self.audio_rdm)
            self.duration = media.get_duration() // 1000
            self.player.set_media(media)

            self.video_label.place_forget()
            self.video_label.place(x=0, y=0, width=295, height=166)
            self.video_label.bind("<ButtonRelease>", self.pause_music)
            self.player.set_hwnd(self.video_label.winfo_id())

            self.player.play()

            threading.Timer(1, self.update_time_label).start()
            volumethread = threading.Thread(target=self.refreshvolume, daemon=True)
            volumethread.start()

    def update_time_label(self):

        value = self.player.get_state()

        if self.playing_music:

            if value == vlc.State.Playing:

                current_time = self.player.get_time() // 1000
                formatted_time = time.strftime("%M:%S", time.gmtime(current_time))
                self.video_time_label.config(text=formatted_time)
                threading.Timer(0.5, self.update_time_label).start()

            elif value == vlc.State.Ended:
                self.play_random_music(self)
            else:
                pass

    def refreshvolume(self):

        if self.playing_music:

            while True:
                self.set_volume(self.volume_scale.get())
                time.sleep(0.1)

    def set_volume(self, volume_scale):

        if self.playing_music:

            self.player.audio_set_volume(volume_scale)
            self.volume_percent.config(text=f"{volume_scale}%")

    def pause_music(self, args):

        if self.playing_music is None:
            self.play_random_music(args)

        elif self.playing_music:
            print("On Pause")
            self.playing_music = False
            self.btn_music(volume=50)
            self.player.pause()
            threading.Timer(1, self.update_time_label).start()
            #threading.Timer(1, self.set_volume).start()
        else:
            print("On Play")
            self.playing_music = True
            self.btn_music(volume=50)
            self.player.play()
            threading.Timer(1, self.update_time_label).start()
            #threading.Timer(1, self.set_volume).start()

    def stop_music(self, args):

        self.playing_music = None
        self.audio_choose = None
        self.audio_random = None
        self.video_title_label.config(text="")
        self.video_time_label.config(text="")
        self.video_label.place_forget()
        self.player.stop()
        self.btn_music(volume=50)

    def on_progress(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100

        #self.url_entry.delete(0, END)
        #self.url_entry.insert(0, f" {percentage_of_completion:.0f}%")

        self.master.after(1, self.update_interface)
        self.master.update_idletasks()

    def update_interface(self):
        self.master.update_idletasks()

    def perform_dl(self, event=None):

        url = self.url_entry.get()
        youtube = YouTube(url)
        to_dl = url
        self.url_entry.delete(0, END)
        self.url_entry.insert(0, "Initialisation...")
        clean_title = re.sub(r'[<>:"/\\|?*]', '', youtube.title)
        print(clean_title)

        threading.Timer(2, lambda: self.perform_dl_audio(to_dl)).start()

    def perform_dl_audio(self, to_dl):

        try:
            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Début du téléchargement audio...")

            destination_folder = "C:\DATA\PROJET_X\Rubikon_png\music_dl"

            youtube = YouTube(to_dl)
            #youtube.register_on_progress_callback(self.on_progress)

            clean_title = re.sub(r'[<>:"/\\|?*]', '', youtube.title)

            audio_stream = youtube.streams.filter(file_extension='mp4', progressive=False, only_audio=True).first()
            audio_filename = f"{clean_title}_audio.mp4"

            audio_stream.download(output_path=destination_folder, filename=audio_filename)

            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Téléchargement audio terminé !")

        except Exception as e:
            print("An error occurred:", e)

        threading.Timer(2, lambda: self.perform_dl_video(to_dl)).start()

    def perform_dl_video(self, to_dl):

        try:
            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Début du téléchargement vidéo...")

            destination_folder = "C:\DATA\PROJET_X\Rubikon_png\music_dl"

            youtube = YouTube(to_dl)
            #youtube.register_on_progress_callback(self.on_progress)

            clean_title = re.sub(r'[<>:"/\\|?*]', '', youtube.title)

            video_stream = youtube.streams.filter(file_extension='mp4', progressive=False, only_video=True).first()
            video_filename = f"{clean_title}_video.mp4"

            video_stream.download(output_path=destination_folder, filename=video_filename)

            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Téléchargement vidéo terminé !")

        except Exception as e:
            print("An error occurred:", e)

        threading.Timer(2, lambda: self.perform_fusion(clean_title)).start()

    def perform_fusion(self, clean_title):

        try:
            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Début de la Fusion...")

            destination_folder = "C:\DATA\PROJET_X\Rubikon_png\music_dl"

            video_filename = f"{clean_title}_video.mp4"
            video_path = os.path.join(destination_folder, video_filename)

            audio_filename = f"{clean_title}_audio.mp4"
            audio_path = os.path.join(destination_folder, audio_filename)

            merged_filename = f"{clean_title}.mp4"
            merged_path = os.path.join(destination_folder, merged_filename)

            cmd = [
                "C:/Program Files/ffmpeg-6.0-essentials_build/ffmpeg-6.0-essentials_build/bin/ffmpeg.exe",
                "-i", video_path,
                "-i", audio_path,
                "-c:v", "copy",
                "-c:a", "aac",
                merged_path
            ]
            directory_path = "C:/DATA/PROJET_X/Rubikon_png/music_dl/info_music_dl/"

            output_file = open(f"{directory_path}{clean_title}_ffmpeg.txt", "w")
            subprocess.run(cmd, stdout=output_file, stderr=output_file)
            output_file.close()

            if os.path.exists(video_path):
                os.remove(video_path)
            if os.path.exists(audio_path):
                os.remove(audio_path)

            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Fusion terminée !")

        except Exception as e:
            print("An error occurred:", e)

    def on_url_entry_focus_in(self, event):
        if not self.url_entry.get() == "":
            self.url_entry.delete(0, END)

    def on_url_entry_focus_out(self, event):
        if not self.url_entry.get():
            self.url_entry.insert(0, "")

    def stop_updates(self):
        if self.callback_id_time is not None:
            self.master.after_cancel(self.callback_id_time)
            self.callback_id_time = None

    def reduce_unclic(self, args):
        from home_page import HomePage

        self.stop_updates()
        self.master.destroy()
        root = tk.Tk()
        HomePage(root)
        root.mainloop()

    def logo_unclic(self, event):
        self.logo_button.change_state("unclic")

        if self.logo_open:
            self.logo_open = False
            self.master.after(100, self.regress_logo)

        elif self.logo_open is False:
            self.logo_open = True
            self.master.after(100, self.expand_logo)

    def expand_logo(self):
        current_height_logo = int(self.home_page_canvas.winfo_height())

        if current_height_logo <= 180:
            current_height_logo += 5
            self.home_page_canvas.place_configure(height=current_height_logo)
            self.master.after(2, self.expand_logo)

    def regress_logo(self):
        current_height_logo = int(self.home_page_canvas.winfo_height())

        if current_height_logo >= 45:
            current_height_logo -= 5
            self.home_page_canvas.place_configure(height=current_height_logo)
            self.master.after(2, self.regress_logo)

    def powertoys_unclic(self, event):
        self.powertoys_button.change_state("unclic")

        if self.powertoys_open:
            self.powertoys_open = False
            self.master.after(100, self.regress_power)

        elif self.powertoys_open is False:
            self.powertoys_open = True
            self.master.after(100, self.expand_power)

    def expand_power(self):
        current_width_power = int(self.canvas_powertoys_bg.winfo_width())

        if current_width_power <= 296:
            current_width_power += 4
            self.canvas_powertoys_bg.place_configure(width=current_width_power)
            self.master.after(2, self.expand_power)

    def regress_power(self):
        current_width_power = int(self.canvas_powertoys_bg.winfo_width())

        if current_width_power >= 44:
            current_width_power -= 4
            self.canvas_powertoys_bg.place_configure(width=current_width_power)
            self.master.after(2, self.regress_power)

    def music_unclic(self, event):
        self.music_button.change_state("unclic")

        if self.music_open:

            self.music_open = False

            self.master.after(100, self.regress_music)

        elif self.music_open is False:

            self.music_open = True

            self.master.after(100, self.expand_music)

    def expand_music(self):
        current_width_music = int(self.music_dl_canvas.winfo_width())

        if current_width_music <= 320:
            current_width_music += 8
            self.music_dl_canvas.place_configure(width=current_width_music)
            self.master.after(2, self.expand_music)

    def regress_music(self):
        self.url_entry.delete(0, END)
        current_width_music = int(self.music_dl_canvas.winfo_width())

        if current_width_music >= 44:
            current_width_music -= 8
            self.music_dl_canvas.place_configure(width=current_width_music)
            self.master.after(2, self.regress_music)

    def colorpicker_unclic(self, args):
        self.colorpicker_button.change_state("unclic")

        pyautogui.keyDown('win')
        pyautogui.keyDown('shift')
        pyautogui.keyDown('c')

        pyautogui.keyUp('win')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('c')

    def screenruler_unclic(self, args):
        self.screenruler_button.change_state("unclic")

        pyautogui.keyDown('win')
        pyautogui.keyDown('shift')
        pyautogui.keyDown('m')

        pyautogui.keyUp('win')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('m')

