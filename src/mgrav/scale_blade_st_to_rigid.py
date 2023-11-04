# This script is used to make a rigid blade

# LAC
# November '23
# M Janssen


from lacbox.io import load_st, save_st

input_path = '../../IIIB_scaled_turbine/data/IIIB_scaled_turbine_Blade_st.dat'
output_path = '../../results/mgrav/IIIB_scaled_turbine_Blade_st_rigid.dat'

st_data = load_st(input_path)
print(f"Number of sets: len(st_data)={len(st_data)}")
print(f"Number of subsets: len(st_data[0])={len(st_data[0])}")
print(f"Subset keys: st_data[i][j].keys()={st_data[0][0].keys()}")


# Up scaling
s = 1E10  # scale up the data

for iset, set in enumerate(st_data):
    for jsubset, subset in enumerate(set):
        for name in ['I_x', 'I_y', 'I_p']:
            st_data[iset][jsubset][name] = subset[name]*s

# Saving the upscaled data

save_st(output_path, st_data)
# Results need to be copied over accordingly
