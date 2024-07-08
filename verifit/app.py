""" Control script for pulling Verifit REM and SII data

    Written by: Travis M. Moore
    Created: Nov. 17, 2022
    Last edited: Nov. 29, 2022
"""

###########
# Imports #
###########
# Import custom modules
import verifitmodel
import estatmodel


#########
# BEGIN #
#########
###################
# Verifit Targets #
###################
# # Define path to Verifit files for batch processing
# _verifit_path = '//starfile/Public/Temp/CAR Group/G23 Validation/Verifit'
# # Create verifit class instance
# v = verifitmodel.VerifitData(_verifit_path)
# # Get dataframe of all data
# v.get_all_data()
# #print(v.all_data)


#################
# ESTAT Targets #
#################
# Define path to estat files for batch processing
_estat_path = r'\\starfile\Public\Temp\CAR Group\G23 Validation\Estat'
#r'C:\Users\MooTra\Downloads\P0128_CorrectCouplingPreVR.csv'
# Create estat class instance
e = estatmodel.Estatmodel(_estat_path)
# Get dataframe of all data
e.get_targets()
print(e.estat_targets)
