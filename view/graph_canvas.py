from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import networkx as nx

class GraphCanvas(FigureCanvas):
    """
    Canvas Matplotlib untuk menampilkan graf berarah berbobot (Dijkstra).
    - node_colors: dict {node_id: "#RRGGBB"}
    - highlight_edges: list[(u, v)] untuk menyorot jalur terpendek
    """
    def __init__(self, parent=None):
        self.fig = Figure(figsize=(6, 5), tight_layout=True)
        super().__init__(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.set_axis_off()
        self._pos_cache = None

    def draw_graph(self, G_dijkstra, node_colors=None, highlight_edges=None, title="Graf Kegiatan (Dijkstra)"):
        self.ax.clear()
        self.ax.set_axis_off()

        if G_dijkstra.number_of_nodes() == 0:
            self.ax.set_title("Graf kosong")
            self.draw()
            return

        # Layout (cache biar stabil)
        if self._pos_cache is None or set(self._pos_cache.keys()) != set(G_dijkstra.nodes()):
            self._pos_cache = nx.spring_layout(G_dijkstra, seed=42)
        pos = self._pos_cache

        # Warna node
        default_color = "#99CCFF"
        node_color_list = []
        for n in G_dijkstra.nodes():
            if node_colors and n in node_colors:
                node_color_list.append(node_colors[n])
            else:
                node_color_list.append(default_color)

        # Gambar node & edge
        nx.draw_networkx_nodes(G_dijkstra, pos, ax=self.ax, node_color=node_color_list, node_size=1100, edgecolors="#333333")
        nx.draw_networkx_labels(G_dijkstra, pos, ax=self.ax, font_size=9)

        # Semua edges
        nx.draw_networkx_edges(G_dijkstra, pos, ax=self.ax, arrows=True, arrowstyle='-|>', width=1.8)

        # Label bobot
        edge_labels = nx.get_edge_attributes(G_dijkstra, "weight")
        if edge_labels:
            nx.draw_networkx_edge_labels(G_dijkstra, pos, edge_labels=edge_labels, ax=self.ax, font_color='crimson', font_size=8)

        # Sorot jalur terpendek
        if highlight_edges:
            nx.draw_networkx_edges(G_dijkstra, pos, edgelist=highlight_edges, ax=self.ax, edge_color='orange', width=4, arrows=True, arrowstyle='-|>')

        self.ax.set_title(title, fontsize=11)
        self.draw()