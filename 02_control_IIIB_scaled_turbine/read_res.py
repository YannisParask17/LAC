import matplotlib.pyplot as plt
from lacbox.io import ReadHAWC2
import numpy as np
from scipy.signal import find_peaks

fn1 = './res/iiib_c1.hdf5'
fn2 = './res/iiib_c2.hdf5'
fn3 = './res/iiib_c3.hdf5'
fn4 = './res/iiib_c4.hdf5'
fn5 = './res/iiib_c5.hdf5'
fn6 = './res/iiib_c6.hdf5'
fn7 = './res/iiib_c7.hdf5'
fn7_0058 = './res/iiib_c7_0058.hdf5'
fn7_0048 = './res/iiib_c7_omega0048_zeta07.hdf5'
fn7_0052 = './res/iiib_c7_omega0052_zeta07.hdf5'
fn7_0054 = './res/iiib_c7_omega0054_zeta07.hdf5'
fn7_00625 = './res/iiib_c7_omega00625_zeta07.hdf5'
# fn7_00_075 = './res/iiib_c7_omega005_zeta075.hdf5'

# Split into two, as there should be two plots
f_names1=[fn1, fn2, fn3]
f_names2=[fn4, fn5, fn6]
f_names3=[fn1, fn7_0048, fn7_0052, fn7_0054, fn7_0058, fn7_00625]

labels_1 = ['C1', 'C2', 'C3']
labels_2 = ['C4', 'C5', 'C6']
labels_3 = ['C1', r'$\omega_{\Omega}=$0.048Hz', 
            '$\omega_{\Omega}=$0.052Hz', '$\omega_{\Omega}=$0.054Hz', 
            '$\omega_{\Omega}=$0.058Hz', '$\omega_{\Omega}=$0.0625Hz']

# First plot : C1 to C3

fig1, ax1 = plt.subplots(4, figsize=(8, 5), sharex=True)
ax1[0].set(ylabel='Wind Speed, Vz\n[m/s]')
ax1[1].set(ylabel='Pitch Angle\n[deg]')
ax1[2].set(ylabel='Rotor Speed\n[rad/s]')
ax1[3].set(ylabel='Power\n[W]',
            xlabel='Time\n[s]')


for i, fn in enumerate(f_names1):
    h2res = ReadHAWC2(fn)

    print(h2res.__dict__.keys())
    names, units, desc = h2res.chaninfo

    # plot the time series
    ax1[0].plot(h2res.t, h2res.data[:, 14], label=labels_1[i])
    ax1[1].plot(h2res.t, h2res.data[:, 3], label=labels_1[i])
    ax1[2].plot(h2res.t, h2res.data[:, 9], label=labels_1[i])
    ax1[3].plot(h2res.t, h2res.data[:, 110], label=labels_1[i])

for ax in ax1.flat:
    ax.grid(True)
ax1[0].legend(loc='upper center', ncols=3)
plt.tight_layout()
plt.savefig('../results/control_response_c1_c3.pdf')

fig2, ax2 = plt.subplots(4, figsize=(8, 5), sharex=True)
ax2[0].set(ylabel='Wind Speed, Vz\n[m/s]')
ax2[1].set(ylabel='Pitch Angle\n[deg]')
ax2[2].set(ylabel='Rotor Speed\n[rad/s]')
ax2[3].set(ylabel='Power\n[W]',
           xlabel='Time\n[s]')

for i, fn in enumerate(f_names2):
    h2res = ReadHAWC2(fn)

    print(h2res.__dict__.keys())
    names, units, desc = h2res.chaninfo

    # plot the time series
    ax2[0].plot(h2res.t, h2res.data[:, 14], label=labels_2[i])
    ax2[1].plot(h2res.t, h2res.data[:, 3], label=labels_2[i])
    ax2[2].plot(h2res.t, h2res.data[:, 9], label=labels_2[i])
    ax2[3].plot(h2res.t, h2res.data[:, 110], label=labels_2[i])

ax2[0].legend(loc='upper center', ncols=3)
for ax in ax2.flat:
    ax.grid(True)
plt.tight_layout()
plt.savefig('../results/control_response_c4_c6.pdf')

fig3, ax3 = plt.subplots(4, figsize=(8, 5), sharex=True)
ax3[0].set(ylabel='Wind Speed, Vz\n[m/s]')
ax3[1].set(ylabel='Pitch Angle\n[deg]')
ax3[2].set(ylabel='Rotor Speed\n[rad/s]')
ax3[3].set(ylabel='Power\n[W]',
           xlabel='Time\n[s]')


for i, fn in enumerate(f_names3):
    h2res = ReadHAWC2(fn)

    print(h2res.__dict__.keys())
    names, units, desc = h2res.chaninfo
    # breakpoint()
    # plot the time series
    ax3[0].plot(h2res.t, h2res.data[:, 14], label=labels_3[i])
    ax3[1].plot(h2res.t, h2res.data[:, 3], label=labels_3[i])
    ax3[2].plot(h2res.t, h2res.data[:, 9], label=labels_3[i])
    ax3[3].plot(h2res.t, h2res.data[:, 110], label=labels_3[i])

ax3[0].legend(loc='upper center', ncols=3)
for ax in ax3.flat:
    ax.grid(True)

plt.tight_layout()
plt.savefig('../results/control_response_c1_c7.pdf')
# plt.show()




# Zoom in at the above rated region (Step 12-13 m/s)

pitch_opt_13 = 7.78 # taken from the opt file for 13 m/s

fig3, ax3 = plt.subplots(4, figsize=(8, 5), sharex=True)
ax3[0].set(ylabel='Wind Speed, Vz\n[m/s]')
ax3[1].set(ylabel='Pitch Angle\n[deg]')
ax3[2].set(ylabel='Rotor Speed\n[rad/s]')
ax3[3].set(ylabel='Power\n[W]',
            xlabel='Time\n[s]')

t_settling = np.zeros(len(f_names3)) # initialise settling time
overshoot = np.zeros(len(f_names3)) # initialise overshoot

for i, fn in enumerate(f_names3):

    if i == 0:
        mark = '--'
    else:
        mark = '-'

    h2res = ReadHAWC2(fn)
    print(h2res.__dict__.keys())
    names, units, desc = h2res.chaninfo

    # Isolate only the 12-13 m/s step
    mask1 = (h2res.t > 465)
    mask2 = (h2res.t < 510)
    filt =  np.logical_and(mask1, mask2)

    pitch_filt = h2res.data[:, 3][filt]
    time_filt = h2res.t[filt]

    # Find settling time
    # if i == len(f_names3)-1:
        # breakpoint()
    start_time_idx = np.where(h2res.data[:, 14][filt] == 13.)[0][0]
    start_time = time_filt[start_time_idx]

    
    pitch_peaks_idx = find_peaks(abs(pitch_filt), height=5)[0]
    pitch_peaks = pitch_filt[pitch_peaks_idx]

    mask = (abs(abs(pitch_peaks)-pitch_opt_13)/pitch_opt_13 <=0.05)
    # find the first true element of the mask
    temp_idx = np.where(mask==True)[0][0]
    # breakpoint()
    # find the value of the pitch at that point
    pitch_ss = pitch_filt[pitch_filt==pitch_peaks[temp_idx]][0]
    

    # find the value of time when pitch_filt equals to that point   

    # settling_time_abs = time_filt[abs((pitch_opt_13-pitch_filt)/pitch_opt_13)<=0.05][0]
    settling_time_abs = time_filt[pitch_filt == pitch_ss][0]
    t_settling[i] = settling_time_abs - start_time # settling time array (store data)

    # Find percentagewise overshoot 
    pitch_max_idx = np.argmax(pitch_filt)
    pitch_max = pitch_filt[pitch_max_idx] # find the maximum pitch
    overshoot[i] = abs(pitch_opt_13-np.max(pitch_peaks))/pitch_opt_13 * 100  # in percentage


    # plot the time series
    
    ax3[0].plot(h2res.t[filt], h2res.data[:, 14][filt], mark, label=labels_3[i], linewidth=.8)
    
    ax3[1].plot(h2res.t[filt], h2res.data[:, 3][filt], mark, label=labels_3[i], linewidth=.8)

    ax3[2].plot(h2res.t[filt], h2res.data[:, 9][filt], mark, label=labels_3[i], linewidth=.8)
    
    ax3[3].plot(h2res.t[filt], h2res.data[:, 110][filt], mark, label=labels_3[i], linewidth=.8)
    

    
fig3.legend(labels_3, loc='outside upper center', ncols=3)    
fig3.show()

breakpoint()
for ax in ax3.flat:
    ax.grid(True)

# plt.tight_layout()
plt.savefig('../results/control_response_c1_c7_aboverated.pdf')
plt.show()
