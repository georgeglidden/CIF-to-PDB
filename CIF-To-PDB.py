# CIF to PDB 
#
# The script will convert in a batch mode CIF files in a folder to PDB in outputs_pdbs,
# 
## Requirements
# - Python 3.x
#
## Python packages:
# - Open Babel
#
# conda install openbabel
#
## USAGE 
#
# python script_name.py path_to_CIFS_files_FOLDER/
#
# 2023 Jean-Marie Bourhis 

import os
import pdb
import subprocess
import sys
import pathlib
from tqdm import tqdm

# Define the input and output directories
input_cif_directory = None
output_pdb_directory = None
default_output_dir = "output_pdbs"

try:
    n_args = len(sys.argv)
    if n_args > 1:
        input_cif_directory = pathlib.Path(sys.argv[1])
        # if an input dir is given, use it.
    else:
        input_cif_directory = pathlib.Path('.')
        # otherwise, the cwd will be used.
    if n_args > 2:
        output_pdb_directory = pathlib.Path(sys.argv[2])
        # if an output dir is given, use it.
    else:
        output_pdb_directory = input_cif_directory / default_output_dir
        # otherwise, append the default output dir to the input dir.
    input_cif_directory = str(input_cif_directory)
    output_pdb_directory = str(output_pdb_directory)
except Exception as e:
    print(f"could not parse args!")
    raise e
finally:
    print(f"input_cif_directory={input_cif_directory}\noutput_pdb_directory={output_pdb_directory}")

# Create output and temporary directories if they don't exist
os.makedirs(output_pdb_directory, exist_ok=True)

# Get a list of CIF files in the input directory and sort them
cif_files = [f for f in os.listdir(input_cif_directory) if f.endswith(".cif")]
cif_files.sort()  # Sort alphabetically

# Wrap the loop with tqdm to add a progress bar
for cif_file in tqdm(cif_files, desc="Converting files"):
    cif_path = os.path.join(input_cif_directory, cif_file)
    pdb_file = cif_file.replace(".cif", ".pdb")
    pdb_path = os.path.join(output_pdb_directory, pdb_file)

    # Convert CIF to PDB using Open Babel
    obabel_command = ["obabel", cif_path, "-O", pdb_path]
    with open(os.devnull, 'w') as devnull:
        subprocess.run(obabel_command, stdout=devnull, stderr=devnull)

      # Remove headers using awk
    awk_command = ["awk", '/^ATOM |^TER/']
    with open(os.path.join(output_pdb_directory, pdb_file), "rb") as input_file:
        awk_process = subprocess.run(awk_command, stdin=input_file, stdout=subprocess.PIPE, text=True)
        tmp2_content = awk_process.stdout

    with open(os.path.join(output_pdb_directory, pdb_file), "w") as tmp2_file:
        tmp2_file.write(tmp2_content)

print("Conversion complete.")
