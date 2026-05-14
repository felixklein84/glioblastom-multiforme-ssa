"""Shared plotting style — colors, fonts, sizes.

The only module that touches matplotlib rcParams.
"""

from __future__ import annotations

import matplotlib as mpl

# Consistent palette for the 4 states across all plots
STATE_COLORS: dict[str, str] = {
    "S": "#1f77b4",   # blue   — GSC
    "P": "#ff7f0e",   # orange — Progenitor
    "D": "#2ca02c",   # green  — Differentiated
    "Q": "#9467bd",   # purple — Quiescent
}

TOTAL_COLOR = "#444444"


def apply() -> None:
    """Apply package-wide matplotlib defaults."""
    mpl.rcParams.update({
        "figure.figsize": (8.0, 4.5),
        "figure.dpi": 110,
        "savefig.dpi": 150,
        "savefig.bbox": "tight",
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linestyle": ":",
        "font.size": 10,
        "legend.frameon": False,
    })
