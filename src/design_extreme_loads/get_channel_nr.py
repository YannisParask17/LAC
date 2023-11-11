# Script to look at the channel numbers

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from lacbox.io import ReadHAWC2
from rich import print
import pandas as pd
fname = "/home/mi/repos/LAC/IIIB_scaled_turbine_gbar/res_steady/notilt/dtu_10mw_steady_notilt_05.0.hdf5"

h2res = ReadHAWC2(fname)
print(h2res.__dict__.keys())  #
names, units, desc = h2res.chaninfo
print(names[118])  # But that is channel 119 due to the indexing !
print(desc[118])  # But that is channel 119 due to the indexing !
df = pd.DataFrame(h2res.data)
deflection = df[118]
deflection = deflection[df[0]>200]

mean = deflection.mean()
max = deflection.max()
min = deflection.min()
std = deflection.std()

print(f"Mean: {mean}")
print(f"Max: {max}")
print(f"Min: {min}")
print(f"Std: {std}")
