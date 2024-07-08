""" Verifit .xml to .csv Converter """
# Currently only extracts REMs

# Import data science packages
import pandas as pd
import xml.etree.ElementTree as ET

# Import system packages
import glob
import os
from pathlib import Path

# Import GUI packages
import tkinter as tk
from tkinter import filedialog


# Read in file
#path = './Verifit_Files'
root = tk.Tk()
root.withdraw()
path = filedialog.askdirectory()

files = Path(path).glob('*.xml')
files = list(files)

dfs = [] # empty list to hold dfs
for file in files:
    # Get file name and read in data
    file_name = os.path.basename(file)
    df = pd.read_xml(file)

    # Get XML tree structure and root
    tree = ET.parse(file)
    root = tree.getroot()

    # Get tag with 12th-octave frequency list
    freqs = root.find("./test[@name='frequencies']/data[@name='12ths']").text
    freqs = freqs.split()
    freqs = [int(float(freq)) for freq in freqs]

    # Actual SPL REM values
    spls = {}
    # Left
    spls['spl_L1'] = root.find("./test[@side='left']/data[@internal='map_rearspl1']").text
    spls['spl_L2'] = root.find("./test[@side='left']/data[@internal='map_rearspl2']").text
    spls['spl_L3'] = root.find("./test[@side='left']/data[@internal='map_rearspl3']").text
    # Right
    spls['spl_R1'] = root.find("./test[@side='right']/data[@internal='map_rearspl1']").text
    spls['spl_R2'] = root.find("./test[@side='right']/data[@internal='map_rearspl2']").text
    spls['spl_R3'] = root.find("./test[@side='right']/data[@internal='map_rearspl3']").text
    # Split numbers into list
    for key in spls:
        spls[key] = spls[key].split()
        spls[key] = [float(x) for x in spls[key]]


    # TARGET SPL REM values
    targets = {}
    # Left
    targets['target_L1'] = root.find("./test[@side='left']/data[@internal='map_rear_targetspl1']").text
    targets['target_L2'] = root.find("./test[@side='left']/data[@internal='map_rear_targetspl2']").text
    targets['target_L3'] = root.find("./test[@side='left']/data[@internal='map_rear_targetspl3']").text
    # Right
    targets['target_R1'] = root.find("./test[@side='right']/data[@internal='map_rear_targetspl1']").text
    targets['target_R2'] = root.find("./test[@side='right']/data[@internal='map_rear_targetspl2']").text
    targets['target_R3'] = root.find("./test[@side='right']/data[@internal='map_rear_targetspl3']").text
    # Split numbers into list
    for key in targets:
        targets[key] = targets[key].split()[:-2]
        targets[key] = [float(x) for x in targets[key]]


    # Create, shape and index new dataframes
    # Desired frequencies for index
    index_freqs = [250, 500, 750, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
    # SPL dataframe
    spls = pd.DataFrame(spls, index=freqs)
    spls = spls.loc[index_freqs]
    spls = spls.unstack()
    spls = spls.unstack()
    # TARGET dataframe
    targets = pd.DataFrame(targets, index=index_freqs)
    targets = targets.unstack()
    targets = targets.unstack()
    # DIFFERENCE dataframe
    diff_index = ['spl-tar_L1', 'spl-tar_L2', 'spl-tar_L3', 'spl-tar_R1', 'spl-tar_R2', 'spl-tar_R3']
    diffs = spls - targets.values
    diffs.index = diff_index

    # Stack and add filename column
    final = pd.concat([spls, targets, diffs])
    final.reset_index(inplace=True) # Make index a column
    final = final.rename(columns={'index':'Curve'}) # Rename index column
    final.insert(0, 'Filename', file_name) # Add filename column

    # Append dataframe to list of dataframes
    dfs.append(final)

# Concatenate list of dfs into single df
rem = pd.concat(dfs, ignore_index=True)
#print(rem)

# Write dataframe to disk
rem.to_csv('REM_vals2.csv', index=False)




# print(f"\n\n\nTop level: {root.tag}")
# print("\n\n\nShow all children in root")
# for child in root:
#     print(child.tag, child.attrib)

# print("\n\n\nShow elements for the entire tree")
# print([elem.tag for elem in root.iter()])

# print("\n\n\nList all attributes of test in the tree")
# for test in root.iter('test'):
#     print(test.attrib)

# print("\n\n\nList data with name test1_on-ear")
# #for test in root.findall("./test/data/[@name='test1_on-ear']"):
# for test in root.findall("./test/data/[@xscale='12th']"):
#     print(test.attrib)


# print("\n\n\nTest")
# for x in root.findall('test'):
#     for element in x:
#         ele_name = element.tag
#         ele_value = x.find(element.tag).text
#         print(ele_name, " : ", ele_value)


# for x in root.findall('test'):
#     attributes = x.attrib
#     print(attributes)
#     type = attributes.get('type')
#     print(type)


# File|Side|Level|Freqs
# for ii in range(1,3):
#     print(ii)
#     map = 'map_rearspl' + str(ii)
#     print(map)
#     cases = root.findall(f"./test/data[@name='test1_on-ear'][@yunit='dBspl'][@internal='map_rearspl1']")

