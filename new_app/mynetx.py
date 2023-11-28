import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# Sample DataFrame with 'source', 'destination', and 'edge_weight' columns representing edges
data = {'source': ['A', 'B', 'C', 'A', 'D', 'B', 'E', 'C'],
        'destination': ['B', 'C', 'A', 'D', 'B', 'E', 'C', 'A'],
        'edge_weight': [2, 1, 3, 2, 1, 2, 1, 3]}

# Create a DataFrame
df = pd.DataFrame(data)

# Create a graph from the dataset
G = nx.from_pandas_edgelist(df, 'source', 'destination', ['edge_weight'])

# Calculate centrality metrics for the original network
degree_centrality = nx.degree_centrality(G)
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G)

# Visualize the original network
plt.figure(figsize=(8, 8))
pos = nx.spring_layout(G)  # Define layout for better visualization
nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=700, node_color='skyblue', font_color='black', edge_color='gray', font_size=8)
plt.title('Original Network')
plt.show()

# Simulate node failure (remove a node)
node_to_remove = 'C'
G_without_node = G.copy()
G_without_node.remove_node(node_to_remove)

# Calculate centrality metrics for the network without the removed node
degree_centrality_without_node = nx.degree_centrality(G_without_node)
closeness_centrality_without_node = nx.closeness_centrality(G_without_node)
betweenness_centrality_without_node = nx.betweenness_centrality(G_without_node)

# Visualize the network after node failure
plt.figure(figsize=(8, 8))
pos_without_node = nx.spring_layout(G_without_node)
nx.draw(G_without_node, pos_without_node, with_labels=True, font_weight='bold', node_size=700, node_color='lightcoral', font_color='black', edge_color='gray', font_size=8)
plt.title(f'Network after removing node {node_to_remove}')
plt.show()

# Compare centrality metrics before and after node removal
print(f"Degree Centrality for {node_to_remove} before removal: {degree_centrality.get(node_to_remove)}")
print(f"Degree Centrality for {node_to_remove} after removal: {degree_centrality_without_node.get(node_to_remove)}")

print(f"Closeness Centrality for {node_to_remove} before removal: {closeness_centrality.get(node_to_remove)}")
print(f"Closeness Centrality for {node_to_remove} after removal: {closeness_centrality_without_node.get(node_to_remove)}")

print(f"Betweenness Centrality for {node_to_remove} before removal: {betweenness_centrality.get(node_to_remove)}")
print(f"Betweenness Centrality for {node_to_remove} after removal: {betweenness_centrality_without_node.get(node_to_remove)}")
