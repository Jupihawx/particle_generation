from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()
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


# create a new 'Live Programmable Source'
liveProgrammableSource1 = LiveProgrammableSource(registrationName='LiveProgrammableSource1')
liveProgrammableSource1.Script = ''
liveProgrammableSource1.ScriptRequestInformation = ''
liveProgrammableSource1.PythonPath = ''
liveProgrammableSource1.ScriptCheckNeedsUpdate = ''

# Properties modified on liveProgrammableSource1
liveProgrammableSource1.OutputDataSetType = 'vtkTable' 

## This script reads the existing parquet file series and display them at the correct time step
liveProgrammableSource1.Script = """import numpy as np 
import pandas as pd
import time
# assuming data.csv is a CSV file with the 1st row being the names names for
# the columns


def GetUpdateTimestep(algorithm):
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    return outInfo.Get(executive.UPDATE_TIME_STEP()) \
              if outInfo.Has(executive.UPDATE_TIME_STEP()) else None


req_time = GetUpdateTimestep(self)
data=np.empty([1,3])
data_x=data[:,0]
data_y=data[:,1]
data_z=data[:,2]

current_time_simulated_file= open("./current_time_simulated.txt","r")
simulation_time=int(current_time_simulated_file.read())

if req_time > simulation_time-10: # If the vizualisation goes too fast with respect to the simulation, wait a second
    time.sleep(1)
    print("Displaying faster than simulating, waiting for a second..")


for i in range(0,6):
    try:
        current_data=pd.read_parquet("./csv{1}/particles_positions_{0}.parquet".format(str(int(req_time)),i)).values
        data_x=np.concatenate((data_x,current_data[:,0]))
        data_y=np.concatenate((data_y,current_data[:,1]))
        data_z=np.concatenate((data_z,current_data[:,2]))
        
    except:
        pass

current_time_file= open("./current_time.txt","w+")
current_time_file.write(str(int(req_time)))
current_time_file.close()
output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)

data_x=np.delete(data_x,0)
data_y=np.delete(data_y,0)
data_z=np.delete(data_z,0)


output.RowData.append(data_x, "X")
output.RowData.append(data_y, "Y")
output.RowData.append(data_z, "Z")

coms = pd.read_csv("front_end_back_end_communication.csv")
while coms.loc[0, 'pause'] == 1:
    coms = pd.read_csv("front_end_back_end_communication.csv")
    continue



"""

# This scripts generate timesteps corresponding to the number of parquet file existing for paraview
liveProgrammableSource1.ScriptRequestInformation = """def setOutputTimesteps(algorithm, timesteps):
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)

    outInfo.Remove(executive.TIME_STEPS())
    for timestep in timesteps:
        outInfo.Append(executive.TIME_STEPS(), timestep)

    outInfo.Remove(executive.TIME_RANGE())
    outInfo.Append(executive.TIME_RANGE(), timesteps[0])
    outInfo.Append(executive.TIME_RANGE(), timesteps[-1])


setOutputTimesteps(self, range(0,10000))

"""
liveProgrammableSource1.PythonPath = ''
# This script updates the source every second
liveProgrammableSource1.ScriptCheckNeedsUpdate = """
import time
import os

if not hasattr(self, "_my_time"):
  setattr(self, "_my_time", time.time())

t = time.time()

lastTime = getattr(self, "_my_time")
# adapt here to set the time (in sec) you want to wait between updates
if t - lastTime > 2:
  setattr(self, "_my_time", t)
  self.SetNeedsUpdate(True)

"""





liveProgrammableSourcePointer = LiveProgrammableSource(registrationName='Pointer to Source') # Create a source that reads the position of the CSV injection point and display it on screen for the user to know where injection happens
liveProgrammableSourcePointer.Script = ''
liveProgrammableSourcePointer.ScriptRequestInformation = ''
liveProgrammableSourcePointer.PythonPath = ''
liveProgrammableSourcePointer.ScriptCheckNeedsUpdate = ''

# Properties modified on liveProgrammableSource1
liveProgrammableSourcePointer.OutputDataSetType = 'vtkTable' 

liveProgrammableSourcePointer.Script = """import pandas as pd

df = pd.read_csv("points_data.csv") # data controlling the points
x=df.loc[0, 'center_x']
y=df.loc[0, 'center_y']
z=df.loc[0, 'center_z']
output.RowData.append(x, "X")
output.RowData.append(y, "Y")
output.RowData.append(z, "Z")
"""

liveProgrammableSourcePointer.PythonPath = ''
liveProgrammableSourcePointer.ScriptCheckNeedsUpdate = """self.SetNeedsUpdate(True)"""

tableToPointsSource = TableToPoints(registrationName='TableToPoints of Source', Input=liveProgrammableSourcePointer)
tableToPointsSource.XColumn = 'X'
tableToPointsSource.YColumn = 'Y'
tableToPointsSource.ZColumn = 'Z'
glyph = Glyph(registrationName='Injection position', Input=tableToPointsSource,
    GlyphType='Arrow')
glyph.OrientationArray = ['POINTS', 'No orientation array']
glyph.ScaleArray = ['POINTS', 'No scale array']
glyph.ScaleFactor = 0.1
glyph.GlyphTransform = 'Transform2'
glyph.GlyphType = 'Sphere'
glyph.ScaleFactor = 10.0

glyph2Display = Show(glyph, renderView1, 'GeometryRepresentation')
glyph2Display.Representation = 'Surface'
glyph2Display.ColorArrayName = [None, '']
glyph2Display.SelectTCoordArray = 'None'
glyph2Display.SelectNormalArray = 'Normals'
glyph2Display.SelectTangentArray = 'None'
glyph2Display.OSPRayScaleArray = 'Normals'
glyph2Display.OSPRayScaleFunction = 'PiecewiseFunction'
glyph2Display.SelectOrientationVectors = 'None'
glyph2Display.ScaleFactor = 0.010000610351562501
glyph2Display.SelectScaleArray = 'None'
glyph2Display.GlyphType = 'Arrow'
glyph2Display.GlyphTableIndexArray = 'None'
glyph2Display.GaussianRadius = 0.000500030517578125
glyph2Display.SetScaleArray = ['POINTS', 'Normals']
glyph2Display.ScaleTransferFunction = 'PiecewiseFunction'
glyph2Display.OpacityArray = ['POINTS', 'Normals']
glyph2Display.OpacityTransferFunction = 'PiecewiseFunction'
glyph2Display.DataAxesGrid = 'GridAxesRepresentation'
glyph2Display.PolarAxes = 'PolarAxesRepresentation'
glyph2Display.SelectInputVectors = ['POINTS', 'Normals']
glyph2Display.WriteLog = ''
glyph2Display.ScaleTransferFunction.Points = [-0.9749279022216797, 0.0, 0.5, 0.0, 0.9749279022216797, 1.0, 0.5, 0.0]

# init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
glyph2Display.OpacityTransferFunction.Points = [-0.9749279022216797, 0.0, 0.5, 0.0, 0.9749279022216797, 1.0, 0.5, 0.0]

glyph2Display.SetRepresentationType('Wireframe')
glyph2Display.AmbientColor = [1.0, 0.0, 0.0]
glyph2Display.DiffuseColor = [1.0, 0.0, 0.0]








# Create a new 'SpreadSheet View'
spreadSheetView1 = CreateView('SpreadSheetView')
spreadSheetView1.ColumnToSort = ''
spreadSheetView1.BlockSize = 1024

# show data in view
liveProgrammableSource1Display = Show(liveProgrammableSource1, spreadSheetView1, 'SpreadSheetRepresentation')

# get layout
layout1 = GetLayoutByName("Layout #1")

# add view to a layout so it's visible in UI
AssignViewToLayout(view=spreadSheetView1, layout=layout1, hint=0)

# Properties modified on liveProgrammableSource1Display
liveProgrammableSource1Display.Assembly = ''

# get animation scene
animationScene1 = GetAnimationScene()

# get the time-keeper
timeKeeper1 = GetTimeKeeper()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# update the view to ensure updated data information
renderView1.Update()

# update the view to ensure updated data information
spreadSheetView1.Update()

# destroy spreadSheetView1
Delete(spreadSheetView1)
del spreadSheetView1

# close an empty frame
layout1.Collapse(2)

# set active view
SetActiveView(renderView1)

# create a new 'Table To Points'
tableToPoints1 = TableToPoints(registrationName='TableToPoints1', Input=liveProgrammableSource1)
tableToPoints1.XColumn = 'X'
tableToPoints1.YColumn = 'X'
tableToPoints1.ZColumn = 'X'

# Properties modified on tableToPoints1
tableToPoints1.YColumn = 'Y'
tableToPoints1.ZColumn = 'Z'

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
tableToPoints1Display.ScaleFactor = 1.3371082652686948
tableToPoints1Display.SelectScaleArray = 'None'
tableToPoints1Display.GlyphType = 'Arrow'
tableToPoints1Display.GlyphTableIndexArray = 'None'
tableToPoints1Display.GaussianRadius = 0.06685541326343473
tableToPoints1Display.SetScaleArray = [None, '']
tableToPoints1Display.ScaleTransferFunction = 'PiecewiseFunction'
tableToPoints1Display.OpacityArray = [None, '']
tableToPoints1Display.OpacityTransferFunction = 'PiecewiseFunction'
tableToPoints1Display.DataAxesGrid = 'GridAxesRepresentation'
tableToPoints1Display.PolarAxes = 'PolarAxesRepresentation'
tableToPoints1Display.SelectInputVectors = [None, '']
tableToPoints1Display.WriteLog = ''

# update the view to ensure updated data information
renderView1.Update()

#exec(open("./update.py").read()) # Important script for live update

    #exec(open("./Initialize.py").read())