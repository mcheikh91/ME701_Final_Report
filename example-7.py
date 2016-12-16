import sys
# visit
sys.path.append("/home/neo/visit/2.11.0/linux-x86_64/lib/site-packages")
import visit as vs
vs.Launch()
vs.OpenDatabase("visit-data/noise.silo")
vs.AddPlot("Pseudocolor", "hardyglobal")
vs.AddPlot("Mesh", "Mesh")
vs.DrawPlots()
v = vs.GetView3D()
print "The view is: ", v
v.viewNormal = (-0.571619, 0.405393, 0.713378)
v.viewUp = (0.308049, 0.911853, -0.271346)
vs.SetView3D(v)

d = input('Press anything to quit')

