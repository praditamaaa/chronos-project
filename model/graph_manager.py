import networkx as nx

class GraphManager:
    """Mengelola dua graf: 
       1) DiGraph berbobot (Dijkstra)
       2) Graph tak berarah (Coloring)"""
    def __init__(self):
        self.G_dijkstra = nx.DiGraph()
        self.G_conflict = nx.Graph()

    # Node
    def add_activity(self, activity):
        attrs = {"label": activity.name,
                 "duration": activity.duration,
                 "location": activity.location}
        self.G_dijkstra.add_node(activity.id, **attrs)
        self.G_conflict.add_node(activity.id, **attrs)

    # Edge berarah (untuk Dijkstra)
    def add_connection(self, src, dst, weight):
        self.G_dijkstra.add_edge(src, dst, weight=weight)

    # Edge tak berarah (untuk Coloring)
    def add_conflict(self, a, b):
        self.G_conflict.add_edge(a, b)

    # Analisis
    def get_shortest_path(self, start, end):
        try:
            return nx.dijkstra_path(self.G_dijkstra, start, end, weight="weight")
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def get_shortest_path_edges(self, start, end):
        path = self.get_shortest_path(start, end)
        return [(path[i], path[i+1]) for i in range(len(path)-1)] if len(path) > 1 else []

    def get_coloring(self):
        if self.G_conflict.number_of_nodes() == 0:
            return {}
        return nx.coloring.greedy_color(self.G_conflict, strategy="largest_first")
