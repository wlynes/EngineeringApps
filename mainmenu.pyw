#! r"C:\Users\wlynes\Documents\Python\custommenu\Scripts\python"

import tkinter as tk
import subprocess

def script1():
    # subprocess.run(["startupconverter.exe"])
    subprocess.Popen(["python","FeetInches.py"],
                      creationflags=subprocess.CREATE_NO_WINDOW)
def script2():
    # subprocess.run(["concprops.exe"])
    subprocess.Popen(["python","concprops.py"],
                      creationflags=subprocess.CREATE_NO_WINDOW)
def script3():
    # subprocess.run(["anchorbolts.exe"])
    subprocess.Popen(["python","anchorboltreax.py"],
                      creationflags=subprocess.CREATE_NO_WINDOW)
def script4():
    # subprocess.run(["aisclookup.exe"])
    subprocess.Popen(["python","aisclookup.py"],
                      creationflags=subprocess.CREATE_NO_WINDOW)
def script5():
    subprocess.Popen(["python","RC_Interaction.py"],
                      creationflags=subprocess.CREATE_NO_WINDOW)
def script6():
    subprocess.Popen(["python","anchors_aci-ch17.py"],
                      creationflags=subprocess.CREATE_NO_WINDOW)

fs = ('Helvetica',16)

# Create the main window
root = tk.Tk()
root.title("Remote")
root.geometry("225x395")
# root.iconbitmap(r"C:\Users\wlynes\OneDrive - high.net\Templates\Icons\Will-High.ico")
root.iconbitmap("images\Will-High.ico")

# Create the buttons and pack them into the window
button1 = tk.Button(root, text="ft'-in\" to f.eet'", font=fs,command=script1,height=2,width=20)
button1.pack()

button4 = tk.Button(root, text="AISC Shapes Lookup", command=script4,height=2,width=20,font=fs)
button4.pack()

button3 = tk.Button(root, text="Anchor Bolt Reactions", command=script3,height=2,width=20,font=fs)
button3.pack()

button6 = tk.Button(root, text="Anchoring to Concrete", command=script6,height=2,width=20,font=fs)
button6.pack()

button2 = tk.Button(root, text="Concrete Properties", command=script2,height=2,width=20,font=fs)
button2.pack()

button5 = tk.Button(root, text="RC Interaction", command=script5,height=2,width=20,font=fs)
button5.pack()

# Run the main loop
root.mainloop()