import tkinter as tk
from tkinter import ttk
import re
from fractions import Fraction
import math
from tkinter import messagebox


def feet_and_inches_string_formats():
  # Some valid input strings
  _strFormats = [r"(\d+)\'-(\d+)\s(\d+)/(\d+)\"", # a'-b c/d" (default)
                r"(\d+)\'\s(\d+)\s(\d+)/(\d+)\"", # a' b c/d" (without the dash)
                r"(\d+)-(\d+)\s(\d+)/(\d+)", # a-b c/d (default without ' " marks)
                r"(\d+)\s(\d+)\s(\d+)\s(\d+)", # a b c/d (without - ' " marks)
                r"(\d+)\'-(\d+)\"", # a'-b" (whole inches only)]
                r"(\d+)-(\d+)", # a-b (whole inches without ' " marks)
                r"(\d+)\s(\d+)"] # a-b (whole inches without ' " marks)
  return _strFormats
  
def feet_and_inches_to_decimal_feet(s):
    validFormats = feet_and_inches_string_formats()
    
    for i, chk in enumerate(validFormats):
      if m := re.match(chk, s):
        feet = int(m.group(1))
        inches = int(m.group(2))
        if chk in validFormats[-3:]:
            numerator = 0
            denominator = 1
        else:
            numerator = int(m.group(3))
            denominator = int(m.group(4))
            # Convert the fraction to a decimal value and add it to the inches
    
    inches += numerator / denominator

    # Add the feet and inches to get the total distance in decimal feet
    return feet + inches / 12   
      




def convert_dectostring():
  # Get the input value and convert it to a float
  input = float(input_entry.get())

  # Convert input to feet and inches
  feet = int(input)
  inches = (input - feet) * 12

  # get the selected precision
  precision = selected_precision.get()
  multiple = 1 / precision

  # CONVERT TO INCHES AND FRACTION WITH SELECTED PRECISION
  # Get the whole inches
  wholeinches = int(inches)
  
  # Get the remainder (0.XXXX")
  decInches = inches - wholeinches

  # Still got the mooooooves
  numerator = round(decInches*precision,0)
  denominator = precision
  frac = Fraction(numerator/denominator)
  if frac == 1:
    wholeinches += 1
    numerator=0

  # Build the output string
  if numerator == 0:
    output = "{}'-{}\"".format(feet, wholeinches)
  else:
    output = "{}'-{} {}\"".format(feet, wholeinches,frac)

  # Set the output string in the text box
  output_text.set(output)

# Create the Tkinter window
window = tk.Tk()
window.title("Freedom Units Converter")
window.iconbitmap("images\Will-High.ico")

# list of precision options
precision_options = [0,2,4,8,16,32]
selected_precision = tk.IntVar()
selected_precision.set(precision_options[-1])

# Create a ttk.Notebook widget as the parent for the tabs
notebook = ttk.Notebook(window)
notebook.pack()

# Create a tab for the feet and inches to decimal feet conversion
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text="Feet and Inches to Decimal Feet")

# Add a label and an entry widget to input the feet and inches string
label1 = tk.Label(tab1, text="Enter a distance in feet and inches:", font=("Helvetica", 16))
label1.pack()

entry1 = tk.Entry(tab1, font=("Helvetica", 16), width=20)
entry1.pack()

# Add a button to perform the conversion
def convert1():
    # Get the value from the entry widget and convert it to decimal feet
    value = entry1.get()
    result = feet_and_inches_to_decimal_feet(value)
    resultstring = "{:.4f}".format(result)
    # Display the result in a label
    result1.set(resultstring)

button1 = tk.Button(tab1, text="Convert", command=convert1, font=("Helvetica", 16))
button1.pack()

# Add a label to display the result
result1 = tk.StringVar()
result_label1 = tk.Entry(tab1, state="readonly",textvariable=result1, font=("Helvetica", 16))
result_label1.pack(pady=2)




# Create a 2nd tab
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text="Decimal Feet to Feet and Inches")

# Create the input label and entry box
input_label = tk.Label(tab2, text="Enter a decimal value in feet:", font=("Helvetica", 16))
input_label.pack()

input_entry = tk.Entry(tab2, font=("Helvetica", 16), width=20)
input_entry.pack()

# create the radio buttons
# for i, precision in enumerate(precision_options):
#     tk.Radiobutton(window, text=str(precision), variable=selected_precision, value=precision).pack(anchor=tk.W)
tk.OptionMenu(tab2, selected_precision, *precision_options).pack()


# Create the output label and text box
output_label = tk.Label(tab2, text="Result:", font=("Helvetica", 16))
output_label.pack()

output_text = tk.StringVar()
output_box = tk.Entry(tab2, textvariable=output_text, state="readonly", font=("Helvetica", 16), width=20)
output_box.pack()



# Create the convert button
convert_button = tk.Button(tab2, text="Convert", font=("Helvetica", 16), command=convert_dectostring)
convert_button.pack()


# Run the main loop
window.mainloop()