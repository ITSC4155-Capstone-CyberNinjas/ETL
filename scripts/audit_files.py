# audit_files.py

"""
A small script to check discrepancies in raw and transformed file. 
Used to see what files failed to transfer
"""

import os 
from pathlib import Path 

RAW_PATH = Path('/media/calvinhathcock/Secondary SSD/ITSC_4155_Capstone/dataset/raw/wifi/var/log/remote/wireless-encoded')
TRANFORMED_PATH = Path("/home/calvinhathcock/Documents/College/UNCC/Fall 2022/ITSC 4155/Project/transformed_data")

raw_files = set( [x[:-4] for x in os.listdir(RAW_PATH)] )
transformed_files =  set( [x[7:-4] for x in os.listdir(TRANFORMED_PATH)] )

print(f'length of raw: {len(raw_files)} \nlength of transformed: {len(transformed_files)}')
print(f'difference: {len(raw_files) - len(transformed_files)}')

print(raw_files.difference(transformed_files))
print(len(raw_files.difference(transformed_files)))