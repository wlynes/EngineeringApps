# Depandapotomus
from dirsync import sync
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from contextlib import redirect_stdout
import os
from datetime import datetime

class App():
    """The application object
    """
    def __init__(self, master):
        """Initializes the App object

        Args:
            master (tk Object): The window object
        """
        self.master = master
        self.sauce = tk.StringVar()
        self.destiny = tk.StringVar()
        self.init_widgets()
        
    def init_widgets(self):
        """Initializes the widgets upon calling the App object
        """
        self.master.title("Folder Sync\'r \'n Litter Gitt\'r")
        self.master.geometry('400x200')
        self.master.iconbitmap("images\Will-High.ico")
        self.color1 = "#3D7A97" # Steel Manual Blue
        self.color2 = '#000000' # black
        self.f = ('Arial', 14)
        self.master.tk_setPalette(background=self.color1, foreground=self.color2)
     
        # Buttons
        tk.Button(self.master,text="Select SOURCE Folder",command=self.clickSource,font=self.f).pack(expand=True,fill='both')
        tk.Entry(self.master,textvariable=self.sauce,font=self.f,background=self.color2,foreground=self.color1).pack(expand=True,fill='both')
        tk.Button(self.master,text="Select DESTINATION Folder",command=self.clickDestination,font=self.f).pack(expand=True,fill='both')
        tk.Entry(self.master,textvariable=self.destiny,background=self.color2,foreground=self.color1,font=self.f).pack(expand=True,fill='both')
        tk.Button(self.master,text="DO IT!",command=self.doIt,font=self.f).pack(side='bottom',expand=True,fill='both')

    def clickSource(self):
        self.theway = rf'{filedialog.askdirectory()}'
        self.sauce.set(self.theway)
    
    def clickDestination(self):
        self.theway2 = rf'{filedialog.askdirectory()}'
        self.destiny.set(self.theway2)

    def doIt(self):
        _sauce = self.sauce.get()
        _destiny = self.destiny.get()
        
        # Create a text file name
        self.outpath = _destiny
        self.username = os.getlogin()
        self.now = datetime.now().strftime('%Y-%m-%d_%H%M%S')
        self.outname = self.outpath + "/" + "LAST UPDATED_" + self.now + '_' + self.username + '.txt'
        self.newfilename = rf'{self.outname}'

        with open(self.newfilename, 'w') as filzz:
            with redirect_stdout(filzz):
                sync(_sauce,_destiny,'sync',purge=True,verbose=False)

        messagebox.showinfo(title='Success!',message='Aww yeah, keepin\' it fresh.\nKeepin\' it real.')

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

main()