import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import re
from fractions import Fraction
import math
from random import random
from tkinter import messagebox


class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Freedom Converter")
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")
        self.iconbitmap(r"images\Will-High.ico")

        tabs = TabHolder(self).pack()


class TabHolder(ctk.CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tab1 = self.add("Decimal ft -> ft\'-in\"")
        self.tab2 = self.add("ft\'-in\" -> Decimal ft")
        self.tab3 = self.add("VDOT Decimal to ft\'-in.ches\"")
        self.tab4 = self.add("VDOT ft\'-in.ches\" -> Decimal")

        self.tab1_entry = ctk.StringVar(value="{:.8f}".format(10. * random()))
        self.tab1_result = ctk.StringVar()
        self.selected_precision = ctk.StringVar()

        self.tab3_entry = ctk.StringVar(value="{:8f}".format(10. * random()))
        self.tab3_result = ctk.StringVar()

        self.tab4_entry = ctk.StringVar()
        self.tab4_result = ctk.StringVar()

        self.tab2_entry = ctk.StringVar()
        self.tab2_result = ctk.StringVar()

        self.build_tab1()
        self.build_tab2()
        self.build_tab3()
        self.build_tab4()

    def build_tab1(self):
        precision_options = [0, 2, 4, 8, 16, 32, 64, 128]
        self.selected_precision.set(16)

        input_label = ctk.CTkLabel(self.tab1, text="Enter a decimal value in feet:", font=(
            "Consolas", 18)).pack(fill="x")
        self.tab1_entrbx = ctk.CTkEntry(
            self.tab1, textvariable=self.tab1_entry, font=("Consolas", 18)).pack(fill="x")

        prec_label = ctk.CTkLabel(
            self.tab1, text="Select precision:", font=("Consolas", 14)).pack(padx=2)
        seg_button = ctk.CTkSegmentedButton(self.tab1,
                                            values=precision_options,
                                            variable=self.selected_precision,
                                            font=("Consolas", 14)).pack(padx=2, pady=2)

        calc_button = ctk.CTkButton(self.tab1, text="CONVERT", font=("Consolas", 18),
                                    command=self.tab1_click).pack(fill="x", padx=2, pady=10)

        self.output_entry = ctk.CTkEntry(self.tab1, textvariable=self.tab1_result, font=(
            "Consolas", 22), state="readonly").pack(fill="x", padx=2, pady=10)

    def tab1_click(self):
        inp = float(self.tab1_entry.get())

        # Convert input to feet and inches
        feet = int(inp)
        inches = (inp - feet) * 12

        # get the selected precision
        precision = int(self.selected_precision.get())
        multiple = 1 / precision

        # CONVERT TO INCHES AND FRACTION WITH SELECTED PRECISION
        # Get the whole inches
        wholeinches = int(inches)

        # Get the remainder (0.XXXX")
        decInches = inches - wholeinches

        # Still got the mooooooves
        numerator = round(decInches*precision, 0)
        denominator = precision
        frac = Fraction(numerator/denominator)
        if frac == 1:
            wholeinches += 1
            numerator = 0

        # Build the output string
        if numerator == 0:
            output = "{}'-{}\"".format(feet, wholeinches)
        else:
            output = "{}'-{} {}\"".format(feet, wholeinches, frac)

        # Set the output string in the text box
        self.tab1_result.set(output)

    def build_tab2(self):
        input_label = ctk.CTkLabel(
            self.tab2, text="Enter a value in ft'-in\":", font=("Consolas", 18)).pack(fill="x")
        self.tab2_entrbx = ctk.CTkEntry(
            self.tab2, textvariable=self.tab2_entry, font=("Consolas", 18)).pack(fill="x")

        calc_button = ctk.CTkButton(self.tab2, text="CONVERT", font=("Consolas", 18),
                                    command=self.tab2_click).pack(fill="x", padx=2, pady=10)

        self.output_entry = ctk.CTkEntry(self.tab2, textvariable=self.tab2_result, font=(
            "Consolas", 22), state="readonly").pack(fill="x", padx=2, pady=10)

    def tab2_click(self):
        validFormats = [r"(\d+)\'-(\d+)\s(\d+)/(\d+)\"",  # a'-b c/d" (default)
                        # a' b c/d" (without the dash)
                        r"(\d+)\'\s(\d+)\s(\d+)/(\d+)\"",
                        # a-b c/d (default without ' " marks)
                        r"(\d+)-(\d+)\s(\d+)/(\d+)",
                        # a b c/d (without - ' " marks)
                        r"(\d+)\s(\d+)\s(\d+)\s(\d+)",
                        r"(\d+)\'-(\d+)\"",  # a'-b" (whole inches only)]
                        r"(\d+)-(\d+)",  # a-b (whole inches without ' " marks)
                        r"(\d+)\s(\d+)"]  # a-b (whole inches without ' " marks)

        value = self.tab2_entry.get()

        for i, chk in enumerate(validFormats):
            if m := re.match(chk, value):
                feet = int(m.group(1))
                inches = int(m.group(2))
                if chk in validFormats[-3:]:
                    numerator = 0
                    denominator = 1
                else:
                    numerator = int(m.group(3))
                    denominator = int(m.group(4))
                # Convert the fraction to a decimal value and add it to the inches
                inches += numerator / denominator
        self.tab2_result.set("{:6f}".format(feet + inches / 12))

    def build_tab3(self):
        input_label = ctk.CTkLabel(self.tab3, text="Enter a value in decimal feet:",
                                   font=("Consolas", 18)).pack(fill="x")
        self.tab3_entrbx = ctk.CTkEntry(
            self.tab3, textvariable=self.tab3_entry, font=(
                "Consolas", 18)).pack(fill="x")

        conv_button = ctk.CTkButton(self.tab3, text="CONVERT",
                                    font=("Consolas", 18), command=self.tab3_click,
                                    fg_color="#F47735").pack(
            fill="x", padx=2, pady=10)

        self.output_entry = ctk.CTkEntry(self.tab3, textvariable=self.tab3_result,
                                         font=("Consolas", 22), state="readonly").pack(
            fill="x", padx=2, pady=10)

    def tab3_click(self):
        inp = float(self.tab3_entry.get())

        # Convert to feet and inches
        feet = int(inp)
        inches = (inp - feet) * 12

        # Build the output string
        output = "{}'-{:.4f}\"".format(feet, inches)

        # Set the output string in the text box
        self.tab3_result.set(output)

    def build_tab4(self):
        input_label = ctk.CTkLabel(
            self.tab4, text="Enter a value in ft'-in.ches\":", font=("Consolas", 18)).pack(fill="x")

        self.tab4_entrbx = ctk.CTkEntry(
            self.tab4, textvariable=self.tab4_entry, font=("Consolas", 18)).pack(fill="x")

        calc_button = ctk.CTkButton(self.tab4, text="CONVERT", font=("Consolas", 18),
                                    command=self.tab4_click,
                                    fg_color="#F47735").pack(fill="x", padx=2, pady=10)

        self.output_entry = ctk.CTkEntry(self.tab4, textvariable=self.tab4_result, font=(
            "Consolas", 22), state="readonly").pack(fill="x", padx=2, pady=10)

    def tab4_click(self):
        # Valid formats:    a'-b.cdefghi"  --OR--    a' b.cdefghi"
        value = self.tab4_entry.get()

        # Look for feet and inches delimiters
        for dd in [" ", "-"]:
            if dd in value:
                parts = value.split(dd)
                if len(parts) > 2:
                    self.tab4_result.set("Error - too many parts")
                else:
                    feet, inches = parts

                # look for ' and " markers
                if "'" in feet:
                    feet = feet[:-1]

                if '"' in inches:
                    inches = inches[:-1]

                # Convert to double float, decimal feet
                decimal = float(feet) + float(inches) / 12.

                self.tab4_result.set("{:6f}\'".format(decimal))


def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
