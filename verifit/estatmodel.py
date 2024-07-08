""" Estat targets data class

    Create a dataframe of desired values from tech toolbox
    .csv file. 

    Written by: Travis M. Moore
    Created: Nov. 28, 2022
    Last edited: Nov. 29, 2022
"""

###########
# Imports #
###########
# Import GUI packages
import tkinter as tk
from tkinter import filedialog

# Import system packages
from pathlib import Path

# Import data science packages
import pandas as pd


#########
# BEGIN #
#########
class Estatmodel:
    def __init__(self, path=None):
        if not path:
            # Show file dialog to get path
            root = tk.Tk()
            root.withdraw()
            path = filedialog.askdirectory()
            print(path)

        files = Path(path).glob('*.csv')
        self.files = list(files)


    def get_targets(self):
        freqs = [250, 500, 800, 1000, 1500, 2000, 3000, 4000, 6000, 8000]
        freqs = [str(val) for val in freqs]

        df_list = []

        for file in self.files:
            # Read in .csv file as dataframe
            df = pd.read_csv(file, header=None)
            # Trim junk from .csv file
            vals_df = df.iloc[20:,:]
            # Set the first column (freqs) as the index
            vals_df = vals_df.set_index([0])
            vals_df = vals_df.loc[freqs,[1,2,3,4,5,6,7,8]]
            # Convert freq index to column
            vals_df.reset_index(level=0, inplace=True)
            # Append df to list of dfs
            df_list.append(vals_df)

        # Concatenate list of dfs
        self.estat_targets = pd.concat(df_list)
        header = ['freq', 'spl50_L', 'spl50_R', 'spl65_L', 'spl65_R', 'spl80_L', 'spl80_R', 'MPO_L', 'MPO_R']
        self.estat_targets.columns = header
