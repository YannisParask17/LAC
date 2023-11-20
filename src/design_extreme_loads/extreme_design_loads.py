# %%
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


def get_designloads(HAWC2val_dtu10mw):

    max_abs = np.max(np.abs(HAWC2val_dtu10mw), axis=1)
    max_abs_stacked = max_abs.reshape(len(max_abs) // 6,6)
    average_max_abs_stacked = np.mean(max_abs_stacked, axis=1) 

    return np.max(average_max_abs_stacked)



stats_path = '../../IIIB_scaled_turbine_gbar/postprocess_hawc2/turbulent/iiib_scaled_turbine_turb_tcb.hdf5'  # path to mean steady stats
subfolder = '.'  # which subfolder to plot: tilt, notilt, notiltrigid, notiltnodragrigid

subfolder_dtu10mw = 'tca'  # which subfolder to plot: tilt, notilt, notiltrigid, notiltnodragrigid
stats_path_dtu10mw = '../../IIIB_scaled_turbine_gbar/postprocess_hawc2/turbulent/dtu_10mw_turb_stats.hdf5'  # path to mean steady stats
save_path = '' 


# load the HAWC2 data from the stats file -> IIIB Redesign
stats_df = pd.read_hdf(stats_path, 'stats_df')
df = stats_df[stats_df.subfolder == subfolder]

# load the HAWC2 data from the stats file -> DTU10MW
stats_df_dtu10mw = pd.read_hdf(stats_path_dtu10mw, 'stats_df')
df_dtu10mw = stats_df_dtu10mw[stats_df_dtu10mw.subfolder == subfolder_dtu10mw]

# %%

channels = {19: 'Tower-base FA [kNm]',
            20: 'Tower-base SS [kNm]',
            22: 'Yaw-bearing tilt [kNm]',
            23: 'Yaw-bearing roll [kNm]',
            27: 'Shaft torsion [kNm]',
            28: 'Out-of-plane BRM [kNm]',
            29: 'In-plane BRM [kNm]',
            119: 'Tower clearance [m]'}
i_wind = 15  # wind channel, needed for plotting versus wind speed

# %%

# initialise lists for design loads
desload_redesign = []
desload_dtu10mw = []


# loop over each channels and plot the steady state with the theory line
for iplot, (ichan, name) in enumerate(channels.items()):
    
    # isolate OoP BRM
    # ichan = 119

    # extract hawc2 wind and channel to plot from the HAWC2 stats -> IIIB Redesign
    h2_wind = df.loc[df.ichan == i_wind, 'mean']
    HAWC2val = df.loc[df.ichan == ichan, ['max', 'min']]

    # extract hawc2 wind and channel to plot from the HAWC2 stats -> DTU 10MW
    h2_wind_dtu10mw = df_dtu10mw.loc[df_dtu10mw.ichan == i_wind, 'mean']
    HAWC2val_dtu10mw = df_dtu10mw.loc[df_dtu10mw.ichan == ichan, ['max', 'min']]

    # sort by increasing wind speed (convert to numpy arrays first)
    h2_wind = np.array(h2_wind)
    h2_wind, HAWC2val = np.round(np.array(h2_wind)), np.array(HAWC2val)
    h2_wind_dtu10mw, HAWC2val_dtu10mw = np.round(np.array(h2_wind_dtu10mw)), np.array(HAWC2val_dtu10mw)
    i_h2 = np.argsort(h2_wind)
    i_h2_dtu10mw = np.argsort(h2_wind_dtu10mw)

    # sorted hawc2 channels by increasing wind speed 
    HAWC2val = HAWC2val[i_h2]
    HAWC2val_dtu10mw = HAWC2val_dtu10mw[i_h2_dtu10mw] 

    # extract maximum load
    max_abs = np.max(np.abs(HAWC2val_dtu10mw), axis=1)
    max_abs_stacked = max_abs.reshape(len(max_abs) // 6,6)
    average_max_abs_stacked = np.mean(max_abs_stacked, axis=1) 

    maximum_load = get_designloads(HAWC2val)
    maximum_load_dtu10mw = get_designloads(HAWC2val_dtu10mw)

    # for tower clearance -> only the minimum of the minimum values is considered
    if ichan == 119:
        design_load = np.min(HAWC2val[:,1])
        design_load_dtu10mw = np.min(HAWC2val_dtu10mw[:,1])

    else:
        # compute characteristic and design load
        charact_load = 1.35 * maximum_load
        design_load = 1.25 * charact_load

        charact_load_dtu10mw =  1.35 * maximum_load_dtu10mw
        design_load_dtu10mw = 1.25 * charact_load_dtu10mw

    # store values
    desload_redesign.append(design_load)
    desload_dtu10mw.append(design_load_dtu10mw)


desload_redesign, desload_dtu10mw = np.array(desload_redesign), np.array(desload_dtu10mw)

labels = ['TbFA', 
          'TbSS', 
          'YbPitch', 
          'YbRoll', 
          'ShftTrs', 
          'OoPBRM', 
          'IPBRM', 
          'TC']
# print(labels)

print("=============DESIGN LOADS - REDESIGN IIIB==============")
for i, lab in enumerate(labels):
    print(f'{lab} : {round(desload_redesign[i], 2)} kNm')

print("=============DESIGN LOADS - DTU10MW IA==============")
for i, lab in enumerate(labels):
    print(f'{lab} : {round(desload_dtu10mw[i] ,2)} kNm')

print("=============RELATIVE INCREASE==============")
for i, lab in enumerate(labels):
    print(f'{lab} : {(desload_redesign[i] - desload_dtu10mw[i] ) / desload_dtu10mw[i] * 100} %')

# %%


# compare design loads between DTU10MW IA and redesign IIIB
fig, ax = plt.subplots(1, figsize=(8,4))
barWidth = .25
br1 = np.arange(len(desload_redesign)) 
br2 = [x + barWidth for x in br1] 

ax.bar(br1, np.divide(desload_redesign, desload_dtu10mw), color ='r', width = barWidth, 
        edgecolor ='grey', label ='Redesign IIIB') 
ax.bar(br2, np.divide(desload_dtu10mw, desload_dtu10mw), color ='g', width = barWidth, 
        edgecolor ='grey', label ='DTU10MW IA') 
ax.set_xticks([r + barWidth for r in range(len(br1))], 
        labels)
ax.set_ylabel('Normalised extreme design loads')
ax.legend()
fig.savefig("task5_evaluation_extreme.pdf")
plt.show() 