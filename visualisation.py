# Need to create a server on a terminal through : ./pvserver --multi-clients
# Then connect to the server through paraview_built

from paraview.simple import *
import time
import pandas as pd
import builtins
import numpy as np


def show_slice(wind_value,wind_direction):

    simulated_ang=["0" ,"0.3307", "0.6614" , "0.9921" ,  "1.3228" , "1.6535"  , "1.9842"  , "2.3149"  , "2.6456" ,  "2.9762" , "3.3069", "3.6376 " ,   "3.9683"  ,  "4.2990" ,   "4.6297", " 4.9604", "5.2911"  ,  "5.6218"  ,  "5.9525"] # ! Case 3.6 et 4.9 missing because problem in the sim??
    simulated_ang = [int(eval(i)*180/np.pi) for i in simulated_ang] # Convert to °
    simulated_vel=[5, 10, 15]

    if wind_direction not in simulated_ang: # Simple condition to have the current velocity input from the UI actually snap to the closest actual velocity simulation from the simulation
        wind_direction=simulated_ang[builtins.min(range(len(simulated_ang)), key = lambda i: abs(simulated_ang[i]-wind_direction))]

    if wind_value not in simulated_vel: # Simple condition to have the current velocity input from the UI actually snap to the closest actual velocity simulation from the simulation
        wind_value=simulated_vel[builtins.min(range(len(simulated_vel)), key = lambda i: abs(simulated_vel[i]-wind_value))]

    try: # Try to modify the source for the slice
            
        afoam=FindSource('afoam')
        ReplaceReaderFileName(afoam, ['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/cases/val_{0}_ang_{1}.vtm'.format(wind_value,wind_direction)], 'FileName')

        afoam=GetActiveSource()
        RenameProxy(afoam, 'sources', 'afoam')
        RenameSource('afoam', afoam)

    except: # If the source for the slice does not exist, create it

        afoam = XMLMultiBlockDataReader(registrationName='afoam', FileName=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/cases/val_{0}_ang_{1}.vtm'.format(wind_value,wind_direction)]) # Depending on the slider position, the simulator with select a vtm file representing the field at that given angle
        slice1 = Slice(registrationName='Slice1', Input=afoam)
        slice1.SliceType = 'Plane'
        slice1.HyperTreeGridSlicer = 'Plane'
        slice1.SliceOffsetValues = [0.0]
        slice1.SliceType.Origin = [0.0, 0.0, 100.0]
        slice1.SliceType.Normal = [0.0, 0.0, 1.0]
        # get active view
        
        HideInteractiveWidgets(proxy=slice1.SliceType)

        # show data in view
        slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')
        slice1Display.Representation = 'Surface'
        slice1Display.ColorArrayName = [None, '']
        slice1Display.SelectTCoordArray = 'None'
        slice1Display.SelectNormalArray = 'None'
        slice1Display.SelectTangentArray = 'None'
        slice1Display.OSPRayScaleArray = 'U'
        slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
        slice1Display.SelectOrientationVectors = 'U'
        slice1Display.ScaleFactor = 399.99992675781255
        slice1Display.SelectScaleArray = 'None'
        slice1Display.GlyphType = 'Arrow'
        slice1Display.GlyphTableIndexArray = 'None'
        slice1Display.GaussianRadius = 19.999996337890625
        slice1Display.SetScaleArray = ['POINTS', 'U']
        slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
        slice1Display.OpacityArray = ['POINTS', 'U']
        slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
        slice1Display.DataAxesGrid = 'GridAxesRepresentation'
        slice1Display.PolarAxes = 'PolarAxesRepresentation'
        slice1Display.SelectInputVectors = ['POINTS', 'U']
        slice1Display.WriteLog = ''


        ColorBy(slice1Display, ('POINTS', 'U', 'Magnitude'))
        slice1Display.RescaleTransferFunctionToDataRange(True, False)

        # show color bar/color legend
        slice1Display.SetScalarBarVisibility(renderView1, True)

        # get color transfer function/color map for 'U'
        uLUT = GetColorTransferFunction('U')

        # get opacity transfer function/opacity map for 'U'
        uPWF = GetOpacityTransferFunction('U')

        # get 2D transfer function for 'U'
        uTF2D = GetTransferFunction2D('U')


Connect('localhost') # Connect to the local server launched through the terminal (see README)

try: # Delete the displayed data if it exists already, if not, nothing happens

    buildingsstl = FindSource('buildings.stl')
    tableToPoints1 = FindSource('TableToPoints1')
    programmableSource1 = FindSource('ProgrammableSource1')
    slice1=FindSource('Slice1')
    afoam=FindSource('afoam')
    cylinder2=FindSource('Cylinder2')

    Delete(cylinder2)
    del cylinder2
    Delete(buildingsstl)
    del buildingsstl
    Delete(programmableSource1)
    del programmableSource1
    Delete(tableToPoints1)
    del tableToPoints1
    Delete(afoam)
    del afoam
    Delete(slice1)
    del slice1



except:
    pass

current_time_file = open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/current_time_vizu.txt", "w") # Initialize the displayed time to 0
current_time_file.write("0")
current_time_file.close()

buildingsstl = STLReader(registrationName='buildings.stl', FileNames=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/constant/triSurface/buildings.stl']) # Load the STL for graphical representation
renderView1 = GetActiveViewOrCreate('RenderView') # Show the buildings

# show data in view
buildingsstlDisplay = Show(buildingsstl, renderView1, 'GeometryRepresentation')

cylinder2 = Cylinder(registrationName='Cylinder2') # Create the "floor"
cylinder2.Height = 1
cylinder2.Radius = 2000.0
cylinder2.Center = [0.0, 0.0, -1]
cylinder2.Resolution = 360
cylinder2Display = Show(cylinder2, renderView1, 'GeometryRepresentation')
cylinder2Display.Orientation = [90.0, 0.0, 0.0]
cylinder2Display.PolarAxes.Orientation = [90.0, 0.0, 0.0]
cylinder2Display.Opacity = 0.1


# get color transfer function/color map for 'STLSolidLabeling'
sTLSolidLabelingLUT = GetColorTransferFunction('STLSolidLabeling')

# trace defaults for the display properties.
buildingsstlDisplay.Representation = 'Surface'
buildingsstlDisplay.ColorArrayName = ['CELLS', 'STLSolidLabeling']
buildingsstlDisplay.LookupTable = sTLSolidLabelingLUT
buildingsstlDisplay.SelectTCoordArray = 'None'
buildingsstlDisplay.SelectNormalArray = 'None'
buildingsstlDisplay.SelectTangentArray = 'None'
buildingsstlDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
buildingsstlDisplay.SelectOrientationVectors = 'None'
buildingsstlDisplay.ScaleFactor = 198.62966918945312
buildingsstlDisplay.SelectScaleArray = 'STLSolidLabeling'
buildingsstlDisplay.GlyphType = 'Arrow'
buildingsstlDisplay.GlyphTableIndexArray = 'STLSolidLabeling'
buildingsstlDisplay.GaussianRadius = 9.931483459472657
buildingsstlDisplay.SetScaleArray = [None, '']
buildingsstlDisplay.ScaleTransferFunction = 'PiecewiseFunction'
buildingsstlDisplay.OpacityArray = [None, '']
buildingsstlDisplay.OpacityTransferFunction = 'PiecewiseFunction'
buildingsstlDisplay.DataAxesGrid = 'GridAxesRepresentation'
buildingsstlDisplay.PolarAxes = 'PolarAxesRepresentation'
buildingsstlDisplay.SelectInputVectors = [None, '']
buildingsstlDisplay.WriteLog = ''


# reset view to fit data
renderView1.ResetCamera(False)

# get the material library
materialLibrary1 = GetMaterialLibrary()

# show color bar/color legend
buildingsstlDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# get opacity transfer function/opacity map for 'STLSolidLabeling'
sTLSolidLabelingPWF = GetOpacityTransferFunction('STLSolidLabeling')

# get 2D transfer function for 'STLSolidLabeling'
sTLSolidLabelingTF2D = GetTransferFunction2D('STLSolidLabeling')

# turn off scalar coloring
ColorBy(buildingsstlDisplay, None)

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(sTLSolidLabelingLUT, renderView1)


programmableSource1 = ProgrammableSource(registrationName='ProgrammableSource1')
programmableSource1.Script = ''
programmableSource1.ScriptRequestInformation = ''
programmableSource1.PythonPath = ''

# This scripts reads the data from parquet and displays it, all the while it writes if rendering is done to the text file
programmableSource1.OutputDataSetType = 'vtkTable'
programmableSource1.Script = """import numpy as np  
import pandas as pd
import time
# assuming data.csv is a CSV file with the 1st row being the names names for
# the columns

f = open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/rendering_done.txt", "r+")
f.truncate(0)

f.write("0")


data=np.empty([1,3])
data_x=data[:,0]
data_y=data[:,1]
data_z=data[:,2]



current_data=pd.read_parquet("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/csv0/particles_positions_{0}.parquet").values
data_x=np.concatenate((data_x,current_data[:,0]))
data_y=np.concatenate((data_y,current_data[:,1]))
data_z=np.concatenate((data_z,current_data[:,2]))
        

data_x=np.delete(data_x,0)
data_y=np.delete(data_y,0)
data_z=np.delete(data_z,0)


output.RowData.append(data_x, "X")
output.RowData.append(data_y, "Y")
output.RowData.append(data_z, "Z")



f.truncate(0)
f.write("1")
""".format(0)


programmableSource1.ScriptRequestInformation = ''
programmableSource1.PythonPath = ''

tableToPoints1 = TableToPoints(registrationName='TableToPoints1', Input=programmableSource1)
tableToPoints1.XColumn = 'X'
tableToPoints1.YColumn = 'Y'
tableToPoints1.ZColumn = 'Z'

renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
tableToPoints1Display = Show(tableToPoints1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
tableToPoints1Display.Representation = 'Surface'
tableToPoints1Display.ColorArrayName = [None, '']
tableToPoints1Display.SelectTCoordArray = 'None'
tableToPoints1Display.SelectNormalArray = 'None'
tableToPoints1Display.SelectTangentArray = 'None'
tableToPoints1Display.OSPRayScaleFunction = 'PiecewiseFunction'
tableToPoints1Display.SelectOrientationVectors = 'None'
tableToPoints1Display.ScaleFactor = 2.565365511851337
tableToPoints1Display.SelectScaleArray = 'None'
tableToPoints1Display.GlyphType = 'Arrow'
tableToPoints1Display.GlyphTableIndexArray = 'None'
tableToPoints1Display.GaussianRadius = 0.12826827559256684
tableToPoints1Display.SetScaleArray = [None, '']
tableToPoints1Display.ScaleTransferFunction = 'PiecewiseFunction'
tableToPoints1Display.OpacityArray = [None, '']
tableToPoints1Display.OpacityTransferFunction = 'PiecewiseFunction'
tableToPoints1Display.DataAxesGrid = 'GridAxesRepresentation'
tableToPoints1Display.PolarAxes = 'PolarAxesRepresentation'
tableToPoints1Display.SelectInputVectors = [None, '']
tableToPoints1Display.WriteLog = ''

# reset view to fit data
renderView1.ResetCamera(False)

# update the view to ensure updated data information

renderView1.Update()

############################################################### SETUP COMPLETED




i=0
p_wind_direction=0
p_wind_value=0

while 1:

    try:
        coms = pd.read_csv("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/front_end_back_end_communication.csv")
    except:
        continue

    if i>=coms.loc[0, 'max time']: # Loops back if the user inputed a max time that has been reached
        i=0

    if coms.loc[0, 'pause']==0: # Handle the pause, only continue if the user did not pause
        i=i+1
        programmableSource1.Script = """import numpy as np 
import pandas as pd
import time



f = open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/rendering_done.txt", "r+")
f.truncate(0)

f.write("0")

req_time = 0
data=np.empty([1,3])
data_x=data[:,0]
data_y=data[:,1]
data_z=data[:,2]

current_data=pd.read_parquet("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/csv0/particles_positions_{0}.parquet").values
data_x=np.concatenate((data_x,current_data[:,0]))
data_y=np.concatenate((data_y,current_data[:,1]))
data_z=np.concatenate((data_z,current_data[:,2]))
            


data_x=np.delete(data_x,0)
data_y=np.delete(data_y,0)
data_z=np.delete(data_z,0)

output.RowData.append(data_x, "X")
output.RowData.append(data_y, "Y")
output.RowData.append(data_z, "Z")

f.truncate(0)
f.write("1")
""".format(i) # Update the filter to the new value of i

        wait_rendering_file = open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/rendering_done.txt","r") 

        while not wait_rendering_file.read(): # Block here if the rendering is not done on paraview side
            continue

        try:
            time.sleep(1/coms.loc[0, 'fps']) # Handles the FPS inputed by the user
        except:
            time.sleep(1) # When the user delete the fps totally, the code would crash, instead, make it so fps=1

        try:
            current_time_simulated_file= open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/current_time_simulated.txt","r")
            simulation_time=int(current_time_simulated_file.read())
        except:
            pass


        while i > simulation_time-10: # Wait if the displaying is catching up to the simulation (with a 10 frame buffer to avoid any issues)
            time.sleep(0.5) # Display going too fast
            try:
                current_time_simulated_file= open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/current_time_simulated.txt","r")
                simulation_time=int(current_time_simulated_file.read())
            except:
                pass

        current_time_file = open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/current_time_vizu.txt", "w") # Write at what time we are currently vizualizing
        current_time_file.write(str(i))
        current_time_file.close()


        try: # Handle the display or not of the slice
            injection_data = pd.read_csv("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/points_data.csv") # CSV with info about the injection and time simulation
            wind_direction=injection_data.loc[0,'Velocity direction']
            wind_value=injection_data.loc[0,'Velocity magnitude']


            if not coms.loc[0, 'slice']:
                slice1=FindSource("Slice1")
                renderView1 = GetActiveViewOrCreate('RenderView')
                Hide(slice1,renderView1)
                Show(tableToPoints1, renderView1, 'GeometryRepresentation')
            elif coms.loc[0, 'slice']:
                slice1=FindSource("Slice1")
                renderView1 = GetActiveViewOrCreate('RenderView')
                Show(slice1, renderView1, 'GeometryRepresentation')
                Show(tableToPoints1, renderView1, 'GeometryRepresentation')


            if p_wind_direction !=  wind_direction or p_wind_value != wind_value:
                p_wind_direction=wind_direction
                p_wind_value=wind_value


                show_slice(wind_value,wind_direction)


        except:
            pass


    continue