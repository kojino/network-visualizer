import networkx as nx # Library for Graphs
import networks as model
import plotting as plot
import networkx as nx

G = model.Copying(125, 7, 7, 0.07, 0.05)
print "Done"
# G = model.ErdosRenyi(1000,0.15)
# print "Done"
# G = model.PrefferentialAttachement(500, 4)
# print "Done"
# G = model.StayConnected(11, 10)
# print "Done"
# G = model.OptimizeStayConnected(G, 5)
# print "Done"
# G = model.BilateralConnection(30, 0.8, 0.5)
# print "Done"
# G = model.OptimizeBilateralconnection(G, 5)
# print "Done"

# G = model.Copying(30, 7, 7, 0.07, 0.05)
# G = model.OptimizeStayConnected(G, 5)
#plot.PlotNetwork(G)


#plot.PlotNetwork(G, "abc")
#plot.PlotDegreeDistribution(G)
#plot.PlotClusterDistribution(G)

