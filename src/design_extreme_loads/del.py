# Script to postprocess design extreme loads
# Noveber '23
# M Janssen

import pandas as pd
import matplotlib.pyplot as plt
import os
from rich import print


# ----------------------
# Paths
# ----------------------

loads_path = "../../dtu_10mw/dtu_10mw_steady_stats.hdf5"
subfolder = "notilt"  # Subfolder to look at. could be tilt or notilt (e.g)
fname_str = "dtu_10mw_steady_notilt_"  # strng to remove to get wind speeds. Needs to be adapted for each row of files
safety_factor = 1.35 * 1.25

stats_df = pd.read_hdf(loads_path)
df = stats_df[stats_df.subfolder ==subfolder].copy()

# Multiply by safety factor


#safety_factor
# Tower base fore-aft;              19
# Tower base side-side;             20
# Yaw bearing tilt;                 22
# Yaw bearing roll;                 23
# Shaft torsion;                    27
# Out-of-plane blade root moment1;  120
# In-plane blade root moment1;      121
# Tip deflection.
#r = 1.35 * 1.25
channels = {4: 'Pitch angle [deg]',
            10: 'Rotor speed [rad/s]',
            13: 'Thrust [kN]',
            81: 'Generator torque [Nm]',
            111: 'Electrical power [W]',
            
            19: 'Tower-base FA [kNm]',
            20: 'Tower-base SS [kNm]',
            22: 'Yaw-bearing tilt [kNm]',
            23: 'Yaw-bearing roll [kNm]',
            27: 'Shaft torsion [kNm]',
            120: 'Out-of-plane BRM [kNm]',
            121: 'In-plane BRM [kNm]'}

channel_id = [19,
              20,
              22,
              23,
              27,
              120,
              121,
              ]


#df[df.ichan==19]
df["U"] = df.filename.str.replace(fname_str, "").str.replace(".hdf5", '').astype(float)  # Extract velocity from filename
channel = 19

fig, axs = plt.subplots(3, 1)
for i, channel in enumerate([19, 20]):
    mean_scaled = df[df.ichan==channel]['mean'] * safety_factor
    min_scaled = df[df.ichan==channel]['min'] * safety_factor
    max_scaled = df[df.ichan==channel]['max'] * safety_factor

    axs[i].scatter(df[df.ichan==channel]['U'], mean_scaled, label='mean')
    axs[i].scatter(df[df.ichan==channel]['U'], min_scaled, label='min')
    axs[i].scatter(df[df.ichan==channel]['U'], max_scaled, label='max')
    axs[i].legend()
    axs[i].grid()
    axs[i].set_title(channels[channel])
plt.show()


