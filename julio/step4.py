
# %%
from lacbox.io import load_c2def, save_c2def
import matplotlib.pyplot as plt
import numpy as np

# %%
htc_path = 'C:/Users/julio/OneDrive/Documents/ICAI/DTU/_Loads_aerodynamics_and_control/assignment_1/dtu_10mw/dtu_10mw_hawc2s_redesign1.htc'

c2_def = load_c2def(htc_path)


# %%
c2_def_new = c2_def.copy()

R_1 = 89.14
R_2 = 92.49
r_hub = 2.8

sf = (R_1 - r_hub)/(R_2- r_hub)

c2_def_new[:, 2] *= sf

save_path = 'dtu_10mw_hawc2s_redesign1.txt'

save_c2def(save_path, c2_def_new)
# %%

fig, ax = plt.subplots(1, figsize=(9, 3.5))

ax.plot(c2_def[:, 2], c2_def[:, 3], label='Old')
ax.plot(c2_def_new[:, 2], c2_def_new[:, 3], label='New')

ax.set(xlabel='Blade span', ylabel='Twist [deg]')
ax.legend()

fig.tight_layout()
# %%
