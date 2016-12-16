import sys
# visit
sys.path.append("/home/neo/visit/2.11.0/linux-x86_64/lib/site-packages")
import visit as vs
vs.Launch()
vs.OpenDatabase("visit-data/noise.silo")
vs.AddPlot("Pseudocolor", "hardyglobal")
vs.AddOperator("Slice")
s = vs.SliceAttributes()
s.project2d = 0
s.originPoint = (0,5,0)
s.originType=s.Point
s.normal = (0,1,0)
s.upAxis = (-1,0,0)
vs.SetOperatorOptions(s)
vs.AddOperator("Reflect")
vs.DrawPlots()
# Now reflect before slicing. We’ll only get 1 slice plane
# instead of 2.
vs.DemoteOperator(1)
vs.DrawPlots()

d = input('Press anything to quit')

