from vtk import *
from vtk.util.numpy_support import vtk_to_numpy
import netCDF4 as nc4
import sys


class VTU2NC4(object):
    def __init__(self):
        self.filenames = []
        self.data = []
        self.t = []
    def readVTUInput(self,ifile,timestep):
        self.ifilenames.append(ifile)
        self.t.append(timestep)
        reader = vtk.vtkXMLUnstructuredGridReader()
        reader.SetFileName(ifile)
        reader.Update()
        self.data.append({})
        points = vtk_to_numpy(output.GetPoints().GetData())
        self.data[-1]['x'] = points[:,0]
        self.data[-1]['y'] = points[:,1]
        self.data[-1]['z'] = points[:,2]
        pointdata = output.GetPointData()
        fieldnames = []
        for i in np.arange(pointdata.GetNumberOfArrays()):
            liste.append(pointdata.GetArrayName(i))
        self.data[-1]
    def setPVDInput(self,ifile):
        pass
    def writeNC4Output(self,ofile):
        pass
    def writeXDMFOutput(self,ofile):
        pass


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print("Wrong number of arguments given.")
        raise RuntimeError
    convert = VTU2NC4()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if input_file.split(".")[1] == "vtu":
        convert.setVTUInput(input_file)
    elif input_file.split(".")[1] == "pvd":
        convert.setPVDInput(input_file)
    else:
        print("Not supported file extension.")
        raise RuntimeError
    if output_file.split(".")[2] == "xmdf":
        pass
    elif output_file.split(".")[2] == "nc4" or convert.ofile.split(".")[2] == "h5":
        pass
