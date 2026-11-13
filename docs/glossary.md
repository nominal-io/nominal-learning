% Each entry's first paragraph is a plain-text summary that link tooltips reuse; details and links follow it.

# Glossary

{.lead}
Test and measurement terms used on the test stands, with the other names you may hear for them.

## Accuracy

How close a measurement is to the true value.

A sensor's accuracy is stated as a percentage of its full scale or of its reading, such as ±0.25% FS. Accuracy isn't the same as [precision](#precision): a sensor can give the same wrong reading every time.

## Actuator

A device that changes something physical when the stand commands it, such as a valve, motor, compressor or pressure regulator.

Also called an output device, or in process control a final control element. With sensors, actuators are also called control points.

On the fluids panel, `v_2` and `pump_1` are actuators. On the dyno, the DUT and the two load motors are.

## Administrative control

A hazard control that changes how people work, such as a procedure, training, a sign, or a limit on who can enter an area.

Lockout/tagout and the workshop's safety briefing are administrative controls. They work only if people follow them, so they back up engineering controls rather than replace them. See [Hierarchy of controls](#hierarchy-of-controls).

## Aliasing

A false, slower signal that appears in data when a channel is sampled too slowly for how fast its value changes.

To avoid it, sample at more than twice the fastest frequency in the signal, called the Nyquist rate, or remove faster content before sampling with an anti-aliasing [filter](#filter).

## Analog-to-digital converter (ADC)

The part of a DAQ that turns a sensor's voltage or current into a number.

Its number of bits sets its [resolution](#resolution): a 16-bit ADC divides its range into 65,536 steps.

## CAN bus

A [communications bus](#communications-bus) that connects the controllers in a vehicle or machine, so they can exchange commands and measurements over one pair of wires.

Short for controller area network. The dyno's three motor controllers share one CAN bus. Other industrial networks, such as Modbus and EtherCAT, do the same kind of job.

## Calibration

Comparing a sensor or instrument with a known reference, then correcting or recording the difference.

Calibration is repeated on a schedule, because sensors [drift](#drift). Traceability means each reference was itself calibrated, in a chain back to a national standard.

## Channel

A named value that a stand reads or writes, such as `p_1`, together with the series of values it records over time.

Also called a tag in SCADA, PLC and historian software, a signal, a point, or in flight test a parameter or measurand. In Nominal, a tag is something else: see [Tag](#tag).

A channel has a data type, and units if it's a quantity. It can hold a measurement, a command, a calculated value such as the dyno's torque, or a state such as whether the stand is running. Nominal's own definition is in the [platform glossary](https://dev.nominal.io/platform/reference/glossary/#channel).

## Characterization

Testing that maps how a DUT behaves across its operating range, rather than checking that it passes.

The dyno's sequence is a characterization: it runs a range of speeds at three loads. An acceptance test, by contrast, checks a DUT against [pass/fail criteria](#passfail-criteria).

## Closed loop

Control that keeps adjusting a command from a measurement of the result, so the result holds at its setpoint.

Also called feedback control. Open-loop control sends a command without checking the result. The dyno's DUT runs closed loop: its motor controller adjusts the current to hold the commanded speed.

## Command

A value written to ask a stand for something, such as "open the valve 40%" or "spin at 1,000 RPM".

Also called a demand, a request, a write, or an output. The value a command asks for is its [setpoint](#setpoint).

A command doesn't tell you what happened. The [measurement](#measurement) that shows its effect does.

## Communications bus

A data connection that a computer uses to send commands to instruments and read their measurements, as messages rather than as raw electrical signals.

Also called a bus, a fieldbus, or an industrial network. Examples include [CAN bus](#can-bus), Modbus, EtherCAT, Ethernet, RS-232 serial and GPIB, and point-to-point links such as USB. The messages follow a protocol, such as SCPI for lab instruments.

On the dyno, the motor controllers share a CAN bus, and the power supply connects over USB and takes SCPI commands.

## Control cycle

One pass of the loop that control software runs at a set rate: read the latest commands and measurements, decide, and write the results.

Also called a control loop, a tick, or on a PLC a scan cycle. Its rate is the loop rate, in hertz (Hz).

## Control point

A general name for a sensor or an actuator on a stand, or for the I/O point it connects to.

See [Sensor](#sensor), [Actuator](#actuator) and [I/O point](#io-point).

## Control software

Software that reads a stand's channels, decides what each actuator should do, and writes commands, in a loop at a set rate.

Also called control logic, control code, or on a PLC a PLC program or ladder logic.

Control software works with channels, not with hardware. [Drivers](#driver) connect channels to hardware. On the dyno, the control software also limits each command to a safe range, converts torque commands to current, and trips the stand when a measurement leaves its allowed range.

## Current loop

A way of sending a measurement or command as an electrical current between 4 and 20 mA, where 4 mA is the bottom of the range and 20 mA the top.

Also called a 4–20 mA signal. Because the bottom of the range is 4 mA, a reading of 0 mA means a broken wire rather than a zero value.

On the fluids panel, `p_1` reports 0 to 100 psig as 4 to 20 mA, and `v_2` takes its command the same way.

## Data acquisition (DAQ)

Hardware that connects sensors and actuators to a computer. It reads the sensors' signals and drives the actuators.

Also called a DAQ system, an I/O system, remote I/O, or a data logger if it records on its own. Its modules plug into a chassis. A [PLC](#plc) reads and drives I/O too, and also runs control software on the same hardware.

The fluids panel has a DAQ. On the dyno, the motor controllers and the power supply do the same job.

## Deadband

A band around a setpoint inside which a difference is ignored, so small fluctuations don't cause a reaction.

Also called a dead zone.

## Derating

Lowering a device's allowed output, such as its current, when conditions such as temperature make full output unsafe.

A motor controller can derate as it heats up, so its motor may fall short of its command near the temperature limit.

## Derived channel

A channel calculated from other channels rather than measured, such as the dyno's torque, which is calculated from each motor's current.

Also called a calculated channel, a computed channel, or a math channel.

A stand's control software can calculate one while it runs. In a Nominal workbook, a formula or transform builds one from other channels after the test.

## Device under test (DUT)

The device or system a test stand tests, such as the dyno's electric axle.

Also called a unit under test (UUT), a test article, equipment under test (EUT), or in materials testing a specimen.

## Drift

A slow change in a sensor's reading, over time or with temperature, when the quantity it measures hasn't changed.

Zero drift shifts the whole reading. Span drift changes how far the reading moves for a given change in the quantity. [Calibration](#calibration) corrects both.

## Driver

The software that talks to one piece of hardware and turns its signals into channel values, and channel values into its signals.

Also called a device driver, an instrument driver, or a hardware adapter.

## Duty cycle

The fraction of time something is on. For a pulsed signal, such as one that drives a motor, it's the fraction of each cycle the signal is high.

For a device, duty cycle also means the pattern of running and resting it needs to stay within its temperature limits.

## Dwell

Holding a command steady for a set time, so the measurements can settle and be recorded.

Also called a hold. A long dwell, such as one to see how hot a DUT gets, is called a soak. The dyno's sequence dwells at each sweep step, for the time in **Dwell per Step**.

## Dynamometer (dyno)

A test stand that loads a motor or engine and records its speed and torque.

The motors that apply the load are also called load motors, absorbers or absorption units. The workshop's e-axle dyno has a load motor on each side of the axle.

## E-stop

An emergency stop button that puts a stand in a safe state through hardware alone, without any software.

Also called an emergency stop, an emergency off (EMO), or a kill switch.

An E-stop is a [human safety](#human-safety) control. Its circuit is wired [fail-safe](#fail-safe): pressing the button opens the circuit, so a broken wire stops the stand too. On the fluids panel, the E-stop opens the vent valve and releases the pressure.

An E-stop is for emergencies. It backs up [guards](#guard) and other controls, and doesn't replace them. Pressing it isn't [lockout/tagout](#lockouttagout-loto), because anyone can release it.

## Encoder

A sensor on a shaft that reports its position or speed as a stream of pulses.

A tachometer measures speed only. On the dyno, each motor controller reports its own motor's speed.

## Engineering control

A hazard control built into the equipment that keeps people away from a hazard, such as a guard, an interlock, or fail-safe wiring.

Engineering controls work without anyone having to remember them, so the [hierarchy of controls](#hierarchy-of-controls) ranks them above administrative controls and PPE. On these stands, the E-stop, the fail-safe vent valve and the dyno's guard are engineering controls.

## Engineering units

The units a quantity is measured in, such as psig, RPM or °C, as opposed to the raw electrical signal a sensor sends.

Also called EU or scaled units. The raw signal is also called raw counts or the raw value. Converting one to the other is called scaling. [Calibration](#calibration) checks and corrects that conversion.

## Excitation

Power that a DAQ supplies to a sensor so it can work, such as a voltage across a strain gauge.

In vibration and acoustics testing, excitation also means the [stimulus](#stimulus-and-response) applied to the DUT.

## Fail-safe

A design where a failure, such as a power loss or a broken wire, leaves the system in a state that is safe to the human using it.

Also called de-energize-to-trip, or fail-safe wiring when the wiring does it. A fail-safe valve or circuit needs power to stay in its running state, so losing power moves it to the safe one.

On the fluids panel, the vent valve is normally open: it needs power to stay closed, so losing power or pressing the E-stop releases the pressure. Fail-safe wiring is how these stands keep [human safety](#human-safety) without software.

## Failure mode and effects analysis (FMEA)

A review that lists each way each part of a system can fail, what happens as a result, and how the failure is detected or prevented.

A [risk assessment](#risk-assessment) starts from hazards. An FMEA starts from failures.

FMEAs are named for what they analyze:

- Design FMEA (DFMEA): how a product's design can fail.
- Process FMEA (PFMEA): how a manufacturing or assembly process can fail, and produce a bad part.
- System FMEA: how subsystems and the interfaces between them can fail.
- FMEA-MSR, for monitoring and system response: how well a product's diagnostics detect a failure in use, and put it in a safe state. The automotive AIAG-VDA FMEA handbook defines it, with DFMEA and PFMEA.
- FMECA, for failure mode, effects and criticality analysis: an FMEA that also ranks each failure mode by its severity and likelihood. It comes from the US military standard MIL-STD-1629A.

An FMEA scores each failure for severity, occurrence and detection. Their product, from 1 to 1,000, is the risk priority number (RPN). The AIAG-VDA handbook replaces the RPN with an action priority (AP) of high, medium or low.

## Filter

Processing that removes unwanted parts of a signal, such as a low-pass filter, which removes fast noise and keeps slow changes.

A filter can be hardware, before the ADC, or software, after it. Filtering delays a signal slightly, which matters for [closed-loop](#closed-loop) control.

## Fixture

Hardware that holds a DUT in place on a test stand and connects it to the stand's sensors, actuators and power.

Also called a jig, or for electronics a test socket.

## Flow meter

A sensor that measures how much fluid passes per unit of time, such as liters per minute.

On the fluids panel, `fm_1` is a flow meter. The panel's float gauge is a rotameter: a float rides up a tapered tube as flow increases, and you read it by eye.

A flow meter can be a bare [transducer](#transducer) wired to a DAQ, or an [instrument](#instrument) with its own display and bus connection.

## Front panel

The physical controls and display on an instrument, such as knobs, buttons and a screen, for operating it by hand.

Also called a local interface. While a computer controls an instrument over a [communications bus](#communications-bus), the instrument can lock its front panel, which is called remote mode. The dyno's power supply has a front panel.

LabVIEW calls the user interface of each of its programs a front panel, after the instruments its programs imitate, which is why those programs are called virtual instruments (VIs). A LabVIEW front panel is software on a screen: an [HMI](#hmi), not part of an instrument.

## Gauge pressure

Pressure measured relative to the surrounding air, in units such as psig, so an open tank reads 0.

Absolute pressure, in psia, is measured relative to a vacuum, so the air around you reads about 14.7 psia at sea level. Differential pressure, in psid, is the difference between two points. The fluids panel's channels are in psig.

## Ground loop

Unwanted current that flows when two connected devices are grounded at points with slightly different voltages, which adds [noise](#noise) or an offset to measurements.

Electrically isolating the devices breaks the loop.

## Guard

A physical barrier that keeps people away from a hazard, such as moving parts.

Also called guarding, a shield or an enclosure. A guard is an [engineering control](#engineering-control). An interlocked guard also stops the machine when it's opened. The dyno has a guard around its moving parts.

## Hazard

A source of possible harm, such as stored air pressure, a spinning shaft, or a live electrical circuit.

Risk combines how likely the harm is with how bad it would be. [Hazard controls](#hazard-control) reduce it.

## Hazard control

A measure that reduces the risk from a hazard, such as a guard, a procedure, or safety glasses.

Also called a safety control, or a control. This is a different sense from [control software](#control-software) or [closed-loop](#closed-loop) control. Hazard controls are chosen in the order of the [hierarchy of controls](#hierarchy-of-controls).

## Hierarchy of controls

The order in which to choose hazard controls, from most to least effective: elimination, substitution, engineering controls, administrative controls, and personal protective equipment (PPE).

1. Elimination removes the hazard, such as by running a check with the stand unpressurized.
2. Substitution replaces the hazard with a smaller one, such as a lower pressure.
3. [Engineering controls](#engineering-control) keep people away from the hazard, such as guards, interlocks, and fail-safe wiring.
4. [Administrative controls](#administrative-control) change how people work, such as procedures, training, and lockout/tagout.
5. [PPE](#personal-protective-equipment-ppe) is worn to reduce exposure, such as safety glasses.

Where one control isn't enough, combine them. Software trips aren't on the list, because they protect equipment, not people. The hierarchy comes from [NIOSH](https://www.cdc.gov/niosh/hierarchy-of-controls/about/index.html), and [OSHA](https://www.osha.gov/safety-management/hazard-prevention) recommends it.

## Historian

A database that records the time series of a plant's or stand's tags, so operators can look back at them.

Also called a process historian or a data historian.

## HMI

Short for human-machine interface: the screen an operator uses to watch a stand's channels and send commands.

Also called an operator interface, a control app, or a SCADA screen. In the workshop, the dyno's control app is its HMI.

An instrument's [front panel](#front-panel) is its own physical HMI. LabVIEW calls its software HMIs front panels too.

## Human safety

Protecting people from a stand's hazards, such as stored pressure, moving parts and electrical energy. On these stands, hardware keeps human safety: fail-safe wiring, the E-stop and guards, which all work without software.

Also called personnel safety or operator safety. Compare [machine safety](#machine-safety).

Ordinary control software can't keep people safe, because it can stall or crash. Software can be part of human safety only on a [safety controller](#safety-controller) designed and certified for it. Procedures, training and PPE add to the hardware: see [Hierarchy of controls](#hierarchy-of-controls).

## Hysteresis

When a reading or a switch point depends on which direction the value is moving.

A pressure switch that turns a compressor off at a high pressure and back on at a lower one has hysteresis on purpose, so the compressor doesn't switch on and off rapidly. In a sensor, hysteresis is an error: its reading on the way up differs from its reading on the way down.

## I/O point

One input or output on a DAQ, wired to one sensor or actuator.

Also called a point, an I/O channel, a physical channel, or a control point.

There are four kinds:

- Analog input: a sensor that reports a value in a range, such as a pressure.
- Digital input: a sensor that reports on or off, such as a switch.
- Analog output: an actuator you set anywhere in a range, such as a proportional valve.
- Digital output: an actuator you turn on or off, such as a relay that switches a compressor.

These are abbreviated AI, DI, AO and DO.

## Instrument

A self-contained device with its own transducers and electronics built in, and any actuators it needs, which a computer controls over a communications bus and a person through its front panel.

Also called an integrated instrument or a smart device. More loosely, any measuring device is called an instrument.

An instrument does its own measuring and driving, so the computer exchanges messages with it instead of wiring each signal to a DAQ. On the dyno, the motor controllers and the power supply are instruments. A mass flow controller is another example: it has a flow sensor and a valve built in.

## Interlock

A condition that must be true before a stand allows an action, or that stops the stand if it changes, such as a switch on a guard or a test cell's door.

A hardware interlock, wired [fail-safe](#fail-safe), is an [engineering control](#engineering-control) for [human safety](#human-safety). A software interlock protects only the machine. For example, the dyno's software won't send motor commands unless the stand is running.

## Latency

The delay between something happening and its effect showing up, such as between a sensor reading and the value appearing on screen.

Also called lag or delay.

## Leak check

A test that fills a vessel with pressure, seals it, and measures how fast the pressure drops.

Also called a leak test or a pressure decay test. The test passes if the pressure drops more slowly than an allowed rate.

## Limit

A value a measurement must stay above or below. A test limit decides pass or fail. A protection limit causes a [trip](#trip), which protects the equipment.

Also called a threshold or a bound, or in rocket engine testing a redline. Upper and lower limits together make an allowed range.

## Load cell

A sensor that measures force, using strain gauges that stretch slightly under load.

A load cell needs [excitation](#excitation) from the DAQ. A [torque sensor](#torque-sensor) works the same way, on a twisting shaft.

## Lockout/tagout (LOTO)

A procedure that isolates every energy source on a machine, such as electrical power or air pressure, and locks it off before anyone works on it.

Each person working puts their own lock and tag on the isolation point, and only they remove it. That protects them from the machine starting, or releasing stored energy, while they work.

Lockout/tagout is an [administrative control](#administrative-control) that uses physical locks, and it's part of [human safety](#human-safety). Pressing an E-stop isn't lockout, because anyone can release it.

## Machine safety

Protecting a stand and its DUT from damage. On these stands, the control software keeps machine safety, by limiting commands to a safe range and tripping when a measurement leaves its allowed range.

Also called machine protection or equipment protection. Compare [human safety](#human-safety).

Safety standards, such as ISO 12100, use "safety of machinery" for something else: protecting people from a machine's hazards, which this glossary calls human safety.

## Measurement

A value a sensor reports about what actually happened, such as a pressure or a speed.

Also called a reading, a sample, feedback, a readback, telemetry, or in process control the process value (PV).

## Noise

Random variation in a measurement that doesn't come from the quantity being measured.

Signal-to-noise ratio (SNR) compares the size of the real signal with the noise. [Filters](#filter), shielded cables and electrical isolation reduce noise.

## Normally open (NO)

A valve that's open when it has no power, so losing power lets fluid through.

Also called fail-open. A normally closed (NC) valve is the opposite.

For an electrical contact, normally open means the circuit is open, so no current flows, when it isn't actuated. That's the opposite effect from a normally open valve.

## Operating envelope

The range of conditions, such as speed, load, pressure and temperature, that a DUT or a stand is designed to run in.

Also called the operating range, or for power electronics the safe operating area (SOA).

## Pass/fail criteria

The conditions a test result must meet for the DUT to pass, such as a maximum leak rate.

Also called acceptance criteria. They come from the DUT's specification.

## Personal protective equipment (PPE)

Equipment people wear to reduce their exposure to a hazard, such as safety glasses, gloves, or hearing protection.

PPE is the last level of the [hierarchy of controls](#hierarchy-of-controls). Use it with the other controls, not instead of them.

## PID control

A closed-loop control method that sets its output from the error between the setpoint and the measurement: in proportion to the error (P), to its sum over time (I), and to its rate of change (D).

Tuning a PID controller means choosing how much weight each term gets.

## PLC

Short for programmable logic controller: a rugged industrial computer that reads inputs, runs control software in a fixed scan cycle, and drives outputs.

PLCs are programmed in languages such as ladder logic.

## Precision

How close repeated measurements of the same value are to each other.

Also called repeatability. A precise sensor can still be inaccurate, if it's off by the same amount every time. Compare [accuracy](#accuracy).

## Pressure regulator

A valve that holds the pressure downstream of it at a set value, as long as the supply pressure is higher.

An electronic pressure regulator takes its setpoint as a command, such as `pr_2` on the fluids panel.

## Proof test

A test that pressurizes a part to a set pressure, above what it sees in service, to prove it holds without damage.

Also called a proof pressure test.

## Proportional valve

A valve that opens partway, in proportion to its command, rather than only open or shut.

On the fluids panel, `v_2` is a proportional valve. Compare a [solenoid valve](#solenoid-valve).

## Ramp

Changing a command gradually at a set rate, instead of in one step.

The rate is the ramp rate, such as RPM per second. The dyno's sequence ramps the DUT's speed at the rate in **DUT Speed Ramp Rate**.

## Range

The span of values a sensor or channel can measure, such as 0 to 100 psig.

Also called the measurement range or span. The top of the range is full scale (FS), and a sensor's specifications can be given as a percentage of it, such as ±0.5% FS.

## Redundancy

Using two or more independent parts for one function, so that one failure doesn't defeat it.

Safety circuits use redundancy, such as an E-stop with two separate contacts, each able to stop the machine. A single point of failure is a part whose failure alone defeats a function.

## Regen

Short for regenerative braking: a motor braking by working as a generator, which turns the energy it absorbs into electrical power.

On the dyno, the load motors generate power as they brake, and the power supply absorbs it. In the sequence's regen step, the load motors push the axle and the DUT brakes against them.

## Resolution

The smallest change a measurement can show.

For a DAQ, the [ADC](#analog-to-digital-converter-adc)'s number of bits sets it. Resolution isn't [accuracy](#accuracy): a reading can show many digits and still be wrong.

## Risk assessment

A structured review that finds a stand's hazards, estimates the risk of each, and decides which controls bring the risk down to an acceptable level.

ISO 12100 describes how to do one for machines. An [FMEA](#failure-mode-and-effects-analysis-fmea) is a related review that starts from how each part can fail.

## RTD

Short for resistance temperature detector: a temperature sensor whose resistance rises with temperature, such as a Pt100.

It's more accurate and stable than a [thermocouple](#thermocouple), over a smaller temperature range.

## Run

In general, one execution of a test. In Nominal, a run is a named period of time on one or more assets, such as a test, a flight or a race session.

See Nominal's [Run](https://dev.nominal.io/platform/reference/glossary/#run) entry.

## Safety

Freedom from unacceptable risk of harm. A test stand has two kinds: machine safety, which protects the equipment and the DUT, and human safety, which protects people.

On these stands, the control software keeps [machine safety](#machine-safety), and fail-safe hardware keeps [human safety](#human-safety). Software can stall or crash, so it never keeps people safe here.

| Failure | What protects against it | Kind of safety |
| --- | --- | --- |
| A measurement leaves its allowed range, such as an overspeed or an overtemperature | A [trip](#trip) in the control software | Machine safety |
| The control software stops sending commands | A [watchdog](#watchdog) in the hardware, such as in the dyno's motor controllers | Machine safety |
| Power is lost | [Fail-safe](#fail-safe) hardware, such as the fluids panel's normally open vent valve | Human safety |
| A person is in danger, or a stand does something unexpected | The [E-stop](#e-stop), wired fail-safe | Human safety |
| A person could reach a moving or pressurized part | [Guards](#guard) and [interlocks](#interlock) | Human safety |
| Someone works on the stand | [Lockout/tagout](#lockouttagout-loto) | Human safety |

[Hazard controls](#hazard-control) for human safety are chosen in the order of the [hierarchy of controls](#hierarchy-of-controls).

## Safety controller

Hardware designed and certified to carry out safety functions, such as stopping a machine when an E-stop is pressed or a guard opens.

Also called a safety relay, or a safety PLC if it's programmable. Unlike ordinary control software, it's built to standards such as ISO 13849 and IEC 61508, with [redundancy](#redundancy) and self-checks, so it can be relied on for [human safety](#human-safety).

## Sample rate

How often a channel's value is read, in samples per second or hertz (Hz).

Also called a sampling rate, a scan rate, or an acquisition rate. Sampling too slowly causes [aliasing](#aliasing).

## SCADA

Short for supervisory control and data acquisition: software that monitors and controls equipment spread across a site from one place.

It shows [HMI](#hmi) screens, records data in a [historian](#historian), and names each value a [tag](#tag).

## Sensor

A device that measures something physical, such as pressure or flow, and turns it into an electrical signal.

Also called a probe. With actuators, sensors are also called control points.

A sensor wired to a DAQ is a [transducer](#transducer), or a transmitter if it has electronics that output a standard signal such as 4–20 mA. A sensor built into a device with its own electronics and bus connection is part of an [instrument](#instrument). A gauge shows a measurement on the device itself, like the fluids panel's float gauge, and doesn't produce a channel.

## Sequence

A test's steps in order, from start up to shut down, each with what to do and what you should see.

Also called a procedure, a test procedure, a test script, or in process industries a recipe. The dyno runs its sequence from a script named **Procedure**.

## Setpoint

The value a command asks for, such as a speed of 1,000 RPM.

Also called a target, a demand, a reference, or SP. The dyno's software limits each setpoint to a safe range before sending it.

## Solenoid valve

An on/off valve that an electromagnet opens or closes when it's powered.

Compare a [proportional valve](#proportional-valve).

## Steady state

When a stand's measurements have stopped changing after a change in its commands.

The changing period before it is the transient. A [dwell](#dwell) gives a measurement time to reach steady state before it's recorded.

## Step response

How a measurement responds when its command changes suddenly, in one step.

It's described by the rise time, how long the measurement takes to get most of the way to its new value; the overshoot, how far it goes past; and the settling time, how long until it stays within a band around the new value.

## Stimulus and response

A stimulus is what a test applies to the DUT, such as a speed, a load or a pressure. The response is how the DUT reacts, as its sensors measure it.

Also called input and output, or in vibration and acoustics testing excitation and response. On the dyno, the load torque is a stimulus, and the DUT's current is its response.

## Stop category

How a machine stops, as defined in IEC 60204-1. Category 0 removes power at once, category 1 makes a controlled stop and then removes power, and category 2 makes a controlled stop and leaves power on.

An E-stop has to be category 0 or 1.

## Sweep

Running a test across a range of one input, such as speed, in steps or continuously, and recording the response at each point.

The dyno's sequence sweeps the DUT's speed at each of three loads.

## Tag

In Nominal, a key-value pair on data points, such as `motor_id: 1`, that lets you filter part of a dataset. In SCADA, PLC and historian software, a tag is what Nominal calls a channel.

See [Channel](#channel), and Nominal's [Tag](https://dev.nominal.io/platform/reference/glossary/#tag) entry.

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

## Tolerance

How far a value may be from its target and still be acceptable, such as 100 mm ± 0.1 mm.

A tolerance sets the [limits](#limit) of a pass/fail check.

## Torque sensor

A sensor that measures the twisting force on a shaft, with strain gauges on the shaft or in a flange.

Also called a torque transducer or a torque cell. The dyno has none: it calculates torque from each motor's current.

## Transducer

A device that converts one form of energy into another, such as a pressure into an electrical signal, or an electrical signal into motion.

On a test stand, a transducer is a sensor that outputs an electrical signal for a DAQ to read, such as the pressure transducer on the fluids panel's `p_1`. It has no bus connection or front panel of its own, unlike an [instrument](#instrument).

A transmitter is a transducer with built-in electronics that output a standard signal, such as a 4–20 mA [current loop](#current-loop).

## Trip

An automatic stop that the control software makes when a measurement leaves its allowed range.

Also called an automatic abort or an interlock trip. An abort that an operator starts, such as the dyno's **Abort** button, isn't a trip.

A trip is a [machine safety](#machine-safety) control. It can't keep people safe, because software can stall or crash. The [E-stop](#e-stop) and [fail-safe](#fail-safe) wiring do that.

## Uncertainty

The range around a measurement within which the true value is expected to lie, given every known source of error.

Also called measurement uncertainty. Combining the sources, such as sensor accuracy, ADC resolution and noise, is called an uncertainty budget or error budget.

## Unit under test (UUT)

Another name for a device under test (DUT): the device or system a test stand tests.

See [Device under test (DUT)](#device-under-test-dut).

## Watchdog

A timer that puts a device in a safe state if the software controlling it stops checking in.

On the dyno, each motor controller stops driving its motor if no command arrives for half a second, so a crashed program can't leave a motor running.

## Workbook

Where you analyze time-series data in Nominal, in tabs and panels, after a test or live.

Nominal's own definition is in the [platform glossary](https://dev.nominal.io/platform/reference/glossary/#workbook).

## Zero offset

A sensor's reading when the quantity it measures is zero.

Also called zero error or bias. Zeroing subtracts it, and on a scale it's called taring. In Nominal, an [offset](https://dev.nominal.io/platform/reference/glossary/#offset) is a time shift, not this.
