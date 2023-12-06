# -*- coding: utf-8 -*-
"""Make folders with both steady and turbulent set-ups.
"""
from pathlib import Path

from lacbox.htc import make_steady, make_turb


# path to master (TURBULENT!) htc file and range of wind speeds of interest
htc_path = Path('htc_master/scaled_turbine_turb_copy_old.htc')
wsps = range(5, 25)


# =======================================================================================
# CASE 1: Steady with, no tower shadow, no shear.

htc_dir = Path('./htc_steady/')
res_dir = './res_steady/'

# 1a: With normal tilt

tilt = None
subfolder = 'tilt'

basename = f'iiib_scaled_turbine_{subfolder}'
make_steady(htc_path, wsps, tilt=tilt, htc_dir=htc_dir, res_dir=res_dir,
            basename=basename, subfolder=subfolder, clean_htc=True)

# 1b: Without tilt

tilt = 0
subfolder = 'notilt'

basename = f'iiib_scaled_turbine_{subfolder}'
make_steady(htc_path, wsps, tilt=tilt, htc_dir=htc_dir, res_dir=res_dir,
            basename=basename, subfolder=subfolder)

# 1c: Without tilt, rigid tower/blades

tilt = 0
subfolder = 'notiltrigid'

basename = f'iiib_scaled_turbine_{subfolder}'
make_steady(htc_path, wsps, tilt=tilt, htc_dir=htc_dir, res_dir=res_dir,
            basename=basename, subfolder=subfolder, rigid=True)

# 1d: Without tilt or drag, rigid tower/blades

tilt = 0
subfolder = 'notiltnodragrigid'

basename = f'iiib_scaled_turbine_{subfolder}'
make_steady(htc_path, wsps, tilt=tilt, htc_dir=htc_dir, res_dir=res_dir,
            basename=basename, subfolder=subfolder, rigid=True, withdrag=False)

# =======================================================================================
# CASE 2: Turbulent wind.

htc_dir = Path('./htc_turb/')
res_dir = './res_turb/'

# 2a: Class A

# subfolder = 'tca'
# turbclass = 'A'

# basename = f'iiib_scaled_turbine_turb_{subfolder}'
# make_turb(htc_path, wsps, turbclass, htc_dir=htc_dir, res_dir=res_dir,
#           subfolder=subfolder, basename=basename, seed=1337, clean_htc=True)

# 2b: Class B

subfolder = 'tcb'
turbclass = 'B'

basename = f'iiib_scaled_turbine_turb_{subfolder}'
make_turb(htc_path, wsps, turbclass, htc_dir=htc_dir, res_dir=res_dir,
          subfolder=subfolder, basename=basename, seed=42)
