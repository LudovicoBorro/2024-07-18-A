from model.modello import Model

model = Model()
model.buildGraph(3,7)
nodes, edges = model.graphDetails()
print(f"Grafo creato con {nodes} nodi e {edges} archi!")