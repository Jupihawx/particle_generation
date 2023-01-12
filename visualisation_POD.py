# Need to create a server on a terminal through : ./pvserver --multi-clients
# Then connect to the server through paraview_built

from paraview.simple import *
import time
import pandas as pd
import builtins
import numpy as np
from scipy import interpolate
from scipy.optimize import curve_fit

Connect('localhost') # Connect to the local server launched through the terminal (see README)

try: # Delete the displayed data if it exists already, if not, nothing happens

    buildingsstl = FindSource('buildings.stl')
    tableToPoints1 = FindSource('TableToPoints1')
    programmableSource1 = FindSource('ProgrammableSource1')
    slice1=FindSource('Slice1')
    cylinder2=FindSource('Cylinder2')
    basesAndMean_total_19basesvtu=FindSource('BasesAndMean_total_19bases.vtu')
    calculator1=FindSource('Calculator1')

    ###################### CA NE MARCHE PAS PCK IL Y EN A UN QUI PAUSE PROBLEME ET APRES CA ARRETE DE FAIRE TOURNER LE CODE!!! TROUVE LEQUEL ET CHECK SI RESET SESSION CEST BIEN
    Delete(cylinder2)
    Delete(buildingsstl)
    Delete(programmableSource1)
    Delete(tableToPoints1)
    Delete(basesAndMean_total_19basesvtu)
    Delete(calculator1)
    Delete(slice1)



    del cylinder2
    del buildingsstl
    del programmableSource1
    del tableToPoints1
    del basesAndMean_total_19basesvtu
    del calculator1
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


# Loads a heavy VTU holding all the bases 19, that then will be used to simulate the different wind. Technically, we could use less basis at the cost of the precision of the result
basesAndMean_total_19basesvtu = XMLUnstructuredGridReader(registrationName='BasesAndMean_total_19bases.vtu', FileName=['/home/boris/OpenFOAM/boris-v2206/run/ROM/Own_code/BasesAndMean_total_19bases.vtu'])
basesAndMean_total_19basesvtu.CellArrayStatus = ['U']
basesAndMean_total_19basesvtu.PointArrayStatus = ['Mean', 'Base0', 'Base1', 'Base2', 'Base3', 'Base4', 'Base5', 'Base6', 'Base7', 'Base8', 'Base9', 'Base10', 'Base11', 'Base12', 'Base13', 'Base14', 'Base15', 'Base16', 'Base17', 'Base18']

# Properties modified on basesAndMean_total_19basesvtu
basesAndMean_total_19basesvtu.CellArrayStatus = []
basesAndMean_total_19basesvtu.TimeArray = 'None'

# show data in view
basesAndMean_total_19basesvtuDisplay = Show(basesAndMean_total_19basesvtu, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
basesAndMean_total_19basesvtuDisplay.Representation = 'Surface'
basesAndMean_total_19basesvtuDisplay.ColorArrayName = [None, '']
basesAndMean_total_19basesvtuDisplay.SelectTCoordArray = 'None'
basesAndMean_total_19basesvtuDisplay.SelectNormalArray = 'None'
basesAndMean_total_19basesvtuDisplay.SelectTangentArray = 'None'
basesAndMean_total_19basesvtuDisplay.OSPRayScaleArray = 'Base0'
basesAndMean_total_19basesvtuDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
basesAndMean_total_19basesvtuDisplay.SelectOrientationVectors = 'Base0'
basesAndMean_total_19basesvtuDisplay.ScaleFactor = 400.0
basesAndMean_total_19basesvtuDisplay.SelectScaleArray = 'Base0'
basesAndMean_total_19basesvtuDisplay.GlyphType = 'Arrow'
basesAndMean_total_19basesvtuDisplay.GlyphTableIndexArray = 'Base0'
basesAndMean_total_19basesvtuDisplay.GaussianRadius = 20.0
basesAndMean_total_19basesvtuDisplay.SetScaleArray = ['POINTS', 'Base0']
basesAndMean_total_19basesvtuDisplay.ScaleTransferFunction = 'PiecewiseFunction'
basesAndMean_total_19basesvtuDisplay.OpacityArray = ['POINTS', 'Base0']
basesAndMean_total_19basesvtuDisplay.OpacityTransferFunction = 'PiecewiseFunction'
basesAndMean_total_19basesvtuDisplay.DataAxesGrid = 'GridAxesRepresentation'
basesAndMean_total_19basesvtuDisplay.PolarAxes = 'PolarAxesRepresentation'
basesAndMean_total_19basesvtuDisplay.ScalarOpacityUnitDistance = 27.775292883875284
basesAndMean_total_19basesvtuDisplay.OpacityArrayName = ['POINTS', 'Base0']
basesAndMean_total_19basesvtuDisplay.SelectInputVectors = ['POINTS', 'Base0']
basesAndMean_total_19basesvtuDisplay.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
basesAndMean_total_19basesvtuDisplay.ScaleTransferFunction.Points = [-0.0005533699387113467, 0.0, 0.5, 0.0, 0.0011464366539011405, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
basesAndMean_total_19basesvtuDisplay.OpacityTransferFunction.Points = [-0.0005533699387113467, 0.0, 0.5, 0.0, 0.0011464366539011405, 1.0, 0.5, 0.0]
renderView1.Update()

# hide data in view
Hide(basesAndMean_total_19basesvtu, renderView1)

# The calculator calculates the reconstructed case at a given angle from the 19 bases as well as the interpolation of the coefficients, done below. The first value is just given to initialize
calculator1 = Calculator(registrationName='Calculator1', Input=basesAndMean_total_19basesvtu)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.Function = 'Mean-1835.977244744856*Base0-4020.1868125881056*Base1-1761.3323038954372*Base2+972.0952450449845*Base3+638.7500754734808*Base4+617.6556332534561*Base5+666.5008914550156*Base6-602.8693311192545*Base7+221.6197347628428*Base8-589.2407767447528*Base9+612.8529871311732*Base10+178.95545725719398*Base11-20.721528660218933*Base12-418.1801871459541*Base13+551.5875279406702*Base14+190.94793894506833*Base15+791.3346626073784*Base16+83.68250265674467*Base17-2.311911773134057e-11*Base18'

# show data in view
calculator1Display = Show(calculator1, renderView1, 'UnstructuredGridRepresentation')

# trace defaults for the display properties.
calculator1Display.Representation = 'Surface'
calculator1Display.ColorArrayName = [None, '']
calculator1Display.SelectTCoordArray = 'None'
calculator1Display.SelectNormalArray = 'None'
calculator1Display.SelectTangentArray = 'None'
calculator1Display.OSPRayScaleArray = 'Base0'
calculator1Display.OSPRayScaleFunction = 'PiecewiseFunction'
calculator1Display.SelectOrientationVectors = 'Result'
calculator1Display.ScaleFactor = 400.0
calculator1Display.SelectScaleArray = 'Base0'
calculator1Display.GlyphType = 'Arrow'
calculator1Display.GlyphTableIndexArray = 'Base0'
calculator1Display.GaussianRadius = 20.0
calculator1Display.SetScaleArray = ['POINTS', 'Base0']
calculator1Display.ScaleTransferFunction = 'PiecewiseFunction'
calculator1Display.OpacityArray = ['POINTS', 'Base0']
calculator1Display.OpacityTransferFunction = 'PiecewiseFunction'
calculator1Display.DataAxesGrid = 'GridAxesRepresentation'
calculator1Display.PolarAxes = 'PolarAxesRepresentation'
calculator1Display.ScalarOpacityUnitDistance = 27.775292883875284
calculator1Display.OpacityArrayName = ['POINTS', 'Base0']
calculator1Display.SelectInputVectors = ['POINTS', 'Result']
calculator1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
calculator1Display.ScaleTransferFunction.Points = [-0.0005533699387113467, 0.0, 0.5, 0.0, 0.0011464366539011405, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
calculator1Display.OpacityTransferFunction.Points = [-0.0005533699387113467, 0.0, 0.5, 0.0, 0.0011464366539011405, 1.0, 0.5, 0.0]
# update the view to ensure updated data information
Hide(basesAndMean_total_19basesvtu, renderView1)

renderView1.Update()

# hide data in view
Hide(calculator1, renderView1)

# create a new 'Slice'
slice1 = Slice(registrationName='Slice1', Input=calculator1)
slice1.SliceType = 'Plane'
slice1.HyperTreeGridSlicer = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0, 0.0, 300.0956263784319]

# init the 'Plane' selected for 'HyperTreeGridSlicer'
slice1.HyperTreeGridSlicer.Origin = [0.0, 0.0, 300.0956263784319]

# toggle interactive widget visibility (only when running from the GUI)
HideInteractiveWidgets(proxy=slice1.SliceType)

# Properties modified on slice1.SliceType
slice1.SliceType.Origin = [0.0, 0.0, 100.0]
slice1.SliceType.Normal = [0.0, 0.0, 1.0]

# show data in view
slice1Display = Show(slice1, renderView1, 'GeometryRepresentation')

# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = [None, '']
slice1Display.SelectTCoordArray = 'None'
slice1Display.SelectNormalArray = 'None'
slice1Display.SelectTangentArray = 'None'
slice1Display.OSPRayScaleArray = 'Base0'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'Result'
slice1Display.ScaleFactor = 399.99992675781255
slice1Display.SelectScaleArray = 'Base0'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'Base0'
slice1Display.GaussianRadius = 19.999996337890625
slice1Display.SetScaleArray = ['POINTS', 'Base0']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'Base0']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'
slice1Display.SelectInputVectors = ['POINTS', 'Result']
slice1Display.WriteLog = ''

# init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
slice1Display.ScaleTransferFunction.Points = [-0.0002039755027129337, 0.0, 0.5, 0.0, 0.000996576878763453, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
slice1Display.OpacityTransferFunction.Points = [-0.0002039755027129337, 0.0, 0.5, 0.0, 0.000996576878763453, 1.0, 0.5, 0.0]

# hide data in view
Hide(calculator1, renderView1)

# update the view to ensure updated data information
renderView1.Update()


ColorBy(slice1Display, ('POINTS', 'Result', 'Magnitude'))

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Result'
resultLUT = GetColorTransferFunction('Result')

# get opacity transfer function/opacity map for 'Result'
resultPWF = GetOpacityTransferFunction('Result')

# get 2D transfer function for 'Result'
resultTF2D = GetTransferFunction2D('Result')

slice1 = GetActiveSource()
renderView1 = GetActiveViewOrCreate('RenderView')
slice1Display = GetDisplayProperties(slice1, view=renderView1)

slice1Display.RescaleTransferFunctionToDataRange(False, True)
resultLUT = GetColorTransferFunction('Result')
resultPWF = GetOpacityTransferFunction('Result')
resultTF2D = GetTransferFunction2D('Result')

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


###################################################### Calculate the function for interpolation##############################################


angles = [0, 18, 37, 56, 75, 94, 113, 132 ,151 ,170, 189, 208, 227, 246, 265, 284, 303, 322, 341]
angles.append(360) # Adds the angle 360 to cover the whole range
Coeffs = pd.read_csv("/home/boris/OpenFOAM/boris-v2206/run/ROM/Own_code/coeffs.csv",header=None)
Coeffs=Coeffs.to_numpy() 
Coeffs=np.vstack((Coeffs,Coeffs[0,:])) # Add the value 0 of coefficient to 360 (periodic solutions verified in the ipynb)
f_interpolated=[]


for i in range(0,19):
    f_interpolated.append(interpolate.interp1d(angles, Coeffs[:,i], 'cubic')) # Calculate each interpolation function for each coefficient


def update_slice(wind_direction):

    Text=["Mean"]
    nb_bases=20
    coeffs_interpolated=[]
    coeffs_interpolated=[f(wind_direction) for f in f_interpolated] # Calculate the coefficient for a given wind direction

    i=0
    for i in range(nb_bases-1): # Generates the text that will be passed to the Calculator with each coefficient for each base
        if coeffs_interpolated[i] > 0:
            Text.append("+")
            Text.append("{0}*Base{1}".format(coeffs_interpolated[i],i))
                        
        if coeffs_interpolated[i] < 0:
            Text.append("{0}*Base{1}".format(coeffs_interpolated[i],i))

    calculator1.Function = '{0}'.format(''.join(Text))

    UpdatePipeline() # Update the view
    slice1 = GetActiveSource()
    renderView1 = GetActiveViewOrCreate('RenderView')
    slice1Display = GetDisplayProperties(slice1, view=renderView1)

    slice1Display.RescaleTransferFunctionToDataRange(False, True)
    resultLUT = GetColorTransferFunction('Result')
    resultPWF = GetOpacityTransferFunction('Result')
    resultTF2D = GetTransferFunction2D('Result')



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
            simulation_time=0
            


        while i > simulation_time-10: # Wait if the displaying is catching up to the simulation (with a 10 frame buffer to avoid any issues)
            time.sleep(0.5) # Display going too fast
            try:
                current_time_simulated_file= open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/current_time_simulated.txt","r")
                simulation_time=int(current_time_simulated_file.read())
                
                # The four lines below are just there so that when the user plays with the wind direction, it still displays it changing, even though the simulation is still being processed. That helps for a better feel of the UI mostly.
                injection_data = pd.read_csv("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/points_data.csv") # CSV with info about the injection and time simulation
                wind_direction=injection_data.loc[0,'Velocity direction']
                wind_value=injection_data.loc[0,'Velocity magnitude']
                update_slice(wind_direction)
            except:
                simulation_time=0

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
                update_slice(wind_direction)
            elif coms.loc[0, 'slice']:
                slice1=FindSource("Slice1")
                renderView1 = GetActiveViewOrCreate('RenderView')
                Show(slice1, renderView1, 'GeometryRepresentation')
                Show(tableToPoints1, renderView1, 'GeometryRepresentation')
                update_slice(wind_direction)


            if p_wind_direction !=  wind_direction or p_wind_value != wind_value:
                p_wind_direction=wind_direction
                p_wind_value=wind_value
                update_slice(wind_direction)
                


        except:
            pass


    continue