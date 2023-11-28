import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
import pandas as pd

# Sample DataFrame with 'source' and 'destination' columns representing edges
data = {'source': ['banani', 'paltan', 'uttara', 'uttara', 'kawran bazar', 'mohammadpur', 'paltan', 'badda', 'gazipur', 'dhanmondi', 'paltan', 'gazipur'],
        'destination': ['paltan', 'uttara', 'kawran bazar', 'dhanmondi', 'mohammadpur', 'motijhil', 'badda', 'gazipur', 'kawran bazar', 'farmgate', 'gazipur', 'dhanmondi']}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(df, 'source', 'destination')

# Set a random seed for consistent layouts
random_seed = 42
pos = nx.spring_layout(G, seed=random_seed)

# Initialize node and edge colors
node_colors_mapping = {node: 'blue' for node in G.nodes()}
edge_colors = ['black' for _ in G.edges()]
edge_widths = [1.0 for _ in G.edges()]

# Keep track of the state of each node (up or down)
node_states = {node: True for node in G.nodes()}  # All nodes start in the "up" state

# Function to find affected edges when nodes go down
def get_affected_edges(graph, nodes):
    affected_edges = []
    for node in nodes:
        if graph.has_node(node):
            neighbors = list(graph.neighbors(node))
            for neighbor in neighbors:
                affected_edges.append((node, neighbor))
        else:
            print(f"Node {node} not found in the network.")
    return affected_edges

# Function to toggle the state of a node (up or down)
def toggle_node_state(node):
    node_states[node] = not node_states[node]

# Rest of the code remains unchanged...
# (Including the on_node_click function and the code to draw the graph)

# Assign indices to the edges for tracking
for i, edge in enumerate(G.edges()):
    G[edge[0]][edge[1]]['index'] = i

# Draw the initial graph with node and edge colors
fig, ax = plt.subplots()
nx.draw(G, pos, with_labels=True, node_color=list(node_colors_mapping.values()), edge_color=edge_colors, width=edge_widths)

# Connect the mouse click event to the on_node_click function
fig.canvas.mpl_connect('button_press_event', on_node_click)

mplcursors.cursor(hover=True)

plt.show()
