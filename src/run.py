import customtkinter as ctk
from src.model.clickbait import Clickbait
from src.view.mainwindow import MainWindow
from src.controller.appcontroller import AppController


class App:
    def __init__(self):
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        print("Initializing Model...")
        model = Clickbait()

        print("Initializing User Interface...")
        view = MainWindow()

        AppController(model, view)

        print("Application started.")
        view.mainloop()
