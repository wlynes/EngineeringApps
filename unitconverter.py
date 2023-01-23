import tkinter as tk
from tkinter import messagebox
import re
from fractions import Fraction
import forallpeople as fap
import os
import json


# class Measurement:
#     def __init__(self) -> None:
#         # Default units environments (metric default default)
#         # us_customary, electrical, structural, thermal
#         pass

#     def _CombineEnvs(self):
#         env_path = r"C:\Python\Lib\site-packages\forallpeople\environments"
#         for root, dirname, filename in os.walk(env_path):
#             envs = filename

#         for e in envs:
#             os.path.join(env_path, e)


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.input = tk.StringVar()
        self.output = tk.StringVar()
        self.build_window()

    def build_window(self):
        self.root.geometry("480x215")
        self.root.title("Units converter")
        self.root.iconbitmap(r"images\Will-High.ico")

        # Big entry window
        tk.Entry(master=self.root, relief="solid", width=24,
                 font=("Consolas", 36), textvariable=self.input).pack(side="top", fill="both")

        # Big convert button
        tk.Button(master=self.root, text="CONVERT", command=self.click,
                  width=24, font=("Consolas", 36, "bold")).pack(fill="both")

        # Big result window
        tk.Entry(master=self.root, relief="solid", width=24,
                 font=("Consolas", 36), state="readonly",
                 textvariable=self.output).pack(fill="both")

    def click(self):
        # Clear the output window
        self.output.set("")
        incoming = self.input.get()
        self.mag, self.oldu, self.newu = string_parser(incoming)
        self.cnv = converter_unit_processor(self.mag, self.oldu, self.newu)

        # Put it in the box!
        self.output.set(self.cnv)


def converter_unit_processor(mag, oldu: str, newu: str, env: str = None):
    env = "structural" if env == None else env
    # TODO Expand json of unit types.  Structural seems OK for now.
    fap.environment(env_name=env)
    mag = float(mag)

    try:
        w = mag * eval("fap." + oldu)
    except:
        messagebox.showerror(title="Invalid Quantity or Units",
                             message="Make sure to use the unit symbology from the Python package forallpeople.")

    try:
        n = w.to(unit_name=newu)
    except:
        messagebox.showerror(title="Invalid Quantity or Units",
                             message="Make sure to use the unit symbology from the Python package forallpeople.")

    if n:
        return n
    else:
        pass
    print(w)


def string_parser(s: str):
    # Example of valid input string: 11.619 feet to m
    # Python will split first:  11.619 feet, m with " to " as the delimiter.
    # Then Pythonw will split:  11.619, feet with " " as the delimiter.

    delimiter1 = " to "
    delimiter2 = " "

    try:
        expr, newu = s.split(delimiter1)
    except:
        messagebox.showerror(title="Invalid Conversion Operator", message=("Please check your entry format: \n\n" +
                                                                           "18.861 m to inch"))
    try:
        mag, oldu = expr.split(delimiter2)
    except:
        messagebox.showerror(title="Invalid Format", message=("Please check your entry format: \n\n" +
                                                              "18.861 m to inch"))

    return mag, oldu, newu


def main():
    w = App()
    w.root.mainloop()


if __name__ == "__main__":
    main()
