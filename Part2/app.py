# ISO Value -> Surface rendering
import vtk
from PyQt5 import QtCore, QtWidgets
import sys
from PyQt5.QtCore import QRect
from lib.dialog import chooseFolder
from rendering import VolumeRendering, SurfaceRendering
from GUI import  Ui_MainWindow
class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self) 
        self.renderingType =1
        self.directory = None
        self.state = False
    
        self.ui.actionNew_Folder.triggered.connect(self.NewFolder)
        self.ui.label.setText(str(self.ui.Slider.value()))
        self.ui.Slider.sliderReleased.connect(self.changeISO_value)
        self.ui.volume_button.clicked.connect(self.changeToVolRendering)
        self.ui.surface_button.clicked.connect(self.changeToSurfaceRendering) 
        
    def changeToVolRendering(self):
        self.renderingType = 1
        if self.state == True or self.directory == None:
            return
        self.state=True
        # excute volume rendering
        VolumeRendering(self.directory)

    def changeToSurfaceRendering(self):
        value=self.ui.Slider.value()
        self.state = False
        if self.renderingType == 0 or self.directory == None:
            return
        self.renderingType = 0
        # excute surface rendering
        SurfaceRendering(self.directory,iso_value=value)
        
    def changeISO_value(self):
        value=self.ui.Slider.value()
        self.ui.label.setText(str(self.ui.Slider.value()))
        if self.renderingType == 1 or self.directory == None :
            return
        SurfaceRendering(self.directory,iso_value=value)


    def NewFolder(self):
        self.directory = chooseFolder().one_file()
        if self.directory=="":
            chooseFolder().warnDialog("You didn't choose any data")
        else:
            self.ui.label_2.setText("Data is uploaded correctly")
        

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()
if __name__ == "__main__":
    main()

