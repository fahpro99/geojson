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
node_states = {node: False for node in G.nodes()}

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

# Function to check if there is a path from source to destination after removing nodes
def is_path_available(graph, source, destination, affected_edges):
    temp_graph = graph.copy()
    temp_graph.remove_edges_from(affected_edges)
    return nx.has_path(temp_graph, source, destination)

# Function to find all possible paths from source to destination
def find_all_paths(graph, source, destination, affected_edges):
    temp_graph = graph.copy()
    temp_graph.remove_edges_from(affected_edges)
    return list(nx.all_simple_paths(temp_graph, source, destination))

# Function to handle node click event
def on_node_click(event):
    if event.xdata is not None and event.ydata is not None:
        clicked_nodes = []
        # Find the nearest nodes to the clicked coordinates
        for n, (x, y) in pos.items():
            x = float(x)  # Convert x to float
            y = float(y)  # Convert y to float
            if (event.xdata - x)**2 + (event.ydata - y)**2 < 0.02:
                clicked_nodes.append(n)

        if clicked_nodes:
            # Toggle the state of the clicked nodes
            for node in clicked_nodes:
                toggle_node_state(node)

            affected_edges = get_affected_edges(G, clicked_nodes)

            print(f"Affected Edges after Nodes {clicked_nodes} Go Down:")
            print(affected_edges)

            # Choose a source and destination for the path check
            source = 'banani'
            destination = 'gazipur'

            # Check if there is a path after removing the down nodes
            if is_path_available(G, source, destination, affected_edges):
                print(f"\nPath from {source} to {destination} is available.")
                # Highlight the possible path nodes in different colors
                path_nodes = find_all_paths(G, source, destination, affected_edges)
                for i, path in enumerate(path_nodes):
                    color = f"C{i}"  # Use a different color for each path
                    for path_node in path:
                        node_colors_mapping[path_node] = color

                    # Highlight the edges along the possible paths
                    for j in range(len(path) - 1):
                        edge_colors[G[path[j]][path[j + 1]]['index']] = color

                    # Print nodes and edges along the available path
                    print(f"Nodes along Path {i + 1}:")
                    print(path)
                    print(f"Edges along Path {i + 1}:")
                    print([(path[j], path[j + 1]) for j in range(len(path) - 1)])
            else:
                print(f"\nPath from {source} to {destination} is not available.")

            # Highlight the clicked nodes based on their state
            for node in clicked_nodes:
                if node_states[node]:
                    node_colors_mapping[node] = 'red'
                    # Highlight the affected edges in red with a thicker line
                    for affected_edge in affected_edges:
                        edge_index = G[affected_edge[0]][affected_edge[1]]['index']
                        edge_colors[edge_index] = 'red'
                        edge_widths[edge_index] = 2.5
                else:
                    node_colors_mapping[node] = 'blue'
                    # Reset the edge colors and widths
                    for affected_edge in affected_edges:
                        edge_index = G[affected_edge[0]][affected_edge[1]]['index']
                        edge_colors[edge_index] = 'black'
                        edge_widths[edge_index] = 1.0

            # Draw the updated graph with node and edge colors
            plt.clf()
            nx.draw(G, pos, with_labels=True, node_color=list(node_colors_mapping.values()), edge_color=edge_colors, width=edge_widths)
            plt.draw()

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
