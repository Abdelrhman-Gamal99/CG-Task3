import vtk
from vtk.util.misc import vtkGetDataRoot

# volume rendering
def VolumeRendering(directory):
    print(directory)
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)


    v16 = vtk.vtkDICOMImageReader()
    v16.SetDirectoryName(directory)


    volumeMapper = vtk.vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(v16.GetOutputPort())
    volumeMapper.SetBlendModeToComposite()
    volumeColor = vtk.vtkColorTransferFunction()
    volumeColor.AddRGBPoint(0,    0.0, 0.0, 0.0)
    volumeColor.AddRGBPoint(500,  1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
    volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)



    volumeScalarOpacity = vtk.vtkPiecewiseFunction()
    volumeScalarOpacity.AddPoint(0,    0.00)
    volumeScalarOpacity.AddPoint(500,  0.15)
    volumeScalarOpacity.AddPoint(1000, 0.15)
    volumeScalarOpacity.AddPoint(1150, 0.85)
    volumeGradientOpacity = vtk.vtkPiecewiseFunction()
    volumeGradientOpacity.AddPoint(0,   0.0)
    volumeGradientOpacity.AddPoint(90,  0.5)
    volumeGradientOpacity.AddPoint(100, 1.0)
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(volumeColor)
    volumeProperty.SetScalarOpacity(volumeScalarOpacity)
    volumeProperty.SetGradientOpacity(volumeGradientOpacity)
    volumeProperty.SetInterpolationTypeToLinear()
    volumeProperty.ShadeOn()
    volumeProperty.SetAmbient(0.4)
    volumeProperty.SetDiffuse(0.6)
    volumeProperty.SetSpecular(0.2)
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    # Finally, add the volume to the renderer
    ren.AddViewProp(volume)
    camera =  ren.GetActiveCamera()
    c = volume.GetCenter()
    camera.SetFocalPoint(c[0], c[1], c[2])
    camera.SetPosition(c[0] + 400, c[1], c[2])
    camera.SetViewUp(0, 0, -1)

    # Increase the size of the render window
    renWin.SetSize(640, 480)

    # Interact with the data.
    iren.Initialize()
    renWin.Render()
    iren.Start()

# Surface rendering
skinExtractor = vtk.vtkContourFilter()
def SurfaceRendering(directory, iso_value=500):
    aRenderer = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(aRenderer)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    v16 = vtk.vtkDICOMImageReader()
    v16.SetDirectoryName(directory)

    skinExtractor.SetInputConnection(v16.GetOutputPort())
    skinExtractor.SetValue(0, iso_value)
    skinNormals = vtk.vtkPolyDataNormals()
    skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
    skinNormals.SetFeatureAngle(60.0)
    skinMapper = vtk.vtkPolyDataMapper()
    skinMapper.SetInputConnection(skinNormals.GetOutputPort())
    skinMapper.ScalarVisibilityOff()
    skin = vtk.vtkActor()
    skin.SetMapper(skinMapper)


    
    aCamera = vtk.vtkCamera()
    aCamera.SetViewUp(0, 0, -1)
    aCamera.SetPosition(0, 1, 0)
    aCamera.SetFocalPoint(0, 0, 0)
    aCamera.ComputeViewPlaneNormal()

   
    aRenderer.AddActor(skin)
    aRenderer.SetActiveCamera(aCamera)
    aRenderer.ResetCamera()
    aCamera.Dolly(1)

    # Set a background color for the renderer and set the size of the
    # render window (expressed in pixels).
    aRenderer.SetBackground(0, 0, 0)
    renWin.SetSize(640, 480)

   
    aRenderer.ResetCameraClippingRange()

    # Interact with the data.
    iren.Initialize()
    renWin.Render()
    iren.Start()
