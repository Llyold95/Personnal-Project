import tkinter as tk
from login_page import LoginPage
from home_page import HomePage
from home_page_reduce import HomePageReduce

def start_app():

    start_home_page_reduce()


def start_login_page():

    root = tk.Tk()
    LoginPage(root)
    root.mainloop()


def start_home_page():

    root = tk.Tk()
    HomePage(root)
    root.mainloop()


def start_home_page_reduce():
    root = tk.Tk()
    HomePageReduce(root)
    root.mainloop()


if __name__ == "__main__":

    start_app()
