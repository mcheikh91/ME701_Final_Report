import sys
# visit
sys.path.append("/home/neo/visit/2.11.0/linux-x86_64/lib/site-packages")
import visit as vs
vs.Launch()
vs.OpenDatabase("visit-data/globe.silo")
vs.DefineScalarExpression("myvar", "sin(u) + cos(w)")
# Plot the scalar expression variable.
vs.AddPlot("Pseudocolor", "myvar")
vs.DrawPlots()
# Plot a vector expression variable.
vs.DefineVectorExpression("myvec", "{u,v,w}")
vs.AddPlot("Vector", "myvec")
vs.DrawPlots()

d = input('Press anything to quit')

