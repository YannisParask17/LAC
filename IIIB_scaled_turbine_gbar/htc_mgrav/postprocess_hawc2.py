# -*- coding: utf-8 -*-
"""Post-process a selection of HAWC2 files run on the cluster.
"""
from pathlib import Path

from lacbox.postprocess import process_statistics


# inputs
res_dir = Path('mgrav_res')  # directory with res files to process
calc_del = True  # calculate DELs in the statistics? It takes longer.
# save_path = './notilt/iiib_scaled_turbine_steady_stats.csv'  # where should I save the stats file?
save_path = 'mgrav_res.csv'  # where should I save the stats file?

# call the function
stats_df = process_statistics(res_dir, save_path)
