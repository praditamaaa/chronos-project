from PySide6.QtWidgets import QTableWidgetItem
from model.graph_manager import GraphManager
from model.activity import Activity

class MainController:
    def __init__(self, view):
        self.view = view
        self.graph = GraphManager()
        self.activities = []  # list[Activity]

        # Signals
        self.view.add_button.clicked.connect(self.add_activity)
        self.view.calc_button.clicked.connect(self.calculate_path)
        self.view.color_button.clicked.connect(self.color_graph)
        self.view.clear_button.clicked.connect(self.clear_graph)
        self.view.add_conflict_btn.clicked.connect(self.add_conflict_edge)

        # contoh awal opsional (bisa dihapus kalau mau kosong)
        # self._seed_example()

    def _seed_example(self):
        data = [
            ("Bangun", 15, "Rumah"),
            ("Sarapan", 30, "Rumah"),
            ("Pergi ke Kampus", 45, "Jalan"),
            ("Kuliah", 120, "Kampus"),
            ("Gym", 60, "Gym"),
            ("Istirahat", 30, "Rumah"),
        ]
        for name, dur, loc in data:
            self._add_activity_core(name, dur, loc, auto_connect=True)
        self._refresh_canvas("Graf awal (contoh)")

    # ------- Helpers -------
    def _add_activity_core(self, name: str, duration: int, location: str, auto_connect: bool):
        new_id = len(self.activities) + 1
        act = Activity(new_id, name, duration, location)
        self.activities.append(act)
        self.graph.add_activity(act)

        # auto connect ke node sebelumnya (berarah), bobot = durasi target
        if auto_connect and len(self.activities) >= 2:
            prev_id = self.activities[-2].id
            self.graph.add_connection(prev_id, act.id, weight=duration)

        # update table
        row = self.view.table.rowCount()
        self.view.table.insertRow(row)
        self.view.table.setItem(row, 0, QTableWidgetItem(str(act.id)))
        self.view.table.setItem(row, 1, QTableWidgetItem(act.name))
        self.view.table.setItem(row, 2, QTableWidgetItem(str(act.duration)))
        self.view.table.setItem(row, 3, QTableWidgetItem(act.location))

    def _refresh_canvas(self, title="Graf Kegiatan (Dijkstra)"):
        self.view.graph_canvas.draw_graph(self.graph.G_dijkstra, title=title)

    # ------- Slots -------
    def add_activity(self):
        name = self.view.name_input.text().strip()
        duration_txt = self.view.duration_input.text().strip()
        location = self.view.location_input.text().strip()

        if not name or not duration_txt or not location:
            self.view.output_label.setText("Isi semua field (Nama, Durasi, Lokasi).")
            return

        try:
            duration = int(duration_txt)
            if duration <= 0:
                raise ValueError
        except ValueError:
            self.view.output_label.setText("Durasi harus bilangan bulat positif.")
            return

        self._add_activity_core(name, duration, location, auto_connect=True)
        self._refresh_canvas(f"Kegiatan '{name}' ditambahkan.")
        self.view.output_label.setText(f"Kegiatan '{name}' ditambahkan.")

        # reset input
        self.view.name_input.clear()
        self.view.duration_input.clear()
        self.view.location_input.clear()

    def calculate_path(self):
        if len(self.activities) < 2:
            self.view.output_label.setText("Tambahkan minimal dua kegiatan.")
            return

        start = 1
        end = len(self.activities)
        path = self.graph.get_shortest_path(start, end)
        edges = self.graph.get_shortest_path_edges(start, end)

        title = "Jalur Terpendek (disorot oranye)" if edges else "Tidak ada jalur"
        self.view.graph_canvas.draw_graph(self.graph.G_dijkstra, highlight_edges=edges, title=title)

        if path:
            path_str = " → ".join(str(p) for p in path)
            self.view.output_label.setText(f"Jalur terpendek {start}→{end}: {path_str}")
        else:
            self.view.output_label.setText("Tidak ada jalur ditemukan.")

    def color_graph(self):
        # Coloring berdasarkan graf konflik (tak berarah)
        color_map_idx = self.graph.get_coloring()  # {node: colorIndex}
        palette = {
            0: "#FF9999",  # merah muda
            1: "#99FF99",  # hijau
            2: "#9999FF",  # biru
            3: "#FFD966",  # kuning
            4: "#FFCCFF",  # pink
            5: "#A3E4D7",  # teal
            6: "#F5B7B1",  # salmon
        }
        node_colors = {n: palette.get(c, "#CCCCCC") for n, c in color_map_idx.items()}

        # Jika belum ada edge konflik sama sekali, semua node mungkin color 0 (atau kosong)
        # Tangani juga node tanpa entri (beri warna default)
        for n in self.graph.G_dijkstra.nodes():
            node_colors.setdefault(n, "#99CCFF")

        self.view.graph_canvas.draw_graph(self.graph.G_dijkstra, node_colors=node_colors, title="Pewarnaan (berdasarkan graf konflik)")
        self.view.output_label.setText(f"Hasil pewarnaan (node:color_index): {color_map_idx}")

    def add_conflict_edge(self):
        a = int(self.view.conflict_a.value())
        b = int(self.view.conflict_b.value())
        if a == b:
            self.view.output_label.setText("A dan B tidak boleh sama.")
            return
        if a not in self.graph.G_conflict.nodes() or b not in self.graph.G_conflict.nodes():
            self.view.output_label.setText("ID tidak valid. Pastikan aktivitasnya ada.")
            return
        self.graph.add_conflict(a, b)
        self.view.output_label.setText(f"Konflik ditambahkan: {a} — {b} (untuk coloring).")

    def clear_graph(self):
        # Reset semua
        self.graph = GraphManager()
        self.activities.clear()
        self.view.table.setRowCount(0)
        self._refresh_canvas("Graf dikosongkan")
        self.view.output_label.setText("Graf dan data dibersihkan.")