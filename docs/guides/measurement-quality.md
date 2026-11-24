# Measurement quality

{.lead}
Every measurement is off by some amount. To trust a result, you need to know by how much.

## Accuracy, precision and resolution

These three words describe different things, and a measurement can be good at one and poor at another.

- {gloss}`Accuracy` is how close a reading is to the true value.
- {gloss}`Precision` is how close repeated readings of the same value are to each other.
- {gloss}`Resolution` is the smallest change a reading can show.

A pressure gauge that always reads 2 psig high is precise, but not accurate. A 16-bit module reading a pressure transducer can show steps of 0.002 psig, while the transducer itself is accurate only to ±0.5 psig. The worked example below shows where those numbers come from.

## Kinds of error

| Error | What it does | How to deal with it |
| --- | --- | --- |
| Offset, or zero error | Shifts every reading by the same amount | Calibrate it out, or check the reading at zero |
| Gain, or span error | Scales every reading by a small percentage, so it grows with the reading | Calibrate it out |
| Nonlinearity | Bends the response away from a straight line | Calibrate at several points, or accept it |
| Hysteresis | Makes the reading depend on whether the value is rising or falling | Approach each test point from the same direction |
| Non-repeatability | Gives slightly different readings for the same value | Average, or accept it |
| Noise | Adds random variation to each reading | Average, filter, or improve wiring and shielding |
| Drift | Moves the reading slowly over time or with temperature | Recalibrate on a schedule, and control temperature |

Offset, gain and nonlinearity are the same every time, so calibration can remove them. Hysteresis is repeatable too, but it depends on direction. Noise and non-repeatability are random, so averaging reduces them. Drift is slow, so a calibration removes it only until the reading drifts again.

Datasheets state errors in two ways. A percentage of span, the full output range, is a fixed amount across the range. A percentage of reading scales with the value. The NI-9203 current input module, for example, states its gain error as a percentage of reading and its offset error as a percentage of range.[^ni-9203]

## Bits and resolution

An {gloss}`analog-to-digital converter <analog-to-digital converter>` (ADC) divides its input range into steps. An N-bit ADC has 2{sup}`N` steps, so each step, one least significant bit (LSB), is the range divided by 2{sup}`N`.

The NI-9203 has a 16-bit ADC. In its unipolar mode it measures 0 to 20 mA, with 6.5% of overrange, for a range of 21.5 mA. That gives 330 nA per step.[^ni-9203]

A 4–20 mA sensor uses only 16 mA of that range, so a 0–100 psig transducer gets about 48,500 steps, or about 0.002 psig per step. The unused steps below 4 mA aren't wasted: a reading near 0 mA means a broken wire.

Converting to the nearest step adds an error of up to half a step. For an ideal N-bit converter, that sets a best possible signal-to-noise ratio of 6.02 × N + 1.76 dB, or 98 dB for 16 bits.[^ee-quantization] Real converters add their own noise. The NI-9203's input noise is 1 LSB RMS, and its nonlinearity is up to ±3 LSB.[^ni-9203]

More bits don't mean more accuracy. The NI-9203's calibrated offset error alone is 0.06% of its range, 12.9 µA, which is about 39 steps.[^ni-9203] Steps smaller than that offset are real changes in the signal, but they don't say what the true value is.

## Sample rate and aliasing

To capture a signal, sample faster than twice the highest frequency in it. Content above half the sample rate shows up in the data at false, lower frequencies. This is {gloss}`aliasing`, and it can't be undone afterwards, so an anti-aliasing filter goes before the ADC.[^ee-sampling]

The NI-9203 samples at up to 200,000 samples per second,[^ni-9203] far faster than a pressure transducer can respond: the WIKA A-10's response time is under 4 ms.[^wika-a10] On a fluids panel, which runs compressed air through valves and pressure transducers, the pressures change over seconds, so a low sample rate is enough for them.

On an e-axle {gloss}`dyno <dynamometer>`, where a motor drives the e-axle under test and load motors brake it, the software reads each motor controller about 16 times a second. That's enough to follow changes slower than 8 Hz, such as speed steps and temperature, but not to measure vibration. [Frequency domain](frequency-domain.md#worked-example-what-an-e-axle-dynos-data-can-show) works out which of the dyno's frequencies that rules out, and what an accelerometer would need.

## Worked example: an error budget for a pressure reading

The fluids panel's supply pressure, `p_1`, is a 0–100 psig transducer with a 4–20 mA output, read by an NI current input module. This example works out how accurate a reading of 85 psig is, using a real transducer and module:

- The transducer is a WIKA A-10, 0–100 psig, 4–20 mA, with the 0.25% nonlinearity option. Its accuracy is ±0.5% of span, which includes nonlinearity, hysteresis, offset and gain error. Its long-term drift is ±0.1% of span.[^wika-a10]
- The module is an NI-9203 in unipolar mode, calibrated, anywhere from −40 °C to 70 °C. Its maximum gain error is ±0.18% of reading, and its maximum offset error is ±0.06% of its 21.5 mA range.[^ni-9203]
- The stand is indoors at 15–25 °C, the transducer's reference temperature, so the transducer's temperature error doesn't apply.[^wika-a10]

### 1. Find the signal

The transducer maps 0–100 psig to 4–20 mA, so 1 mA is 6.25 psig, and 85 psig is:

```text
4 mA + (85 / 100) × 16 mA = 17.6 mA
```

### 2. Add up the module's error

NI's formula for a C Series module's absolute accuracy is the reading times the gain error, plus the range times the offset error, plus noise.[^ni-accuracy]

```text
gain:    17.6 mA × 0.18% = 31.7 µA
offset:  21.5 mA × 0.06% = 12.9 µA
noise:   3 × 0.33 µA ÷ √100 ≈ 0.1 µA   (3 sigma, averaging 100 readings)
total:                     ≈ 44.7 µA
```

At 6.25 psig per mA, 44.7 µA is ±0.28 psig. At the module's typical accuracy, near 25 °C, the same sum is 11.4 µA, or ±0.07 psig.

### 3. Add up the transducer's error

```text
accuracy:  0.5% × 100 psig = 0.50 psig
drift:     0.1% × 100 psig = 0.10 psig
```

### 4. Combine them

When errors are independent, NI combines them as the square root of the sum of their squares (RSS).[^ni-accuracy] The worst case adds them directly:

| Source | Error (psig) |
| --- | ---: |
| Transducer accuracy | ±0.50 |
| Transducer long-term drift | ±0.10 |
| NI-9203 accuracy, calibrated maximum | ±0.28 |
| Combined, RSS | ±0.58 |
| Combined, worst case | ±0.88 |

The reading is 85.0 psig, give or take about 0.6 psig.

- The transducer dominates. A better module wouldn't help much. A better transducer, or a calibration of the whole chain against a reference gauge, would.
- The resolution, 0.002 psig, is about 300 times finer than the accuracy. Don't report more digits than the accuracy supports.
- Without calibration, the module alone could be off by up to 232 µA, or ±1.45 psig, using the NI-9203's uncalibrated maximum errors of ±0.66% of reading and ±0.54% of range.[^ni-9203]

Outside its reference temperature, the transducer's temperature error can reach 1.0% of span typically and 2.5% at most, ±2.5 psig, over its 0–80 °C operating range.[^wika-a10] That would dominate every other error in the budget.

The transducer's signal noise, up to 0.3% of span,[^wika-a10] is random, so averaging reduces it. Averaging 100 readings divides random noise by √100, a factor of 10.[^ni-accuracy]

## Uncertainty

The error budget above gives limits. Metrology states the same result as an {gloss}`uncertainty`, using the method in the *Guide to the expression of uncertainty in measurement* (GUM).[^gum]

The GUM combines standard uncertainties, which are like standard deviations. To turn a datasheet limit of ±a into a standard uncertainty, treat the true error as equally likely anywhere in that range, which gives a/√3. Combine the standard uncertainties by RSS, then multiply by a coverage factor, k. With k = 2, the result covers about 95% of cases.[^nist-tn1297] To estimate a standard uncertainty from repeated readings, see [Describing a set of results](statistical-analysis.md#describing-a-set-of-results).

For the example above:

```text
combined standard uncertainty:  0.58 psig ÷ √3 = 0.34 psig
expanded uncertainty (k = 2):   2 × 0.34 psig ≈ 0.7 psig
```

So the reading is 85.0 psig ± 0.7 psig, at k = 2.

## Calibration

{gloss}`Calibration` compares an instrument with a known reference and corrects or records the difference. The NI-9203 ships with a NIST-traceable calibration, and NI recommends recalibrating it every year.[^ni-9203] Traceable means each reference was itself calibrated, in a chain back to a national standard.

A module calibration covers the module, not the transducer. To calibrate the whole chain, apply known pressures from a reference, record the readings, and fit a correction. That removes the repeatable errors of every part at once.

## Checks you can do on a stand

Each check finds one kind of error from [Kinds of error](#kinds-of-error):

- **Zero check.** Vent the fluids panel and read `p_1`. It should read 0 psig. Anything else is offset error.
- **Two-sensor check.** Where two sensors measure the same thing, compare them. A difference that grows with the value is gain error.
- **Repeatability check.** Run the same step twice and compare the readings.
- **Noise check.** Hold a steady condition, and look at the spread of the readings. On the dyno, hold a speed and compare the standard deviation of the speed channel with the speed itself.
- **Hysteresis check.** Step a value up, then back down through the same points, and compare.

## Further reading

- NI, [Calculating Absolute Accuracy or System Accuracy](https://www.ni.com/en/support/documentation/supplemental/18/calculating-absolute-accuracy-or-system-accuracy.html).
- JCGM, [Guide to the expression of uncertainty in measurement (GUM) and the International Vocabulary of Metrology (VIM)](https://www.bipm.org/en/committees/jc/jcgm/publications), free from the BIPM.
- NIST, [Technical Note 1297](https://www.nist.gov/pml/nist-technical-note-1297), a short guide to evaluating and expressing uncertainty.
- EE Notebook, [Sampling Theory](https://applied-ee.github.io/ee-notebook/docs/audio-signal/sampling-and-conversion/sampling-theory/) and [Quantization Effects](https://applied-ee.github.io/ee-notebook/docs/audio-signal/practical-signal-reality/quantization-effects/).

## References

[^ni-9203]: NI, ["NI-9203 Specifications"](https://www.ni.com/docs/en-US/bundle/ni-9203-specs/page/specs.html), 2022-06-21. Retrieved 2026-11-12.
[^wika-a10]: WIKA, ["Datasheet A-10: Pressure transmitter for general industrial applications"](https://www.transcat.com/media/pdf/Wika_A-10.pdf), 02/2008, US edition, hosted by Transcat. WIKA's current edition is data sheet PE 81.60. Retrieved 2026-11-12.
[^ee-quantization]: EE Notebook, ["Quantization Effects"](https://applied-ee.github.io/ee-notebook/docs/audio-signal/practical-signal-reality/quantization-effects/). Retrieved 2026-11-12.
[^ee-sampling]: EE Notebook, ["Sampling Theory"](https://applied-ee.github.io/ee-notebook/docs/audio-signal/sampling-and-conversion/sampling-theory/). Retrieved 2026-11-12.
[^ni-accuracy]: NI, ["Calculating Absolute Accuracy or System Accuracy"](https://www.ni.com/en/support/documentation/supplemental/18/calculating-absolute-accuracy-or-system-accuracy.html), updated 2026-01-27. Retrieved 2026-11-12.
[^gum]: JCGM, [JCGM 100:2008, Evaluation of measurement data: Guide to the expression of uncertainty in measurement](https://www.bipm.org/en/committees/jc/jcgm/publications), BIPM. Retrieved 2026-11-12.
[^nist-tn1297]: B. N. Taylor and C. E. Kuyatt, [NIST Technical Note 1297: Guidelines for Evaluating and Expressing the Uncertainty of NIST Measurement Results](https://www.nist.gov/pml/nist-technical-note-1297), 1994. Retrieved 2026-11-12.
