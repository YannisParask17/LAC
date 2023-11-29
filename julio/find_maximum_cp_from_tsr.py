# %% Import modules
from scripts.aero_design_functions import get_design_functions, solve_tc, solve_bem, CLP_fun, CP_fun, CLT_fun, CT_fun, chord_fun, twist_deg_fun
from lacbox.aero import root_chord, min_tc_chord, max_twist
from lacbox.io import load_ae, save_ae, load_c2def, save_c2def
import numpy as np
import matplotlib.pyplot as plt
# import json
import pandas as pd

# Inputs
R = 92.5  # length of blade [m] -> Should not be blade length, but radius
r_old = 178.3/2
# tsr = 9.0  # TSR [-]
B = 3  # number of blades
a = 1/3  # axial induction [-]
r_hub = 2.8

chord_max = 6.0     # Maximum chord size [m]
chord_root = 5.38   # Chord at the root [m]


# Switches

plot_thickness = True

# IO of the AE file
data_path = "../dtu_10mw"

ae_path = '../dtu_10mw/data/DTU_10MW_RWT_ae.dat' 
htc_path = r'..\dtu_10mw\dtu_10mw_hawc2s_rigid_1point.htc'


# Out
c2def_save_path = '../results/hawc_files/c2_def_scaled_JULIO.txt'
out_path = '../results/hawc_files/10MW_IIIB_ae_JULIO.dat'
json_out = "../results/design_parameters_at_max_cp_JULIO.json"

c2def_save_path1 = '../results/hawc_files/c2_def_scaled.txt' # For origina design
out_path1 = '../results/hawc_files/10MW_IIIB_ae.dat'
json_out1 = "../results/design_parameters_at_max_cp_.json"

# Function for the absolute thickness vs span for the 35 m blade
def thickness(r):
    """Absolute thickness [m] as a function of blade span [m] with the adapted polynomial coeffs"""
    p_edge = [-1.850596047180256051e-13,
              7.691381134546526722e-11,
              -1.354769902773717907e-08,
              1.305293765103693518e-06,
              -7.377855176793037461e-05,
              2.410743711971400152e-03,
              -3.989165296263064847e-02,
              1.221564339981970615e-01,
              5.541080966680200781e+00]  # polynomial coefficients
    t_poly = np.polyval(p_edge, r)  # evaluate polynomial
    t = np.minimum(t_poly, chord_root)  # clip at max thickness
    return t


# Aero dynamic polar design functions and the values (t/c vs. cl, cd, aoa)
cl_des, cd_des, aoa_des, tc_vals, cl_vals, cd_vals, aoa_vals = get_design_functions(2)


# Computing the spacing of the elements from the ae file
ae_data = load_ae(ae_path)      # Get the RWT data
r_old = ae_data[-1, 0]+r_hub
scaling_factor = (R-r_hub)/(r_old-r_hub)
rad_positions_ae = ae_data[:, 0]* scaling_factor
r_lst = r_hub + rad_positions_ae
r_lst[-1]=r_lst[-1]-0.05
_, chord_original, tc_original, _ = load_ae(ae_path, unpack=True)



# Solving for the relative thickness (t/c)
# Computing absolute thickness
t = thickness(r_lst-r_hub)
# Plot the thickness
if plot_thickness:  # Super inefficient code, but good enough
    # pass data to variables
    radius_plot, chord_plot, tc_ratio_plot, pcset_plot = load_ae(ae_path, unpack=True)
    thickness_plot = tc_ratio_plot*chord_plot/100
    plt.figure(figsize=(4.5, 2.2))
    plt.plot(radius_plot/r_old, thickness_plot, color='C0', label="RWT")
    plt.plot((r_lst-r_hub)/R, t, color='C1', label="Scaled")
    plt.xlabel("r/R (-)")
    plt.ylabel("Thickness (m)")
    plt.grid()
    plt.legend()
    plt.savefig("../results/aero_design/thickness_limited.pdf", bbox_inches='tight')
    plt.show()


def solve_CP(cl_des, r_lst, t, tsr, R, a, B):
    # Solving for t/c
    tc_ideal = solve_tc(cl_des, r_lst, t, tsr, R, a, B)
    # Getting ideal aero cl (before changing chord)
    cl_ideal = cl_des(tc_ideal)  # [-]

    # Chord [m]
    chord_ideal = chord_fun(r_lst, tsr, R, a, B, cl_ideal)          # calculating ideal chord
    chord = root_chord(r_lst, chord_ideal, chord_root, chord_max)   # transition from ideal to root chord
    chord = min_tc_chord(chord, t)                              # maintain minimum t/c at the tip

    # Updating t/c and polar design values
    tc = t/chord*100
    cl = cl_des(tc)             # [-]
    cd = cd_des(tc)             # [-]
    aoa_ideal = aoa_des(tc)     # [deg]

    # Twist [deg]
    twist_ideal = twist_deg_fun(r_lst, tsr, R, a, aoa_ideal)  # [deg]
    twist = max_twist(twist_ideal, 20)  # Limiting the twist angle at 20 degrees

    # Updating aoa
    aoa = twist_deg_fun(r_lst, tsr, R, a, 0)-twist  # Updating the design aoa for the constraint twist

    # Updating a
    a = solve_bem(r_lst, tsr, R, chord, cl, B)
    CLT = CLT_fun(r_lst, tsr, R, a, B, cl, cd, chord)
    CLP = CLP_fun(r_lst, tsr, R, a, B, cl, cd, chord)
    CT = CT_fun(r_lst, R, CLT)
    CP = CP_fun(r_lst, R, CLP)
    return CT, CP, chord, tc, cl, cd, twist, aoa, a, CLT, CLP


tsr_list = np.linspace(6, 9, 40)
CP_list = np.zeros(len(tsr_list))
CT_list = np.zeros(len(tsr_list))
chord_lst = []
tc_lst = np.zeros_like(tsr_list)
cl_lst = np.zeros_like(tsr_list)
cd_lst = np.zeros_like(tsr_list)
twist_lst = np.zeros_like(tsr_list)
aoa_lst = np.zeros_like(tsr_list)
for i, tsr in enumerate(tsr_list):
    CT, CP, chord, tc, cl, cd, twist, aoa, _, _, _ = solve_CP(cl_des, r_lst, t, tsr, R, a, B)
    CP_list[i] = CP
    CT_list[i] = CT
    chord_lst.append(chord)
    print(i)

idx_opt = np.argmax(CP_list)

# %% Plotting chords
plt.figure()
for i in range(0, 10, 2):
    print(i)
    try:
        plt.plot(r_lst, chord_lst[idx_opt+i], label=f"TSR = {tsr_list[idx_opt+i]:.3f}")
    except IndexError:
        pass
plt.legend()
plt.show()
# # %% Plotting design functions
# tc_plot = np.linspace(0, 100, 100)
# fig, axs = plt.subplots(3, 1)

# axs[0].plot(tc_plot, cl_des(tc_plot), "k")
# axs[0].plot(tc_vals, cl_vals, "ok")
# axs[0].set_ylabel("$C_l$ [-]")

# axs[1].plot(tc_plot, cd_des(tc_plot), "k")
# axs[1].plot(tc_vals, cd_vals, "ok")
# axs[1].set_ylabel("$C_d$ [-]")

# axs[2].plot(tc_plot, aoa_des(tc_plot), "k")
# axs[2].plot(tc_vals, aoa_vals, "ok")
# axs[2].set_ylabel(r"$\alpha$ [-]")
# axs[2].set_xlabel(r"$t/c$ [deg]")

# fig.tight_layout()

# fig.show()

# # %% Plot the chord, twist and thickness
# fig, axs = plt.subplots(3, 1, num=2, clear=True)
# # t/c
# axs[0].plot(r_lst, tc_ideal, "C0--", lw=1)
# axs[0].plot(r_lst, tc, "C0")

# axs[0].set_ylabel('Rel. thickness [%]')
# # Chord
# axs[1].plot(r_lst, chord_ideal, "C0--", lw=1)
# axs[1].plot(r_lst, chord, "C0")
# axs[1].set_ylabel('Chord [m]')
# # Twist
# axs[2].plot(r_lst, twist_ideal, "C0--", lw=1)
# axs[2].plot(r_lst, twist, "C0")
# axs[2].set_ylabel('Twist [deg]')
# axs[2].set_xlabel('Rotor span [m]')
# fig.tight_layout()
# fig.show()

# # # %% Plot r vs. t/c, cl, cd, aoa
# fig, ax = plt.subplots(2, 2, num=4, clear=True)
# # t/c
# ax[0, 0].plot(r_lst, tc_ideal, "C0--", lw=1)
# ax[0, 0].plot(r_lst, tc, "C0")
# ax[0, 0].set_ylabel("t/c [%]")
# # cl
# ax[0, 1].plot(r_lst, cl_ideal, "C0--", lw=1)
# ax[0, 1].plot(r_lst, cl)
# ax[0, 1].set_ylabel("$C_l$ [-]")
# # cl/cd
# ax[1, 0].plot(r, cd)
# ax[1, 0].set_ylabel("$C_d$ [-]")
# ax[1, 0].set_xlabel("Span [m]")
# # aoa
# ax[1, 1].plot(r_lst, aoa)
# ax[1, 1].set_ylabel(r"$\alpha$ [deg]")
# ax[1, 1].set_xlabel("Span [m]")

# # # %% Plot r vs. CLT, CLP
# fig, axs = plt.subplots(3, 1, num=3, clear=True)
# axs[0].plot(r_lst, CLT)
# axs[0].axhline(y=8/9, ls="--", color="k", lw=1)
# axs[0].grid('on')
# axs[0].set_ylabel('Local thrust ($C_{LT}$) [-]')
# axs[0].set_ylim(0, 1.0)
# axs[1].plot(r_lst, CLP)
# axs[1].axhline(y=16/27, ls="--", color="k", lw=1)
# axs[1].grid('on')
# axs[1].set_ylabel('Local Power ($C_{LP}$) [-]')
# axs[2].plot(r_lst, a)
# axs[2].axhline(y=1/3, ls="--", color="k", lw=1)
# axs[2].grid('on')
# axs[2].set_ylabel('Axial induction ($a$) [-]')
# axs[2].set_xlabel('Rotor span [m]')
# fig.suptitle(f"$C_T$={CT:1.3f}, $C_P$={CP:1.3f}")
# fig.tight_layout()
# fig.show()


#  %% TSR vs CP

CP_max = np.argmax(CP_list)
tsr_max = tsr_list[CP_max]

fig, ax1 = plt.subplots(figsize=(5, 2.5))
print(tsr_list)
ax2 = ax1.twinx()
ax1.plot(tsr_list, CP_list, "b--", label="CP")
ax2.plot(tsr_list, CT_list, "r-.", label="CT")
ax2.axvline(tsr_max, label = r"$CP_{max}$ " +f"($\lambda$ = {tsr_max:2.2f})", color = "grey", markersize = 5)
# lns4 = ax1.axhline(16/27, label = "Betz Limit")
ax1.set_xlabel(r"Tip Speed Ratio [-]")
ax1.set_ylabel("Power Coefficient [-]")
ax2.set_ylabel("Thrust Coefficient [-]")
ax1.grid(True)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
ax1.legend(lines, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1.4))

# lns = lns1+lns2
# labs = [l.get_label() for l in lns]
# ax1.legend(lns, labs, loc=[0.02, 0.87])

plt.tight_layout()
# plt.savefig('../results/aero_design/cp_ct.pdf', bbox_inches='tight')
plt.show(block=True)

#%%
CT, CP, chord, tc, cl, cd, twist, aoa, a, CLT, CLP = solve_CP(cl_des, r_lst, t, tsr_max, R, a, B)

df_new = pd.DataFrame({"r" : r_lst, "a" : a,"CT": CT, "CP": CP, "CLP" : CLP, "CLT" : CLT, "chord": chord, "tc": tc, "cl": cl, "cd": cd, "twist": twist, "aoa": aoa})
df_new.to_json(json_out)


# Change the ae file and save it
ae_new = ae_data.copy()
ae_new[:, 0] = rad_positions_ae     # radial position
ae_new[:, 1] = chord    # Chord
ae_new[:, 2] = tc       # T/C ratio
save_ae(out_path1, ae_new)

# Change the C2Def

# Get the centerline from the c2def block in the htc file
c2_def = load_c2def(htc_path)  # x, y , z , theta

c2_def_new = c2_def.copy()
c2_def_new[:, 2] *= scaling_factor      # Scale the z coordinate
twist_interp = - np.interp(c2_def_new[:, 2], rad_positions_ae, twist)
c2_def_new[:, 3] = twist_interp               # Add new twist

save_c2def(c2def_save_path1, c2_def_new)


print("Done!")

# %%
# Julio's design
#I choose a TSR of 7.5 

tsr_chosen = 7.5 

CT_julio, CP_julio, chord_julio, tc_julio, cl_julio, cd_julio, twist_julio, aoa_julio, a_julio, CLT_julio, CLP_julio = solve_CP(cl_des, r_lst, t, tsr_chosen, R, a, B)

# # %% Plot r vs. CLT, CLP
fig, axs = plt.subplots(3, 1, num=3, clear=True)
axs[0].plot(r_lst, CLT_julio)
axs[0].axhline(y=8/9, ls="--", color="k", lw=1)
axs[0].grid('on')
axs[0].set_ylabel('Local thrust ($C_{LT}$) [-]')
axs[0].set_ylim(0, 1.0)
axs[1].plot(r_lst, CLP_julio)
axs[1].axhline(y=16/27, ls="--", color="k", lw=1)
axs[1].grid('on')
axs[1].set_ylabel('Local Power ($C_{LP}$) [-]')
axs[2].plot(r_lst, a_julio)
axs[2].axhline(y=1/3, ls="--", color="k", lw=1)
axs[2].grid('on')
axs[2].set_ylabel('Axial induction ($a$) [-]')
axs[2].set_xlabel('Rotor span [m]')
fig.suptitle(f"$C_T$={CT:1.3f}, $C_P$={CP:1.3f}")
fig.tight_layout()
fig.show()

# %% Plot the chord, twist and thickness
r_lst_orig = ae_data[:, 0] + r_hub

fig, axs = plt.subplots(3, 1, num=2, clear=True, sharex=True)

# t/c
axs[0].grid(True)  # Add grid
axs[0].plot(r_lst_orig, tc_original, color="tab:red", linestyle="--", lw=1, label='DTU 10MW RWT')
axs[0].plot(r_lst, tc, color="tab:blue", linestyle="--", label='1st Redesign')
axs[0].plot(r_lst, tc_julio, color="tab:blue", label='2nd Redesign')

axs[0].set_ylabel('Rel. thickness [%]')
axs[0].legend()

# Chord
axs[1].grid(True)  # Add grid
axs[1].plot(r_lst_orig, chord_original, color="tab:red", linestyle="--", lw=1)
axs[1].plot(r_lst, chord, color="tab:blue", linestyle="--")
axs[1].plot(r_lst, chord_julio, color="tab:blue")
axs[1].set_ylim(bottom=0)
axs[1].set_ylabel('Chord [m]')
# Twist
axs[2].grid(True)  # Add grid
# axs[2].plot(r_lst, 0, "C0--", lw=1)
# axs[2].plot(r_lst, twist_julio, "C0")
# axs[2].set_ylabel('Twist [deg]')

axs[2].set_xlabel('Rotor span [m]')
# axs[2].set_xlabel('Rotor span [m]')
fig.tight_layout()
fig.show()
# %%

fig, ax1 = plt.subplots(figsize=(5, 2.5))
print(tsr_list)
ax2 = ax1.twinx()
ax1.plot(tsr_list, CP_list, "b--", label="CP")
ax2.plot(tsr_list, CT_list, "r-.", label="CT")
ax2.axvline(tsr_max, label = r"$CP_{max}$ " +f"($\lambda$ = {tsr_max:2.2f})", color = "grey", markersize = 5, linestyle="--")
ax2.axvline(tsr_chosen, label = r"$CP_{design}$ " +f"($\lambda$ = 7.5)", color = "grey", markersize = 5)
# lns4 = ax1.axhline(16/27, label = "Betz Limit")
ax1.set_xlabel(r"Tip Speed Ratio [-]")
ax1.set_ylabel("Power Coefficient [-]")
ax2.set_ylabel("Thrust Coefficient [-]")
ax1.grid(True)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
lines = lines1 + lines2
labels = labels1 + labels2
ax1.legend(lines, labels, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 1.35))


# %%

df_new = pd.DataFrame({"r" : r_lst, "a" : a_julio,"CT": CT_julio, "CP": CP_julio, "CLP" : CLP_julio, "CLT" : CLT_julio, "chord": chord_julio, "tc": tc_julio, "cl": cl_julio, "cd": cd_julio, "twist": twist_julio, "aoa": aoa_julio})
df_new.to_json(json_out)


# Change the ae file and save it
ae_new = ae_data.copy()
ae_new[:, 0] = rad_positions_ae     # radial position
ae_new[:, 1] = chord_julio    # Chord
ae_new[:, 2] = tc_julio       # T/C ratio
save_ae(out_path, ae_new)



#%%
# Change the C2Def
# Get the centerline from the c2def block in the htc file
c2_def = load_c2def(htc_path)  # x, y , z , theta

c2_def_new = c2_def.copy()
c2_def_new[:, 2] *= scaling_factor      # Scale the z coordinate
twist_interp = - np.interp(c2_def_new[:, 2], rad_positions_ae, twist)
c2_def_new[:, 3] = twist_interp               # Add new twist

save_c2def(c2def_save_path, c2_def_new)


print("Done!")