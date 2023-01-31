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
    def __init__(self, Fy=50., E=29000., G=11200.,filename=None,edition = '14th',kx=1.0,ky=1.0,Lx=120.,Ly=120.):
        current_file = path.abspath(__file__)
        self.cwd = path.abspath(path.join(current_file, pardir))
        self.py_path = path.abspath(path.join(current_file, pardir, pardir, "Scripts", "python.exe"))              
        
        if filename == None:
            self.filename= path.abspath(path.join(self.cwd, "AISC14.csv"))
        else:
            self.filename= path.abspath(path.join(self.cwd, filename))      
        
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
        with open(self.filename,'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        data = np.array(data)
        shapes_array = np.array(data[:,3])
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
                rolledprops[k] = float(data[row_index,v])
            except:
                rolledprops[k] = str(data[row_index,v])
        
        return rolledprops

    def rolled_section(self,shape):
        rolledprops = self._aisc_lookup(shape)     
        return rolledprops


def get_shapelist(filename):
    with open(filename,'r') as f:
            reader = csv.reader(f)
            data = list(reader)
    data = np.array(data)
    shapes_array = np.array(data[1:,3])
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
        outputvarlt = tk.StringVar()
        outputvarlt.set(txt[0])
        tk.Entry(window,state="readonly",textvariable=outputvarlt,font=font2,width=10).grid(row=i+2,column=1,sticky="W")

    # Populate output values on right
    for i, txt in enumerate(propsrt):
        outputvarrt = tk.StringVar()
        outputvarrt.set(txt[0])
        tk.Entry(window,state="readonly",textvariable=outputvarrt,font=font2,width=10).grid(row=i+2,column=5,sticky="W")

def update(data):
    # Clear the listbox
    my_list.delete(0,END)

    # Add shapes to listbox
    for item in data:
        my_list.insert(END, item)

def fillout(e):
    # Clear the entrybox
    shape_input.delete(0,END)

    # Add clicked list item to entry box
    shape_input.insert(0,my_list.get(ACTIVE))

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
bgcolor = "#3D7A97"
fgcolor = "#FEFEE8"
gray = "#EAEAEA"
navy = "#003C7C"

# Window object
window = tk.Tk()
window.title('AISC Shapes Lookup')
window.config(bg=bgcolor)
window.geometry("720x360")
window.iconbitmap("EngineeringApps\images\Will-High.ico")

# Define 2 custom fonts
font1 = ('Arial',16)
font2 = ('Arial',12)

# Get the csv file and convert the shapes column to a list
filename = r"C:\Users\wlyne\.EngApps\EngineeringApps\AISC14.csv"
shapes_list = get_shapelist(filename)


# Build the labels and shit.
label1 = tk.Label(window,text='Start Typing a Shape Name',bg=bgcolor,fg=fgcolor)
shape_input = tk.Entry(window,font=font2,width=10,bg=gray,fg=navy)
label1.grid(row = 0, column = 0, sticky='NW', padx=2, pady=2)
shape_input.grid(row = 0, column = 1, padx=2, pady=2, sticky="NW")

# Create a listbox
my_list = tk.Listbox(window,width=12,height=4,bg=gray,fg=navy) 
my_list.grid(row=0,column=2)

# Add shapes to listbox
update(shapes_list)

# Create a binding on the listbox onclick
my_list.bind("<<ListboxSelect>>",fillout)

# Create a bind on the entry box
shape_input.bind("<KeyRelease>", check)




# Define Output 
fmt = "{:2f}"
resultslt = np.array([['Ag =','','in2'],
                    ['d =','','in'],
                    ['tw =','','in'],
                    ['bf =','','in'],
                    ['tf =','','in'],
                    ['bf/2tf =','',''],
                    ['h/tw =','',''],
                    ['b/t =','',''],
                    ['D/t =','',''],
                    ['h/tdes =','',''],
                    ['b/tdes =','','']])

resultsrt = np.array([['Ix =','','in4'],
                      ['Zx =','','in3'],
                      ['Sx =','','in3'],
                      ['rx =','','in'],
                      ['Iy =','','in4'],
                      ['Zy =','','in3'],
                      ['Sy =','','in3'],
                      ['ry =','','in'],
                      ['J =','','in4'],
                      ['Cw =','','in6'],
                      ['e0 =','','in']])

rowslt = np.shape(resultslt)[0]
rowsrt = np.shape(resultsrt)[0]


# Populate output labels on left
for i, txt in enumerate(resultslt):
    tk.Label(window,text=txt[0],font=font2,width=10,bg=bgcolor,fg=fgcolor).grid(row=i+2,column=0,sticky="E")
    tk.Entry(window,state="readonly",font=font2,width=10).grid(row=i+2,column=1,sticky="W")
    tk.Label(window,text=txt[2],font=font2,width=5,bg=bgcolor,fg=fgcolor).grid(row=i+2,column=2,sticky="W")

# Populate output labels on right
for i, txt in enumerate(resultsrt):
    tk.Label(window,text=txt[0],font=font2,width=10,bg=bgcolor,fg=fgcolor).grid(row=i+2,column=4,sticky="E")
    tk.Entry(window,state="readonly",font=font2,width=10).grid(row=i+2,column=5,sticky="W")
    tk.Label(window,text=txt[2],font=font2,width=5,bg=bgcolor,fg=fgcolor).grid(row=i+2,column=6,sticky="W")

get_values_button = tk.Button(window,text='Get Properties',font=font1,command=getvalues,bg=navy,fg=fgcolor)
get_values_button.grid(row=0,column=3,sticky="NW")



# # # # # NAAAWWWW..... still doesn't work.  fuck it for now.  kisses, -bjt 20221229_2119
# # Look up a section by required Ix, Sx, rx, Zx, (same for Y)


# def get_optimal_shapes():
#     prop = lookupselectedvalue.get()
#     criteria = float(enterbyvalue.get())

#     # Get the .csv file as a numpy array
#     with open(filename,'r') as f:
#             reader = csv.reader(f)
#             data = list(reader)
#     data = np.array(data)
#     nrows, ncols = np.shape(data)

#     # Return the column index 
#     col_index = acols[prop] 

#     # define a holding array for column values that meet initial criteria
#     hold_array = np.empty((0,ncols))

#     # iterate through the csv data. if the column data meets criteria, return the whole row to the Dwight, you are gonna make us so happy.
#     j = 0 # initialize a counter

#     for i in range(nrows):
#         check_value = data[i,col_index]
#         try:
#             check_value = float(check_value)
#             if check_value >= criteria:
#                 np.append(hold_array,data[i,:])
#                 j += 1
#         except:
#             continue
    
#     # Define the csv column index for Ag
#     A_col = 10
#     # Define the csv column index for shape name
#     name_col = 3
#     # process process it my mang
#     A_array = hold_array[1:,A_col] # Strip out the text headers
#     A_sort_ind = np.argsort(A_array) # Returns indices of a sorted array
    
#     name_sort = []
#     for i, nn in enumerate(A_sort_ind):
#         name_sort.append(data[nn+1,name_col])
    
#     # Clear the listbox
#     my_val_list.delete(0,END)

#     # Add shapes to listbox
#     for item in name_sort:
#         my_val_list.insert(END, item)








# lookups = ['Ix', 'Sx', 'Zx', 'rx', 'Iy', 'Sy', 'Zy', 'ry']

# lookupbyproplabel = tk.Label(window,text='Lookup by Property, sorted ascending values by area (in prog...)',font=font2,bg=bgcolor,fg=fgcolor,pady=6)
# lookupbyproplabel.grid(row=13,column=0,columnspan=3,sticky='NW')

# lookupselectedvalue = tk.StringVar()
# lookupselect = tk.OptionMenu(window,lookupselectedvalue,lookups[1],*lookups)
# lookupselect.grid(row=14,column=1, sticky="NW")

# label100 = tk.Label(window,text='Select Property:',font=font1,bg=bgcolor,fg=fgcolor)
# label100.grid(row=14,column=0, sticky="NE",pady=10)

# label101 = tk.Label(window,text='Enter Value:',font=font1,bg=bgcolor,fg=fgcolor)
# label101.grid(row=15,column=0, sticky="NE",pady=10)

# button100 = tk.Button(window,text='Get Optimal Shapes',font=font1,bg=navy,fg=fgcolor,command=get_optimal_shapes)
# button100.grid(row=15,column=3)

# enterbyvalue = tk.StringVar()
# enterbyvaluebox = tk.Entry(window,textvariable=enterbyvalue,font=font1,bg=gray,fg=navy, width=10)
# enterbyvaluebox.grid(row=15,column=1,columnspan=2, sticky="NW")

# # Create a listbox
# label102 = tk.Label(window,text="Optimal Shapes:",bg=bgcolor,fg=fgcolor,font=font1)
# label102.grid(row=17,column=0,sticky="NE",pady=10)
# my_val_list = tk.Listbox(window,width=20,height=12,bg=gray,fg=navy,font=font2)
# my_val_list.grid(row=17,column=1,sticky="NW",pady=10)














window.mainloop()
