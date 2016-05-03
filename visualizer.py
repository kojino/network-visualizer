from flask import Flask, render_template, request, jsonify
import networks, plotting


app = Flask(__name__)

@app.route('/')

def home():

    return render_template('home.html')

@app.route('/about/')

def about():

    return render_template('about.html')

@app.route('/visualizer/')

def visualizer():
  return render_template('visualizer.html')

@app.route('/_display_graph/')

def display_graph():
  model = request.form.get("model", "none", type=str)
  # model = str(request.form.get('model'))
  return jsonify(result=model)

  # if model == "ER":
  #   N=int(request.form.get('N_ER'))
  #   p=float(request.form.get('p'))
  #   G=networks.ErdosRenyi(N, p)
  #   return jsonify(result=lotting.PlotNetwork(G))
  # elif model == "PA":
  #   N=int(request.form.get('N_PA'))
  #   addNodes=int(request.form.get('addNodes'))
  #   G=networks.PrefferentialAttachement(N, addNodes)
  #   return jsonify(result=plotting.PlotNetwork(G))
  # elif model == "CM":
  #   N=int(request.form.get('N_CM'))
  #   NSet=int(request.form.get('NSet'))
  #   NNeighbor=int(request.form.get('NNeighbor'))
  #   PSet=float(request.form.get('PSet'))
  #   PNeighbor=float(request.form.get('PNeighbor'))
  #   G=networks.Copying(N, NSet, NNeighbor, PSet, PNeighbor)
  #   return jsonify(result=plotting.PlotNetwork(G))
  # elif model == "SC":
  #   N=int(request.form.get('N_SC'))
  #   c=float(request.form.get('c_SC'))
  #   G=networks.StayConnected(N, c)
  #   return jsonify(result=plotting.PlotNetwork(G))
  # else:
  #   N=int(request.form.get('N_BC'))
  #   delta=float(request.form.get('delta'))
  #   c=float(request.form.get('c_BC'))
  #   G=networks.BilateralConnection(N, delta, c)
  #   return jsonify(result=plotting.PlotNetwork(G))

if __name__ == '__main__':

    app.run(debug=True)