import numpy as np
import re
import os

class Variable(object):
    def __init__(self):
        pass

    def addData(self,filename,data):
        if filename == 'rho':   # density
            self.rho = data
        elif filename == 'U':   # velocity
            self.U = data
        elif filename == 'T':   # temperature
            self.T = data
        elif filename == 'p':   # pressure
            self.p = data
        elif filename == 'nu':  
            self.nu = data
        else:                   # Unknown Data
            self.unknown_data = data
            self.unknown_name = filename

class Data(object) :

    def __init__(self):
        self.constants = []
        self.variables = []
        self.time      = []

    def ReadVariable(self,Loc,Time):
        Loc_Data = Loc +'/'+ str(Time)+'/'

        if Time != 0:

            V = Variable()
            
            for filename in os.listdir(Loc_Data): # Looping over all the files in the choosen directory    
                if filename != 'uniform':
                    f = open(Loc_Data+filename,'r') # open filename
        
                    Lines = f.readlines()
                    Type = re.findall('scalar|vector',Lines[19])[0]
                    n_pts = int(Lines[20])

                    data = []

                    FirstData = 22
                    for i in range(n_pts):
                        if Type == 'scalar':
                            s = float(Lines[FirstData+i])
                            data.append(s)
                        else: 
                            s =  Lines[FirstData+i].split(' ')
                            x = float(s[0].split('(')[1])
                            y = float(s[1])
                            z = float(s[2].split(')')[0])
                            data.append([x,y,z])

                    f.close()

                    V.addData(filename,data)

            self.variables.append(V)
            self.time.append(Time)    


                 

