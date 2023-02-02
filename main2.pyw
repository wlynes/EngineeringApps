#!C:\Users\wlyne\.EngApps\Scripts\python
import customtkinter as cnt
import subprocess
from datetime import datetime
import time
from typing import *


class MainApp(cnt.CTk):
    def __init__(self) -> None:
        super().__init__()

        # self.geometry("240x600")
        self.title("Menu 2.0.0 2023-01-31")

        cnt.set_default_color_theme("blue")
        cnt.set_appearance_mode("dark")

        tdf = TimeAndDateFrame(master=self).pack(fill="x", padx=2, pady=2)

        hl = HorizLine(master=self).pack(fill="x", padx=2, pady=2)

        button1 = cnt.CTkButton(master=self, font=("Consolas", 24), text="f.eet\' to ft'-in\"",
                                command=lambda: self.button_click("FeetInches2.py")).pack(fill="both", padx=2, pady=2)
        button2 = cnt.CTkButton(master=self, font=(
            "Consolas", 24), text="AISC Shapes Lookup", command=lambda: self.button_click("aisclookup2.py")).pack(fill="both", padx=2, pady=2)
        button3 = cnt.CTkButton(master=self, font=(
            "Consolas", 24), text="Lookup AISC Shape by Property", command=lambda: self.button_click("aiscbyproperty.py")).pack(fill="both", padx=2, pady=2)
        button5 = cnt.CTkButton(master=self, font=(
            "Consolas", 24), text="Unit Converter", command=lambda: self.button_click("unitconverter2.py")).pack(fill="both", padx=2, pady=2)

    def button_click(self, script):
        subprocess.Popen(["pythonw", script])


class TimeAndDateFrame(cnt.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None, border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent", fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None, background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None, overwrite_preferred_drawing_method: Union[str, None] = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color,
                         border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.current_date = datetime.today().strftime("%A, %Y-%m-%d")
        self.label2 = cnt.CTkLabel(self, font=(
            "Consolas", 24, "italic"), justify="center", text_color="#1F6AA5")
        self.label2.pack(fill="both", expand=True)
        self.update_time()

    def update_time(self):
        current_time = time.strftime("%H:%M:%S")
        self.label2.configure(text="{} {}".format(
            self.current_date, current_time))
        self.label2.after(1000, self.update_time)


class HorizLine(cnt.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 2, corner_radius: Optional[Union[int, str]] = None, border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "#dce4ee", fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None, background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None, overwrite_preferred_drawing_method: Union[str, None] = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color,
                         border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.configure(fg_color="#1F6AA5",
                       border_color="#1F6AA5",
                       bg_color="#1F6AA5")


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
