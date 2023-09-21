# Script to read in the data including chord and t/c ratio and put it into an ae file
#
import pandas as pd
from lacbox.io import load_ae, save_ae
import json

# Path to read in the AE file and where to save it
json_path= '../results/design_parameters_at_max_cp.json'
in_path = '../dtu_10mw/data/DTU_10MW_ae.dat'
out_path = '../results/hawc_files/10MW_1a_ae.dat'

breakpoint()
#f = open(json_path)
#json_data = json.load(f)  # a list of dictionaries, list contains all airfoils 1 to 6
#data = pd.read_json(json_data)     # Get our data
#f.close()

json_data = pd.read_json(json_path)

ae_data = load_ae(in_path)      # Get the RWT data


ae_new = ae_data.copy()
ae_new[:, 0] = data['radius']   # radial position
ae_new[:, 1] = data['chord']    # Chord
ae_new[:, 2] = data['tc']       # T/C ratio

# Finally save the data
save_ae(out_path, ae_new)
print("Done!")

