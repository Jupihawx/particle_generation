import threading
import os
import glob
import pandas as pd
import shutil
import time

number_of_threads=4

def unique_thread_simulation(thread_number, thread_id):
        os.system("/home/boris/opt/ParaView-build/paraview_build/bin/pvpython Particle_Simulation_parquet_real_time_v2_unique_thread.py --thread_number {0} --thread_id {1}".format(thread_number,thread_id))

current_time_simulated_file= open("./current_time_simulated.txt","r+") # Re initialize, better safe than sorry
current_time_simulated_file.truncate(0)
current_time_simulated_file.write(str(0)) 
current_time_simulated_file.close()


t=[]
for i in range(number_of_threads): # Launch each thread with the right argument
    t.append(threading.Thread(target=unique_thread_simulation, args=(number_of_threads, i)))
    t[i].start()


i=0
wind_direction=0
injection_position=0
injection_radius=0
injection_amount=0
coefficient_diffusion = 0
wind_value=0


while True:


    ## First, like the simulation, check if there is no change on the UI. If there is, come back in time in the simulation to re-simulate at the time the UI have been modified by the user
    p_wind_direction=wind_direction
    p_injection_position=injection_position
    p_injection_radius=injection_radius
    p_injection_amount=injection_amount
    p_coefficient_diffusion = coefficient_diffusion
    p_wind_value=wind_value

    while True:
        try:         # Read all the values
            current_time_file=open("./current_time_vizu.txt","r") # Used to select at what time the simulation starts, as well as showing the user the current time
            current_time=int(current_time_file.read())
            current_time_file.close()

            coms = pd.read_csv("front_end_back_end_communication.csv") 
        
            injection_data = pd.read_csv("./points_data.csv") # CSV with info about the injection and time simulation
            injection_position=[int(injection_data.loc[0, 'center_x']),int(injection_data.loc[0, 'center_y']),int(injection_data.loc[0, 'center_z'])]
            injection_radius=int(injection_data.loc[0, 'radius_points'])
            injection_amount=int(injection_data.loc[0, 'number_points'])
            coefficient_diffusion=float(injection_data.loc[0, 'diffCoeff'])
            particle_request=int(coms.loc[0, 'clean particles'])

            wind_direction=injection_data.loc[0,'Velocity direction']
            wind_value=injection_data.loc[0,'Velocity magnitude']

        except:
            continue # If error, try again
        break # If not, continue



    if p_wind_direction != wind_direction or p_injection_amount != injection_amount or p_injection_radius != injection_radius or p_injection_position != injection_position or p_coefficient_diffusion != coefficient_diffusion or p_wind_value != wind_value:
        i=current_time  
        current_time_simulated_file= open("./current_time_simulated.txt","r+") 
        current_time_simulated_file.truncate(0)
        current_time_simulated_file.write(str(i)) # Writes at what time the current simulation is. 
        current_time_simulated_file.close()
        time.sleep(0.2) # Wait a bit so that the individual thread have time to themselves re-simulate a few cases

    if particle_request==1:
        i=current_time  
        current_time_simulated_file= open("./current_time_simulated.txt","r+") 
        current_time_simulated_file.truncate(0)
        current_time_simulated_file.write(str(i)) 
        current_time_simulated_file.close()
        time.sleep(1) # Wait a bit so that the individual thread have time to themselves re-simulate a few cases
        

    filelist = glob.glob('csv0/particles_positions_{0}_t*.parquet'.format(str(i))) # Checks how many files of index i are existing. 
    
    if len(filelist) == number_of_threads: # If there is as many files as thread, it means each thread finished its job and that the current code can aggregate the data to a single file for the vizualisation to be done

        data=[]
        for file in filelist: # append the data of each sub-file together
            value=pd.DataFrame(pd.read_parquet(file).values)
            data.append(value)
        
        data=pd.concat(data)
        
        treated_data = pd.DataFrame({"1": data.iloc[:,0], # Necessary step when using parquet
                            "2": data.iloc[:,1],
                            "3": data.iloc[:,2]})



        treated_data.to_parquet('./csv0/particles_positions_{0}.parquet'.format(str(i)),index=None,compression=None) # Write the data


        current_time_simulated_file= open("./current_time_simulated.txt","r+") 
        current_time_simulated_file.truncate(0)
        current_time_simulated_file.write(str(i)) # Writes at what time the current simulation is.
        current_time_simulated_file.close()



        i+=1 