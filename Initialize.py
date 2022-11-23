from paraview.simple import *
paraview.simple._DisableFirstRenderCameraReset()
buildingsstl = STLReader(registrationName='buildings.stl', FileNames=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/constant/triSurface/buildings.stl'])
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
liveProgrammableSource1.Script = """import numpy as np
# assuming data.csv is a CSV file with the 1st row being the names names for
# the columns


def GetUpdateTimestep(algorithm):
    \"\"\"Returns the requested time value, or None if not present\"\"\"
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)
    return outInfo.Get(executive.UPDATE_TIME_STEP()) \\
              if outInfo.Has(executive.UPDATE_TIME_STEP()) else None


req_time = GetUpdateTimestep(self)
data = np.genfromtxt("./csv/particles_positions_{0}.csv".format(str(int(req_time))), dtype=None, delimiter=\',\', autostrip=True)
current_time_file= open("./current_time.txt","w+")
current_time_file.write(str(int(req_time)))

output.GetInformation().Set(output.DATA_TIME_STEP(), req_time)
output.RowData.append(data[:,0], "X")
output.RowData.append(data[:,1], "Y")
output.RowData.append(data[:,2], "Z")
"""
liveProgrammableSource1.ScriptRequestInformation = """import glob
import os
import builtins
import re

# Code for 'RequestInformation Script'.
def setOutputTimesteps(algorithm, timesteps):
    executive = algorithm.GetExecutive()
    outInfo = executive.GetOutputInformation(0)

    outInfo.Remove(executive.TIME_STEPS())
    for timestep in timesteps:
        outInfo.Append(executive.TIME_STEPS(), timestep)

    outInfo.Remove(executive.TIME_RANGE())
    outInfo.Append(executive.TIME_RANGE(), timesteps[0])
    outInfo.Append(executive.TIME_RANGE(), timesteps[-1])

# As an example, let's say we have 4 files in the file series that we
# want to say are producing time 0, 10, 20, and 30


try:
    list_of_files = glob.glob('./csv/particles_positions_*.csv') # * means all if need specific format then *.csv
    number_of_files = builtins.max(list_of_files,key=os.path.getctime)
    last_timestep=re.findall(r'\d+',number_of_files)
    setOutputTimesteps(self, range(0,int(last_timestep[0])+1))
except:
    setOutputTimesteps(self, 0)

    
"""
liveProgrammableSource1.PythonPath = ''
liveProgrammableSource1.ScriptCheckNeedsUpdate = """
import time
import os

if not hasattr(self, "_my_time"):
  setattr(self, "_my_time", time.time())

t = time.time()
lastTime = getattr(self, "_my_time")
# adapt here to set the time (in sec) you want to wait between updates
if t - lastTime > 1 and os.path.exists(\'./csv/\'): # Does not update if no file are existing
  setattr(self, "_my_time", t)
  self.SetNeedsUpdate(True)
"""



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

exec(open("./update.py").read())

    #exec(open("./Initialize.py").read())