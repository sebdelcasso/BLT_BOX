# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BLT_BOX is a technical drawing/CAD visualization tool for designing box layouts with PMMA (acrylic) panels. It generates matplotlib plots and SVG exports of geometric shapes (rounded rectangles, cross shapes) used in box fabrication.

## Commands

**Package manager:** `uv`

```bash
# Install dependencies
uv sync

# Run the GUI (recommended)
uv run python gui.py

# Run the headless script (outputs combined_shape.svg + matplotlib window)
uv run python box.py
```

No build, test, or lint tooling is currently configured.

## Architecture

**`box.py`** — Core drawing library. All functions are fully parameterized (no globals):

- `draw_cross()`: renders cross-shaped PMMA elements
- `draw_side_rectangle()`: renders rectangular border elements (top/bottom/left/right)
- `draw_topbottom()`: renders the main rounded rectangular frame with side borders
- `draw_all()`: assembles the full layout (2 top/bottom frames + 4 crosses)

The `__main__` block runs `draw_all()` with hardcoded defaults and exports `combined_shape.svg`.

**`gui.py`** — Tkinter GUI that imports from `box.py`. Provides sliders for all parameters (h, v, PMMA thickness, border offset, rounding, cross height, line thickness) with a live matplotlib preview embedded in the window and an SVG export button.

All geometry is drawn using `matplotlib.patches` (FancyBboxPatch, Rectangle) and `matplotlib.path.Path`. Dimensions represent real-world measurements in millimeters; code comments are in French.
