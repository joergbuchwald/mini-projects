import sys
from vtk import *

class VTU2ascii(object):
    def __init__(self, ifile, ofile):
        self.ifile = ifile
        self.ofile = ofile
    def readData(self):
        reader = vtkXMLUnstructuredGridReader()
        reader.SetFileName(self.ifile)
        reader.Update()
        self.data = reader.GetOutput()
    def writeData(self,datamode="ascii"):
        writer = vtkXMLUnstructuredGridWriter()
        writer.SetFileName(self.ofile)
        writer.SetInputData(self.data)
        if datamode == "binary":
            writer.SetDataModeToBinary()
        elif datamode == "appended":
            writer.SetDataModeToAppended()
        else:
            writer.SetDataModeToAscii()
        writer.Write()
if __name__ == '__main__':
    converter = VTU2ascii(sys.argv[1], sys.argv[2])
    converter.readData()
    converter.writeData()
