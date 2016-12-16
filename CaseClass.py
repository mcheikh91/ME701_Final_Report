import numpy as np
import re
import os
import sys
from MeshClass import *
from DataClass import *

class Case(object):
    def __init__(self):
        self.mesh = Mesh()
        self.data = Data()

    def getData(self, data):
        self.data = data

    def getMesh(self, mesh):
        self.mesh = mesh

    def loadOpenFoamFile(self,loc):
        loc_mesh = loc + "/constant/polyMesh/"
        #print loc_mesh
        mesh = Mesh()
        mesh.ReadOpenFoamMesh(loc_mesh)
        if not mesh.cells:
            print "Cell list is being created"
            mesh.EvaluateCellFaces()
            mesh.EvaluateCellPoints()
            mesh.ReorderCellPoints()
        self.mesh = mesh
        for filename in os.listdir(loc): # Looping over all the files in the choosen directory    
            if filename == 'constant':
                pass
            elif filename == 'system':
                pass
            else:
                time = eval(filename)
                self.data.ReadVariable(loc,time)

    def print_output_vtk(self):
        mesh = self.mesh    
        data = self.data
        time = data.time
        
        points = mesh.points
        n_pt  = len(points)
        cells  = mesh.cells 
        n_cel  = len(cells) 

        step = 0
        for time_step in time:
              
            str1 = "Results/results-time-"
            str2 = str(time_step)
            str3 = ".vtk"
            step_header = "".join((str1,str2,str3))
            f_out = open (step_header, 'w') 
            print >> f_out, "# vtk DataFile Version 2.0"
            print >> f_out, str2, "-th Step"
            print >> f_out, "ASCII"
            print >> f_out, "DATASET UNSTRUCTURED_GRID"
            print >> f_out, "POINTS", n_pt, "float"

            for p in points:
                print >> f_out, p[0], p[1], p[2]

            cell_list_size = n_cel
            cell_type = []
            for c in cells:
                if len(c) == 8:
                    cell_type.append(12)
                else:
                    cell_type.append(13)
                for p in c:
                    cell_list_size = cell_list_size + 1

            print >> f_out, "CELLS", n_cel, cell_list_size
            for c in cells:
                f_out.write( str(len(c)) )
                for i in range(len(c)):
                    f_out.write(' '+str(c[i]))
                f_out.write('\n')
            print >> f_out, "CELL_TYPES", n_cel
            
            for c_t in cell_type:
                print >> f_out, str(c_t)

            print >> f_out, "CELL_DATA", n_cel

            ####################################
            try:
                data.variables[step].rho
            except:
                pass
            else:
                rho  = data.variables[step].rho
                print >> f_out, "SCALARS Density float 1"
                print >> f_out, "LOOKUP_TABLE default"
                for r in rho:
                    print >> f_out, r 

            
            #################################### 
            try:
                U    = data.variables[step].U      
            except:
                pass
            else:
                print >> f_out, "SCALARS X-Velocity float 1"
                print >> f_out, "LOOKUP_TABLE default"
                for u in U:
                    print >> f_out, u[0]
                print >> f_out, "SCALARS Y-Velocity float 1"
                print >> f_out, "LOOKUP_TABLE default"
                for u in U:
                    print >> f_out, u[1]
                print >> f_out, "SCALARS Z-Velocity float 1"
                print >> f_out, "LOOKUP_TABLE default"
                for u in U:
                    print >> f_out, u[2]

            ####################################
            try:
                p    = data.variables[step].p 
            except:
                pass
            else:
                print >> f_out, "SCALARS Pressure float 1"
                print >> f_out, "LOOKUP_TABLE default"
                for pr in p:
                    print >> f_out, pr
            ####################################
            try:
                temp = data.variables[step].T
            except:
                pass
            else:
                print >> f_out, "SCALARS Temperature float 1"
                print >> f_out, "LOOKUP_TABLE default"
                for te in temp:
                    print >> f_out, te
            ####################################
            f_out.close()
            step = step + 1
