# Scipt to plot the frequecies and damping of the single blades aeroelastic modes
#
#


# From the HAWCSTAB2 Documentation:
# In case of an aero- or aeroservo-elastic analysis (for both blade only and turbine), an additional
# N columns are added (after the 1 + 2N columns for frequencies and damping) referring to the
# real part of the eigenvalue of each respective mode. As a result, the output file will now contain
# 1 + 3N columns

# -----------------------------------------#
# Imports
# -----------------------------------------#

import numpy as np
import matplotlib.pyplot as plt
from lacbox.io import load_cmb

# -----------------------------------------#
# Data processing
# -----------------------------------------#
plotting = True
# Path to the .cmb file
cmb_type = "aeroelastic"
cmb_path= "dtu_10mw_single_blade_aero_modes.cmb"
mode_names = ['1st flap', '1st edge', '2nd flap', '2nd edge']
turbine_name = "DTU 10MW"

# Load the data
wsp, dfreqs, zetas = load_cmb(cmb_path, cmb_type)  # wind speed, damped natural freqs, and damping values

# print the shape
dfreqs.shape  # n_wsp x n_modes

if plotting:
    fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.7))

    # left plot: damped nat freqs in ground-fixed frame
    axs[0].plot(wsp, dfreqs, marker='.')
    axs[0].set(xlabel='Wind speed [m/s]', ylabel='Damped nat. frequencies [Hz]')
    axs[0].grid()

    # right plot: percent criticl damping
    lines = axs[1].plot(wsp, zetas, marker='.')
    axs[1].set(xlabel='Wind speed [m/s]', ylabel='Modal damping [% critical]')
    axs[1].grid()

    # add legend with 6 columns in center
    fig.legend(loc='outside upper center', handles=lines,
               labels=mode_names, ncols=4)

    # add figure title and scale nicely
    fig.suptitle(f'{cmb_type.capitalize()} Campbell diagram for {turbine_name}',
                 y=0.84)
    fig.tight_layout(rect=[0, 0, 1, 0.87])
    plt.savefig(cmb_path.replace('.cmb', '.pdf'), bbox_inches='tight')
    plt.show()


# -----------------------------------------#
# Plotting
# -----------------------------------------#
