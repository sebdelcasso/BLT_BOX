# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BLT_BOX is a technical drawing/CAD visualization tool for designing box layouts with PMMA (acrylic) panels. It generates matplotlib plots and SVG exports of geometric shapes (rounded rectangles, cross shapes) used in box fabrication.

## Commands

**Package manager:** `uv`

```bash
# Install dependencies
uv sync

# Run the main visualization (outputs combined_shape.svg + matplotlib window)
uv run python box.py

# Run the alternative top/bottom visualization
uv run python main.py
```

No build, test, or lint tooling is currently configured.

## Architecture

Single entry point: **`box.py`**. Contains:

- `draw_cross()`: renders cross-shaped PMMA elements
- `draw_side_rectangle()`: renders rectangular border elements (top/bottom/left/right)
- `draw_topbottom()`: renders the main rounded rectangular frame with side borders

The `__main__` block assembles a combined layout (2 top/bottom frames + 4 crosses) and exports `combined_shape.svg`.

All geometry is drawn using `matplotlib.patches` (FancyBboxPatch, Rectangle) and `matplotlib.path.Path`. Dimensions represent real-world measurements in millimeters; code comments are in French.