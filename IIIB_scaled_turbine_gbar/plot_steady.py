# -*- coding: utf-8 -*-
"""Compare mean value of steady simulations in HAWC2 (blue dots) to "theory" (lines).

For the operational parameters (i.e., pitch, rotor speed, etc.), the "theoretical" values
are the corresponding values in a .pwr file.

For the load channels of interest, the theoretical lines are calculated according to the
theoretical equations we derived for each load channel, as a function of thrust/torque/
gravity moment.

YOUR TASK! Add the lines that calculate the theory, as prompted by the slides.
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def load_hawc2s(path):
    """load channels from a pwr or opt file"""
    pwr = True if path.endswith('.pwr') else False
    data = np.loadtxt(path, skiprows=1)
    if pwr:
        u = data[:, 0]  # wind speed [m/s]
        paero = data[:, 1] * 1e3  # aerodynamic power [W]
        thrust = data[:, 2] * 1e3  # thrust [N]
        pitch = data[:, 8]  # pitch [deg]
        rotspd = data[:, 9] * np.pi/30  # rotational speed [rad/s]
        aerotrq = paero / rotspd  # aerodynamic torque [Nm]
    else:
        u = data[:, 0]  # wind speed [m/s]
        pitch = data[:, 1]  # pitch [deg]
        rotspd = data[:, 2] * np.pi/30  # rotational speed [rad/s]
        paero = data[:, 3] * 1e3  # aerodynamic power [W]
        thrust = data[:, 4] * 1e3  # thrust [N]
        aerotrq = paero / rotspd  # aerodynamic torque [Nm]
    return u, pitch, rotspd, paero, thrust, aerotrq


hawc2s_path = 'data/IIIB_scaled_turbine_flex.opt'  # path to .pwr or .opt file
stats_path = 'postprocess_hawc2/steady/iiib_scaled_turbine_steady_stats.hdf5'  # path to mean steady stats
subfolder = '.'  # which subfolder to plot: tilt, notilt, notiltrigid, notiltnodragrigid

geneff = 0.94  # generator/gearbox efficienty [%]
Mgrav = 6250  # yaw-bearing pitch moment due to gravity [kNm]
if 'notilt' in subfolder:
    dz_yb = 2.75  # distance from hub center to yaw bearing [m]
    dz_tb = 115.63 + dz_yb  # distance from hub center to tower base [m]
else:
    dz_yb = 2.75 + 7.1*np.sin(5*np.pi/180)  # distance from hub center to yaw bearing [m]
    dz_tb = 115.63 + dz_yb  # distance from hub center to tower base [m]

# define the channels and names to plot
channels = {4: 'Pitch angle [deg]',
            10: 'Rotor speed [rad/s]',
            13: 'Thrust [kN]',
            81: 'Generator torque [Nm]',
            111: 'Electrical power [W]',
            19: 'Tower-base FA [kNm]',
            20: 'Tower-base SS [kNm]',
            22: 'Yaw-bearing tilt [kNm]',
            23: 'Yaw-bearing roll [kNm]',
            27: 'Shaft torsion [kNm]',
            120: 'Out-of-plane BRM [kNm]',
            121: 'In-plane BRM [kNm]'}
i_wind = 15  # wind channel, needed for plotting versus wind speed

# load the HAWC2 data from the stats file. Isolate the simulations with no tilt.
stats_df = pd.read_hdf(stats_path, 'stats_df')
df = stats_df[stats_df.subfolder == subfolder]
breakpoint()
# load the stuff we need from the HAWC2S opt/pwr file for the operational data comparisons
h2s_u, h2s_pitch, h2s_rotspd, h2s_paero, h2s_thrust, h2s_aerotrq = load_hawc2s(hawc2s_path)

# initialize the figure and axes
fig, axs = plt.subplots(4, 3, figsize=(16, 9), clear=True)

# loop over each channels and plot the steady state with the theory line
for iplot, (ichan, name) in enumerate(channels.items()):
    
    # extract hawc2 wind and channel to plot from the HAWC2 stats
    h2_wind = df.loc[df.ichan == i_wind, 'mean']
    HAWC2val = df.loc[df.ichan == ichan, 'mean']

    # hawc2 channels we need for the theoretical calculations
    h2_thrust = df.loc[df.ichan == 13, 'mean']  # thrust [kN]
    h2_aero_trq = df.loc[df.ichan == 81, 'mean'] / geneff * 1e-3  # aerodynamic torque [kNm]
    
    # PART 1. HAWC2 operational data versus HAWC2S "theory" from opt/pwr file.
    if 'pitch angle' in name.lower():  # pitch angle
        u_theory = h2s_u
        theory = h2s_pitch
    elif 'rotor speed' in name.lower():  # rotor speed
        u_theory = h2s_u
        theory = h2s_rotspd  # CORRECT ME!!!
    elif 'thrust' in name.lower():  # thrust
        u_theory = h2s_u
        theory = h2s_thrust * 1e-3  # CORRECT ME!!!
    elif 'torque' in name.lower():  # generator torque
        u_theory = h2s_u
        theory = h2s_aerotrq * geneff  # CORRECT ME!!!
    elif 'power' in name.lower():  # electrical power
        u_theory = h2s_u
        theory = h2s_paero * geneff  # CORRECT ME!!!

    # PART 2. Theoretical lines are equations in lecture calculated from hawc2 values.
    elif ' FA' in name:  # tower-base fore-aft
        u_theory = h2_wind
        theory = h2_thrust * dz_tb - Mgrav
    elif ' SS' in name:  # tower-base side-side
        u_theory = h2_wind
        theory = h2_aero_trq  # CORRECT ME!!!
    elif 'bearing tilt' in name.lower():  # yaw bearing pitch
        u_theory = h2_wind
        theory = h2_thrust * dz_yb - Mgrav   # CORRECT ME!!!
    elif 'bearing roll' in name.lower():  # yaw bearing roll
        u_theory = h2_wind
        theory = h2_aero_trq  # CORRECT ME!!!
    elif 'torsion' in name.lower():  # shaft torsion
        u_theory = h2_wind
        theory =  -h2_aero_trq # CORRECT ME!!!
    elif 'out-of-plane' in name.lower():  # blade root out-of-plane moment
        u_theory = h2_wind
        theory = np.full_like(u_theory, np.nan)  # leave me -- no theory for OoP moment
    elif 'in-plane' in name.lower():  # blade root in-plane moment
        u_theory = h2_wind
        theory = h2_aero_trq/3  # CORRECT ME!!!
    
    # other values have no theory
    else:
        u_theory = h2_wind
        theory = np.nan * np.ones_like(u_theory)

    # sort both the theory and the hawc2 by increasing wind speed (convert to numpy arrays first)
    u_theory, theory = np.array(u_theory), np.array(theory)
    h2_wind, HAWC2val = np.array(h2_wind), np.array(HAWC2val)
    i_theory = np.argsort(u_theory)
    i_h2 = np.argsort(h2_wind)

    # define legend label for the "theoretical" line
    if np.nan in theory:
        theory_label = None
    elif np.array_equal(u_theory, h2s_u):
        theory_label = 'HAWC2S'
        linestyle, color = ':', 'r'
    else:
        theory_label = 'Theoretical equation'
        linestyle, color = '--', '#ffa500'

    # plot the results
    ax = axs.flatten()[iplot]
    ax.plot(u_theory[i_theory], theory[i_theory], linestyle=linestyle, c=color, label=theory_label)  # theoretical line
    ax.plot(h2_wind[i_h2], HAWC2val[i_h2], 'o', label='HAWC2 mean')  # HAWC2 steady results
    ax.grid('on')
    ax.set(xlabel='Wind speed [m/s]' if iplot > 8 else None, ylabel=name, xlim=[4, 25])

axs[0, 0].legend()
axs[1, 2].legend()
fig.suptitle(subfolder)
fig.tight_layout()

plt.show()
