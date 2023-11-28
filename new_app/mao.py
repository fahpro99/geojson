import networkx as nx
import pandas as pd
import plotly.graph_objects as go

# Assuming you have a DataFrame with columns "source" and "destination"
# Example data generation (replace this with your actual DataFrame)
df = pd.read_excel('prepared.xlsx')

# Create a directed graph
G = nx.from_pandas_edgelist(df, 'source', 'destination', create_using=nx.Graph())

# Get the positions of the nodes using a layout algorithm
pos = nx.spring_layout(G)

# Extract node positions
node_x = []
node_y = []
for key, value in pos.items():
    node_x.append(value[0])
    node_y.append(value[1])

# Extract node names
node_names = list(G.nodes)

# Create an edge trace
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

# Add edge information to the trace
for edge in G.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

# Create a node trace
node_trace = go.Scatter(
    x=node_x,
    y=node_y,
    mode='markers',
    hoverinfo='text',
    marker=dict(
        showscale=True,
        colorscale='YlGnBu',
        size=10,
        colorbar=dict(
            thickness=15,
            title='Node Connections',
            xanchor='left',
            titleside='right'
        )
    )
)

# Add node information to the trace
node_trace['text'] = node_names

# Create a figure
fig = go.Figure(data=[edge_trace, node_trace],
                layout=go.Layout(
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=0, l=0, r=0, t=0),
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                )

# Show the interactive plot
fig.show()
