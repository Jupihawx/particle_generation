# Need to create a server on a terminal through : ./pvserver --multi-clients
# Then connect to the server through paraview_built

from paraview.simple import *
import time


Connect('localhost')


buildingsstl = STLReader(registrationName='buildings.stl', FileNames=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/constant/triSurface/buildings.stl']) # Load the STL for graphical representation
renderView1 = GetActiveViewOrCreate('RenderView')

# show data in view
buildingsstlDisplay = Show(buildingsstl, renderView1, 'GeometryRepresentation')

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

# Properties modified on programmableSource1
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


for i in range(1,500):
    programmableSource1.Script = """import numpy as np 
import pandas as pd
import time
# assuming data.csv is a CSV file with the 1st row being the names names for
# the columns



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
""".format(i)

    wait_rendering_file = open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/rendering_done.txt","r") 

    while not wait_rendering_file.read():
        continue

    time.sleep(1/30)
    
    current_time_simulated_file= open("/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/current_time_simulated.txt","r")
    simulation_time=int(current_time_simulated_file.read())

    if i > simulation_time-10:
        time.sleep(1/5) # Display going too fast