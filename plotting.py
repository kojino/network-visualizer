import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, mpld3
from mpld3 import plugins
import networkx as nx
import mpld3
import utils
import scipy.stats as ss
import math as m
from collections import Counter
from textwrap import wrap

def PlotNetwork(G):
    N = len(G.nodes())
    pos = nx.spring_layout(G)

    # Adding attributes to nodes
    for node in G.nodes():
        G.node[node]['pos'] = pos[node]

    # Creating color palette:
    # Calculating maximum degree in the graph:
    maxDegree = G.degree()[max(G.degree(), key=G.degree().get)] # Need to simplify
    hexCodes = utils.get_N_HexCol(maxDegree + 1)
    #nodesColor = ["#" + hexCodes[G.degree()[node]] for node in G.nodes()]
    # print "Max Degree: %s" % maxDegree
    # print hexCodes
    nodesColor = [hexCodes[G.degree()[node]] for node in G.nodes()]

    nodesDegree = [G.degree()[i] for i in G.nodes()]
    nodesCluster = [nx.clustering(G)[i] for i in G.nodes()]

    df = pd.DataFrame(index=range(N))
    df['Degree'] = nodesDegree
    df['Cluster'] = nodesCluster

    labels = []
    for i in range(N):
        label = df.ix[[i], :].T
        label.columns = ['Node {0}'.format(i)]
        labels.append(str(label.to_html()))

    # Creating canvas
    fig, ax = plt.subplots()

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos'] # Beginning of an edge point
        x1, y1 = G.node[edge[1]]['pos'] # End of an edge point
        ax.plot([x0,x1],[y0,y1], color='grey', lw=1.5, alpha=0.5, zorder=1)

    points = ax.scatter([(G.node[node]['pos'])[0] for node in G.nodes()],
                        [(G.node[node]['pos'])[1] for node in G.nodes()],
                        c=nodesColor, s = 220, alpha=1, lw = 3, zorder=2)

    tooltip = plugins.PointHTMLTooltip(points,
                                    labels,
                                    voffset=10,
                                    hoffset=10,
                                    css=utils.CSSTableStyle())

    plugins.connect(fig, tooltip)

    # Getting network attributes
    attributesList = G.graph.keys()
    titleName = G.graph['name'] + ". N: " + str(len(G.nodes())) + " "
    fileName = G.graph['name'] + " N-" + str(len(G.nodes())) + " "
    attributesList.remove('name')

    i = 0
    for attribute in attributesList:
        if i == 2:
            titleName += " \n "
        titleName += attribute + ": " + str(G.graph[attribute]) + " "
        fileName += attribute + "-" + str(G.graph[attribute]) + " "
        i += 1

    plt.title(titleName)
    fig.set_size_inches(9,7)
    # plt.show()
    # plt.savefig(fileName + ".png")
    #mpld3.show()
    # mpld3.save_html(fig, name + ".html")
    # plt.close(fig)
    # plt.close()

    return mpld3.fig_to_html(fig)

def PlotDegreeDistribution(G):
    N = len(G.nodes())
    nodesDegrees = [G.degree()[i] for i in G.nodes()]
    mean_degree = sum(nodesDegrees)/len(nodesDegrees)

    dictDegree = Counter(nodesDegrees)
    degreeDist = []
    poissonApproximation = []
    xRange = []
    rv = ss.poisson(mean_degree, loc=0)
    for i in range(max(nodesDegrees) + 1):
        degreeDist.append(dictDegree[i])
        poissonApproximation.append(rv.pmf(i)*N)
        xRange.append(i)

    fig, ax = plt.subplots()
    plt.plot(xRange, degreeDist,
            marker='o',
            markersize=8,
            markeredgewidth=0.0,
            linestyle='-',
            linewidth = 5,
            color='#c9e3a0',
            label='Degree distribution')
    plt.plot(xRange, poissonApproximation,
            marker='o',
            markersize=8,
            markeredgewidth=0.0,
            linestyle='-',
            linewidth = 5,
            color='#82bfd9',
            label='Poisson approximation')
    plt.xlabel('Degree', size = 16)
    plt.ylabel('Frequency', size = 16)
    plt.legend(loc = "best")

    attributesList = G.graph.keys()
    titleName = "Degree Distribution " + G.graph['name'] + ". N: " + str(len(G.nodes())) + " "
    fileName = "Degree Distribution " + G.graph['name'] + " N-" + str(len(G.nodes())) + " "
    attributesList.remove('name')

    for attribute in attributesList:
        titleName += attribute + ": " + str(G.graph[attribute]) + " "
        fileName += attribute + "-" + str(G.graph[attribute]) + " "

    plt.title(titleName)
    #plt.savefig(fileName + ".png")
    #plt.close()
    # mpld3.show()
    fig.set_size_inches(9,7)

    return mpld3.fig_to_html(fig)

def PlotClusterDistribution(G):
    clusterValueDict = nx.clustering(G)
    clusterValues = [clusterValueDict[i] for i in G.nodes()]

    fig, ax = plt.subplots()
    plt.hist(clusterValues, color = '#82bfd9', linewidth = 0.0)
    #plt.title("Clustering Coefficient Distribution", size = 18)
    plt.xlabel("Value", size = 16)
    plt.ylabel("Frequency", size = 16)

    attributesList = G.graph.keys()
    titleName = "Clustering Coefficient " + G.graph['name'] + ". N: " + str(len(G.nodes())) + " "
    fileName = "Clustering Coefficient " + G.graph['name'] + " N-" + str(len(G.nodes())) + " "
    attributesList.remove('name')

    for attribute in attributesList:
        titleName += attribute + ": " + str(G.graph[attribute]) + " "
        fileName += attribute + "-" + str(G.graph[attribute]) + " "

    plt.title(titleName)
    # plt.savefig(fileName + ".png")
    fig.set_size_inches(9,7)
    # mpld3.show()
    # plt.close()
    return mpld3.fig_to_html(fig)






