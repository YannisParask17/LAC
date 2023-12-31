#%%
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from lacbox.io import ReadHAWC2

# define the channels and names to plot
channels = {19: 'DEL Tower-base FA [kNm]',
            20: 'DEL Tower-base SS [kNm]',
            22: 'DEL Yaw-bearing tilt [kNm]',
            23: 'DEL Yaw-bearing roll [kNm]',
            27: 'DEL Shaft torsion [kNm]',
            120: 'DEL Out-of-plane BRM [kNm]',
            121: 'DEL In-plane BRM [kNm]'}

wind_channel = 15

index_steel = list(channels.keys())[:-2]
index_comp = list(channels.keys())[-2:]

# %%
# Loading data

res_path= r"postprocess_hawc2\turbulent\iiib_scaled_turbine_turb_tcb.hdf5"
stats_df = pd.read_hdf(res_path, 'stats_df')
# %%
# The DELs are in del3, del4, del5...

del4_df = stats_df[['filename', 'ichan','del4']][stats_df.ichan.isin(index_steel)]
print(del4_df)
del10_df = stats_df[['filename', 'ichan','del10']][stats_df.ichan.isin(index_comp)]


# %%

res_path_lst = [
                r"postprocess_hawc2\turbulent\iiib_scaled_turbine_turb_tcb.hdf5",
                r"postprocess_hawc2\turbulent\dtu_10mw_turb_stats.hdf5"
                ]

legend_lst = ["Redesign 3B", "DTU 10 MW 1A"]

# initialize the figure and axes
scale = 1.3
fig, axs = plt.subplots(len(channels), figsize=(8.5*scale, 11*scale), sharex = True, clear=True)

for file_i, res_path in enumerate(res_path_lst):
    stats_df = pd.read_hdf(res_path, 'stats_df')

    # loop over each channels
    for iplot, (ichan, name) in enumerate(channels.items()):
        wind = stats_df.loc[stats_df.ichan == wind_channel, 'mean']
        val = stats_df.loc[stats_df.ichan == ichan, ['del4','del10']]

        if file_i==0:
            marker, color = 'o', 'r'
        else:
            marker, color = 'x', 'k'

        # plot the results
        ax = axs.flatten()[iplot]
        if iplot >= len(channels)-2:
            ax.scatter(wind,val.del10, marker = marker, color = color, label = legend_lst[file_i])
        else:
            ax.scatter(wind,val.del4, marker = marker, color = color, label = legend_lst[file_i])
        ax.grid('on')
        ax.set(ylabel=name, xlim=[4, 25])

# Add legend
for ax in axs:
    ax.legend(loc='upper left')
plt.xlabel('Wind speed [m/s]')
fig.tight_layout()
plt.show()

# %%

for iplot, (ichan, name) in enumerate(channels.items()):
    wind = stats_df.loc[stats_df.ichan == wind_channel, 'mean']
    del4_val = stats_df.loc[stats_df.ichan == ichan, 'del4']


# %%
