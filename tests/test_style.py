import pytest


def test_set_plotly_style_registers_the_template():
    pio = pytest.importorskip("plotly.io")
    from learning.style import TEMPLATE, set_plotly_style

    previous = pio.templates.default
    try:
        set_plotly_style()
        assert TEMPLATE in pio.templates
        assert pio.templates.default == f"plotly_white+{TEMPLATE}"
    finally:
        pio.templates.default = previous


def test_set_matplotlib_style_sets_the_colors():
    mpl = pytest.importorskip("matplotlib")
    from learning.style import COLORS, set_matplotlib_style

    with mpl.rc_context():
        set_matplotlib_style()
        assert mpl.rcParams["axes.prop_cycle"].by_key()["color"][0] == COLORS[0]
        assert mpl.rcParams["figure.facecolor"] == "none"
