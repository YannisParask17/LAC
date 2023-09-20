# Compute the site conditions / wind stuff for the new class
# M Janssen
# September '23


import numpy as np
import matplotlib.pyplot as plt


def wind_speed_cdf(v_hub, v_avg):
    """
    Cummulative density function of the Wind speed from IEC ch. 6.3.1.1 (Rayleigh dist.)
    """
    p = 1 - np.exp(- np.pi* (v_hub/(2*v_avg))**2)
    return p


def get_prob_per_bin(v_range, v_avg):
    """
    Get the probability of a wind velocity bin. Assume uniform bin size
    """
    bin_size = v_range[1] - v_range[0]
    probabilities = np.empty(len(v_range))
    for i, v in enumerate(v_range):
        v_upper = v + 0.5*bin_size
        v_lower = v - 0.5*bin_size
        probabilities[i] = wind_speed_cdf(v_upper, v_avg) - wind_speed_cdf(v_lower, v_avg)
        #breakpoint()
    return probabilities


if __name__=="__main__":
   
    # --------------------------------------------------------#
    # Parameters
    # --------------------------------------------------------#
   
    savepath="../results/aero_design/wind_dist.pdf"


    # Known values for the new site
    # We scale from 1a to 3b
    v_ref = 37.5  # Class 3b

    v_avg = 0.2 * v_ref

    # --------------------------------------------------------#
    # Visualization
    # --------------------------------------------------------#

    v_range = np.linspace(0.1, 50, 500)
    p_range = get_prob_per_bin(v_range, v_avg)
    P_range = wind_speed_cdf(v_range, v_avg)
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(v_range, p_range)
    axs[1].set_xlabel("Wind speed (m/s)")
    axs[0].set_ylabel("Probability density (-)")
    axs[1].set_ylabel("Cummulative probability (-)")
    axs[1].plot(v_range, P_range)
    axs[0].grid()
    axs[1].grid()
    plt.savefig(savepath, bbox_inches='tight')
    plt.show()
