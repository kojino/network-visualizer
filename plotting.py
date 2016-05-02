import pandas as pd
import numpy as np
import matplotlib.pyplot as plt, mpld3
from mpld3 import plugins
import networkx as nx
import mpld3
import utils
import time
import scipy.stats as ss
import math as m


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
    nodesColor = ["#" + hexCodes[G.degree()[node]] for node in G.nodes()]

    nodesDegree = [G.degree()[i] for i in G.nodes()]
    nodesCluster = [nx.clustering(G)[i] for i in G.nodes()]

    df = pd.DataFrame(index=range(N))
    df['Degree'] = nodesDegree
    df['Cluster'] = nodesCluster

    labels = []
    for i in range(N):
        label = df.ix[[i], :].T
        label.columns = ['Row {0}'.format(i)]
        labels.append(str(label.to_html()))

    # Creating canvas
    fig, ax = plt.subplots()

    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos'] # Beginning of an edge point
        x1, y1 = G.node[edge[1]]['pos'] # End of an edge point
        ax.plot([x0,x1],[y0,y1], color='grey', lw=1.5, alpha=0.5)

    points = ax.scatter([(G.node[node]['pos'])[0] for node in G.nodes()],
                        [(G.node[node]['pos'])[1] for node in G.nodes()],
                        c=nodesColor, s = 220, alpha=1, lw = 3)

    tooltip = plugins.PointHTMLTooltip(points, 
                                    labels, 
                                    voffset=10, 
                                    hoffset=10, 
                                    css=utils.CSSTableStyle())

    plugins.connect(fig, tooltip)

    #mpld3.show()
    #mpld3.save_html(fig, "Plot_" + str(30-len(G.nodes())) + ".html")
    #plt.close(fig)

    return mpld3.fig_to_html(fig)

def PlotDegreeDistribution(G):
    N = len(G.nodes())
    nodesDegrees = [G.degree()[i] for i in G.nodes()]
    mean_degree = sum(nodesDegrees)/len(nodesDegrees)
      
    # You typically want your plot to be ~1.33x wider than tall.  
    # Common sizes: (10, 7.5) and (12, 9)  
    plt.figure(figsize=(12, 9))  
      
    # Remove the plot frame lines. They are unnecessary chartjunk.  
    ax = plt.subplot(111)  
    ax.spines["top"].set_visible(False)  
    ax.spines["right"].set_visible(False)  
      
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
      
    plt.xticks(fontsize=14)
    plt.yticks(fontsize=14)
      
    plt.xlabel("Degree", fontsize=16)
    plt.ylabel("Frequency", fontsize=16)
    plt.hist(nodesDegrees,  color="#3F5D7D") #, bins = [x for x in range(max(nodesDegrees))]) #, bins=100)  
    
    xRange = range(max(nodesDegrees)) 
    h = plt.plot(xRange, [m.e**(-mean_degree)*(mean_degree**x)*N/m.factorial(x) for x in xRange], lw=2)

    mpld3.show();  

    

    #m.e**(-mean_degree)*(mean_degree**x)/m.factorial(x)



