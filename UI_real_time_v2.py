import pandas as pd
import pyautogui
import time
import pyperclip
from tkinter import *
#from tkinter import ttk
import os
import shutil
import threading

df = pd.read_csv("points_data.csv") # data controlling the points
coms = pd.read_csv("front_end_back_end_communication.csv") # data controlling the UI

def vizualize():
    os.system("/home/boris/opt/ParaView-build/paraview_build/bin/pvpython visualisation_POD.py")

def get_current_time():
        current_time=open("./current_time_vizu.txt","r").read()
        label_time.config(text="current time : {0}".format(current_time))
        master.after(10,get_current_time)

def get_current_simulation_time():
        current_time_simu=open("./current_time_simulated.txt","r").read()
        label_time_simu.config(text="current simulated time up to: {0}".format(current_time_simu))
        master.after(1000,get_current_simulation_time)

def write_values(*arg): # Used to write down the value on the csv
    df = pd.read_csv("points_data.csv")
    coms = pd.read_csv("front_end_back_end_communication.csv")

    df.loc[0, 'center_x'] = str(w1.get())
    df.loc[0, 'center_y'] = str(w2.get())
    df.loc[0, 'center_z'] = str(w3.get())
    df.loc[0, 'number_points'] = str(w4.get())
    df.loc[0, 'radius_points'] = str(w5.get())
    df.loc[0, 'diffCoeff'] = str(w6.get())
    df.loc[0, 'Velocity direction'] = str(w7.get()) 
    df.loc[0, 'Velocity magnitude'] = str(w8.get()) 

    coms.loc[0, 'max time'] = str(sv1.get()) 
    coms.loc[0, 'fps'] = str(sv2.get()) 
    coms.loc[0,'slice'] = str(var1.get())


    df.to_csv("points_data.csv", index=False)
    coms.to_csv("front_end_back_end_communication.csv", index=False)

def simulate():
    write_values()
    coms = pd.read_csv("front_end_back_end_communication.csv")
    coms.loc[0, 'simulation requested'] = 1
    coms.to_csv("front_end_back_end_communication.csv", index=False)

    os.system("/home/boris/opt/ParaView-build/paraview_build/bin/pvpython Particle_Simulation_parquet_real_time_v2_POD.py")
    #os.system("~/opt/ParaView-5.11/bin/mpiexec -np 4 ~/opt/ParaView-build/paraview_build/bin/pvbatch Particle_Simulation_parquet_real_time_v2_parallel.py")

def parallel_simulate():
    thread_simulation= threading.Thread(target=simulate)
    thread_simulation.start()
"""     if len(threading.enumerate())>1:
        write_values()
        coms = pd.read_csv("front_end_back_end_communication.csv")
        coms.loc[0, 'simulation requested'] = 1
        coms.to_csv("front_end_back_end_communication.csv", index=False)
        print("LAUNCHING SIMULATION") """



def rgb_to_hex(rgb):
    return '%02x%02x%02x' % rgb


def update_window(event): # Used to choose the right line to modify the csv 
    df = pd.read_csv("points_data.csv")

    df.loc[:, 'currently_selected'] = 0
    df.loc[0, 'currently_selected'] = 1
    df.to_csv("points_data.csv", index=False)

    w1.set(df.loc[0, 'center_x'])
    w2.set(df.loc[0, 'center_y'])
    w3.set(df.loc[0, 'center_z'])
    w4.set(df.loc[0, 'number_points'])
    w5.set(df.loc[0, 'radius_points'])
    w6.set(df.loc[0, 'diffCoeff'])
    wr.set(df.loc[0, 'colorR'])
    wg.set(df.loc[0, 'colorG'])
    wb.set(df.loc[0, 'colorB'])
    wb.set(df.loc[0, 'Velocity direction'])
    wb.set(df.loc[0, 'Velocity magnitude'])


    drop.configure(foreground="#"+str(rgb_to_hex((wr.get(),wg.get(),wb.get()))))



def reset():

    shutil.rmtree("./csv{0}/".format(0))


def clean_particles():
    coms = pd.read_csv("front_end_back_end_communication.csv")
    coms.loc[0, 'clean particles'] = 1
    coms.to_csv("front_end_back_end_communication.csv", index=False)


def pause():
    coms = pd.read_csv("front_end_back_end_communication.csv")
    if coms.loc[0, 'pause'] == 1:
        coms.loc[0, 'pause'] = 0
        coms.to_csv("front_end_back_end_communication.csv", index=False)

    else:
        coms.loc[0, 'pause'] =1
        coms.to_csv("front_end_back_end_communication.csv", index=False)





master = Tk()
master.title("Particle Tracer Manager")


w1 = Scale(master, from_=-2000, to=2000,orient=HORIZONTAL,length=300, label='X',width=20, command=write_values)
w1.set(df.loc[0, 'center_x']) #this lines are just to initialize on the first opening 
w1.pack()
w2 = Scale(master, from_=-2000, to=2000,orient=HORIZONTAL,length=300, label='Y',width=20, command=write_values)
w2.set(df.loc[0, 'center_y'])
w2.pack()
w3 = Scale(master, from_=0, to=300,orient=HORIZONTAL,length=300, label='Z',width=20, command=write_values)
w3.set(df.loc[0, 'center_z'])
w3.pack()
w4 = Scale(master, from_=0, to=300,orient=HORIZONTAL,length=300, label='Number of points',width=20, command=write_values)
w4.set(df.loc[0, 'number_points'])
w4.pack()
w5 = Scale(master, from_=0, to=30,orient=HORIZONTAL,length=300, label='Radius',width=20, command=write_values)
w5.set(df.loc[0, 'radius_points'])
w5.pack()
w6 = Scale(master, from_=0, to=10, resolution=0.1, orient=HORIZONTAL,length=300, label='Diffusion coefficient',width=20, command=write_values)
w6.set(df.loc[0, 'diffCoeff'])
w6.pack()
w7 = Scale(master, from_=0, to=360,orient=HORIZONTAL,length=300, label='Velocity direction (°)',width=20, command=write_values)
w7.set(df.loc[0, 'Velocity direction'])
w7.pack()
w8 = Scale(master, from_=5, to=15,orient=HORIZONTAL,length=300, label='Velocity magnitude (m/s)',width=20, command=write_values)
w8.set(df.loc[0, 'Velocity magnitude'])
w8.pack()

timeFrame= Frame(master, pady=20)
timeFrame.pack()



current_time=open("./current_time.txt","r").read()
current_time_simu=open("./current_time_simulated.txt","r").read()

label_time=Label(master, text="current time : {}".format(current_time), font=("Courier 10 bold"))
label_time.pack()

label_time_simu=Label(master, text="current simulated time up to {}".format(current_time_simu), font=("Courier 10 bold"))
label_time_simu.pack()

var1 = IntVar()
c1 = Checkbutton(master, text='Show slice?',variable=var1, onvalue=1, offvalue=0, command=write_values)
c1.pack()
""" Button(master, text='Start', command=parallel_simulate ,pady=30,padx=30).pack(pady=10) # To be done
 """
Button(master, text='Clean particles', command=clean_particles ,pady=10,padx=10).pack(pady=10) # To be done
Button(master, text='Play/Pause', command=pause ,pady=10,padx=10).pack(pady=10) # To be done

""" 
progress = ttk.Progressbar(master, orient = HORIZONTAL, length = 300, mode = 'determinate')
progress.pack(pady = 10)

simulationProgressFile= open("./Simulation_Progress.txt","r")
progress['value']=int(simulationProgressFile.read()) """

sv1= StringVar()
sv2= StringVar()

sv1.initialize(coms.loc[0, 'max time'])
sv2.initialize(coms.loc[0, 'fps'])

sv1.trace("w",lambda name, index, mode, sv1=sv1: write_values(sv1))
sv2.trace("w",lambda name, index, mode, sv2=sv2: write_values(sv2))

label=Label(timeFrame, text="Total time / fps", font=("Courier 10 bold"))
label.pack(side=TOP)

entry= Entry(timeFrame, width= 5, textvariable=sv1)
entry.focus_set()
entry.pack(side=LEFT, padx=10)

entry= Entry(timeFrame, width= 5,textvariable=sv2)
entry.focus_set()
entry.pack(side=LEFT, padx=10)

master.attributes('-topmost', True) #To always have window on top


get_current_time() # Update current time every second

get_current_simulation_time() # Update simulation time every second


thread_visualisation= threading.Thread(target=vizualize) # Launches the vizualisation
thread_visualisation.start()
parallel_simulate() # Launches the simulation






mainloop()
