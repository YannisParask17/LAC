# get the paraemters for controls


import numpy as np

# Functions



def get_kopt(radius, eta, rho, cp, lambda_opt):
    """
    Get the kopt param in 2
    cp should match the lambda opt
    """
    kopt= (eta * rho * np.pi * radius**5 * cp) / (2 * lambda_opt**3)
    return kopt


def get_kpg(eta, i_r, i_g, n_g, omega, zeta, dqdomega):
    """
    Get the kpg param in 2.5
    """
    kpg = eta * (2 * (i_r + n_g**2 * i_g) * omega * zeta + dqdomega)
    return kpg


def get_kig(eta, i_r, i_g, n_g, omega):
    """
    Get the kpg param in 2.5
    """
    kig = eta * (i_r + n_g**2 * i_g) * omega**2
    return kig


def get_kp(zeta, omega, i_r, i_g, n_g, eta, dq_domega, dq_dtheta):
    """
    Get the Kp in #!/usr/bin/env python3
    """
    kp = (2 * zeta * omega * (i_r + n_g**2 * i_g) + dq_domega - dq_domega/eta) / (-dq_dtheta)
    return kp
    # last term on enumerator should be 0


def get_ki(omega, i_r, i_g, n_g, dq_dtheta):
    """
    Get Ki in part #!/usr/bin/env python3
    """
    ki = (omega**2 * (i_r + n_g**2 * i_g)) / (- dq_dtheta)
    return ki



eta = 0.94

dq_dtheta = -1313   # kNM/deg
omega_tau = 0.05    # Hz
zeta_tau = 0.7      # damping ratio
# omega tau is omega _g
omega_theta = 0.06 # Hz
