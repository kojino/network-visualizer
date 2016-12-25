from flask import Flask, render_template, request, jsonify, send_file
import networks, plotting
import networkx as nx

import os
# from intro_to_flask import app

# port = int(os.environ.get("PORT", 5000))
# app.run(debug=True, host='0.0.0.0', port=port)

app = Flask(__name__)

@app.route('/')

def home():

    return render_template('home.html')

@app.route('/visualizer/')

def visualizer():
  return render_template('visualizer.html')

@app.route('/_display_graph/')

def display_graph():
  model = request.args.get("model", "none", type=str)
  if model == "ER":
    N=int(request.args.get('N_ER'))
    p=float(request.args.get('p'))
    G=networks.ErdosRenyi(N, p)
    return jsonify(result=plotting.PlotNetwork(G),degree=plotting.PlotDegreeDistribution(G),cluster=plotting.PlotClusterDistribution(G))
  elif model == "PA":
    N=int(request.args.get('N_PA'))
    addNodes=int(request.args.get('addNodes'))
    G=networks.PrefferentialAttachement(N, addNodes)
    return jsonify(result=plotting.PlotNetwork(G),degree=plotting.PlotDegreeDistribution(G),cluster=plotting.PlotClusterDistribution(G))
  elif model == "CM":
    N=int(request.args.get('N_CM'))
    NSet=int(request.args.get('NSet'))
    NNeighbor=int(request.args.get('NNeighbor'))
    PSet=float(request.args.get('PSet'))
    PNeighbor=float(request.args.get('PNeighbor'))
    G=networks.Copying(N, NSet, NNeighbor, PSet, PNeighbor)
    return jsonify(result=plotting.PlotNetwork(G),degree=plotting.PlotDegreeDistribution(G),cluster=plotting.PlotClusterDistribution(G))
  elif model == "SC":
    N=int(request.args.get('N_SC'))
    c=float(request.args.get('c_SC'))
    opt=str(request.args.get('opt_SC'))
    G=networks.StayConnected(N, c)
    if opt == "1":
      G=networks.OptimizeStayConnected(G, 10)
    return jsonify(result=plotting.PlotNetwork(G),degree=plotting.PlotDegreeDistribution(G),cluster=plotting.PlotClusterDistribution(G))
  else:
    N=int(request.args.get('N_BC'))
    delta=float(request.args.get('delta'))
    c=float(request.args.get('c_BC'))
    opt=str(request.args.get('opt_SC'))
    G=networks.BilateralConnection(N, delta, c)
    if opt == "1":
      G=networks.OptimizeBilateralconnection(G,10)
    return jsonify(result=plotting.PlotNetwork(G),degree=plotting.PlotDegreeDistribution(G),cluster=plotting.PlotClusterDistribution(G))

@app.route('/about/')
def pdf():
    return send_file('./templates/report.pdf', attachment_filename='report.pdf')

if __name__ == '__main__':
  app.run(debug=True)
