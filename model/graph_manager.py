import networkx as nx

class GraphManager:
    """
    Mengelola 2 graf:
    - G_dijkstra: DiGraph berbobot (untuk shortest path)
    - G_conflict: Graph tak berarah (untuk coloring)
    """
    def __init__(self):
        self.G_dijkstra = nx.DiGraph()
        self.G_conflict = nx.Graph()

    # ---- Node / Aktivitas ----
    def add_activity(self, activity):
        attrs = {
            "label": activity.name,
            "duration": activity.duration,
            "location": activity.location,
        }
        self.G_dijkstra.add_node(activity.id, **attrs)
        self.G_conflict.add_node(activity.id, **attrs)

    def remove_activity(self, node_id: int):
        if node_id in self.G_dijkstra:
            self.G_dijkstra.remove_node(node_id)
        if node_id in self.G_conflict:
            self.G_conflict.remove_node(node_id)

    # ---- Edge untuk Dijkstra ----
    def add_connection(self, source_id: int, target_id: int, weight: int):
        """Edge berarah dengan bobot (misal: durasi transisi atau durasi target)."""
        self.G_dijkstra.add_edge(source_id, target_id, weight=weight)

    def remove_connection(self, source_id: int, target_id: int):
        if self.G_dijkstra.has_edge(source_id, target_id):
            self.G_dijkstra.remove_edge(source_id, target_id)

    # ---- Edge untuk Conflict/Coloring ----
    def add_conflict(self, a_id: int, b_id: int):
        self.G_conflict.add_edge(a_id, b_id)

    def remove_conflict(self, a_id: int, b_id: int):
        if self.G_conflict.has_edge(a_id, b_id):
            self.G_conflict.remove_edge(a_id, b_id)

    # ---- Analitik ----
    def get_shortest_path(self, start: int, end: int):
        import networkx as nx
        try:
            path = nx.dijkstra_path(self.G_dijkstra, start, end, weight='weight')
            return path
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return []

    def get_shortest_path_edges(self, start: int, end: int):
        path = self.get_shortest_path(start, end)
        return [(path[i], path[i+1]) for i in range(len(path)-1)] if len(path) >= 2 else []

    def get_coloring(self):
        """Greedy coloring: mapping {node_id: color_index}."""
        import networkx as nx
        if self.G_conflict.number_of_nodes() == 0:
            return {}
        return nx.coloring.greedy_color(self.G_conflict, strategy="largest_first")
