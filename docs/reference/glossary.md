% Each entry's first paragraph is a plain-text summary that link tooltips reuse; details and links follow it.

# Glossary

{.lead}
Test and measurement terms, with the other names you may hear for them. The [guides](../guides/index.md) cover each area in depth.

## Accuracy

How close a measurement is to the true value.

Datasheets state accuracy as a number, such as ±0.25% of full scale (FS) or of the reading. In metrology, that number is the maximum permissible error: the largest error the specification allows. Accuracy isn't the same as [precision](#precision): a sensor can give the same wrong reading every time. See [Measurement quality](../guides/measurement-quality.md).

## Actuator

A device that changes something physical when a control system commands it, such as a valve, motor, compressor or pressure regulator.

Also called an output device, or in process control a final control element. With sensors, actuators are also called control points.

## Administrative control

A hazard control that changes how people work, such as a procedure, training, a sign, or a limit on who can enter an area.

Lockout/tagout and a safety briefing are administrative controls. They work only if people follow them, so they back up engineering controls rather than replace them. See [Hierarchy of controls](#hierarchy-of-controls).

## Alarm

A visible or audible signal that tells an operator about an abnormal condition that needs a timely response.

In software operations, the equivalent is an alert or a page. An alarm needs a person to act, where a [trip](#trip) acts on its own. A condition that needs no response is better recorded as an [event](#event). See [Alarms](../guides/alarms.md).

## Alarm fatigue

When people receive so many alarms, most needing no response, that they become desensitized and miss the alarms that matter.

Also called the cry-wolf effect. See [Alarms](../guides/alarms.md#alarm-fatigue).

## Alarm flood

More alarms than an operator can handle. The UK alarm management guide, EEMUA 191, starts a flood at more than 10 new alarms in 10 minutes.

Also called an alarm storm. See [Alarms](../guides/alarms.md#floods).

## Aliasing

A false, slower signal that appears in data when a channel is sampled too slowly for how fast its value changes.

To avoid it, sample at more than twice the fastest frequency in the signal, or remove faster content before sampling with an anti-aliasing [filter](#filter).

In [design of experiments](#design-of-experiments-doe), aliasing means something else: two effects share one estimate. See [Fractional factorials and aliasing](../guides/statistical-analysis.md#fractional-factorials-and-aliasing).

## Analog-to-digital converter (ADC)

The part of a DAQ that turns a sensor's voltage or current into a number.

Its number of bits sets its [resolution](#resolution): a 16-bit ADC divides its range into 65,536 steps.

## Backpressure

A receiver making a sender wait when it can't keep up, instead of losing data.

TCP's flow control does this by telling the sender how much buffer space the receiver has left. See [Network performance](../guides/network-performance.md#backpressure).

## Bandwidth

The number of bits a link can carry each second.

What a system achieves in practice, its throughput, is often lower. See [Network performance](../guides/network-performance.md#bandwidth-and-throughput).

## Batch

A quantity of material made together, in one run of a process with a distinct start and end, and identified by a batch number.

Batch manufacturing is one of three manufacturing types, with [discrete manufacturing](#discrete-manufacturing) and [continuous processes](#continuous-process). Food manufacturing is a typical example. A batch is tested through samples taken from it.

## CAN bus

A [communications bus](#communications-bus) that connects the controllers in a vehicle or machine, so they can exchange commands and measurements over one pair of wires.

Short for controller area network. See [Communications](../guides/communications.md#can).

## Calibration

Comparing a sensor or instrument with a known reference, and recording the difference so its readings can be corrected.

Calibration doesn't change the sensor. Changing it so it reads correctly, such as by zeroing it, is a separate step called adjustment. Calibration is repeated on a schedule, because sensors [drift](#drift). Traceable calibration links a result to a reference, such as a national standard, through an unbroken chain of calibrations, each adding to the uncertainty.

## Channel

A named value that a system reads or writes, such as `inlet_pressure`, together with the series of values it records over time.

Also called a tag in SCADA, PLC and historian software, a signal, a point, or in flight test a parameter or measurand. In Nominal, a tag is something else: see [Tag](#tag).

A channel has a data type, and units if it's a quantity. It can hold a measurement, a command, a calculated value such as power from voltage and current, or a state such as whether a machine is running. Nominal's own definition is in the [platform glossary](https://dev.nominal.io/platform/reference/glossary/#channel).

## Characterization

Testing that maps how a DUT behaves across its operating range, rather than checking that it passes.

Running a motor across a range of speeds and loads is a characterization. An acceptance test, by contrast, checks a DUT against [pass/fail criteria](#passfail-criteria).

## Closed loop

Control that keeps adjusting a command from a measurement of the result, so the result holds at its setpoint.

Also called feedback control. Open-loop control sends a command without checking the result. A motor controller that adjusts its motor's current to hold a commanded speed runs closed loop. See [Control](../guides/control.md).

## Command

A value written to ask a system for something, such as "open the valve 40%" or "spin at 1,000 RPM".

Also called a demand, a request, a write, or an output. The value a command asks for is its [setpoint](#setpoint).

A command doesn't tell you what happened. The [measurement](#measurement) that shows its effect does.

## Communications bus

A data connection that a computer uses to send commands to instruments and read their measurements, as messages rather than as raw electrical signals.

Also called a bus, a fieldbus, or an industrial network. See [Communications](../guides/communications.md).

## Confidence interval

A range, computed from a sample, that contains the true value, such as a population mean, for a stated share of samples, such as 95%.

Also called confidence limits. See [Confidence intervals](../guides/statistical-analysis.md#confidence-intervals).

## Continuous process

A process that runs without breaks between units of product, such as a refinery, or a rolling mill making aluminum sheet.

Its product has no natural identity, so it's identified by a window of time or quantity, or by the coil or reel it's wound onto.
## Control chart

A plot of a measured characteristic against time or sample number, with a center line at the in-control mean and limits three standard deviations either side. A point outside the limits, or a pattern inside them, means the process has changed.

See [Control charts](../guides/statistical-analysis.md#control-charts).

## Control cycle

One pass of the loop that control software runs at a set rate: read the latest commands and measurements, decide, and write the results.

Also called a control loop, a tick, or on a PLC a scan cycle. Its rate is the loop rate, in hertz (Hz).

## Control point

A general name for a sensor or an actuator, or for the I/O point it connects to.

See [Sensor](#sensor), [Actuator](#actuator) and [I/O point](#io-point).

## Control software

Software that reads a system's channels, decides what each actuator should do, and writes commands, in a loop at a set rate.

Also called control logic, control code, or on a PLC a PLC program or ladder logic.

Control software works with channels, not with hardware. [Drivers](#driver) connect channels to hardware.

## Current loop

A way of sending a measurement or command as an electrical current between 4 and 20 mA, where 4 mA is the bottom of the range and 20 mA the top.

Also called a 4–20 mA signal. Because the bottom of the range is 4 mA, a reading of 0 mA means a broken wire rather than a zero value. See [Sensors and instrumentation](../guides/sensors-and-instrumentation.md#420-ma-current-loops).

## Data acquisition (DAQ)

Hardware that connects sensors and actuators to a computer. It reads the sensors' signals and drives the actuators.

Also called a DAQ system, an I/O system, remote I/O, or a data logger if it records on its own. Its modules plug into a chassis. A [PLC](#plc) reads and drives I/O too, and also runs control software on the same hardware.

## Data lake

Low-cost storage that holds raw data as files in open formats, such as Parquet, and applies a schema when the data is read. A lakehouse adds database features over it, such as transactions and versioning.

See [Warehouses, lakes and lakehouses](../guides/engineering-data.md#warehouses-lakes-and-lakehouses).

## Data warehouse

A database that collects data from a business's operational systems for reporting and decision support, written to a schema chosen in advance.

See [Warehouses, lakes and lakehouses](../guides/engineering-data.md#warehouses-lakes-and-lakehouses).

## Deadband

A band within which a change is ignored, so small fluctuations don't cause a reaction.

Also called a dead zone. It's used in several places:

- **Control:** around a setpoint, so the controller doesn't act on every small error.
- **Alarms:** past an [alarm](#alarm)'s limit, so a noisy value must come back by a margin before the alarm clears.
- **Historians:** a [historian](#historian) stores a new value only when it differs from the last stored value by at least the deadband.
- **Metrology:** an instrument's insensitivity: the largest change in the measured quantity, in either direction, that doesn't change its reading.

## Derating

Lowering a device's allowed output, such as its current, when conditions such as temperature make full output unsafe.

A motor controller can derate as it heats up, so its motor may fall short of its command near the temperature limit.

## Derived channel

A channel calculated from other channels rather than measured, such as power calculated from voltage and current.

Also called a calculated channel, a computed channel, or a math channel. In a Nominal workbook, a formula or transform builds one from other channels after the test.

## Design of experiments (DOE)

A method for choosing test points in advance, so that the results separate the effect of each input, and of their interactions, from random variation.

See [Design of experiments](../guides/statistical-analysis.md#design-of-experiments).

## Design testing

Testing a design, once per version, on a few representative units, to show it meets its requirements with margin.

Also called qualification testing, or in hardware product development a design validation test (DVT). Compare [production testing](#production-testing). See [Test design](../guides/test-design.md).

## Device under test (DUT)

The device or system a test stand tests, such as a motor, a valve or a circuit board.

Also called a unit under test (UUT), a test article, equipment under test (EUT), or in materials testing a specimen.

## Discrete manufacturing

Making separate units that each keep their own identity, such as a serial number.

Assembling electronic and mechanical parts, and machining parts, are discrete.
## Downsampling

Reducing data to fewer values, such as the minimum and maximum of each time bucket, so a chart can show a long recording. Downsample for display, and keep the raw data.

See [Downsampling for display](../guides/engineering-data.md#downsampling-for-display).

## Drift

A slow change in a sensor's reading over time, when the quantity it measures hasn't changed.

Zero drift shifts the whole reading. Span drift changes how far the reading moves for a given change in the quantity. [Calibration](#calibration) measures both, so they can be corrected. A change caused by temperature is a separate error, the temperature error.

## Driver

The software that talks to one piece of hardware and turns its signals into channel values, and channel values into its signals.

Also called a device driver, an instrument driver, or a hardware adapter.

## Duty cycle

The fraction of time something is on. For a pulsed signal, such as one that drives a motor, it's the fraction of each cycle the signal is high.

For a device, duty cycle also means the pattern of running and resting it needs to stay within its temperature limits.

## Dwell

Holding a command steady for a set time, so the measurements can settle and be recorded.

Also called a hold. A long dwell, such as one to see how hot a DUT gets, is called a soak.

## Dynamometer (dyno)

A test stand that loads a motor or engine and records its speed and torque.

The motors that apply the load are also called load motors, absorbers or absorption units.

## E-stop

An emergency stop button that removes power from a machine's actuators, and keeps the machine stopped until someone resets it.

Also called an emergency stop, an emergency off (EMO), or a kill switch. An E-stop backs up [guards](#guard) and other controls, and doesn't replace them. It has to stop the machine in [stop category](#stop-category) 0 or 1. See [Safety](../guides/safety.md#emergency-stop).

## Encoder

A sensor on a shaft that reports its position or speed as a stream of pulses.

A tachometer measures speed only.

## Engineering control

A hazard control built into the equipment that keeps people away from a hazard, such as a guard, an interlock, or fail-safe wiring.

Engineering controls work without anyone having to remember them, so the [hierarchy of controls](#hierarchy-of-controls) ranks them above administrative controls and PPE.

## Engineering units

The units a quantity is measured in, such as psig, RPM or °C, as opposed to the raw electrical signal a sensor sends.

Also called EU or scaled units. The raw signal is also called raw counts or the raw value. Converting one to the other is called scaling. [Calibration](#calibration) checks that conversion, so it can be corrected.

## Equipment protection

Protecting a machine, a plant or its product from damage, as opposed to [safety](#safety), which protects people.

Also called asset protection or machine protection. Accelerators call the system that does it a machine protection system (MPS). See [Safety and equipment protection](../guides/safety.md#safety-and-equipment-protection) and [Protecting equipment](../guides/safety.md#protecting-equipment).

## Event

In Nominal, a named point or span of time on one or more assets, such as a test step, a fault or a limit violation. You review events in a workbook.

See Nominal's [Event](https://dev.nominal.io/platform/reference/glossary/#event) entry.

## Excitation

Power that a DAQ supplies to a sensor so it can work, such as a voltage across a strain gauge.

In vibration and acoustics testing, excitation also means the [stimulus](#stimulus-and-response) applied to the DUT.

## Fail-safe

A design where a failure, such as a power loss or a broken wire, leaves the system in a safe state.

Also called de-energize-to-trip, or fail-safe wiring when the wiring does it. A fail-safe valve or circuit needs power to stay in its running state, so losing power moves it to the safe one. For example, a normally open vent valve releases a vessel's pressure when it loses power. See [Safety](../guides/safety.md#fail-safe-design).

## Failure mode and effects analysis (FMEA)

A review that lists each way each part of a system can fail, what happens as a result, and how the failure is detected or prevented.

A [risk assessment](#risk-assessment) starts from hazards. An FMEA starts from failures. Its types include design FMEA (DFMEA) and process FMEA (PFMEA).
## Fast Fourier transform (FFT)

An efficient way to compute the discrete Fourier transform, which turns a record of samples into a [spectrum](#spectrum). A record of N samples taken at a sample rate fs gives frequency bins fs/N apart, up to fs/2.

See [From samples to a spectrum](../guides/frequency-domain.md#from-samples-to-a-spectrum).

## Filter

Processing that removes unwanted parts of a signal, such as a low-pass filter, which removes fast noise and keeps slow changes.

A filter can be hardware, before the ADC, or software, after it. Filtering delays a signal slightly, which matters for [closed-loop](#closed-loop) control. See [Filters in the frequency domain](../guides/frequency-domain.md#filters-in-the-frequency-domain).

## Fixture

Hardware that holds a DUT in place on a test stand and connects it to the stand's sensors, actuators and power.

Also called a jig, or for electronics a test socket.

## Flow meter

A sensor that measures how much fluid passes per unit of time, such as liters per minute.

A rotameter is a flow gauge with no electrical output: a float rides up a tapered tube as flow increases, and you read it by eye.

## Front panel

The physical controls and display on an instrument, such as knobs, buttons and a screen, for operating it by hand.

Also called a local interface. LabVIEW calls each program's user interface a front panel, after the instruments its programs imitate. A LabVIEW front panel is an [HMI](#hmi) on a screen, not part of an instrument. See [Sensors and instrumentation](../guides/sensors-and-instrumentation.md#instruments).

## Gauge pressure

Pressure measured relative to the surrounding air, in units such as psig, so an open tank reads 0.

Absolute pressure, in psia, is measured relative to a vacuum. Differential pressure, in psid, is the difference between two points.

## Gauge R&R

A study that measures the same items repeatedly, to split a measurement's variation into repeatability, over a short time, and reproducibility, such as between operators or from day to day.

Sources define reproducibility differently. [NIST's statistics handbook](https://www.itl.nist.gov/div898/handbook/mpc/section4/mpc44.htm) includes day-to-day changes at one site. The [International Vocabulary of Metrology](https://www.bipm.org/en/doi/10.59161/jcgm200-2012) calls those intermediate precision, and keeps reproducibility for a change of site, operator or instrument. See [Measurement system analysis](../guides/statistical-analysis.md#measurement-system-analysis).

## Genealogy

The record of what went into each product, and what each material and machine went into.

Also called material traceability. A backward trace goes from a product to its materials, and to the equipment that made and tested it. A forward trace goes from a material [lot](#lot) or a machine to every product it touched.
## Golden unit

A unit known to be good, kept as a reference to develop and check production tests.

Also called a golden sample or reference unit. A golden unit can degrade over time, so check it against its own history. See [Test design](../guides/test-design.md#the-golden-unit).

## Ground loop

Unwanted current that flows when two connected devices are grounded at points with slightly different voltages, which adds [noise](#noise) or an offset to measurements.

Electrically isolating the devices breaks the loop.

## Guard

A physical barrier that keeps people away from a hazard, such as moving parts.

Also called guarding, a shield or an enclosure. A guard is an [engineering control](#engineering-control). An interlocked guard also stops the machine when it's opened.

## Hardware-in-the-loop (HiL)

Testing the real controller hardware, with its real inputs and outputs, against a model of the system it controls, running in real time on a test system.

HiL testing can repeat faults and edge cases that would be dangerous or expensive on the real system. Compare [MiL](#model-in-the-loop-mil), [SiL](#software-in-the-loop-sil) and [PiL](#processor-in-the-loop-pil). See [Test design](../guides/test-design.md#testing-before-the-hardware-is-ready-mil-sil-pil-and-hil).

## Harmonic

A frequency at a whole multiple of a fundamental frequency. A repeating signal that isn't a pure sine wave has harmonics, such as mains interference at multiples of 50 Hz or 60 Hz.

See [Time domain and frequency domain](../guides/frequency-domain.md#time-domain-and-frequency-domain).

## Hazard

A source of possible harm, such as stored air pressure, a spinning shaft, or a live electrical circuit.

Risk combines how likely the harm is with how bad it would be. [Hazard controls](#hazard-control) reduce it.

## Hazard control

A measure that reduces the risk from a hazard, such as a guard, a procedure, or safety glasses.

Also called a safety control, or a control. This is a different sense from [control software](#control-software) or [closed-loop](#closed-loop) control. Hazard controls are chosen in the order of the [hierarchy of controls](#hierarchy-of-controls).

## Hierarchy of controls

The order in which to choose hazard controls, from most to least effective: elimination, substitution, engineering controls, administrative controls, and personal protective equipment (PPE).

An ordinary control system's [trips](#trip) get little or no credit as protection for people. See [Safety](../guides/safety.md#the-hierarchy-of-controls).

## Historian

A database that records the time series of a plant's or machine's tags, so operators can look back at them.

Also called a process historian or a data historian. See [Historians](../guides/engineering-data.md#historians).

## HMI

Short for human-machine interface: the screen an operator uses to watch a machine or process and send it commands.

Also called an operator interface, a control app, or a SCADA screen. An instrument's [front panel](#front-panel) is its own physical HMI.

## Human safety

Protecting people from harm. Safety standards call this [safety](#safety).

Also called personnel safety, personnel protection or operator safety. Compare [equipment protection](#equipment-protection).

## Hysteresis

When a reading or a switch point depends on which direction the value is moving.

A pressure switch that turns a compressor off at a high pressure and back on at a lower one has hysteresis on purpose, so the compressor doesn't switch on and off rapidly. In a sensor, hysteresis is an error: its reading on the way up differs from its reading on the way down.

## I/O point

One input or output on a DAQ, wired to one sensor or actuator.

Also called a point, an I/O channel, a physical channel, or a control point. The four kinds are analog input, digital input, analog output and digital output, abbreviated AI, DI, AO and DO. See [Sensors and instrumentation](../guides/sensors-and-instrumentation.md#daq-inputs-and-outputs).

## Instrument

A self-contained device with its own transducers and electronics built in, and any actuators it needs, which a computer controls over a communications bus and a person through its front panel.

Also called an integrated instrument or a smart device. In metrology, any device used for making measurements is a measuring instrument. A motor controller and a programmable power supply are both instruments in the first sense. See [Sensors and instrumentation](../guides/sensors-and-instrumentation.md#instruments).

## Interaction

In [design of experiments](#design-of-experiments-doe), when the effect of one factor on a response depends on the level of another factor.

See [Why one factor at a time misses interactions](../guides/statistical-analysis.md#why-one-factor-at-a-time-misses-interactions).

## Interface control document (ICD)

A document that defines an interface between two parts of a system, so both sides build to the same definition.

An ICD covers the physical, electrical, data and behavioral details of the interface, and who owns each side.
## Interlock

A condition that must be true before a machine allows an action, or that stops the machine if it changes, such as a switch on a guard or a test cell's door.

An interlock that protects people is a [safety function](#safety-function), built and rated as one, such as a switch wired [fail-safe](#fail-safe) or logic in a [safety controller](#safety-controller). An interlock can also protect equipment, such as control software that sends motor commands only while a machine is running. See [Guards and interlocks](../guides/safety.md#guards-and-interlocks).

## ISA-95

The standard for connecting a factory's control systems to its business systems, published internationally as IEC 62264.

It splits a factory's systems into five levels, from the physical process at level 0 to business planning at level 4, and defines common models for equipment, physical assets, materials and tests. The [MES](#manufacturing-execution-system-mes) is level 3.
## Jitter

The variation in latency from one message to the next.

Where values are timestamped when they arrive, jitter shows up as uneven gaps between samples. See [Network performance](../guides/network-performance.md#jitter).

## Latency

The delay between something happening and its effect showing up, such as between a sensor reading and the value appearing on screen.

Also called lag or delay. See [Network performance](../guides/network-performance.md#latency).

## Leak check

A test that fills a vessel with pressure, seals it, and measures how fast the pressure drops.

Also called a leak test or a pressure decay test. The test passes if the pressure drops more slowly than an allowed rate.

## Limit

A value a measurement must stay above or below. A test limit decides pass or fail. An alarm limit causes an [alarm](#alarm), which asks an operator to act. A protection limit causes a [trip](#trip), which protects the equipment.

Also called a threshold or a bound, or in rocket engine testing a redline. Upper and lower limits together make an allowed range.

## Load cell

A sensor that measures force, using strain gauges that stretch slightly under load.

A load cell needs [excitation](#excitation) from the DAQ. A [torque sensor](#torque-sensor) works the same way, on a twisting shaft.

## Lockout/tagout (LOTO)

A procedure that isolates every energy source on a machine, such as electrical power or air pressure, and locks it off before anyone works on it.

Each person working puts their own lock and tag on the isolation point. Lockout/tagout is an [administrative control](#administrative-control) that uses physical locks. Pressing an E-stop isn't lockout, because anyone can release it. See [Safety](../guides/safety.md#lockouttagout).

## Lot

An identified quantity of material of uniform character and quality, such as a [batch](#batch), part of a batch, or the amount a [continuous process](#continuous-process) makes in a set time.

A lot number identifies a lot, and links it to its history. See [Genealogy](#genealogy).

## Machine safety

A term with two opposite meanings. In the machinery standards, "safety of machinery" means protecting people from a machine's hazards. Some facilities use "machine safety" for protecting the machine itself, which this glossary calls [equipment protection](#equipment-protection).

NIF's Machine Safety System (MSS), for example, protects only the machine. See [Safety and equipment protection](../guides/safety.md#safety-and-equipment-protection).

## Manufacturing execution system (MES)

The factory software that tracks each unit through production, including what to test it against and whether it passed.

In a production test, the test executive gets the unit's details from the MES, and sends the result back.

## Measurement

A value a sensor reports about what actually happened, such as a pressure or a speed.

Also called a reading, a sample, feedback, a readback, telemetry, or in process control the process value (PV). In metrology, a measurement is the process of obtaining a value, and the value it gives is the measured value.

## Model-in-the-loop (MiL)

Testing a model of a controller against a model of the system it controls, with nothing physical involved.

The first in-the-loop stage, before [SiL](#software-in-the-loop-sil). See [Test design](../guides/test-design.md#testing-before-the-hardware-is-ready-mil-sil-pil-and-hil).

## Noise

Random variation in a measurement that doesn't come from the quantity being measured.

Signal-to-noise ratio (SNR) compares the size of the real signal with the noise. [Filters](#filter), shielded cables and electrical isolation reduce noise.

## Normally open (NO)

A valve that's open when it has no power, so losing power lets fluid through.

Also called fail-open. A normally closed (NC) valve is the opposite.

For an electrical contact, normally open means the circuit is open, so no current flows, when it isn't actuated. That's the opposite effect from a normally open valve.

## Operating envelope

The range of conditions, such as speed, load, pressure and temperature, that a device or system is designed to run in.

Also called the operating range, or for power electronics the safe operating area (SOA).

## Order (rotating machinery)

A frequency expressed as the number of times something happens per revolution of a reference shaft. The frequency in Hz is the order times the shaft's speed in RPM, divided by 60, and a gear's mesh order equals its tooth count.

See [Rotating machinery and orders](../guides/frequency-domain.md#rotating-machinery-and-orders).

## Pass/fail criteria

The conditions a test result must meet for the DUT to pass, such as a maximum leak rate.

Also called acceptance criteria. They come from the DUT's specification.

## Personal protective equipment (PPE)

Equipment people wear to reduce their exposure to a hazard, such as safety glasses, gloves, or hearing protection.

PPE is the last level of the [hierarchy of controls](#hierarchy-of-controls). Use it with the other controls, not instead of them.

## PID control

A closed-loop control method that sets its output from the error between the setpoint and the measurement: in proportion to the error (P), to its sum over time (I), and to its rate of change (D).

Tuning a PID controller means choosing how much weight each term gets. See [Control](../guides/control.md#pid-control).

## PLC

Short for programmable logic controller: a rugged industrial computer that reads inputs, runs control software in a fixed scan cycle, and drives outputs.

PLCs are programmed in languages such as ladder logic.

## Power spectral density (PSD)

A [spectrum](#spectrum) whose power in each bin is divided by the bin spacing, in units such as g²/Hz, so a broadband random signal reads the same at any resolution. Use it for random signals, and an amplitude spectrum for tones.

See [Amplitude spectrum or power spectral density](../guides/frequency-domain.md#amplitude-spectrum-or-power-spectral-density).

## Precision

How close repeated measurements of the same value are to each other.

Repeatability is precision under unchanged conditions: the same operator, instrument and place, over a short time. A precise sensor can still be inaccurate, if it's off by the same amount every time. Compare [accuracy](#accuracy).

## Pressure regulator

A valve that holds the pressure downstream of it at a set value, as long as the supply pressure is higher.

An electronic pressure regulator takes its setpoint as a command.

## Process capability

How well an in-control process fits inside its specification limits. Cp compares the limits' width with six standard deviations, and Cpk also accounts for a mean that's off center.

See [Process capability](../guides/statistical-analysis.md#process-capability).

## Processor-in-the-loop (PiL)

Testing a controller's code on its target processor against a model of the system it controls, to check it gives the same results as on a desktop computer.

PiL can also measure how long the code takes to run on the target. It comes between [SiL](#software-in-the-loop-sil) and [HiL](#hardware-in-the-loop-hil). See [Test design](../guides/test-design.md#testing-before-the-hardware-is-ready-mil-sil-pil-and-hil).

## Production testing

Testing every unit built, to catch the ones built wrong.

Also called acceptance testing, or end-of-line (EOL) testing on a production line. Compare [design testing](#design-testing). See [Test design](../guides/test-design.md).

## Proof test

A test that pressurizes a part to a set pressure, above what it sees in service, to prove it holds without damage.

Also called a proof pressure test.

## Proportional valve

A valve that opens partway, in proportion to its command, rather than only open or shut.

Compare a [solenoid valve](#solenoid-valve).

## Ramp

Changing a command gradually at a set rate, instead of in one step.

The rate is the ramp rate, such as RPM per second.

## Range

The interval of values a sensor or channel can measure, such as 0 to 100 psig.

Also called the measurement range. Its width, such as 100 psig, is the span. The top of the range is full scale (FS), and a sensor's specifications can be given as a percentage of it, such as ±0.5% FS.

## Redundancy

Using two or more independent parts for one function, so that one failure doesn't defeat it.

Safety circuits use redundancy, such as an E-stop with two separate contacts, each able to stop the machine. A single point of failure is a part whose failure alone defeats a function.

## Regen

Short for regenerative braking: a motor braking by working as a generator, which turns the energy it absorbs into electrical power.

## Requirement

A statement of what a system has to do or be, written with "shall", that can be checked.

A good requirement says one thing, states what is needed rather than how, and can be verified by test, analysis, demonstration or inspection.
## Resolution

The smallest change a measurement can show.

For a DAQ, the [ADC](#analog-to-digital-converter-adc)'s number of bits sets the smallest step it can show, but noise can hide changes smaller than that. Resolution isn't [accuracy](#accuracy): a reading can show many digits and still be wrong.

## Risk assessment

A structured review that finds a machine's or process's hazards, estimates the risk of each, and decides which controls bring the risk down to an acceptable level.

ISO 12100 describes how to do one for machines. An [FMEA](#failure-mode-and-effects-analysis-fmea) is a related review that starts from how each part can fail.

## RTD

Short for resistance temperature detector: a temperature sensor whose resistance rises with temperature, such as a Pt100.

It's more accurate and stable than a [thermocouple](#thermocouple), over a smaller temperature range.

## Run

In general, one execution of a test. In Nominal, a run is a named period of time on one or more assets, such as a test, a flight or a race session.

See Nominal's [Run](https://dev.nominal.io/platform/reference/glossary/#run) entry.

## Safety

Freedom from unacceptable risk of harm to people. Some standards also count harm that reaches people through damage to property or the environment.

Protecting equipment for its own sake is [equipment protection](#equipment-protection). See [Safety and equipment protection](../guides/safety.md#safety-and-equipment-protection), and [Which control covers which failure](../guides/safety.md#which-control-covers-which-failure).

## Safety controller

Hardware designed and certified to carry out safety functions, such as stopping a machine when an E-stop is pressed or a guard opens.

Also called a safety relay, or a safety PLC if it's programmable. It's built and rated to standards such as ISO 13849-1 or IEC 62061, so it can carry [safety functions](#safety-function). See [Safety](../guides/safety.md#safety-controllers).

## Safety function

A function whose failure can immediately increase the risk to people, such as stopping a machine when a guard opens.

ISO 13849-1 rates how reliably it works as a performance level (PL), and IEC 62061 and IEC 61511 as a safety integrity level (SIL). In process plants, a [safety instrumented system](#safety-instrumented-system-sis) carries out safety instrumented functions (SIFs). See [Safety functions and the control system](../guides/safety.md#safety-functions-and-the-control-system).

## Safety instrumented system (SIS)

In process plants, the system that carries out safety instrumented functions, from sensors to final elements such as valves. It's kept separate from the basic process control system (BPCS) that runs the process.

IEC 61511 sets its requirements. Some labs use SIS for a safety interlock system instead, such as NIF's, which protects people. See [Safety functions and the control system](../guides/safety.md#safety-functions-and-the-control-system).

## Sample rate

How often a channel's value is read, in samples per second or hertz (Hz).

Also called a sampling rate, a scan rate, or an acquisition rate. Sampling too slowly causes [aliasing](#aliasing).

## SCADA

Short for supervisory control and data acquisition: software that monitors and controls equipment spread across a site from one place.

It shows [HMI](#hmi) screens, records data in a [historian](#historian), and names each value a [tag](#tag).

## Sensor

A device that measures something physical, such as pressure or flow, and turns it into an electrical signal.

Also called a probe. With actuators, sensors are also called control points.

A sensor is a kind of [transducer](#transducer). It can be wired to a DAQ on its own, or built into an [instrument](#instrument) with its own electronics and bus connection. A gauge, such as a dial pressure gauge, shows a measurement on the device itself and doesn't produce a channel. In metrology, the sensor is only the part the quantity acts on directly, such as the Bourdon tube inside a dial pressure gauge, whatever its output.

## Sequence

A test's steps in order, from start up to shut down, each with what to do and what you should see.

Also called a procedure, a test procedure, a test script, or in process industries a recipe.

## Setpoint

The value a command asks for, such as a speed of 1,000 RPM.

Also called a target, a demand, a reference, or SP.

## Shelving

Hiding an alarm from operators for a limited time, such as while someone works on its cause.

Shelving hides an alarm without fixing it, so alarm software such as Ignition limits how long an alarm stays shelved. See [Alarms](../guides/alarms.md#fixing-nuisance-alarms).

## Software-in-the-loop (SiL)

Testing a controller's code on a desktop computer against a model of the system it controls, with no real hardware.

SiL checks that the code behaves like the controller's model. It comes between [MiL](#model-in-the-loop-mil) and [PiL](#processor-in-the-loop-pil). See [Test design](../guides/test-design.md#testing-before-the-hardware-is-ready-mil-sil-pil-and-hil).

## Solenoid valve

An on/off valve that an electromagnet opens or closes when it's powered.

Compare a [proportional valve](#proportional-valve).

## Spectral leakage

Energy from one frequency spreading into other bins of a [spectrum](#spectrum), because the record doesn't hold a whole number of its cycles. A [window](#window-function) reduces it.

See [Leakage and windows](../guides/frequency-domain.md#leakage-and-windows).

## Spectrogram

A plot of how a signal's [spectrum](#spectrum) changes over time, made from the spectra of short, overlapping records. For rotating machinery, the same plot against speed is called a colormap.

See [Signals that change: the spectrogram](../guides/frequency-domain.md#signals-that-change-the-spectrogram).

## Spectrum

A plot of how much of a signal is at each frequency, computed from a time series with an [FFT](#fast-fourier-transform-fft).

See [Frequency domain](../guides/frequency-domain.md).

## Standard deviation

A measure of how far a set of values spreads around its mean. For a sample, it's the square root of the sum of the squared differences from the mean, divided by one less than the number of values.

See [Describing a set of results](../guides/statistical-analysis.md#describing-a-set-of-results).

## Steady state

When a system's measurements have stopped changing after a change in its commands.

The changing period before it is the transient. A [dwell](#dwell) gives a measurement time to reach steady state before it's recorded.

## Step response

How a measurement responds when its command changes suddenly, in one step.

It's described by the rise time, the overshoot, and the settling time. See [Control](../guides/control.md#reading-a-step-response).

## Stimulus and response

A stimulus is what a test applies to the DUT, such as a speed, a load or a pressure. The response is how the DUT reacts, as its sensors measure it.

Also called input and output, or in vibration and acoustics testing excitation and response.

## Stop category

How a machine stops, as defined in IEC 60204-1. Category 0 removes power at once, category 1 makes a controlled stop and then removes power, and category 2 makes a controlled stop and leaves power on.

An E-stop has to be category 0 or 1.

## Sweep

Running a test across a range of one input, such as speed, in steps or continuously, and recording the response at each point.

## Tag

In Nominal, a key-value pair on data points, such as `motor_id: 1`, that lets you filter part of a dataset. In SCADA, PLC and historian software, a tag is what Nominal calls a channel.

See [Channel](#channel), and Nominal's [Tag](https://dev.nominal.io/platform/reference/glossary/#tag) entry.

## Test executive

Software that runs a test's steps in order, records each step's result, and decides whether the unit passed.

Also called a test sequencer. NI TestStand is one. Nominal's [TestStand steps](https://dev.nominal.io/ni-teststand/) can create runs and events from a TestStand sequence.

## Test plan

A document that says what to test on a DUT, how, and the [pass/fail criteria](#passfail-criteria).

A test plan is carried out as one or more [sequences](#sequence). Each scenario in it is a test case.

## Test stand

The equipment that runs tests on a device under test: its sensors, actuators, DAQ, power, and the software that drives them.

Also called a test rig, a rig, a test bench, a tester, a test station, or automatic test equipment (ATE). A test cell is a room or enclosure built around one.

## Thermistor

A temperature sensor made of a resistor whose resistance changes strongly with temperature.

An NTC thermistor's resistance falls as it heats up.

## Thermocouple

A temperature sensor made of two different metals joined at the tip, which produces a small voltage that depends on temperature.

It covers a wide range of temperatures. To read it, the DAQ also measures the temperature where the wires connect, which is called cold-junction compensation.

## Time-series database

A database built to store and query values by time. Compression that uses the regular gaps between timestamps, and the small changes between values, can store each value in far fewer bytes than its raw size.

See [Time-series databases](../guides/engineering-data.md#time-series-databases).

## Tolerance

How far a value may be from its target and still be acceptable, such as 100 mm ± 0.1 mm.

A tolerance sets the [limits](#limit) of a pass/fail check.

## Torque sensor

A sensor that measures the twisting force on a shaft, with strain gauges on the shaft or in a flange.

Also called a torque transducer or a torque cell.

## Traceability

The links between each requirement, the requirements it came from and was split into, and the tests that check it.

Bidirectional traceability means you can follow those links both up and down. In manufacturing, traceability also means following a product back to its materials, or a material forward to its products: see [Genealogy](#genealogy).

In metrology, traceability, or metrological traceability, means a result can be related to a reference, such as a national standard, through an unbroken chain of calibrations, each adding to the uncertainty. See [Calibration](#calibration).

## Transducer

A device that converts energy from one form to another, such as a pressure into an electrical signal, or an electrical signal into motion.

A [sensor](#sensor), such as a pressure transducer, is a transducer that measures. An [actuator](#actuator) is one that acts. A transmitter is a transducer with built-in electronics that output a standard signal, such as a 4–20 mA [current loop](#current-loop). In metrology, a measuring transducer is any device whose output has a specified relation to its input, such as a thermocouple.

## Trip

An automatic stop that the control software makes when a measurement leaves its allowed range.

Also called an automatic abort or an interlock trip. An abort that an operator starts isn't a trip. Nor is an [alarm](#alarm), which asks an operator to act rather than acting itself.

A trip in an ordinary control system is [equipment protection](#equipment-protection), and gets little or no credit as protection for people. A trip that protects people is a [safety function](#safety-function), carried out by a rated system such as a [safety controller](#safety-controller).

## Uncertainty

How far the true value may be from a measurement, given as a range and a probability, such as ±0.7 psig at about 95%.

Also called measurement uncertainty. An uncertainty budget lists each source of uncertainty, and how they're calculated and combined. An error budget does the same with each source's error limits. See [Measurement quality](../guides/measurement-quality.md#uncertainty).

## Unit under test (UUT)

Another name for a device under test (DUT): the device or system a test stand tests.

See [Device under test (DUT)](#device-under-test-dut).

## V-model

A layout of a project as a V: requirements split into designs down the left side, and parts built, integrated and tested up the right, each level against its matching specification.

Also called the Vee. See [Test design](../guides/test-design.md#the-v-model).

## Watchdog

A timer that puts a device in a safe state if the software controlling it stops checking in.

For example, a motor controller can stop driving its motor if no command arrives within a set time, so a crashed program can't leave the motor running.

## Window function

A curve that multiplies a record before an [FFT](#fast-fourier-transform-fft), tapering to zero at both ends to reduce [spectral leakage](#spectral-leakage). A Hann window suits most signals, and a flat top window reads a tone's amplitude accurately.

Also called a window. See [Leakage and windows](../guides/frequency-domain.md#leakage-and-windows).

## Workbook

Where you analyze time-series data in Nominal, in tabs and panels, after a test or live.

Nominal's own definition is in the [platform glossary](https://dev.nominal.io/platform/reference/glossary/#workbook).

## Zero offset

A sensor's reading when the quantity it measures is zero.

Also called zero error. It's a kind of bias: a systematic error, in this case the one at zero. Zeroing subtracts the zero offset, and on a scale it's called taring. In Nominal, an [offset](https://dev.nominal.io/platform/reference/glossary/#offset) is a time shift, not this.
