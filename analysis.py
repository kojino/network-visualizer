import networkx as nx # Library for Graphs
import networks as model
import plotting as plot
import pandas as pd
import numpy as np
import networkx as nx


# Erdos-Renyi graph:

ErdosRenyi = pd.DataFrame(np.nan, 
			index=[], 
			columns=['Nodes', 'p', 'graph', 'degreeDist', 'clusterDist'])

for i in range(1, 25 + 1):
	print "Iteration %s" % i
	G = model.ErdosRenyi(1000,float(i)/float(100))
	degreeDist = model.DegreeDistribution(G)
	clusterDist = model.ClusterDistribution(G)
	print degreeDist
	print clusterDist
	plot.PlotDegreeDistribution(G)
	#ErdosRenyi.loc[i-1] = [1000, float(i)/float(100), 3, degreeDist, 5]
	#[1000, i/100, G, degreeDist, clusterDist]

#ErdosRenyi.to_csv('ErdosRenyi.csv', sep=';')

"""

# Prefferential Attachement:

PrefferentialAttachement = pd.DataFrame(np.nan, 
							index=[], 
							columns=['Nodes', 'NodesAtStep', 'graph', 'degreeDist', 'clusterDist'])

for i in range(1, 25 + 1):
	G = model.PrefferentialAttachement(1000,i)
	PrefferentialAttachement.loc[i] = [1000, 
						i, 
						G, 
						model.DegreeDistribution(G),
						model.ClusterDistribution(G)]

PrefferentialAttachement.to_csv('PrefferentialAttachement.csv', sep=';')

# Copying model:

Copying = pd.DataFrame(np.nan, 
					index=[], 
					columns=['Nodes', 'NSet', 'NNeighbor', 'PSet', 'PNeighbor', 'graph', 'degreeDist', 'clusterDist'])

for NSet in [8, 16, 24, 32]:
	for NNeighbor in [8, 16, 24, 32]:
		for PSet in [0.0125, 0.05, 0.1, 0.15]:
			for PNeighbor in [0.0125, 0.05, 0.1, 0.15]:
				G = model.Copying(1000, NSet, NNeighbor, PSet, PNeighbor)
				Copying.loc[i] = [1000, 
					NSet, NNeighbor, PSet, PNeighbor, 
					G, 
					model.DegreeDistribution(G),
					model.ClusterDistribution(G)]

Copying.to_csv('Copying.csv', sep=';')

# StayConnected Game:

StayConnected = pd.DataFrame(np.nan, 
					index=[], 
					columns=['Nodes', 'isOptimized', 'cost', 'graph'])

for cost in range(1, 25):
	G = model.StayConnected(30, cost)
	StayConnected.loc[i] = [30, False, cost, G]
	G = model.OptimizeStayConnected(G, 5)
	StayConnected.loc[i] = [30, True, cost, G]

StayConnected.to_csv('StayConnected.csv', sep=';')	

# Bilateral Connection Game:

BilateralConnection = pd.DataFrame(np.nan, 
					index=[], 
					columns=['Nodes', 'isOptimized', 'delta', 'cost', 'graph'])

for delta in [0.5, 0.6, 0.7, 0.8]:
	for cost in [0.2, 0.4, 0.8, 1.2]:
		G = model.BilateralConnection(30, delta, cost)
		BilateralConnection.loc[i] = [30, False, delta, cost, G]
		G = model.OptimizeBilateralconnection(G)
		BilateralConnection.loc[i] = [30, True, delta, cost, G]

BilateralConnection.to_csv('BilateralConnection.csv', sep=';')	

"""