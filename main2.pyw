#!C:\Users\wlyne\.EngApps\Scripts\python
import customtkinter as cnt
import subprocess
import sys
from os import path, pardir
import FeetInches2

class MainApp(cnt.CTk):
    def __init__(self) -> None:
        super().__init__()

        # Set a path to the virtual environment
        current_file = path.abspath(__file__)
        self.cwd = path.abspath(path.join(current_file, pardir))
        self.py_path = path.abspath(path.join(current_file, pardir, pardir, "Scripts", "python.exe"))
            
        self.geometry("300x600")
        self.title("Menu 2.0.0 2023-01-27")

        cnt.set_default_color_theme("blue")
        cnt.set_appearance_mode("dark")

        button1 = cnt.CTkButton(master = self, font=("Consolas", 18), text="f.eet\' to ft'-in\"", command=lambda: self.button_click("FeetInches2.py")).pack(fill="both", padx=2, pady=2)
        button2 = cnt.CTkButton(master = self, font=("Consolas", 18), text="AISC Shapes Lookup").pack(fill="both", padx=2, pady=2)
        button3 = cnt.CTkButton(master = self, font=("Consolas", 18), text="Lookup AISC Shape by Property").pack(fill="both", padx=2, pady=2)
        button4 = cnt.CTkButton(master = self, font=("Consolas", 18), text="AISC Shapes Lookup").pack(fill="both", padx=2, pady=2)
        button5 = cnt.CTkButton(master = self, font=("Consolas", 18), text="Unit Converter").pack(fill="both", padx=2, pady=2)

    def button_click(self, script):
        scr = path.abspath(path.join(self.cwd, script))
        subprocess.run([self.py_path, scr])

        



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()


