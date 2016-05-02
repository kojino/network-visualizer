import networkx as nx # Library for Graphs
import networks as model
import plotting as plot
import sys

#G = model.Copying(400,7,7, 0.07, 0.05)
G = model.ErdosRenyi(500,0.0125)
#print plot.PlotNetwork(G)

plot.PlotDegreeDistribution(G)
