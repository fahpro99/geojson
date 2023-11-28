import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

# Assuming you have a DataFrame with columns "source" and "destination"
# Example data generation (replace this with your actual DataFrame)
df = pd.read_excel('prepared.xlsx')

# Create a directed graph
G = nx.from_pandas_edgelist(df, 'source', 'destination', create_using=nx.Graph())

# Draw the network graph with labels shown only when hovering over nodes
plt.figure(figsize=(10, 10))

def on_hover(event):
    for node, (x, y) in pos.items():
        if event.xdata is not None and event.ydata is not None:
            if x - 0.02 < event.xdata < x + 0.02 and y - 0.02 < event.ydata < y + 0.02:
                plt.annotate(str(node), (x, y), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color='red')
            else:
                plt.annotate("", (x, y), textcoords="offset points", xytext=(0, 0), ha='center', fontsize=8)

pos = nx.spring_layout(G)  # You can try different layouts based on your preference
nx.draw(G, pos, with_labels=False, node_size=7)

# Connect the hover function to the figure
plt.connect('motion_notify_event', on_hover)

plt.title("Network Graph from DataFrame")
plt.show()
