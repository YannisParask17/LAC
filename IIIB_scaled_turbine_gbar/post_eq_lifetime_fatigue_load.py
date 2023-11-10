#%%
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lacbox.io import ReadHAWC2
from scipy.stats import weibull_min



#%%

n_T = 20*365*24*60*60 # Number of cycles in a lifetime of a 1 Hz load
n_T = 630720000 # To make sure
n_eq = 1e7 # Number of cycles of equivalent load

#Mean hub wind speed and turbulence intensity
# Class IA
U_mean = 10
TI = 0.16
subfolder='tca' 
# Class IIIB
# U_mean = 7.5
# TI = 0.14 
# subfolder = 'tcb'


# %%
# Loading data

if subfolder=='tca':
    res_path = r"postprocess_hawc2\turbulent\dtu_10mw_turb_stats.hdf5"

    # define the channels and names to plot
    channels = {19: 'DEL Tower-base FA [kNm]',
                20: 'DEL Tower-base SS [kNm]',
                22: 'DEL Yaw-bearing tilt [kNm]',
                23: 'DEL Yaw-bearing roll [kNm]',
                27: 'DEL Shaft torsion [kNm]',
                28: 'DEL Out-of-plane BRM [kNm]',
                29: 'DEL In-plane BRM [kNm]'}
    
elif subfolder=='tcb':
    res_path = r"postprocess_hawc2\turbulent\iiib_scaled_turbine_turb_tcb.hdf5"
    channels = {19: 'DEL Tower-base FA [kNm]',
            20: 'DEL Tower-base SS [kNm]',
            22: 'DEL Yaw-bearing tilt [kNm]',
            23: 'DEL Yaw-bearing roll [kNm]',
            27: 'DEL Shaft torsion [kNm]',
            120: 'DEL Out-of-plane BRM [kNm]',
            121: 'DEL In-plane BRM [kNm]'}

wind_channel = 15

stats_df = pd.read_hdf(res_path, 'stats_df')
stats_df = stats_df[stats_df.subfolder == subfolder]

ws_arr = stats_df.loc[stats_df.ichan == wind_channel, 'mean'].to_numpy()
ws_arr = ws_arr.round()
uniq_ws = np.unique(ws_arr.round())

#%%
#Equivalent load for each wind speed bin. We average them

S_DEL_ws = pd.DataFrame(columns = ['ws', 'ichan', 'del'])
for iplot, (ichan, name) in enumerate(channels.items()):
    if iplot < len(channels)-2:
        m = 4
    else:
        m = 10

    # All the DEL of each simulation for one channel
    S_arr = stats_df.loc[stats_df.ichan == ichan, f'del{m}'].to_numpy()

    for ws in uniq_ws:
        tolerance = 1e-3
        # Masking out the rest of wind speeds
        mask = np.isclose(ws_arr, ws, atol=tolerance)
        m_over_S = S_arr[mask]**m
        S_del_average = (np.mean(m_over_S))**(1/m)
        # Adding the results in a new row
        S_DEL_ws.loc[len(S_DEL_ws.index)] = [ws, ichan, S_del_average]

#%% Debug
# Diff. Tower-base FA
S_DEL_ws_real = [49324.02699912, 56631.4811873,  50234.01868334, 50993.41038225,
 44373.69454597, 43697.00569577, 37484.04714851, 41281.08043197,
 41699.64202409, 38792.80397018, 40949.86810033, 40319.76408666,
 42669.30267881, 42877.00615212, 44632.2680547,  48297.03219026,
 53792.52114493, 52494.36187018, 55461.81641078, 58542.42279516]

diff_S_DEL = (S_DEL_ws['del'][S_DEL_ws.ichan==19] - S_DEL_ws_real)/S_DEL_ws_real*100
print(f"Percentage error of DEL tower-base FA for each WS bin:\n {diff_S_DEL}")

# Diff. Out-of-plane BRM (120)

S_DEL_ws_real = [ 7944.72329887,  9183.96204826, 11579.11146875, 13755.74930197,
 16082.82678328, 17026.12746851, 16998.19203829, 19180.21989099,
 19763.2030041,  18939.21137539, 20059.11256884, 19031.12928522,
 19581.83237752, 20076.26913128, 20509.85822179, 20889.12547177,
 23042.72379119, 24550.08751361, 24124.02236404, 26693.54227915]

diff_S_DEL = (S_DEL_ws['del'][S_DEL_ws.ichan==28] - S_DEL_ws_real)/S_DEL_ws_real*100
print(f"Percentage error of DEL out-of-plane BRM for each WS bin:\n {diff_S_DEL}")
    
# %%
##Wind speed bins probabilities
# Weibull distribution
C = (2/np.sqrt(np.pi))*U_mean
k = 2 # We can use this value as default

# For each wind speed bin calculate probability
ws_bins = np.zeros(len(uniq_ws)+1)
ws_bins[:-1] = uniq_ws - 0.5
ws_bins[-1] = uniq_ws[-1] + 0.5
weib_cdf = weibull_min.cdf(ws_bins, k, scale = C)
prob_U = weib_cdf[1:] - weib_cdf[:-1]
# print(prob_U)

S_life_time = np.zeros(len(channels))
for idx, (ichan, name) in enumerate(channels.items()):
    
    if idx < len(channels)-2:
        m = 4
    else:
        m = 10
        
    print(m, name)

    S = S_DEL_ws.loc[S_DEL_ws.ichan == ichan, 'del'].to_numpy()
    summation = (prob_U*(S**m)).sum()
    S_life_time[idx] = (summation*n_T/n_eq)**(1/m)

#%%
# Debug
S_life_time_real = [125948.5, 56984.70425549112, 33207.45186657704, 4064.6416603915914, 2867.6815812969317,
                    28343.117200575118, 25232.86138408457]

diff_S_lt = ( S_life_time - S_life_time_real)/S_life_time_real*100
print(f'Percentage error of eq. load for a lifetime in % for each channel: \n {diff_S_lt}')


# %% Debug
# SOLVED

prob_U_real = [0.06442809, 0.0709227,  0.07472189, 0.07591763, 0.0747455,  0.07155162,
 0.06675382, 0.06080169, 0.05413969, 0.04717648, 0.04026251, 0.03367663,
 0.02762128, 0.02222493, 0.01755019, 0.01360521, 0.01035688, 0.00774379,
 0.00568809, 0.0041053]

diff_prob_lt = ( prob_U - prob_U_real)/prob_U_real*100
print(f'Percentage error of probabilities in % for each channel: \n {diff_prob_lt}')


plt.figure()
plt.plot(uniq_ws, prob_U, label = 'mine')
plt.plot(uniq_ws, prob_U_real)
plt.legend()

# %%

