import csv
from aisc_columns import aisc_cols_csv as acols
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import csv
import numpy as np
import scipy.stats as ss
from numpy import argsort
from tkinter import END
from tkinter import ACTIVE
import sys
np.set_printoptions(threshold=sys.maxsize)


class PropertySearch:
    def __init__(self) -> None:
        pass


class App:
    def __init__(self) -> None:
        self.root = ctk.CTk()
        self.input = ctk.StringVar()
        self.output = ctk.Variable()
        self.build_window()

        # Bind the enter key
        self.root.bind('<Return>', self.enter)

    def build_window(self):
        self.root.title("Lookup by Property")
        ctk.CTk().iconbitmap(r"images\Will-High.ico")
        # self.root.geometry("800x600")
        # self.root.iconbitmap(r"images\Will-High.ico")
        ctk.set_default_color_theme("blue")
        ctk.set_appearance_mode("dark")

        # Big entry window
        ctk.CTkEntry(master=self.root, border_width=1, width=24,
                     font=("Consolas", 36), textvariable=self.input).pack(side="top", fill="both")

        # Big Search Button
        ctk.CTkButton(master=self.root, text="Get Some", command=self.button_click,
                      width=24, font=("Consolas", 36, "bold")).pack(fill="both")

        # Create a Listbox with scrollbar (TODO)
        listbox = tk.Listbox(master=self.root, width=24, listvariable=self.output,
                             font=("Consolas", 24), selectmode=tk.EXTENDED, background="#343638", fg="#dce4ee").pack(fill="both", expand=True)

    def button_click(self):
        instring = self.input.get()
        self.ordered_shapes = _parser(instring)
        self.output.set("")
        self.output.set(self.ordered_shapes)

    def enter(self, event):
        self.button_click()


def _parser(instring: str):
    # A typical input string should look like:
    # Ix > 400, W (Return a list of all W shapes with Ix > 400 in4)
    # A list can also be entered:
    #       Ix > 400; ["W", "S", "M", "2C", "2L"]
    # The semicolor is the delimiter
    # TODO ADD THIS FEATURE LATER...  JUST GET IT WORKING 20230116_0851

    # First break the expression and the shapes
    # expr, shapes = instring.split(";")
    # expr.strip()
    # shapes.strip()
    expr = instring.strip()

    # Extract the Property & Equality
    prop = expr.split()[0]
    equality = expr.split(prop)[1]

    AgCol = acols["Ag"]
    TypeCol = acols["type"]
    ShapeCol = acols["shape"]

    # retrieve the lookup column from the aisc shapes csv
    try:
        matchColumn = acols[prop]
        # print(matchColumn)
    except:
        messagebox.showerror("Whoops", message="Enter a valid property")
        return

    # Read the csv file
    with open("AISC14.csv", 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    data = np.array(data)
    nrows, ncols = np.shape(data)
    results = np.empty((0, ncols))

    # # Evaluate the shapes list or single shape if given
    # evalstring = " in shapes" if type(shapes) == list else " == shapes"

    for i in range(1, nrows):
        # if eval(str(data[i][matchColumn])+equality) and eval(str(data[i][acols['type']]).strip()+evalstring):
        #     results.append(data[i][:])
        if eval(str(data[i, matchColumn]) + equality):
            results = np.vstack((results, data[i, :]))

    # Sort the list by gross area, ascending values
    resultRows, resultCols = np.shape(results)
    # Convert the areas into floats
    for i in range(resultRows):
        results[i, AgCol] = float(results[i, AgCol])

    areas = [float(n) for n in results[:, AgCol].tolist()]
    area_ranks = ss.rankdata(areas, method="ordinal") - 1

    # order the shapes list now
    ordered_shapes = []
    for i in range(resultRows):
        for j, r in enumerate(area_ranks):
            if r == i:
                ordered_shapes.append(results[j, ShapeCol])

    return ordered_shapes


def main():
    w = App()
    w.root.mainloop()


if __name__ == "__main__":
    main()
