import tkinter as tk
from PIL import Image, ImageTk
import math

window = tk.Tk()
window.title('Quick Anchor Bolt Moment Capacity Calculations')
window.geometry("700x425")
window.iconbitmap(r"images\Will-High.ico")

# import a demo image
image = Image.open('images/absection.png')
img = image.resize((400,300))
my_img=ImageTk.PhotoImage(img)


# Define Big, Med, and Small Text Styles
class ts():
    def __init__(self,font='Arial'):
        self.font = font
        pass
    def big(self):
        return (self.font,16)
    def med(self):
        return (self.font,14)
    def small(self):
        return (self.font,12)

class DefaultValues:
    def __init__(self) -> None:
        self.h:float = 34
        self.b:float = 24
        self.dclr:float = 2.5
        self.dbar:float = 1.5
        self.fc:float = 3.5
        self.fy:float = 53.7

fnt = ts('Arial')
big = fnt.big()
med = fnt.med()
reg = fnt.small()

desmethods = ['ASD','LRFD']

# Grown Man Business
class SectionAnalysis():
    def __init__(self,b,h,dclr,dbar,fc,fy,method):
        self.b = b
        self.h = h
        self.dclr = dclr
        self.dbar = dbar
        self.fc = fc
        self.fy = fy
        self.method = method
    
    def E(self):
        return 57000 * math.sqrt(self.fc*1000) / 1000

    def beta1(self):
        if self.fc <= 4.0:
            return 0.85
        elif self.fc < 8.0:
            return 0.85 - ((0.05*(self.fc-4.0)))
        else:
            return 0.65

    def As(self):
        dbar = self.dbar
        return math.pi / 4 * dbar**2
    
    def DoIt(self):
        E = self.E()
        beta1 = self.beta1()

        # Calculate tension force at fy
        T = 2* self.As() * self.fy
        
        # Depth of concrete stress block
        # Neglecting compression steel
        ay = T / (0.85*self.fc*self.b)
        ax = T / (0.85*self.fc*self.h)

        dy = self.h - self.dclr
        dx = self.b - self.dclr

        Mnx = T * (dy - ay/2)
        Mny = T * (dx - ax/2)

        return Mnx, Mny

def calculate():
    fc = float(e6entry.get())
    b = float(e2entry.get())
    h = float(e3entry.get())
    dclr = float(e4entry.get())
    dbar = float(e5entry.get())
    fy = float(e7entry.get())
    

    section = SectionAnalysis(b,h,dclr,dbar,fc,fy,'LRFD')
    Mnx, Mny = section.DoIt()
    Mnx = Mnx / 12  ;   Mny = Mny / 12 # Convert to kip-ft
    
    outputMx.set("{:.2f}".format(Mnx))
    outputMy.set("{:.2f}".format(Mny))

    _mnx_W.set("{:.2f}".format(Mnx / 1.67))
    _mny_W.set("{:.2f}".format(Mny / 1.67))


l1 = tk.Label(window, text='Define Section Parameters',font=big)
l1.grid(row=0,column=0, columnspan=2)

lpic1 = tk.Label(window,image=my_img)
lpic1.grid(row=0,column=3,rowspan=10, columnspan=4)

units = ['in','in','in','in','ksi','ksi',' ']
l2 = tk.Label(window, text = 'b =', font=med)
l3 = tk.Label(window, text = 'h =', font=med)
l4 = tk.Label(window, text = 'dclr =', font=med)
l5 = tk.Label(window, text = 'dbar =', font=med)
l6 = tk.Label(window, text = "f'c =", font=med)
l7 = tk.Label(window, text = 'fy =', font=med)


for i, label in enumerate([l2, l3, l4, l5, l6, l7]):
    label.grid(row=i+2,column=0, pady=2, padx=2,sticky='E')

default = DefaultValues()
e2entry = tk.DoubleVar(window,value=default.b)
e3entry = tk.DoubleVar(window,value=default.h)
e4entry = tk.DoubleVar(window,value=default.dclr)
e5entry = tk.DoubleVar(window,value=default.dbar)
e6entry = tk.DoubleVar(window,value=default.fc)
e7entry = tk.DoubleVar(window,value=default.fy)



e2 = tk.Entry(window,font=med,width=8, textvariable=e2entry)
e3 = tk.Entry(window,font=med,width=8, textvariable=e3entry)
e4 = tk.Entry(window,font=med,width=8, textvariable=e4entry)
e5 = tk.Entry(window,font=med,width=8, textvariable=e5entry)
e6 = tk.Entry(window,font=med,width=8, textvariable=e6entry)
e7 = tk.Entry(window,font=med,width=8, textvariable=e7entry)


for i, label in enumerate([e2, e3, e4, e5, e6, e7]):
    label.grid(row=i+2,column=1, pady=2, padx=2,sticky="W")

for i, unit in enumerate(units):
    (tk.Label(window,text=unit,font=med)).grid(row=i+2,column=2,pady=2,padx=2,sticky='W')


b1 = tk.Button(window,text='Calculate',font=big,command=calculate)
b1.grid(row=9,column=0, columnspan=3)

(tk.Label(window, text=" ", font=med, width=4)).grid(row=10,column=0)
l9 = tk.Label(window, text='Results', font=big)
l9.grid(row=11,column=0, sticky="W")

tk.Label(window,text=" ").grid(row=10, column=3)



l10 = tk.Label(window, text = 'Mnx =',font=med)
l10.grid(row=12,column=0,sticky='E')

tk.Label(window, text="Mnx / Ω =",font=med).grid(row=12,column=3,sticky='E')
_mnx_W = tk.StringVar()
_mny_W = tk.StringVar()
tk.Entry(window, font=med, state="readonly", width=8, textvariable=_mnx_W).grid(row=12, column=4, sticky="W")
tk.Label(window, text="kip-ft",font=med).grid(row=12,column=5,sticky='W')

l11 = tk.Label(window, text = 'Mny =',font=med)
l11.grid(row=13,column=0,sticky='E')

tk.Label(window, text="Mny / Ω =",font=med).grid(row=13,column=3,sticky='E')
tk.Entry(window, font=med, state="readonly", width=8, textvariable=_mny_W).grid(row=13, column=4, sticky="W")
tk.Label(window, text="kip-ft",font=med).grid(row=13,column=5,sticky='W')

l12 = tk.Label(window, text = 'kip-ft',font=med)
l12.grid(row=12,column=2,sticky='W')

l13 = tk.Label(window, text = 'kip-ft',font=med)
l13.grid(row=13,column=2,sticky='W')

outputMx = tk.StringVar()
outputMy = tk.StringVar()

l14 = tk.Entry(window, textvariable=outputMx, state='readonly',font=med,width=8)
l14.grid(row=12,column=1,sticky="W")

l15 = tk.Entry(window, textvariable=outputMy, state='readonly',font=med,width=8)
l15.grid(row=13,column=1,sticky="W")




window.mainloop()