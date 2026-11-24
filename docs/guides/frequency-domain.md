# Frequency domain

{.lead}
A spectrum shows how much of a signal is at each frequency, which picks out repeating content such as a shaft's rotation or interference from mains power. What it can show depends on the sample rate, the record length and the window you choose.

## Time domain and frequency domain

A time series shows a signal's value at each moment. Any periodic signal can be built from sine waves of the right frequencies and amplitudes, and for sampled data that decomposition is exact. The frequency domain holds the same information as the time domain, in a different form.[^smith-dft][^ni-fft] A spectrum plots the amplitude of each sine wave against its frequency, so two sine waves added together show up as two peaks.[^ni-fft] A single sample tells you the value at one moment, but a vibration's frequency is in the relationship between many samples.[^smith-filters]

The spectrum of a measured signal can have these features:[^smith-spectral]

- A peak at a fundamental frequency, with {gloss}`harmonics <harmonic>` at whole multiples of it, from a repeating signal that isn't a pure sine wave. A three-bladed propeller turning 4.33 times a second makes a peak at 13 Hz, with harmonics at 26 Hz and 39 Hz.
- A flat floor of white {gloss}`noise`, which has an equal amount of every frequency.
- A peak at the mains frequency, with smaller peaks at its multiples, from electrical interference.
- A roll-off just below half the sample rate, from the anti-aliasing filter. If the spectrum doesn't drop there, suspect {gloss}`aliasing`.

## From samples to a spectrum

The discrete Fourier transform (DFT) turns a record of samples into a {gloss}`spectrum`, and the {gloss}`fast Fourier transform` (FFT) is an efficient way to compute it.[^ni-fft] A record of N samples, taken at a {gloss}`sample rate` fs, gives N/2 + 1 frequency bins, evenly spaced from 0 Hz to fs/2:[^smith-dft][^siemens-dsp]

```text
record length:  T  = N / fs
bin spacing:    Δf = fs / N = 1 / T
highest bin:    fs / 2
```

The sample rate sets the top of the spectrum, and the record length sets how finely it's divided. Bins 1 Hz apart need 1 s of data, and bins 0.1 Hz apart need 10 s. Two tones at 100 Hz and 101 Hz merge into one peak with 1 Hz bins, and separate with 0.5 Hz bins.[^siemens-dsp] Padding a record with zeros adds bins, but doesn't separate peaks that the record is too short to resolve.[^smith-spectral]

Content above fs/2 aliases, as [Sample rate and aliasing](measurement-quality.md#sample-rate-and-aliasing) describes. Siemens notes that in many DAQ systems, the anti-aliasing filter starts cutting at 80% of fs/2, so it recommends sampling at 2.5 times the highest frequency you need.[^siemens-dsp]

## Leakage and windows

The FFT treats a record as one period of a signal that repeats forever. If the record doesn't hold a whole number of cycles, the join between its end and its start is a jump, which spreads the tone's energy into other bins. This is {gloss}`spectral leakage`.[^ni-fft] A running motor's frequencies aren't tied to your record length, so they don't normally fit it.[^siemens-leakage]

A {gloss}`window <window function>` multiplies the record by a curve that tapers to zero at both ends, so the ends meet without a jump.[^ni-fft] Every window trades resolution, the width of a peak, against leakage, the height of its tails.[^smith-spectral] With a Hann window, a tone's leakage typically stays within 1.5 bins on each side, and its amplitude is off by up to 15%. A flat top window reads amplitude to within 0.01%, but spreads each tone over 3.43 bins on each side, so two tones 4 Hz apart, with 1 Hz bins, show as one peak. With no window, which is called a rectangular or uniform window, a tone that doesn't fit the record reads up to 36% low, and leaks across the whole spectrum.[^siemens-windows] Choose the window from the signal:[^ni-fft][^siemens-windows]

| Signal | Window |
| --- | --- |
| Tones, or content you don't know yet | Hann |
| Random vibration | Hann |
| One tone whose amplitude must be exact, such as a calibration tone | Flat top |
| A signal that fits the record, such as an impact that dies away inside it | Rectangular |

### Averaging

A longer record gives finer bins, but the same noise. To reduce the noise, split a long measurement into records, window each one, take its FFT, and average the magnitudes. Random noise falls in proportion to the square root of the number of records.[^smith-spectral] SciPy's `welch` function does this, and by default it overlaps the records by half, which it calls a reasonable trade-off for the Hann window.[^scipy-welch]

## Amplitude spectrum or power spectral density

An amplitude spectrum reads in the signal's own units, such as g, and its square, the autopower, in g². A {gloss}`power spectral density` (PSD) divides each bin of the autopower by the bin spacing, so it reads in g²/Hz. Which to use depends on the signal:[^siemens-psd]

- **Tones**, such as those from an engine, a pump or gears, put their energy in one bin. Their height in an autopower doesn't change with the bin spacing, but their height in a PSD does. Use an amplitude spectrum or an autopower.
- **Broadband random signals** spread their energy across many bins. Halve the bin spacing, and each bin's autopower halves, while the PSD stays the same. Use a PSD, which Siemens reports industry uses to quantify random vibration fatigue.

In SciPy, `welch` returns a PSD with `scaling="density"`, and a power spectrum with `scaling="spectrum"`. The square root of a power spectrum's peak estimates a tone's RMS amplitude.[^scipy-welch] This example measures a tone with a flat top window, and the noise around it as a PSD:

```python
import numpy as np
from scipy import signal

fs = 5000.0  # samples per second
t = np.arange(int(10 * fs)) / fs  # a 10 s measurement
rng = np.random.default_rng(0)
# A 300 Hz tone of 2 g peak, in random noise of 0.5 g RMS
x = 2.0 * np.sin(2 * np.pi * 300 * t) + rng.normal(scale=0.5, size=t.size)

# 2 s records give 0.5 Hz bins; welch averages them, overlapped by half
nperseg = int(2 * fs)
f, psd = signal.welch(x, fs, window="hann", nperseg=nperseg)  # g²/Hz
f, power = signal.welch(x, fs, window="flattop", nperseg=nperseg, scaling="spectrum")  # g²

k = np.argmax(power)
print(f"Bin spacing: {f[1]:.2f} Hz, up to {f[-1]:.0f} Hz")
print(f"Tone: {np.sqrt(power[k]):.2f} g RMS at {f[k]:.1f} Hz")
print(f"Noise floor: {np.mean(psd[f > 1000]):.1e} g²/Hz")
```

It prints 0.50 Hz bins up to 2,500 Hz, a tone of 1.42 g RMS at 300.0 Hz, and a noise floor of 1.0 × 10⁻⁴ g²/Hz. A 2 g peak is 1.41 g RMS.[^siemens-windows] The noise's variance, 0.25 g², spread evenly from 0 to 2,500 Hz, is 1.0 × 10⁻⁴ g²/Hz.[^scipy-welch]

## Signals that change: the spectrogram

One spectrum can't show a frequency that moves, such as a shaft's frequency during a speed {gloss}`sweep`. A {gloss}`spectrogram` splits the measurement into short, possibly overlapping records, computes a spectrum for each, and plots them against time. Each record has to be short enough that the frequency content doesn't change much within it.[^mw-pspectrum][^scipy-spectrogram]

The rule Δf = 1/T applies to each record, so a spectrogram trades time resolution against frequency resolution. Records of 0.02 s give 50 Hz bins, and records of 0.2 s give 5 Hz bins.[^siemens-wavelets] In SciPy, `spectrogram` is a legacy function, and SciPy recommends its `ShortTimeFFT` class for new code.[^scipy-spectrogram]

## Rotating machinery and orders

A rotating machine vibrates at frequencies tied to its speed. An {gloss}`order` counts events per revolution of a reference shaft, where a frequency counts events per second, so the frequency in Hz is the order times the speed in RPM, divided by 60. A shaft at 600 RPM turns 10 times a second, so its first order is at 10 Hz, and its second order at 20 Hz.[^siemens-order]

Unbalance shows up at a shaft's frequency of rotation, its first order.[^bk-balancing] A gear meshes once per tooth, so its mesh frequency is its tooth count times its shaft's frequency, and its mesh order equals its tooth count. Measured data also shows harmonics of the mesh frequency, and can show sidebands on either side of it at multiples of any shaft's frequency.[^lim-singh][^siemens-order] A 62-tooth gear that's out of round, pushed in and out of mesh twice per revolution, adds sidebands at orders 60 and 64.[^siemens-colormaps]

### Run-ups and order tracking

For a run-up, compute spectra at small speed steps and stack them along a speed axis. Drawn in 3D, that's a waterfall. Viewed from above, with amplitude as color, it's a colormap. An order is a straight line through the origin, because its frequency rises with speed. A resonance stays at one frequency, and the vibration rises where an order crosses it.[^siemens-order][^siemens-colormaps]

An FFT over a fixed time smears an order whose frequency moves during the record. If a shaft speeds up from 1,000 RPM to 1,060 RPM within one record, its first order moves 1 Hz and its fourth order 4 Hz. Order tracking takes each spectrum over a fixed number of revolutions instead, so orders don't smear. Spectra over a fixed time still show resonances, which order tracking can cut off.[^siemens-tracking] Order tracking needs the shaft's speed as a reference. Siemens has used engine speed read over a vehicle's CAN bus, 20 times a second and interpolated, in place of a tachometer.[^siemens-obd]

## Filters in the frequency domain

A {gloss}`filter` is described by which frequencies it passes: a low-pass filter passes low frequencies, a high-pass filter high ones, and band-pass and band-reject filters pass or block a band between. The cutoff frequency divides the band a filter passes, its passband, from the transition band, where it starts to block. Analog filters put it where the amplitude falls to 0.707, or −3 dB, while digital filters use 99%, 90%, 70.7% or 50%, so check which one a filter uses.[^smith-filters]

A filter can't be optimized for both domains at once: a good {gloss}`step response` means a poor frequency response, and the reverse. If the information is in the time domain, such as the shape of a step, choose a filter for its step response. If it's in the frequency domain, choose one for its frequency response.[^smith-filters] [Control](control.md#reading-a-step-response) covers reading a step response.

### Mains pickup

Interference from mains power shows up as a peak at 50 Hz or 60 Hz, depending on the local grid, with smaller peaks at its multiples, because the mains waveform isn't a pure sine wave.[^ni-powerline][^smith-spectral] Fix it at the source where you can, with better wiring and shielding, and by breaking {gloss}`ground loops <ground loop>`. See [Kinds of error](measurement-quality.md#kinds-of-error).

In software, a notch filter removes a narrow band. MathWorks removes 60 Hz hum with a Butterworth band-stop filter from 59 Hz to 61 Hz, and checks in a periodogram that the peak has gone.[^mw-hum]

## Worked example: what an e-axle dyno's data can show

Take an e-axle {gloss}`dyno <dynamometer>`: a motor drives the e-axle under test, and a load motor on each side brakes it. This dyno is built to map speed, torque, current, power and temperature, and its manual says it isn't a noise and vibration stand. Its software reads each motor controller about 16 times a second, enough to show changes slower than 8 Hz, as [Sample rate and aliasing](measurement-quality.md#sample-rate-and-aliasing) describes. This example works out which of the driveline's frequencies fall below that, and what an added accelerometer would need.

### 1. Find the frequencies

The DUT speed channel is the DUT motor's speed. The manual gives the e-axle's gear ratio, from the motor to the axle, as 9.095. With both load motors braking equally, each half shaft and load motor turns at the axle's speed. The manual doesn't give the gearbox's tooth counts, so suppose the pinion on the motor shaft has 12 teeth.

At 1,500 RPM, the top of the sweep, the motor shaft turns 1,500 / 60 = 25.00 times a second. The axle turns 25.00 / 9.095 = 2.75 times a second, and the pinion meshes at 12 × 25.00 = 300.00 Hz.

| Shaft or event | Order of the motor shaft | At 1,500 RPM (Hz) | At 3,000 RPM, the speed ceiling (Hz) |
| --- | ---: | ---: | ---: |
| DUT motor shaft | 1.00 | 25.00 | 50.00 |
| Axle, half shafts and load motors | 0.11 | 2.75 | 5.50 |
| Mesh of a 12-tooth pinion on the motor shaft | 12.00 | 300.00 | 600.00 |

### 2. Compare them with the controller data

Only the axle's rotation stays below 8 Hz. The motor shaft is above it everywhere in the sweep: even at 500 RPM, the sweep's lowest speed, it turns 8.33 times a second. So the controller data can't show the motor's first order or any gear mesh, and content at those frequencies in a controller channel would alias.

At 3,000 RPM, the motor's first order is at 50 Hz, the mains frequency in 50 Hz countries. To tell the two apart, change the speed: the order moves with it, and the mains peak doesn't.[^siemens-order][^ni-powerline]

### 3. Choose a sample rate and record length

Suppose you add an accelerometer to the e-axle's housing, to see the mesh and its harmonics up to three times the mesh frequency.[^lim-singh] At 3,000 RPM that's 3 × 600 Hz = 1,800 Hz. With Siemens' factor of 2.5 for the anti-aliasing filter, sample at 4,500 samples per second or more.[^siemens-dsp]

Sidebands sit around the mesh at multiples of each shaft's frequency, so the axle, the slowest shaft, sets the closest spacing: 2.75 Hz at 1,500 RPM.[^lim-singh] A 2 s record gives 0.5 Hz bins. With a Hann window, each tone's leakage typically stays within 1.5 bins, or 0.75 Hz, on each side, so sidebands 2.75 Hz apart stay separate.[^siemens-windows] Each sweep test point holds for 10 s by default, enough for five 2 s records, or nine overlapped by half. Averaging N independent records cuts random noise by a factor of √N, so five records cut it by about 2.2.[^smith-spectral]

The mesh is order 12 of the motor shaft, so each 1 RPM change in motor speed moves it 0.2 Hz. To keep it within one 0.5 Hz bin, the speed has to hold within 2.5 RPM during a record, and the sequence only checks that it's within 50 RPM of its setpoint. Check the speed's spread during the hold, as in the [noise check](measurement-quality.md#checks-you-can-do-on-a-stand), or use order tracking, with the DUT speed channel as the reference.

### 4. Check the manual's working assumption

The manual measures the product of the DUT motor's pole pairs and its gear ratio as 36.38, but can't separate the two from CAN data. It assumes 4 pole pairs and a ratio of 9.095. An accelerometer could settle it, because the motor's unbalance shows at its frequency of rotation.[^bk-balancing] At 6,000 electrical RPM, which the software reports as 1,500 RPM, the motor's first order is at 25.00 Hz if it has 4 pole pairs, and at 33.33 Hz if it has 3. The axle's peak is at 2.75 Hz either way.

## Further reading

- S. W. Smith, [The Scientist and Engineer's Guide to Digital Signal Processing](https://www.dspguide.com/), a free textbook. Chapters 8 to 12 cover the DFT and the FFT, and chapter 14 filters.
- NI, [Understanding FFTs and Windowing](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/understanding-ffts-and-windowing.html).
- Siemens, [Index of Testing Knowledge Articles](https://community.sw.siemens.com/articles/en_US/Knowledge/Index-of-Testing-Knowledge-Articles), short articles on spectra, windows, orders and frequency response functions.

## References

[^smith-dft]: S. W. Smith, ["The Discrete Fourier Transform"](https://www.dspguide.com/ch8.htm), chapter 8 of *The Scientist and Engineer's Guide to Digital Signal Processing*, California Technical Publishing, sections 8.1 to 8.3. Retrieved 2026-11-24.
[^smith-spectral]: S. W. Smith, ["Spectral Analysis of Signals"](https://www.dspguide.com/ch9/1.htm), section 9.1 of *The Scientist and Engineer's Guide to Digital Signal Processing*, California Technical Publishing. Retrieved 2026-11-24.
[^smith-filters]: S. W. Smith, ["Introduction to Digital Filters"](https://www.dspguide.com/ch14.htm), chapter 14 of *The Scientist and Engineer's Guide to Digital Signal Processing*, California Technical Publishing, sections 14.2, 14.4 and 14.5. Retrieved 2026-11-24.
[^ni-fft]: NI, ["Understanding FFTs and Windowing"](https://www.ni.com/en/shop/data-acquisition/measurement-fundamentals/analog-fundamentals/understanding-ffts-and-windowing.html), updated 2026-09-03. Retrieved 2026-11-24.
[^ni-powerline]: NI, ["Eliminating Powerline Noise from DC Measurements in NI Software"](https://knowledge.ni.com/KnowledgeArticleDetails?id=kA00Z000000P9oBSAS&l=en-US), knowledge base, updated 2024-05-13. Retrieved 2026-11-24.
[^scipy-welch]: SciPy, ["scipy.signal.welch"](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.welch.html), SciPy 1.18.0 documentation. Retrieved 2026-11-24.
[^scipy-spectrogram]: SciPy, ["scipy.signal.spectrogram"](https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.spectrogram.html), SciPy 1.18.0 documentation. Retrieved 2026-11-24.
[^mw-pspectrum]: MathWorks, ["pspectrum"](https://www.mathworks.com/help/signal/ref/pspectrum.html), Signal Processing Toolbox documentation, section "Spectrogram Computation". Retrieved 2026-11-24.
[^mw-hum]: MathWorks, ["Remove the 60 Hz Hum from a Signal"](https://www.mathworks.com/help/signal/ug/remove-the-60-hz-hum-from-a-signal.html), Signal Processing Toolbox documentation. Retrieved 2026-11-24.
[^siemens-dsp]: Siemens, ["Digital Signal Processing: Sampling Rates, Bandwidth, Spectral Lines, and more…"](https://community.sw.siemens.com/articles/en_US/Knowledge/digital-signal-processing-sampling-rates-bandwidth-spectral-lines-and-more), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^siemens-leakage]: Siemens, ["Windows and Spectral Leakage"](https://community.sw.siemens.com/articles/en_US/Knowledge/windows-and-spectral-leakage), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^siemens-windows]: Siemens, ["Window Types: Hanning, Flattop, Uniform, Tukey, and Exponential"](https://community.sw.siemens.com/articles/en_US/Knowledge/window-types-hanning-flattop-uniform-tukey-and-exponential), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^siemens-psd]: Siemens, ["What is a Power Spectral Density (PSD)?"](https://community.sw.siemens.com/articles/en_US/Knowledge/what-is-a-power-spectral-density-psd), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^siemens-wavelets]: Siemens, ["Wavelets / Time Frequency Analysis"](https://community.sw.siemens.com/articles/en_US/Knowledge/wavelets-time-frequency-analysis), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^siemens-order]: Siemens, ["What's an Order?"](https://community.sw.siemens.com/articles/en_US/Knowledge/what-s-an-order), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^siemens-colormaps]: Siemens, ["Interpreting Colormaps"](https://community.sw.siemens.com/articles/en_US/Knowledge/Interpreting-Colormaps), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^siemens-tracking]: Siemens, ["Order Tracking: Fixed Sampling versus Synchronous Sampling"](https://community.sw.siemens.com/articles/en_US/Knowledge/order-tracking-fixed-sampling-versus-synchronous-sampling), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^siemens-obd]: Siemens, ["No more tach! Use OBDII to get engine and vehicle speed"](https://community.sw.siemens.com/articles/en_US/Knowledge/no-more-tach-use-obdii-to-get-engine-and-vehicle-speed), Simcenter testing knowledge article. Retrieved 2026-11-24.
[^bk-balancing]: M. MacCamhaoil, Brüel & Kjær, ["Static and Dynamic Balancing of Rigid Rotors"](https://www.bksv.com/doc/BO0276.pdf), application note BO 0276. Retrieved 2026-11-24.
[^lim-singh]: T. C. Lim and R. Singh, ["A Review of Gear Housing Dynamics and Acoustics Literature"](https://ntrs.nasa.gov/api/citations/19900012071/downloads/19900012071.pdf), NASA Contractor Report 185148, October 1989. Retrieved 2026-11-24.