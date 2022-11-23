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

injection_data = pd.read_csv("./points_data.csv") # data controlling the points

injection_position=[int(injection_data.loc[0, 'center_x']),int(injection_data.loc[0, 'center_y']),int(injection_data.loc[0, 'center_z'])]

injection_radius=int(injection_data.loc[0, 'radius_points'])
injection_amount=int(injection_data.loc[0, 'number_points'])
coefficient_diffusion=int(injection_data.loc[0, 'diffCoeff'])



total_time=int(injection_data.loc[0, 'total_time'])
dt=int(injection_data.loc[0, 'dt'])

time_steps=total_time*dt

boundaries=[[-2000,2000],[-2000,2000],[0,600]]


current_time_file=open("./current_time.txt","r")
current_time=int(current_time_file.read())


wind_direction=injection_data.loc[0,'Velocity direction']
afoam = XMLMultiBlockDataReader(registrationName='afoam', FileName=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/{0}deg.vtm'.format(wind_direction)]) # TO BE SELECTED FROM THE UI SLIDER
afoam.CellArrayStatus = ['U']
afoam.PointArrayStatus = ['U']



def generate_init(center,radius,number_of_particles):

    path="./csv"
    isExist= os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    place_holder=np.ones((number_of_particles,3))

    #positions=center*place_holder+radius*np.random.normal(0,1,size=(number_of_particles,3))
    positions=center*place_holder+radius*np.random.uniform(0,1,size=(number_of_particles,3))

    pd.DataFrame(positions).to_csv('csv/particles_positions.csv',header=False,index=False)
    pd.DataFrame(positions).to_csv('csv/particles_positions_0.csv',header=False,index=False)


if current_time==0: #Only generate the starting position if the user generates new particles at time 0.
    generate_init(injection_position,injection_radius,injection_amount)

# create a new 'CSV Reader'
particlescsv = CSVReader(registrationName='particles_positions.csv', FileName=['./csv/particles_positions.csv'])
particlescsv.HaveHeaders = 0



#================================================================
# addendum: following script captures some of the application
# state to faithfull
# find source
""" afoam = OpenFOAMReader(registrationName='a.foam', FileName='./a.foam')
afoam.MeshRegions = ['internalMesh']
afoam.CellArrays = ['U'] """




# create a new 'Table To Points'
tableToPoints1 = TableToPoints(registrationName='TableToPoints1', Input=particlescsv)
tableToPoints1.XColumn = 'Field 0'
tableToPoints1.YColumn = 'Field 1'
tableToPoints1.ZColumn = 'Field 2'

# create a new 'Resample With Dataset'
resampleWithDataset1 = ResampleWithDataset(registrationName='ResampleWithDataset1', SourceDataArrays=afoam,
    DestinationMesh=tableToPoints1)
resampleWithDataset1.CellLocator = 'Static Cell Locator'

def generate_points(center,radius,number_of_particles):

    place_holder=np.ones((number_of_particles,3))
    #positions=center*place_holder+radius*np.random.normal(0,1,size=(number_of_particles,3))
    positions=center*place_holder+radius*np.random.uniform(0,1,size=(number_of_particles,3))

    return positions




def update_position(position,velocity,timestep):
    new_position=position+velocity*timestep
    return new_position

def check_out_of_bounds(particles,limits,number_of_new_particles_per_timestep): #MODIFY THIS IN FUTURE TO READ FROM PARAVIEW THE BOUNDS
    particles_to_check=particles[number_of_new_particles_per_timestep:] # Checks only the number of new particles because they are the most likely to be outside of bounds, even though its not 100% they would get removed in the next few steps anyway.
    indexes=[]
    global particles_out_of_bound
    limit_x=limits[0]
    limit_y=limits[1]
    limit_z=limits[2]
    for index, particle in enumerate(particles_to_check):
        if limit_x[0]>particle[0] or particle[0]>limit_x[1] or limit_y[0]>particle[1] or particle[1]>limit_y[1] or limit_z[0]>particle[2] or particle[2]>limit_z[1]:
            indexes.append(index)
            particles_out_of_bound = True

    return np.delete(particles,indexes,0), particles_out_of_bound


def brownian_motion(particles,coefficient_diffusion,timestep):
    noise=np.sqrt(2*coefficient_diffusion*timestep)*np.random.normal(0,1,(len(particles),3))

    return particles+noise 



shutil.copyfile('./csv/particles_positions_{0}.csv'.format(current_time),'./csv/particles_positions.csv') # This copies the user displayed time as the current csv file, used for simulation

particlescsv = FindSource('particles_positions.csv')


vtk_data=sm.Fetch(resampleWithDataset1)
vtk_data = dsa.WrapDataObject(vtk_data)
data = vtk_data.PointData[0]
position= np.array(vtk_data.Points)
particles_out_of_bound=False


#ReplaceReaderFileName(afoam, ['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/avtm.vtm'], 'FileName')


for i in range(current_time,total_time,dt): # Like so, only the time from the current paraview window will be modified




    updated_position=update_position(position,data,dt)

    if i%10==0 or particles_out_of_bound is True: # Checks every 10 time step or if a particle is detected. Helps to fasten the calculation when particles are still in the domain at the cost of a little blockage of 10 timesteps maximum at one point and once.
        updated_position, particles_out_of_bound=check_out_of_bounds(updated_position,boundaries,injection_amount)
    # If you have particle stuck at the exit, just modify check_out_of_bounds method to take into account more particles




    updated_position=brownian_motion(updated_position,coefficient_diffusion,dt)


    new_points=generate_points(injection_position,injection_radius,injection_amount)



    position=np.concatenate((updated_position,new_points))

    pd.DataFrame(position).to_csv('csv/particles_positions.csv',header=False,index=False) # Here
 

    #pd.DataFrame(position).to_csv('csv/particles_position_{0}.csv'.format(i),header=False,index=False)
    shutil.copyfile("csv/particles_positions.csv","csv/particles_positions_{0}.csv".format(i)) # A bit faster than rewritting all


    ReloadFiles(particlescsv)

    #ReplaceReaderFileName(particlescsv, ['./csv/particle_position_{0}.csv'.format(i)], 'FileName')
    #particlescsv = FindSource('particle_position_{0}.csv'.format(i))


    vtk_data=sm.Fetch(resampleWithDataset1) # Here


    vtk_data = dsa.WrapDataObject(vtk_data)


    data = vtk_data.PointData[0]



    #exec(open("./Magic_Code_Threading.py").read())