# Script to plot Cl, Cd and AOA

# -------------------------------------#
# Imports
# -------------------------------------#

import numpy as np
import json
import matplotlib.pyplot as plt

from aero_design_functions import get_design_functions

cl_des1, cd_des1, aoa_des1, tc_vals1, cl_vals1, cd_vals1, aoa_vals1 = get_design_functions(1)
cl_des2, cd_des2, aoa_des2, tc_vals2, cl_vals2, cd_vals2, aoa_vals2 = get_design_functions(2)
cl_des3, cd_des3, aoa_des3, tc_vals3, cl_vals3, cd_vals3, aoa_vals3 = get_design_functions(3)

json_path = "../results/polar_data.json"

# Pull data from file
f = open(json_path)
data = json.load(f)  # a list of dictionaries, list contains all airfoils 1 to 6
f.close()

# initialize arrays
tc_list = np.zeros([6, 1])  # enter all the thicknesses
cl = np.zeros([6, 1])
cd = np.zeros([6, 1])
aoa = np.zeros([6, 1])

# Get out the Cl, Cd, AOA and thickness for each airfoil -> Design point
for i in range(0, 6):
    try:
        if i < 5:
            tc_list[i] = data[i]['tc']
            cl[i] = data[i]['cl_des']
            cd[i] = data[i]['cd_des']
            aoa[i] = data[i]['aoa_des']
        
        if i == 5:  # Which is the cylinder .... Dont mess up the order !
            tc_list[i] = data[i]['tc']
            cl[i] = data[i]['cl'][0]  # Manually set them
            cd[i] = data[i]['cd'][0]
            aoa[i] = data[i]['aoa_des']
    
    except:
        breakpoint()
        print("Something fishy is going on")
# Plot
fig, axs = plt.subplots(3, 1)
axs[0].scatter(tc_list, cl)
axs[1].scatter(tc_list, cd)
axs[2].scatter(tc_list, aoa)

axs[0].set_ylabel('cl')
axs[1].set_ylabel('cd')
axs[2].set_ylabel('aoa')
axs[2].set_xlabel('T/C')
plt.show()
breakpoint()
