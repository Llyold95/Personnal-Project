import tkinter as tk
from app_button import *
import wmi
from pystray import MenuItem as Item
from pynput.mouse import Listener, Button
from tkinter import filedialog
from tkinter import ttk
import pystray
import threading
import datetime
import locale
import requests
from io import BytesIO
import pyautogui
import vlc
import time
import random
import os
from pytube import YouTube
import re
import subprocess
import psutil
import py3nvml
from py3nvml.py3nvml import *


wmi = wmi.WMI()
py3nvml.nvidia_smi.nvmlInit()
deviceCount = py3nvml.nvidia_smi.nvmlDeviceGetCount()
rams = wmi.Win32_PhysicalMemory()


class MainApplication(tk.Tk):

    def __init__(self, master):

        super().__init__(master)
        ################################################################################################################
        # main windows settings
        self.master = master
        pos_x = -10
        self.geometry(f"320x1000+{pos_x}+10")
        self.attributes("-topmost", True)
        self.attributes("-alpha", 0.7)
        self.overrideredirect(True)
        self.attributes("-transparentcolor", '#ffaec8')
        self.config(bg="#ffaec8")
        self.title("Rubikon_VX2")
        ################################################################################################################
        self.win_hide = False
        self.win_open = True
        self.listener = None
        self.icon = None
        self.x_win = None
        self.y_win = None
        self.start_x = None
        self.start_y = None
        ################################################################################################################
        # Frame for motion bar, time widget and logo, mini and exit buttons
        self.move_bar_frame = Frame(self.master, bd=0, width=320, height=40, bg="#06141b")
        self.move_bar_frame.place(x=0, y=0, width=320, height=40)
        # Label for Motion bar
        self.move_bar_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/move.png"))
        self.move_bar_label = Label(self.move_bar_frame, width=320, height=40, image=self.move_bar_png)
        self.move_bar_label.place(x=0, y=0, width=320, height=40)
        self.move_bar_label.bind("<Button-1>", lambda event: self.get_pos(event))
        self.move_bar_label.bind("<B1-Motion>", lambda event: self.move_window(event))
        ################################################################################################################
        # Label for exit button
        self.exit_button_label = Label(self.move_bar_frame, bd=0, highlightthickness=0)
        self.exit_button = LabelButton(master=self, label=self.exit_button_label,
                                       x=10, y=0, width=40, height=40,
                                       button_name="exit")
        # Label for mini button
        self.mini_button_label = Label(self.move_bar_frame, bd=0, highlightthickness=0)
        self.mini_button = LabelButton(master=self, label=self.mini_button_label,
                                       x=235, y=0, width=40, height=40,
                                       button_name="mini")
        # Label for logo button
        self.logo_button_label = Label(self.move_bar_frame, bd=0, highlightthickness=0)
        self.logo_button = LabelButton(master=self, label=self.logo_button_label,
                                       x=275, y=0, width=40, height=40,
                                       button_name="logo")
        ################################################################################################################
        # Label for time widget
        self.time_widget_label = Label(self.move_bar_frame, bg='black', fg='#4a5c6a', font=('Arial', 14, 'bold'),
                                       text="00:00")
        self.time_widget_label.place(x=130, y=6, anchor='nw')
        self.time_widget_label.bind("<Button-1>", lambda event: self.get_pos(event))
        self.time_widget_label.bind("<B1-Motion>", lambda event: self.move_window(event))
        ################################################################################################################
        # set locale language and time
        locale.setlocale(locale.LC_TIME, "fr_FR")
        # Frame for date widget
        self.date_widget_frame = Frame(self.master, bd=0, width=80, height=80, bg="#06141b")
        self.date_widget_frame.place(x=10, y=50, width=80, height=80)
        # Label for date widget
        self.date_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/date_bg.png"))
        self.date_widget_label = Label(self.date_widget_frame, width=80, height=80, image=self.date_widget_png)
        self.date_widget_label.place(x=0, y=0, width=80, height=80)
        # Label for date day widget
        self.date_day_label = Label(self.date_widget_frame, bg='#06141b', fg='#afafaf', font=('Arial', 24, 'bold'),
                                    text="00",
                                    justify='center')
        self.date_day_label.place(x=5, y=0, width=70, height=50)
        # Label for date mount widget
        self.date_mon_label = Label(self.date_widget_frame, bg='#06141b', fg='#afafaf', font=('Arial', 14, 'bold'),
                                    text="",
                                    justify='center')
        self.date_mon_label.place(x=5, y=45, width=70, height=25)
        # Launches the update function of the hour, the day and the month every two seconds
        self.time_date_update()
        ################################################################################################################
        # Frame for weather widget
        self.weat_widget_frame = Frame(self.master, bd=0, width=80, height=80, bg="#06141b")
        self.weat_widget_frame.place(x=100, y=50, width=210, height=80)
        # Label for weather widget
        self.weat_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/weather_bg.png"))
        self.weat_widget_label = Label(self.weat_widget_frame, width=210, height=80, image=self.weat_widget_png)
        self.weat_widget_label.place(x=0, y=0, width=210, height=80)
        # Label for weather icon widget
        self.weat_icon_label = Label(self.weat_widget_frame, bg='#06141b', bd=0, highlightthickness=0)
        self.weat_icon_label.place(x=23, y=5, width=70, height=70)
        # Label for weather temperature in Celsius widget
        self.weat_temp_label = Label(self.weat_widget_frame, bg='#06141b', fg='#afafaf', font=('Arial', 14, 'bold'),
                                     text="")
        self.weat_temp_label.place(x=167, y=5, anchor='n')
        # Label for weather description widget
        self.weat_desc_label = Label(self.weat_widget_frame, bg='#06141b', fg='#afafaf', font=('Arial', 9, 'bold'),
                                     text="")
        self.weat_desc_label.place(x=167, y=33, anchor='n')
        # Launches the update of the icon, temperature in Celsius and description of weather every minute
        self.weather_update()
        ################################################################################################################
        # Frame for powertoys tools widget
        self.powe_widget_frame = Frame(self.master, bd=0, width=300, height=40, bg="#06141b")
        self.powe_widget_frame.place(x=10, y=140, width=300, height=40)
        # Label for weather widget
        self.powe_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/tool_bg.png"))
        self.powe_widget_label = Label(self.powe_widget_frame, width=300, height=40, image=self.powe_widget_png)
        self.powe_widget_label.place(x=0, y=0, width=300, height=40)
        # Label for colorpicker button
        self.colo_button_label = Label(self.powe_widget_frame, bd=0, highlightthickness=0)
        self.colo_button = LabelButton(master=self, label=self.colo_button_label,
                                       x=260, y=0, width=40, height=40,
                                       button_name="colorpicker")
        # Label for screenruler button
        self.scre_button_label = Label(self.powe_widget_frame, bd=0, highlightthickness=0)
        self.scre_button = LabelButton(master=self, label=self.scre_button_label,
                                       x=220, y=0, width=40, height=40,
                                       button_name="screenruler")
        ################################################################################################################
        # path music folder
        self.music_folder = "C:/DATA/PROJET_X/Rubikon_png/music_dl"
        # set music status
        self.playing_music = None
        self.audio_choose = None
        self.audio_random = None
        # load media player instance
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()
        # set duration 0 for music timer
        self.duration = 0
        # set title_song "" for music title
        self.title_song = ""

        # Frame for powertoys tools widget
        self.medi_widget_frame = Frame(self.master, bd=0, width=300, height=215, bg="#06141b")
        self.medi_widget_frame.place(x=10, y=185, width=300, height=215)
        # Label for video widget
        self.vide_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/video_player_bg.png"))
        self.vide_widget_label = Label(self.medi_widget_frame, width=300, height=215, image=self.vide_widget_png)
        self.vide_widget_label.bind("<ButtonRelease>", self.pause_music)
        self.vide_widget_label.place(x=0, y=0, width=300, height=215)
        # video canvas for show video from media player
        self.vide_frame = Frame(self.vide_widget_label, bd=0, width=295, height=166, bg="#06141b")
        self.vide_frame.pack_forget()
        # media title label
        self.vide_title_label = Label(self.medi_widget_frame, text="Video Title",
                                      bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                      justify='center')
        self.vide_title_label.place(x=5, y=175, width=245, height=40)
        # media timer label
        self.vide_time_label = Label(self.medi_widget_frame, text="00:00",
                                     bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                     justify='center')
        self.vide_time_label.place(x=250, y=175, width=45, height=40)
        ################################################################################################################
        self.widget_widget_frame = Frame(self.master, bd=0, width=300, height=310, bg="#ffaec8")
        self.widget_widget_frame.place(x=10, y=410, width=300, height=310)
        ################################################################################################################
        # Frame for video button widget
        self.play_widget_frame = Frame(self.widget_widget_frame, bd=0, width=300, height=80, bg="#06141b")
        self.play_widget_frame.place(x=0, y=0, width=300, height=80)
        # Label for video widget
        self.play_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/player_btn_bg.png"))
        self.play_widget_label = Label(self.play_widget_frame, width=300, height=80, image=self.play_widget_png)
        self.play_widget_label.place(x=0, y=0, width=300, height=80)
        # scale volume
        self.volu_scale = Scale(self.play_widget_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                bg="#4a5c6a",  # couleur "canvas" et du bouton
                                fg="#ccd0cf",  # couleur des numéro
                                relief="flat",  # "raised" "sunken" "flat" "ridge" "solid" "groove"
                                showvalue=False,
                                bd=0,
                                width=12,
                                troughcolor="#0b2532",  # couleur du rail
                                activebackground="#00557b",  # couleur du bouton quand actif
                                highlightbackground="#06141b",  # couleur des bordure du canvas
                                highlightcolor="#253745",  # ?
                                sliderrelief="flat", sliderlength=20,
                                command=self.volume_update)
        self.volu_scale.place(x=6, y=12, width=200, height=16)
        # Label for exit button
        self.volu_button_label = Label(self.play_widget_frame, bd=0, highlightthickness=0)
        self.volu_button = LabelButton(master=self, label=self.volu_button_label,
                                       x=215, y=0, width=40, height=40,
                                       button_name="volume")
        # label volume percent
        self.volu_percent = Label(self.play_widget_frame, text="50%",
                                  bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                  justify='center')
        self.volu_percent.place(x=255, y=0, width=40, height=40)
        self.volume_update()
        # btn back
        self.back_button_label = Label(self.play_widget_frame, bd=0, highlightthickness=0)
        self.back_button = LabelButton(master=self, label=self.back_button_label,
                                       x=45, y=40, width=40, height=40,
                                       button_name="back")
        # btn pause / play
        self.paus_play_button_label = Label(self.play_widget_frame, bd=0, highlightthickness=0)
        self.pause_button = LabelButton(master=self, label=self.paus_play_button_label,
                                        x=85, y=40, width=40, height=40,
                                        button_name="play")
        # btn next
        self.next_button_label = Label(self.play_widget_frame, bd=0, highlightthickness=0)
        self.next_button = LabelButton(master=self, label=self.next_button_label,
                                       x=125, y=40, width=40, height=40,
                                       button_name="next")
        # btn stop
        self.stop_button_label = Label(self.play_widget_frame, bd=0, highlightthickness=0)
        self.stop_button = LabelButton(master=self, label=self.stop_button_label,
                                       x=165, y=40, width=40, height=40,
                                       button_name="stop")
        # btn folder
        self.fold_button_label = Label(self.play_widget_frame, bd=0, highlightthickness=0)
        self.fold_button = LabelButton(master=self, label=self.fold_button_label,
                                       x=215, y=40, width=40, height=40,
                                       button_name="folder")
        ################################################################################################################
        self.music_open = False
        # Frame for download button, url entry and percent download label widget
        self.down_widget_frame = Frame(self.widget_widget_frame, bd=0, width=40, height=40, bg="#06141b")
        self.down_widget_frame.place(x=0, y=40, width=40, height=40)
        # Label for download widget
        self.down_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/music_dl.png"))
        self.down_widget_label = Label(self.down_widget_frame, image=self.down_widget_png)
        self.down_widget_label.place(x=0, y=0, width=40, height=40)
        # btn download
        self.down_button_label = Label(self.down_widget_frame, bd=0, highlightthickness=0)
        self.down_button = LabelButton(master=self, label=self.down_button_label,
                                       x=0, y=0, width=40, height=40,
                                       button_name="dl")
        # Entry for url download
        self.url_entry = Entry(self.down_widget_frame, bd=0, bg='#11212d', font=('Arial', 8), justify='center',
                               fg='#ccd0cf')
        self.url_entry.place(x=52, y=4, width=196, height=30)
        self.url_entry.bind("<FocusIn>", self.on_url_entry_focus_in)
        # self.url_entry.bind("<FocusOut>", self.on_url_entry_focus_out)
        self.url_entry.bind("<Return>", self.perform_dl)
        # Label for download percent widget
        self.dl_percent_label = Label(self.down_widget_frame, text="test",
                                      bg='#06141b', fg='#4a5c6a', font=('Arial', 10, 'bold'),
                                      justify='center')
        self.dl_percent_label.place(x=252, y=0, width=45, height=40)
        ################################################################################################################
        self.processors = wmi.Win32_Processor()
        # Frame for setup cpu, url entry and percent download label widget
        self.cpu_widget_frame = Frame(self.widget_widget_frame, bd=0, width=300, height=40, bg="#06141b")
        self.cpu_widget_frame.place(x=0, y=90, width=300, height=40)
        # Label for download widget
        self.cpu_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/tool_bg.png"))
        self.cpu_widget_label = Label(self.cpu_widget_frame, image=self.cpu_widget_png)
        self.cpu_widget_label.place(x=0, y=0, width=300, height=40)
        # label cpu name
        #self.cpu_name_label = Label(self.cpu_widget_frame, text="device name",
                                    #bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'),
                                    #anchor=W)
        #self.cpu_name_label.place(x=5, y=3, width=295, height=40)
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

        self.cpu_load_bar = ttk.Progressbar(self.cpu_widget_frame,
                                            style="Bluec.Horizontal.TProgressbar",
                                            orient="horizontal",
                                            length=170,
                                            mode="determinate",
                                            maximum=100)
        self.cpu_load_bar.place(x=6, y=14, width=200, height=12)
        # label cpu description
        self.cpu_load_text = Label(self.cpu_widget_frame, text=" CPU",
                                   bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'),
                                   justify='center')
        self.cpu_load_text.place(x=215, y=0, width=40, height=40)
        # label cpu load current #06141b
        self.cpu_load_percent = Label(self.cpu_widget_frame, text="100",
                                      bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                      justify='center')
        self.cpu_load_percent.place(x=255, y=0, width=40, height=40)
        self.setup_cpu_update()
        ################################################################################################################
        self.gpu_widget_frame = Frame(self.widget_widget_frame, bd=0, width=300, height=120, bg="#06141b")
        self.gpu_widget_frame.place(x=0, y=140, width=300, height=120)
        # label gpu widget
        self.gpu_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/setup_gpu_bg_v2.png"))
        self.gpu_widget_label = Label(self.gpu_widget_frame, image=self.gpu_widget_png)
        self.gpu_widget_label.place(x=0, y=0, width=300, height=120)
        # label gpu name
        #self.gpu_name_label = Label(self.gpu_widget_frame, text="",
                                    #bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'),
                                    #anchor=W)
        #self.gpu_name_label.place(x=5, y=3, width=295, height=40)
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

        self.gpu_load_bar = ttk.Progressbar(self.gpu_widget_frame,
                                            style="Bluec.Horizontal.TProgressbar",
                                            orient="horizontal",
                                            length=170,
                                            mode="determinate",
                                            maximum=100)
        self.gpu_load_bar.place(x=6, y=14, width=200, height=12)
        # label gpu description
        self.gpu_load_text = Label(self.gpu_widget_frame, text=" GPU",
                                   bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'),
                                   justify='center')
        self.gpu_load_text.place(x=215, y=0, width=40, height=40)
        # label cpu load current
        self.gpu_load_percent = Label(self.gpu_widget_frame, text="100",
                                      bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                      justify='center')
        self.gpu_load_percent.place(x=255, y=0, width=40, height=40)
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

        self.mem_load_bar = ttk.Progressbar(self.gpu_widget_frame,
                                            style="Bluec.Horizontal.TProgressbar",
                                            orient="horizontal",
                                            length=170,
                                            mode="determinate",
                                            maximum=100)
        self.mem_load_bar.place(x=6, y=54, width=200, height=12)
        # label cpu load minimal
        self.mem_load_text = Label(self.gpu_widget_frame, text=" MEM",
                                   bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'),
                                   justify='center')
        self.mem_load_text.place(x=215, y=40, width=40, height=40)
        # label cpu load current
        self.mem_load_percent = Label(self.gpu_widget_frame, text="100",
                                      bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                      justify='center')
        self.mem_load_percent.place(x=255, y=40, width=40, height=40)
        # gpu load progressbar
        style_blue = ttk.Style()
        style_blue.theme_use('alt')
        ttk.Style().configure("Red.Horizontal.TProgressbar",
                              theme_use='alt',
                              thickness=10,
                              borderwidth=0,
                              troughcolor='#0b2532',
                              background="#CD2626",
                              darkcolor="#283747",
                              lightcolor="#283747",
                              bordercolor="#283747",
                              maximum=100,
                              troughrelief='flat')
        ttk.Style().map('Red.Horizontal.TProgressbar')

        self.tem_load_bar = ttk.Progressbar(self.gpu_widget_frame,
                                            style="Red.Horizontal.TProgressbar",
                                            orient="horizontal",
                                            length=170,
                                            mode="determinate",
                                            maximum=100)
        self.tem_load_bar.place(x=6, y=94, width=200, height=12)
        self.tem_load_text = Label(self.gpu_widget_frame, text=" TEM",
                                   bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'),
                                   justify='center')
        self.tem_load_text.place(x=215, y=80, width=40, height=40)

        # label cpu load current
        self.tem_load_percent = Label(self.gpu_widget_frame, text="100",
                                      bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                      justify='center')
        self.tem_load_percent.place(x=255, y=80, width=40, height=40)
        self.setup_gpu_update()
        ################################################################################################################
        self.ram_widget_frame = Frame(self.widget_widget_frame, bd=0, width=300, height=40, bg="#06141b")
        self.ram_widget_frame.place(x=0, y=270, width=300, height=40)
        # label gpu widget
        self.ram_widget_png = ImageTk.PhotoImage(Image.open("Rubikon_VX2/tool_bg.png"))
        self.ram_widget_label = Label(self.ram_widget_frame, image=self.ram_widget_png)
        self.ram_widget_label.place(x=0, y=0, width=300, height=40)
        # label mem name
        #self.ram_name_label = Label(self.ram_widget_frame, text="Virtual Memory",
                                    #bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'),
                                    #anchor=W)
        #self.ram_name_label.place(x=5, y=3, width=295, height=40)
        # mem load progressbar
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

        self.ram_load_bar = ttk.Progressbar(self.ram_widget_frame,
                                            style="Bluec.Horizontal.TProgressbar",
                                            orient="horizontal",
                                            length=170,
                                            mode="determinate",
                                            maximum=100)
        self.ram_load_bar.place(x=6, y=14, width=200, height=12)
        self.ram_load_text = Label(self.ram_widget_frame, text=" RAM",
                                   bg='#06141b', fg='#4a5c6a', font=('Arial', 9, 'bold'),
                                   justify='center')
        self.ram_load_text.place(x=215, y=0, width=40, height=40)

        # label mem load current
        self.ram_load_percent = Label(self.ram_widget_frame, text="100",
                                      bg='#06141b', fg='#ccd0cf', font=('Arial', 10, 'bold'),
                                      justify='center')
        self.ram_load_percent.place(x=255, y=0, width=40, height=40)
        self.setup_ram_update()
        ################################################################################################################

    # Function that returns the position of the pressed click to "move_window"
    def get_pos(self, event):

        self.start_x = event.x_root
        self.start_y = event.y_root
        self.x_win = self.winfo_x()
        self.y_win = self.winfo_y()

    # Function that allows to move the movement bar by modifying the "self.geometry"
    def move_window(self, event):

        self.geometry("+%s+%s" % (event.x_root - self.start_x + self.x_win,
                                  event.y_root - self.start_y + self.y_win))

    # Function to quit the application
    def on_exit(self, *args):

        self.player.stop()
        self.destroy()

    # Function to reduce the application to an icon in the taskbar
    # Also activates a listener which returns the position of the left click to the "on_click" function
    def on_minimize(self, *args):
        self.mini_button.change_state("unclic")
        self.win_open = False
        image = Image.open("Rubikon_VX2/icon_rubikon_32.ico")
        menu = (Item('Open', lambda: self.on_open()),
                Item('Exit', lambda: self.on_exit()))

        self.icon = pystray.Icon("name", image, "Rubikon_VX2", menu)
        self.listener = Listener(on_click=self.on_click)
        self.listener.start()
        self.withdraw()
        self.icon.run()

    # Static function that assigns the zone where you have to click to reopen the application
    @staticmethod
    def check_coordinates(x, y):
        return 2337 <= x <= 2353 and 1404 <= y <= 1437

    # Function that validates the reopening of the application if the conditions are validated
    def on_click(self, x, y, button, pressed):
        if not pressed and button == Button.left:
            if self.check_coordinates(x, y):
                threading.Timer(0.1, self.on_open).start()

    # Function that stops the listener, destroys the taskbar icon and reopens the application
    def on_open(self):

        self.win_open = True
        if hasattr(self, 'listener'):
            self.listener.stop()
        self.icon.stop()
        self.deiconify()

    # Function that serves to reduce the application to the side or re-enlarge it
    def logo_unclic(self, *args):
        self.logo_button.change_state("unclic")

        if self.win_hide is False:
            self.win_hide = True
            self.after(100, self.regress_video)

        elif self.win_hide:
            self.win_hide = False
            self.after(100, self.expand_logo)

    # Function to re-expand the application
    def regress_logo(self):

        current_winfox = int(self.winfo_x())

        if current_winfox >= -225:
            current_winfox -= 5
            self.geometry(f"320x1000+{current_winfox}+10")
            self.after(2, self.regress_logo)

        elif self.winfo_x() >= -225:
            self.after(10, self.expand_video)

    # Function to reduce the application
    def expand_logo(self):

        current_winfox = int(self.winfo_x())

        if current_winfox <= -10:
            current_winfox += 5
            self.geometry(f"320x1000+{current_winfox}+10")
            self.after(2, self.expand_logo)

        elif self.winfo_x() >= -10:
            self.after(10, self.expand_video)

    def expand_video(self):

        current_height_video = int(self.medi_widget_frame.winfo_height())

        a = int(self.medi_widget_frame.winfo_y())
        b = int(self.medi_widget_frame.winfo_height())

        c = 10

        self.widget_widget_frame.place_configure(y=(a + b) + c)

        if current_height_video <= 210:
            current_height_video += 5
            self.medi_widget_frame.place_configure(height=current_height_video)
            self.after(5, self.expand_video)

    # Function to reduce the download widget
    def regress_video(self):

        current_height_video = int(self.medi_widget_frame.winfo_height())

        a = int(self.medi_widget_frame.winfo_y())
        b = int(self.medi_widget_frame.winfo_height())

        c = 0

        self.widget_widget_frame.place_configure(y=(a + b) + c)

        if current_height_video >= 10:

            current_height_video -= 5
            self.medi_widget_frame.place_configure(height=current_height_video)

            self.after(5, self.regress_video)

        elif self.medi_widget_frame.winfo_height() >= 5:

            self.after(5, self.regress_logo)

    # Function to update the time, day and mount
    def time_date_update(self):

        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        self.time_widget_label.config(text=current_time)

        current_day = now.strftime("%d")
        self.date_day_label.config(text=current_day)

        current_mount = now.strftime("%b")
        self.date_mon_label.config(text=current_mount[:4])
        self.after(2000, self.time_date_update)

    # Function to update the icon weather, temperature in Celsius and description of weather
    def weather_update(self):

        api_key = 'YourOpenWeatherMapKey'
        city = "Geneva"
        country_code = "CH"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{country_code}&lang=fr&appid={api_key}"

        try:
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()

                icon_code = data['weather'][0]['icon']
                icon_url = 'http://openweathermap.org/img/wn/{icon}.png'.format(icon=icon_code)
                response = requests.get(icon_url, stream=True)
                image_data = response.content
                image = Image.open(BytesIO(image_data))

                image = image.resize((70, 70))
                self.icon_image = ImageTk.PhotoImage(image)
                self.weat_icon_label.config(image=self.icon_image)

                self.temperature = data['main']['temp']
                self.temperature_int = int(self.temperature)
                self.temperature_celsius = self.temperature - 273.15
                self.weat_temp_label.config(text=f"{self.temperature_celsius:.0f}°C")

                self.weather_description = data['weather'][0]['description']
                description_words = self.weather_description.split()
                if len(description_words) >= 2:
                    first_word = description_words[0]
                    second_word = description_words[1]
                    self.weat_desc_label.config(text=f"{first_word}\n{second_word}")
                else:
                    self.weat_desc_label.config(text=self.weather_description)

            else:
                print("Erreur lors de la récupération des données de météo.")
        except requests.RequestException as e:
            print("Une erreur s'est produite lors de la requête :", e)

        self.after(60000, self.weather_update)

    # Function to start the "ColorPicker" tool of the "PowerToys" application
    @staticmethod
    def colorpicker_unclic():

        pyautogui.keyDown('win')
        pyautogui.keyDown('shift')
        pyautogui.keyDown('c')

        pyautogui.keyUp('win')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('c')

    # Function to start the "ScreenRuler" tool of the "PowerToys" application
    @staticmethod
    def screenruler_unclic():

        pyautogui.keyDown('win')
        pyautogui.keyDown('shift')
        pyautogui.keyDown('m')

        pyautogui.keyUp('win')
        pyautogui.keyUp('shift')
        pyautogui.keyUp('m')

    # Function that updates the media player timer
    def update_time_label(self):

        value = self.player.get_state()

        if self.playing_music:

            if value == vlc.State.Playing:
                current_time = self.player.get_time() // 1000
                formatted_time = time.strftime("%M:%S", time.gmtime(current_time))
                self.vide_title_label.config(text=self.title_song)
                self.vide_time_label.config(text=formatted_time)
                threading.Timer(0.5, self.update_time_label).start()

            elif value == vlc.State.Ended:
                self.load_random_music()
            else:
                pass

    # Function to update the volume of the media player
    def volume_update(self, *args):

        if self.playing_music is None:
            volume = 50
            self.volu_scale.set(volume)
            self.volu_percent.config(text=f"{self.volu_scale.get()}%")
            self.player.audio_set_volume(volume)
        else:
            volume = int(self.volu_scale.get())
            self.volu_percent.config(text=f"{volume}%")

        self.player.audio_set_volume(volume)

    # Function that opens a folder to allow the choice of a media
    def load_music(self, *args):
        self.stop_music()
        self.audio_choose = True

        self.audio_path = filedialog.askopenfilename(initialdir=self.music_folder,
                                                     filetypes=[("Audio files", "*.mp3 *.mp4 *.wav")])

        if self.audio_path:
            self.title_song = os.path.basename(self.audio_path).replace(".mp4", "")

            self.play_music()

    # Function that launches random media from the folder
    def load_random_music(self, *args):
        self.stop_music()
        self.audio_random = True
        self.audio_rdm = [f for f in os.listdir(self.music_folder) if f.endswith(".mp4") or f.endswith(".wav")]

        if self.audio_rdm:
            random_music = random.choice(self.audio_rdm)
            self.title_song = os.path.basename(random_music).replace(".mp4", "")

            self.audio_rdm = os.path.join(self.music_folder, random_music)

            self.play_music()

    # Function that performs media playback
    def play_music(self, *args):

        if self.audio_choose:

            if self.playing_music is None:

                self.playing_music = True
                self.update_button()
                media = self.Instance.media_new(self.audio_path)
                self.duration = media.get_duration() // 1000
                self.player.set_media(media)

                self.vide_frame.pack_forget()
                self.vide_frame.pack(padx=0, pady=5)
                self.player.set_hwnd(self.vide_frame.winfo_id())

                self.player.play()

                threading.Timer(1, self.update_time_label).start()

            elif self.playing_music:

                self.playing_music = True
                self.update_button()
                media = self.Instance.media_new(self.audio_path)
                self.duration = media.get_duration() // 1000
                self.player.set_media(media)

                self.vide_frame.pack_forget()
                self.vide_frame.pack(padx=0, pady=5)
                self.player.set_hwnd(self.vide_frame.winfo_id())

                self.player.play()

                threading.Timer(1, self.update_time_label).start()

        elif self.audio_random:

            self.playing_music = True
            self.update_button()
            media = self.Instance.media_new(self.audio_rdm)
            self.duration = media.get_duration() // 1000
            self.player.set_media(media)

            self.vide_frame.pack_forget()
            self.vide_frame.pack(padx=0, pady=5)
            self.player.set_hwnd(self.vide_frame.winfo_id())

            self.player.play()

            threading.Timer(1, self.update_time_label).start()

    # Function that plays random music if no media is playing, otherwise pauses the media or play
    def pause_music(self, *args):

        if self.playing_music is None:
            self.playing_music = True
            self.update_button()
            self.load_random_music()

        elif self.playing_music:
            self.playing_music = False
            self.update_button()

            self.player.pause()
            threading.Timer(1, self.update_time_label).start()

        else:
            self.playing_music = True
            self.update_button()

            self.player.play()
            threading.Timer(1, self.update_time_label).start()

    # function for stop and reset media
    def stop_music(self, *args):

        self.playing_music = None
        self.update_button()
        self.audio_choose = None
        self.audio_random = None
        self.vide_title_label.config(text="")
        self.vide_time_label.config(text="")
        self.vide_frame.pack_forget()

        self.player.stop()

    # Function that updates the preview of the play/pause button
    def update_button(self):

        self.paus_play_button_label = Label(self.play_widget_frame, bd=0, highlightthickness=0)
        if self.playing_music is None:
            pause_button_name = "play"
        elif self.playing_music is False:
            pause_button_name = "play"
        else:
            pause_button_name = "pause"
        self.pause_button = LabelButton(master=self, label=self.paus_play_button_label,
                                        x=85, y=40, width=40, height=40,
                                        button_name=pause_button_name)

    # Function that serves to reduce the download widget or to resize it
    def music_unclic(self, *args):

        if self.music_open:

            self.music_open = False

            self.after(100, self.regress_music)

        elif self.music_open is False:

            self.music_open = True

            self.after(100, self.expand_music)

    # Function to re-expand the download widget
    def expand_music(self):

        self.dl_percent_label.config(text="")
        current_width_music = int(self.down_widget_frame.winfo_width())

        if current_width_music <= 292:
            current_width_music += 8
            self.down_widget_frame.place_configure(width=current_width_music)
            self.after(10, self.expand_music)

    # Function to reduce the download widget
    def regress_music(self):
        self.url_entry.delete(0, END)
        current_width_music = int(self.down_widget_frame.winfo_width())

        if current_width_music >= 44:
            current_width_music -= 8
            self.down_widget_frame.place_configure(width=current_width_music)
            self.after(10, self.regress_music)

    # Function that clears the entry field when focus in
    def on_url_entry_focus_in(self, event):
        if not self.url_entry.get() == "":
            self.url_entry.delete(0, END)

    # Function that initiates the download
    def perform_dl(self, event=None):

        url = self.url_entry.get()
        youtube = YouTube(url)
        to_dl = url
        self.url_entry.delete(0, END)
        self.url_entry.insert(0, "Initialisation...")
        clean_title = re.sub(r'[<>:"/\\|?*]', '', youtube.title)
        print(clean_title)

        threading.Timer(1, lambda: self.perform_dl_audio(to_dl)).start()

    # Function to update the download percentage
    def download_update(self, stream, chunk, bytes_remaining):

        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100

        self.dl_percent_label.config(text=f"{percentage_of_completion:.0f}%")
        print(percentage_of_completion)
        self.after(10, self.update_interface)
        self.update_idletasks()

    # Function that uses the application to update the percentage of the download
    def update_interface(self):

        self.update_idletasks()

    # Function to download music from url
    def perform_dl_audio(self, to_dl):

        try:
            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Début du téléchargement audio...")

            destination_folder = "C:/DATA/PROJET_X/Rubikon_png/music_dl"

            youtube = YouTube(to_dl, on_progress_callback=self.download_update)

            audio_stream = youtube.streams.filter(file_extension='mp4', progressive=False, only_audio=True).first()
            clean_title = re.sub(r'[<>:"/\\|?*]', '', youtube.title)

            audio_filename = f"{clean_title}_audio.mp4"

            audio_stream.download(output_path=destination_folder, filename=audio_filename)

            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Téléchargement audio terminé !")

        except Exception as e:
            print("An error occurred:", e)

        threading.Timer(1, lambda: self.perform_dl_video(to_dl)).start()

    # Function to download video from url
    def perform_dl_video(self, to_dl):

        try:
            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Début du téléchargement vidéo...")

            destination_folder = "C:/DATA/PROJET_X/Rubikon_png/music_dl"

            youtube = YouTube(to_dl, on_progress_callback=self.download_update)

            video_stream = youtube.streams.filter(file_extension='mp4', progressive=False, only_video=True).first()
            clean_title = re.sub(r'[<>:"/\\|?*]', '', youtube.title)

            video_filename = f"{clean_title}_video.mp4"

            video_stream.download(output_path=destination_folder, filename=video_filename)

            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Téléchargement vidéo terminé !")

        except Exception as e:
            print("An error occurred:", e)

        threading.Timer(1, lambda: self.perform_fusion(clean_title)).start()

    # Function that merges the music with the video after downloading
    def perform_fusion(self, clean_title):

        try:
            self.url_entry.delete(0, END)
            self.url_entry.insert(0, "Début de la Fusion...")

            destination_folder = "C:/DATA/PROJET_X/Rubikon_png/music_dl"

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
            self.url_entry.insert(0, "Fusion terminé !")
            print('Fusion terminé !')

            threading.Timer(3, lambda: self.music_unclic(self)).start()
        except Exception as e:
            print("An error occurred:", e)

    def setup_cpu_update(self):

        cpu_name = self.processors[0].Name
        clean_name = re.sub(r'[(R)TM@<>:"/\\|?*]', '', cpu_name)
        #self.cpu_name_label.config(text=clean_name)

        cpu_percent = psutil.cpu_percent(interval=1)

        self.cpu_load_percent.config(text=f"{cpu_percent:.0f}%")
        self.cpu_load_bar["value"] = cpu_percent

        threading.Timer(0.5, self.setup_cpu_update).start()

    def setup_gpu_update(self):

        for i in range(0, deviceCount):
            handle = py3nvml.nvidia_smi.nvmlDeviceGetHandleByIndex(i)

            # gpu name
            name = py3nvml.nvidia_smi.nvmlDeviceGetName(handle)
            #self.gpu_name_label.config(text=name)
            # gpu current load
            util = py3nvml.nvidia_smi.nvmlDeviceGetUtilizationRates(handle)
            gpu_util = util.gpu

            # update load label %
            self.gpu_load_percent.config(text=f"{gpu_util:.0f}%")
            # update load progressbar
            self.gpu_load_bar["value"] = gpu_util

            # mem current load
            mem_util = util.memory

            # update mem label %
            self.mem_load_percent.config(text=f"{mem_util:.0f}%")
            # update mem progressbar
            self.mem_load_bar["value"] = mem_util

            # tem current load
            tem = nvmlDeviceGetTemperature(handle, NVML_TEMPERATURE_GPU)

            # update tem label %
            self.tem_load_percent.config(text=f"{tem:.0f}°")
            # update tem progressbar
            self.tem_load_bar["value"] = tem

            threading.Timer(0.5, self.setup_gpu_update).start()

    def setup_ram_update(self):

        ram_percent = psutil.virtual_memory().percent

        ram_0 = rams[0].Capacity
        ram_1 = rams[1].Capacity
        ram_0 = int(ram_0)
        ram_1 = int(ram_1)
        total_ram = ram_0 + ram_1
        total_ram = int(total_ram)
        ram_giga = total_ram / (1024 ** 3)
        #self.ram_name_label.config(text=f"Physical Memory (RAM): {ram_giga:.1f} GB")

        self.ram_load_percent.config(text=f"{ram_percent:.0f}%")
        self.ram_load_bar["value"] = ram_percent

        threading.Timer(0.5, self.setup_ram_update).start()


if __name__ == "__main__":
    app = MainApplication(None)
    app.mainloop()
