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
import time
import builtins
from pandas.util import hash_pandas_object

while True: # The code is running constantly, either because then pvpython does not have to boot-up again and its faster


    try:
        coms = pd.read_csv("front_end_back_end_communication.csv")
        shutil.rmtree('./csv0') # Remove current solution to free up space and avoid any interference between runs
    except:
        pass

    simulation_requested=coms.loc[0, 'simulation requested']# Checks when the UI requests a simulation, since the code is constantly running in a thread, this allows to launch easily

    if simulation_requested==1: # When the UI sends a notification to this code to run.
        coms.loc[0, 'simulation requested'] = 0 # write 0, meaning the code did read the request for simulation and will run
        coms.to_csv("front_end_back_end_communication.csv", index=False)

        current_case=0

        try: # Free up memory from previous run
            Delete(programmableSource1)
            Delete(tableToPoints1)
            Delete(resampleWithDataset1)
            Delete(afoam)
        except:
            pass


        ##### disable automatic camera reset on 'Show'
        paraview.simple._DisableFirstRenderCameraReset()

        injection_data = pd.read_csv("./points_data.csv") # CSV with info about the injection and time simulation
        injection_position=[int(injection_data.loc[current_case, 'center_x']),int(injection_data.loc[current_case, 'center_y']),int(injection_data.loc[current_case, 'center_z'])]
        injection_radius=int(injection_data.loc[current_case, 'radius_points'])
        injection_amount=int(injection_data.loc[current_case, 'number_points'])
        coefficient_diffusion=float(injection_data.loc[current_case, 'diffCoeff'])

        total_time=int(coms.loc[0, 'max time'])+500 # ARBITRARY, BASICALLY THE SIMULATION WILL RUN UP TO 500 STEPS AFTER THE LATEST TIME DISPLAYED (kind of a buffer)

        
        dt=int(injection_data.loc[current_case, 'dt'])
        time_steps=total_time*dt

        boundaries=[[-2000,2000],[-2000,2000],[0,600]] # Need to be entered by the user, it represents the boundary of the domain being simulated

        current_time_file=open("./current_time_vizu.txt","r") # Used so that the back-end (this code), knows what what time it is in the paraview viewer.
        current_time=int(current_time_file.read())
        current_time_file.close()


        simulated_ang=["0" ,"0.3307", "0.6614" , "0.9921" ,  "1.3228" , "1.6535"  , "1.9842"  , "2.3149"  , "2.6456" ,  "2.9762" , "3.3069", "3.6376 " ,   "3.9683"  ,  "4.2990" ,   "4.6297", " 4.9604", "5.2911"  ,  "5.6218"  ,  "5.9525"] # ! Case 3.6 et 4.9 missing because problem in the sim??
        simulated_ang = [int(eval(i)*180/np.pi) for i in simulated_ang] # Convert to °
        simulated_vel=[5, 10, 15]



        wind_direction=injection_data.loc[current_case,'Velocity direction']
        wind_value=injection_data.loc[current_case,'Velocity magnitude']

        if wind_direction not in simulated_ang: # Simple condition to have the current velocity input from the UI actually snap to the closest actual velocity simulation from the simulation
            wind_direction=simulated_ang[builtins.min(range(len(simulated_ang)), key = lambda i: abs(simulated_ang[i]-wind_direction))]

        if wind_value not in simulated_vel: # Simple condition to have the current velocity input from the UI actually snap to the closest actual velocity simulation from the simulation
            wind_value=simulated_vel[builtins.min(range(len(simulated_vel)), key = lambda i: abs(simulated_vel[i]-wind_value))]


        afoam = XMLMultiBlockDataReader(registrationName='afoam', FileName=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/cases/val_{0}_ang_{1}.vtm'.format(int(wind_value),int(wind_direction))]) # Depending on the slider position, the simulator with select a vtm file representing the field at that given angle
        afoam.CellArrayStatus = ['U']
        afoam.PointArrayStatus = ['U']



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
            pd.DataFrame(df_i).to_parquet('./csv{0}/particles_positions_0.parquet'.format(str(current_case)),index=None,compression=None) # Using parquet since it is way faster to write/read. Only issue is the need to compile your own version of paraview so the library pyarrow is included (venv)
            pd.DataFrame(df_i).to_parquet('./csv{0}/particles_positions_{1}.parquet'.format(str(current_case),str(current_time)),index=None,compression=None)



        if current_time==0: #Only generate the starting position if the user generates new particles at time 0.
            generate_init(injection_position,injection_radius,injection_amount,current_case,current_time)

        programmableSource1 = ProgrammableSource(registrationName='ProgrammableSource1') # This source represents the "reader" of the parquet files. Themselves being the positions of the particles at a given time
        programmableSource1.OutputDataSetType = 'vtkTable'
        programmableSource1.Script = """
import numpy as np
import pandas as pd

data = pd.read_parquet("./csv{0}/particles_positions.parquet")

output.RowData.append(data.values[:,0], "X")
output.RowData.append(data.values[:,1], "Y")
output.RowData.append(data.values[:,2], "Z")
        """.format(str(current_case))


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

        def clean_particles(): # Simply calculate the new position.
            empty_particles_array=np.empty((1,3))
            return empty_particles_array


        def update_position(position,velocity,timestep): # Simply calculate the new position.
            position, velocity = check_stuck_particles(position,velocity)
            new_position=position+velocity*timestep
            return new_position

        def check_stuck_particles(position,velocity): # Function to check if particles are stuck somewhere (V +- 0) and delete them
            norm_velocity=np.linalg.norm(velocity,axis=1)
            indexes_stuck=[i for i,v in enumerate(norm_velocity) if v < 1e-3]

            if indexes_stuck:
                return np.delete(position,indexes_stuck,0),np.delete(velocity,indexes_stuck,0)
            else:
                return position, velocity

            # __DEPRECATED__.It seems like the condition to check if particles are stuck (Speed +- 0) also allows to target particles that are out of bound, and thus this method is deprecated
        def check_out_of_bounds(particles,limits,number_of_new_particles_per_timestep): # This is used to calculate if a particle is out of the bounds or not. It is extra computing power, but in the case particles are exiting, it helps the simulation since they are removed.
            indexes=[]
            global particles_out_of_bound
            limit_x=limits[0]
            limit_y=limits[1]
            limit_z=limits[2]

            indexes_outside_x=[i for i,v in enumerate(particles[:,0]) if limit_x[0] + limit_x[0]*0.05  > v or v > limit_x[1] - limit_x[1]*0.05] # changed 5% on the dimensions to make sure the particules are removed.
            indexes_outside_y=[i for i,v in enumerate(particles[:,1]) if limit_y[0] + limit_y[0]*0.05  > v or v > limit_y[1] - limit_y[1]*0.05]
            indexes_outside_z=[i for i,v in enumerate(particles[:,2]) if limit_z[0] + limit_z[0]*0.05  > v or v > limit_z[1] - limit_z[1]*0.05]

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





        ##### INITIALIZE


        generate_init(injection_position,injection_radius,injection_amount,current_case,current_time) 

        vtk_data=sm.Fetch(resampleWithDataset1) # This is the key commmand that gets the info from paraview, but also the slowest in this script since it calls for UpdatePipeline() in the client side of paraview, which takes time and explain why the code is not fully real time.
        vtk_data = dsa.WrapDataObject(vtk_data)
        data = vtk_data.PointData[0]
        position= np.array(vtk_data.Points)
        particles_out_of_bound=False


        last_time=time.time()

        #target_point=[30,-300,300] # Modify this point if you want your injection to move linearly to this point

        for i in range(0,total_time,dt): # Create "fake" files that are mostly empty, not necessary but nice to have so that even if somehow paraview displays a case not yet generated, there will be no error message
            shutil.copyfile("csv{0}/particles_positions.parquet".format(str(current_case)),"csv{1}/particles_positions_{0}.parquet".format(i,current_case)) 

        i=0
        checker_com=hash_pandas_object(coms)
        checker_injection=hash_pandas_object(injection_data)
        p_checker_com=checker_com
        p_checker_injection=checker_injection


        ##### LAUNCH THE SIMULATION 

        while True: 

            try: # This loops checks if info inputed by the user changed, and does the modification. This only happens in the case of that the simulation is over, and that the script is waiting for another user input. If the data is modified during the simulation, it is handled below.
                coms = pd.read_csv("front_end_back_end_communication.csv") #
                injection_data = pd.read_csv("./points_data.csv") # CSV with info about the injection and time simulation
                total_time=int(coms.loc[0, 'max time'])+500 # ARBITRARY, BASICALLY THE SIMULATION WILL RUN UP TO 500 STEPS AFTER THE LATEST TIME DISPLAYED (kind of a buffer)

                checker_com=hash_pandas_object(coms)
                checker_injection=hash_pandas_object(injection_data)


                if checker_com.iloc[0] != p_checker_com.iloc[0] or checker_injection.iloc[0] != p_checker_injection.iloc[0]: # Checks the hash of the file to see if any change was made. If so, the simulation goes back to the given time where the change has been made and relaunch the calculations
                    i=i-1 
                    if i<0:
                        i=0
                    p_checker_com=checker_com
                    p_checker_injection=checker_injection

            except:
                pass




        ##### LAUNCH THE CALCULATIONS
         
            while i < total_time: # The real time simulation mode will run until i reaches the specified time total_time. It is useful to have a long time so that the simulation never really stops.

                ### This part checks if any modification happened in the UI ###

                current_time_simulated_file= open("./current_time_simulated.txt","r+") 
                current_time_simulated_file.truncate(0)
                current_time_simulated_file.write(str(i)) # Writes at what time the current simulation is. This will then be used by paraview to know if Paraview displays too fast with respect to the simulation (if it is the case, paraview will pause for a second to let the simulation have some advance)
                current_time_simulated_file.close()

                p_wind_direction=wind_direction
                p_injection_position=injection_position
                p_injection_radius=injection_radius
                p_injection_amount=injection_amount
                p_coefficient_diffusion = coefficient_diffusion
                p_wind_value=wind_value

                while True: # This loop is just used due to threading issues that can arise. Basically the code reads really fast the csv file, but when the user modifies it, it can happen that it reads a file being saved, hence creating an error. With this method, the program will retry until there is no error.
                    try:         # Read all the values
                        current_time_file=open("./current_time_vizu.txt","r") # Used to select at what time the simulation starts, as well as showing the user the current time
                        current_time=int(current_time_file.read())
                        current_time_file.close()

                        coms = pd.read_csv("front_end_back_end_communication.csv") # For later use
                    
                        injection_data = pd.read_csv("./points_data.csv") # CSV with info about the injection and time simulation
                        injection_position=[int(injection_data.loc[current_case, 'center_x']),int(injection_data.loc[current_case, 'center_y']),int(injection_data.loc[current_case, 'center_z'])]
                        injection_radius=int(injection_data.loc[current_case, 'radius_points'])
                        injection_amount=int(injection_data.loc[current_case, 'number_points'])
                        coefficient_diffusion=float(injection_data.loc[current_case, 'diffCoeff'])

                        wind_direction=injection_data.loc[current_case,'Velocity direction']
                        wind_value=injection_data.loc[current_case,'Velocity magnitude']

                    except:
                        continue # If error, try again
                    break # If not, continue


                if wind_direction not in simulated_ang: # Simple condition to have the current velocity input from the UI actually snap to the closest actual velocity simulation from the simulation
                    wind_direction=simulated_ang[builtins.min(range(len(simulated_ang)), key = lambda i: abs(simulated_ang[i]-wind_direction))]

                if wind_value not in simulated_vel: # Simple condition to have the current velocity input from the UI actually snap to the closest actual velocity simulation from the simulation
                    wind_value=simulated_vel[builtins.min(range(len(simulated_vel)), key = lambda i: abs(simulated_vel[i]-wind_value))]


                #Below, if a difference is noted between what is currently simulated and what the user input, we need the simulation to go back to the time at which the user is currently to re-do the simulation. Because the simulation does not wait for the paraview time to compute (which makes more sense), it needs to come back in time to simulate the change at the right time
                if p_wind_direction != wind_direction or p_injection_amount != injection_amount or p_injection_radius != injection_radius or p_injection_position != injection_position or p_coefficient_diffusion != coefficient_diffusion or p_wind_value != wind_value:
                    Delete(afoam)
                    i=current_time  # Simulate in advance. Creates a small delay in the vizualization, but is beneficial since it gives a small head-start to the backend
                    afoam = XMLMultiBlockDataReader(registrationName='afoam', FileName=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/cases/val_{0}_ang_{1}.vtm'.format(int(wind_value),int(wind_direction))]) # Depending on the slider position, the simulator with select a vtm file representing the field at that given angle
                    afoam.CellArrayStatus = ['U']
                    afoam.PointArrayStatus = ['U']
                    shutil.copyfile("csv{1}/particles_positions_{0}.parquet".format(i,current_case),"csv{0}/particles_positions.parquet".format(str(current_case))) # Copy the requested time as the current time
        
                    position=pd.read_parquet("csv{0}/particles_positions.parquet".format(str(current_case)))  # Now, we "came back" in time and ready to re-simulate the simulation with the new parameters, at the correct time
                    position=position.to_numpy()



                ### This part creates the paraview tools to calculate the velocity at given probe points (paraview side) ###

                #Below, do all the pvpython side of thing to find the U vector for each position. The filters are deleted and re-added because otherwise paraview does no seems to update the value.
                #The method below is sub-optimal, because new proxies are being made and remove. But Paraview is stubborn and I could not find any workaround to update an existing source. Yet, this method is still faster than reading through CSV, even though the CSV reader do have a "Reload Files" method.

                Delete(programmableSource1)
                Delete(tableToPoints1)
                Delete(resampleWithDataset1)

                
                programmableSource1 = ProgrammableSource(registrationName='ProgrammableSource1')
                programmableSource1.OutputDataSetType = 'vtkTable'
                programmableSource1.Script = """
    import numpy as np
    import pandas as pd

    data = pd.read_parquet("./csv{0}/particles_positions.parquet")

    output.RowData.append(data.values[:,0], "X")
    output.RowData.append(data.values[:,1], "Y")
    output.RowData.append(data.values[:,2], "Z")
                """.format(str(current_case))

                
                tableToPoints1 = TableToPoints(registrationName='TableToPoints1', Input=programmableSource1)
                tableToPoints1.XColumn = 'X'
                tableToPoints1.YColumn = 'Y'
                tableToPoints1.ZColumn = 'Z'

                # create a new 'Resample With Dataset'
                resampleWithDataset1 = ResampleWithDataset(registrationName='ResampleWithDataset1', SourceDataArrays=afoam,
                    DestinationMesh=tableToPoints1)
                resampleWithDataset1.CellLocator = 'Static Cell Locator'
                

                vtk_data=sm.Fetch(resampleWithDataset1) 

                vtk_data = dsa.WrapDataObject(vtk_data)

                data = vtk_data.PointData[0] # Way of probing in paraview


                ### This part creates calculates the position from the probed points above (python side) and writes it down to parquet files ###


                updated_position=update_position(position,data,dt) # Update the position

                # It seems like the condition to check if particles are stuck (Speed +- 0) also allows to target particles that are out of bound, and thus this method is deprecated
                """ if i%dt*10==0 or particles_out_of_bound is True: # Checks every 10 time step or if a particle is detected. Helps to fasten the calculation when particles are still in the domain at the cost of a little blockage of 10 timesteps maximum at one point and once.
                    updated_position, particles_out_of_bound=check_out_of_bounds(updated_position,boundaries,injection_amount)
                # If you have particle stuck at the exit, just modify check_out_of_bounds method to take into account more particles
            """
                updated_position=brownian_motion(updated_position,coefficient_diffusion,dt) # Add the brownian motion to the simulated particles


                new_points=generate_points(injection_position,injection_radius,injection_amount) # Generate new points
                #new_points=generate_points(moving_injection_position(target_point,(i-current_time)*dt/(total_time-current_time)),injection_radius,injection_amount) # Generate new points. Use this line if you want the source to move, otherwise use the one above

                position=np.concatenate((updated_position,new_points)) # Add the new points to the existing ones



                df = pd.DataFrame({"1": position[:,0],
                                    "2": position[:,1],
                                    "3": position[:,2]})

                pd.DataFrame(df).to_parquet('./csv{0}/particles_positions.parquet'.format(str(current_case)),index=None,compression=None) # Write the file to parquet so it can be read by paraview


                shutil.copyfile("csv{0}/particles_positions.parquet".format(str(current_case)),"csv{1}/particles_positions_{0}.parquet".format(i,current_case)) # A bit faster than rewritting all


                ### This part prints for the user information ###

                live_time=time.time() #Below lines used to inform the user of the current progress of the simulation in the CLI
                if live_time-last_time >= 1 or i==total_time-dt:
                    if i< total_time-dt:
                        os.system('clear')
                        print("Current wind direction : {0}°, and velocity : {1} m/s".format(wind_direction, wind_value))
                        print("Current injection position : {0}".format(injection_position))
                        print("Injecting {0} particle per seconds, within a radius of {1} m and a diffusion coefficient of {2} ".format(injection_amount, injection_radius, coefficient_diffusion))

                        print("Simulation Currently at {0}s".format((i*dt)))
                    else:
                        os.system('clear')
                        print("Simulation Done!")
                    last_time=live_time

            
                ### This part checks if the user asked to clean the particles, and does so if asked ###

                if coms.loc[0, 'clean particles'] == 1:# Checks when the UI requests asks to delete the particles
                    print("PARTICLES CLEANED")
                    position=clean_particles()
                    i=current_time
                    df = pd.DataFrame()

                    pd.DataFrame(df).to_parquet('./csv{0}/particles_positions.parquet'.format(str(current_case)),index=None,compression=None) # Write the file to parquet so it can be read by paraview
                    shutil.copyfile("csv{0}/particles_positions.parquet".format(str(current_case)),"csv{1}/particles_positions_{0}.parquet".format(i,current_case)) # A bit faster than rewritting all

                    coms.loc[0, 'clean particles'] = 0 # write 0, meaning the code did read 
                    coms.to_csv("front_end_back_end_communication.csv", index=False)


                i=i+1
                # DEPRECATED, but can be used to pause the simulation if needed.
                #while coms.loc[0, 'pause'] == 1:# Checks when the UI requests asks pause the simulation. 
                while False:# due to deprecated function just above

                    try:
                        coms = pd.read_csv("front_end_back_end_communication.csv")
                    except:
                        continue
                    continue



