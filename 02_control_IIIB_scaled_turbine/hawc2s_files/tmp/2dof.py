import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

def second_order_system(y, t, omega, zeta):
    dydt = [y[1], -2 * zeta * omega * y[1] - omega**2 * y[0]]
    return dydt

# Time vector
t = np.linspace(0, 100, 1000)

# Different values of stiffness (omega) and damping ratio (zeta)
omegas = [0.05, 0.055, 0.625]  # You can add more values
zetas = [0.7, 0.7]  # You can add more values

# Plotting
plt.figure(figsize=(10, 6))

for omega in omegas:
    for zeta in zetas:
        # System parameters
        y0 = [1.0, 0.0]  # initial displacement and velocity

        # Solve the differential equation
        sol = odeint(second_order_system, y0, t, args=(omega, zeta))

        # Plot the displacement over time
        label = f'Omega={omega/(2*np.pi)}, Zeta={zeta}'
        plt.plot(t, sol[:, 0], label=label)

plt.xlabel('Time')
plt.ylabel('Displacement')
plt.title('Second Order System Response for Different Stiffness and Damping')
plt.legend()
plt.grid(True)
plt.show()

