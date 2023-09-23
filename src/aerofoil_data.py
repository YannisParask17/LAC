#  %%
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from lacbox.io import load_c2def, save_c2def, load_pc
import json
from aero_design_functions import get_design_functions

# %%

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


def get_Cldes(cl_list, aoa_list, cd_list, aoa_limiter=False):

    if aoa_limiter:
        aoa_clmax = aoa_limiter
    else:
        aoa_clmax = aoa_list[cl_list == np.max(cl_list)]

    mask1 = (aoa_list > 0)
    mask2 = (aoa_list < aoa_clmax)
    mask = np.logical_and(mask1,mask2)

    # find cl_max based on aoa>0 and aoa<aoa_max
    cl_max = np.max(cl_list[mask])
    # cl design = cl_max - 0.4
    cl_des = cl_max - 0.4

    # interpolate cl
    temp_cl_list = cl_list[mask]
    temp_aoa_list = aoa_list[mask]

    # interpolating data : calculate aoa, cd at cl_des   
    aoa_des = np.interp(cl_des, temp_cl_list, temp_aoa_list)
    if cd_list is not None:
        temp_cd_list = cd_list[mask]
        cd_des = np.interp(cl_des, temp_cl_list, temp_cd_list)

    return cl_des, cd_des, aoa_des


def interp_cl(cl_des, cl_list, aoa_list, cd_list=None, aoa_limiter=None):
    '''
    Returns the aoa and cd for the selected cl_design 
    by interpolating airfoil data  
    '''

    # slicing the aoa data for aoa > 0 and aoa < aoa@cl_max
    if aoa_limiter:
        aoa_clmax = 10
    else:
        aoa_clmax = aoa_list[cl_list == np.max(cl_list)]
    
    aoa_clmax_idx = aoa_list < aoa_clmax
    aoa_nonnegative = aoa_list > 0
    mask = np.logical_and(aoa_clmax, aoa_nonnegative)
    # creating cl and aoa lists in ascending order for interpolation
    # (np.interp need the data to be in ascending order) 
    temp_cl_list = cl_list[ aoa_nonnegative & aoa_clmax_idx]
    temp_aoa_list = aoa_list[aoa_nonnegative & aoa_clmax_idx]
    temp_cl_list = cl_list[mask]
    temp_aoa_list = aoa_list[mask]
    
    try:
        # interpolating data : calculate aoa, cd at cl_des   
        aoa_des = np.interp(cl_des, temp_cl_list, temp_aoa_list)
        if cd_list is not None:
            temp_cd_list = cd_list[aoa_nonnegative & aoa_clmax_idx]
            temp_cd_list = cd_list[mask]
            cd_des = np.interp(cl_des, temp_cl_list, temp_cd_list)

        # print(f'cd_des : {cd_des}')
        # print(f'temp_cd_list : {temp_cd_list}')
        print(aoa_clmax)
        return aoa_des, cd_des
    except:
        print(len(temp_cl_list), len(temp_aoa_list), len(cd_list))


def calc_aero(polar_data):
    # neglect cylinder and t/c=60% airfoil (as mentioned in the assignment description) 

    
    for iprof, prof in enumerate(polar_data):

        if polar_data[iprof]['tc'] == 100:
            continue
        
        if polar_data[iprof]['tc'] == 48:
            aoa_limiter = 10
        else:
            aoa_limiter = False

        polar_data[iprof]['cl_des'], polar_data[iprof]['cd_des'], polar_data[iprof]['aoa_des'] = get_Cldes(polar_data[iprof]['cl'],
                                                                                                           polar_data[iprof]['aoa_deg'],
                                                                                                           polar_data[iprof]['cd'],
                                                                                                           aoa_limiter)

    return polar_data



def plot_polar(polar_data_list, savename=None):
    '''
    Visualizes polar data for each aerofoil section of the blade
    '''

    fig, ax = plt.subplots(1,3, figsize=(15,5))
    lab = []
    symbols = ['x', 'o', 'D', 'v']

    for polar_data in polar_data_list:
        for iprof, prof in enumerate(polar_data):
            
            # neglect cylinder
            if (polar_data[iprof]['tc'] == 100) or (polar_data[iprof]['tc'] == 60):
                continue

            ax[0].plot(polar_data[iprof]['cd'],polar_data[iprof]['cl'])
            ax[0].plot(polar_data[iprof]['cd_des'],polar_data[iprof]['cl_des'], f'k{symbols[iprof]}')
            
            ax[1].plot(polar_data[iprof]['aoa_deg'],polar_data[iprof]['cl'])
            ax[1].plot(polar_data[iprof]['aoa_des'],polar_data[iprof]['cl_des'], f'k{symbols[iprof]}')
            
            ax[2].plot(polar_data[iprof]['aoa_deg'],polar_data[iprof]['cl']/polar_data[iprof]['cd'])
            ax[2].plot(polar_data[iprof]['aoa_des'],polar_data[iprof]['cl_des']/polar_data[iprof]['cd_des'], f'k{symbols[iprof]}')
            
            lab.append(polar_data[iprof]['comment'][:11])
            lab.append(f'design-point:{polar_data[iprof]["comment"][:11]}')
        
            ax[0].set_xlabel(r'$C_d$ [-]')
            ax[0].set_ylabel(r'$C_l$ [-]')
            ax[0].set_xlim((0,.2))
            # ax[0].set_ylim((0,2))
            ax[0].grid(True)

            ax[1].set_xlabel(r'$\alpha$ [deg]')
            ax[1].set_ylabel(r'$C_l$ [-]')
            ax[1].set_xlim((0,20))
            # ax[1].set_ylim((-.1,2))
            ax[1].grid(True)

            ax[2].set_xlabel(r'$\alpha$ [deg]')
            ax[2].set_ylabel(r'$C_l/C_d$ [-]')
            ax[2].set_xlim((0,20))
            ax[2].grid(True)

        fig.legend(lab, loc='upper center', ncol=4)

    if savename:
        plt.savefig(f'../results/{savename}', bbox_inches='tight')

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
    raw_data = load_pc('../dtu_10mw/data/DTU_10MW_RWT_pc.dat')
    polar_data = calc_aero(raw_data)
    # plot_polar([polar_data], 'polar_data.pdf')

    # Store data in json file
    # save_json(polar_data, '../../results/polar_data.json')

    sliced_data = np.copy(polar_data)
    mask1 = (polar_data[0]['aoa_deg'] >= 0) 
    mask2 = (polar_data[0]['aoa_deg'] <= 30)
    mask = np.logical_and(mask1, mask2)
        
    for iprof, prof in enumerate(polar_data):
        sliced_data[iprof]['aoa_deg'] = polar_data[iprof]['aoa_deg'][mask] 
        sliced_data[iprof]['cl'] = polar_data[iprof]['cl'][mask] 
        sliced_data[iprof]['cd'] = polar_data[iprof]['cd'][mask] 

    plot_polar([sliced_data], 'polar_data.pdf')

# %%
cl_des1, cd_des1, aoa_des1, tc_vals1, cl_vals1, cd_vals1, aoa_vals1 = get_design_functions(1)
cl_des2, cd_des2, aoa_des2, tc_vals2, cl_vals2, cd_vals2, aoa_vals2 = get_design_functions(2)
cl_des3, cd_des3, aoa_des3, tc_vals3, cl_vals3, cd_vals3, aoa_vals3 = get_design_functions(3)

tc_plot = np.linspace(0, 100, 101)
cl1 = cl_des1(tc_plot)
cl2 = cl_des2(tc_plot)
cl3 = cl_des3(tc_plot)

cd1 = cd_des1(tc_plot)
cd2 = cd_des2(tc_plot)
cd3 = cd_des3(tc_plot)

aoa1 = aoa_des1(tc_plot)
aoa2 = aoa_des2(tc_plot)
aoa3 = aoa_des3(tc_plot)

tc_list = [polar_data[iprof]['tc'] for iprof,prof in enumerate(polar_data) if not prof['tc']==100]
cl = [polar_data[iprof]['cl_des'] for iprof,prof in enumerate(polar_data) if not prof['tc']==100]
cd = [polar_data[iprof]['cd_des'] for iprof,prof in enumerate(polar_data) if not prof['tc']==100]
aoa = [polar_data[iprof]['aoa_des'] for iprof,prof in enumerate(polar_data) if not prof['tc']==100]

tc_list = np.array(tc_list)
cl = np.array(cl)
cd = np.array(cd)
aoa = np.array(aoa)


fig, axs = plt.subplots(3, 1, figsize=(15,5))
axs[0].scatter(tc_list[:-1], cl[:-1])
axs[0].plot(tc_plot, cl1)
axs[0].plot(tc_plot, cl2)
axs[0].plot(tc_plot, cl3)
# axs[0].scatter(tc_vals1, cl_vals1)

axs[1].scatter(tc_list[:-1], cl[:-1]/cd[:-1])
axs[1].plot(tc_plot, cl1/cd1)
axs[1].plot(tc_plot, cl2/cd2)
axs[1].plot(tc_plot, cl3/cd3)
axs[2].scatter(tc_list[:-1], aoa[:-1])
axs[2].plot(tc_plot, aoa1)
axs[2].plot(tc_plot, aoa2)
axs[2].plot(tc_plot, aoa3)

axs[0].set_ylabel(r'$C_l$ [-]')
axs[1].set_ylabel(r'$C_l/C_d$ [-]')
axs[2].set_ylabel(r'$\alpha$ [deg]')
axs[2].set_xlabel(r'$t/c$ [-]')
axs[0].grid()
axs[1].grid()
axs[2].grid()

lbs = ['design datapoints', 'DF 1', 'DF2', 'DF3']
fig.legend(lbs, loc='upper center', ncol=4)
plt.show()
