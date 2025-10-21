from model.activity import Activity
from model.graph_manager import GraphManager
from tkinter import messagebox

class MainController:
    def __init__(self, view):
        self.view = view
        self.graph = GraphManager()
        self.activities = []

        # Sambungkan tombol
        self.view.add_button.configure(command=self.add_activity)
        self.view.shortest_button.configure(command=self.calculate_path)
        self.view.color_button.configure(command=self.color_graph)
        self.view.clear_button.configure(command=self.clear_all)

        self.refresh_graph("Graf kosong")

    # ------------------------------------------------------
    def add_activity(self):
        """Tambah node baru dan hubungkan otomatis dengan node sebelumnya"""
        try:
            name = self.view.name_entry.get().strip()
            duration = int(self.view.duration_entry.get().strip())
            location = self.view.location_entry.get().strip()
            if not name or not location:
                messagebox.showwarning("Peringatan", "Isi semua field kegiatan!")
                return

            act_id = len(self.activities) + 1
            activity = Activity(act_id, name, duration, location)
            self.activities.append(activity)
            self.graph.add_activity(activity)

            # koneksi otomatis
            if len(self.activities) > 1:
                prev = self.activities[-2]
                self.graph.add_connection(prev.id, activity.id, weight=duration)

            self.refresh_graph(f"Kegiatan '{name}' ditambahkan.")
            self.view.name_entry.delete(0, "end")
            self.view.duration_entry.delete(0, "end")
            self.view.location_entry.delete(0, "end")

        except ValueError:
            messagebox.showerror("Error", "Durasi harus berupa angka.")

    def calculate_path(self):
        if len(self.activities) < 2:
            messagebox.showinfo("Info", "Tambahkan minimal dua kegiatan.")
            return
        start, end = 1, len(self.activities)
        path = self.graph.get_shortest_path(start, end)
        if not path:
            self.view.output_label.configure(text="Tidak ada jalur ditemukan.")
            self.refresh_graph()
            return
        edges = self.graph.get_shortest_path_edges(start, end)
        self.view.graph_canvas.draw_graph(self.graph.G_dijkstra, highlight_edges=edges)
        self.view.output_label.configure(text=f"Jalur terpendek: {' → '.join(map(str, path))}")

    def color_graph(self):
        colors = self.graph.get_coloring()
        palette = ["#FF9999", "#99FF99", "#9999FF", "#FFD966", "#FFCCFF", "#A3E4D7"]
        node_colors = {n: palette[c % len(palette)] for n, c in colors.items()}
        for n in self.graph.G_dijkstra.nodes():
            node_colors.setdefault(n, "#99CCFF")
        self.view.graph_canvas.draw_graph(self.graph.G_dijkstra, node_colors=node_colors)
        self.view.output_label.configure(text=f"Hasil pewarnaan: {colors}")

    def clear_all(self):
        self.graph = GraphManager()
        self.activities.clear()
        self.refresh_graph("Graf dihapus.")
        self.view.output_label.configure(text="Graf dihapus.")

    def refresh_graph(self, title="Graf Kegiatan"):
        self.view.graph_canvas.draw_graph(self.graph.G_dijkstra, title=title)
