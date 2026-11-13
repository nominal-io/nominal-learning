# Control

{.lead}
Control makes a measurement follow a command. A controller compares the measured value with the setpoint, and adjusts its output until they match.

## Setpoint, process variable and error

Control theory names three quantities:[^ni-pid]

- The **process variable** is the quantity being controlled, as its sensor measures it. It's a {gloss}`measurement`.
- The **{gloss}`setpoint`** is the value you want the process variable to have.
- The **error** is the difference between the two.

On the dyno, when the sequence asks for 1,000 RPM, that's the setpoint. The DUT's measured speed is the process variable, and the gap between them is the error.

## Open loop and closed loop

An open-loop system sends a command and doesn't check the result. In the workshop, you command the fluids panel's proportional valve, `v_2`, and read the flow on `fm_1`, but nothing adjusts `v_2` to hold a flow. If the supply pressure changes, the flow changes with it.

A {gloss}`closed loop <closed loop>` measures the process variable, compares it with the setpoint, and adjusts its output, over and over at a fixed rate.[^ni-pid] The dyno's DUT runs closed loop: its motor controller measures the speed and adjusts the motor current to hold the setpoint as the load changes.

Loops can also run inside instruments, where they can be fast. The fluids panel's electronic pressure regulator, `pr_2`, holds its own outlet pressure at whatever setpoint it's commanded. The dyno's motor controllers hold speed themselves. The stand's control software then works one level up, setting the setpoints those inner loops follow.

## PID control

"Proportional-integral-derivative (PID) control is by far the most common way of using feedback in engineering systems."[^fbs-pid] A PID controller sets its output from the error, as the sum of three terms:

```text
output = Kp × error + Ki × (sum of error over time) + Kd × (rate of change of error)
```

- **Proportional.** Depends only on the present error. Raising its gain speeds up the response, but too much gain makes the process variable oscillate.[^ni-pid]
- **Integral.** Sums the error over time, so it keeps pushing until no error is left. It removes steady-state error, but increases overshoot.[^ni-pid]
- **Derivative.** Pushes back when the process variable is changing fast, which reduces overshoot. It's very sensitive to noise in the measurement, so most real systems use only a little of it.[^ni-pid]

Tuning a PID controller means choosing the three gains. Classic methods such as Ziegler–Nichols tuning give starting values from a simple test of the process.[^ni-pid][^fbs-pid]

Integral windup happens when the controller's output hits a limit, such as a motor controller's current limit. The loop is then effectively open: the output stays at the limit whatever the process variable does. The error persists, so the integral term keeps growing. When the error finally changes sign, the oversized integral holds the output at its limit for a while longer, and the process variable overshoots. Anti-windup prevents this by keeping the controller's output close to the limit, so it changes as soon as the error does.[^fbs-pid] Controllers such as LabVIEW's PID VI include it.[^ni-pid]

## Reading a step response

The step response is how the process variable responds when the setpoint jumps to a new value. It's described by four numbers:[^fbs-linear]

| Measure | Definition |
| --- | --- |
| Steady-state value | Where the process variable ends up, if it settles |
| Rise time | The time for the process variable to go from 10% to 90% of the way to its final value |
| Overshoot | How far the process variable goes past its final value, as a percentage |
| Settling time | The time until the process variable stays within 5% of its final value for good |

Texts differ on the details: some use a 2% band for settling time instead of 5%. Say which you use.

The steady-state error is the difference between the setpoint and the steady-state value. A loop without an integral term can end with some.

To measure rise time in Nominal, plot the setpoint and the measurement together in a {gloss}`workbook`, and read the times where the measurement crosses 10% and 90% of the change.

## Ramps, limits and settling: the dyno's sequence

The dyno's sequence doesn't jump its setpoints. It ramps them, and checks that the DUT has settled before it holds each test point:

1. **Ramp.** The DUT's speed setpoint moves at **DUT Speed Ramp Rate**, 200 RPM/s by default, and the load torque at **Load Torque Ramp Rate**, 0.5 Nm/s. Moving from a test point at 500 RPM to one at 750 RPM takes 1.25 s, and the warm-up's climb from 0 to 2,000 RPM takes 10 s.
2. **Settle.** Once a ramp ends, the sequence waits until the DUT's measured speed is within 50 RPM of its setpoint. If it isn't within 15 s, the sequence aborts.
3. **Hold.** Only then does the test point's hold time start, 10 s by default for each sweep test point, so the recorded data is at {gloss}`steady state`.

Throughout, every setpoint is clamped to its channel's range before it's sent.

A ramp asks less of the inner loop than a jump does. The motor controller doesn't have to accelerate as hard, so its current stays further from its limit, and the speed tracks the setpoint more closely.

At the end of the warm-up, the sequence measures the ratio between the DUT's speed and the load motors' speed, and projects the load motors' speed at the fastest test point of the plan. If that projection is above the load motors' overspeed limit, the sequence aborts before the sweep starts, instead of finding out at full speed.

## Loop rates

A loop can't correct faster than it measures. If a loop runs too slowly for the process it controls, it reacts late, and a late correction overshoots or oscillates.

The dyno's software runs several loops at different rates:

| Loop | Times a second |
| --- | ---: |
| Sending commands to, and reading, each motor controller | ~16 |
| The sequence, which updates the setpoints | 10 |
| Reading the power supply | 2 |

The motor controllers' own speed and current loops run inside them, much faster than any of these. That's why the software can set the speed only 10 times a second and still get a steady speed.

## Sequences and states

Above the control loops, a {gloss}`sequence` decides which setpoints apply when. The software that runs it is a state machine: at any moment the stand is in one state, and only certain commands are allowed in each.

The dyno's software has these states:

| State | What it means |
| --- | --- |
| OFF | Not connected. |
| ARMING | Connecting the instruments and powering the bus. |
| ARMED | Powered and ready. Setpoints can be staged, but no motor commands are sent. |
| RUNNING | Sending motor commands. |
| STOPPING | Bringing every motor to zero, then back to ARMED. |
| TRIP_STOPPING | Stopping every motor after a trip. |
| TRIPPED | Stopped after a measurement left its allowed range. Can return to ARMED only once every measurement is back in range. |
| DISARMING | Turning off the power supply and disconnecting, then back to OFF. |

The states are a form of protection in themselves: the software sends motor commands only in RUNNING, STOPPING and TRIP_STOPPING. See [Safety](safety.md).

## Further reading

- K. J. Åström and R. M. Murray, [Feedback Systems: An Introduction for Scientists and Engineers](https://fbswiki.org/wiki/index.php/Main_Page), a free textbook, with chapters on linear systems and PID control.
- NI, [The PID Controller & Theory Explained](https://www.ni.com/en/shop/labview/pid-theory-explained.html).

## References

[^ni-pid]: NI, ["The PID Controller & Theory Explained"](https://www.ni.com/en/shop/labview/pid-theory-explained.html), updated 2025-03-07. Retrieved 2026-11-12.
[^fbs-pid]: K. J. Åström and R. M. Murray, ["PID Control"](https://www.cds.caltech.edu/~murray/books/AM08/pdf/fbs-pid_24Jul2020.pdf), chapter 11 of *Feedback Systems: An Introduction for Scientists and Engineers*, 2nd edition, version 3.1.5, 2020-07-24, Princeton University Press. Retrieved 2026-11-13.
[^fbs-linear]: K. J. Åström and R. M. Murray, ["Linear Systems"](https://fbswiki.org/wiki/index.php/Linear_Systems), chapter 6 of *Feedback Systems: An Introduction for Scientists and Engineers*, 2nd edition, Princeton University Press. Retrieved 2026-11-12.
