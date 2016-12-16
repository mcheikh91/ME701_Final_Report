import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from MeshClass import *
from DataClass import *
from CaseClass import *

Loc = "OpenFoamCases/"

Files = ['elbow/','Coutte_Flow_40x40-FixedTemperature/','forwardStep/']

Loc = Loc + Files[0]

# Reading Mesh Data and Evaluating the initail points

case = Case()
case.loadOpenFoamFile(Loc)
case.print_output_vtk()

# visit
sys.path.append("/home/neo/visit/2.11.0/linux-x86_64/lib/site-packages")
import visit as vs
vs.Launch()
vs.OpenDatabase("Results/results-time-*.vtk database")
vs.AddPlot("Pseudocolor", 'X-Velocity')
vs.AddPlot("Mesh","X-Velocity")
vs.DrawPlots()

for time in range(vs.TimeSliderGetNStates()):
    vs.SetTimeSliderState(time)
    vs.SaveWindow()

d = input('Press anything to quit')

