# Depandapotomus
from dirsync import sync
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from contextlib import redirect_stdout
import os
from datetime import datetime

window = tk.Tk()
window.title('Folder Sync\'r \'n Litter Gitt\'r')
window.geometry('400x200')
window.iconbitmap("images\Will-High.ico")
color2 = '#000000' # black
color1 = "#3D7A97" # Steel Manual Blue
f = ('Arial', 14)
window.tk_setPalette(background=color1, foreground=color2)

# rfpath = lambda: rf'{filedialog.askdirectory()}'
sauce = tk.StringVar()
destiny = tk.StringVar()

def clickSource():
    theway = rf'{filedialog.askdirectory()}'
    sauce.set(theway)

def clickDestination():
    theway2 = rf'{filedialog.askdirectory()}'
    destiny.set(theway2)

def doIt():
    _sauce = sauce.get()
    _destiny = destiny.get()
      

    # Create a text file name
    outpath = _destiny
    username = os.getlogin()
    now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
    outname = outpath + "/" + "__UPDATE_" + now + '_' + username + '.txt'
    newfilename = rf'{outname}'

    with open(newfilename, 'w') as filzz:
        with redirect_stdout(filzz):
            sync(_sauce,_destiny,'sync',purge=True,verbose=True)

    messagebox.showinfo(title='Success!',message='Aww yeah, keepin\' it fresh.\nKeepin\' it real.')





tk.Button(window,text="Select SOURCE Folder",command=clickSource,font=f).pack(expand=True,fill='both')
tk.Entry(window,textvariable=sauce,font=f,background=color2,foreground=color1).pack(expand=True,fill='both')
tk.Button(window,text="Select DESTINATION Folder",command=clickDestination,font=f).pack(expand=True,fill='both')
tk.Entry(window,textvariable=destiny,background=color2,foreground=color1,font=f).pack(expand=True,fill='both')
tk.Button(window,text="DO IT!",command=doIt,font=f).pack(side='bottom',expand=True,fill='both')



window.mainloop()

