#
# LAC Week 3
# Code to compute the scaling of the rotor
# M Janssen, September 2023

from lacbox.io import load_st, load_ae, load_c2def, save_c2def, save_ae, load_pc, save_pc
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import r2_score
# -------------------------------------------------------------------- #
# Switches
# -------------------------------------------------------------------- # show_figures = False
show_plots = False
task_4 = False
# -------------------------------------------------------------------- #
# Parameters
# -------------------------------------------------------------------- #

# Reload the data from the original st file
data_path = "../dtu_10mw"
st_path = data_path + "./data/DTU_10MW_RWT_Blade_st.dat"

# define the path where the ae and ind files are
ae_path = data_path + '/data/DTU_10MW_RWT_ae.dat'
ind_path = data_path + '/dtu_10mw_hawc2s_rigid_1point_u8000.ind'
htc_path = data_path + '/dtu_10mw_hawc2s_rigid_1point.htc'
pc_path = data_path + '/DTU_10MW_RWT_pc.dat'

# OUTPUT paths
c2def_save_path = 'c2_def_scaled.txt'
ae_save_path = 'DTU_10MW_RWT_ae_test_scaling.dat'
thickness_out_path = '../results/aero_design/thickness.dat'
polynomial_path = '../results/aero_design/thickness_polynomial.dat'


visualize_thickness = False


# -------------------------------------------------------------------- #
# Functions
# -------------------------------------------------------------------- #


def scale_rotor(rx, ix, iy, vx, verbose=False):
    """
    Compute new radius and scaling factor by solving the equation from the lecture

    """
    # Function inside function from compying. Ugly but works
    def get_vy(rx, ry, vx):
        vy = vx * (rx/ry) **(2/3)
        return vy

    def get_ry(vx, vy, ix, iy, rx):
        ry = rx * ((vx * (1 + 2*ix)) / (vy * (1 + 2*iy))) **(2/3)
        return ry

    res = 1
    err = 0.01
    ry = 1
    while abs(res) > err:
        vy = get_vy(rx, ry, vx)
        r_old = ry
        ry = get_ry(vx, vy, ix, iy, rx)

        res = r_old - ry
        if verbose:
            print(vy)
            print(ry)
            print(res)
   
    if verbose:
        print(f"The new radius is:{ry}")
        print(f"The new v is:{vy}")
    scaling_factor = ry/rx
    return ry, scaling_factor


# -------------------------------------------------------------------- #
# Script
# Question 1 and 2
# -------------------------------------------------------------------- #


# Initial values 

rx = 178.3/2    # Radius of the reference turbine
ix = 0.16       # Class a
iy = 0.14       # Class b
vx = 11.4       # V rated for the 10 mw reference turbine

radius_new, scaling_factor = scale_rotor(rx, ix, iy, vx)

# load aero data -> Thickness
ae = load_ae(ae_path)

# pass data to variables
radius, chord, tc_ratio, pcset = load_ae(ae_path, unpack=True)
thickness = tc_ratio*chord/100

# Get the centerline from the c2def block in the htc file
c2_def = load_c2def(htc_path)  # x, y , z , theta

# Scale up the thickness
thickness_new = thickness * scaling_factor   # Scale up thickness
z_new = c2_def[:, 2] * scaling_factor         # Scale up the z direction
radius_new = radius * scaling_factor

# Thickness data into dataframe and save as csv
df = pd.DataFrame(data={"radius": radius_new, "thickness": thickness_new})
df.to_csv(thickness_out_path, index=False)

# Fit a polynomial to the thickness
#polynomial_coeffs = np.polynomial.polynomial.Polynomial.fit(radius_new, thickness_new, 4)
#poly = np.polynomial.polynomial.Polynomial(polynomial_coeffs)
poly_coeffs = np.polyfit(radius_new, thickness_new, 8)
thickness_poly = np.polyval(poly_coeffs, radius_new)
r2 = r2_score(thickness_new, thickness_poly)

np.savetxt(polynomial_path, poly_coeffs)
breakpoint()



if visualize_thickness:
    plt.scatter(radius_new, thickness_new)
    plt.plot(radius_new, thickness_poly)
    plt.show()
    breakpoint()




c2_def_new = c2_def.copy()
c2_def_new[:, 2] *= scaling_factor  # Scale the z coordinate

save_c2def(c2def_save_path, c2_def_new)

if show_plots:
    fig, ax = plt.subplots(1, figsize=(9, 3.5))

    ax.plot(c2_def[:, 2], c2_def[:, 0], label='Old')
    ax.plot(c2_def_new[:, 2], c2_def_new[:, 0], label='New')

    ax.set(xlabel='Blade span', ylabel='Twist [deg]')
    ax.legend()

    fig.tight_layout()
    plt.show()

# Scale thickness in AE

ae_new = ae.copy()
# ae: [ Curve length, Chord, rel.thickness, pc set number]
# ae_new[:, 0] *= scaling_factor
# ae_new[:, 1] *= scaling_factor
# save_ae(ae_save_path, ae_new)


# -------------------------------------------------------------------- #
# Script
# Question 3
# <For Step 4: Describe other issues influencing the design such as tip speed, maximum chord, number of
# blades etc. (the maximum tip speed should be chosen so that it is obtained below rated wind speed)
# ------------------------------------------------------------------- #

# Tip speed: 85 ?
tip_speed = 80  # m/s should be a compromise between less noise limitations offshore, but taking wild life into account, stay on the lower range
n_blades = 3
chord_max = 6.5  # Taken over from the RWT


# -------------------------------------------------------------------- #
# Script
# Question 4
# Choosing design lift/ angle of attack
# ------------------------------------------------------------------- #

if task_4:
    # Start task 4
   
    # PC file contains the airfoil stuff
    pc_data = load_pc(pc_path)
    print(f"Number of profiles: len(pc_data)={len(pc_data)}")
    print(f"Profile keys: pc_data[i].keys()={pc_data[0].keys()}")
    


