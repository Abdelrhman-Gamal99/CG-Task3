from PyQt5 import QtWidgets

class chooseFolder(QtWidgets.QFileDialog) :
    def __init__(self) :
        super(chooseFolder,self).__init__()
        self.setFileMode(QtWidgets.QFileDialog.AnyFile)

    def one_file(self) :
        # directory = self.getOpenFileName(None,'select folder',__file__,'folder')
        directory = self.getExistingDirectory(None, 'Select folder:',__file__, QtWidgets.QFileDialog.ShowDirsOnly)
        return directory
    def warnDialog(self,message):
        window = QtWidgets.QMessageBox()
        window.setWindowTitle("error")
        window.setText(message)
        window.exec_()

    

