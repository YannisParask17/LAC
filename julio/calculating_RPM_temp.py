# %%
import numpy as np

#%%
TSR = np.linspace(7,10,26)
R = 92.5
V_0 = 8
RPM = TSR*V_0/R*30/np.pi

for rpm in RPM:
    print(rpm)
# %%
# Calculating the new V_rated with P_rated = P(V_rated)
TSR_max = 8
C_p = 0.4712
P_rated = 10E6
rho = 1.225
P_prim = 1/2*rho*C_p*np.pi*R**2
V_rated = (P_rated/P_prim)**(1/3)
print(V_rated)

#%%
#Calculating the omega_max
omega_max = TSR_max*V_rated/R
print(f"{omega_max} rad/s \n{omega_max*30/np.pi} RPM")

#%%
# Tip speed
V_tip = omega_max*R
print(V_tip)
# %%
