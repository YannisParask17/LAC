import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

file_path = "./hawc2s_files/IIIB_scaled_turbine_flex_C5_omega_001_zeta07_ctrl_tuning.txt"

results = np.loadtxt(file_path, skiprows=17)
# Define the function you want to fit
def Q(theta, Q0, K1, K2):
    return Q0 * (1 + theta / K1 + theta**2 / K2)

# Your known data points for Q and T
theta = results[:,0]  # Replace with your actual T values
dQA_dtheta = results[:,1]  # Replace with your actual Q values

# Use curve_fit to fit the data
init_K1 = 1
init_K2 = 1
Q0 = results[0,1]

initial_guess = [init_K1, init_K2]  # Provide initial guesses for K1 and K2
params, covariance = curve_fit(lambda theta, K1, K2: Q(theta, Q0, K1, K2), theta, dQA_dtheta, p0=initial_guess)

# Extract the fitted parameters
fitted_K1, fitted_K2 = params

rms = np.sqrt(np.mean((dQA_dtheta - Q(theta, Q0, fitted_K1, fitted_K2))**2))


print(f"K1:{fitted_K1}\nK2:{fitted_K2}")
# Print the fitted values
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(theta, dQA_dtheta, "rx", label="HAWC2S Results")
ax.plot(theta, Q(theta, Q0, fitted_K1, fitted_K2), "b-", label="Curve Fitting (Least Squares)")
ax.text(0.02, 0.02, f'RMS = {rms:.2f}', fontsize=12, transform=ax.transAxes)
ax.set_xlabel("Pitch Angle [deg]")
ax.set_ylabel("Aerodynamic Torque Gain [kNm/deg]")
plt.grid()
plt.legend()
plt.tight_layout()
plt.show()
