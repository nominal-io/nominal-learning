# Before the workshop

{.lead}
In the workshop, you operate two test stands, then find what happened in the data. Read this first. It takes about 10 minutes.

## What a test stand does

A test stand holds the device under test (DUT), puts it through controlled conditions, and measures how it responds. A test might check that a motor delivers its rated torque, or that a pressure vessel holds pressure without leaking.

Every stand has two kinds of devices around the DUT:

- **Actuators** change something physical when the stand tells them to. Valves, motors, compressors and pressure regulators are actuators.
- **Sensors** measure something physical, such as pressure or flow, and turn it into an electrical signal.

## Data acquisition and control

Sensors and actuators reach the computer in one of two ways. Each can be wired on its own to a data acquisition (DAQ) system, or built into an instrument that the computer talks to over a communications bus.

On the fluids panel, each device is wired to a DAQ. Its sensors are {gloss}`transducers <transducer>`: each turns one physical quantity, such as pressure, into an electrical signal for the DAQ to read. The DAQ has four kinds of input and output:

| Kind | What connects to it | Example on the fluids panel |
| --- | --- | --- |
| Analog input | A sensor that reports a value in a range | `p_1`, the supply pressure |
| Digital input | A sensor that reports on or off | `sw_1`, the switch that shows the slide is retracted |
| Analog output | An actuator you set anywhere in a range | `v_2`, the proportional valve |
| Digital output | An actuator you turn on or off | `pump_1`, the compressor |

On the dyno, the motor controllers and the power supply are {gloss}`instruments <instrument>`. Each has its own transducers, electronics and power stage built in. A motor controller measures its motor's speed, current and temperature, and switches the power that drives it. The computer sends commands and reads measurements as messages over a {gloss}`communications bus`: a CAN bus for the motor controllers, and a USB connection for the power supply. The power supply also has a {gloss}`front panel` of buttons and a screen, for running it by hand.

A flow meter, for example, can be a bare transducer wired to a DAQ, or an instrument with its own display and bus connection.

Software turns each DAQ input and output, and each instrument reading and command, into a **channel**: a named value, with units if it's a quantity, such as `p_1` in psig. The part of the software that talks to a DAQ or an instrument is called a driver. It turns each electrical signal into a channel's value. For example, the pressure sensor on `p_1` outputs a current between 4 and 20 mA, which software scales to a pressure between 0 and 100 psig.

Control software works with the channels, not with the hardware. It runs in a loop at a set rate. Each time around, it reads the latest commands and measurements, decides what each actuator should do, and writes the results. Some channels are calculated rather than measured. The dyno's torque channels, for example, are calculated from each motor's current.

## Commands and measurements

A **command** is a value you write to ask for something, such as "open the valve 40%" or "spin at 1,000 RPM". The value it asks for is the **setpoint**. A **measurement** is a value a sensor reports about what actually happened.

A command doesn't tell you what happened. For that, read the measurement that shows its effect. On the fluids panel, you command `v_2`, and `fm_1` measures the flow that results. On the dyno, you command the DUT's speed, and its motor controller measures the speed it actually reaches.

A command and its measurement can differ. Valves take time to move, motors take time to speed up, and under load a motor may not reach its target at all. Software can also change a command on its way to the hardware. The dyno's software limits each command to a safe range, so asking for more than the maximum sends the maximum. It also converts units: you command the load motors in torque, and it sends each one the current that produces that torque.

In the workshop, you compare commands with measurements. Where a measurement doesn't follow its command, find out why.

## Sequences

Tests run as sequences of steps, in order: start up, run the test steps, shut down. Each step says what to do and what you should see, such as "Close the valve. Pressure holds steady." Writing down what you expect before each step is how a test catches problems.

## Limits and safety

A stand has two kinds of safety, and different things keep each one:

- **Machine safety** protects the stand and the DUT from damage. The control software keeps it. It watches the measurements and stops the test when one leaves its allowed range, which is called a trip.
- **Human safety** protects people. Hardware keeps it, with **fail-safe** wiring that works without any software. Fail-safe means that a failure, such as a cut wire or a power loss, leaves the stand in its safe state.

The emergency stop (E-stop) button is wired fail-safe. On the fluids panel, pressing the E-stop or losing power opens a vent valve, which releases the air pressure. A valve that opens when it loses power is called normally open.

Software can stall or crash, so on these stands it never keeps people safe. The [glossary's Safety entry](../glossary.md#safety) shows which control protects against which failure.

## Where the data goes

While a test runs, every channel streams to Nominal. Each measurement is stored with its time, so you can line up what you commanded with what happened. After the run, you open the data in a workbook to plot it and compare it.

## The two stands

The **fluids panel** controls compressed air. A compressor fills a supply line that feeds three branches:

- **Flow control:** a proportional valve sets how much air flows, and a flow meter measures it.
- **Linear actuation:** a valve pushes an air-driven slide out and back, and two switches report when it reaches each end.
- **Proof and leak:** a regulator fills a small pressure vessel, a valve seals it off, and a pressure transducer shows how fast it loses pressure. A vessel that leaks too fast fails a leak check.

The **e-axle dyno** tests an electric axle, which is its DUT. A dynamometer (dyno) loads a motor and records its speed and torque. Here, the axle's own motor drives it, and a load motor on each side of the axle brakes it. This dyno calculates torque from each motor's current rather than measuring it directly. The load motors generate energy as they brake, and the stand's power supply absorbs it. Running a range of speeds at three loads shows how the DUT behaves across its operating range.

% SCREENSHOT: photo of each stand, with the parts above labeled

## Check yourself

Answers are in the [facilitator guide](facilitator-guide.md).

1. On the fluids panel, you command the flow valve to 50%. Which channel tells you how much air is actually flowing?
2. The dyno's DUT is commanded to 1,500 RPM, but measures 1,470 RPM while the load motors brake. Is something broken?
3. Someone's code has a bug, and the fluids panel's software stops responding mid-test. What makes the panel safe?
