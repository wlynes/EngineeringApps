import tkinter as tk
from tkinter.ttk import *
import math

window = tk.Tk()
window.title('Basic Concrete Properties')
window.iconbitmap(r"images\Will-High.ico")

class properties():
    def __init__(self, fc):
        self.fc = fc

    def E(self):
        return 57000 * math.sqrt(self.fc*1000) / 1000

    def beta1(self):
        if self.fc <= 4.0:
            return 0.85
        elif self.fc < 8.0:
            return 0.85 - ((0.05*(self.fc-4.0)))
        else:
            return 0.65
    
    def fr(self):
        return 7.5 * math.sqrt(self.fc * 1000) / 1000

fs = ('Helvetica',14)
    
label1 = tk.Label(window, text="f'c (ksi) = ",font=fs)
entry1 = tk.Entry(window, font=fs)

# Grid method
label1.grid(row = 0, column = 0, sticky = 'W', pady = 2)
entry1.grid(row = 0, column = 1, pady = 2)


def calculate():
    fc = float(entry1.get())
    props = properties(fc)
    E = props.E()
    beta1 = props.beta1()
    fr = props.fr()
    
    output1.set("{:.2f}".format(E))
    output2.set("{:.2f}".format(beta1))
    output3.set("{:.3f}".format(fr))
    

button = tk.Button(window, text='Calculate', command=calculate, font=fs)
button.grid(row = 0, column = 2)

label2 = tk.Label(window, text='Results', font=fs)
label2.grid(row=2,column=1,pady=2)

l3 = tk.Label(window,text='Ec = ', font=fs)
l3.grid(row=3,column=0, pady=2)

output1 = tk.StringVar()
output2 = tk.StringVar()
output3 = tk.StringVar()

outputbox1 = tk.Entry(window, textvariable=output1, state="readonly", font=fs)
outputbox1.grid(row=3,column=1,pady=2)

l4 = tk.Label(window,text='β1 = ', font=fs)
l4.grid(row=4,column=0, pady=2)
outputbox2 = tk.Entry(window, textvariable=output2, state="readonly", font=fs)
outputbox2.grid(row=4,column=1,pady=2)

l5 = tk.Label(window,text='fr = ', font=fs)
l5.grid(row=5,column=0, pady=2)
outputbox3 = tk.Entry(window, textvariable=output3, state="readonly", font=fs)
outputbox3.grid(row=5,column=1,pady=2)

l6 = tk.Label(window,text="ksi",font=fs)
l6.grid(row=3,column=2,pady=2)
l7 = tk.Label(window,text="ksi",font=fs)
l7.grid(row=5,column=2,pady=2)


window.mainloop()




"""
input:  f'c (ksi)
output:
E = 57000 * sqrt(f'c) / 1000 --> ksi
beta1 = whatever the fuck tkhat equation is
Modulus of rupture = 7.5 sqrt(f'c)





"""