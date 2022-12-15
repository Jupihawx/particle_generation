This needs to use a built version of paraview. To do so, follow the tutorial there: https://www.paraview.org/Wiki/ParaView:Build_And_Install

Then, create a virtual environment and install numpy and pyarrow: 

    virtualenv .venv
    source .venv/bin/activate
    pip install pyarrow
    pip install numpy


Then, create an environment variable for paraview 

vi ~/.bash_profile
export PV_VENV=PATH/TO/.venv

export PV_VENV=PATH/TO/.venv


Then launch the built version of paraview to use the particle tracer.
Additionally, you need to modify the UI code so that it launches pvpython with your own built version.