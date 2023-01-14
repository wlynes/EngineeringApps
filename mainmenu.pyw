#! r"C:\Users\wlynes\Documents\Python\custommenu\Scripts\python"

import tkinter as tk
import subprocess


def script1():
    # subprocess.run(["startupconverter.exe"])
    subprocess.Popen(["python", "FeetInches.py"],
                     creationflags=subprocess.CREATE_NO_WINDOW)


def script2():
    # subprocess.run(["concprops.exe"])
    subprocess.Popen(["python", "concprops.py"],
                     creationflags=subprocess.CREATE_NO_WINDOW)


def script3():
    # subprocess.run(["anchorbolts.exe"])
    subprocess.Popen(["python", "anchorboltreax.py"],
                     creationflags=subprocess.CREATE_NO_WINDOW)


def script4():
    # subprocess.run(["aisclookup.exe"])
    subprocess.Popen(["python", "aisclookup.py"],
                     creationflags=subprocess.CREATE_NO_WINDOW)


def script5():
    subprocess.Popen(["python", "RC_Interaction.py"],
                     creationflags=subprocess.CREATE_NO_WINDOW)


def script6():
    subprocess.Popen(["python", "anchors.py"],
                     creationflags=subprocess.CREATE_NO_WINDOW)


def script7():
    subprocess.Popen(["python", "syncdirs.py"],
                     creationflags=subprocess.CREATE_NO_WINDOW)


def script8():
    subprocess.Popen(["python", "unitconverter.py"],
                     creationflags=subprocess.CREATE_NO_WINDOW)


fs = ('Helvetica', 16)

# Create the main window
root = tk.Tk()
root.title("Remote")
root.geometry("225x525")
# root.iconbitmap(r"C:\Users\wlynes\OneDrive - high.net\Templates\Icons\Will-High.ico")
root.iconbitmap("images\Will-High.ico")

# Create the buttons and pack them into the window
button1 = tk.Button(root, text="ft'-in\" to f.eet'",
                    font=fs, command=script1, height=2, width=20)
button1.pack(fill="both")

button8 = tk.Button(root, text="Unit Converter",
                    command=script8, height=2, width=20, font=fs)
button8.pack(fill="both")

button4 = tk.Button(root, text="AISC Shapes Lookup",
                    command=script4, height=2, width=20, font=fs)
button4.pack(fill="both")

button3 = tk.Button(root, text="Anchor Bolt Reactions",
                    command=script3, height=2, width=20, font=fs)
button3.pack(fill="both")

button6 = tk.Button(root, text="Anchoring to Concrete",
                    command=script6, height=2, width=20, font=fs)
button6.pack(fill="both")

button2 = tk.Button(root, text="Concrete Properties",
                    command=script2, height=2, width=20, font=fs)
button2.pack(fill="both")

button5 = tk.Button(root, text="RC Interaction",
                    command=script5, height=2, width=20, font=fs)
button5.pack(fill="both")

button7 = tk.Button(root, text="Sync Folders",
                    command=script7, height=2, width=20, font=fs)
button7.pack(fill="both")


# Run the main loop
root.mainloop()
