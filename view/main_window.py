import customtkinter as ctk
from .graph_canvas import GraphCanvas

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Chronos Graph Optimizer – CustomTkinter Edition")
        self.geometry("1000x700")

        # ------------------ Input ------------------
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(fill="x", padx=10, pady=10)

        self.name_entry = ctk.CTkEntry(input_frame, placeholder_text="Nama kegiatan")
        self.duration_entry = ctk.CTkEntry(input_frame, placeholder_text="Durasi (menit)")
        self.location_entry = ctk.CTkEntry(input_frame, placeholder_text="Lokasi")
        self.add_button = ctk.CTkButton(input_frame, text="Tambah")

        self.name_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        self.duration_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        self.location_entry.pack(side="left", padx=5, pady=5, expand=True, fill="x")
        self.add_button.pack(side="left", padx=5, pady=5)

        # ------------------ Tombol Analisis ------------------
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(fill="x", padx=10, pady=(0, 10))

        self.shortest_button = ctk.CTkButton(button_frame, text="Hitung Jalur Terpendek")
        self.color_button = ctk.CTkButton(button_frame, text="Warna Graf")
        self.clear_button = ctk.CTkButton(button_frame, text="Bersihkan")

        self.shortest_button.pack(side="left", padx=5, pady=5)
        self.color_button.pack(side="left", padx=5, pady=5)
        self.clear_button.pack(side="left", padx=5, pady=5)

        # ------------------ Output & Canvas ------------------
        self.output_label = ctk.CTkLabel(self, text="Output akan tampil di sini.", anchor="w")
        self.output_label.pack(fill="x", padx=10, pady=(0, 5))

        self.graph_canvas = GraphCanvas(self)
        self.graph_canvas.pack(fill="both", expand=True, padx=10, pady=(0, 10))
