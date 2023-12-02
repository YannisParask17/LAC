# %%
import matplotlib.pyplot as plt
import numpy as np
from lacbox.aero import root_chord, min_tc_chord, max_twist
from lacbox.io import load_ae, save_ae, load_c2def, save_c2def, load_pwr
import json

# %%
r_hub = 2.8

# Input files
htc_path = r"..\dtu_10mw\dtu_10mw_hawc2s_rigid_1point.htc"
ae_path = '../dtu_10mw/data/DTU_10MW_RWT_ae.dat' 
redesign_data_path = "../results/design_parameters_at_max_cp_JULIO.json"

# Computing the spacing of the elements from the ae file
span_RWT, chord_RWT, tc_RWT, _  = load_ae(ae_path, unpack=True)      # Get the RWT data
r_RWT = span_RWT + r_hub

c2_def = load_c2def(htc_path)
twist_RWT = - np.interp(span_RWT, c2_def[:, 2], c2_def[:,3])
c2_def[:,3]

with open(redesign_data_path, 'r') as json_file:
    redesign_data_dict = json.load(json_file)

r_new = list(redesign_data_dict['r'].values())
chord_new = list(redesign_data_dict['chord'].values())
tc_new = list(redesign_data_dict['tc'].values())
twist_new = list(redesign_data_dict['twist'].values())
# %% Plot the chord, twist and thickness

fig, axs = plt.subplots(3, 1, num=2, clear=True, sharex=True)

# t/c
axs[0].grid(True)  # Add grid
axs[0].plot(r_RWT, tc_RWT, color="tab:red",  lw=1, label='DTU 10MW RWT')
axs[0].plot(r_new, tc_new, color="tab:blue", label='Redesign')

axs[0].set_ylabel('Rel. thickness [%]')
axs[0].legend()

# Chord
axs[1].grid(True)  # Add grid
axs[1].plot(r_RWT, chord_RWT, color="tab:red",  lw=1)
axs[1].plot(r_new, chord_new, color="tab:blue" )
axs[1].set_ylim(bottom=0)
axs[1].set_ylabel('Chord [m]')
# Twist
axs[2].grid(True)  # Add grid
axs[2].plot(r_RWT, twist_RWT,color="tab:red",  lw=1)
axs[2].plot(r_new, twist_new, color="tab:blue")
axs[2].set_ylabel('Twist [deg]')

axs[2].set_xlabel('Rotor span [m]')
fig.tight_layout()
fig.show()
# %%

pwr_path = r"..\IIIB_scaled_turbine_Julio\IIIB_scaled_turbine_rigid_varTSR_JULIO.pwr"
# Load the data
pwr_data = load_pwr(pwr_path)

R = 92.5
V=8

ws_lst = pwr_data["V_ms"]
pwr_lst = pwr_data["P_kW"]
tsr_lst = pwr_data["Speed_rpm"]*np.pi/30*R/V
Cp_lst = pwr_data["Cp"]
Ct_lst = pwr_data["Ct"]
tsr_max = tsr_lst[np.argmax(Cp_lst)]



# %%
# Path for the file
pwr_path = r"..\IIIB_scaled_turbine_Julio\IIIB_scaled_turbine_JULIO.pwr"
# Load the data
pwr_data = load_pwr(pwr_path)

ws_lst = pwr_data["V_ms"]
pwr_lst = pwr_data["P_kW"]
thrust_lst = pwr_data["T_kN"]
tsr_lst = pwr_data["Speed_rpm"]*np.pi/30*R/V
Cp_lst = pwr_data["Cp"]
Ct_lst = pwr_data["Ct"]

pwr_path = r"..\dtu_10mw\dtu_10mw_hawc2s_flex_minrotspd.pwr"
# Load the data
pwr_data_RWT = load_pwr(pwr_path)

ws_RWT = pwr_data_RWT["V_ms"]
pwr_RWT = pwr_data_RWT["P_kW"]
thrust_RWT = pwr_data_RWT["T_kN"]
tsr_RWT = pwr_data_RWT["Speed_rpm"]*np.pi/30*R/V
Cp_RWT = pwr_data_RWT["Cp"]
Ct_RWT = pwr_data_RWT["Ct"]

#%%

fig, axs = plt.subplots(2, 2, num=2, clear=True, sharex=True, figsize = (8.5,4), layout="constrained")

axs[0,0].grid(True)
axs[0,0].plot(ws_lst, pwr_RWT)
axs[0,0].plot(ws_lst, pwr_lst)
axs[0,0].set_ylabel("Mech. Power [kW]")

axs[1,0].grid(True)
axs[1,0].plot(ws_lst, Cp_RWT)
axs[1,0].plot(ws_lst, Cp_lst)
axs[1,0].set_ylabel("$C_P$ [-]")
axs[1,0].set_xlabel("Wind speed [m/s]")


axs[0,1].grid(True)
axs[0,1].plot(ws_lst, thrust_RWT)
axs[0,1].plot(ws_lst, thrust_lst)
axs[0,1].set_ylabel("Thrust [kN]")

axs[1,1].grid(True)
axs[1,1].plot(ws_lst, Ct_RWT)
axs[1,1].plot(ws_lst, Ct_lst)
axs[1,1].set_ylabel("$C_T$ [-]")
axs[1,1].set_xlabel("Wind speed [m/s]")

# %%


# %%

