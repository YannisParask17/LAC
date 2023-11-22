#%%
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lacbox.io import ReadHAWC2
from scipy.stats import weibull_min

HOURS_IN_A_YEAR = 8760

# define the channels and names to plot
channels = {111: 'Electrical power [W]'}
power_channel = 111
wind_channel = 15

#%%
# Loading data
debug_10mw = False

res_path = r"postprocess_hawc2\turbulent\iiib_scaled_turbine_turb_tcb.hdf5"
if debug_10mw:
    res_path = r"postprocess_hawc2\turbulent\dtu_10mw_turb_stats.hdf5"


stats_df = pd.read_hdf(res_path, 'stats_df')
if debug_10mw: stats_df = stats_df[stats_df.subfolder=='tcb']

power = stats_df.loc[stats_df.ichan == power_channel, 'mean'].to_numpy()
ws_arr = stats_df.loc[stats_df.ichan == wind_channel, 'mean'].to_numpy()
ws_arr = ws_arr.round()
# We order them
ws_idx_order = np.argsort(ws_arr)
power = power[ws_idx_order]
ws_arr = ws_arr[ws_idx_order]
uniq_ws, num_seeds_ws = np.unique(ws_arr,return_counts=True)

#%%
#Mean hub wind speed and turbulence intensity
# Class IA
# U_mean = 10
# TI = 0.16
# Class IIIB
U_mean = 7.5
TI = 0.14 

# Weibull distribution
C = (2/np.sqrt(np.pi))*U_mean
k = 2 # We can use this value as default

# For each wind speed bin calculate probability
ws_bins = np.zeros(len(uniq_ws)+1)
ws_bins[:-1] = uniq_ws - 0.5
ws_bins[-1] = uniq_ws[-1] + 0.5
weib_cdf = weibull_min.cdf(ws_bins, k, scale = C)
prob_U = weib_cdf[1:] - weib_cdf[:-1]



print(f"ws_bins = {ws_bins}")
print(f"{prob_U}")
#%%

# Mean power production
prob_all = np.repeat(prob_U, num_seeds_ws)
mean_power = np.zeros(len(uniq_ws))
for idx, ws in enumerate(uniq_ws):
    mean_power[idx]=  power[np.isclose(ws_arr, ws, atol=1e-2)].mean()
# %%
# Comparison

mean_power_real = np.array([ 0.95938967,  1.75168289,  2.54685342,  3.78603814,  5.25633765,  7.34238965,
  8.72473284,  9.75989313,  9.92772521, 10.00003879, 10.00007033, 10.0000928,
 10.00007717, 10.00009396, 10.00010863, 10.00015959, 10.00014411, 10.00023013,
 10.00021951, 10.00025728])*1e6

diff_mean_power = (mean_power_real-mean_power)/mean_power_real*100
print(f"Percentage error of power for each WS bin:\n {diff_mean_power}")
# GOOD

prob_U_real = [0.09822154, 0.10112075, 0.09843279, 0.09128194, 0.08103839, 0.06910383,
 0.05673472, 0.04492539, 0.03435648, 0.02540085, 0.01817049, 0.01258493,
 0.00844375, 0.00549053, 0.0034614,  0.00211633, 0.00125524, 0.00072242,
 0.0004035,  0.00021877]

diff_prob = (prob_U_real-prob_U)/prob_U_real*100
print(f"Percentage error of probability for each WS bin:\n {diff_prob}")
#GOOD
# %%

P_mean =  np.sum(mean_power*prob_U)
# Anual energy production
AEP = P_mean*HOURS_IN_A_YEAR
# %%

# Capacity factor
cp = AEP/(10E6*HOURS_IN_A_YEAR)
print("AEP: ", AEP, "CP: ", cp)

AEP_list = []
for i in np.arange(4, 25):
    U_new = np.linspace(i, i+1, 10)
    P_aero_new = np.interp(U_new, ws_arr, power)
    prob_U_new = weibull_min.pdf(U_new, k, scale = C)
    P_mean_new =  np.trapz(P_aero_new*prob_U_new, U_new)
    AEP_list.append(P_mean_new*365*24)

U_new = np.arange(4.5, 25.5, 1)
fig, ax = plt.subplots(figsize = (10, 4))
ax.bar(U_new, np.array(AEP_list)*1e-9)
ax.set(xlabel = "Wind Speed [m/s]",
       ylabel = "AEP [GWh]")
ax.text(0.8, 0.9, f"Total AEP: {AEP*1e-9:.1f} GWh", transform = ax.transAxes)
plt.grid()
plt.tight_layout()
plt.savefig("AEP_per_wind_speed.pdf")
plt.show()


# %%
U_new = np.linspace(4, 25, 100)
P_aero_new = np.interp(U_new, ws_arr, power)
prob_U_new = weibull_min.pdf(U_new, k, scale = C)

fig, ax = plt.subplots(figsize = (10, 4))
ax.plot(U_new, prob_U_new)
ax.set(xlabel = "Wind Speed [m/s]",
       ylabel = "p [-]")
# ax.text(0.8, 0.9, , transform = ax.transAxes)
plt.grid()
fig.suptitle(f"Weibull Distribution (C: {C:.1f}, k: {k:.1f})")
plt.savefig("Weibull.pdf")
plt.show()
# %%

print(prob_U)
print(AEP)
print(mean_power)