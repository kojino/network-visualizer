import networkx as nx # Library for Graphs
import networks as model
import plotting as plot
import pandas as pd
from collections import Counter
import networkx as nx

#G = model.Copying(125, 7, 7, 0.07, 0.05)
#G = model.ErdosRenyi(1000,0.025)
#G = model.PrefferentialAttachement(500, 4)
G = model.StayConnected(30, 10)
#G = model.BilateralConnection(30, 0.8, 0.5)

plot.PlotNetwork(G)

G = model.OptimizeStayConnected(G, 10)
#G = model.OptimizeBilateralconnection(G, 5)

plot.PlotNetwork(G)

#plot.PlotNetwork(G, "abc")
#plot.PlotDegreeDistribution(G)
#plot.PlotClusterDistribution(G, "abc")
