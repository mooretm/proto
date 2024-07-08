""" Verifit data class

    This object extracts and organzies Verifit session 
    files from the original .xml.

    Returns:
        1. REM SPL and TARGET values
        2. Aided SII (NOTE: unaided SII not available from session file!)
        3. .csv files of selected data

    Written by: Travis M. Moore
    Created: Nov. 17, 2022
    Last edited: Nov. 28, 2022
"""

###########
# Imports #
###########
# Import data science packages
import pandas as pd
import xml.etree.ElementTree as ET

# Import system packages
import os
from pathlib import Path

# Import GUI packages
import tkinter as tk
from tkinter import filedialog


class VerifitData:
    def __init__(self, path=None):
        if not path:
            # Show file dialog to get path
            root = tk.Tk()
            root.withdraw()
            path = filedialog.askdirectory()
            print(path)

        files = Path(path).glob('*.xml')
        self.files = list(files)

        # Desired frequencies for index
        self.audiogram_freqs = [250, 500, 750, 1000, 1500, 2000, 
            3000, 4000, 6000, 8000]


    def get_root(self, file):
        # Get XML tree structure and root
        tree = ET.parse(file)
        self.root = tree.getroot()

        # Get tag with 6th-octave frequency list
        freqs = self.root.find("./test[@name='frequencies']/data[@name='12ths']").text
        freqs = freqs.split()
        self.sixth_oct_freqs = [int(float(freq)) for freq in freqs]
        
        # Create file name
        filename = os.path.basename(file)
        self.filename = filename[:-4]
        self.subjectname = filename.split('_')[0]


    def get_all_data(self):
        self.get_aided_sii()
        self.get_measured_spls()
        self.get_target_spls()
        self.all_data = pd.concat([self.measured_spls, self.target_spls, self.aided_sii])


    def write_to_csv(self):
        print('')
        print('-' * 50)
        print("verifitmodel: Creating .csv file...\n")
        self.get_all_data()
        self.all_data.sort_values(by='filename')
        self.all_data.to_csv('Verifit_data.csv', index=False)
        print("verifitmodel: .csv file created successfully!")
        print('-' * 50)
        print('')


    ####################
    # AIDED SII VALUES #
    ####################
    # NOTE: Verifit session file does not include unaided SII!
    def get_aided_sii(self):
        print("verifitmodel: Fetching aided SII data...")
        sii_list = []
        sii_dict = {}

        for file in self.files:
            self.get_root(file)

            try:
            # Left
                sii_dict['sii_L1'] = self.root.find("./test[@side='left']/data[@internal='map_rear_sii1']").text
                sii_dict['sii_L2'] = self.root.find("./test[@side='left']/data[@internal='map_rear_sii2']").text
                sii_dict['sii_L3'] = self.root.find("./test[@side='left']/data[@internal='map_rear_sii3']").text
                #sii_dict['sii_L4'] = self.root.find("./test[@side='left']/data[@internal='map_rear_sii4']").text
                # Right
                sii_dict['sii_R1'] = self.root.find("./test[@side='right']/data[@internal='map_rear_sii1']").text
                sii_dict['sii_R2'] = self.root.find("./test[@side='right']/data[@internal='map_rear_sii2']").text
                sii_dict['sii_R3'] = self.root.find("./test[@side='right']/data[@internal='map_rear_sii3']").text
                #sii_dict['sii_R4'] = self.root.find("./test[@side='right']/data[@internal='map_rear_sii4']").text
            except AttributeError:
                print(f"\n{self.filename} is missing data! Aborting!\n")
                exit()

            sii_list.append(pd.DataFrame(sii_dict, index=[str(self.filename)]))

        aided_sii = pd.concat(sii_list)
        aided_sii.reset_index(inplace=True)
        aided_sii = aided_sii.rename(columns={'index':'filename'})
        self.aided_sii = pd.melt(aided_sii, id_vars='filename', value_vars=list(aided_sii.columns[1:]))
        print("verifitmodel: Completed!\n")


    #######################
    # MEASURED SPL VALUES #
    #######################
    def get_measured_spls(self):
        print("verifitmodel: Fetching measured SPL data...")
        spls_list = []

        for file in self.files:
            self.get_root(file)
            
            spls_dict = {}

            # Measured SPL REM values
            try:
                # Left MEASURED spls
                spls_dict['spl_L1'] = self.root.find("./test[@side='left']/data[@internal='map_rearspl1']").text
                spls_dict['spl_L2'] = self.root.find("./test[@side='left']/data[@internal='map_rearspl2']").text
                spls_dict['spl_L3'] = self.root.find("./test[@side='left']/data[@internal='map_rearspl3']").text
                # Right MEASURED spls
                spls_dict['spl_R1'] = self.root.find("./test[@side='right']/data[@internal='map_rearspl1']").text
                spls_dict['spl_R2'] = self.root.find("./test[@side='right']/data[@internal='map_rearspl2']").text
                spls_dict['spl_R3'] = self.root.find("./test[@side='right']/data[@internal='map_rearspl3']").text
            except AttributeError:
                print(f"\n{self.filename} is missing MEASURED REM data! Aborting!\n")
                exit()

            # Split numbers into list
            for key in spls_dict:
                spls_dict[key] = spls_dict[key].split()
                spls_dict[key] = [float(x) for x in spls_dict[key]]

            #spls_dict['freqs'] = freqs
            df = pd.DataFrame(spls_dict, index=self.sixth_oct_freqs)
            df = df.loc[self.audiogram_freqs]
            df.reset_index(inplace=True)
            df = df.rename(columns={'index':'freq'})
            df = pd.melt(df, id_vars='freq', value_vars=list(df.columns[1:]))
            # Add file name to df
            df.insert(loc=0, column='filename', value = self.filename)

            spls_list.append(df)
        
        self.measured_spls = pd.concat(spls_list)
        print("verifitmodel: Completed!\n")


    #####################
    # TARGET SPL VALUES #
    #####################
    def get_target_spls(self):
        print("verifitmodel: Fetching target SPL data...")
        target_list = []

        for file in self.files:
            self.get_root(file)
            
            target_dict = {}

            # TARGET spl values
            try:
                # Left TARGET spls
                target_dict['target_L1'] = self.root.find("./test[@side='left']/data[@internal='map_rear_targetspl1']").text
                target_dict['target_L2'] = self.root.find("./test[@side='left']/data[@internal='map_rear_targetspl2']").text
                target_dict['target_L3'] = self.root.find("./test[@side='left']/data[@internal='map_rear_targetspl3']").text
                # Right TARGET spls
                target_dict['target_R1'] = self.root.find("./test[@side='right']/data[@internal='map_rear_targetspl1']").text
                target_dict['target_R2'] = self.root.find("./test[@side='right']/data[@internal='map_rear_targetspl2']").text
                target_dict['target_R3'] = self.root.find("./test[@side='right']/data[@internal='map_rear_targetspl3']").text
            except AttributeError:
                print(f"\n{self.filename} is missing TARGET REM data! Aborting!\n")
                exit()

            # Split numbers into list
            for key in target_dict:
                target_dict[key] = target_dict[key].split()

                target_dict[key] = [x for x in target_dict[key] if x != '_']

                target_dict[key] = [float(x) for x in target_dict[key]]

            df = pd.DataFrame(target_dict, index=self.audiogram_freqs)
            df.reset_index(inplace=True)
            df = df.rename(columns={'index':'freq'})
            df = pd.melt(df, id_vars='freq', value_vars=list(df.columns[1:]))
            # Add file name to df
            df.insert(loc=0, column='filename', value = self.filename)

            target_list.append(df)
        
        self.target_spls = pd.concat(target_list)
        print("verifitmodel: Completed!\n")
