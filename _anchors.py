"""
Anchoring to Concrete per ACI 318-19 Ch. 17
... because relying on proprietary design
software sucks and gets your endless spam email.

2023-01-03 William J. Lynes, P.E.

Updates as of the time I remembered to make this:
20230104_1940:  The goal is to create an additional
tab showing the Structural Analysis 

See ACI 318-19 Ch. 17 for more information.  Get
off my case already.


TODO Updated 20230104_0611
PRE:
    - Do a structural analysis to see which anchors in the group
     are actually loaded in tension... etc... ✔ done! 20230105_1540

INPUT:
    - Include cracked/uncracked designation.  The program currently conservatively
      assumes cracked sections
    - Include Steel type:  ductile or brittle.  Program assumes ductile
    - Include critical distances per § 17.9

OUTPUT:
    - V, N interaction diagram
    - create a nicer input graphic ]done.

"""

# import libraries
import numpy as np
import math
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from sectionproperties.pre.library.primitive_sections import circular_section
from sectionproperties.analysis.section import Section
import os
import matplotlib
matplotlib.use("TkAgg") # use Tkinter backend
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # FigureCanvas for Matplotlib
from matplotlib.figure import Figure  # create Matplotlib figure
# from tkinter import messagebox
# from PIL import Image, ImageTk
# import datetime
# import os

# Default number format
numfmt = "{:.2f}"

# Default values
def default_values():
    # Page 9 of 10, Redhead Trubolt Wedge Anchor Catalog
    # Example calculation
    da = 0.50 #in; anchor diameter
    fc = 2.5 #ksi; concrete strength
    fy = 55.0 #ksi; anchor yield strength
    futa = 75.0 #ksi; anchor ultimate strength
    heff = 3.375 #in
    anchor_cat:int = 1
    tpld = 0.5 #in; baseplate thickness

    return da, fc, fy, futa, heff, anchor_cat, tpld

"""

RON BURGUNDY, ANCHORMAN.
ANCHOR CLASS

"""

class Anchor():
    def __init__(self, da=0.75,fy=60,fc=3.5, wc=150, suppl_reinf:bool=True, anchor_type:str="PI",anchor_cat:int=1,steel_type:str="ductile"):
        self.fc = fc
        self.fy = fy
        self.wc = wc
        self.da = da
        self.suppl_reinf = suppl_reinf
        self.anchor_type = anchor_type
        self.anchor_cat = anchor_cat
        self.steel_type = steel_type

    def conc_props(self):
        # Modulus of Elasticity
        self.Ec = 57000 * math.sqrt(self.fc * 1000) / 1000
        
        # β1
        if self.fc <= 4.:
            self.beta1 = 0.85
        elif self.fc < 8:
            self.beta1 = 0.85 - 0.05*(self.fc-4)
        else:
            self.beta1 = 0.65
        # Ag
        # self.Ag = self.b*self.h

        # Lightweight modification factor, λ
        if self.wc <= 100.:
            self.lam = 0.75
        elif self.wc <= 135.:
            self.lam = min(0.0075*self.wc,1.0)
        else:
            self.lam = 1.0

    def anchor_props(self):
        self.Aa = math.pi / 4 * self.da**2

    def resistance_factors_steel(self):
        # LRFD for now... would like ASD
        # Table 17.5.3(a)
        if self.steel_type == 'ductile':
            self.fst = 0.75 ;   self.fsv = 0.65
        else:
            self.fst = 0.65 ;   self.fsv = 0.60

    def resistance_factors_conc1(self):
        # Table 17.5.3(b) - Anchor strength governed by concrete breakout,
        # bond, and side-face blowout
        if self.suppl_reinf:
            if self.anchor_type == 'CI':
                self.fct1 = 0.75
            elif self.anchor_cat == 1:
                self.fct1 = 0.75
            elif self.anchor_cat == 2:
                self.fct1 = 0.65
            else:
                self.fct1 = 0.60
            self.fcv1 = 0.75
        else:
            if self.anchor_type == 'CI':
                self.fct1 = 0.70
            elif self.anchor_cat == 1:
                self.fct1 = 0.65
            elif self.anchor_cat == 2:
                self.fct1 = 0.55
            else:
                self.fct1 = 0.45
            self.fcv1 = 0.70

    def resistance_factors_conc2(self):
        # Table 17.5.3(c) Anchor strength governed by
        # concrete pullout or pryout strength
        if self.anchor_type == 'CI':
            self.fct2 = 0.70
        elif self.anchor_cat == 1:
            self.fct2 = 0.65
        elif self.anchor_cat == 2:
            self.fct2 = 0.55
        else:
            self.fct2 = 0.45
        self.fcv2 = 0.70

    def sec_17_9(self, heff):
        # Minimum anchor spacing
        _d = self.da
        smin = 6*_d

        # Minimum edge distance
        cmin = 6*_d # using Table 19.9.2(b)

        # Critical edge distance
        cac = 4*heff

        return smin, cmin, cac
    
    def sec_17_6_1(self):
        # Nsa = AseN * futa
        AseN = self.Aa
        futa = 75. # hard-coded... red-head
        Nsa = AseN * futa
        return Nsa, AseN, futa

    def sec_17_6_2(self, heff, ca1, ca2, ca3, ca4, s1, s2, nx, ny, FX,FY,FZ,MX,MY,MZ, eTx, eTy):
        # For a single anchor
        # Ncb = (ANc/ANco) * yedN * ycN * ycpN * Nb
        # For a group of anchors
        # Ncbg = (ANc/ANco) * yecN * yedN * ycN * ycpN * Nb

        # Projected influence area of single anchor, not limited by edge dist or spacing
        ANco = 9*heff**2

        nshortsides = 0
        for ca in [ca1, ca2, ca3, ca4]:
            nshortsides += (ca < 1.5*heff)

        if nshortsides >= 3:
            heff = max(ca1/1.5, ca2/1.5, ca3/1.5, ca4/1.5, s1/3, s2/3)

        # Actual influence area anchor group
        x = min(ca1, 1.5*heff) + min(ca3,1.5*heff) + (nx - 1) * s1
        y = min(ca3, 1.5*heff) + min(ca4,1.5*heff) + (ny - 1) * s2
        ANc = x*y

        # Basic single anchor breakout strength
        # Nb = kc * lama * sqrt(f'c)*heff^1.5
        kc = 24 if self.anchor_type=="CI" else 17
        Nb = kc * math.sqrt(self.fc * 1000) *  heff**(1.5) / 1000

        # Breakout eccentricity factor yecN
        eNx = eTx
        eNy = eTy
        
        yecNx, yecNy = [min(1.0,1/(1+eNx/(1.5*heff))),
                min(1.0,1/(1+eNy/(1.5*heff)))]
        
        yecN = min(yecNx, yecNy)

        # Breakout edge effect factor, yedN
        camin = min(ca1, ca2, ca3, ca4)
        if camin >= 1.5*heff:
            yedN = 1.0
        else:
            yedN = 0.7 + 0.3* camin/(1.5*heff)

        # Breakout cracking factor, ycN
        ycN = 1.0 # Assume cracked concrete

        # Breakout splitting factor, ycpN
        ycpN = 1.0 # Assume cracked concrete

        Ncb = (ANc/ANco) * yedN * ycN * ycpN * Nb
        Ncbg = (ANc/ANco) * yecN * yedN * ycN * ycpN * Nb

        return Ncb, Ncbg, ANc, ANco, yecN, yedN, ycN, ycpN, Nb

    def sec_17_6_3(self):
        # Npn = ycP*Np
        Np = 8 * self.Aa * self.fc 

        # Pullout cracking factor ycP
        ycP = 1.0 # Assume cracked concrete
        
        Npn = ycP * Np
        return Np, ycP, Npn

    def sec_17_6_4(self):
        # Reserved for future use --
        # I don't use headed anchors atm...
        pass

    def sec_17_6_5(self):
        # Reserved for future use --
        # I don't use adhesive anchors atm...
        pass


class anchorgroup():
    def __init__(self, da:float, ca1:float, ca2:float, ca3:float, ca4:float, s1:float, s2:float, nx:int, ny:int, FX:float, FY:float, FZ:float, MX:float, MY:float, MZ:float):
        self.da = da
        self.ca1 = ca1
        self.ca2 = ca2
        self.ca3 = ca3
        self.ca4 = ca4
        self.s1 = s1
        self.s2 = s2
        self.nx = nx
        self.ny = ny
        self.FX = FX
        self.FY = FY
        self.FZ = FZ
        self.MX = MX
        self.MY = MY
        self.MZ = MZ

        # Calculated
        self.Ab = math.pi / 4 * da**2 # Area of a single anchor
        self.Lx = (nx - 1) * s1 # Length of group along X axis
        self.Ly = (ny - 1) * s2 # Length of group along Y axis

        # The origin (0,0) is placed arbitrarily at the bottom left anchor center point
        # Calculate the x coordinates of the columns and the y coordinates of the rows
        # self.xcoords = [s1*i for i in range(nx)]
        # self.ycoords = [s2*i for i in range(ny)]

        self.coords = []

        # Iterate by column and fill in the rows, bottom to top, left to right.
        # Calculate each anchor's coordinates
        for j in range(ny):
            for i in range(nx):
                _x = i * s1
                _y = j * s2
                self.coords.append((_x,_y))
        
        # Build the compound geometry.  See sectionproperties documentation for
        # a better explanation.  This is very elegant but took me forever to figure out. 
        for i, c in enumerate(self.coords):
            _x, _y = c
            _anchor = circular_section(d = da, n = 64).shift_section(x_offset = _x, y_offset = _y)
            if i == 0:
                geometry = _anchor
            else:
                geometry = geometry | _anchor

        # Calculate the centroids - all anchor section areas are equal & cancel out
        _xlist = [i[0] for i in list(self.coords)]
        _ylist = [i[1] for i in list(self.coords)]
        
        self.xc = sum(_xlist) / len(_xlist)
        self.yc = sum(_ylist) / len(_ylist)
   
    def calc_I(self):
        '''
        I previously calculated Ix, Iy, et al manually.  There is a perfectly
        beautiful library called sectionproperties available for Python, and
        that uses actual FEA to calculate this stuff.  So yeah, let's do that.      
               
        '''      
        # Loop through the rows and columns and build each anchor.  Each
        # anchor is stored in a list of objects, which will all be added
        # together at the end to create a geometry for sectionproperties

        # Number of points on the circle
        _n = 64    
       
        for i, c in enumerate(self.coords):
            _x, _y = c
            # Create a circular sectionproperties Geometry object
            # with diameter d = self.da and number of discretized segments
            # representing the circle = 64 (for now; can change to make even more accurate)
            # Anchor is also shifted by its x,y coordinates
            _anchor = circular_section(d = self.da, n = _n).shift_section(x_offset=_x,y_offset=_y)
            # If this is the first anchor, create the geometry.  Otherwise, add to it with the union operator.
            if i == 0:
                geometry = _anchor
            else:
                geometry = geometry | _anchor
        
        # Create a mesh with a mesh size proportional to is number of discretizations
        _arcLength = math.pi * self.da / _n
        # Theoretical area of equilateral triangle with side length = _arclength
        _aet = round(math.sqrt(3) / 4 * _arcLength**2)
        
        # Create the mesh and section objects.  
        geometry.create_mesh(mesh_sizes=[.1])
        section = Section(geometry)       
        
        # Have the sectionproperties library do my bidding.
        section.calculate_geometric_properties()
        

        # Extract Ixc and Iyc from sectionproperties
        # 'c' means moment about its geometric centroid
        Ix, Iy, __Ixy = section.get_ic()

        # About the z axis (polar)
        Ip = Ix + Iy

        # Commit to self
        self.Ix = Ix    ;   self.Iy = Iy    ;   self.Ip = Ip

        # Return values for output if desired
        return Ix, Iy, Ip 
   
    def analyze(self):
        # X-X Tension = FZ/(nx*ny) ± MY * x / Iy * Ab
        # Y-Y Tension = FZ/(nx*ny) ± MX * y / Ix * Ab
        # Shear = sqrt(FX^2 + FY^2) ± MZ * r / Ip * Ab

        # Initialize
        Tx = []
        Ty = []
        Vxy = []
        
        # Tension in critical anchor - x direction (FZ + MY)
        for i in range(self.nx):
            x = i * self.s1
            T = self.FZ / (self.nx * self.ny) + self.MY * x * self.Ab / self.Iy
            Tx.append(T)
        
        # Maximum additive tension in critical anchor
        Tcr_x = max(Tx)

        
        # Find the center of tension
        _T = 0.
        for i, t in enumerate(Tx):
            if t > 0:
                _T += t
                _Tx = _T * (i * self.s1)
        eTx = _Tx / _T

        # Tension in critical anchor - y direction (FZ + MX)
        for i in range(self.ny):
            y = i * self.s2
            T = self.FZ / (self.nx * self.ny) + self.MX * y * self.Ab / self.Ix
            Ty.append(T)
        
        # Maximum additive tension in critical anchor
        Tcr_y = max(Ty)
        
        # Find the center of tension
        _T = 0.
        for i, t in enumerate(Ty):
            if t > 0:
                _T += t
                _Ty = _T * (i * self.s2)
        eTy = _Ty / _T

        # Find the XY planar shear (FX + FY + MZ)
        
        for i in range(self.nx):
            for j in range(self.ny):
                _x = i * self.s1
                _y = j * self.s2
                r = math.sqrt(_x**2 + _y**2)
                _V = math.sqrt(self.FX**2 + self.FY**2) / (self.nx * self.ny) + self.MZ * r * self.Ab / self.Ip
                Vxy.append(_V)
        Vcr_xy = max(Vxy)

        # Commit to self
        self.Tx = Tx
        self.Ty = Ty
        self.Vxy = Vxy
        self.Tcr_x = Tcr_x
        self.Tcr_y = Tcr_y
        self.Vcr_xy = Vcr_xy
        self.eTx = eTx
        self.eTy = eTy

        # returns
        return Tx, Ty, Vxy, Tcr_x, Tcr_y, Vcr_xy, eTx, eTy




"""
CLICK IT OR TICK IT, MOTHERFUCKER.
"""

            
def click_button():
    # Get input values
    da = float(input_da.get()) # Anchor diameter
    fy = float(input_fy.get()) # Anchor yield strength
    fc = float(input_fc.get()) # Concrete strength
    suppl_reinf = bool(input_reinf_pres.get()) # Is supplemental reinf present?
    anchor_type = a_type.get() # Type of anchor
    anchor_class = a_class.get() # Class of PI anchor
    ca1 = float(input_ca1.get())
    s1 = float(input_s1.get())
    ca2 = float(input_ca2.get())
    s2 = float(input_s2.get())
    ca3 = float(input_ca3.get())
    ca4 = float(input_ca4.get())
    tp = float(input_tplate.get())
    nx = int(input_nx.get())
    ny = int(input_ny.get())
    heff = float(input_heff.get())

    # Get input loads
    FX = float(input_FX.get())
    FY = float(input_FY.get())
    FZ = float(input_FZ.get())
    MX = float(input_MX.get())
    MY = float(input_MY.get())
    MZ = float(input_MZ.get())

    # Instantiate an anchor object
    a = Anchor(da=da, fy=fy, fc=fc, suppl_reinf=suppl_reinf, anchor_type=anchor_type,
               anchor_cat=anchor_class)

    # Perform an analysis on the anchor group
    # Instantiate a anchorgroup object
    bg = anchorgroup(da,ca1,ca2,ca3,ca4,s1,s2,nx,ny,FX,FY,FZ,MX,MY,MZ)
    # Calculate moments of inertia
    Ix, Iy, Ip = bg.calc_I()
    # Calculate critical forces in anchor group
    Tx, Ty, Vxy, Tcr_x, Tcr_y, Vcr_xy, eTx, eTy = bg.analyze()
    # Set the output values
    out_Ix.set(numfmt.format(Ix))
    out_Iy.set(numfmt.format(Iy))
    out_Ip.set(numfmt.format(Ip))

    out_TxFZ.set(numfmt.format(FZ / (nx*ny)))
    out_TxMY.set(numfmt.format(Tcr_x - FZ / (nx*ny)))
    out_TX.set(numfmt.format(Tcr_x))

    out_TyFZ.set(numfmt.format(FZ / (nx*ny)))
    out_TyMX.set(numfmt.format(Tcr_y - FZ / (nx*ny)))
    out_TY.set(numfmt.format(Tcr_y))

    out_VFX.set(numfmt.format(FX / (nx*ny)))
    out_VFY.set(numfmt.format(FY / (nx*ny)))
    out_VMZ.set(numfmt.format(Vcr_xy - math.sqrt(FX**2 + FY**2)/(nx*ny)))
    out_VXY.set(numfmt.format(Vcr_xy))





        
    # Calculate concrete properties
    a.conc_props()
    
    # Calculate anchor properties
    a.anchor_props()

    # Calculate resistance factors
    a.resistance_factors_steel()
    a.resistance_factors_conc1()
    a.resistance_factors_conc2()

    # Calculate minimum spacing & edge distances
    smin, cmin, cac = a.sec_17_9(heff)
    out_smin.set(numfmt.format(smin))
    out_cmin.set(numfmt.format(cmin))
    out_cac.set(numfmt.format(cac))

    # Calculate nominal strength of anchor in tension
    Nsa, AseN, futa = a.sec_17_6_1()
    # Apply factors
    f_Nsa = Nsa * a.fst
    Nsa_W = f_Nsa / 1.5
    out_Nsa.set(numfmt.format(Nsa))
    out_AseN.set(numfmt.format(AseN))
    out_futa.set(numfmt.format(futa))
    out_f_Nsa.set(numfmt.format(f_Nsa))
    out_Nsa_W.set(numfmt.format(Nsa_W))
    
    # Calculate concrete breakout strength of anchors in tension
    Ncb, Ncbg, ANc, ANco, yecN, yedN, ycN, ycpN, Nb = a.sec_17_6_2(heff, ca1, ca2, ca3, ca4, s1, s2, nx, ny, FX,FY,FZ,MX,MY,MZ, eTx, eTy)
    f_Ncb, f_Ncbg = [Ncb*a.fct1, Ncbg*a.fct1]
    Ncb_W, Ncbg_W = [f_Ncb / 1.5, f_Ncbg / 1.5]
      
    out_Ncb.set(numfmt.format(Ncb))
    out_Ncbg.set(numfmt.format(Ncbg))
    out_f_Ncb.set(numfmt.format(f_Ncb))
    out_f_Ncbg.set(numfmt.format(f_Ncbg))
    out_Ncb_W.set(numfmt.format(Ncb_W))
    out_Ncbg_W.set(numfmt.format(Ncbg_W))
    # Ncb, Ncbg, ANc, ANco, yecN, yedN, ycN, ycpN, Nb
    out_ANc.set(numfmt.format(ANc))
    out_ANco.set(numfmt.format(ANco))
    out_yecN.set(numfmt.format(yecN))
    out_yedN.set(numfmt.format(yedN))
    out_ycN.set(numfmt.format(ycN))
    out_ycpN.set(numfmt.format(ycpN))
    out_Nb.set(numfmt.format(Nb))

    # Calculate pullout strength of a single anchor
    Np, ycP, Npn = a.sec_17_6_3()
    f_Npn = a.fct2 * Npn
    Npn_W = f_Npn / 1.5
    # Populate output variables
    out_Np.set(numfmt.format(Np))
    out_ycP.set(numfmt.format(ycP))
    out_Npn.set(numfmt.format(Npn))
    out_f_Npn.set(numfmt.format(f_Npn))
    out_Npn_W.set(numfmt.format(Npn_W))







# Build the UI with tkinter
# Instantiate the global object, window
window = tk.Tk()
window.title('Analysis of Post-Installed Anchors')
window.geometry("1040x900")
window.iconbitmap(r"images\Will-High.ico")

# Define the notebook for tabs
notebook = ttk.Notebook(window)
notebook.pack()

# Create tabs
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Input")

tab3 = ttk.Frame(notebook)
notebook.add(tab3, text='Analysis')

tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Output")






# tab1.configure(bg='#005DAA')
# VDOTblue_bgcolor = '#005DAA'

"""
INPUT NEEDS
- LIGHTWEIGHT CONCRETE INDICATOR (CHKBOX?)
- ANCHOR DIAMETER (IN) ✔ 
- EFFECTIVE EMBEDMENT DEPTH (IN) ✔ 
- CAST IN/POST-INSTALLED ✔ 
- CLASS OF PI ANCHOR (1,2, OR 3) ✔ 
- IS REINFORCEMENT PRESENT (CHKBOX?) ✔ 
- FORCES AND MOMENTS

STRENGTH CALCULATIONS PER §17.5.1.2:
A. STEEL STRENGTH OF CONCRETE IN TENSION (17.6.1) ✔ 
B. CONCRETE BREAKOUT STRENGTH OF ANCHOR IN TENSION (17.6.2) ✔ 
C. PULLOUT STRENGTH OF A SINGLE CAST-IN ANCHOR AND SINGLE (17.6.3) ✔ 
   POST-INSTALLED EXPANSION, SCREW, AND UNDERCUT ANCHOR IN TENSION 
D. CONCRETE SIDE-FACE BLOWOUT STRENGTH OF HEADED ANCHOR IN TENSION (17.6.4) ⚠ skip it...
E. BOND STRENGTH OF ADHESIVE ANCHOR IN TENSION (17.6.5) ⚠ skip it...
F. STEEL STRENGTH OF ANCHOR IN SHEAR (17.7.1)
G. CONCRETE BREAKOUT STRENGTH OF ANCHOR IN SHEAR (17.7.2)
H. CONCRETE PRYOUT STRENGTH OF ANCHOR IN SHEAR (17.7.3)

ANCHOR GROUP EFFECTS PER § 17.5.1.3
CRITICAL SPACING


"""
# Define text sizes
large = ('Arial',14,"bold")
medium = ('Arial',12)
medbold = ('Arial',12,"bold")
small = ('Arial',10)
vsmall = ('Arial',8)




# Building the input tab

# Define the starting row/column of the grid
row = 0    ;   col = 0

# Populate default values
dad, fcd, fyd, _futad, heffd, anchor_catd, tpld = default_values()


"""
Oh hells yeah, big dog.  It's time for the inputs!
What what!!

There's probably a better way to do this, but I like
the grid() method rather than the pack() style.
That's just how I get down.

So yeah, I"m keeping a row and col counter so I can move shit
around without finger punching rows and columns manually like a bitch.
Wiggy wiggy.

What's up.


LFG.
"""

tk.Label(tab1,text='Let\'s Do This, Ace.',font=large).grid(row=row,column=col,sticky="NW")
row =+ 1

# Helper graphic
image = Image.open(r'images\anchorgrp.PNG')
img = image.resize((365,305))
my_img=ImageTk.PhotoImage(img)
lpic1 = tk.Label(tab1,image=my_img)
lpic1.grid(row=0,column=3,rowspan=10)


# Anchor Diameter Input
tk.Label(tab1,text='Material and Geometry',font=medbold).grid(row=row,column=col,sticky="NW")
row += 1
input_da = tk.DoubleVar()
input_da.set(numfmt.format(dad))
tk.Label(tab1,text='Anchor diameter (in), da =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_da,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0

# Concrete Strength Input
input_fc = tk.DoubleVar()
input_fc.set(numfmt.format(fcd))
tk.Label(tab1,text='Concrete strength (ksi), f\'c =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_fc,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Anchor Yield Strength Input
input_fy = tk.DoubleVar()
input_fy.set(numfmt.format(fyd))
tk.Label(tab1,text='Anchor yield strength (ksi), fy =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_fy,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Reinforcement present Input
input_reinf_pres = tk.IntVar()
input_reinf_pres.set(1)
tk.Label(tab1,text='Supplemental Reinforcement Present?',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Checkbutton(tab1,variable=input_reinf_pres, onvalue=1, offvalue=0, font=medium).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Cracked section Input - TODO: make this actually do something... Just look at my cousin.  He's broke; don't do shit.
# input_cracked_section = tk.IntVar()
# input_cracked_section.set(1)
# tk.Label(tab1,text='Cracked Section?',font=medium).grid(row=row,column=col,sticky="NE")
# col =+ 1
# tk.Checkbutton(tab1,variable=input_cracked_section, onvalue=1, offvalue=0, font=medium).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col =0

# space
tk.Label(tab1,text=" ",font=large).grid(row=row,column=col, sticky="NW")
row += 1

# Anchor Heading
tk.Label(tab1,text="Anchors", font=medbold).grid(row=row,column=col,sticky="NW")
row += 1

# Anchor type Input
a_type = tk.StringVar()
a_type_options = ["CI", "PI"]
a_type.set("PI")
tk.Label(tab1,text='Select Anchor Type',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.OptionMenu(tab1,a_type,*a_type_options).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0


# Anchor Class Input
a_class = tk.IntVar()
a_class_options = [1,2,3]
a_class.set(1)
tk.Label(tab1,text='Select Anchor Class',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.OptionMenu(tab1,a_class,*a_class_options).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Effective depth
input_heff = tk.DoubleVar()
input_heff.set(numfmt.format(heffd))
tk.Label(tab1,text='Effective embedment depth (in), heff =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_heff,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# ca1 Input
input_ca1 = tk.DoubleVar()
input_ca1.set(999.0)
tk.Label(tab1,text='East Edge Dist (in), ca1 =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_ca1,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# ca3 Input
input_ca3 = tk.DoubleVar()
input_ca3.set(999.0)
tk.Label(tab1,text='West Edge Dist (in), ca3 =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_ca3,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# ca2 Input
input_ca2 = tk.DoubleVar()
input_ca2.set(999.0)
tk.Label(tab1,text='North Edge Dist (in), ca2 =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_ca2,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# ca4 Input
input_ca4 = tk.DoubleVar()
input_ca4.set(999.0)
tk.Label(tab1,text='South Edge Dist (in), ca4 =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_ca4,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# s1 Input
input_s1 = tk.DoubleVar()
input_s1.set(5.)
tk.Label(tab1,text='West-East Spacing (in), s1 =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_s1,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# s2 Input
input_s2 = tk.DoubleVar()
input_s2.set(5.)
tk.Label(tab1,text='North-South Spacing (in), s2 =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_s2,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Number of anchors in x Input
input_nx = tk.IntVar()
input_nx.set(2)
tk.Label(tab1,text='Number of east-west anchors, nx =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_nx,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Number of anchors input_FXin y Input
input_ny = tk.IntVar()
input_ny.set(1)
tk.Label(tab1,text='Number of north-south anchors, ny =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_ny,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Plate Thickness Input
input_tplate = tk.DoubleVar()
input_tplate.set(tpld)
tk.Label(tab1,text='Plate Thickness (in), tp =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_tplate,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Space, then Forces Heading
tk.Label(tab1,text=" ",font=large).grid(row=row,column=col,sticky="NW")
row +=1 ;   col = 0
tk.Label(tab1,text="Forces",font=medbold).grid(row=row,column=col,sticky="NW")
row +=1

# FX
input_FX = tk.DoubleVar()
input_FX.set(10)
tk.Label(tab1,text='FX (shear) (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_FX,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# FY
input_FY = tk.DoubleVar()
input_FY.set(0)
tk.Label(tab1,text='FY (shear) (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_FY,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# FZ
input_FZ = tk.DoubleVar()
input_FZ.set(20)
tk.Label(tab1,text='FZ (axial) (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_FZ,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# MX
input_MX = tk.DoubleVar()
input_MX.set(0)
tk.Label(tab1,text='MX (north-south moment) (kip-ft) =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_MX,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# MY
input_MY = tk.DoubleVar()
input_MY.set(0)
tk.Label(tab1,text='MY (east-west moment) (kip-ft) =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_MY,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# MZ
input_MZ = tk.DoubleVar()
input_MZ.set(0)
tk.Label(tab1,text='MZ (torsion) (kip-ft) =',font=medium).grid(row=row,column=col,sticky="NE")
col =+ 1
tk.Entry(tab1,textvariable=input_MZ,font=medium, width=6).grid(row=row,column=col,sticky="NW")
row += 1    ;   col =0

# Calculate button
tk.Button(tab1,text="CALCULATE",font=large,command=click_button).grid(row=row,column=col)


"""

TAB 3, OR IS IT TAB 2.
ANALYSIS RESULTS TAB!!

"""
# Create a frame so this can scroll
def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas3 = tk.Canvas(tab3, borderwidth=0)
frame3 = tk.Frame(canvas3)
vsb3 = tk.Scrollbar(canvas3, orient="vertical", command=canvas3.yview)
canvas3.configure(yscrollcommand=vsb3.set)
vsb3.pack(side="right", fill="y")
canvas3.pack(side="left", fill="both", expand=True)
canvas3.create_window((4,4),window=frame3, anchor="nw")
frame3.bind("<Configure>", lambda event, canvas3=canvas3: onFrameConfigure(canvas3))





# Starting row & column.  New tab, new day!
row = 0 ;   col = 0
tk.Label(frame3,text='Anchor Group Analysis',font=large).grid(row=row,column=col,sticky="NW")
row += 1
tk.Label(frame3,text=' ',font=large).grid(row=row,column=col,sticky="NW")
row += 1

# Section properties gang
out_Ix = tk.StringVar()
out_Iy = tk.StringVar()
out_Ip = tk.StringVar()

tk.Label(frame3,text='Anchor Group Properties',font=medbold).grid(row=row,column=col,sticky="NW")
row += 1
tk.Label(frame3,text='Number of Anchors in the X direction, nx =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=input_nx,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Anchor spacing in the X direction (in), s1 =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=input_s1,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Number of Anchors in the Y direction, ny =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=input_ny,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Anchor spacing in the Y direction (in), s2 =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=input_s2,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Moment of Inertia about the Y-Y axis (in4), Iy =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_Iy,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Moment of Inertia about the X-X axis (in4), Ix =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_Ix,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Polar Moment (in4), Ip =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_Ip,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1





# X-X Direction
# De lare variables dawg.  Where'd the c go?
out_TxFZ = tk.StringVar()
out_TxMY = tk.StringVar()
out_TX = tk.StringVar()

tk.Label(frame3,text='Tension, X-X Axis',font=medbold).grid(row=row,column=col,sticky="NW")
row += 1
tk.Label(frame3,text='Uniform Tension Per Anchor from FZ (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_TxFZ,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Max. Tension Due to MY (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_TxMY,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Governing Tension (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_TX,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text=' ',font=medbold).grid(row=row,column=col,sticky="NW")
row += 1

# Y-Y Direction
# Declare variables
out_TyFZ = tk.StringVar()
out_TyMX = tk.StringVar()
out_TY = tk.StringVar()

tk.Label(frame3,text='Tension, Y-Y Axis',font=medbold).grid(row=row,column=col,sticky="NW")
row += 1
tk.Label(frame3,text='Uniform Tension Per Anchor from FZ (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_TyFZ,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Max. Tension Due to MX (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_TyMX,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Governing Tension (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_TY,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text=' ',font=medbold).grid(row=row,column=col,sticky="NW")
row += 1

# X-Y Shear Plane
# Declare variables
out_VFX = tk.StringVar()
out_VFY = tk.StringVar()
out_VMZ = tk.StringVar()
out_VXY = tk.StringVar()

tk.Label(frame3,text='Shear, X-Y Plane',font=medbold).grid(row=row,column=col,sticky="NW")
row += 1
tk.Label(frame3,text='Uniform Shear Per Anchor from FX (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_VFX,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Uniform Shear Per Anchor from FY (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_VFY,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Shear in Critical Anchor from MZ (kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_VMZ,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text='Governing Shear in Critical Anchor(kip) =',font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame3,textvariable=out_VXY,font=medium,state="readonly",relief="solid",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col -= 1
tk.Label(frame3,text=' ',font=medbold).grid(row=row,column=col,sticky="NW")
row += 1



























"""
# Build the output tab
FUCK YEAH, OUTPUT!!

\m/  \m/


Uncomment the additional variables if you want.  I couldn't figure out how to scroll
with tkinter, so it all needs to fit on one screen.  Fug.

"""
# Make it scroll dude.
# Create a frame so this can scroll

canvas2 = tk.Canvas(tab2, borderwidth=0)
frame2 = tk.Frame(canvas2)
vsb2 = tk.Scrollbar(canvas2, orient="vertical", command=canvas2.yview)
canvas2.configure(yscrollcommand=vsb2.set)
vsb2.pack(side="right", fill="y")
canvas2.pack(side="left", fill="both", expand=True)
canvas2.create_window((4,4),window=frame2, anchor="nw")
frame2.bind("<Configure>", lambda event, canvas2=canvas2: onFrameConfigure(canvas2))



# Populate some output homes!!
tk.Label(frame2,text=" ",font=large).grid(row=0,column=2)

row = 0 ;   col = 0

tk.Label(frame2,text="Output",font=large).grid(row=row,column=col,sticky="NW")
row += 1    

# Populate min edge dist & spacing
out_smin = tk.StringVar()
out_cmin = tk.StringVar()
out_cac = tk.StringVar()

tk.Label(frame2,text="Minimum Spacing and Edge Distances (§17.9.2)",font=medbold).grid(row=row,column=col,sticky="NE")
row += 1
tk.Label(frame2,text="Minimum Spacing, smin (in) =",font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame2,textvariable=out_smin,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text="Minimum Edge Distance, cmin (in) =",font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame2,textvariable=out_cmin,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text="Critical Edge Distance, cac (in) =",font=medium).grid(row=row,column=col,sticky="NE")
col +=1
tk.Entry(frame2,textvariable=out_cac,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text=" ",font=medium).grid(row=row,column=col,sticky="NW")
row +=1

# Results for 17.6.1
tk.Label(frame2,text="Steel Strength of Anchor in Tension (§17.6.1)",font=medbold).grid(row=row,column=col,sticky="NE")
# row +=1 
out_Nsa = tk.StringVar()
out_AseN = tk.StringVar()
out_futa = tk.StringVar()
out_f_Nsa = tk.StringVar()
out_Nsa_W = tk.StringVar()
# tk.Label(frame2,text="AseN (in2) =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_AseN,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
# tk.Label(frame2,text="futa (ksi) =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_futa,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text="Nsa (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_Nsa,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text="𝜙Nsa (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_f_Nsa,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text="Nsa / Ω (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_Nsa_W,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text=" ",font=large).grid(row=row,column=col,sticky="NE")
row += 1    ;   col = 0


# Results for 17.6.2
tk.Label(frame2,text="Concrete Breakout Strength of Anchor in Tension (§17.6.2)",font=medbold).grid(row=row,column=col,sticky="NE")
# row +=1 
out_ANc = tk.DoubleVar()
# # tk.Label(frame2,text="ANc (in2) =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_ANc,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
out_ANco = tk.DoubleVar()
# tk.Label(frame2,text="ANco (in2) =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_ANco,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
out_yecN = tk.DoubleVar()
# tk.Label(frame2,text="𝜓ecN =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_yecN,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
out_yedN = tk.DoubleVar()
# tk.Label(frame2,text="𝜓edN =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_yedN,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
out_ycN = tk.DoubleVar()
# tk.Label(frame2,text="𝜓cN =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_ycN,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
out_ycpN = tk.DoubleVar()
# tk.Label(frame2,text="𝜓cpN =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_ycpN,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
out_Nb = tk.DoubleVar()
# tk.Label(frame2,text="Nb (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_Nb,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
out_Ncb = tk.DoubleVar()
tk.Label(frame2,text="Single Anchor, Ncb (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_Ncb,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
out_f_Ncb = tk.DoubleVar()
tk.Label(frame2,text="Single Anchor, 𝜙Ncb (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_f_Ncb,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
out_Ncb_W = tk.DoubleVar()
tk.Label(frame2,text="Single Anchor, Ncb / Ω (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_Ncb_W,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
out_Ncbg = tk.DoubleVar()
tk.Label(frame2,text="Anchors as a Group, Ncbg (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_Ncbg,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
out_f_Ncbg = tk.DoubleVar()
tk.Label(frame2,text="Anchors as a Group, 𝜙Ncb (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_f_Ncbg,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
out_Ncbg_W = tk.DoubleVar()
tk.Label(frame2,text="Anchors as a Group, Ncb / Ω (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_Ncbg_W,font=medium,state="readonly",width=8,relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text=" ",font=large).grid(row=row,column=col,sticky="NE")
row += 1    ;   col = 0

# Results for 17.6.3
tk.Label(frame2,text="Pullout Strength of a Single CI or PI Anchor in Tension (§17.6.3)",font=medbold).grid(row=row,column=col,sticky="NE")
row +=1 
out_Np = tk.StringVar()
out_ycP = tk.StringVar()
out_Npn = tk.StringVar()
out_f_Npn = tk.StringVar()
out_Npn_W = tk.StringVar()

# tk.Label(frame2,text="Np (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_Np,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
# tk.Label(frame2,text="𝜓cP =", font=medium).grid(row=row,column=col,sticky="NE")
# col += 1
# tk.Entry(frame2,textvariable=out_ycP,font=medium,state="readonly",width=8).grid(row=row,column=col,sticky="NW")
# row += 1    ;   col = 0
tk.Label(frame2,text="Npn (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_Npn,font=medium,state="readonly",width=8, relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text="𝜙Npn (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_f_Npn,font=medium,state="readonly",width=8, relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text="Npn / Ω (kip) =", font=medium).grid(row=row,column=col,sticky="NE")
col += 1
tk.Entry(frame2,textvariable=out_Npn_W,font=medium,state="readonly",width=8, relief="solid").grid(row=row,column=col,sticky="NW")
row += 1    ;   col = 0
tk.Label(frame2,text=" ", font=medium).grid(row=row,column=col,sticky="NE")
row += 1    ;   col = 0






window.mainloop()









