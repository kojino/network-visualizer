# Standard libraries for scraping and storing data
import numpy as np
import pandas as pd
import networkx as nx # Library for Graphs
import random # Random number generating function
import utils
import plotting as plot
import operator

def ErdosRenyi(N, p):

	return nx.erdos_renyi_graph(N, p)

def PrefferentialAttachement(N, addNodes):
	initNodes = 2 * addNodes + 1
	G = nx.complete_graph(initNodes)

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
	G = nx.complete_graph(1)

	for i in range(1, N):
		existingNodes = list(G.nodes())
		random.shuffle(existingNodes)

		optimalToConnect = 0
		optimalUtility = float("-inf")

		for nodeToConnect in existingNodes:
			G.add_edge(i, nodeToConnect)

			sumPathLengths = 0
			for node in G.nodes():
				sumPathLengths -= nx.dijkstra_path_length(G, i, node)

			if sumPathLengths > optimalUtility:
				optimalToConnect = nodeToConnect
				optimalUtility = sumPathLengths

			G.remove_edge(i, nodeToConnect)

		G.add_edge(i,nodeToConnect)

		print optimalUtility

		existingNodes.remove(nodeToConnect)

		for nodeToConnect in existingNodes:
			G.add_edge(i, nodeToConnect)

			sumPathLengths = 0
			for node in G.nodes():
				sumPathLengths -= nx.dijkstra_path_length(G, i, node)

			if sumPathLengths - optimalUtility > c:
				optimalUtility = sumPathLengths
			else:
				G.remove_edge(i, nodeToConnect)

	return G

def BilateralConnection(N, delta, c):
	G = nx.erdos_renyi_graph(N/4, 0.25)

	for i in range(10, N):
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

		print ranking

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

















