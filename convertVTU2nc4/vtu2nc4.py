import numpy as np
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
        self.filenames.append(ifile)
        self.t.append(timestep)
        reader = vtkXMLUnstructuredGridReader()
        reader.SetFileName(ifile)
        reader.Update()
        output = reader.GetOutput()
        self.data.append({})
        points = vtk_to_numpy(output.GetPoints().GetData())
        self.data[-1]['x'] = points[:,0]
        self.data[-1]['y'] = points[:,1]
        self.data[-1]['z'] = points[:,2]
        pointdata = output.GetPointData()
        fieldnames = []
        for i in np.arange(pointdata.GetNumberOfArrays()):
            fieldnames.append(pointdata.GetArrayName(i))
            fielddata = vtk_to_numpy(pointdata.GetArray(fieldnames[-1]))
            try:
                field_dim = fielddata.shape[1]
                for j in np.arange(field_dim):
                    self.data[-1][fieldnames[-1]+'_'+str(j)] = fielddata[:,j]
            except IndexError:
                field_dim = 1
                self.data[-1][fieldnames[-1]] = fielddata[:]
        return True
    def readPVDInput(self,ifile):
        pass
    def writeNC4Output(self,ofile):
        datafile = nc4.Dataset(ofile,'w',format='NETCDF4')
        datafile.createDimension('pos',None)
        datafile.createDimension('t',len(self.t))
        t = datafile.createVariable('t', np.float32, ('t',))
        x = datafile.createVariable('x', np.float32, ('pos',))
        y = datafile.createVariable('y', np.float32, ('pos',))
        z = datafile.createVariable('z', np.float32, ('pos',))
        t[:] = self.t
        x[:] = self.data[-1]['x']
        z[:] = self.data[-1]['x']
        y[:] = self.data[-1]['x']
        var = {}
        for variable in self.data[-1]:
            if not (variable == 'x' or variable == 'y' or variable == 'z'):
                var[variable] = datafile.createVariable(variable, np.float32, ('pos','t'))
        for timestep in self.t:
            for variable in var:
                var[variable][:,timestep] = self.data[timestep][variable]
        datafile.close()
        return True
    def writeXDMFOutput(self,ofile):
        reader = []
        multiblock = vtkMultiBlockDataSet()
        for i, filename in enumerate(self.filenames):
            reader.append(vtkXMLUnstructuredGridReader())
            reader[i].SetFileName(filename)
            reader[i].Update()
            multiblock.SetBlock(i,reader[i].GetOutput())
        try:
            writer = vtkXdmfWriter()
        except:
            print("The vtkXdmf module is probably not installed. Please check!")
            raise RuntimeError
        writer.SetFileName(ofile)
        writer.SetInputData(multiblock)
        writer.WriteAllTimeStepsOn()
        writer.Write()

if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print("Wrong number of arguments given.")
        raise RuntimeError
    convert = VTU2NC4()
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    if input_file.split(".")[1] == "vtu":
        convert.readVTUInput(input_file,0)
    elif input_file.split(".")[1] == "pvd":
        convert.readPVDInput(input_file)
    else:
        print("Not supported file extension.")
        raise RuntimeError
    if output_file.split(".")[1] == "xmdf":
        convert.writeXDMFOutput(output_file)
    elif (output_file.split(".")[1] == "nc4"
            or output_file.split(".")[1] == "h5"
            or output_file.split(".")[1] == "nc"):
        convert.writeNC4Output(output_file)
