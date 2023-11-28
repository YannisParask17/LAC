# %%
# This fixes from the original code (one used in the report, not present in the repo):
# - Not using the real S_thickness (the original sims to have used the S_chord)
# - Using the blade span and not the rotor radius

# NOTE: we used in our a report a better version of the code we have here.
# That version had S_chord more less correct. The rest of things were as bad.

# %%
import numpy as np
import matplotlib.pyplot as plt
from lacbox.io import load_st, save_st, load_ae
from scripts.structural_scaling import EIx, EIy, GK, md

# %%

# Output
st_path = "../results/dtu_10mw_redesign_st_JULIO.dat"
st_figure_path = '../results/st_comparison_JULIO.pdf'

# blade st data
path_st_file_DTU10MW = "../dtu_10mw/data/DTU_10MW_RWT_Blade_st.dat"
path_struct_params_10mw = "../data/structural_parameters_DTU10MW.dat"
st_data_DTU10MW = load_st(path_st_file_DTU10MW, 0, 0)
st_data = st_data_DTU10MW.copy()
st_data1 = st_data_DTU10MW.copy()
# st_data = load_st(path_st_file_DTU10MW, 0, 0)       # Loading st_data to overwrite

# Design chord
ae_path = '../dtu_10mw/data/DTU_10MW_RWT_ae.dat'
r_RWT, c_RWT, tc_RWT, pcset_RWT = load_ae(ae_path, unpack=True)

ae_path_redesign = r'..\results\hawc_files\10MW_IIIB_ae_JULIO.dat'
r_for_c_redesign, c_redesign, tc_redesign, _ = load_ae(ae_path_redesign, unpack=True)
t_redesign = c_redesign*tc_redesign/100

ae_path_redesign1 = r'..\results\hawc_files\10MW_IIIB_ae.dat' # Original design
r_for_c_redesign1, c_redesign1, tc_redesign1, _ = load_ae(ae_path_redesign1, unpack=True)
t_redesign1 = c_redesign1*tc_redesign1/100

# Load structural data
# This has the mechanical properties of the different airfoils
s0, t_skin0, t_blade0, w_cap0, chord0, t_cap0 = np.loadtxt(path_struct_params_10mw, unpack=True)

# We interpolate to have the same number of points
c_RWT = np.interp(s0, r_RWT, c_RWT)
c_redesign = np.interp(s0, r_for_c_redesign, c_redesign)
t_redesign = np.interp(s0, r_for_c_redesign, t_redesign)
c_redesign1 = np.interp(s0, r_for_c_redesign1, c_redesign1)
t_redesign1 = np.interp(s0, r_for_c_redesign1, t_redesign1)
# %%
# Dummy scaled chord and thickness (assuming S_R=R1/R0=1.05 -> c1=S_R*c0, t_blade1=S_R*t_blade0)
# !! Use your own values !!
R_hub = 2.8
Span_dtu10mw = 86.366
Span_scaled = st_data["s"][-1]
S_span = Span_scaled/Span_dtu10mw     #1.037  # Scaling factor
chord1 = c_redesign
t_blade1 = t_redesign

# Scaling factors
S_chord = chord1/chord0
S_thickness = t_blade1/t_blade0
rho_DTU10MW = st_data_DTU10MW["m"]/st_data_DTU10MW["A"]

# Scaling ST-data
st_data["s"] *= S_span
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

#%%
R_hub = 2.8
Span_dtu10mw = 86.366
Span_scaled = 92.5-R_hub
S_span = Span_scaled/Span_dtu10mw     #1.037  # Scaling factor
chord1 = c_redesign1
t_blade1 = t_redesign1

# Scaling factors
S_chord = chord1/chord0
S_thickness = t_blade1/t_blade0
rho_DTU10MW = st_data_DTU10MW["m"]/st_data_DTU10MW["A"]

# Scaling ST-data
st_data1["s"] *= S_span
st_data1["m"] = md(t_skin0, chord1, t_blade1, w_cap0, t_cap0)
st_data1["x_cg"] *= S_chord
st_data1["y_cg"] *= S_thickness
st_data1["ri_x"] *= S_chord
st_data1["ri_y"] *= S_thickness
st_data1["x_sh"] *= S_chord
st_data1["y_sh"] *= S_thickness
# Not changing E
# Not changing G
st_data1["I_x"] = EIx(t_skin0, chord1, t_blade1, w_cap0, t_cap0)/st_data_DTU10MW["E"]
st_data1["I_y"] = EIy(t_skin0, chord1, t_blade1, w_cap0, t_cap0)/st_data_DTU10MW["E"]
st_data1["I_p"] = GK(t_skin0, chord1, t_blade1, w_cap0, t_cap0)/st_data_DTU10MW["G"]
# Not changing k_x
# Not changing k_y
st_data1["A"] = md(t_skin0, chord1, t_blade1, w_cap0, t_cap0)/rho_DTU10MW
# Not changing pitch
st_data1["x_e"] *= S_chord
st_data1["y_e"] *= S_thickness

# Saving scaled ST-file
# Uncomment to save the new ST-file
save_st(st_path, st_data)

# Plotting m, I_x, I_y, I_p, S_chord, S_thickness
fig, axs = plt.subplots(3, 2, figsize=(7, 6))
# m_d
ax = axs[0, 0]
ax.plot(st_data["s"]/st_data["s"][-1], st_data["m"], label="scaled")
ax.plot(st_data1["s"]/st_data["s"][-1], st_data1["m"], label="scaled",linestyle='--')
ax.plot(st_data_DTU10MW["s"]/st_data_DTU10MW["s"][-1], st_data_DTU10MW["m"], label="DTU 10MW")
ax.set_ylabel("$m_d$ [kg/m]")
ax.grid()
# I_p
ax = axs[0, 1]
ax.plot(st_data["s"]/st_data["s"][-1], st_data["I_p"], label="scaled")
ax.plot(st_data_DTU10MW["s"]/st_data_DTU10MW["s"][-1], st_data_DTU10MW["I_p"], label="DTU 10MW")
ax.set_ylabel("$I_p$ [m$^4$]")
ax.grid()
# I_x
ax = axs[1, 0]
ax.plot(st_data["s"]/st_data["s"][-1], st_data["I_x"], label="scaled")
ax.plot(st_data_DTU10MW["s"]/st_data_DTU10MW["s"][-1], st_data_DTU10MW["I_x"], label="DTU 10MW")
ax.set_ylabel("$I_x$ [m$^4$]")
ax.grid()
ax.legend()
# I_y
ax = axs[1, 1]
ax.plot(st_data["s"]/st_data["s"][-1], st_data["I_y"], label="scaled")
ax.plot(st_data_DTU10MW["s"]/st_data_DTU10MW["s"][-1], st_data_DTU10MW["I_y"], label="DTU 10MW")
ax.set_ylabel("$I_y$ [m$^4$]")
ax.grid()
# S_chord
ax = axs[2, 0]
ax.plot(st_data["s"]/st_data["s"][-1], S_chord, label="scaled")
ax.set_ylabel("$S_{chord}$ [-]")
ax.set_xlabel("Blade length [m]")
ax.grid()
# S_thickness
ax = axs[2, 1]
ax.plot(st_data["s"]/st_data["s"][-1], S_thickness, label="scaled")
ax.set_ylabel("$S_{thickness}$ [-]")
ax.set_xlabel("Blade length [m]")
ax.grid()

fig.tight_layout()
plt.savefig(st_figure_path)
plt.show()


# %%
# Comparing weight

mass0 = np.trapz( st_data_DTU10MW["m"], st_data_DTU10MW["s"])
mass2 = np.trapz( st_data["m"], st_data["s"])
mass1 = np.trapz( st_data1["m"], st_data1["s"])

max_grav_m1 = np.trapz(st_data_DTU10MW["m"]*9.81*st_data_DTU10MW["s"], st_data_DTU10MW["s"])
max_grav_m2 = np.trapz(st_data["m"]*9.81*st_data["s"], st_data["s"])
max_grav_m1 = np.trapz(st_data1["m"]*9.81*st_data1["s"], st_data1["s"])

print(f"Mass RWT = {mass1} kg \nMass redesign = {mass2} kg")
print(f"M_max RWT = {max_grav_m1} Nm \nM_max redesign = {max_grav_m2} kg")

# %%
