HOW TO USE:

1_Launch pv_server (~/opt/ParaView-build/paraview_build/bin/pvserver --multi-clients) in multi clients mode
2_Connect your paraview GUI to the server (localhost)
3_ Launch the "UI_real_time_v2.py" with pvpython (must be the same build than the pvsserver). Enjoy!
    If you want faster calculcation, but not as fast reaction to parameters change, use UI_real_time_v2_thread.py
    To modify the number of thread, simply modify the value in "thread_management.py"



This needs to use a built version of paraview. To do so, follow the tutorial there: https://www.paraview.org/Wiki/ParaView:Build_And_Install

Then, create a virtual environment and install numpy and pyarrow: 

    virtualenv .venv
    source .venv/bin/activate
    pip install pyarrow
    pip install numpy


Then, create an environment variable for paraview  (https://discourse.paraview.org/t/quick-guide-to-using-pytorch-in-paraview/9037)

vi ~/.bash_profile
export PV_VENV=PATH/TO/.venv

export PV_VENV=PATH/TO/.venv


Then launch the built version of paraview to use the particle tracer.
Additionally, you need to modify the UI code so that it launches pvpython with your own built version.




V2_



sudo apt install python3-virtualenv
virtualenv paraview_env
source paraview_env/bin/activate


pip install pyarrow
deactivate

vEnv='/home/boris/environments/paraview_env/bin/activate_this.py'
exec(open(vEnv).read(), {'__file__': vEnv})

current_data=pd.read_parquet("./csv/particles_positions")


vEnv='~/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/.venv/bin'
exec(open(vEnv).read(), {'__file__': vEnv})


export PV_VENV=/home/boris/environments/venv

from paraview.web import venv





////////////// WORKING

- Download and install python3.9
- Create a virtualenv with python3.9 as executable, ex: virtualenv --python="/usr/bin/python3.9" "/home/boris/environments/paraviewvenv39"
- In pvpython and paraview, first import pandas and then launch the vEnv

virtualenv --python="/usr/bin/python3.9" "/home/boris/environments/paraviewvenv39"

import numpy as np
import pandas as pd

vEnv='/home/boris/environments/paraviewvenv39/bin/activate_this.py'
exec(open(vEnv).read(), {'__file__': vEnv})

import pyarrow

current_data=pd.read_parquet("./particles_positions_5.parquet")



//// WINDOWS


-Download and install python 3.9

 -Create a virtualenv and install pyarrow and fastparquet:

  python -m virtualenv -p="C:\Users\Boris\AppData\Local\Programs\Python\Python39\python.exe" "Path/to/venv"

  .\Scripts\Activate.ps1 

    pip install numpy, pyarrow, pandas, fastparquet


Create an environment variable : PV_VENV="Path/to/venv"

#vEnv='C:/Users/Boris/Desktop/Particles_simulation/virtualenv39/Scripts/activate_this.py'
#exec(open(vEnv).read(), {'__file__': vEnv})



https://linuxize.com/post/how-to-install-python-3-9-on-ubuntu-20-04/

https://stackoverflow.com/questions/24123150/pyvenv-3-4-returned-non-zero-exit-status-1

https://kitware.github.io/trame/docs/tutorial-paraview.html

