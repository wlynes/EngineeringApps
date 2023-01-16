import tkinter as tk
from tkinter import messagebox
import re
from fractions import Fraction
import forallpeople as fap


class Measurement:
    def __init__(self, environment: str = 'us_customary') -> None:
        # Default units environments (metric default default)
        # us_customary, electrical, structural, thermal
        pass

    # def InputValue(self):


class App:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.input = tk.StringVar()
        self.output = tk.StringVar()
        self.build_window()

        # Bind the Enter key
        self.root.bind('<Return>', self.enter)

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

    def enter(self, event):
        self.click()


def converter_unit_processor(mag, oldu: str, newu: str, env: str = "wjl"):
    # TODO Expand json of unit types.  Structural seems OK for now.
    fap.environment(env_name=env, top_level=True)
    mag = float(mag)

    try:
        w = mag * eval(oldu)
    except NameError:
        messagebox.showerror(title="Invalid Units",
                             message=oldu + " not defined")
    except:
        messagebox.showerror(title="Invalid Quantity or Units",
                             message="Make sure to use the unit symbology from the Python package forallpeople.")

    try:
        n = w.to(unit_name=newu)
    except NameError:
        messagebox.showerror(title="Invalid Units",
                             message=newu + " not defined")
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
