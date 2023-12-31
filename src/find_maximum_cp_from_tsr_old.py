# %% Import modules
from aero_design_functions import get_design_functions, solve_tc, solve_bem, CLP_fun, CP_fun, CLT_fun, CT_fun, chord_fun, twist_deg_fun
from lacbox.aero import root_chord, min_tc_chord, max_twist
import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd

# f = open("polar_data.json",)
# data = json.load(f)
# f.close()
# df = pd.DataFrame(data)
# Inputs
R = 92.5  # length of blade [m]
# tsr = 9.0  # TSR [-]
B = 3  # number of blades
a = 1/3  # axial induction [-]
r_hub = 2.8
r = np.linspace(r_hub, R-0.6, 50)  # Rotor span [m]
chord_max = 6.0 # Maximum chord size [m]
chord_root = 5.38 # Chord at the root [m]

# Function for the absolute thickness vs span for the 35 m blade
def thickness(r):
    """Absolute thickness [m] as a function of blade span [m]"""
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

# Solving for the relative thickness (t/c)
# Computing absolute thickness
t = thickness(r)
breakpoint()

def solve_CP(cl_des, r, t, tsr, R, a, B):
# Solving for t/c
    tc_ideal = solve_tc(cl_des, r, t, tsr, R, a, B)
    # Getting ideal aero cl (before changing chord)
    cl_ideal = cl_des(tc_ideal)  # [-]

    # Chord [m]
    chord_ideal = chord_fun(r, tsr, R, a, B, cl_ideal) # calculating ideal chord
    chord = root_chord(r, chord_ideal, chord_root, chord_max) # transition from ideal to root chord
    chord = min_tc_chord(chord, t) # maintain minimum t/c at the tip

    # Updating t/c and polar design values
    tc = t/chord*100
    cl = cl_des(tc)  # [-]
    cd = cd_des(tc) # [-]
    aoa_ideal = aoa_des(tc) # [deg]

    # Twist [deg]
    twist_ideal = twist_deg_fun(r, tsr, R, a, aoa_ideal) # [deg]
    twist = max_twist(twist_ideal, 20) # Limiting the twist angle at 20 degrees

    # Updating aoa
    aoa = twist_deg_fun(r, tsr, R, a, 0)-twist # Updating the design aoa for the constraint twist

    # Updating a
    a = solve_bem(r, tsr, R, chord, cl, B)
    CLT = CLT_fun(r, tsr, R, a, B, cl, cd, chord)
    CLP = CLP_fun(r, tsr, R, a, B, cl, cd, chord)
    CT = CT_fun(r, R, CLT)
    CP = CP_fun(r, R, CLP)
    return CT, CP, chord, tc, cl, cd, twist, aoa

tsr_list = np.linspace(6, 9, 40)
CP_list = np.zeros(len(tsr_list))
CT_list = np.zeros(len(tsr_list))
for i, tsr in enumerate(tsr_list):
    CT, CP, chord, tc, cl, cd, twist, aoa = solve_CP(cl_des, r, t, tsr, R, a, B)
    CP_list[i] = CP
    CT_list[i] = CT
    print(i)

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
# axs[0].plot(r, tc_ideal, "C0--", lw=1)
# axs[0].plot(r, tc, "C0")

# axs[0].set_ylabel('Rel. thickness [%]')
# # Chord
# axs[1].plot(r, chord_ideal, "C0--", lw=1)
# axs[1].plot(r, chord, "C0")
# axs[1].set_ylabel('Chord [m]')
# # Twist
# axs[2].plot(r, twist_ideal, "C0--", lw=1)
# axs[2].plot(r, twist, "C0")
# axs[2].set_ylabel('Twist [deg]')
# axs[2].set_xlabel('Rotor span [m]')
# fig.tight_layout()
# fig.show()

# # %% Plot r vs. t/c, cl, cd, aoa
# fig, ax = plt.subplots(2, 2, num=4, clear=True)
# # t/c
# ax[0, 0].plot(r, tc_ideal, "C0--", lw=1)
# ax[0, 0].plot(r, tc, "C0")
# ax[0, 0].set_ylabel("t/c [%]")
# # cl
# ax[0, 1].plot(r, cl_ideal, "C0--", lw=1)
# ax[0, 1].plot(r, cl)
# ax[0, 1].set_ylabel("$C_l$ [-]")
# # cl/cd
# ax[1, 0].plot(r, cd)
# ax[1, 0].set_ylabel("$C_d$ [-]")
# ax[1, 0].set_xlabel("Span [m]")
# # aoa
# ax[1, 1].plot(r, aoa)
# ax[1, 1].set_ylabel(r"$\alpha$ [deg]")
# ax[1, 1].set_xlabel("Span [m]")

# # %% Plot r vs. CLT, CLP
# fig, axs = plt.subplots(3, 1, num=3, clear=True)
# axs[0].plot(r, CLT)
# axs[0].axhline(y=8/9, ls="--", color="k", lw=1)
# axs[0].grid('on')
# axs[0].set_ylabel('Local thrust ($C_{LT}$) [-]')
# axs[0].set_ylim(0, 1.0)
# axs[1].plot(r, CLP)
# axs[1].axhline(y=16/27, ls="--", color="k", lw=1)
# axs[1].grid('on')
# axs[1].set_ylabel('Local Power ($C_{LP}$) [-]')
# axs[2].plot(r, a)
# axs[2].axhline(y=1/3, ls="--", color="k", lw=1)
# axs[2].grid('on')
# axs[2].set_ylabel('Axial induction ($a$) [-]')
# axs[2].set_xlabel('Rotor span [m]')
# fig.suptitle(f"$C_T$={CT:1.3f}, $C_P$={CP:1.3f}")
# fig.tight_layout()
# fig.show()


#%% TSR vs CP

CP_max = np.argmax(CP_list)
tsr_max = tsr_list[CP_max]
breakpoint()

fig, ax1 = plt.subplots(figsize=(5,2.5))
print(tsr_list)
ax2 = ax1.twinx()
ax1.plot(tsr_list, CP_list, "b--", label = "CP")
ax2.plot(tsr_list, CT_list, "r-.", label = "CT")
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
plt.show(block = True)


CT, CP, chord, tc, cl, cd, twist, aoa = solve_CP(cl_des, r, t, tsr_max, R, a, B)

df_new = pd.DataFrame({"CT" : CT, "CP" : CP, "chord" : chord, "tc" : tc, "cl" : cl, "cd" : cd, "twist" : twist, "aoa" : aoa})
df_new.to_json("design_parameters_at_max_cp.json")
