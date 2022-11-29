# trace generated using paraview version 5.11.0-RC2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

from paraview.simple import *
from paraview.vtk.numpy_interface import dataset_adapter as dsa
from paraview import servermanager as sm
import pandas as pd
import numpy as np
import os
import shutil

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

injection_data = pd.read_csv("./points_data.csv") # CSV with info about the injection and time simulation

injection_position=[int(injection_data.loc[0, 'center_x']),int(injection_data.loc[0, 'center_y']),int(injection_data.loc[0, 'center_z'])]

injection_radius=int(injection_data.loc[0, 'radius_points'])
injection_amount=int(injection_data.loc[0, 'number_points'])
coefficient_diffusion=float(injection_data.loc[0, 'diffCoeff'])



total_time=int(injection_data.loc[0, 'total_time'])
dt=int(injection_data.loc[0, 'dt'])

time_steps=total_time*dt

boundaries=[[-2000,2000],[-2000,2000],[0,600]] # Need to be entered by the user, it represents the boundary of the domain being simulated


current_time_file=open("./current_time.txt","r") # Used to select at what time the simulation starts, as well as showing the user the current time
current_time=int(current_time_file.read())


wind_direction=injection_data.loc[0,'Velocity direction']

afoam = XMLMultiBlockDataReader(registrationName='afoam', FileName=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/{0}deg.vtm'.format(wind_direction)]) # Depending on the slider position, the simulator with select a vtm file representing the field at that given angle
afoam.CellArrayStatus = ['U']
afoam.PointArrayStatus = ['U']



def generate_init(center,radius,number_of_particles): # Used to generate the intial files

    path="./csv"
    isExist= os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    place_holder=np.ones((number_of_particles,3))

    positions=center*place_holder+radius*np.random.uniform(0,1,size=(number_of_particles,3)) # Generate the position of the particle being injected

    df_i = pd.DataFrame({"1": positions[:,0], # Necessary step when using parquet
                         "2": positions[:,1],
                         "3": positions[:,2]})

    pd.DataFrame(df_i).to_parquet('./csv/particles_positions.parquet',index=None,compression=None) # Using parquet since it is way faster to write/read. Only issue is the need to compile your own version of paraview so the library pyarrow is included (venv)
    pd.DataFrame(df_i).to_parquet('./csv/particles_positions_0.parquet',index=None,compression=None)



if current_time==0: #Only generate the starting position if the user generates new particles at time 0.
    generate_init(injection_position,injection_radius,injection_amount)

programmableSource1 = ProgrammableSource(registrationName='ProgrammableSource1') # This source represents the "reader" of the parquet files. Themselves being the positions of the particles at a given time
programmableSource1.OutputDataSetType = 'vtkTable'
programmableSource1.Script = """import numpy as np
import pandas as pd

data = pd.read_parquet("./csv/particles_positions.parquet")

output.RowData.append(data.values[:,0], "X")
output.RowData.append(data.values[:,1], "Y")
output.RowData.append(data.values[:,2], "Z")
"""


# create a new 'Table To Points'
tableToPoints1 = TableToPoints(registrationName='TableToPoints1', Input=programmableSource1) # The table to points converts the source above into something usable by paraview
tableToPoints1.XColumn = 'X'
tableToPoints1.YColumn = 'Y'
tableToPoints1.ZColumn = 'Z'

# create a new 'Resample With Dataset'
resampleWithDataset1 = ResampleWithDataset(registrationName='ResampleWithDataset1', SourceDataArrays=afoam, # This filter takes the particles and the field as input, and outputs the velocity of each particle. This is the main usage of paraview for getting the velocity at a given point, but it would be nice in the future to have another more efficient program to do so.
    DestinationMesh=tableToPoints1)
resampleWithDataset1.CellLocator = 'Static Cell Locator'

def generate_points(center,radius,number_of_particles): # Used to generate new points at the injection

    place_holder=np.ones((number_of_particles,3))
    #positions=center*place_holder+radius*np.random.normal(0,1,size=(number_of_particles,3)) # Either normal distribution injection, or uniform
    positions=center*place_holder+radius*np.random.uniform(0,1,size=(number_of_particles,3))

    return positions




def update_position(position,velocity,timestep): # Simply calculate the new position.
    new_position=position+velocity*timestep
    return new_position

def check_out_of_bounds(particles,limits,number_of_new_particles_per_timestep): # This is used to calculate if a particle is out of the bounds or not. It is extra computing power, but in the case particles are exiting, it helps the simulation since they are removed.
    particles_to_check=particles[number_of_new_particles_per_timestep*5:] # Checks only the number of new particles because they are the most likely to be outside of bounds, even though its not 100% they would get removed in the next few steps anyway.
    indexes=[]
    global particles_out_of_bound
    limit_x=limits[0]
    limit_y=limits[1]
    limit_z=limits[2]

    indexes_outside_x=[i for i,v in enumerate(particles[:,0]) if limit_x[0] > v or v > limit_x[1]]
    indexes_outside_y=[i for i,v in enumerate(particles[:,1]) if limit_y[0] > v or v > limit_y[1]]
    indexes_outside_z=[i for i,v in enumerate(particles[:,2]) if limit_z[0] > v or v > limit_z[1]]

    indexes=np.concatenate((indexes_outside_x,indexes_outside_y,indexes_outside_z), axis=0)

    if indexes.any():
        indexes=indexes.astype(int)
        particles_out_of_bound = True # This value is used below, so that we do not check every timestep if particles are out, until one is actually out
        return np.delete(particles,indexes,0), particles_out_of_bound
    else:
        return particles, particles_out_of_bound



def brownian_motion(particles,coefficient_diffusion,timestep): # Simple generation of noise through brownian motion
    noise=np.sqrt(2*coefficient_diffusion*timestep)*np.random.normal(0,1,(len(particles),3))

    return particles+noise 



shutil.copyfile('./csv/particles_positions_{0}.parquet'.format(current_time),'./csv/particles_positions.parquet') # This copies the user displayed time as the current csv file, used for simulation


vtk_data=sm.Fetch(resampleWithDataset1) # This is the key commmand that gets the info from paraview, but also the slowest in this script since it calls for UpdatePipeline() in the client side of paraview, which takes time and explain why the code is not fully real time.
vtk_data = dsa.WrapDataObject(vtk_data)
data = vtk_data.PointData[0]
position= np.array(vtk_data.Points)
particles_out_of_bound=False


for i in range(current_time,total_time,dt): # Like so, only the time from the current paraview window will be modified


    updated_position=update_position(position,data,dt) # Update the positionn

    if i%dt*10==0 or particles_out_of_bound is True: # Checks every 10 time step or if a particle is detected. Helps to fasten the calculation when particles are still in the domain at the cost of a little blockage of 10 timesteps maximum at one point and once.
        updated_position, particles_out_of_bound=check_out_of_bounds(updated_position,boundaries,injection_amount)
    # If you have particle stuck at the exit, just modify check_out_of_bounds method to take into account more particles
 
    updated_position=brownian_motion(updated_position,coefficient_diffusion,dt) # Add the brownian motion to the simulated particles


    new_points=generate_points(injection_position,injection_radius,injection_amount) # Generate new points


    position=np.concatenate((updated_position,new_points)) # Add the new points to the existing ones

    df = pd.DataFrame({"1": position[:,0],
                         "2": position[:,1],
                         "3": position[:,2]})

    pd.DataFrame(df).to_parquet('./csv/particles_positions.parquet',index=None,compression=None) # Write the file to parquet so it can be read by paraview


    shutil.copyfile("csv/particles_positions.parquet","csv/particles_positions_{0}.parquet".format(i)) # A bit faster than rewritting all


    ####### The method below is sub-optimal, because new proxies are being made and remove. But Paraview is stubborn and I could not find any workaround to update an existing source. Yet, this method is still faster than reading through CSV, even though the CSV reader do have a "Reload Files" method.

    Delete(programmableSource1)
    Delete(tableToPoints1)
    Delete(resampleWithDataset1)


    programmableSource1 = ProgrammableSource(registrationName='ProgrammableSource1')
    programmableSource1.OutputDataSetType = 'vtkTable'
    programmableSource1.Script = """
    import numpy as np
    import pandas as pd

    data = pd.read_parquet("./csv/particles_positions.parquet")

    output.RowData.append(data.values[:,0], "X")
    output.RowData.append(data.values[:,1], "Y")
    output.RowData.append(data.values[:,2], "Z")
    """


    tableToPoints1 = TableToPoints(registrationName='TableToPoints1', Input=programmableSource1)
    tableToPoints1.XColumn = 'X'
    tableToPoints1.YColumn = 'Y'
    tableToPoints1.ZColumn = 'Z'

    # create a new 'Resample With Dataset'
    resampleWithDataset1 = ResampleWithDataset(registrationName='ResampleWithDataset1', SourceDataArrays=afoam,
        DestinationMesh=tableToPoints1)
    resampleWithDataset1.CellLocator = 'Static Cell Locator'
    
    ###########


    vtk_data=sm.Fetch(resampleWithDataset1) 

    vtk_data = dsa.WrapDataObject(vtk_data)

    data = vtk_data.PointData[0]


    #exec(open("./Particle_Simulation_parquet.py").read()) # Used to launch the code manually