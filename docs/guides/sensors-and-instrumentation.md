# Sensors and instrumentation

{.lead}
A test stand measures with sensors and acts with actuators. Each one is either wired to a DAQ as a bare signal, or built into an instrument that exchanges messages with the computer.

## Two ways in: wired to a DAQ, or through an instrument

A {gloss}`transducer` turns one physical quantity into an electrical signal, and nothing more. It's wired to an input on a {gloss}`data acquisition (DAQ) <data acquisition>` system, which measures the signal. A fluids panel, which runs compressed air through valves, works this way: its pressure transducers, its switches and its valves are each wired to the panel's DAQ.

An {gloss}`instrument` has its own transducers, electronics and actuators built in. The computer exchanges messages with it over a {gloss}`communications bus` instead of measuring its signals. An e-axle {gloss}`dyno <dynamometer>`, where a motor drives the e-axle under test and a load motor on each side brakes it, works this way: its motor controllers and its power supply are instruments.

| | Wired to a DAQ | Instrument |
| --- | --- | --- |
| What crosses the wire | An electrical signal, such as a current or a voltage | Messages, such as "set speed to 1,000 RPM" or "speed is 998 RPM" |
| Where the measuring happens | In the DAQ | Inside the instrument |
| What you configure | The DAQ channel's range, scaling and sample rate | The instrument's settings, through its messages or its front panel |
| Example | A fluids panel | An e-axle dyno |

A flow meter, for example, can come either way: as a bare transducer for a DAQ, or as an instrument with its own display and bus connection.

## DAQ inputs and outputs

A DAQ has four kinds of {gloss}`I/O point`. The fluids panel's DAQ uses a separate NI C Series module for each kind:

| Kind | What connects to it | Example on the fluids panel | Module |
| --- | --- | --- | --- |
| Analog input | A sensor that reports a value in a range | `p_1`, the supply pressure | NI-9203, current input |
| Digital input | A sensor that reports on or off | `sw_1`, the slide's retracted switch | NI-9421, 24 V digital input |
| Analog output | An actuator you set anywhere in a range | `v_2`, the proportional valve | NI-9265, current output |
| Digital output | An actuator you turn on or off | `pump_1`, the compressor's relay | NI-9476, 24 V digital output |

Analog signals come in several forms, and each needs a matching input: a voltage, a 4–20 mA current, a small voltage from a thermocouple, or a resistance bridge that needs power from the DAQ.

## 4–20 mA current loops

A {gloss}`current loop` carries a measurement as a current between 4 and 20 mA. A loop power supply, the transducer and the DAQ's input are wired in series, in one loop.[^ni-current-loop]

Current loops suit test stands and industrial sites for two reasons:[^ni-current-loop]

- The same current flows everywhere in a loop, so the wire's resistance doesn't change the reading the way it changes a voltage over a long cable.
- The range starts at 4 mA, a live zero. A reading of 0 mA means the loop is broken, not that the value is zero.

A two-wire transducer takes its power from the loop itself. The WIKA A-10 pressure transducer, for example, runs from an 8–30 V supply and draws no more than 25 mA, its signal current.[^wika-a10]

To scale a 4–20 mA reading to a value, use the transducer's range:

```text
value = low + (current − 4 mA) ÷ 16 mA × (high − low)
```

For `p_1`, a 0–100 psig transducer, 12 mA is 50 psig, and 17.6 mA is 85 psig.

Outputs can use the same signal. The fluids panel commands its proportional valve, `v_2`, with a 4–20 mA output.

## Sensors by quantity

### Pressure

A pressure transducer reports pressure relative to a reference. {gloss}`Gauge pressure`, in psig, is relative to the surrounding air, so an open line reads 0. Absolute pressure, in psia, is relative to a vacuum. Differential pressure, in psid, is the difference between two ports. Every pressure channel on the fluids panel is in psig.

### Temperature

NI compares three kinds of temperature sensor:[^ni-temperature]

| Sensor | How it works | Range | Trade-offs |
| --- | --- | ---: | --- |
| {gloss}`Thermocouple` | Two different metals, joined at the tip, make a voltage that depends on temperature | About −210 to 1,760 °C | Widest range, but a small, nonlinear signal |
| {gloss}`RTD` | A metal winding, often platinum, whose resistance changes with temperature | About −240 to 650 °C | Best accuracy, stability and linearity |
| {gloss}`Thermistor` | A resistor, typically with a negative temperature coefficient, whose resistance falls as it heats | About −40 to 250 °C | Most sensitive, but narrowest range |

A thermocouple needs cold-junction compensation and amplification.[^ni-temperature] Its voltage depends on the difference in temperature between the tip and the point where its wires connect to the DAQ. The DAQ measures the temperature at that connection, and corrects for it.

The dyno's motor controllers read a temperature sensor in each motor. The control software treats a reading at or below 0 °C as a sensor fault, such as a missing sensor or a broken wire, rather than a real temperature, and trips the stand. Treating an impossible reading as a fault is the same idea as a current loop's live zero.

### Strain, force and torque

A strain gauge is a resistor that stretches with the surface it's bonded to. Strain is the change in length divided by the original length.[^ni-strain]

The change in resistance is tiny, so strain gauges are wired in a Wheatstone bridge: a quarter, half or full bridge, depending on how many of its four arms are active gauges. A bridge needs {gloss}`excitation`, a voltage from the DAQ to power it. A shunt calibration checks the bridge's output by switching in a known resistor.[^ni-strain]

A {gloss}`load cell` measures force with strain gauges in a bridge,[^ni-strain] and a {gloss}`torque sensor` does the same on a twisting shaft. The dyno has no torque sensor. It calculates torque from motor current instead, as shown below.

### Flow

A {gloss}`flow meter` measures how much fluid passes per unit time. On the fluids panel, `fm_1` reports 0 to 100 L/min. The panel's float gauge is a rotameter: a float rides up a tapered tube as flow increases, and you read it by eye, so it has no channel.

## Instruments

The dyno has two kinds of instrument:

- **Motor controllers.** Each one measures its motor's current, speed and temperature, and switches the power that drives the motor. The computer sends each one a speed or current command about 16 times a second over a CAN bus, and reads back its measurements.
- **A power supply.** One box both sources and sinks power on the 48 V bus. It measures its own voltage and current, takes SCPI commands over USB, and holds its setpoint without being resent.

See [Communications](communications.md) for the buses and protocols.

An instrument can also have a {gloss}`front panel` of knobs, buttons and a screen for running it by hand. While a computer controls it, an instrument can lock its front panel in remote mode, so the two don't fight.

LabVIEW calls its programs virtual instruments (VIs) "because their appearance and operation imitate physical instruments, such as oscilloscopes and multimeters", and calls each program's user interface its front panel.[^labview] A LabVIEW front panel is software on a screen, not part of an instrument.

## From signal to channel

Software called a {gloss}`driver` talks to the DAQ or the instrument, and turns each reading into a {gloss}`channel`: a named value in {gloss}`engineering units`, such as `p_1` in psig. For a transducer, that means scaling the raw signal, like the 4–20 mA formula above. For an instrument that reports in engineering units, the driver decodes its messages.

Some channels are calculated from others. These are {gloss}`derived channels <derived channel>`.

### Worked example: the dyno's torque

The dyno has no torque sensor, so its software calculates each motor's torque from its current, using a constant per motor:

| Motor | Torque at maximum current | Constant |
| --- | ---: | ---: |
| DUT | 27.503 Nm at 35 A | 0.786 Nm/A |
| Left load motor | 3.812 Nm at 20 A | 0.191 Nm/A |
| Right load motor | 3.800 Nm at 20 A | 0.190 Nm/A |

A load motor drawing 10 A is producing about 1.9 Nm. That calculation carries two kinds of error:

- Every error in the current measurement passes straight through to torque.
- The constant is a property of the motor, and it doesn't account for friction or losses between the motor and the axle. A torque sensor on the shaft would measure what reaches the axle.

Because torque is current times a constant, each motor's torque and current channels always move together.

## Choosing a sensor

When you choose a sensor, check:

- **Range.** It covers the values you expect, with headroom for overload.
- **Accuracy.** It's good enough once every error is added up. See [Measurement quality](measurement-quality.md).
- **Response time.** It's fast enough for how quickly the value changes.
- **Output.** It matches an input you have, such as 4–20 mA or a bridge.
- **Environment.** Its temperature range, vibration rating and wetted materials suit the stand.
- **Failure behavior.** A failure shows up as an obvious fault, like 0 mA on a current loop, not as a believable value.

## Further reading

- NI, [Measuring Temperature with Thermocouples, RTDs, and Thermistors](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-temperature-with-thermocouples-rtds-and-thermistors.html).
- NI, [Measuring Strain with Strain Gages](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-strain-with-strain-gages.html).
- NI, [4-20 mA Current Loop Fundamentals, System Design, and Setup](https://www.ni.com/white-paper/6940/en/).
- NIST, [ITS-90 Thermocouple Database](https://its90.nist.gov/), the reference tables for thermocouple voltage against temperature.

## References

[^ni-current-loop]: NI, ["4-20 mA Current Loop Fundamentals, System Design, and Setup"](https://www.ni.com/white-paper/6940/en/), updated 2025-02-03. Retrieved 2026-11-12.
[^wika-a10]: WIKA, ["Datasheet A-10: Pressure transmitter for general industrial applications"](https://www.transcat.com/media/pdf/Wika_A-10.pdf), 02/2008, US edition, hosted by Transcat. Retrieved 2026-11-12.
[^ni-temperature]: NI, ["Measuring Temperature with Thermocouples, RTDs, and Thermistors"](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-temperature-with-thermocouples-rtds-and-thermistors.html). Retrieved 2026-11-12.
[^ni-strain]: NI, ["Measuring Strain with Strain Gages"](https://www.ni.com/en/shop/data-acquisition/sensor-fundamentals/measuring-strain-with-strain-gages.html). Retrieved 2026-11-12.
[^labview]: NI, ["Getting Started with LabVIEW"](https://download.ni.com/support/manuals/321527e.pdf), November 2001 edition. Retrieved 2026-11-12.
