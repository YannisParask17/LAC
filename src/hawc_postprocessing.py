# %%
import lacbox.io as lac
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from aero_design_functions import get_design_functions

def plot_spanwise(ind_data_list, labels=None, save_name=None):
    """
    Gets the dictionary for spanwise data imported via lacbox
    and plots a, ap, cl, cd, CT, CP along the span 
    """
    print("Plotting spanwise results...")
    fig, ax = plt.subplots(3,2, figsize=(12,5))
    for ind_data in ind_data_list:
        ax[0, 0].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["a"])
        ax[0, 0].set_ylabel(r"$a$ (-)")


        ax[0, 1].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["ap"])
        ax[0, 1].set_ylabel(r"$a'$ (-)")

        ax[1, 0].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["Cl"])
        ax[1, 0].set_ylabel(r"$C_l$ (-)")

        ax[1, 1].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["Cd"])
        ax[1, 1].set_ylabel(r"$C_d$ (-)")

        ax[2, 0].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["CP"])
        ax[2, 0].set_ylabel(r"$C_P$ (-)")
        ax[2, 0].set_xlabel(r"$r/R$ (-)")

        ax[2, 1].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["CT"])
        ax[2, 1].set_xlabel(r"$r/R$ (-)")
        ax[2, 1].set_ylabel(r"$C_T$ (-)")

    ax[0, 0].grid()
    ax[0, 1].grid()
    ax[1, 0].grid()
    ax[1, 1].grid()
    ax[2, 0].grid()
    ax[2, 1].grid()

    if labels:
        fig.legend(labels, loc='upper center', ncol=5)

    print("Done!")

    # Save figure
    if save_name:
        print("Saving figure...")
        plt.savefig(f"results/{save_name}", bbox_inches='tight')
        print("Done!")

    plt.show()
    return None


def plot_spanwise_modified(ind_data_list, labels=None, save_name=None):
    """
    Gets the dictionary for spanwise data imported via lacbox
    and plots a, ap, cl, cd, CT, CP along the span 
    """
    print("Plotting spanwise results...")
    fig, ax = plt.subplots(3,2, figsize=(12,5))
    for ind_data in ind_data_list:
        ax[0, 0].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["a"])
        ax[0, 0].set_ylabel(r"$a$ [-]")

        ax[0, 1].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["Cl"])
        ax[0, 1].set_ylabel(r"$C_l$ [-]")

        ax[1, 0].plot(ind_data["s_m"]/max(ind_data["s_m"]), np.rad2deg(ind_data["aoa_rad"]))
        ax[1, 0].set_ylabel(r"$\alpha$ [deg]")

        ax[1, 1].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["Cl"]/ind_data["Cd"])
        ax[1, 1].set_ylabel(r"$C_l/C_d$ [-]")

        ax[2, 0].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["CP"])
        ax[2, 0].set_ylabel(r"$C_P$ [-]")
        ax[2, 0].set_xlabel(r"$r/R$ [-]")

        ax[2, 1].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["CT"])
        ax[2, 1].set_xlabel(r"$r/R$ [-]")
        ax[2, 1].set_ylabel(r"$C_T$ [-]")

    ax[0, 0].grid()
    ax[0, 1].grid()
    ax[1, 0].grid()
    ax[1, 1].grid()
    ax[2, 0].grid()
    ax[2, 1].grid()

    if labels:
        fig.legend(labels, loc='upper center', ncol=5)

    print("Done!")

    # Save figure
    if save_name:
        print("Saving figure...")
        plt.savefig(f"results/{save_name}", bbox_inches='tight')
        print("Done!")

    plt.show()
    return None

def prepare_geometry(filename_ind, filename_ae):
    """

    """
    # Import files
    print("Preparing geometric properties...")
    ind_data = lac.load_ind(filename_ind)
    r, _, t_c, _ = lac.load_ae(filename_ae, unpack=True) 

    # Create a new dictionary with all geometric data in the spanwise direction
    req_fields = ["s_m", "chord_m", "twist_rad"] 
    geometric_props = {key : val for key,val in ind_data.items() if key in req_fields}
    geometric_props["t_c"], geometric_props["r"] = t_c, r
    # Note that for t/c plotting, different number of discrete points is used
    # "chord_m" and "twist_rad" are plotted against "s_m" as radial positions 
    # "t_c" is plotted against "r" as radial positions (This is due to HAWC2S ouputs)
    print("Done!")

    return geometric_props

def plot_geometry(geom_dict, save_name=None):

    print("Plotting geometric properties...")
    fig, ax = plt.subplots(1,3)
    ax[0].plot(geom_dict["s_m"]/max(geom_dict["s_m"]), geom_dict["chord_m"])
    ax[0].set_ylabel(r"Chord (m)")
    ax[0].set_xlabel(r"$r/R$ (-)")
    ax[0].grid()

    # print(ind_data.keys())
    ax[1].plot(geom_dict["s_m"]/max(geom_dict["s_m"]), np.rad2deg(geom_dict["twist_rad"]))
    ax[1].set_ylabel(r"Twist (deg)")
    ax[1].set_xlabel(r"$r/R$ (-)")
    ax[1].grid()

    ax[2].plot(geom_dict["r"]/max(geom_dict["r"]), geom_dict["t_c"])
    ax[2].set_ylabel(r"$t/c (\%)$ ")
    ax[2].set_xlabel(r"$r/R$ (-)")
    ax[2].grid()
    print("Done!")

    # Save figure
    if save_name:
        print("Saving figure...")
        plt.savefig(f"results/{save_name}", bbox_inches='tight')
        print("Done!")

    plt.show()
    
    return None


def rpm2rads(omega_rpm):
    return omega_rpm * (2*np.pi) / 60


def rads2rpm(omega_rads):
    return omega_rads * 60 / (2*np.pi)


def plot_performance(pwr_data_list, labels=None, save_name=None):
    """
    Getting dictionary with power and thrust for different TSR values
    and plots them
    """
    fig, ax = plt.subplots(1,2, figsize=(9,3))
    for pwr_data in pwr_data_list:
        ax[0].plot(rpm2rads(pwr_data["Speed_rpm"])*pwr_data["Tip_z_m"]/pwr_data["V_ms"], pwr_data["Cp"] )
        ax[0].set_xlabel("Tip speed ratio (-)")
        ax[0].set_ylabel(r"$C_P$ (-)")

        ax[1].plot(rpm2rads(pwr_data["Speed_rpm"])*pwr_data["Tip_z_m"]/pwr_data["V_ms"], pwr_data["Ct"] )
        ax[1].set_xlabel("Tip speed ratio (-)")
        ax[1].set_ylabel(r"$C_T$ (-)")

    ax[0].grid()
    ax[1].grid()

    if labels:
        fig.legend(labels, loc='upper center', ncol=2)

    if save_name:
        print("Saving figure...")
        plt.savefig(f"results/{save_name}", bbox_inches="tight")
        print("Done")

    plt.show()
    return None

def plot_powercurve(pwr_data_list, labels=None, save_name=None):
    """
    Getting dictionary with power and thrust for different wind speeds
    and generates the power curve 
    """
    fig, ax = plt.subplots(2,2, figsize=(12,3))
    for pwr_data in pwr_data_list:
        ax[0,0].plot(pwr_data["V_ms"], pwr_data["P_kW"])

        ax[0,1].plot(pwr_data["V_ms"], pwr_data["T_kN"])

        ax[1,0].plot(pwr_data["V_ms"], pwr_data["Cp"])

        ax[1,1].plot(pwr_data["V_ms"], pwr_data["Ct"] )
        
    ax[0,0].set_ylabel(r"Mechanical Power [kW]")
    ax[0,1].set_ylabel(r"Thrust [kN]")
    ax[1,0].set_ylabel(r"$C_P$ [-]")
    ax[1,1].set_ylabel(r"$C_T$ (-)")
    ax[1,0].set_xlabel("Wind speed [m/s]")
    ax[1,1].set_xlabel("Wind speed [m/s]")

    ax[0, 0].set_xticklabels([])
    ax[0, 1].set_xticklabels([])

    ax[0,0].grid()
    ax[0,1].grid()
    ax[1,0].grid()
    ax[1,1].grid()

    if labels:
        fig.legend(labels, loc='upper center', ncol=2)

    if save_name:
        print("Saving figure...")
        plt.savefig(f"../results/{save_name}", bbox_inches="tight")
        print("Done")

    plt.show()
    return None

def plot_deflections(ind_data_list, labels=None, save_name=None):
    """
    Getting dictionary with power and thrust for different wind speeds
    and generates the power curve 
    """
    fig, ax = plt.subplots(1,2, figsize=(12,3))
    for ind_data in ind_data_list:
        ax[0].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["UX0_m"])

        ax[1].plot(ind_data["s_m"]/max(ind_data["s_m"]), ind_data["UY0_m"])
        
    ax[0].set_ylabel(r"Edgewise deflection [m]")
    ax[0].set_xlabel(r"$r/R$ [-]")
    ax[1].set_ylabel(r"Flapwise deflection [m]")
    ax[1].set_xlabel(r"$r/R$ [-]")

    ax[0].grid()
    ax[1].grid()

    if labels:
        fig.legend(labels, loc='upper center', ncol=2)

    if save_name:
        print("Saving figure...")
        plt.savefig(f"../results/{save_name}", bbox_inches="tight")
        print("Done")

    plt.show()
    return None
    

if __name__ == "__main__":

    # file paths
    path_dtu10mw = "../dtu_10mw/"
    path_scaled = "../dtu_10mw_redesign/"


    # import hawc results
    ind_scaled_opt = lac.load_ind(path_scaled + "dtu_10mw_hawc2s_rigid_1point_u4000.ind")
    ind_scaled_rated = lac.load_ind(path_scaled + "dtu_10mw_hawc2s_rigid_1point_u11100.ind")
    ind_scaled_14 = lac.load_ind(path_scaled + "dtu_10mw_hawc2s_rigid_1point_u14000.ind")
    ind_scaled_18 = lac.load_ind(path_scaled + "dtu_10mw_hawc2s_rigid_1point_u18000.ind")
    ind_scaled_25 = lac.load_ind(path_scaled + "dtu_10mw_hawc2s_rigid_1point_u25000.ind")
    print(ind_scaled_opt.keys())

    # plot spanwise for different operational points
    # lab = ['optimal', 'rated', r'above rated-$u=$14m/s', r'above rated-$u=$18m/s',r'cut-out']
    # plot_spanwise_modified([ind_scaled_opt, ind_scaled_rated, ind_scaled_14, ind_scaled_18,  ind_scaled_25], labels=lab)

    # import design code results
    ind_scaled_dc = pd.read_json('../results/design_parameters_at_max_cp.json')
    print(ind_scaled_dc.head())

    # plot hawc vs design code spanwise results
    lab = ["HAWC2", "Design code"]

    fig, ax = plt.subplots(3, 2, figsize=(11, 4.2))
    ax[0, 0].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), ind_scaled_opt["a"])
    ax[0, 0].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), ind_scaled_dc["a"])
    ax[0, 0].set_ylabel(r"$a$ [-]")

    ax[0, 1].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), ind_scaled_opt["Cl"])
    ax[0, 1].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), ind_scaled_dc["cl"])
    ax[0, 1].set_ylabel(r"$C_l$ [-]")

    ax[1, 0].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), np.rad2deg(ind_scaled_opt["aoa_rad"]))
    ax[1, 0].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), ind_scaled_dc["aoa"])
    ax[1, 0].set_ylabel(r"$\alpha$ [deg]")

    ax[1, 1].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), ind_scaled_opt["Cl"]/ind_scaled_opt["Cd"])
    ax[1, 1].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), ind_scaled_dc["cl"]/ind_scaled_dc["cd"])
    ax[1, 1].set_ylabel(r"$C_l/C_d$ [-]")

    ax[2, 0].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), ind_scaled_opt["CP"])
    ax[2, 0].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), ind_scaled_dc["CLP"])
    ax[2, 0].set_ylabel(r"$C_P$ [-]")
    ax[2, 0].set_xlabel(r"$r/R$ [-]")

    ax[2, 1].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), ind_scaled_opt["CT"])
    ax[2, 1].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), ind_scaled_dc["CLT"])
    ax[2, 1].set_xlabel(r"$r/R$ [-]")
    ax[2, 1].set_ylabel(r"$C_T$ [-]")

    ax[0, 0].set_xticklabels([])
    ax[1, 0].set_xticklabels([])
    ax[0, 1].set_xticklabels([])
    ax[1, 1].set_xticklabels([])
    
    ax[0, 0].grid(axis='both')
    ax[0, 1].grid()
    ax[1, 0].grid()
    ax[1, 1].grid()
    ax[2, 0].grid()
    ax[2, 1].grid()

    fig.legend(lab, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 0.97))
    fig.savefig('../results/spanwise_comparison.pdf', bbox_inches='tight')

    # side-by-side plots of the actual lift
    # coefficient and the design lift coefficient versus relative thickness (left plot) and versus radius
    # (right plot) for design pitch and TSR.

    # import t/c from ae file -> THE PROBLEM MIGHT BE HERE
    r_ae, c_ae, tc_ae, _ = lac.load_ae(path_scaled + "data/10MW_1a_ae.dat", unpack=True)
    tc_hawc = np.interp(ind_scaled_opt["s_m"], r_ae, tc_ae)  # Bringing tc in the same spacing of the ind file
    print(f"tc_hawc : {tc_hawc}")

    fig, ax = plt.subplots(3, 2, figsize=(11, 4.2))

    # Left plot:  Cl over t/c
    ax[0, 0].plot(tc_hawc, ind_scaled_opt["Cl"])
    ax[0, 0].plot(ind_scaled_dc["tc"], ind_scaled_dc["cl"])
    ax[0, 0].set_ylabel(r"$C_l$ [-]")
    # ax[0, 0].set_xlabel(r"$t/c$ [-]")

    ax[0, 1].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), ind_scaled_opt["Cl"])
    ax[0, 1].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), ind_scaled_dc["cl"])
    ax[0, 1].set_ylabel(r"$C_l$ [-]")
    # ax[0, 1].set_xlabel(r"$r/R$ [-]")

    # Same for the Cl/cd
    ax[1, 0].plot(tc_hawc, ind_scaled_opt["Cl"]/ind_scaled_opt["Cd"])
    ax[1, 0].plot(ind_scaled_dc["tc"], ind_scaled_dc["cl"]/ind_scaled_dc["cd"])
    ax[1, 0].set_ylabel(r"$C_l / C_d$ [-]")
    # ax[1, 0].set_xlabel(r"$t/c$ [-]")

    ax[1, 1].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), ind_scaled_opt["Cl"] / ind_scaled_opt["Cd"])
    ax[1, 1].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), ind_scaled_dc["cl"]/ind_scaled_dc["cd"])
    ax[1, 1].set_ylabel(r"$C_l/C_d$ [-]")
    # ax[1, 1].set_xlabel(r"$r/R$ [-]")

    # And for the AOA
    # breakpoint()
    ax[2, 0].plot(tc_hawc, np.rad2deg(ind_scaled_opt["aoa_rad"]))
    ax[2, 0].plot(ind_scaled_dc["tc"], (ind_scaled_dc["aoa"]))
    ax[2, 0].set_ylabel(r"aoa $[^\circ]$")
    ax[2, 0].set_xlabel(r"$t/c$ [%]")

    ax[2, 1].plot(ind_scaled_opt["s_m"]/max(ind_scaled_opt["s_m"]), np.rad2deg(ind_scaled_opt["aoa_rad"]))
    ax[2, 1].plot(ind_scaled_dc["r"]/max(ind_scaled_dc["r"]), (ind_scaled_dc["aoa"]))
    ax[2, 1].set_ylabel(r"aoa $[^\circ]$")
    ax[2, 1].set_xlabel(r"$r/R$ [-]")
    
    ax[0, 0].set_xticklabels([])
    ax[1, 0].set_xticklabels([])
    ax[0, 1].set_xticklabels([])
    ax[1, 1].set_xticklabels([])

    [[ax_c.grid() for ax_c in axs]for axs in ax]
    fig.show()
    fig.legend(lab, loc='upper center', ncol=2, bbox_to_anchor=(0.5, 0.97))
    fig.savefig('../results/cl_comparison.pdf', bbox_inches='tight')


    # Rotor speed vs wind speed
    pwr_scaled = lac.load_pwr(path_scaled + "dtu_10mw_hawc2s_rigid_1point.pwr")
    print(pwr_scaled.keys())

    fig, ax = plt.subplots(1,2, figsize=(8,3))   
    ax[0].plot(pwr_scaled["V_ms"], pwr_scaled["Speed_rpm"])
    ax[0].set_xlabel("Wind speed [m/s]")
    ax[0].set_ylabel("Rotor speed [rpm]")
    ax[0].grid()

    ax[1].plot(pwr_scaled["V_ms"], pwr_scaled["Pitch_deg"])
    ax[1].set_xlabel("Wind speed [m/s]")
    ax[1].set_ylabel("Pitch angle [deg]")
    ax[1].grid()

    fig.show()
    fig.savefig("../results/omega_pitch_vs_windspeed.pdf", bbox_inches='tight')


    # power and thrust vs wind speed
    pwr_dtu10mw = lac.load_pwr(path_dtu10mw + "dtu_10mw_hawc2s_rigid.pwr")
    lab = ["DTU10MW", "Scaled"]
    plot_powercurve([pwr_dtu10mw, pwr_scaled], labels=lab, save_name="comparison_powercurve.pdf")

    

    # deflections in the spanwise direction
    ind_scaled_flex = lac.load_ind(path_scaled + 'dtu_10mw_hawc2s_flex_u8000.ind') # for optimal tsr
    ind_dtu10mw_flex = lac.load_ind(path_dtu10mw + 'dtu_10mw_hawc2s_flexible_varTSR_u8004.ind')
    lab = ["DTU10MW", "Scaled"]
    plot_deflections([ind_dtu10mw_flex, ind_scaled_flex], labels=lab, save_name='deflections_comparison.pdf')


    # spanwise Cp and CT comparison dtu10mw vs scaled 
    fig, ax = plt.subplots(1,2, figsize=(12,3))   
    ax[0].plot(ind_dtu10mw_flex["s_m"]/max(ind_dtu10mw_flex["s_m"]), ind_dtu10mw_flex["CP"])
    ax[0].plot(ind_scaled_flex["s_m"]/max(ind_scaled_flex["s_m"]), ind_scaled_flex["CP"])
    ax[0].set_ylabel(r"$C_P$ [-]")
    ax[0].set_xlabel(r"$r/R$ [-]")
    ax[0].grid()

    ax[1].plot(ind_dtu10mw_flex["s_m"]/max(ind_dtu10mw_flex["s_m"]), ind_dtu10mw_flex["CT"])
    ax[1].plot(ind_scaled_flex["s_m"]/max(ind_scaled_flex["s_m"]), ind_scaled_flex["CT"])
    ax[1].set_xlabel(r"$r/R$ [-]")
    ax[1].set_ylabel(r"$C_T$ [-]")
    ax[1].grid()

    lab = ["DTU10MW-flex", "Scaled-flex"]
    fig.legend(lab, loc='upper center', ncol=2)
    fig.savefig('../results/spanwiseCPCT_comparison.pdf', bbox_inches='tight')
    fig.show()

    plt.show()

    # compare Cp and CT at optimal tsr for u=8m/s  for dtu10mw and scaled turbine
    CP_dtu10mw_8ms = pwr_dtu10mw["Cp"][pwr_dtu10mw["V_ms"]==8]
    CT_dtu10mw_8ms = pwr_dtu10mw["Ct"][pwr_dtu10mw["V_ms"]==8]

    CP_scaled_8ms = pwr_scaled["Cp"][pwr_scaled["V_ms"]==8]
    CT_scaled_8ms = pwr_scaled["Ct"][pwr_scaled["V_ms"]==8]

    print("DTU10MW")
    print(f"CP : {CP_dtu10mw_8ms} \t CT : {CT_dtu10mw_8ms}")
    print("\nScaled design")
    print(f"CP : {CP_scaled_8ms} \t CT : {CT_scaled_8ms}")
    
    
# %%
