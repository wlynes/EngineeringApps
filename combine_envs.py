import json
import os

# list of JSON files to combine
filepath = r"C:\Users\wlyne\Python\Lib\site-packages\forallpeople\environments"
files = ["default.json", "electrical.json",
         "structural.json", "thermal.json", "us_customary.json"]
newfile = os.path.join(filepath, "unitconverter.json")

pathandfiles = []
for f in files:
    pathandfiles.append(os.path.join(filepath, f))

# dictionary to store the data from all files
data = {}

# loop through the list of files
for file in pathandfiles:
    # open the file and read the data
    with open(file, 'r') as fff:
        file_data = json.load(fff)
    # add the data from the file to the dictionary
    data.update(file_data)

# remove duplicates from the dictionary
data = dict(sorted(data.items(), key=lambda item: item[0]))

# write the combined data to a new file
with open(newfile, 'w') as f:
    json.dump(data, f)
