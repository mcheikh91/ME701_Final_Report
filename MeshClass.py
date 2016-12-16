import numpy as np
import re
import math

class Mesh(object) :

    def __init__(self):        
        self.points     = []
        self.faces      = []
        self.owners     = []
        self.neighbours = [] 
        self.cells_faces= []
        self.cells      = []
        self.face_center= []
        self.face_area  = []
        self.face_normal= []
        self.cell_center= []
        self.cell_volume= []
        self.type       = 'none'

    def __str__(self):  
        if self.type == 'openFoam':
            S1 = "# of points: \t %i \n"     % len(self.points)
            S2 = "# of faces: \t %i \n"      % len(self.faces)
            S3 = "# of owners: \t %i \n"     % len(self.owners)
            S4 = "# of neighbours: \t %i\n" % len(self.neighbours)
            S5 = "Data type: \t %s" % self.type    
            return S1+S2+S3+S4+S5
        else:
            return "Empty Mesh"

    def ReadOpenFoamMesh(self,Loc): 
        ''' 
        This method reads an openfoam mesh and save it in self
        '''

        ##### Reading the Point Data #####
        f = open(Loc+'points','r')

        Lines = f.readlines()

        n_pts = int(Lines[18])

        Points = []

        FirstPoint = 20
        for i in range(n_pts):
            s =  Lines[FirstPoint+i].split()
            x = float(s[0].split('(')[1])
            y = float(s[1])
            z = float(s[2].split(')')[0])
            Points.append([x,y,z])

        f.close()

        ##### Reading Faces #####

        f = open(Loc+'faces','r')

        Lines = f.readlines()

        n_faces = int(Lines[18])

        Faces = []

        FirstFace = 20
        for i in range(n_faces):
            s =  re.findall('\d+',Lines[FirstFace+i])
            s.pop(0) # Removes the first element from the list
            s = map(int,s)
            Faces.append(s)

        f.close()

        ##### Reading Owner Cells #####

        f = open(Loc+'owner','r')

        Lines = f.readlines()

        n_owner = int(Lines[19])

        Owner = []

        FirstOwner = 21
        for i in range(n_owner):
            s =  re.findall('\d+',Lines[FirstOwner+i])
            s = int(s[0])
            Owner.append(s)

        f.close()

        ##### Reading Neighbour Cells #####

        f = open(Loc+'neighbour','r')

        Lines = f.readlines()

        n_neigh = int(Lines[19])

        Neigh = []

        FirstNeighbour = 21
        for i in range(n_neigh):
            s =  re.findall('\d+',Lines[FirstNeighbour+i])
            s = int(s[0])
            Neigh.append(s)

        f.close()

        self.points = Points
        self.faces  = Faces
        self.owners  = Owner
        self.neighbours  = Neigh
        self.type = 'openFoam'
        ''''
        try:
            f = open(Loc+'cells','r')
        except:
            print "Cells list not found"
        else:
            print "Cells list is found"
            Lines = f.readlines()
            num_cells = int(Lines[18])
            cells = []

            FirstCell = 20

            for i in range(num_cells):
                s =  re.findall('\d+',Lines[FirstCell+i])
                s.pop(0)
                points = []
                for point in s:
                    points.append(int(point))
                cells.append(points)
            f.close()
            self.cells_faces = cells
        '''

    def EvaluateCellFaces(self):
        '''
        This method creates a cell list, with the index of the list 
        refering to each cell and the elements of the list refers to the
        faces that make up each cell.
        '''
        cells_faces = [ [] for i in range(max(self.owners)+1)]
        face_number = 0
        for o in self.owners: # o represents the owner cell of the face
            cell = cells_faces[o]
            cell.append(face_number)
            cells_faces[o] = cell
            face_number = face_number + 1

        face_number = 0
        for n in self.neighbours: # o represents the neighbour cell of the face
            cell = cells_faces[n]
            cell.append(face_number)
            cells_faces[n] = cell
            face_number = face_number + 1

        self.cells_faces = cells_faces

    def EvaluateCellPoints(self):
        '''
        This method creates a cell list, with the index of the list 
        refering to each cell and the elements of the list refers to the
        points that bound the vertices of each cell.
        '''        
        cells = []

        # cells is a list containing the points of each cell
        #    with the cell number being the index of the list

        for cell in self.cells_faces:
            c = []        
            for face in cell:
                for point in self.faces[face]:
                    try:
                        c.index(point) # Trys to see if the point is in the array
                    except:
                        c.append(point) # adds the point if it is not in the array
            cells.append(c)
        self.cells = cells

    def ReorderCellPoints(self):
        '''
        This method reorder the points of the cell in a way,
        that allows visit to accuretly draw the cells.
        The method used is based on the shortest distance.
        '''
        cells  = self.cells
        points = self.points
        new_cells = []
        for cell in cells:
            c = list(cell) # convert from ndarray to list
            new_c = []
            if len(c) == 8:
                new_c.append(c[0])
                while len(c) > 1:
                    if len(new_c)!= 4:
                        main_pt = c.pop(0)
                    else:
                        c.pop(0)
                        main_pt = new_c[0]
                    main_cr=points[main_pt]
                    dist = float('inf')
                    for point in c:
                        cr = points[point]
                        rel_dist = 0
                        for i in range(len(cr)):
                            rel_dist = rel_dist + (cr[i] - main_cr[i])**2.0              
                        rel_dist = math.sqrt(rel_dist)
                        if rel_dist < dist:
                            dist = rel_dist
                            sec_pt = point
                            index = c.index(point)
                    old_pt = c[0]
                    c[0] = sec_pt
                    c[index] = old_pt
                    new_c.append(sec_pt)
            else:
                main_pt = c[0];
                main_pt_z = points[main_pt][2] # This is the z of the main point 
                plain1 = [c[0]]
                plain2 = []
                c.pop(0)
                for point in c:
                    if points[point][2] == main_pt_z: # have the same z
                        plain1.append(point)
                    else:
                        plain2.append(point)
                new_c = plain1[:]
                for point1 in plain1:
                    c1 = points[point1]
                    for point2 in plain2:
                        c2 = points[point2]
                        if c1[0] == c2[0] and c1[1] == c2[1]: # comparing the x-component of both points
                            new_c.append(point2) 

            new_cells.append(new_c)
        self.cells = new_cells                        

    def CalculateFaceCenter(self):
        # Not Defined Yet
        pass

    def CalculateFaceArea(self):
        # Not Defined Yet
        pass

    def CalculateCellCenter(self):
        # Not Defined Yet
        pass

    def CalculateCellVolume(self):
        # Not Defined Yet
        pass

    def CalculateFaceNormal(self):
        # Not Defined Yet
        pass        
        


    
