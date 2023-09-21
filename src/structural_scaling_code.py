# %%
import numpy as np
import matplotlib.pyplot as plt
from lacbox.io import load_st, save_st, load_ae
from structural_scaling import EIx, EIy, GK, md

# %%
# blade st data
path_st_file_DTU10MW = "../dtu_10mw/data/DTU_10MW_RWT_Blade_st.dat"
st_data_DTU10MW = load_st(path_st_file_DTU10MW, 0, 0)
st_data = load_st(path_st_file_DTU10MW, 0, 0) # Loading st_data to overwrite

# Design chord
ae_path = '../dtu_10mw/data/DTU_10MW_RWT_ae.dat'
r_RWT, c_RWT, tc_RWT, pcset_RWT = load_ae(ae_path, unpack=True)


# Load structural data
s0, t_skin0, t_blade0, w_cap0, chord0, t_cap0 = np.loadtxt("structural_parameters_DTU10MW.dat", unpack=True)

# We interpolate to have the same number of points
c_RWT = np.interp(s0, r_RWT, c_RWT)
# %%
# Dummy scaled chord and thickness (assuming S_R=R1/R0=1.05 -> c1=S_R*c0, t_blade1=S_R*t_blade0)
# !! Use your own values !!
S_radius = 92.5 / 89.15     #1.037  # Scaling factor
# chord1 = S_radius*chord0
chord1 = c_RWT
t_blade1 = S_radius*t_blade0

# Scaling factors
S_chord = chord1/chord0
S_thickness = t_blade1/t_blade0
rho_DTU10MW = st_data_DTU10MW["m"]/st_data_DTU10MW["A"]

# Scaling ST-data
st_data["s"] *= S_radius
st_data["m"] = md(t_skin0, chord1, t_blade1, w_cap0, t_cap0)
st_data["x_cg"] *= S_chord
st_data["y_cg"] *= S_thickness
st_data["ri_x"] *= S_chord
st_data["ri_y"] *= S_thickness
st_data["x_sh"] *= S_chord
st_data["y_sh"] *= S_thickness
# Not changing E
# Not changing G
st_data["I_x"] = EIx(t_skin0, chord1, t_blade1, w_cap0, t_cap0)/st_data_DTU10MW["E"]
st_data["I_y"] = EIy(t_skin0, chord1, t_blade1, w_cap0, t_cap0)/st_data_DTU10MW["E"]
st_data["I_p"] = GK(t_skin0, chord1, t_blade1, w_cap0, t_cap0)/st_data_DTU10MW["G"]
# Not changing k_x
# Not changing k_y
st_data["A"] = md(t_skin0, chord1, t_blade1, w_cap0, t_cap0)/rho_DTU10MW
# Not changing pitch
st_data["x_e"] *= S_chord
st_data["y_e"] *= S_thickness

# Saving scaled ST-file
# Uncomment to save the new ST-file
save_st("../dtu_10mw_redesign/data/dtu_10mw_redesign_st.dat", st_data)
save_st("../results/hawc_files/dtu_10mw_redesign_st.dat", st_data)

# Plotting m, I_x, I_y, I_p, S_chord, S_thickness
fig, axs = plt.subplots(3, 2, figsize=(7, 6))
# m_d
ax = axs[0, 0]
ax.plot(st_data["s"], st_data["m"], label="scaled")
ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["m"], label="DTU 10MW")
ax.set_ylabel("$m_d$ [kg/m]")
ax.grid()
# I_p
ax = axs[0, 1]
ax.plot(st_data["s"], st_data["I_p"], label="scaled")
ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["I_p"], label="DTU 10MW")
ax.set_ylabel("$I_p$ [m$^4$]")
ax.grid()
# I_x
ax = axs[1, 0]
ax.plot(st_data["s"], st_data["I_x"], label="scaled")
ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["I_x"], label="DTU 10MW")
ax.set_ylabel("$I_x$ [m$^4$]")
ax.grid()
ax.legend()
# I_y
ax = axs[1, 1]
ax.plot(st_data["s"], st_data["I_y"], label="scaled")
ax.plot(st_data_DTU10MW["s"], st_data_DTU10MW["I_y"], label="DTU 10MW")
ax.set_ylabel("$I_y$ [m$^4$]")
ax.grid()
# S_chord
ax = axs[2, 0]
ax.plot(st_data["s"], S_chord, label="scaled")
ax.set_ylabel("$S_{chord}$ [-]")
ax.set_xlabel("Blade length [m]")
ax.grid()
# S_thickness
ax = axs[2, 1]
ax.plot(st_data["s"], S_thickness, label="scaled")
ax.set_ylabel("$S_{thickness}$ [-]")
ax.set_xlabel("Blade length [m]")
ax.grid()

fig.tight_layout()
plt.show()


# %%
