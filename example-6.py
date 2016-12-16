import sys
# visit
sys.path.append("/home/neo/visit/2.11.0/linux-x86_64/lib/site-packages")
import visit as vs
vs.Launch()
vs.OpenDatabase("visit-data/noise.silo")
vs.AddPlot("Pseudocolor", "hgslice")
vs.AddPlot("Mesh", "Mesh2D")
vs.AddPlot("Label", "hgslice")
vs.DrawPlots()
print "The current view is:", vs.GetView2D()
# Get an initialized 2D view object.
v = vs.GetView2D()
v.windowCoords = (-7.67964, -3.21856, 2.66766, 7.87724)
vs.SetView2D(v)

d = input('Press anything to quit')

