import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lacbox.io import load_c2def, save_c2def, load_pc
import json

'''
The following code plots polar data of the 10MW RWT blade
as well as the design points for each airfoil of that blade
'''


def numpy_to_list(obj):
    """

    Parameters
    ----------
    obj : list of dictionaries. Each dictionary contains np arrays

    Returns
    -------
    obj : json serialisable list -> can be written in a txt file

    """
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def save_json(polar_data, save_name):

    print('Saving data in json file...')
    with open(save_name, 'w') as fp:
        json.dump(polar_data, fp, default=numpy_to_list)
        print('Done!')
    return None


def interp_cl(cl_des, cl_list, aoa_list, cd_list=None):
    '''
    Returns the aoa and cd for the selected cl_design 
    by interpolating airfoil data  
    '''

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


def calc_aero(polar_data):
    
    for iprof, prof in enumerate(polar_data):
        polar_data[iprof]['cl_max'] = np.max(polar_data[iprof]['cl'])
        polar_data[iprof]['cl_des'] = polar_data[iprof]['cl_max'] - .4

        # neglect cylinder and t/c=60% airfoil (as mentioned in the assignment description) 
        if polar_data[iprof]['comment'] == 'Cylinder':
            continue
        
        # compute aoa and cd for chosen cl (cl_max - 0.4)
        polar_data[iprof]['aoa_des'], polar_data[iprof]['cd_des'] = interp_cl(polar_data[iprof]['cl_des'],
                                                                            polar_data[iprof]['cl'],
                                                                            polar_data[iprof]['aoa_deg'],
                                                                            polar_data[iprof]['cd'])
    return polar_data



def plot_polar(polar_data_list, savename=None):
    '''
    Visualizes polar data for each aerofoil section of the blade
    '''

    fig, ax = plt.subplots(1,3, figsize=(12,6))
    lab = []

    for polar_data in polar_data_list:
        for iprof, prof in enumerate(polar_data):
            
            # neglect cylinder
            if polar_data[iprof]['comment'] == 'Cylinder':
                continue

            ax[0].plot(polar_data[iprof]['cd'],polar_data[iprof]['cl'], label=f'{polar_data[iprof]["comment"]}')
            ax[0].plot(polar_data[iprof]['cd_des'],polar_data[iprof]['cl_des'], 'xk', label=f'design point-{polar_data[iprof]["comment"]}')
            
            ax[1].plot(polar_data[iprof]['aoa_deg'],polar_data[iprof]['cl'], label=f'{polar_data[iprof]["comment"]}')
            ax[1].plot(polar_data[iprof]['aoa_des'],polar_data[iprof]['cl_des'], 'xk', label=f'design point-{polar_data[iprof]["comment"]}')
            
            ax[2].plot(polar_data[iprof]['aoa_deg'],polar_data[iprof]['cl']/polar_data[iprof]['cd'], label=f'{polar_data[iprof]["comment"]}')
            ax[2].plot(polar_data[iprof]['aoa_des'],polar_data[iprof]['cl_des']/polar_data[iprof]['cd_des'], 'xk', label=f'design point-{polar_data[iprof]["comment"]}')
            
            lab.append(polar_data[iprof]['comment'])
            lab.append(f'design-point:{polar_data[iprof]["comment"]}')
        
            ax[0].set_xlabel(r'$C_d$ [-]')
            ax[0].set_ylabel(r'$C_l$ [-]')
            ax[0].set_xlim((0,.25))
            ax[0].set_ylim((1,2))
            ax[0].grid(True)

            ax[1].set_xlabel(r'$\alpha$ [deg]')
            ax[1].set_ylabel(r'$C_l$ [-]')
            ax[1].set_xlim((0,25))
            ax[1].set_ylim((-.1,2))
            ax[1].grid()

            ax[2].set_xlabel(r'$\alpha$ [deg]')
            ax[2].set_ylabel(r'$C_l/C_d$ [-]')
            ax[2].set_xlim((0,25))
            ax[2].grid()

            fig.legend(lab, loc='upper center', ncol=4, fontsize=9)
    
    plt.tight_layout()    
    if savename:
        plt.savefig(f'../../results/{savename}', bbox_inches='tight')

    plt.show()

    return None


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
    raw_data = load_pc('../../dtu_10mw/data/DTU_10MW_RWT_pc.dat')
    polar_data = calc_aero(raw_data)
    plot_polar([polar_data], 'polar_data.pdf')
    # Store data in json file
    save_json(polar_data, '../../results/polar_data.json')

