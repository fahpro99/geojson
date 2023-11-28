import networkx as nx
import matplotlib.pyplot as plt

import pandas as pd

# Sample DataFrame with 'source' and 'destination' columns representing edges
data = {'source': ['banani', 'paltan', 'uttara', 'uttara', 'kawran bazar', 'mohammadpur', 'paltan', 'badda', 'gazipur', 'dhanmondi', 'paltan', 'gazipur'],
        'destination': ['paltan', 'uttara', 'kawran bazar', 'dhanmondi', 'mohammadpur', 'motijhil', 'badda', 'gazipur', 'kawran bazar', 'farmgate', 'gazipur', 'dhanmondi']}

# Create a DataFrame
df = pd.DataFrame(data)

# Add a default edge weight (e.g., 1) to the DataFrame
df['edge_weight'] = 1


# Create a graph from the dataset
G = nx.from_pandas_edgelist(df, 'source', 'destination', ['edge_weight'])

# Visualize the original network
nx.draw(G, with_labels=True, font_weight='bold')
plt.title('Original Network')
plt.show()

# Simulate node failure (replace 'node_to_remove' with the actual node)
node_to_remove = 'paltan'
G.remove_node(node_to_remove)

# Re-visualize the network after node failure
nx.draw(G, with_labels=True, font_weight='bold')
plt.title(f'Network after removing node {node_to_remove}')
plt.show()
