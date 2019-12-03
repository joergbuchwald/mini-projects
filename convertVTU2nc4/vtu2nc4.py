from vtk import *
from vtk.util.numpy_support import vtk_to_numpy
import sys

class VTU2NC4(object):
    def __init__(self):
        pass


if __name__ == '__main__':
    if not len(sys.argv) == 3:
        print("Wrong number of arguments given.")
        ifile = sys.argv[1]
        ofile = sys.argv[2]
        if ifile.split(".")[1] == "vtu":
            pass
        elif ofile.split(".")[1] == "pvd":
            pass
        else:
            print("Wrong file extension.")
