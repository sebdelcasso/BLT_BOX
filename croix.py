import matplotlib.pyplot as plt
from matplotlib.path import Path
from matplotlib.patches import PathPatch






if __name__ == '__main__':
    largeur = 80  # largeur totale de la croix (bras horizontal)
    hauteur_min = 20  # hauteur du bras horizontal
    pmma_thickness_mm = 3
    line_thickness_mm = 0.1
    # Conversion mm -> points
    mm_to_pt = 2.834645669
    line_thickness = line_thickness_mm * mm_to_pt
    draw_side(largeur, hauteur_min, pmma_thickness_mm, line_thickness)