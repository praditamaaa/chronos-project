from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTableWidget, QSpinBox, QGroupBox, QFormLayout
)
from PySide6.QtCore import Qt
from graph_canvas import GraphCanvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chronos Graph Optimizer — Level 1 (MVC + Visual)")
        self.setGeometry(120, 80, 1080, 720)

        root = QVBoxLayout()

        # --- Panel Input Aktivitas ---
        form_box = QGroupBox("Tambah Aktivitas")
        form = QFormLayout()
        self.name_input = QLineEdit()
        self.duration_input = QLineEdit()
        self.location_input = QLineEdit()
        self.add_button = QPushButton("Tambah Aktivitas")
        form.addRow("Nama", self.name_input)
        form.addRow("Durasi (menit)", self.duration_input)
        form.addRow("Lokasi", self.location_input)
        form.addRow(self.add_button)
        form_box.setLayout(form)
        root.addWidget(form_box)

        # --- Tabel Aktivitas ---
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["ID", "Nama", "Durasi", "Lokasi"])
        self.table.horizontalHeader().setStretchLastSection(True)
        root.addWidget(self.table)

        # --- Panel Edge/Analisis ---
        actions_row = QHBoxLayout()

        # koneksi otomatis: tombol ini opsional (kita pakai koneksi otomatis saat tambah)
        self.calc_button = QPushButton("Hitung Jalur Terpendek (1 → terakhir)")
        self.color_button = QPushButton("Warna Graf (Conflict Coloring)")
        self.clear_button = QPushButton("Bersihkan Graf")

        actions_row.addWidget(self.calc_button)
        actions_row.addWidget(self.color_button)
        actions_row.addWidget(self.clear_button)

        root.addLayout(actions_row)

        # --- Panel Konflik sederhana (manual) ---
        conflict_box = QGroupBox("Tambah Konflik (untuk Coloring)")
        conflict_layout = QHBoxLayout()
        self.conflict_a = QSpinBox()
        self.conflict_a.setMinimum(1)
        self.conflict_b = QSpinBox()
        self.conflict_b.setMinimum(1)
        self.add_conflict_btn = QPushButton("Tambah Konflik A—B")
        conflict_layout.addWidget(QLabel("A:"))
        conflict_layout.addWidget(self.conflict_a)
        conflict_layout.addWidget(QLabel("B:"))
        conflict_layout.addWidget(self.conflict_b)
        conflict_layout.addWidget(self.add_conflict_btn)
        conflict_box.setLayout(conflict_layout)
        root.addWidget(conflict_box)

        # --- Output & Canvas ---
        self.output_label = QLabel("Output akan tampil di sini.")
        self.output_label.setAlignment(Qt.AlignLeft)
        root.addWidget(self.output_label)

        self.graph_canvas = GraphCanvas()
        root.addWidget(self.graph_canvas)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)
