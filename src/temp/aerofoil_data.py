import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lacbox.io import load_c2def, save_c2def, load_pc


def plot_polar(polar_data, savename=None):

    fig, ax = plt.subplots(1,3)
    lab = []

    for iprof, prof in enumerate(polar_data):
        
        polar_data[iprof]['cl_max'] = np.max(polar_data[iprof]['cl'])
        polar_data[iprof]['cl_des'] = polar_data[iprof]['cl_max'] - .4

        # neglect cylinder and t/c=60% airfoil (as mentioned in the assignment description) 
        if polar_data[iprof]['comment'] == 'Cylinder' or polar_data[iprof]['comment'] == 'FFA-W3-"600" (Re=6x10^6)':
            continue
        
        # compute aoa and cd for chosen cl (cl_max - 0.4)
        polar_data[iprof]['aoa_des'], polar_data[iprof]['cd_des'] = interp_cl(polar_data[iprof]['cl_des'],
                                                                              polar_data[iprof]['cl'],
                                                                              polar_data[iprof]['aoa_deg'],
                                                                              polar_data[iprof]['cd'])

        ax[0].plot(polar_data[iprof]['cd'],polar_data[iprof]['cl'], label=f'{polar_data[iprof]["comment"]}')
        ax[0].plot(polar_data[iprof]['cd_des'],polar_data[iprof]['cl_des'], 'xk', label=f'design point-{polar_data[iprof]["comment"]}')
        
        ax[1].plot(polar_data[iprof]['aoa_deg'],polar_data[iprof]['cl'], label=f'{polar_data[iprof]["comment"]}')
        ax[1].plot(polar_data[iprof]['aoa_des'],polar_data[iprof]['cl_des'], 'xk', label=f'design point-{polar_data[iprof]["comment"]}')
        
        ax[2].plot(polar_data[iprof]['aoa_deg'],polar_data[iprof]['cl']/polar_data[iprof]['cd'], label=f'{polar_data[iprof]["comment"]}')
        ax[2].plot(polar_data[iprof]['aoa_des'],polar_data[iprof]['cl_des']/polar_data[iprof]['cd_des'], 'xk', label=f'design point-{polar_data[iprof]["comment"]}')
        
        lab.append(polar_data[iprof]['comment'])
        lab.append(f'design-point:{polar_data[iprof]["comment"]}')

    ax[0].set_xlabel('cd (-)')
    ax[0].set_ylabel('cl (-)')
    ax[0].grid()

    ax[1].set_xlabel('aoa (deg)')
    ax[1].set_ylabel('cl (-)')
    ax[1].grid()

    ax[2].set_xlabel('aoa (deg)')
    ax[2].set_ylabel('cl/cd (-)')
    ax[2].set_xlim((-50,50))
    ax[2].grid()

    fig.legend(lab, loc='upper center', ncol=2)
    
    if savename:
        plt.savefig(f'../../results/{savename}', bbox_inches='tight')

    plt.show()




def interp_cl(cl_des, cl_list, aoa_list, cd_list=None):
    
    # slicing the aoa data for aoa > 0 and aoa < aoa@cl_max
    aoa_clmax = aoa_list[cl_list == np.max(cl_list)]
    aoa_clmax_idx = aoa_list < aoa_clmax
    aoa_nonnegative = aoa_list > 0
    
    # creating cl and aoa lists in ascending order for interpolation
    # (np.interp need the data to be in ascending order) 
    temp_cl_list = cl_list[ aoa_nonnegative & aoa_clmax_idx]
    temp_aoa_list = aoa_list[aoa_nonnegative & aoa_clmax_idx]
    
    # interpolating data : calculate aoa, cd at cl_des   
    aoa_des = np.interp(cl_des, temp_cl_list, temp_aoa_list)
    if cd_list is not None:
        temp_cd_list = cd_list[aoa_nonnegative & aoa_clmax_idx]
        cd_des = np.interp(cl_des, temp_cl_list, temp_cd_list)

    # print(f'cd_des : {cd_des}')
    # print(f'temp_cd_list : {temp_cd_list}')
    return aoa_des, cd_des


if __name__ == '__main__':

    # plot scaled centerline
    # c2_def = load_c2def('../../dtu_10mw/dtu_10mw_hawc2s_rigid_1point.htc')
    # R_scale = 1.037
    # c2_def_scaled = c2_def.copy()
    # c2_def_scaled[:,2] *= R_scale # scaling radius
    # c2_def_scaled[:,1] *= R_scale # scaling centreline
    # # print(type(c2_def_scaled))
    # c2_def_scaled[:,1] = np.clip(c2_def_scaled[:,1], np.min(c2_def_scaled[:,1]), None) # scaling centerline

    # plt.plot(c2_def[:,2], c2_def[:,1])
    # plt.plot(c2_def_scaled[:,2], c2_def_scaled[:,1])
    # plt.show()


    # Plot polar data
    polar_data = load_pc('../../dtu_10mw/data/DTU_10MW_RWT_pc.dat')
    print(polar_data)
    plot_polar(polar_data, 'assignment1/polar_data.pdf')
