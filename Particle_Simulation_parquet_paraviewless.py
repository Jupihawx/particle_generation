# trace generated using paraview version 5.11.0-RC2
#import paraview
#paraview.compatibility.major = 5
#paraview.compatibility.minor = 11

import pandas as pd
import numpy as np
import os
import shutil
import time
import argparse
import pyvista as pv



parser = argparse.ArgumentParser(description='Particle simulation script.')
parser.add_argument("--id", help="Choose the id of the particle case to simulate.", type=int)
args = parser.parse_args()
current_case=args.id

current_case=0 ### A SUPPRIMER SUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMERSUPPRIMER
 

##### disable automatic camera reset on 'Show'

injection_data = pd.read_csv("./points_data.csv") # CSV with info about the injection and time simulation


injection_position=[int(injection_data.loc[current_case, 'center_x']),int(injection_data.loc[current_case, 'center_y']),int(injection_data.loc[current_case, 'center_z'])]

injection_radius=int(injection_data.loc[current_case, 'radius_points'])
injection_amount=int(injection_data.loc[current_case, 'number_points'])
coefficient_diffusion=float(injection_data.loc[current_case, 'diffCoeff'])



total_time=int(injection_data.loc[current_case, 'total_time'])
dt=int(injection_data.loc[current_case, 'dt'])

time_steps=total_time*dt

boundaries=[[-2000,2000],[-2000,2000],[0,600]] # Need to be entered by the user, it represents the boundary of the domain being simulated


current_time_file=open("./current_time.txt","r") # Used to select at what time the simulation starts, as well as showing the user the current time
current_time=int(current_time_file.read())


wind_direction=injection_data.loc[current_case,'Velocity direction']

grid = pv.read('test.vtk')




def moving_injection_position(destination_point, time): # Format imput : [[x y z t];[x1 y1 z1 t1]]
    return [int(injection_data.loc[current_case, 'center_x'])*(1-time)+destination_point[0]*time,int(injection_data.loc[current_case, 'center_y'])*(1-time)+destination_point[1]*time,int(injection_data.loc[current_case, 'center_z'])*(1-time)+destination_point[2]*time ]
        


def generate_init(center,radius,number_of_particles,current_case,current_time): # Used to generate the intial files

    path="./csv{0}".format(str(current_case))
    isExist= os.path.exists(path)
    if not isExist:
        os.makedirs(path)

    place_holder=np.ones((number_of_particles,3))

    positions=center*place_holder+radius*np.random.uniform(0,1,size=(number_of_particles,3)) # Generate the position of the particle being injected

    df_i = pd.DataFrame({"1": positions[:,0], # Necessary step when using parquet
                         "2": positions[:,1],
                         "3": positions[:,2]})

    pd.DataFrame(df_i).to_parquet('./csv{0}/particles_positions.parquet'.format(str(current_case)),index=None,compression=None) # Using parquet since it is way faster to write/read. Only issue is the need to compile your own version of paraview so the library pyarrow is included (venv)
    pd.DataFrame(df_i).to_parquet('./csv{0}/particles_positions_{1}.parquet'.format(str(current_case),str(current_time)),index=None,compression=None)



if current_time==0: #Only generate the starting position if the user generates new particles at time 0.
    generate_init(injection_position,injection_radius,injection_amount,current_case,current_time)


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

    indexes_outside_x=[i for i,v in enumerate(particles[:,0]) if limit_x[0] > v or v > limit_x[1]] # if bug, replace particles_to_check with particles
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






try:
    shutil.copyfile('./csv{1}/particles_positions_{0}.parquet'.format(current_time,current_case),'./csv{0}/particles_positions.parquet'.format(str(current_case))) # This copies the user displayed time as the current csv file, used for simulation when the user wants to continue the simulation that already have happenened
except:
    generate_init(injection_position,injection_radius,injection_amount,current_case,current_time) # In the case that the user creates a simulation at a time different than 0, but that there is no previous particles (case above)


position= pd.read_parquet("./csv{0}/particles_positions.parquet".format(str(current_case)))
position=position.to_numpy()
data=grid.probe(pv.PointSet(position)).point_data.get_array("U")
particles_out_of_bound=False


last_time=time.time()

target_point=[30,-300,300] # Modify this point if you want your injection to move linearly to this point

for i in range(current_time,total_time,dt): # Like so, only the time from the current paraview window will be modified

    live_time=time.time() #Below lines used to inform the user of the current progress of the simulation in the CLI
    if live_time-last_time >= 1 or i==total_time-dt:
        if i< total_time-dt:
            os.system('clear')
            print("Simulating from {1}s to {2}s. You can already display the particles in ParaView by clicking the start icon. \n Currently at {0}% ({3}s)".format((int((i-current_time)/((total_time-dt)-current_time)*100)), current_time, total_time, i*dt))
        else:
            os.system('clear')
            print("Simulation Done!")
        last_time=live_time



    updated_position=update_position(position,data,dt) # Update the positionn

    if i%dt*10==0 or particles_out_of_bound is True: # Checks every 10 time step or if a particle is detected. Helps to fasten the calculation when particles are still in the domain at the cost of a little blockage of 10 timesteps maximum at one point and once.
        updated_position, particles_out_of_bound=check_out_of_bounds(updated_position,boundaries,injection_amount)
    # If you have particle stuck at the exit, just modify check_out_of_bounds method to take into account more particles
 
    updated_position=brownian_motion(updated_position,coefficient_diffusion,dt) # Add the brownian motion to the simulated particles


    #new_points=generate_points(injection_position,injection_radius,injection_amount) # Generate new points
    new_points=generate_points(moving_injection_position(target_point,(i-current_time)*dt/(total_time-current_time)),injection_radius,injection_amount) # Generate new points. Use this line if you want the source to move, otherwise use the one above

    position=np.concatenate((updated_position,new_points)) # Add the new points to the existing ones

    df = pd.DataFrame({"1": position[:,0],
                         "2": position[:,1],
                         "3": position[:,2]})

    pd.DataFrame(df).to_parquet('./csv{0}/particles_positions.parquet'.format(str(current_case)),index=None,compression=None) # Write the file to parquet so it can be read by paraview


    shutil.copyfile("csv{0}/particles_positions.parquet".format(str(current_case)),"csv{1}/particles_positions_{0}.parquet".format(i,current_case)) # A bit faster than rewritting all


    ####### The method below is sub-optimal, because new proxies are being made and remove. But Paraview is stubborn and I could not find any workaround to update an existing source. Yet, this method is still faster than reading through CSV, even though the CSV reader do have a "Reload Files" method.



    #position= pd.read_parquet("./csv{0}/particles_positions.parquet")
    data=grid.probe(pv.PointSet(position)).point_data.get_array("U")


    #exec(open("./Particle_Simulation_parquet.py").read()) # Used to launch the code manually