# %%
import matplotlib.pyplot as plt

from lacbox.io import load_cmb
import numpy as np
import pandas as pd
# %%
turbine_name = '10 MW - IIIB'
opt_path = '../../IIIB_scaled_turbine/data/IIIB_scaled_turbine_flex.opt'  # path to opt file, to be added as an exercise
cmb_paths = {'structural': '../../IIIB_scaled_turbine/10mw_3b_whole_turbine_structure.cmb',
             'aeroelastic': '../../IIIB_scaled_turbine/10mw_3b_whole_turbine.cmb'
             }

mode_names = {'structural': ['1st Tower FA', '1st Tower SS', '1st Backward whirling flap', '1st symmetric flapwise',
                             '1st FW flap ', '1st BW whirling edge',
                             '1st FW edge', '2nd BW Flap',
                             '2nd FW flap', '2nd symmetric flap', '1st symmetric edge'],
              'aeroelastic': ['1st Tower FA', '1st Tower SS', '1st BW flap', '1st symmetric flap',
                              '1st FW flap', '1st BW edge',
                              '1st FW edge', '2nd BW flap',
                              '2nd FW flap', '2nd symmetric flap', '1st symmetric edge', '1P', '3P', '6P']}


# Read opt data
#opt_data = np.loadtxt(opt_path, delimiter='\t', skiprows=1)
opt_data = pd.read_csv(opt_path, delim_whitespace=True, skiprows=1, header=None,
                       names=['u', 'pitch_deg', 'rpm', 'power', 'thrust'])


# -----------------------------------#
# Functions
# -----------------------------------#
def rpm2hz(rpm):
    return (rpm/60)


# breakpoint()
# analysis type
for antype in ['structural', 'aeroelastic']:
    cmb_path = cmb_paths[antype]

    # load campbell diagram, skip if missing
    try:
        wsp, dfreqs, zetas = load_cmb(cmb_path, cmb_type=antype)
    except:
        print(f'File {cmb_path} not found! Skipping.')
        continue
    
    fig, axs = plt.subplots(1, 2, figsize=(7.5, 3.7))

    # left plot: damped nat freqs in ground-fixed frame
    axs[0].plot(wsp, dfreqs, marker='.')
    axs[0].plot(opt_data.u, rpm2hz(opt_data.rpm), 'k--', label='1P')
    axs[0].plot(opt_data.u, 3* rpm2hz(opt_data.rpm), 'k-.', label='3P')
    axs[0].plot(opt_data.u, 6* rpm2hz(opt_data.rpm), 'k.-.', label='6P')
    axs[0].set(xlabel='Wind speed [m/s]', ylabel='Damped nat. frequencies [Hz]')
    axs[0].grid()

    # right plot: percent criticl damping
    lines = axs[1].plot(wsp, zetas, marker='.')
    axs[1].set(xlabel='Wind speed [m/s]', ylabel='Modal damping [% critical]')
    axs[1].grid()

    # add legend with 6 columns in center
    #fig.legend(loc='outside lower center', handles=lines,
    # fig.legend(loc='outside lower center', bbox_to_anchor=(0.5, -0.2), handles=lines,
            #    labels=mode_names[antype], ncols=4)
    fig.legend(loc='outside lower center', bbox_to_anchor=(0.5, -0.25), labels=mode_names[antype], ncols=5)

    # add figure title and scale nicely
    fig.suptitle(f'{antype.capitalize()} Campbell diagram for {turbine_name}',
                 y=0.84)
    fig.tight_layout(rect=[0, 0, 1, 0.87])


    plt.savefig(cmb_path.replace("cmb", "pdf"), bbox_inches='tight')
plt.show()

