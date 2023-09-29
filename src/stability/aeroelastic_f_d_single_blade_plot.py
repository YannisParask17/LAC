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
import pandas as pd


def rpm2hz(rpm):
    return (rpm/60)

s_name = 'aeroelastic_f_d_single_blade_plot.py'
# -----------------------------------------#
# Data processing
# -----------------------------------------#
plotting = True
# Path to the .cmb file
opt_path = '../../IIIB_scaled_turbine/data/IIIB_scaled_turbine_flex.opt'  # path to opt file, to be added as an exercise
result_path = '../../results/stability/'
cmb_type = "aeroelastic"
#cmb_paths = {'structural': '../../IIIB_scaled_turbine/10mw_3b_single_blade_structure.cmb',
#             'aeroelastic': '../../IIIB_scaled_turbine/10mw_3b_single_blade.cmb'
#             }

cmb_path = '../../IIIB_scaled_turbine/10mw_3b_single_blade.cmb'

# Read opt data
#opt_data = np.loadtxt(opt_path, delimiter='\t', skiprows=1)
opt_data = pd.read_csv(opt_path, delim_whitespace=True, skiprows=1, header=None,
                       names=['u', 'pitch_deg', 'rpm', 'power', 'thrust'])


mode_names = ['1st flap', '1st edge', '2nd flap', '2nd edge', '1P', '3P']
turbine_name = "IIIB"

# Load the data
wsp, dfreqs, zetas = load_cmb(cmb_path, cmb_type)  # wind speed, damped natural freqs, and damping values
# breakpoint()

# cmb_data = np.loadtxt(cmb_path, skiprows=1)  # wind speed, damped natural freqs, and damping values
# wsp, dfreqs, zetas = cmb_path[:,0], cmb_path[:,1:5], cmb_path[:,5:]
# print the shape
dfreqs.shape  # n_wsp x n_modes

if plotting:
    fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.7))

    # left plot: damped nat freqs in ground-fixed frame
    axs[0].plot(wsp, dfreqs, marker='.')
    axs[0].plot(opt_data.u, rpm2hz(opt_data.rpm), 'k--')
    axs[0].plot(opt_data.u, 3* rpm2hz(opt_data.rpm), 'k-.')
    axs[0].set(xlabel='Wind speed [m/s]', ylabel='Damped nat. frequencies [Hz]')
    axs[0].grid()

    # right plot: percent criticl damping
    lines = axs[1].plot(wsp, zetas, marker='.')
    axs[1].set(xlabel='Wind speed [m/s]', ylabel='Modal damping [% critical]')
    axs[1].grid()

    # add legend with 6 columns in center
    fig.legend(loc='outside lower center',
               labels=mode_names, bbox_to_anchor=(0.5, -0.2), ncols=3)


    # add figure title and scale nicely
    fig.suptitle(f'{cmb_type.capitalize()} Campbell diagram for {turbine_name}',
                 y=0.84)
    fig.tight_layout(rect=[0, 0, 1, 0.87])
    plt.savefig(result_path + turbine_name + '_' + s_name.replace('.py', '.pdf'), bbox_inches='tight')
    print(f"Figure saved to {result_path + '_' + turbine_name +  s_name.replace('.py', '.pdf')} ")
plt.show()


# -----------------------------------------#
# Plotting
# -----------------------------------------#
