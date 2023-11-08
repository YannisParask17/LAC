import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    from rich import print
except:
    pass
from lacbox.io import ReadHAWC2
from lacbox.test import test_data_path
from pathlib import Path
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



hawc2s_path = '../../IIIB_scaled_turbine_gbar/data/IIIB_scaled_turbine_flex.opt'  # path to .pwr or .opt file
stats_path = '../../IIIB_scaled_turbine_gbar/postprocess_hawc2/turbulent/iiib_scaled_turbine_turb_tcb.hdf5'  # path to mean steady stats
subfolder = '.'  # which subfolder to plot: tilt, notilt, notiltrigid, notiltnodragrigid
subfolder_dtu10mw = 'tca'  # which subfolder to plot: tilt, notilt, notiltrigid, notiltnodragrigid
stats_path_dtu10mw = '../../IIIB_scaled_turbine_gbar/postprocess_hawc2/turbulent/dtu_10mw_turb_stats.hdf5'  # path to mean steady stats
save_path = '' 

geneff = 0.94  # generator/gearbox efficienty [%]

# define the channels and names to plot
channels_oper = {4: 'Pitch angle [deg]',
            10: 'Rotor speed [rad/s]',
            13: 'Thrust [kN]',
            81: 'Generator torque [Nm]',
            111: 'Electrical power [W]'}

i_wind = 15  # wind channel, needed for plotting versus wind speed


# load the HAWC2 data from the stats file. Isolate the simulations with no tilt.
stats_df = pd.read_hdf(stats_path, 'stats_df')
df = stats_df[stats_df.subfolder == subfolder]
# load the HAWC2 data from the stats file. Isolate the simulations with no tilt.
stats_df_dtu10mw = pd.read_hdf(stats_path_dtu10mw, 'stats_df')
df_dtu10mw = stats_df_dtu10mw[stats_df_dtu10mw.subfolder == subfolder_dtu10mw]

# load the stuff we need from the HAWC2S opt/pwr file for the operational data comparisons
h2s_u, h2s_pitch, h2s_rotspd, h2s_paero, h2s_thrust, h2s_aerotrq = load_hawc2s(hawc2s_path)

# initialize the figure and axes
fig, axs = plt.subplots(5, figsize=(16, 9), clear=True)

if False:
    # loop over each channels and plot the steady state with the theory line
    for iplot, (ichan, name) in enumerate(channels_oper.items()):
        
        # extract hawc2 wind and channel to plot from the HAWC2 stats -> IIIB Redesign
        h2_wind = df.loc[df.ichan == i_wind, 'mean']
        HAWC2val = df.loc[df.ichan == ichan, ['mean', 'max', 'min']]

        # hawc2 channels we need for the theoretical calculations
        h2_thrust = df.loc[df.ichan == 13, ['mean', 'max', 'min']]  # thrust [kN]
        h2_aero_trq = df.loc[df.ichan == 81, ['mean', 'max', 'min']] / geneff * 1e-3  # aerodynamic torque [kNm]
        # breakpoint()

        # extract hawc2 wind and channel to plot from the HAWC2 stats -> DTU 10MW
        h2_wind_dtu10mw = df_dtu10mw.loc[df_dtu10mw.ichan == i_wind, 'mean']
        HAWC2val_dtu10mw = df_dtu10mw.loc[df_dtu10mw.ichan == ichan, ['mean', 'max', 'min']]

        # hawc2 channels we need for the theoretical calculations
        h2_thrust_dtu10mw = df_dtu10mw.loc[df_dtu10mw.ichan == 13, ['mean', 'max', 'min']]  # thrust [kN]
        h2_aero_trq_dtu10mw = df_dtu10mw.loc[df.ichan == 81, ['mean', 'max', 'min']] / geneff * 1e-3  # aerodynamic torque [kNm]
        # breakpoint()


        # PART 1. HAWC2 operational data versus HAWC2S "theory" from opt/pwr file.
        breakpoint()
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

        # # PART 2. Theoretical lines are equations in lecture calculated from hawc2 values.
        # elif ' FA' in name:  # tower-base fore-aft
        #     u_theory = h2_wind
        #     theory = h2_thrust * dz_tb - Mgrav
        # elif ' SS' in name:  # tower-base side-side
        #     u_theory = h2_wind
        #     theory = h2_aero_trq  # CORRECT ME!!!
        # elif 'bearing tilt' in name.lower():  # yaw bearing pitch
        #     u_theory = h2_wind
        #     theory = h2_thrust * dz_yb - Mgrav   # CORRECT ME!!!
        # elif 'bearing roll' in name.lower():  # yaw bearing roll
        #     u_theory = h2_wind
        #     theory = h2_aero_trq  # CORRECT ME!!!
        # elif 'torsion' in name.lower():  # shaft torsion
        #     u_theory = h2_wind
        #     theory =  -h2_aero_trq # CORRECT ME!!!
        # elif 'out-of-plane' in name.lower():  # blade root out-of-plane moment
        #     u_theory = h2_wind
        #     theory = np.full_like(u_theory, np.nan)  # leave me -- no theory for OoP moment
        # elif 'in-plane' in name.lower():  # blade root in-plane moment
        #     u_theory = h2_wind
        #     theory = h2_aero_trq/3  # CORRECT ME!!!
        
        # # other values have no theory
        # else:
        #     u_theory = h2_wind
        #     theory = np.nan * np.ones_like(u_theory)

        # sort both the theory and the hawc2 by increasing wind speed (convert to numpy arrays first)
        u_theory, theory = np.array(u_theory), np.array(theory)
        h2_wind, HAWC2val = np.array(h2_wind), np.array(HAWC2val)
        h2_wind_dtu10mw, HAWC2val_dtu10mw = np.array(h2_wind_dtu10mw), np.array(HAWC2val_dtu10mw)
        i_theory = np.argsort(u_theory)
        i_h2 = np.argsort(h2_wind)
        i_h2_dtu10mw = np.argsort(h2_wind_dtu10mw)


        # breakpoint()
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
        ax.plot(u_theory[i_theory], theory[i_theory], linestyle=linestyle, c=color)  # theoretical line
        ax.plot(h2_wind[i_h2], HAWC2val[i_h2], 'o',  color='C0')  # HAWC2 steady results
        ax.plot(h2_wind_dtu10mw[i_h2_dtu10mw], HAWC2val_dtu10mw[i_h2_dtu10mw], 'x', color='C1')  # HAWC2 steady results

        ax.grid('on')
        ax.set(xlabel='Wind speed [m/s]' if iplot > 8 else None, ylabel=name, xlim=[4, 25])

    # Add legend
    ax.lines[0].set_label(theory_label)  # Set the label for the line
    ax.lines[1].set_label("Redesign-IIIB")  # Set the label for the line
    ax.lines[4].set_label('DTU10MW-IA')  # Set the label for the line
    fig.legend(loc='outside upper center', ncol=3)
    fig.suptitle(subfolder)
    fig.tight_layout()
    fig.savefig('task1_operation.eps')
    plt.show()





# LOADS IN TURBULENCE
channels = {19: 'Tower-base FA [kNm]',
            20: 'Tower-base SS [kNm]',
            22: 'Yaw-bearing tilt [kNm]',
            23: 'Yaw-bearing roll [kNm]',
            27: 'Shaft torsion [kNm]',
            120: 'Out-of-plane BRM [kNm]',
            121: 'In-plane BRM [kNm]'}
i_wind = 15  # wind channel, needed for plotting versus wind speed


# NEEDS TO BE CHANGED : THIS IS FOR THE DTU10MW
Mgrav = 6250  # yaw-bearing pitch moment due to gravity [kNm]
dz_yb = 2.75 + 7.1*np.sin(5*np.pi/180)  # distance from hub center to yaw bearing [m]
dz_tb = 115.63 + dz_yb  # distance from hub center to tower base [m]


# initialize the figure and axes
fig, axs = plt.subplots(7, figsize=(16, 9), clear=True)

# loop over each channels and plot the steady state with the theory line
for iplot, (ichan, name) in enumerate(channels.items()):
    
    # extract hawc2 wind and channel to plot from the HAWC2 stats -> IIIB Redesign
    h2_wind = df.loc[df.ichan == i_wind, 'mean']
    HAWC2val = df.loc[df.ichan == ichan, ['mean', 'max', 'min']]
    max_val = np.max(df.loc[df.ichan == ichan, ['max']])
    min_val = np.min(df.loc[df.ichan == ichan, ['min']])
    abs_val = np.max([max_val, abs(min_val)])
    # hawc2 channels we need for the theoretical calculations
    h2_thrust = df.loc[df.ichan == 13, ['mean', 'max', 'min']]  # thrust [kN]
    h2_aero_trq = df.loc[df.ichan == 81, ['mean', 'max', 'min']] / geneff * 1e-3  # aerodynamic torque [kNm]
    # breakpoint()

    # extract hawc2 wind and channel to plot from the HAWC2 stats -> DTU 10MW
    h2_wind_dtu10mw = df_dtu10mw.loc[df_dtu10mw.ichan == i_wind, 'mean']
    HAWC2val_dtu10mw = df_dtu10mw.loc[df_dtu10mw.ichan == ichan, ['mean', 'max', 'min']]

    # hawc2 channels we need for the theoretical calculations
    h2_thrust_dtu10mw = df_dtu10mw.loc[df_dtu10mw.ichan == 13, ['mean', 'max', 'min']]  # thrust [kN]
    h2_aero_trq_dtu10mw = df_dtu10mw.loc[df.ichan == 81, ['mean', 'max', 'min']] / geneff * 1e-3  # aerodynamic torque [kNm]
    breakpoint()


    # # PART 1. HAWC2 operational data versus HAWC2S "theory" from opt/pwr file.
    # if 'pitch angle' in name.lower():  # pitch angle
    #     u_theory = h2s_u
    #     theory = h2s_pitch
    # elif 'rotor speed' in name.lower():  # rotor speed
    #     u_theory = h2s_u
    #     theory = h2s_rotspd  # CORRECT ME!!!
    # elif 'thrust' in name.lower():  # thrust
    #     u_theory = h2s_u
    #     theory = h2s_thrust * 1e-3  # CORRECT ME!!!
    # elif 'torque' in name.lower():  # generator torque
    #     u_theory = h2s_u
    #     theory = h2s_aerotrq * geneff  # CORRECT ME!!!
    # elif 'power' in name.lower():  # electrical power
    #     u_theory = h2s_u
    #     theory = h2s_paero * geneff  # CORRECT ME!!!
    # breakpoint()

    # PART 2. Theoretical lines are equations in lecture calculated from hawc2 values.
    if ' FA' in name:  # tower-base fore-aft
        u_theory = h2_wind
        theory = h2_thrust['mean'] * dz_tb - Mgrav
        max_fa = abs_val
    elif ' SS' in name:  # tower-base side-side
        u_theory = h2_wind
        theory = h2_aero_trq['mean']  # CORRECT ME!!!
        max_ss = max_val
    elif 'bearing tilt' in name.lower():  # yaw bearing pitch
        u_theory = h2_wind
        theory = h2_thrust['mean'] * dz_yb - Mgrav   # CORRECT ME!!!
        max_bearing_tilt = abs_val
    elif 'bearing roll' in name.lower():  # yaw bearing roll
        u_theory = h2_wind
        theory = h2_aero_trq['mean']  # CORRECT ME!!!
        max_bearing_roll = abs_val
    elif 'torsion' in name.lower():  # shaft torsion
        u_theory = h2_wind
        theory = -h2_aero_trq['mean']  # CORRECT ME!!!
        max_torsion = abs_val
    elif 'out-of-plane' in name.lower():  # blade root out-of-plane moment
        u_theory = h2_wind

        theory = np.full_like(u_theory, np.nan)  # leave me -- no theory for OoP moment
        max_oop_moment = abs_val
    elif 'in-plane' in name.lower():  # blade root in-plane moment
        u_theory = h2_wind
        theory = h2_aero_trq['mean']/3  # CORRECT ME!!!
        max_ip_moment = abs_val
    
    # other values have no theory
    else:
        u_theory = h2_wind
        theory = np.nan * np.ones_like(u_theory)

    # sort both the theory and the hawc2 by increasing wind speed (convert to numpy arrays first)
    u_theory, theory = np.array(u_theory), np.array(theory)
    h2_wind, HAWC2val = np.array(h2_wind), np.array(HAWC2val)
    h2_wind_dtu10mw, HAWC2val_dtu10mw = np.array(h2_wind_dtu10mw), np.array(HAWC2val_dtu10mw)
    i_theory = np.argsort(u_theory)
    i_h2 = np.argsort(h2_wind)
    i_h2_dtu10mw = np.argsort(h2_wind_dtu10mw)


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
    ax.plot(u_theory[i_theory], theory[i_theory], linestyle=linestyle, c=color)  # theoretical line
    ax.plot(h2_wind[i_h2], HAWC2val[i_h2], 'o',  color='C0')  # HAWC2 steady results
    ax.plot(h2_wind_dtu10mw[i_h2_dtu10mw], HAWC2val_dtu10mw[i_h2_dtu10mw], 'x', color='C1')  # HAWC2 steady results

    ax.grid('on')
    ax.set(xlabel='Wind speed [m/s]' if iplot > 8 else None, ylabel=name, xlim=[4, 25])

# Add legend
ax.lines[0].set_label(theory_label)  # Set the label for the line
ax.lines[1].set_label("Redesign-IIIB")  # Set the label for the line
ax.lines[4].set_label('DTU10MW-IA')  # Set the label for the line
fig.legend(loc='outside upper center', ncol=3)
fig.suptitle(subfolder)
fig.tight_layout()
#fig.savefig('task1_loads_stats.eps')
#plt.show()

# ===============================================================
# To-do
# ===============================================================
# 1. Use Mgrav value for our design
# 2. Find channel number for tip deflection and include it
# 3. Manipulate graph layout a bit
# 4. Stay sexy
# ===============================================================
print("=============MAX VALUES==============")
print(f"Max FA:\t{max_fa}")
print(f"Max SS:\t{max_ss}")
print(f"Max torsion:\t{max_torsion}")
print(f"Max bearing_tilt:\t{max_bearing_tilt}")
print(f"Max bearing_roll:\t{max_bearing_roll}")
print(f"Max ip moment:\t{max_ip_moment}")
print(f"Max oop moment:\t{max_oop_moment}")

print("=============DESIGN LOADS==============")
safety_factor = 1.35 * 1.25
print(f"Max FA:\t{max_fa*safety_factor}")
print(f"Max SS:\t{max_ss*safety_factor}")
print(f"Max torsion:\t{max_torsion*safety_factor}")
print(f"Max bearing_tilt:\t{max_bearing_tilt*safety_factor}")
print(f"Max bearing_roll:\t{max_bearing_roll*safety_factor}")
print(f"Max ip moment:\t{max_ip_moment*safety_factor}")
print(f"Max oop moment:\t{max_oop_moment*safety_factor}")
