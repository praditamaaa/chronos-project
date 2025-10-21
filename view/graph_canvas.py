import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx

class GraphCanvas(ctk.CTkFrame):
    """Canvas Matplotlib di CustomTkinter"""
    def __init__(self, master):
        super().__init__(master)
        self.figure = Figure(figsize=(5, 4), tight_layout=True)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        self.pos = None

    def draw_graph(self, G, highlight_edges=None, node_colors=None, title="Graf Kegiatan"):
        self.ax.clear()
        if G.number_of_nodes() == 0:
            self.ax.text(0.5, 0.5, "Graf kosong", ha="center", va="center")
            self.canvas.draw()
            return

        if not self.pos or set(G.nodes()) != set(self.pos.keys()):
            self.pos = nx.spring_layout(G, seed=42)

        default_color = "#99CCFF"
        colors = [node_colors.get(n, default_color) if node_colors else default_color for n in G.nodes()]

        nx.draw(G, pos=self.pos, ax=self.ax,
                node_color=colors, node_size=900, with_labels=True,
                edge_color="#555", arrows=True)
        edge_labels = nx.get_edge_attributes(G, "weight")
        if edge_labels:
            nx.draw_networkx_edge_labels(G, pos=self.pos, edge_labels=edge_labels,
                                         font_color="crimson", ax=self.ax)

        if highlight_edges:
            nx.draw_networkx_edges(G, pos=self.pos, edgelist=highlight_edges,
                                   edge_color="orange", width=3, ax=self.ax, arrows=True)

        self.ax.set_title(title)
        self.canvas.draw()
