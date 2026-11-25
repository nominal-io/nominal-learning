---
jupytext:
  text_representation:
    format_name: myst
kernelspec:
  display_name: Python 3 (ipykernel)
  language: python
  name: python3
---

# Production leak check

{.lead}
Simulate a production {gloss}`leak check` on a batch of vessels: pass or fail each vessel against its requirement, and watch the trend of the pressure drop across vessels. The data is simulated, so the notebook needs no hardware and no Nominal profile.

The test is the production test from the worked example in [Test design](../test-design.md#worked-example-one-requirement-two-tests), which explains how it differs from a design test of the same requirement. The simulation's numbers are made up for this notebook, not measured on a real vessel.

{download}`Download the notebook <leak-test.md>` to run it in JupyterLab.

**Requirements:** the packages the notebook imports: NumPy, pandas, matplotlib and `nominal-learning`. [Running the notebooks](../notebooks/running.md#one-notebook) explains how to set them up.

+++

## The requirement and the test

The vessel has this {gloss}`requirement`:

> The vessel shall lose no more than 1 psig in 60 s, after being filled to 72 psig and sealed.

The production test fills each vessel to 72 psig at room temperature, seals it, and records its pressure for 60 s. The vessel passes if its pressure drops by no more than 1 psi.

```{code-cell} ipython3
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from learning.style import set_matplotlib_style

set_matplotlib_style()  # plots that suit the page in its light and dark themes

FILL_PSIG = 72.0  # fill pressure
HOLD_S = 60.0  # how long the test records the sealed vessel's pressure
LIMIT_PSI = 1.0  # the most pressure a vessel may lose in the hold
RATE_HZ = 10  # pressure readings a second
NOISE_PSI = 0.02  # the pressure sensor's noise, as a standard deviation

t = np.arange(int(HOLD_S * RATE_HZ) + 1) / RATE_HZ  # 0 to 60 s
```

The simulation gives each vessel a constant leak rate, so its pressure falls in a straight line, and adds noise to every reading. The test takes the pressure drop from the slope of a straight line fitted to all the readings in the hold:

```{code-cell} ipython3
def leak_down(loss_psi, rng):
    """Simulate the pressure of a vessel that loses `loss_psi` in the hold."""
    no_noise = FILL_PSIG - loss_psi * t / HOLD_S  # a straight line down from 72 psig
    return no_noise + rng.normal(0, NOISE_PSI, t.size)


def pressure_drop(pressure):
    """Return the pressure lost over the hold, from a straight line fitted to it."""
    slope = np.polyfit(t, pressure, 1)[0]  # psi/s
    return -slope * HOLD_S


def judge(drop):
    """Pass or fail a vessel on its pressure drop."""
    return "pass" if drop <= LIMIT_PSI else "fail"
```

## Check the test

Before the test judges production vessels, run it on a {gloss}`golden vessel <golden unit>`, known to be good, and on a vessel known to leak. [Test design](../test-design.md#the-golden-unit) explains why it needs both. The test has to pass the first and fail the second:

```{code-cell} ipython3
rng = np.random.default_rng(1)
# The golden vessel loses 0.20 psi in 60 s, and the leaky one 2.50 psi.
check = {
    "golden vessel": leak_down(0.20, rng),
    "leaky vessel": leak_down(2.50, rng),
}

for name, pressure in check.items():
    drop = pressure_drop(pressure)
    print(f"{name}: lost {drop:.2f} psi in 60 s, {judge(drop)}")
```

The golden vessel's pressure stays well above 71 psig, 1 psi below the fill pressure, while the leaky vessel's falls below it after about 24 s:

```{code-cell} ipython3
fig, ax = plt.subplots()
for name, pressure in check.items():
    ax.plot(t, pressure, label=name)
lowest = FILL_PSIG - LIMIT_PSI  # the lowest pressure that passes at 60 s, psig
ax.axhline(lowest, color="C4", linestyle="--", label="72 psig − 1 psi")
ax.set(xlabel="Time since sealing (s)", ylabel="Pressure (psig)")
ax.legend(loc="lower left");
```

## Test a batch

Test 100 vessels in the order they were built. From vessel 41 on, the simulated leak rate rises a little with each vessel:

```{code-cell} ipython3
rng = np.random.default_rng(27)
vessel = np.arange(1, 101)
# Loss in 60 s, psi: about 0.30, then 0.012 more for each vessel after vessel 40.
loss = rng.normal(0.30, 0.06, vessel.size) + 0.012 * np.clip(vessel - 40, 0, None)
pressures = [leak_down(loss_psi, rng) for loss_psi in loss]

drops = np.array([pressure_drop(p) for p in pressures])
results = pd.Series([judge(d) for d in drops], index=vessel)
print(results.value_counts().to_string())
print(f"failed: vessels {results.index[results == 'fail'].to_list()}")
```

## Watch the trend

Pass or fail alone shows nothing until a vessel fails. To see the rise sooner, plot every vessel's pressure drop on an individuals control chart, as in [Statistical analysis and DOE](../statistical-analysis.md#control-charts). The first 40 vessels set the limits, and the chart flags a vessel beyond them, or the eighth in a row on one side of the center line:

```{code-cell} ipython3
baseline = drops[:40]
center = baseline.mean()
sigma = np.abs(np.diff(baseline)).mean() / 1.128  # from the average moving range
ucl, lcl = center + 3 * sigma, center - 3 * sigma

beyond = vessel[(drops > ucl) | (drops < lcl)]
side = np.sign(drops - center)  # +1 above the center line, −1 below
run_of_8 = vessel[7:][np.abs(np.convolve(side, np.ones(8), "valid")) == 8]
first_flag = min(beyond.min(), run_of_8.min())
print(f"center line {center:.2f} psi, UCL {ucl:.2f} psi, LCL {lcl:.2f} psi")
print(f"first beyond the limits: vessel {beyond.min()}")
print(f"first eighth in a row on one side: vessel {run_of_8.min()}")
```

```{code-cell} ipython3
passed = drops <= LIMIT_PSI
fig, ax = plt.subplots()
ax.plot(vessel[passed], drops[passed], ".", label="pass")
ax.plot(vessel[~passed], drops[~passed], "x", color="C4", label="fail")
ax.axhline(LIMIT_PSI, color="C4", label="test limit")
ax.axhline(center, color="C1", label="center line")
ax.axhline(ucl, color="C1", linestyle="--", label="control limits")
ax.axhline(lcl, color="C1", linestyle="--")
ax.axvline(first_flag, color="grey", linestyle=":", label="first flag")
ax.set(xlabel="Vessel, in build order", ylabel="Pressure drop in 60 s (psi)")
ax.legend(loc="lower left", bbox_to_anchor=(0, 1), ncols=3);  # above the plot
```

Vessels 1 to 93 all pass, while their pressure drops climb toward the test limit from vessel 41 on. The chart flags vessel 50, the eighth in a row above the center line, and vessel 54 is the first beyond the upper control limit. Both come about 40 vessels before the first failure, at vessel 94. That's the warning that [Test design](../test-design.md#worked-example-one-requirement-two-tests) describes: a slow rise across passing vessels warns of a process problem before vessels start to fail.
