# %%
import numpy as np

#%%
TSR = np.linspace(7,8,13)
R = 92.5
V_0 = 8
RPM = TSR*V_0/R*30/np.pi

for rpm in RPM:
    print(rpm)
# %%
