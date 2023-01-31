#!C:\Users\wlyne\.EngApps\Scripts\python
import customtkinter as cnt
import subprocess


class MainApp(cnt.CTk):
    def __init__(self) -> None:
        super().__init__()

        # self.geometry("240x600")
        self.title("Menu 2.0.0 2023-01-31")

        cnt.set_default_color_theme("blue")
        cnt.set_appearance_mode("dark")

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


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
