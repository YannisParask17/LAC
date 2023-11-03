# Script to postprocess design extreme loads
# 
#
#
import pandas as pd
import os
from rich import print




# ----------------------
# Paths
# ----------------------

loads_path = "../../dtu_10mw/dtu_10mw_steady_stats.hdf5"
subfolder = "notilt"  # Subfolder to look at. could be tilt or notilt (e.g)
fname_str = "dtu_10mw_steady_notilt_"  # strng to remove to get wind speeds. Needs to be adapted for each row of files

stats_df = pd.read_hdf(loads_path)
df = stats_df[stats_df.subfolder ==subfolder]

#print(df.)
# Make sure the wind speed is the same as wanted


# Find max of all max, min of all min


# Multiply by safety factor


#safety_factor
# Tower base fore-aft;              19
# Tower base side-side;             20
# Yaw bearing tilt;                 22
# Yaw bearing roll;                 23
# Shaft torsion;                    27
# Out-of-plane blade root moment1;  120
# In-plane blade root moment1;      121
# Tip deflection.r = 1.35 * 1.25
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



df[df.ichan==19]
df["U"] = df.filename.str.replace(fname_str, "").str.replace(".hdf5", '').astype(float)
plt.scatter()
breakpoint()


