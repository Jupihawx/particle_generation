from paraview.simple import *
import time
import pandas as pd
import builtins
import numpy as np


Connect('localhost') # Connect to the local server launched through the terminal (see README)



# create a new 'STL Reader'
buildingsstl = STLReader(registrationName='buildings.stl', FileNames=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/constant/triSurface/buildings.stl'])

# get active view
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

# create a new 'XML Unstructured Grid Reader'
basesAndMean_total_19basesvtu = XMLUnstructuredGridReader(registrationName='BasesAndMean_total_19bases.vtu', FileName=['/home/boris/OpenFOAM/boris-v2206/run/ROM/Own_code/BasesAndMean_total_19bases.vtu'])
basesAndMean_total_19basesvtu.CellArrayStatus = ['U']
basesAndMean_total_19basesvtu.PointArrayStatus = ['U', 'Mean', 'Base0', 'Base1', 'Base2', 'Base3', 'Base4', 'Base5', 'Base6', 'Base7', 'Base8', 'Base9', 'Base10', 'Base11', 'Base12', 'Base13', 'Base14', 'Base15', 'Base16', 'Base17', 'Base18']

# Properties modified on basesAndMean_total_19basesvtu
basesAndMean_total_19basesvtu.CellArrayStatus = []
basesAndMean_total_19basesvtu.PointArrayStatus = ['Base0', 'Base1', 'Base10', 'Base11', 'Base12', 'Base13', 'Base14', 'Base15', 'Base16', 'Base17', 'Base18', 'Base2', 'Base3', 'Base4', 'Base5', 'Base6', 'Base7', 'Base8', 'Base9', 'Mean']
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

# update the view to ensure updated data information
renderView1.Update()

# hide data in view
Hide(basesAndMean_total_19basesvtu, renderView1)

# create a new 'Calculator'
calculator1 = Calculator(registrationName='Calculator1', Input=basesAndMean_total_19basesvtu)
calculator1.Function = ''

# Properties modified on calculator1
calculator1.Function = '3*Base0'

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

# hide data in view
Hide(basesAndMean_total_19basesvtu, renderView1)

# update the view to ensure updated data information
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

# set scalar coloring
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




##################################################
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
from scipy import interpolate
from scipy.optimize import curve_fit



angles = [0, 18, 37, 56, 75, 94, 113, 132 ,151 ,170, 189, 208, 227, 246, 265, 284, 303, 322, 341]
angles.append(360)

Coeffs = pd.read_csv("/home/boris/OpenFOAM/boris-v2206/run/ROM/Own_code/coeffs.csv",header=None)
Coeffs=Coeffs.to_numpy()
Coeffs=np.vstack((Coeffs,Coeffs[0,:]))


f_interpolated=[]
for i in range(0,19):

    f_interpolated.append(interpolate.interp1d(angles, Coeffs[:,i], 'cubic'))


x = np.linspace(min(angles), max(angles), 360)


i=0
for i in range(0,360):
    Text=["Mean"]
    nb_bases=20
    coeffs_interpolated=[]

    coeffs_interpolated=[f(i) for f in f_interpolated]

    i=0
    for i in range(nb_bases-1):
        if coeffs_interpolated[i] > 0:
            Text.append("+")
            Text.append("{0}*Base{1}".format(coeffs_interpolated[i],i))
                         
        if coeffs_interpolated[i] < 0:
            Text.append("{0}*Base{1}".format(coeffs_interpolated[i],i))

    calculator1.Function = '{0}'.format(''.join(Text))   
    UpdatePipeline()
    slice1 = GetActiveSource()
    renderView1 = GetActiveViewOrCreate('RenderView')
    slice1Display = GetDisplayProperties(slice1, view=renderView1)

    slice1Display.RescaleTransferFunctionToDataRange(False, True)
    resultLUT = GetColorTransferFunction('Result')
    resultPWF = GetOpacityTransferFunction('Result')
    resultTF2D = GetTransferFunction2D('Result')

    

