import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, PathPatch
from matplotlib.path import Path

def draw_cross(ax, largeur, hauteur_min, pmma_thickness, x_offset=0, y_offset=0):
    """
    Dessine une croix centrée avec possibilité de décalage.
    :param ax: axes matplotlib
    :param largeur: largeur totale de la croix (bras horizontal)
    :param hauteur_min: hauteur du bras horizontal
    :param pmma_thickness: épaisseur PMMA ajoutée aux bras
    :param x_offset: décalage en x
    :param y_offset: décalage en y
    """
    hauteur_totale = hauteur_min + 2*pmma_thickness
    largeur_bras_vertical = largeur / 2

    L = largeur / 2
    H = hauteur_totale / 2
    bw = largeur_bras_vertical / 2
    bh = hauteur_min / 2

    vertices = [
        (-L, bh),
        (-bw, bh),
        (-bw, H),
        (bw, H),
        (bw, bh),
        (L, bh),
        (L, -bh),
        (bw, -bh),
        (bw, -H),
        (-bw, -H),
        (-bw, -bh),
        (-L, -bh),
        (-L, bh)
    ]

    # Appliquer offset
    vertices = [(x + x_offset, y + y_offset) for x, y in vertices]

    codes = [Path.MOVETO] + [Path.LINETO]*(len(vertices)-1)
    path = Path(vertices, codes)
    cross = PathPatch(path, fill=False, linewidth=line_thickness_pt, edgecolor='red')
    ax.add_patch(cross)


def draw_side_rectangle(side, ax, h_mm, v_mm, pmma_thickness, x_offset=0, y_offset=0):
    """
    Dessine un rectangle latéral avec possibilité de décalage.
    :param side: "top", "bottom", "left", "right"
    :param ax: axes matplotlib
    :param h_mm: largeur totale
    :param v_mm: hauteur totale
    :param pmma_thickness: épaisseur du rectangle
    :param x_offset: décalage en x
    :param y_offset: décalage en y
    """
    half_h = h_mm / 2
    half_v = v_mm / 2

    if side == "top":
        x = (h_mm - half_h) / 2
        y = v_mm - border_offset - pmma_thickness
        width = half_h
        height = pmma_thickness
    elif side == "bottom":
        x = (h_mm - half_h) / 2
        y = border_offset
        width = half_h
        height = pmma_thickness
    elif side == "left":
        x = border_offset
        y = (v_mm - half_v) / 2
        width = pmma_thickness
        height = half_v
    elif side == "right":
        x = h_mm - border_offset - pmma_thickness
        y = (v_mm - half_v) / 2
        width = pmma_thickness
        height = half_v
    else:
        raise ValueError("side must be: top, bottom, left, or right")

    # Appliquer l'offset
    x += x_offset
    y += y_offset

    rect = Rectangle((x, y), width, height, linewidth=line_thickness_pt, edgecolor="red", facecolor="none")
    ax.add_patch(rect)


def draw_topbottom(ax, h_mm, v_mm, rounding, x_offset=0, y_offset=0):
    """
    Dessine le rectangle arrondi avec les 4 rectangles latéraux, avec offset.
    """
    # Rectangle extérieur
    outer = FancyBboxPatch(
        (0 + x_offset, 0 + y_offset),
        h_mm,
        v_mm,
        boxstyle=f"round,pad=0.0,rounding_size={rounding}",
        linewidth=line_thickness_pt,
        edgecolor="red",
        facecolor="none"
    )
    ax.add_patch(outer)

    # 4 rectangles latéraux
    for s in ["top", "bottom", "left", "right"]:
        draw_side_rectangle(s, ax, h_mm, v_mm, pmma_thickness_mm, x_offset=x_offset, y_offset=y_offset)


if __name__ == "__main__":

    # Paramètres
    pmma_thickness_mm = 3
    border_offset = 3
    h_mm = 80
    v_mm = 80
    rounding = 10
    line_thickness_mm = 0.1
    mm_to_pt = 2.834645669
    line_thickness_pt = line_thickness_mm * mm_to_pt

    # Croix centrale
    largeur_croix = h_mm
    hauteur_croix = 20


    fig, ax = plt.subplots()
    y_offset = 0
    for i in range(2):
        draw_topbottom(ax, h_mm, v_mm, rounding, x_offset=0, y_offset=y_offset)
        y_offset += v_mm

    for i in range(2):
        draw_cross(ax, largeur_croix, hauteur_croix, pmma_thickness_mm, x_offset=largeur_croix/2, y_offset=y_offset+(hauteur_croix/2)+pmma_thickness_mm)
        y_offset += (hauteur_croix + (pmma_thickness_mm*2))

    largeur_croix = v_mm - (2*pmma_thickness_mm)

    for i in range(2):
        draw_cross(ax, largeur_croix, hauteur_croix, pmma_thickness_mm, x_offset=largeur_croix/2, y_offset=y_offset+(hauteur_croix/2)+pmma_thickness_mm)
        y_offset += (hauteur_croix + (pmma_thickness_mm*2))



    ax.set_aspect('equal')
    ax.autoscale_view()

    # Sauvegarde SVG
    plt.savefig("combined_shape.svg", format="svg")
    plt.show()
