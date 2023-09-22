import lacbox.io as lac
import numpy as np
import matplotlib.pyplot as plt

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
        fig.legend(labels, loc='upper center', ncol=2)

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
        ax[0].plot(rpm2rads(pwr_data["Speed_rpm"])*pwr_data["Tip_z_m"]/pwr_data["V_ms"][0], pwr_data["Cp"] )
        ax[0].set_xlabel("Tip speed ratio (-)")
        ax[0].set_ylabel(r"$C_P$ (-)")

        ax[1].plot(rpm2rads(pwr_data["Speed_rpm"])*pwr_data["Tip_z_m"]/pwr_data["V_ms"][0], pwr_data["Ct"] )
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
    



if __name__ == "__main__":
    # Import power data
    pwr_data = lac.load_pwr("dtu_10mw_hawc2s_rigid_1point.pwr")
    print(pwr_data)

    # Import induction data
    ind_data = lac.load_ind("dtu_10mw_hawc2s_rigid_1point_u8000.ind")
    ind_data2 = lac.load_ind("dtu_10mw_hawc2s_rigid_1point_u8000.ind")
    print(ind_data)

    # Import ae file (radial position ,chord, relative thickness)
    r, chord, t_c, _ = lac.load_ae("data/DTU_10MW_RWT_ae.dat", unpack=True) 

    # Plot spanwise results
    plot_spanwise([ind_data], None, "spanwise_rigid.pdf")

    # Plot geometric properties
    geom = prepare_geometry("dtu_10mw_hawc2s_rigid_1point_u8000.ind", "data/DTU_10MW_RWT_ae.dat")
    plot_geometry(geom, "spanwise_geometry.pdf")


    # Plot performance for different TSR
    pwrdata_tsr = lac.load_pwr("dtu_10mw_hawc2s_rigid_varTSR.pwr")
    plot_performance([pwrdata_tsr], None,"performance_varTSR.pdf")

    # Plot spanwise results for different TSR
    ind_data6 = lac.load_ind("dtu_10mw_hawc2s_rigid_varTSR_u8000.ind") # tsr=6
    ind_data65 = lac.load_ind("dtu_10mw_hawc2s_rigid_varTSR_u8001.ind") # tsr=6.5
    ind_data7 = lac.load_ind("dtu_10mw_hawc2s_rigid_varTSR_u8002.ind") # tsr=7
    ind_data75 = lac.load_ind("dtu_10mw_hawc2s_rigid_varTSR_u8003.ind") # tsr=7.5
    ind_data8 = lac.load_ind("dtu_10mw_hawc2s_rigid_varTSR_u8004.ind") # tsr=8
    ind_data85 = lac.load_ind("dtu_10mw_hawc2s_rigid_varTSR_u8005.ind") # tsr=8.5
    ind_data9 = lac.load_ind("dtu_10mw_hawc2s_rigid_varTSR_u8006.ind") # tsr=9
    ind_data_list = [ind_data6, ind_data65, ind_data7, ind_data75, ind_data8, ind_data85, ind_data9]
    lab = [r"$tsr=6$",r"$tsr=6.5$",r"$tsr=7$",r"$tsr=7.5$",r"$tsr=8$",r"$tsr=8.5$",r"$tsr=9$"]
    plot_spanwise(ind_data_list, lab, "spanwise_rigid_TSR.pdf")

    # Compare rigid vs flexible blade
    pwrdata_tsr_flex = lac.load_pwr("dtu_10mw_hawc2s_flexible_varTSR.pwr")
    lab = ["rigid", "flexible"]
    plot_performance([pwrdata_tsr,pwrdata_tsr_flex], lab, "performanceflexrigid_varTSR.pdf")
    plot_performance([pwrdata_tsr,pwrdata_tsr_flex], lab, "performanceflexrigid_varTSR.eps")

    ind_data6_flex = lac.load_ind("dtu_10mw_hawc2s_flexible_varTSR_u8000.ind") # tsr=6
    ind_data9_flex = lac.load_ind("dtu_10mw_hawc2s_flexible_varTSR_u8006.ind") # tsr=9
    ind_data_list = [ind_data6, ind_data6_flex, ind_data9, ind_data9_flex]
    lab = [r"$TSR=6$ rigid", r"$TSR=6$ flex", r"$TSR=9$ rigid", r"$TSR=9$ flex"]
    plot_spanwise(ind_data_list,lab,"spanwise_rigidflex_TSR.pdf")
    plot_spanwise(ind_data_list,lab,"spanwise_rigidflex_TSR.eps")

