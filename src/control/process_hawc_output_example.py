# Plot to postprocess data from the HAWC2 output file (HDF5)
# October '23

# -- Imports -- #
import matplotlib.pyplot as plt
import numpy as np
from lacbox.io import ReadHAWC2

# ------------------------- Read and process data----------------------- #
fname = '../res/dtu_10mw_step.hdf5'
h2res = ReadHAWC2(fname)

names, units, desc = h2res.chaninfo
print('There are', len(names), 'channels in this output file.')
print(names)

# Find indices of relevant channels
idx_wind = np.where(['WSP gl. coo.,' in name for name in names])[0]
idx_pitch = np.where([('pitch' in name) and ('angle' in name) and not ('DLL' in name) and not ('speed' in name) for name in desc])[0]
idx_rot_speed = np.where(['shaft_rot angle speed' in name for name in desc])[0]
idx_power = np.where(['Ae rot. power' in name for name in names])[0]


# wind speed, pitch angle, rotation speed, and electrical power1 vs.
# time must be presented


# assign the relevant data to variables for convenience
wsp_u, wsp_v, wsp_w, wsp_abs, wsp_direction = h2res.data[:, idx_wind].T
pitch1, pitch2, pitch3 = h2res.data[:, idx_pitch].T
rot_speed = h2res.data[:, idx_rot_speed].T[0, :]
aero_power = h2res.data[:, idx_power].T[0, :]


# ------------------------- Plotting ----------------------- #
breakpoint()
fig, axs = plt.subplots(4, 1, figsize=(8, 5))

handles_0 = axs[0].plot(h2res.t, wsp_abs, 'k--')
handles_1 = axs[1].plot(h2res.t, pitch1, 'k--')
handles_2 = axs[2].plot(h2res.t, rot_speed, 'k--')
handles_3 = axs[3].plot(h2res.t, aero_power, 'k--')

[ax.grid() for ax in axs]
axs[0].set_xticklabels([])
axs[1].set_xticklabels([])
axs[2].set_xticklabels([])

axs[3].set_xlabel('t in s')

axs[0].set_ylabel('Wind speed\nin m/s')
axs[1].set_ylabel(r'Pitch angle\n in $^\circ$')
axs[2].set_ylabel('Rotor speed\n in ()')
axs[3].set_ylabel('Mechanical power\n')


axs[0].legend(['Wind speed'])
axs[1].legend(['Pitch angle'])
axs[2].legend(['Rotor speed'])
axs[3].legend(['Mechanical Power'])
plt.show()


if False: # Old stuff from the example
    handles = ax.plot(h2res.t, h2res.data[:, idx_blades])
    l, = ax.plot(h2res.t, Mx_mean, 'k--')
    labels = [f'Blade {i+1}' for i in range(3)] + ['Sum of blades']
    ax.set(xlim=[100, 200],
        xlabel='Time [s]',
        ylabel='Blade root moment [kNm]')
    ax.legend(handles + [l], labels);
    plt.show()
    breakpoint()


print("Done")
