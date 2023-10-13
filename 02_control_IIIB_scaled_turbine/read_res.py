import matplotlib.pyplot as plt
import numpy as np
from lacbox.io import ReadHAWC2

fname =  './res/dtu_10mw_step.hdf5'

h2res = ReadHAWC2(fname)

print(h2res.__dict__.keys())
names, units, desc = h2res.chaninfo

# plot the time series
fig, axes = plt.subplots(4, figsize=(10, 7), sharex=True)
for ax in axes.flat:
    ax.grid(True)

axes[0].plot(h2res.t, h2res.data[:, 14])
axes[0].set(ylabel='Wind Speed, Vz [m/s]')

axes[1].plot(h2res.t, h2res.data[:, 3])
axes[1].set(ylabel='Pitch Angle [deg]')

axes[2].plot(h2res.t, h2res.data[:, 9])
axes[2].set(ylabel='Rotor Speed [s]')

axes[3].plot(h2res.t, h2res.data[:, 11])
axes[3].set(ylabel='Power [kW]',
          xlabel='Time [s]')
plt.tight_layout()