import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from box import draw_all, MM_TO_PT

PARAMS = [
    # (label, key, min, max, default, resolution)
    ("Largeur h (mm)",        "h_mm",              20,  200, 80,  1),
    ("Hauteur v (mm)",        "v_mm",              20,  200, 80,  1),
    ("Épaisseur PMMA (mm)",   "pmma_thickness_mm",  1,   10,  3,  0.5),
    ("Offset bord (mm)",      "border_offset",      1,   20,  3,  0.5),
    ("Arrondi",               "rounding",           1,   30, 10,  1),
    ("Hauteur croix (mm)",    "hauteur_croix",      5,   60, 20,  1),
    ("Épaisseur trait (mm)",  "line_thickness_mm", 0.05, 0.5, 0.1, 0.01),
]


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BLT Box Generator")
        self.resizable(True, True)

        # ── Panneau gauche : contrôles ──────────────────────────────────
        left = ttk.Frame(self, padding=12)
        left.pack(side=tk.LEFT, fill=tk.Y)

        self.vars = {}
        for label, key, mn, mx, default, res in PARAMS:
            var = tk.DoubleVar(value=default)
            self.vars[key] = var

            ttk.Label(left, text=label).pack(anchor=tk.W, pady=(6, 0))

            row = ttk.Frame(left)
            row.pack(fill=tk.X)

            val_lbl = ttk.Label(row, text=f"{default:.2f}", width=7, anchor=tk.E)
            val_lbl.pack(side=tk.RIGHT)

            scale = tk.Scale(
                row, from_=mn, to=mx, variable=var,
                orient=tk.HORIZONTAL, resolution=res,
                showvalue=False, length=220,
                command=lambda _, v=var, l=val_lbl: self._on_change(v, l),
            )
            scale.pack(side=tk.LEFT, fill=tk.X, expand=True)

        ttk.Separator(left, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=12)
        ttk.Button(left, text="Exporter SVG", command=self.export_svg).pack(fill=tk.X)

        # ── Panneau droit : aperçu matplotlib ──────────────────────────
        right = ttk.Frame(self)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots()
        self.fig.tight_layout()
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.redraw()

    def _on_change(self, var, label):
        label.config(text=f"{var.get():.2f}")
        self.redraw()

    def _params(self):
        return {k: v.get() for k, v in self.vars.items()}

    def redraw(self):
        p = self._params()
        self.ax.clear()
        draw_all(
            self.ax,
            h_mm=p["h_mm"],
            v_mm=p["v_mm"],
            rounding=p["rounding"],
            pmma_thickness=p["pmma_thickness_mm"],
            border_offset=p["border_offset"],
            line_thickness_pt=p["line_thickness_mm"] * MM_TO_PT,
            hauteur_croix=p["hauteur_croix"],
        )
        self.ax.set_aspect("equal")
        self.ax.autoscale_view()
        self.ax.axis("off")
        self.canvas.draw()

    def export_svg(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".svg",
            filetypes=[("SVG files", "*.svg")],
            initialfile="combined_shape.svg",
        )
        if path:
            self.fig.savefig(path, format="svg")
            messagebox.showinfo("Export", f"SVG exporté :\n{path}")


if __name__ == "__main__":
    app = App()
    app.mainloop()
