"""Draw the thumbnails on the category pages' cards, as SVGs in ``docs/_static/thumbnails/``.

Run with ``just gen-thumbnails``. Each is a small, simplified picture of the page's topic, drawn in
grey and teal on a transparent background, so it reads in the light and dark themes. The data is
made up, and seeded, so rerunning the script reproduces the files.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import matplotlib

matplotlib.use("svg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.axes import Axes  # noqa: E402

OUT = Path(__file__).parent.parent / "docs" / "_static" / "thumbnails"
GREY = "#8c8c8c"
TEAL = "#00b386"
ORANGE = "#f28e2b"
RNG = np.random.default_rng(42)

plt.rcParams.update(
    {
        "svg.fonttype": "path",
        "svg.hashsalt": "learning",
        "font.size": 9,
        "text.color": GREY,
        "axes.edgecolor": GREY,
        "axes.labelcolor": GREY,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.linewidth": 1,
        "lines.linewidth": 1.6,
    }
)


def _axes(ax: Axes, xlabel: str, ylabel: str) -> None:
    """Label a plot's axes and leave out its ticks."""
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_facecolor("none")


def _diagram(ax: Axes) -> None:
    """Turn the axes off, for a drawing rather than a plot."""
    ax.set_axis_off()
    ax.set_xlim(0, 4)
    ax.set_ylim(0, 3)


def frequency_domain(ax: Axes) -> None:
    """A spectrum: a noise floor with peaks at a few frequencies."""
    f = np.linspace(0, 500, 2000)
    level = -80 + 3 * RNG.standard_normal(f.size)
    for f0, height in [(50, 25), (120, 18), (180, 40), (240, 70), (300, 35), (360, 25), (420, 12)]:
        level = np.maximum(level, -80 + height * np.exp(-(((f - f0) / 2.5) ** 2)))
    ax.plot(f, level, color=TEAL, linewidth=1.2)
    _axes(ax, "Frequency (Hz)", "Magnitude (dB)")


def statistical_analysis(ax: Axes) -> None:
    """A control chart: points around a mean, between control limits."""
    x = np.arange(25)
    y = RNG.normal(0, 1, x.size)
    for level, style in [(0, "-"), (3, "--"), (-3, "--")]:
        ax.axhline(level, color=GREY, linestyle=style, linewidth=1)
    ax.plot(x, y, color=TEAL, marker="o", markersize=3.5)
    ax.set_ylim(-4, 4)
    _axes(ax, "Sample", "Value")


def sensors_and_instrumentation(ax: Axes) -> None:
    """A 4–20 mA transmitter's output: 4 mA at the bottom of its range, 20 mA at the top."""
    ax.plot([0, 100], [4, 20], color=TEAL)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 22)
    _axes(ax, "Pressure", "Current (mA)")
    ax.set_yticks([4, 20])
    ax.tick_params(colors=GREY)


def measurement_quality(ax: Axes) -> None:
    """Readings spread around a mean that is off from the true value."""
    readings = RNG.normal(10.4, 0.25, 400)
    ax.hist(readings, bins=24, color=TEAL, alpha=0.8)
    ax.axvline(10, color=GREY, linestyle="--", linewidth=1)
    ax.text(9.97, ax.get_ylim()[1] * 0.92, "true value", ha="right")
    _axes(ax, "Reading", "Count")


def test_design(ax: Axes) -> None:
    """The V-model, simplified to three levels: design down the left, tests up the right."""
    _diagram(ax)
    left = ["Requirements", "System design", "Component\ndesign"]
    right = ["Acceptance test", "System test", "Component\ntest"]
    for level, (design, test) in enumerate(zip(left, right, strict=True)):
        y = 2.65 - 0.75 * level
        x0, x1 = 0.1 + 0.55 * level, 3.9 - 0.55 * level
        ax.plot([x0 + 0.05, x1 - 0.05], [y, y], color=GREY, linewidth=0.8, linestyle=":")
        ax.text(x0, y + 0.1, design, ha="left", va="bottom", fontsize=8.5)
        ax.text(x1, y + 0.1, test, ha="right", va="bottom", fontsize=8.5)
    ax.plot([0.1, 2, 3.9], [2.65, 0.05, 2.65], color=TEAL)
    ax.text(2, 0.4, "Build", ha="center", fontsize=8.5)


def control(ax: Axes) -> None:
    """A step response: the measurement overshoots the new setpoint, then settles on it."""
    t = np.linspace(0, 10, 500)
    setpoint = np.where(t < 1, 0, 1.0)
    tau = np.clip(t - 1, 0, None)
    zeta, wn = 0.35, 2.2
    wd = wn * np.sqrt(1 - zeta**2)
    response = 1 - np.exp(-zeta * wn * tau) * (np.cos(wd * tau) + zeta / np.sqrt(1 - zeta**2) * np.sin(wd * tau))
    ax.plot(t, setpoint, color=GREY, linestyle="--", linewidth=1)
    ax.plot(t, np.where(t < 1, 0, response), color=TEAL)
    ax.text(9.8, 1.06, "setpoint", ha="right")
    ax.set_ylim(-0.1, 1.5)
    _axes(ax, "Time", "Measurement")


def distributed_control(ax: Axes) -> None:
    """Three controllers on one network, each with its own I/O."""
    _diagram(ax)
    ax.plot([0.3, 3.7], [2.4, 2.4], color=GREY, linewidth=1)
    for x in (0.8, 2, 3.2):
        ax.plot([x, x], [2.4, 1.9], color=GREY, linewidth=1)
        ax.add_patch(plt.Rectangle((x - 0.4, 1.4), 0.8, 0.5, fill=False, edgecolor=TEAL, linewidth=1.6))
        for dx in (-0.25, 0.25):
            ax.plot([x + dx, x + dx], [1.4, 0.95], color=GREY, linewidth=1)
            ax.add_patch(plt.Circle((x + dx, 0.8), 0.15, fill=False, edgecolor=GREY, linewidth=1))
    ax.text(2, 2.55, "network", ha="center")


def alarms(ax: Axes) -> None:
    """A measurement crosses its alarm limit, and comes back down after the operator responds."""
    t = np.linspace(0, 10, 500)
    y = 50 + 25 * np.exp(-(((t - 5) / 1.6) ** 2)) + RNG.normal(0, 0.6, t.size)
    limit = 65
    ax.axhline(limit, color=GREY, linestyle="--", linewidth=1)
    ax.plot(t, y, color=TEAL)
    ax.fill_between(t, limit, y, where=y > limit, color=ORANGE, alpha=0.5)
    ax.text(0.2, limit + 1.5, "alarm limit")
    ax.set_ylim(40, 82)
    _axes(ax, "Time", "Temperature")


def safety(ax: Axes) -> None:
    """A measurement reaches its trip limit, and the safety function shuts the equipment down."""
    t = np.linspace(0, 10, 500)
    trip = 6.2
    y = np.where(t < trip, 20 + 60 / (1 + np.exp(-(t - 4.2) * 1.2)), 0)
    y = np.where(t < trip, y, 80 * np.exp(-(t - trip) * 3))
    ax.axhline(75, color=GREY, linestyle="--", linewidth=1)
    ax.plot(t, y, color=TEAL)
    ax.text(0.2, 77, "trip limit")
    ax.set_ylim(-5, 92)
    _axes(ax, "Time", "Pressure")


def communications(ax: Axes) -> None:
    """The three layers that the communications guide merges the OSI model into."""
    _diagram(ax)
    for i, name in enumerate(["Physical layer", "Protocol layer", "Application layer"]):
        y = 0.3 + 0.85 * i
        color = TEAL if i == 0 else GREY
        ax.add_patch(plt.Rectangle((0.6, y), 2.8, 0.65, fill=False, edgecolor=color, linewidth=1.6))
        ax.text(2, y + 0.325, name, ha="center", va="center", fontsize=10)


def network_performance(ax: Axes) -> None:
    """Data offered faster than the link carries: the link delivers its capacity, and the rest waits."""
    t = np.linspace(0, 10, 500)
    offered = 30 + 70 / (1 + np.exp(-(t - 5) * 1.3))
    capacity = 70
    ax.axhline(capacity, color=GREY, linestyle="--", linewidth=1)
    ax.plot(t, offered, color=GREY, linewidth=1.2)
    ax.plot(t, np.minimum(offered, capacity), color=TEAL)
    ax.text(0.2, capacity + 3, "link capacity")
    ax.text(9.8, 92, "offered", ha="right")
    ax.set_ylim(0, 110)
    _axes(ax, "Time", "Data rate")


def engineering_data(ax: Axes) -> None:
    """Several channels, sampled over the same time."""
    t = np.linspace(0, 10, 600)
    channels = [
        np.sin(2 * np.pi * 0.6 * t) + 0.15 * RNG.standard_normal(t.size),
        np.clip((t - 2) / 4, 0, 1) + 0.04 * RNG.standard_normal(t.size),
        np.where((t % 3) < 1.5, 1.0, 0.0),
    ]
    for i, y in enumerate(channels):
        y = (y - y.min()) / (y.max() - y.min())
        ax.plot(t, y * 0.8 + 1.2 * i, color=TEAL if i == 0 else GREY, linewidth=1.2)
    _axes(ax, "Time", "Channels")


def bench_bringup(ax: Axes) -> None:
    """The DMM reads 12 V until its leads move from the 12 V output to the 5 V rail."""
    t = np.linspace(0, 10, 500)
    v = np.where(t < 6, 12.0, 5.0) + RNG.normal(0, 0.05, t.size)
    ax.axhline(5, color=GREY, linestyle="--", linewidth=1)
    ax.plot(t, v, color=TEAL)
    ax.text(0.2, 5.5, "5 V rail")
    ax.set_ylim(0, 14)
    _axes(ax, "Time", "DMM voltage")


def leak_check(ax: Axes) -> None:
    """Each vessel's pressure drop: passing units creep up toward the limit before any fails."""
    units = np.arange(1, 61)
    drop = 0.3 + 0.012 * np.clip(units - 25, 0, None) + RNG.normal(0, 0.04, units.size)
    ax.axhline(1.0, color=GREY, linestyle="--", linewidth=1)
    ax.plot(units, drop, color=TEAL, marker="o", markersize=3, linewidth=1)
    ax.text(1, 1.04, "limit")
    ax.set_ylim(0, 1.2)
    _axes(ax, "Vessel", "Pressure drop")


THUMBNAILS: dict[str, Callable[[Axes], None]] = {
    "frequency-domain": frequency_domain,
    "statistical-analysis": statistical_analysis,
    "sensors-and-instrumentation": sensors_and_instrumentation,
    "measurement-quality": measurement_quality,
    "test-design": test_design,
    "control": control,
    "distributed-control": distributed_control,
    "alarms": alarms,
    "safety": safety,
    "communications": communications,
    "network-performance": network_performance,
    "engineering-data": engineering_data,
    "bench-bringup": bench_bringup,
    "leak-check": leak_check,
}


def main() -> None:
    """Draw every thumbnail."""
    OUT.mkdir(parents=True, exist_ok=True)
    for name, draw in THUMBNAILS.items():
        fig, ax = plt.subplots(figsize=(4, 3))
        fig.patch.set_alpha(0)
        draw(ax)
        fig.tight_layout()
        fig.savefig(OUT / f"{name}.svg", transparent=True, metadata={"Date": None})
        plt.close(fig)


if __name__ == "__main__":
    main()
