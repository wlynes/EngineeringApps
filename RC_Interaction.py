# import libraries
import numpy as np
import math
import tkinter as tk
from PIL import Image, ImageTk
import datetime
import os

# Default number format
numfmt = "{:.2f}"


# Methods, or whate tha fuk
def button_click():
    # Instantiate an RC Interaction Diagram object
    rc = RC_Interaction()

    # Get the input
    rc.get_input_tkinter()   

    # Get steel properties
    rc.get_steel_props()

    # Get concrete properties
    rc.get_conc_props()

    # Iterate through 'c' depths and return values
    Pax, Max, Pnx, Mnx, esbx, Pkvx, Mkvx = rc.the_iterator()
    get_results(Pkvx, Mkvx, 12,0)

    # Plot
    plot_diagram(Pax, Max, Pkvx, Mkvx)

def default_values():
    h = 32.0 #in
    b = 24.0 #in
    dclr = 2.5 #in
    dbar = 1.125 #in
    fc = 3.5 #ksi
    fy = 53.7 #ksi

    return h, b, dclr, dbar, fc, fy
 
class RC_Interaction():
    def __init__(self):
        # Constants
        self.ec = 0.003
        self.E = 29000
    
    def get_input_tkinter(self):
        # Get input 
        self.h = inp001.get()
        self.b = inp002.get()
        self.dclr = inp003.get()
        self.dbar = inp004.get()
        self.fc = inp005.get()
        self.fy = inp006.get()
        self.nbar = inp007.get()

        # Define additional constants from input values
        self.ey = self.fy / self.E  

    def get_steel_props(self):
        
        self.Ast = math.pi / 4 * self.dbar**2
        self.nby, self.nbx = (self.nbar, self.nbar)
        self.AstTop = self.Ast * self.nbar
        self.AstBottom = self.Ast * self.nbar
        self.dsTop = self.dclr
        self.dsBottom = self.h - self.dclr
     
    def get_conc_props(self):
        self.Ec = 57000 * math.sqrt(self.fc * 1000)
        if self.fc <= 4.:
            self.beta1 = 0.85
        elif self.fc < 8:
            self.beta1 = 0.85 - 0.05*(self.fc-4)
        else:
            self.beta1 = 0.65
        self.Ag = self.b*self.h
        
    def get_safety_factor(self,e):
        if abs(e) <= self.ey:
            self.phi, self.classification = 0.65, 'CC'
        elif abs(e) < self.ey + 0.003:
            self.phi, self.classification = 0.65+0.25*(abs(e)-self.ey)/(0.003), 'Tr'
        else:
            self.phi, self.classification = 0.90, 'TC'
        return 1.5/self.phi, self.classification

    def stress_strain(self, a, c):
        self.ysTop = self.dclr
        self.ysBottom = self.h - self.dclr

        if c > self.ysBottom + self.dbar / 2:
            self.Acc = self.b * a - (self.AstTop - self.AstBottom)
            self.esBottom = self.ec / c * (c - self.ysBottom)
            self.fsBottom = min(self.fy, self.esBottom * self.E)
            self.esTop = self.ec / c * (c - self.ysTop)
            self.fsTop = min(self.fy, self.esTop * self.E)             
        elif c > self.ysTop + self.dbar / 2:
            self.Acc = self.b * a - self.AstTop
            self.esBottom = -1 * self.ec / c * (self.ysBottom - c)
            self.fsBottom = max(-self.fy, self.esBottom * self.E)  
            self.esTop = self.ec / c * (c - self.ysTop)
            self.fsTop = min(self.fy, self.esTop * self.E) 
        else:
            self.Acc = self.b * a
            self.esBottom = -1 * self.ec / c * (self.ysBottom - c)
            self.fsBottom = max(-self.fy, self.esBottom * self.E) 
            self.esTop = -1 * self.ec / c * (self.ysTop - c)
            self.fsTop = max(-self.fy, self.esTop * self.E) 
        
    def get_forces(self, a):
            self.Cc = 0.85 * self.fc * self.Acc
            self.FsTop = self.fsTop * self.AstTop
            self.FsBottom = self.fsBottom * self.AstBottom
            P = min(0.80*self.P0, self.Cc + self.FsTop + self.FsBottom)
            M = self.Cc*(self.h/2 - a/2) + self.FsTop*(self.h/2 - self.ysTop) + self.FsBottom*(self.h/2 - self.ysBottom)
            return P, M

    def the_iterator(self, tol=0.0001):
        # Initialize arrays
        Pnx = []
        Mnx = []
        Pax = []
        Max = []
        esb = []
        Pkv = {}
        Mkv = {}
        
        # Calculate the first values of axial and moment arrays
        self.P0 = 0.85 * self.fc * (self.Ag - (self.AstTop + self.AstBottom)) + self.fy * (self.AstTop + self.AstBottom)
        Pnx.append(0.80*self.P0)
        Mnx.append(0.)
        Pax.append(0.80*self.P0/(1.50/0.65))
        Max.append(0.)
        esb.append(0.)
        Pkv.update({'PC':Pax[0]})   ;   Mkv.update({'PC':0.}) # Pure c8ompression (PC)

    
        # Iterate through depths of c, from bottom of section to top of section beginning with pure compression
        c = self.h
        while c >= 0.:
            a = self.beta1 * c
            self.stress_strain(a,c)
            P, M = self.get_forces(a)
            W, classification = self.get_safety_factor(self.esBottom)
            Pnx.append(P)
            Mnx.append(M/12)
            Pax.append(P/W)
            Max.append((M/12)/W)
            esb.append(self.esBottom)
            

            # Check for other key vals
            # Onset of cracking (OOC)
            if c == self.h: 
                Pkv.update({'OOC': P/W})    ;   Mkv.update({'OOC': (M/12)/W})
            
            # Onset of Tension Steel Yielding (TSY)
            if abs(abs(self.esBottom) - self.ey) <= tol:
                Pkv.update({'TSY': P/W})    ;   Mkv.update({'TSY': (M/12)/W})
            
            # Balanced Strain (BAL)
            if abs(abs(self.esBottom) - self.ec) <= tol:
                Pkv.update({'BAL': P/W})    ;   Mkv.update({'BAL': (M/12)/W})

            # Onset of Tension Controlled Section (TCL)
            if abs(abs(self.esBottom) - (self.ey + 0.003)) <= tol:
                Pkv.update({'TCL': P/W})    ;   Mkv.update({'TCL': (M/12)/W})
            
            # Pure Tension (PT)
            Mkv.update({'PT': 0.})
            Pkv.update({'PT':-self.fy*(self.AstBottom + self.AstTop)/(1.5/0.9)})

            c -= self.h/1000

        # Interpolate the pure bending value
        for i, val in enumerate(Pax):
            if val >= 0 and Pax[i+1] < 0:
                dMdP = (Max[i] - Max[i+1]) / (val - Pax[i+1])
                Pkv.update({'PB':0})    ;   Mkv.update({'PB':Max[i+1]+dMdP*(0-Pax[i+1])})

        self.Pkv = Pkv  ;   self.Mkv = Mkv    

        return Pax, Max, Pnx, Mnx, esb, Pkv, Mkv

def get_results(Pkv, Mkv,start_row,start_column):
    # interyy.get_results(Pay, May, Pkvy, Mkvy, 12,4)
    kvtable = np.array([['Limit State', 'Pn/Ω (kip)', 'Mn/Ω (kip*ft)'],
                        ["Pure Compression", numfmt.format(Pkv['PC']), numfmt.format(Mkv['PC'])],
                        ['Onset of Cracking', numfmt.format(Pkv['OOC']), numfmt.format(Mkv['OOC'])],
                        ['Tension Steel Yielding', numfmt.format(Pkv['TSY']), numfmt.format(Mkv['TSY'])],
                        ['Balanced Strain', numfmt.format(Pkv['BAL']), numfmt.format(Mkv['BAL'])],
                        ['Tension Controlled Section', numfmt.format(Pkv['TCL']), numfmt.format(Mkv['TCL'])],
                        ['Pure Bending', numfmt.format(Pkv['PB']),numfmt.format(Mkv['PB'])],
                        ['Pure Tension',numfmt.format(Pkv['PT']),numfmt.format(Mkv['PT'])]])
    
    kvrows, kvcolumns = np.shape(kvtable)
    
    # Output the table
    for i in range(kvrows):
        for j in range(kvcolumns):
            tv = tk.StringVar()
            tv.set(kvtable[i][j])
            tk.Entry(window,textvariable=tv,font=font3,state="readonly").grid(row=start_row+i,column=start_column+j,pady=2,sticky='NW')

def plot_diagram(Pax,Max,Pkv:dict,Mkv:dict):
    import matplotlib
    matplotlib.use("TkAgg") # use Tkinter backend
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # FigureCanvas for Matplotlib
    from matplotlib.figure import Figure  # create Matplotlib figure
    
    fig = Figure(figsize=(5,4))
    ax = fig.add_subplot(111)
    
    # Plot the interaction values
    ax.plot(Max,Pax,linestyle="solid",color="black",linewidth=1.5)
    
    ax.set_title('Interaction Diagram')
    ax.set_xlabel('Mnx / Ω (kip-ft)')
    ax.set_ylabel('Pnx / Ω (kip)')
    ax.grid(True)
    
    # Iterate through Pkv and Mkv to plot reference lines to interaction diagram
    for k, v in Pkv.items():
        x = [0., Mkv[k]]
        y = [0., Pkv[k]]
        midpoint = (Mkv[k] / 2, Pkv[k] / 2)
        rotation = math.degrees(math.atan2(Pkv[k], Mkv[k]))
        length = math.sqrt(Mkv[k]**2 + Pkv[k]**2)
        location = (0.8 * math.cos(math.radians(rotation)) * length, 0.8 * math.sin(math.radians(rotation)) * length)


        label = k
        ax.plot(x,y,linestyle='dashed',color='blue',linewidth=0.5)
        ax.plot(Mkv[k],Pkv[k],'bo')
        ax.annotate(label, xy=location, rotation=rotation,bbox=dict(facecolor='white',edgecolor='white',boxstyle='round'),
                    fontsize=6, horizontalalignment='center')
    
    # Plot the P and M values
    Pu = inp_P.get()
    Mu = inp_M.get()
    ax.plot(Mu,Pu,'ro',markersize=8)
    ax.annotate('Mu, Pu',xy=(Mu,Pu),xytext=(10,10),textcoords='offset points',color='red',fontsize=8)

    # draw plot in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)  # create FigureCanvasTkAgg object
    plot_widget = canvas.get_tk_widget()  # get Tkinter widget for plot
    plot_widget.grid(row=10, column=3,rowspan=10, columnspan=4)  # place widget in Tkinter grid
   

# Motherfuckin Tk windwow window
window = tk.Tk()
window.title('Interaction Diagrams for R.C. Columns v0.1')
window.geometry("1040x800")
window.iconbitmap(r"images\Will-High.ico")

# Define two text styles.  Whoops, I did three.  Jerk turkey.
font1 = ('Arial',14)
font2 = ('Arial',12)
font3 = ('Arial',10)

# Get default values to populate input boxes
defh, defb, defdclr, defdbar, deffc, deffy = default_values()

# Inputs
title001 = tk.Label(window,text='Define section parameters',font=font1,pady=2)
title001.grid(row=0,column=0,columnspan=2,sticky="NW")

tk.Label(window,text="  ",font=font1).grid(row=0,column=2)
tk.Label(window,text="  ",font=font1).grid(row=0,column=3)
tk.Label(window,text="  ",font=font1).grid(row=0,column=4)

# LOL, this was before I did the row, col counters.  Jesus, that might
# be clunky as shit, but it's way more flexible than this shit.

title002 = tk.Label(window, text='Enter ASD Axial Force and Bending Moment', font=font1)
title002.grid(row=0,column=5,sticky="NW")
tk.Label(window,text="P (kip) =", font=font2).grid(row=1,column=5,sticky="NE")
tk.Label(window,text="M (kip-ft) =", font=font2).grid(row=2,column=5,sticky="NE")
inp_P = tk.DoubleVar()
inp_M = tk.DoubleVar()
inp_P.set(500.0)
inp_M.set(200.0)

tk.Entry(window,textvariable=inp_P,font=font2).grid(row=1,column=6)
tk.Entry(window,textvariable=inp_M,font=font2).grid(row=2,column=6)

inp001 = tk.DoubleVar()
inp001.set(numfmt.format(defh))
label001 = tk.Label(window,text='h =',font=font2,pady=2)
label001.grid(row=1,column=0,sticky="NE")
inpb001 = tk.Entry(window,textvariable=inp001,font=font2,width=8)
inpb001.grid(row=1,column=1,sticky="NW")

inp002 = tk.DoubleVar()
inp002.set(numfmt.format(defb))
label002 = tk.Label(window,text='b =',font=font2,pady=2)
label002.grid(row=2,column=0,sticky="NE")
inpb002 = tk.Entry(window,textvariable=inp002,font=font2,width=8)
inpb002.grid(row=2,column=1,sticky="NW")

inp003 = tk.DoubleVar()
inp003.set(numfmt.format(defdclr))
label003 = tk.Label(window,text='dclr =',font=font2,pady=2)
label003.grid(row=3,column=0,sticky="NE")
inpb003 = tk.Entry(window,textvariable=inp003,font=font2,width=8)
inpb003.grid(row=3,column=1,sticky="NW")

inp004 = tk.DoubleVar()
inp004.set(numfmt.format(defdbar))
label004 = tk.Label(window,text='dbar =',font=font2,pady=2)
label004.grid(row=4,column=0,sticky="NE")
inpb004 = tk.Entry(window,textvariable=inp004,font=font2,width=8)
inpb004.grid(row=4,column=1,sticky="NW")

inp005 = tk.DoubleVar()
inp005.set(numfmt.format(deffc))
label005 = tk.Label(window,text='f\'c =',font=font2,pady=2)
label005.grid(row=5,column=0,sticky="NE")
inpb005 = tk.Entry(window,textvariable=inp005,font=font2,width=8)
inpb005.grid(row=5,column=1,sticky="NW")

inp006 = tk.DoubleVar()
inp006.set(numfmt.format(deffy))
label006 = tk.Label(window,text='fy =',font=font2,pady=2)
label006.grid(row=6,column=0,sticky="NE")
inpb006 = tk.Entry(window,textvariable=inp006,font=font2,width=8)
inpb006.grid(row=6,column=1,sticky="NW")

inp007 = tk.IntVar()
inp007.set(numfmt.format(2))
label007 = tk.Label(window,text='nbar/row =',font=font2,pady=2)
label007.grid(row=7,column=0,sticky="NE")
inpb007 = tk.Entry(window,textvariable=inp007,font=font2,width=8)
inpb007.grid(row=7,column=1,sticky="NW")

# Calculate button!
button001 = tk.Button(window,text='Construct Diagrams',font=font1,pady=2,command=button_click)
button001.grid(row=8,column=0,columnspan=3)

# Output key values
label008 = tk.Label(window,text='Key Interaction Values',font=font2,pady=10)
label008.grid(row=10,column=0)

label009 = tk.Label(window,text='X-X Axis',font=font3,pady=2)
label009.grid(row=11,column=0, sticky='NW')

window.mainloop()