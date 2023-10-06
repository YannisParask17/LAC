from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from lacbox.io import ReadHAWC2
from lacbox.test import test_data_path

fname = '../res/dtu_10mw_step.hdf5'
breakpoint()
h2res = ReadHAWC2(fname)

names, units, desc = h2res.chaninfo
print('There are', len(names), 'channels in this output file.')
print(names)

breakpoint()
# find the indices that we think correspond to flapwise blade moment
idx_blades = np.where(['Mx coo: blade' in name for name in names])[0]
print('Identified indices of blade channels are', idx_blades)

# print the corresponding description
[print(desc[i]) for i in idx_blades]

# print the coresponding units
[print(units[i]) for i in idx_blades] # had a semicolon before 

breakpoint()



# assign the relevant data to variables for convenience
Mx1, Mx2, Mx3 = h2res.data[:, idx_blades].T


# calculate statistics
print('Mean values:')
[print(Mx.mean()) for Mx in [Mx1, Mx2, Mx3]]
Mx_mean = h2res.data[:, idx_blades].mean(axis=1)

# plot the time series
fig, ax = plt.subplots(figsize=(12, 5))
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

