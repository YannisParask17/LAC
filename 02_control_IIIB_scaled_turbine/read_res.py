import matplotlib.pyplot as plt
from lacbox.io import ReadHAWC2


fn1 = './res/iiib_c1.hdf5'
fn2 = './res/iiib_c2.hdf5'
fn3 = './res/iiib_c3.hdf5'
fn4 = './res/iiib_c4.hdf5'
fn5 = './res/iiib_c5.hdf5'
fn6 = './res/iiib_c6.hdf5'
fn7 = './res/iIIB_C7.hdf5'

# Split into two, as there should be two plots
f_names1=[fn1, fn2, fn3]
f_names2=[fn4, fn5, fn6]

labels_1 = ['C1', 'C2', 'C3']
labels_2 = ['C4', 'C5', 'C6']

# First plot : C1 to C3

fig1, ax1 = plt.subplots(4, figsize=(8, 5), sharex=True)
ax1[0].set(ylabel='Wind Speed, Vz [m/s]')
ax1[1].set(ylabel='Pitch Angle [deg]')
ax1[2].set(ylabel='Rotor Speed [s]')
ax1[3].set(ylabel='Power [kW]',
            xlabel='Time [s]')


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
plt.savefig('../results/control/control_response_c1_c3.pdf')

fig2, ax2 = plt.subplots(4, figsize=(8, 5), sharex=True)
ax2[0].set(ylabel='Wind Speed, Vz [m/s]')
ax2[1].set(ylabel='Pitch Angle [deg]')
ax2[2].set(ylabel='Rotor Speed [s]')
ax2[3].set(ylabel='Power [kW]',
           xlabel='Time [s]')

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
plt.savefig('../results/control/control_response_c4_c6.pdf')
plt.show()
