import customtkinter as ctk
from typing import *
from random import random
import re


class App(ctk.CTk):
    def __init__(self, fg_color: Optional[Union[str, Tuple[str, str]]] = None, **kwargs):
        super().__init__(fg_color, **kwargs)

        self.title("VDOT Feet and Inches Converter")
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")
        self.iconbitmap(r"images\Will-High.ico")

        tabs = TabHolder(self).pack()


class TabHolder(ctk.CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tab1 = self.add("Decimal ft -> ft\'-in.ches\"")
        self.tab2 = self.add("ft\'-in.ches\" -> Decimal ft")

        self.tab1_entry = ctk.StringVar(value="{:8f}".format(10. * random()))
        self.tab1_result = ctk.StringVar()

        self.tab2_entry = ctk.StringVar()
        self.tab2_result = ctk.StringVar()

        self.build_tab1()
        self.build_tab2()

    def build_tab1(self):
        input_label = ctk.CTkLabel(self.tab1, text="Enter a value in decimal feet:",
                                   font=("Consolas", 18)).pack(fill="x")
        self.tab1_entrbx = ctk.CTkEntry(
            self.tab1, textvariable=self.tab1_entry, font=(
                "Consolas", 18)).pack(fill="x")

        conv_button = ctk.CTkButton(self.tab1, text="CONVERT",
                                    font=("Consolas", 18), command=self.tab1_click).pack(
            fill="x", padx=2, pady=2)

        self.output_entry = ctk.CTkEntry(self.tab1, textvariable=self.tab1_result,
                                         font=("Consolas", 22), state="readonly").pack(
            fill="x", padx=2, pady=10)

    def tab1_click(self):
        inp = float(self.tab1_entry.get())

        # Convert to feet and inches
        feet = int(inp)
        inches = (inp - feet) * 12

        # Build the output string
        output = "{}'-{:.4f}\"".format(feet, inches)

        # Set the output string in the text box
        self.tab1_result.set(output)

    def build_tab2(self):
        input_label = ctk.CTkLabel(
            self.tab2, text="Enter a value in ft'-in.ches\":", font=("Consolas", 18)).pack(fill="x")

        self.tab2_entrbx = ctk.CTkEntry(
            self.tab2, textvariable=self.tab2_entry, font=("Consolas", 18)).pack(fill="x")

        calc_button = ctk.CTkButton(self.tab2, text="CONVERT", font=("Consolas", 18),
                                    command=self.tab2_click).pack(fill="x", padx=2, pady=10)

        self.output_entry = ctk.CTkEntry(self.tab2, textvariable=self.tab2_result, font=(
            "Consolas", 22), state="readonly").pack(fill="x", padx=2, pady=10)

    def tab2_click(self):
        # Valid formats:    a'-b.cdefghi"  --OR--    a' b.cdefghi"
        value = self.tab2_entry.get()

        # Look for feet and inches delimiters
        for dd in [" ", "-"]:
            if dd in value:
                parts = value.split(dd)
                if len(parts) > 2:
                    self.tab2_result.set("Error - too many parts")
                else:
                    feet, inches = parts

                # look for ' and " markers
                if "'" in feet:
                    feet = feet[:-1]

                if '"' in inches:
                    inches = inches[:-1]

                # Convert to double float, decimal feet
                decimal = float(feet) + float(inches) / 12.

                self.tab2_result.set("{:6f}\'".format(decimal))


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
