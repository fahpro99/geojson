import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Sample DataFrame with 'source' and 'destination' columns representing edges
data = {'source': [1, 2, 3, 3, 4, 6, 2, 8, 9, 5, 2, 9],
        'destination': [2, 3, 4, 5, 6, 7, 8, 9, 4, 10, 9, 7]}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a graph from the DataFrame
G = nx.from_pandas_edgelist(df, 'source', 'destination')

# Set a random seed for consistent layouts
random_seed = 42
pos = nx.spring_layout(G, seed=random_seed)

# Initialize node and edge colors
node_colors = ['blue' for _ in G.nodes()]
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

# Function to handle mouse click event
def on_click(event, ax):
    if event.xdata is not None and event.ydata is not None:
        clicked_nodes = []
        # Find the nearest nodes to the clicked coordinates
        for n, (x, y) in pos.items():
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
            source = 1
            destination = 7

            # Reset all node colors to blue and affected edges to default
            for n in G.nodes():
                node_colors[n - 1] = 'blue'

            for e in G.edges():
                edge_colors[G[e[0]][e[1]]['index']] = 'black'
                edge_widths[G[e[0]][e[1]]['index']] = 1.0

            # Check if there is a path after removing the down nodes
            if is_path_available(G, source, destination, affected_edges):
                print(f"\nPath from {source} to {destination} is available.")
                # Highlight the possible path nodes in different colors
                path_nodes = find_all_paths(G, source, destination, affected_edges)
                for i, path in enumerate(path_nodes):
                    color = f"C{i}"  # Use a different color for each path
                    for path_node in path:
                        node_colors[path_node - 1] = color

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
                    node_colors[node - 1] = 'red'
                    # Highlight the affected edges in red with a thicker line
                    for affected_edge in affected_edges:
                        edge_index = G[affected_edge[0]][affected_edge[1]]['index']
                        edge_colors[edge_index] = 'red'
                        edge_widths[edge_index] = 2.5

            # Draw the updated graph with node and edge colors
            ax.clear()
            nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, width=edge_widths, ax=ax)
            plt.draw()

# Assign indices to the edges for tracking
for i, edge in enumerate(G.edges()):
    G[edge[0]][edge[1]]['index'] = i

# Draw the initial graph with node and edge colors
fig, ax = plt.subplots()
nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color=edge_colors, width=edge_widths, ax=ax)

# Connect the mouse click event to the on_click function
fig.canvas.mpl_connect('button_press_event', lambda event: on_click(event, ax))

plt.show()
