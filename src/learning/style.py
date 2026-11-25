"""Plotly and matplotlib styles for the notebooks' plots."""

from __future__ import annotations

TEMPLATE = "learning"
"""Name the style is registered under in ``plotly.io.templates``."""

_GRID = "rgba(128, 128, 128, 0.2)"
_TEXT = "#8a8a8a"
# plotly's qualitative palette, starting at teal, as in the plotly style
COLORS = [
    "#00CC96",
    "#AB63FA",
    "#FFA15A",
    "#19D3F3",
    "#FF6692",
    "#B6E880",
    "#FF97FF",
    "#FECB52",
    "#636EFA",
    "#EF553B",
]
"""The color cycle of both styles, starting at teal."""


def set_matplotlib_style() -> None:
    """Make matplotlib's figures suit the docs pages, in both dark and light themes.

    Figures are wide, with a transparent background, grey text and faint gridlines, and lines start at
    teal. In a Jupyter kernel, figures are drawn as SVG, so they stay sharp on the page. It applies to
    every figure made afterwards.

    Needs matplotlib.
    """
    import matplotlib as mpl
    from cycler import cycler

    mpl.rcParams.update(
        {
            "figure.figsize": (8, 3.2),
            "figure.facecolor": "none",
            "axes.facecolor": "none",
            "savefig.transparent": True,
            "axes.edgecolor": _TEXT,
            "axes.labelcolor": _TEXT,
            "axes.titlecolor": _TEXT,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.color": "#808080",
            "grid.alpha": 0.2,
            "xtick.color": _TEXT,
            "ytick.color": _TEXT,
            "text.color": _TEXT,
            "legend.frameon": False,
            "axes.prop_cycle": cycler(color=COLORS),
        }
    )
    try:
        from matplotlib_inline.backend_inline import set_matplotlib_formats
    except ImportError:  # not in a Jupyter kernel's environment
        return
    set_matplotlib_formats("svg")


def set_plotly_style() -> None:
    """Make the learning style the default for plotly figures.

    The style is wide and transparent, with faint gridlines and grey text, so plots sit on the page in
    both dark and light themes. Lines start at teal. It applies to every plotly figure made afterwards.

    The style is registered as ``"learning"`` and layered on ``plotly_white``. To use it for one figure,
    pass ``template="plotly_white+learning"`` after calling this once.

    Needs plotly, from the ``plotly`` extra (``nominal-learning[plotly]``).
    """
    import plotly.io as pio
    from plotly.colors import qualitative

    axis = dict(gridcolor=_GRID, linecolor=_GRID, zeroline=False)
    pio.templates[TEMPLATE] = dict(
        layout=dict(
            paper_bgcolor="rgba(0, 0, 0, 0)",
            plot_bgcolor="rgba(0, 0, 0, 0)",
            font=dict(color="#8a8a8a", family="Geist, sans-serif"),
            colorway=qualitative.Plotly[2:] + qualitative.Plotly[:2],  # teal first
            height=320,
            margin=dict(l=50, r=10, t=40, b=40),
            xaxis=axis,
            yaxis=axis,
            legend=dict(orientation="h", x=0, y=1.02, yanchor="bottom"),  # top left, clear of the toolbar
            hovermode="x unified",
        )
    )
    pio.templates.default = f"plotly_white+{TEMPLATE}"
