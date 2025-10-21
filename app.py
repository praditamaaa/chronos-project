import customtkinter as ctk
from view.main_window import MainWindow
from controller.main_controller import MainController
from config import init_theme

def run_app():
    init_theme()
    root = MainWindow()
    MainController(root)
    root.mainloop()

if __name__ == "__main__":
    run_app()