import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, PathPatch
from matplotlib.path import Path

def draw_side(largeur, hauteur_min, pmma_thickness, line_thickness):
    hauteur_totale = hauteur_min + (2 * pmma_thickness_mm)         # hauteur totale de la croix (bras vertical)
    largeur_bras_vertical = largeur/2  # largeur du bras vertical
    # Demi-dimensions
    L = largeur / 2
    H = hauteur_totale / 2
    bw = largeur_bras_vertical / 2
    bh = hauteur_min / 2
    # Vertices pour une seule forme (contour de la croix parfaitement symétrique)
    vertices = [
        (-L, bh),        # coin supérieur gauche du bras horizontal
        (-bw, bh),       # jonction bras horizontal / vertical
        (-bw, H),        # haut bras vertical
        (bw, H),         # haut bras vertical droit
        (bw, bh),        # jonction bras horizontal / vertical droit
        (L, bh),         # coin supérieur droit du bras horizontal
        (L, -bh),        # coin inférieur droit du bras horizontal
        (bw, -bh),       # jonction bras horizontal / vertical
        (bw, -H),        # bas bras vertical
        (-bw, -H),       # bas bras vertical gauche
        (-bw, -bh),      # jonction bras horizontal / vertical gauche
        (-L, -bh),       # coin inférieur gauche bras horizontal
        (-L, bh)         # retour départ
    ]

    codes = [Path.MOVETO] + [Path.LINETO] * (len(vertices) - 1)

    # Création du Path et du patch
    path = Path(vertices, codes)
    shape = PathPatch(path, fill=False, linewidth=line_thickness, edgecolor='red')

    # Affichage
    fig, ax = plt.subplots()
    ax.add_patch(shape)
    ax.set_aspect('equal')
    ax.autoscale_view()
    plt.show()






def draw_side_rectangle(side, ax):
    """Draw one rectangle along a given side: top, bottom, left, right"""

    half_h = h_mm / 2
    half_v = v_mm / 2

    if side == "top":
        x = (h_mm - half_h) / 2
        y = v_mm - border_offset - pmma_thickness_mm
        width = half_h
        height = pmma_thickness_mm

    elif side == "bottom":
        x = (h_mm - half_h) / 2
        y = border_offset
        width = half_h
        height = pmma_thickness_mm

    elif side == "left":
        x = border_offset
        y = (v_mm - half_v) / 2
        width = pmma_thickness_mm
        height = half_v

    elif side == "right":
        x = h_mm - border_offset - pmma_thickness_mm
        y = (v_mm - half_v) / 2
        width = pmma_thickness_mm
        height = half_v

    else:
        raise ValueError("side must be: top, bottom, left, or right")

    rect = Rectangle((x, y), width, height,
                     linewidth=line_thickness_pt, edgecolor="red", facecolor="none")
    ax.add_patch(rect)


def draw_topbottom(h_mm, v_mm, line_thickness_pt):
    fig, ax = plt.subplots()

    # ---- draw outer shape ----
    outer = FancyBboxPatch(
        (0, 0),
        h_mm,
        v_mm,
        boxstyle=f"round,pad=0.0,rounding_size={rounding}",
        linewidth=line_thickness_pt,
        edgecolor="red",
        facecolor="none"
    )
    ax.add_patch(outer)

    # ---- draw the four rectangles using one function ----
    for s in ["top", "bottom", "left", "right"]:
        draw_side_rectangle(s, ax)

    ax.set_xlim(-10, h_mm + 10)
    ax.set_ylim(-10, v_mm + 10)
    ax.set_aspect("equal")
    plt.show()

if __name__ == '__main__':

    pmma_thickness_mm = 3
    border_offset = 3  # distance from the side
    h_mm = 100
    v_mm = 100

    rounding = 10

    # conversion mm -> pt
    mm_to_pt = 2.834645669
    line_thickness_pt = 0.1 * mm_to_pt  # épaisseur du trait

    draw_topbottom(h_mm, v_mm, line_thickness_pt)


    largeur = h_mm  # largeur totale de la croix (bras horizontal)
    hauteur_min = 20  # hauteur du bras horizontal

    draw_side(largeur, hauteur_min, pmma_thickness_mm, line_thickness_pt)