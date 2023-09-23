# Equations for the chord and twist distribution

import numpy as np
import matplotlib.pyplot as plt

# ------------------#
# Functions
# ------------------#


def calc_chord(r_ratio, cl, tsr, n_blades):
    """ Compute the chord to Radius ratio for the given parameters

    Args:
        cl (float): Design lift coefficient
        tsr (float): Tip speed ratio
        n_blades (int): Number of blades
        r_ratio (float, np.array): Fraction of the position along the blade 

    Returns:
        flaot: Chord
    """    
    
    chord = (16 * np.pi)/(9) * (1/ (cl * tsr**2 * n_blades)) * (1/r_ratio)
    return chord 

def calc_twist_rad(r_ratio, tsr, alpha):
    """ Calculate the desired twist in rad

    Args:
        r_ratio (float, np.array): Fraction of the position along the blade 
        tsr (float): Tip speed ratio
        alpha (float): Design angle of attack 

    Returns:
        float: Combined pitch and twist angle in rad
    """    
    
    theta = 2/3 * (1/tsr)  * (1 / r_ratio) -alpha
    return theta

def calc_twist_deg(r_ratio, tsr, alpha):
    """ Calculate the desired twist in rad
    Wrapper

    Args:
        r_ratio (float, np.array): Fraction of the position along the blade 
        tsr (float): Tip speed ratio
        alpha (float): Design angle of attack 

    Returns:
        float: Combined pitch and twist angle in rad
    """    

    theta_rad = calc_twist_rad(rad_positions, tsr, alpha)
    theta_deg = np.rad2deg(theta_rad) 
    return theta_deg


if __name__ == '__main__':
   
    tsr= 8
    cl = 1
    n_blades = 3
    alpha = 0
    rad_positions = np.linspace(0.08, 1, 200)
    
    tsr_list = [6, 8, 10, 12]
    
    fig, axs = plt.subplots(1, 2)
    n_blades = 3
    cl = 1
    tsr = 8
    for tsr in tsr_list:

        chord_list = calc_chord(rad_positions, cl, tsr, n_blades)
        twist_list = calc_twist_deg(rad_positions, tsr, alpha)
    
        axs[0].plot(rad_positions, chord_list, label=f"TSR={tsr}")
        axs[1].plot(rad_positions, twist_list, label=f"TSR={tsr}")
    
    [ax.grid() for ax in axs]
    axs[0].set_xlabel("Radius r/R (-)")
    axs[1].set_xlabel("Radius r/R (-)")
    axs[0].set_ylabel("Chord c/R (-)")
    axs[1].set_ylabel("Twist (deg)")
    
    axs[0].legend()  # (loc='upper center', bbox_to_anchor=(0.5, -1.5),
    # ncol=3, fancybox=True, shadow=False)
    axs[0].set_ylim([0, 0.4])
    fig.set_figheight(2)
    fig.set_figwidth(10)
    
    plt.savefig("../../results/aero_design/chord_twist_tsr.pdf", bbox_inches='tight')
    # plt.savefig("../../results/task1/chord_twist.pdf", bbox_inches='tight')
    # plt.show()

    # Do comparison of different amount of blades
    cl_list = [0.6, 0.8, 1, 1.2, 1.4]
    n_blade_list = [2, 3, 4, 5, 100]

    fig, axs = plt.subplots(1, 2)
    n_blades = 3
    cl = 1
    tsr = 8
    for n_blades in n_blade_list:

        chord_list = calc_chord(rad_positions, cl, tsr, n_blades)
        twist_list = calc_twist_deg(rad_positions, tsr, alpha)
    
        axs[0].plot(rad_positions, chord_list, label=f"B={n_blades}")
    
    n_blades = 3
    cl = 1
    tsr = 8
    for cl in cl_list:

        chord_list = calc_chord(rad_positions, cl, 8, 3)
        twist_list = calc_twist_deg(rad_positions, 8, alpha)
    
        axs[1].plot(rad_positions, chord_list, label=f'$C_l= {{{cl}}}$')

    [ax.grid() for ax in axs]
    axs[0].set_xlabel("Radius r/R (-)")
    axs[1].set_xlabel("Radius r/R (-)")
    axs[0].set_ylabel("Chord c/R (-)")
    axs[1].set_ylabel("Chord c/R (-)")
    
    axs[0].legend()  #(loc='upper center', bbox_to_anchor=(0.5, -1.5),
    axs[1].legend()  #(loc='upper center', bbox_to_anchor=(0.5, -1.5),
    # ncol=3, fancybox=True, shadow=False) 
    axs[0].set_ylim([0, 0.4])
    axs[1].set_ylim([0, 0.4])
    fig.set_figheight(2)
    fig.set_figwidth(10)
    plt.savefig("../../results/aero_design/chord_cl_n_blades.pdf", bbox_inches='tight')
    plt.show()
