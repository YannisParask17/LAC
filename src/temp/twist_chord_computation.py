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
    
    
    chord_list = calc_chord(rad_positions, cl, tsr, n_blades)
    chord_list_tsr_10 = calc_chord(rad_positions, cl, 10, n_blades)
    chord_list_tsr_6 = calc_chord(rad_positions, cl, 6, n_blades)
    
    chord_list_cl_06 = calc_chord(rad_positions, 0.6, tsr, n_blades)
    chord_list_cl_14 = calc_chord(rad_positions, 1.4, tsr, n_blades)
    
    twist_list = calc_twist_deg(rad_positions, tsr, alpha)
    twist_list_tsr6 = calc_twist_deg(rad_positions, 6, alpha)
    twist_list_tsr10 = calc_twist_deg(rad_positions, 10, alpha)
    
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(rad_positions, chord_list, label='cl=1, tsr=8, n_blades=8')
    axs[0].plot(rad_positions, chord_list_tsr_10, label='cl=1, tsr=10, n_blades=8')
    axs[0].plot(rad_positions, chord_list_tsr_6, label='cl=1, tsr=6, n_blades=8')
    axs[0].plot(rad_positions, chord_list_cl_06, label='cl=0.6, tsr=8, n_blades=8')
    axs[0].plot(rad_positions, chord_list_cl_14, label='cl=1.4, tsr=8, n_blades=8')
    
    axs[1].plot(rad_positions, twist_list)
    axs[1].plot(rad_positions, twist_list_tsr10)
    axs[1].plot(rad_positions, twist_list_tsr6)
    
    [ax.grid() for ax in axs]
    axs[1].set_xlabel("Radius r/R (-)")
    axs[0].set_ylabel("Chord c/R (-)")
    axs[1].set_ylabel("Twist (deg)")
    
    axs[0].legend(loc='upper center', bbox_to_anchor=(0.5, -1.5),
            ncol=3, fancybox=True, shadow=False) 
    axs[0].set_ylim([0,0.18])
    fig.set_figheight(4)
    fig.set_figwidth(6)
    #plt.savefig("../../results/task1/chord_twist.pdf", bbox_inches='tight')
    #plt.show()

    # Do comparison of different amount of blades
    cl_list = [0.6, 0.8, 1, 1.2, 1.4]
    n_blade_list = [2, 3, 4, 5, 100]

    plt.figure(2)
    fig, axs = plt.subplots(1, 2)
    for n_blades in n_blade_list:
        chord_list = calc_chord(rad_positions, cl, tsr, n_blades)
        twist_list = calc_twist_deg(rad_positions, tsr, alpha)
    
        axs[0].plot(rad_positions, chord_list, label=f"N={n_blades}")
    
    for cl in cl_list:
        chord_list = calc_chord(rad_positions, cl, 8, 2.5)
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
    fig.set_figheight(2.5)
    fig.set_figwidth(8.3)
    plt.savefig("../../results/aero_design/chord_cl_n_blades.pdf", bbox_inches='tight')
    plt.show()
