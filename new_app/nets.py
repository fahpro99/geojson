import networkx as nx
import matplotlib.pyplot as plt
import random

# Generate random data for demonstration
num_nodes = 6000

# Create a directed graph
G = nx.DiGraph()

# Add nodes
for i in range(num_nodes):
    G.add_node(f"Source_{i}")
    G.add_node(f"Destination_{i}")

# Add edges (connections between sources and destinations)
for i in range(num_nodes):
    source_node = f"Source_{i}"
    destination_node = f"Destination_{i}"
    G.add_edge(source_node, destination_node)

# Draw the network graph
pos = nx.spring_layout(G)  # You can try different layouts based on your preference

plt.figure(figsize=(10, 10))
nx.draw(G, pos, with_labels=False, node_size=5)
plt.title("Network Graph with 6000 Sources and Destinations")
plt.show()
