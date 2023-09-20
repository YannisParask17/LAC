# Script to plot Cl, Cd and AOA

# -------------------------------------#
# IMports 
# -------------------------------------#

import numpy as np
import json
import matplotlib.pyplot as plt


json_path = "../results/polar_data.json"
# Opening JSON file
f = open(json_path)

breakpoint()
# returns JSON object as
# a dictionary
data = json.load(f)  # a list of dictionaries, list contains all airfoils 1 to 6
     
breakpoint()
# Closing file
f.close()

tc_list = np.empty([6, 0])  # enter all the thicknesses
cl = np.empty([6, 0])
cd = np.empty([6, 0])
aoa = np.empty([6, 0])

# Get out the Cl, Cd, AOA and thickness for each airfoil -> Design point
breakpoint()
for i in range(0, 6):
    tc_list[i] = data[i]['tc']
    cl[i] = data[i]['cl_des']
    cd[i] = data[i]['cd_des']
    aoa[i] = data[i]['aoa_des']


fig, axs = plt.subplots(3, 1)
axs[0].plot(tc_list, cl)
axs[1].plot(tc_list, cd)
axs[2].plot(tc_list, aoa)

plt.show()
breakpoint()
