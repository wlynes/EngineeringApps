#!C:\Users\wlyne\.EngApps\Scripts\python
import customtkinter as cnt
import tkinter as tk
from tkinter import ttk
import re
from fractions import Fraction
import math
from random import random
from tkinter import messagebox

class App(cnt.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Feet and Inches Converter")
        cnt.set_default_color_theme("blue")
        cnt.set_appearance_mode("dark")        

        tabs = TabHolder(self).pack()

class TabHolder(cnt.CTkTabview):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.tab1 = self.add("Decimal ft -> ft\'-in\"")
        self.tab2 = self.add("ft\'-in\" -> Decimal ft")
      
        self.tab1_entry = cnt.StringVar(value="{:.8f}".format(10. * random()))
        self.tab1_result = cnt.StringVar()
        self.selected_precision = cnt.StringVar()

        self.tab2_entry = cnt.StringVar()
        self.tab2_result = cnt.StringVar()

        self.build_tab1()
        self.build_tab2()
    
    def build_tab1(self):
        precision_options = [0,2,4,8,16,32, 64, 128]
        self.selected_precision.set(16)
        
        input_label = cnt.CTkLabel(self.tab1, text="Enter a decimal value in feet:", font=("Consolas", 18)).pack(fill="x")
        self.tab1_entrbx = cnt.CTkEntry(self.tab1, textvariable=self.tab1_entry, font=("Consolas", 18)).pack(fill="x")

        prec_label = cnt.CTkLabel(self.tab1, text="Select precision:", font=("Consolas",14)).pack(padx=2)
        seg_button = cnt.CTkSegmentedButton(self.tab1,
                                            values=precision_options,
                                            variable=self.selected_precision,
                                            font=("Consolas", 14)).pack(padx=2,pady=2)
        
        calc_button = cnt.CTkButton(self.tab1, text="CONVERT", font=("Consolas", 18),
                                    command=self.tab1_click).pack(fill="x", padx=2, pady=10)

        self.output_entry = cnt.CTkEntry(self.tab1, textvariable=self.tab1_result, font=("Consolas", 22), state="readonly").pack(fill="x", padx=2, pady=10)

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
        numerator = round(decInches*precision,0)
        denominator = precision
        frac = Fraction(numerator/denominator)
        if frac == 1:
            wholeinches += 1
            numerator=0

        # Build the output string
        if numerator == 0:
            output = "{}'-{}\"".format(feet, wholeinches)
        else:
            output = "{}'-{} {}\"".format(feet, wholeinches,frac)

        # Set the output string in the text box
        self.tab1_result.set(output)

    def build_tab2(self):
        input_label = cnt.CTkLabel(self.tab2, text="Enter a value in ft'-in\":", font=("Consolas", 18)).pack(fill="x")
        self.tab2_entrbx = cnt.CTkEntry(self.tab2, textvariable=self.tab2_entry, font=("Consolas", 18)).pack(fill="x")
            
        calc_button = cnt.CTkButton(self.tab2, text="CONVERT", font=("Consolas", 18),
                                    command=self.tab2_click).pack(fill="x", padx=2, pady=10)

        self.output_entry = cnt.CTkEntry(self.tab2, textvariable=self.tab2_result, font=("Consolas", 22), state="readonly").pack(fill="x", padx=2, pady=10)


    def tab2_click(self):
        validFormats = [r"(\d+)\'-(\d+)\s(\d+)/(\d+)\"", # a'-b c/d" (default)
                r"(\d+)\'\s(\d+)\s(\d+)/(\d+)\"", # a' b c/d" (without the dash)
                r"(\d+)-(\d+)\s(\d+)/(\d+)", # a-b c/d (default without ' " marks)
                r"(\d+)\s(\d+)\s(\d+)\s(\d+)", # a b c/d (without - ' " marks)
                r"(\d+)\'-(\d+)\"", # a'-b" (whole inches only)]
                r"(\d+)-(\d+)", # a-b (whole inches without ' " marks)
                r"(\d+)\s(\d+)"] # a-b (whole inches without ' " marks)
       
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



    # # Add the feet and inches to get the total distance in decimal feet
    # return feet + inches / 12   

def main():
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
