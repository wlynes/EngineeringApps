from os import pardir, path
import tkinter as tk
import customtkinter as cnt
from tkinter import END
from tkinter import ACTIVE
import csv
import numpy as np
import math
from aisc_columns import aisc_cols_csv as acols


class SteelMember():
    def __init__(self, Fy=50., E=29000., G=11200., filename="AISC14.csv", edition='14th', kx=1.0, ky=1.0, Lx=120., Ly=120.):
        self.edition = edition
        self.Fy = Fy
        self.E = E
        self.G = G
        self.kx = kx
        self.ky = ky
        self.Lx = Lx
        self.Ly = Ly
        self.efy = math.sqrt(E / Fy)
        self.filename = filename

    def _aisc_lookup(self, shape):
        with open(self.filename, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        data = np.array(data)
        shapes_array = np.array(data[:, 3])
        shapes_list = shapes_array.tolist()

        # match the row index
        for i, sec in enumerate(shapes_list):
            if sec == shape:
                row_index = i
                exit
        section = shape
        rowindex = row_index
        rolledprops = {}
        for k, v in acols.items():
            try:
                rolledprops[k] = float(data[row_index, v])
            except:
                rolledprops[k] = str(data[row_index, v])

        return rolledprops

    def rolled_section(self, shape):
        rolledprops = self._aisc_lookup(shape)
        return rolledprops


def get_shapelist(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
    data = np.array(data)
    shapes_array = np.array(data[1:, 3])
    shapes_list = shapes_array.tolist()

    return shapes_list


def getvalues():
    shape = shape_input.get()
    member = SteelMember()
    props = member.rolled_section(shape)

    # check if formatted as a number
    for k, v in props.items():
        try:
            props[k] = fmt.format(v)
        except:
            pass

    propslt = np.array([[props['Ag']],
                        [props['d']],
                        [props['tw']],
                        [props['bf']],
                        [props['tf']],
                        [props['bf_2tf']],
                        [props['h_tw']],
                        [props['b_t']],
                        [props['D_t']],
                        [props['h_tdes']],
                        [props['b_tdes']]])

    propsrt = np.array([[props['Ix']],
                        [props['Zx']],
                        [props['Sx']],
                        [props['rx']],
                        [props['Iy']],
                        [props['Zy']],
                        [props['Sy']],
                        [props['ry']],
                        [props['J']],
                        [props['Cw']],
                        [props['e0']]])

    rowslt = np.shape(propslt)[0]
    rowsrt = np.shape(propsrt)[0]

    # Populate output values on left
    for i, txt in enumerate(propslt):
        outputvarlt = cnt.StringVar()
        outputvarlt.set(txt[0])
        cnt.CTkEntry(window, state="readonly", textvariable=outputvarlt,
                     font=font2).grid(row=i+2, column=1, sticky="ew")

    # Populate output values on right
    for i, txt in enumerate(propsrt):
        outputvarrt = cnt.StringVar()
        outputvarrt.set(txt[0])
        cnt.CTkEntry(window, state="readonly", textvariable=outputvarrt,
                     font=font2).grid(row=i+2, column=5, sticky="ew")


def update(data):
    # Clear the listbox
    my_list.delete(0, END)

    # Add shapes to listbox
    for item in data:
        my_list.insert(END, item)


def fillout(e):
    # Clear the entrybox
    shape_input.delete(0, END)

    # Add clicked list item to entry box
    shape_input.insert(0, my_list.get(ACTIVE))


def check(e):
    # Get typed value
    typed = shape_input.get()

    if typed == '':
        data = shapes_list
    else:
        data = []
        for item in shapes_list:
            if typed.lower() in item.lower():
                data.append(item)
    update(data)


# Color palette palatte? palet?  whatever.
# bgcolor = "#3D7A97"
# fgcolor = "#FEFEE8"
# gray = "#EAEAEA"
# navy = "#003C7C"

# Window object
window = cnt.CTk()
window.title('AISC Shapes Lookup')
cnt.set_default_color_theme("blue")
cnt.set_appearance_mode("dark")
# window.geometry("720x360")
window.iconbitmap("images\Will-High.ico")

# Define 2 custom fonts
font1 = ('Consolas', 16)
font2 = ('Consolas', 12)

# Get the csv file and convert the shapes column to a list
filename = "AISC14.csv"
shapes_list = get_shapelist(filename)


# Build the labels and shit.
label1 = cnt.CTkLabel(window, text='Start Typing a Shape Name', font=font1)
shape_input = cnt.CTkEntry(window, font=font2)
label1.grid(row=0, column=0, sticky='NW', padx=2, pady=2)
shape_input.grid(row=0, column=1, padx=2, pady=2, sticky="NW")

# Create a listbox
my_list = tk.Listbox(window, width=12, height=4, font=font2)
my_list.grid(row=0, column=2)

# Add shapes to listbox
update(shapes_list)

# Create a binding on the listbox onclick
my_list.bind("<<ListboxSelect>>", fillout)

# Create a bind on the entry box
shape_input.bind("<KeyRelease>", check)


# Define Output
fmt = "{:2f}"
resultslt = np.array([['Ag =', '', 'in2'],
                      ['d =', '', 'in'],
                      ['tw =', '', 'in'],
                      ['bf =', '', 'in'],
                      ['tf =', '', 'in'],
                      ['bf/2tf =', '', ''],
                      ['h/tw =', '', ''],
                      ['b/t =', '', ''],
                      ['D/t =', '', ''],
                      ['h/tdes =', '', ''],
                      ['b/tdes =', '', '']])

resultsrt = np.array([['Ix =', '', 'in4'],
                      ['Zx =', '', 'in3'],
                      ['Sx =', '', 'in3'],
                      ['rx =', '', 'in'],
                      ['Iy =', '', 'in4'],
                      ['Zy =', '', 'in3'],
                      ['Sy =', '', 'in3'],
                      ['ry =', '', 'in'],
                      ['J =', '', 'in4'],
                      ['Cw =', '', 'in6'],
                      ['e0 =', '', 'in']])

rowslt = np.shape(resultslt)[0]
rowsrt = np.shape(resultsrt)[0]


# Populate output labels on left
for i, txt in enumerate(resultslt):
    cnt.CTkLabel(window, text=txt[0], font=font2).grid(
        row=i+2, column=0, sticky="E")
    cnt.CTkEntry(window, state="readonly", font=font2,
                 width=100).grid(row=i+2, column=1, sticky="ew")
    cnt.CTkLabel(window, text=txt[2], font=font2, width=5).grid(
        row=i+2, column=2, sticky="ew")

# Populate output labels on right
for i, txt in enumerate(resultsrt):
    cnt.CTkLabel(window, text=txt[0], font=font2).grid(
        row=i+2, column=4, sticky="E")
    cnt.CTkEntry(window, state="readonly", font=font2,
                 width=100).grid(row=i+2, column=5, sticky="ew")
    cnt.CTkLabel(window, text=txt[2], font=font2, width=5).grid(
        row=i+2, column=6, sticky="ew")

get_values_button = cnt.CTkButton(
    window, text='Get Properties', font=font1, command=getvalues)
get_values_button.grid(row=0, column=3, sticky="NW")

window.mainloop()
