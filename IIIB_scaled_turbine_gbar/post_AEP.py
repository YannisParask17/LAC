from lacbox.io import ReadHAWC2

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import weibull_min

def load_hawc2s(path):
    """load channels from a pwr or opt file"""
    pwr = True if path.endswith('.pwr') else False
    data = np.loadtxt(path, skiprows=1)
    if pwr:
        u = data[:, 0]  # wind speed [m/s]
        paero = data[:, 1] * 1e3  # aerodynamic power [W]
        thrust = data[:, 2] * 1e3  # thrust [N]
        pitch = data[:, 8]  # pitch [deg]
        rotspd = data[:, 9] * np.pi/30  # rotational speed [rad/s]
        aerotrq = paero / rotspd  # aerodynamic torque [Nm]
    else:
        u = data[:, 0]  # wind speed [m/s]
        pitch = data[:, 1]  # pitch [deg]
        rotspd = data[:, 2] * np.pi/30  # rotational speed [rad/s]
        paero = data[:, 3] * 1e3  # aerodynamic power [W]
        thrust = data[:, 4] * 1e3  # thrust [N]
        aerotrq = paero / rotspd  # aerodynamic torque [Nm]
    return u, pitch, rotspd, paero, thrust, aerotrq

#Mean hub wind speed and turbulence intensity
U_mean = 7.5
TI = 0.14 

# Weibull distribution
C = (2/np.sqrt(np.pi))*U_mean
k = 2 # We can use this value as default

print(f"C = {C}")
print(f"k = {k}")

hawc2s_path = r"data/IIIB_scaled_turbine_flex.opt" # path to .pwr or .opt file

U, _, _, P_aero, _, _ = load_hawc2s(hawc2s_path)

prob_U = weibull_min.pdf(U, k, scale = C)

# Mean power production
P_mean =  np.trapz(P_aero*prob_U, U)
# Anual energy production
AEP = P_mean*365*24

# Capacity factor
cp = AEP/(10E6*365*24)
print("AEP: ", AEP, "CP: ", cp)


AEP_list = []
for i in np.arange(4, 25):
    U_new = np.linspace(i, i+1, 10)
    P_aero_new = np.interp(U_new, U, P_aero)
    prob_U_ew = weibull_min.pdf(U_new, k, scale = C)
    P_mean_new =  np.trapz(P_aero_new*prob_U_ew, U_new)
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


U_new = np.linspace(4, 25, 100)
P_aero_new = np.interp(U_new, U, P_aero)
prob_U_ew = weibull_min.pdf(U_new, k, scale = C)
# Weibull distribution plot
fig, ax = plt.subplots(figsize = (10, 4))
ax.plot(U_new, prob_U_ew)
ax.set(xlabel = "Wind Speed [m/s]",
       ylabel = "p [-]")
# ax.text(0.8, 0.9, , transform = ax.transAxes)
plt.grid()
fig.suptitle(f"Weibull Distribution (C: {C:.1f}, k: {k:.1f})")
plt.savefig("Weibull.pdf")
plt.show()
# plt.show()
