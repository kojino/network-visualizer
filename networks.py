import requests
import numpy as np
import pandas as pd
import networkx as nx # Library for Networks
import random # Random number generating function
import utils
import plotting as plot
import operator
import math as m
from collections import Counter

def ErdosRenyi(N, p):
	if p > 1:
		p = 1
	G = nx.erdos_renyi_graph(N, p)
	G.graph['p'] = p
	G.graph['name'] = "Erdos Renyi"

	return nx.erdos_renyi_graph(N, p)

def PrefferentialAttachement(N, addNodes):
	initNodes = 2 * addNodes + 1
	G = nx.complete_graph(initNodes)
	G.graph['addNodes'] = addNodes
	G.graph['name'] = "Prefferential Attachement"

	# Adding other nodes
	for i in range(initNodes, N):
	    degrees = [] # Initalizing empty degree list

	    # Puttin each node name into the the degree list
	    # Proportional to its degree.
	    for node, neighbors in enumerate(G.adjacency_list()):
	        [degrees.append(x) for x in [node]*len(neighbors)]

	    connected = 0
	    while connected < addNodes:
	        to_connect = random.choice(degrees) # picking random element
	        degrees = [x  for x in degrees if x != to_connect] # removing connected neighbors
	        G.add_edge(i, to_connect) # Adding edge
	        connected += 1

	return G

def Copying(N, NSet, NNeighbor, PSet, PNeighbor):
	initNodes = NSet + NNeighbor + 1
	G = nx.complete_graph(initNodes)

	G.graph['NSet'] = NSet
	G.graph['NNeighbor'] = NNeighbor
	G.graph['PSet'] = PSet
	G.graph['PNeighbor'] = PNeighbor
	G.graph['name'] = 'Copying Model'

	for i in range(initNodes, N):

		# Random subset of existing nodes
		randomSet = random.sample(G.nodes(), NSet)

		# Creating set of random subset neighborhood
		neighbors = []
		for j in randomSet:

			for neighbor in G.adjacency_list()[j]:
				neighbors.append(neighbor)

		neighbors = utils.remove_duplicates(neighbors)

		# Trimming neighborhood if it is too large
		if len(neighbors) > NNeighbor:
			neighbors = random.sample(neighbors, NNeighbor)

		G.add_node(i)

		# Forming edge with subset
		for node in randomSet:
			if random.random() < PSet:
				G.add_edge(i, node)

		# Forming edge with neighborhood
		for node in neighbors:
			if random.random() < PNeighbor:
				G.add_edge(i, node)

	return G

def StayConnected(N, c):
	if N <= 10:
		G = nx.complete_graph(1)
		startNode = 1
	else:
		G = nx.connected_watts_strogatz_graph(int(N/5) + 1, int(N/8) + 1, random.random()/4, 50)
		startNode = int(N/5) + 1
	G.graph['cost'] = c
	G.graph['name'] = 'Stay Connected'
	G.graph['isOptimized'] = False


	# Setting random sponsorship structure for inital edges
	for edge in G.edges():
		if random.random() <= 0.5:
			G.edge[edge[0]][edge[1]]['sponsor'] = edge[0]
			G.edge[edge[1]][edge[0]]['sponsor'] = edge[0]
		else:
			G.edge[edge[0]][edge[1]]['sponsor'] = edge[1]
			G.edge[edge[1]][edge[0]]['sponsor'] = edge[1]

	for i in range(startNode, N):
		existingNodes = list(G.nodes())
		random.shuffle(existingNodes)

		optimalToConnect = 0
		optimalUtility = float("-inf")

		for nodeToConnect in existingNodes:
			G.add_edge(i, nodeToConnect)

			sumPathLengths = 0
			for node in G.nodes():
				if nx.has_path(G, i ,node):
					sumPathLengths -= nx.dijkstra_path_length(G, i, node)

			if sumPathLengths > optimalUtility:
				optimalToConnect = nodeToConnect
				optimalUtility = sumPathLengths

			G.remove_edge(i, nodeToConnect)

		G.add_edge(i, optimalToConnect)
		G.edge[i][optimalToConnect]['sponsor'] = i
		G.edge[optimalToConnect][i]['sponsor'] = i

		existingNodes.remove(optimalToConnect)

		for nodeToConnect in existingNodes:
			G.add_edge(i, nodeToConnect)
			G.edge[i][nodeToConnect]['sponsor'] = i
			G.edge[nodeToConnect][i]['sponsor'] = i

			sumPathLengths = 0
			for node in G.nodes():
				if nx.has_path(G, i ,node):
					sumPathLengths -= nx.dijkstra_path_length(G, i, node)

			if sumPathLengths - optimalUtility > c:
				optimalUtility = sumPathLengths
			else:
				G.remove_edge(i, nodeToConnect)

	return G

def BilateralConnection(N, delta, c):
	if N <= 10:
		G = nx.complete_graph(1)
	else:
		G = nx.connected_watts_strogatz_graph(int(N/5) + 1, int(N/8) + 1, random.random()/4, 50)

	G.graph['cost'] = c
	G.graph['delta'] = delta
	G.graph['name'] = 'Bilateral Connection'
	G.graph['isOptimized'] = False

	for i in range(int(N/5) + 1, N):
		G.add_node(i) # Adding a node to the graph

		existingNodes = list(G.nodes())
		random.shuffle(existingNodes)

		# Calculating utility of connecting to each agent

		utilities = {} # Dictionary to store utilities
		for nodeToConnect in existingNodes:
			G.add_edge(i, nodeToConnect)

			utility = 0
			for node in G.nodes():
				if node != i and nx.has_path(G, i, node):
					utility += delta ** nx.dijkstra_path_length(G, i, node)

			utilities[nodeToConnect] = utility
			G.remove_edge(i, nodeToConnect)

		# Sorting agents by additional utility:
		utilitiesSorted = sorted(utilities.items(), key=operator.itemgetter(1), reverse=True)
		# Creating ranking list in descending order:
		ranking = [key[0] for key in utilitiesSorted]

		for node in ranking:
			# First determine whether new arrived node whant to form
			# an edge with this neighbor:
			initialUtilityNew = 0
			newUtilityNew = 0
			initialUtilityExist = 0
			newUtilityExist = 0

			for neighbor in G.nodes():
				if neighbor != i and nx.has_path(G, i, neighbor):
					initialUtilityNew += delta ** nx.dijkstra_path_length(G, i, neighbor)

			for neighbor in G.nodes():
				if neighbor != node and nx.has_path(G, node, neighbor):
					initialUtilityExist += delta ** nx.dijkstra_path_length(G, node, neighbor)

			# Add edge and calculate new utility:
			G.add_edge(i, node)
			for neighbor in G.nodes():
				if neighbor != node and nx.has_path(G, node, neighbor):
					newUtilityExist += delta ** nx.dijkstra_path_length(G, node, neighbor)

			for neighbor in G.nodes():
				if neighbor != i and nx.has_path(G, i, neighbor):
					newUtilityNew += delta ** nx.dijkstra_path_length(G, i, neighbor)

			if (newUtilityExist - initialUtilityExist < c) or (newUtilityNew - initialUtilityNew < c):
				G.remove_edge(i, node)

	return G

def OptimizeStayConnected(G, iterations):
	G.graph['isOptimized'] = True
	c = G.graph['cost']
	N = len(G.nodes())
	#optAgents = random.sample(G.nodes(), int(N/2))
	optAgents = list(G.nodes())

	numberOfEdgesRemoved = 0
	numberOfEdgesAdded = 0

	for i in range(iterations):
		random.shuffle(optAgents)
		# Looping through agents to rethink connections
		for node in G.nodes():
			neighborhood = G.adjacency_list()[node] # Set of neighbors
			complementToNeighborhood = list(G.nodes()) # Complement to the neghibor set

			for neighbor in neighborhood:
				complementToNeighborhood.remove(neighbor) # removing non-nieghbors
				# #print "Agent %s considers removing an edge from agent %s" % (node,neighbor)


				# Rethink connection only if not sponsoring an edge
				if G[node][neighbor]['sponsor'] == node:

					# Calculating initial utility:
					initialUtility = 0
					for agent in G.nodes():
						if nx.has_path(G, node ,agent):
							initialUtility -= nx.dijkstra_path_length(G, node, agent)

					# Consider dropping an edge:
					G.remove_edge(node, neighbor)
					newUtility = 0
					for agent in G.nodes():
						if nx.has_path(G, node ,agent):
							newUtility -= nx.dijkstra_path_length(G, node, agent)

					if newUtility == 0:
						newUtility = float("-Inf")

					if (initialUtility - newUtility > c) or not nx.has_path(G, node, neighbor): #or (newUtility == 0):
						G.add_edge(node, neighbor)
						G.edge[node][neighbor]['sponsor'] = node
						G.edge[neighbor][node]['sponsor'] = node
						##print "Leave an edge"
					else:
						#print "Remove an edge"
						numberOfEdgesRemoved += 1

			random.shuffle(complementToNeighborhood)
			for neighbor in complementToNeighborhood:
				#print "Agent %s considers adding an edge to agent %s" % (node,neighbor)
				initialUtility = 0
				for agent in G.nodes():
					if nx.has_path(G, node, agent):
						initialUtility -= nx.dijkstra_path_length(G, node, agent)

				# Consider adding an edge
				G.add_edge(node, neighbor)
				G.edge[node][neighbor]['sponsor'] = node
				G.edge[neighbor][node]['sponsor'] = node
				newUtility = 0
				for agent in G.nodes():
					if nx.has_path(G, node, agent):
						newUtility -= nx.dijkstra_path_length(G, node, agent)

				if newUtility - initialUtility < c:
					G.remove_edge(node, neighbor)
					#print "Edge not added"
				else:
					#print "Edge added"
					numberOfEdgesAdded += 1


		#print "Thus far removed %s edges" % numberOfEdgesRemoved
	#print "Total edges removed: %s" % numberOfEdgesRemoved
	#print "Total edges added: %s" % numberOfEdgesAdded

	return G

def OptimizeBilateralconnection(G, iterations):
	G.graph['isOptimized'] = True
	c = G.graph['cost']
	delta = G.graph['delta']
	N = len(G.nodes())

	optAgents = list(G.nodes())

	totalEdgesRemoved = 0
	totalEdgesAdded = 0

	for i in range(iterations):
		random.shuffle(optAgents)
		for node in optAgents:
			neighborhood = G.adjacency_list()[node] # Set of neighbors
			complementToNeighborhood = list(G.nodes()) # Complement to the neghibor set

			random.shuffle(neighborhood)
			for neighbor in neighborhood:
				complementToNeighborhood.remove(neighbor)
				#print "Agent %s considers removing an edge from agent %s" % (node,neighbor)

				# Compute initial utility:
				initialUtility = 0
				for agent in G.nodes():
					if nx.has_path(G, node ,agent):
						initialUtility += delta ** nx.dijkstra_path_length(G, node, agent)

				#print "Agent's %s initial utility is %s" % (node, initialUtility)

				# Consider dropping an edge:
				G.remove_edge(node, neighbor)

				# Compute new utility:
				newUtility = 0
				for agent in G.nodes():
					if nx.has_path(G, node ,agent):
						newUtility += delta ** nx.dijkstra_path_length(G, node, agent)

				#print "Agent's %s utility after removing an edge is %s" % (node, newUtility)

				if initialUtility - newUtility > c:
					G.add_edge(node, neighbor)
					#print "Leave edge"
				else:
					#print "Remove edge"
					totalEdgesRemoved += 1

			random.shuffle(complementToNeighborhood)
			for neighbor in complementToNeighborhood:
				#print "Agent %s considers adding an edge to agent %s" % (node,neighbor)
				initialUtilityNew = 0
				newUtilityNew = 0
				initialUtilityExist = 0
				newUtilityExist = 0

				for agent in G.nodes():
					if agent != node and nx.has_path(G, node, agent):
						initialUtilityNew += delta ** nx.dijkstra_path_length(G, node, agent)

				for agent in G.nodes():
					if agent != neighbor and nx.has_path(G, agent, neighbor):
						initialUtilityExist += delta ** nx.dijkstra_path_length(G, agent, neighbor)

				# Add edge and calculate new utility:
				G.add_edge(node, neighbor)

				for agent in G.nodes():
					if agent != node and nx.has_path(G, agent, node):
						newUtilityNew += delta ** nx.dijkstra_path_length(G, agent, node)

				for agent in G.nodes():
					if neighbor != agent and nx.has_path(G, agent, neighbor):
						newUtilityExist += delta ** nx.dijkstra_path_length(G, agent, neighbor)

				if (newUtilityExist - initialUtilityExist < c) or (newUtilityNew - initialUtilityNew < c):
					G.remove_edge(node, neighbor)
					#print "Edge not added"
				else:
					#print "Edge added"
					totalEdgesAdded += 1


	#print "Removed %s edges" % totalEdgesRemoved
	#print "Added %s edges" % totalEdgesAdded

	return G

def DegreeDistribution(G):
    N = len(G.nodes())
    nodesDegrees = [G.degree()[i] for i in G.nodes()]
    mean_degree = sum(nodesDegrees)/len(nodesDegrees)

    dictDegree = Counter(nodesDegrees)
    degreeDist = []
    poissonApproximation = []
    xRange = []
    for i in range(max(nodesDegrees) + 1):
        degreeDist.append(dictDegree[i])
        poissonApproximation.append(m.e**(-mean_degree)*(mean_degree**i)*N/m.factorial(i))
        xRange.append(i)

    return degreeDist

def ClusterDistribution(G):
	clusterValueDict = nx.clustering(G)
	clusterValues = [clusterValueDict[i] for i in G.nodes()]

	return clusterValues









