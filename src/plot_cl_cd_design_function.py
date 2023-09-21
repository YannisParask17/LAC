# Script to plot Cl, Cd and AOA

# -------------------------------------#
# Imports
# -------------------------------------#

import numpy as np
import json
import matplotlib.pyplot as plt

from aero_design_functions import get_design_functions


def interp_cl(cl_des, cl_list, aoa_list, cd_list=None):
    '''
    Returns the aoa and cd for the selected cl_design
    by interpolating airfoil data
    '''

    # slicing the aoa data for aoa > 0 and aoa < aoa@cl_max
    aoa_clmax = aoa_list[cl_list == np.max(cl_list)]
    aoa_clmax_idx = aoa_list < aoa_clmax
    aoa_nonnegative = aoa_list > 0
    
    # creating cl and aoa lists in ascending order for interpolation
    # (np.interp need the data to be in ascending order) 
    temp_cl_list = cl_list[ aoa_nonnegative & aoa_clmax_idx]
    temp_aoa_list = aoa_list[aoa_nonnegative & aoa_clmax_idx]
    
    # interpolating data : calculate aoa, cd at cl_des   
    aoa_des = np.interp(cl_des, temp_cl_list, temp_aoa_list)
    if cd_list is not None:
        temp_cd_list = cd_list[aoa_nonnegative & aoa_clmax_idx]
        cd_des = np.interp(cl_des, temp_cl_list, temp_cd_list)

    # print(f'cd_des : {cd_des}')
    # print(f'temp_cd_list : {temp_cd_list}')
    return aoa_des, cd_des


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
            aoa[i] = 0
    
    except:
        breakpoint()
        print("Something fishy is going on")

# Modify the 48 & airfoil

cl_48 = np.array(data[3]['cl'])
aoa_48 = np.array(data[3]['aoa_deg'])
cd_48 = np.array(data[3]['cd'])

mask_1 = (aoa_48 > 0)
mask_2 = (aoa_48 < 14)
mask_aoa = np.logical_and(mask_1, mask_2)

max_cl_48_id = np.argmax(cl_48[mask_aoa])
cl_des_48_adapted = cl_48[mask_aoa][max_cl_48_id] - 0.4

aoa_des_48, cd_des_48 = interp_cl(cl_des_48_adapted, cl_48, aoa_48, cd_48)

# index of 48 is 3
# Update the values

cl[3] = cl_des_48_adapted
cd[3] = cd_des_48
aoa[3] = aoa_des_48

cl_36 = np.array(data[3]['cl'])
aoa_36 = np.array(data[3]['aoa_deg'])
cd_36 = np.array(data[3]['cd'])

mask_1 = (aoa_48 > 0)
mask_2 = (aoa_48 < 14)
mask_aoa = np.logical_and(mask_1, mask_2)

max_cl_48_id = np.argmax(cl_48[mask_aoa])
cl_des_48_adapted = cl_48[mask_aoa][max_cl_48_id] - 0.4

aoa_des_48, cd_des_48 = interp_cl(cl_des_48_adapted, cl_48, aoa_48, cd_48)

# index of 48 is 3
# Update the values

cl[3] = cl_des_48_adapted
cd[3] = cd_des_48
aoa[3] = aoa_des_48


breakpoint()


# Getting the Cl and CD from the design functions




cl1 = cl_des1(tc_list)
cl2 = cl_des2(tc_list)
cl3 = cl_des3(tc_list)

cd1 = cd_des1(tc_list)
cd2 = cd_des2(tc_list)
cd3 = cd_des3(tc_list)

aoa1 = aoa_des1(tc_list)
aoa2 = aoa_des2(tc_list)
aoa3 = aoa_des3(tc_list)




# Plot
fig, axs = plt.subplots(3, 1)
axs[0].scatter(tc_list, cl)
axs[0].plot(tc_list, cl1)
axs[0].plot(tc_list, cl2)
axs[0].plot(tc_list, cl3)
#axs[0].scatter(tc_vals1, cl_vals1)
axs[1].scatter(tc_list, cd)
axs[1].plot(tc_list, cd1)
axs[1].plot(tc_list, cd2)
axs[1].plot(tc_list, cd3)
axs[2].scatter(tc_list, aoa)
axs[2].plot(tc_list, aoa1)
axs[2].plot(tc_list, aoa2)
axs[2].plot(tc_list, aoa3)

axs[0].set_ylabel('cl')
axs[1].set_ylabel('cd')
axs[2].set_ylabel('aoa')
axs[2].set_xlabel('T/C')
plt.show()
breakpoint()
