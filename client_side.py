# Need to create a server on a terminal through : ./pvserver --multi-clients
# Then connect to the server through paraview_built

from paraview.simple import *
import time


Connect('localhost')

wind_directions=[0,37,75,170,303]

for wind_direction in wind_directions:

    try:
        Delete(afoam)
        Delete(slice1)

    except:
        pass
    wind_value=5
    
    afoam = XMLMultiBlockDataReader(registrationName='afoam', FileName=['/home/boris/OpenFOAM/boris-v2206/run/Clean/Marina_Particles/cases/val_{0}_ang_{1}.vtm'.format(wind_value,wind_direction)]) # Depending on the slider position, the simulator with select a vtm file representing the field at that given angle
    slice1 = Slice(registrationName='Slice1', Input=afoam)
    slice1.SliceType = 'Plane'
    slice1.HyperTreeGridSlicer = 'Plane'
    slice1.SliceOffsetValues = [0.0]
    slice1.SliceType.Origin = [0.0, 0.0, 100.0]
    slice1.SliceType.Normal = [0.0, 0.0, 1.0]
    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')
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


    renderView1.Update()
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

    time.sleep(5)