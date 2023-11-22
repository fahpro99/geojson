import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def find_affected_nodes(graph, failed_node):
    affected_nodes = set()

    def dfs(node):
        affected_nodes.add(node)
        for neighbor in graph.neighbors(node):
            if neighbor not in affected_nodes:
                dfs(neighbor)

    dfs(failed_node)
    affected_nodes.remove(failed_node)

    return list(affected_nodes)

class NetworkAnalyzerApp:
    def __init__(self, master, graph):
        self.master = master
        self.master.title("Network Analyzer")
        self.graph = graph
        self.failed_node = None

        self.figure, self.ax = plt.subplots(figsize=(5, 5))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        self.canvas.mpl_connect('button_press_event', self.on_click)

        self.draw_graph()

    def on_click(self, event):
        if event.inaxes is not None:
            clicked_node = None
            for node in self.graph.nodes:
                x, y = self.ax.transData.transform_point((self.graph.nodes[node]['pos'][0], self.graph.nodes[node]['pos'][1]))
                if abs(event.x - x) < 0.03 and abs(event.y - y) < 0.03:
                    clicked_node = node
                    break

            if clicked_node:
                self.failed_node = clicked_node
                affected_nodes = find_affected_nodes(self.graph, self.failed_node)
                self.highlight_nodes(affected_nodes)
            else:
                messagebox.showinfo("Node not clicked", "Please click on a node.")

    def highlight_nodes(self, nodes):
        self.draw_graph()
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx_nodes(self.graph, pos=pos, nodelist=nodes, node_color='red')
        nx.draw_networkx_edges(self.graph, pos=pos, edgelist=self.graph.edges, edge_color='red', alpha=0.5)
        self.canvas.draw()

    def draw_graph(self):
        self.ax.clear()
        pos = nx.spring_layout(self.graph)
        nx.draw_networkx(self.graph, pos=pos, ax=self.ax, with_labels=True, node_size=700, node_color='lightblue')
        self.canvas.draw()

def main():
    # Example graph data (you should replace this with your dataset)
    edges = [('A', 'B'), ('B', 'C'), ('B', 'D'), ('C', 'E'), ('D', 'F')]

    # Create a directed graph using NetworkX
    graph = nx.DiGraph()
    graph.add_edges_from(edges)

    # Add positions to nodes for later use in the GUI
    pos = nx.spring_layout(graph)
    nx.set_node_attributes(graph, pos, 'pos')

    root = tk.Tk()
    app = NetworkAnalyzerApp(root, graph)
    root.mainloop()

if __name__ == "__main__":
    main()
