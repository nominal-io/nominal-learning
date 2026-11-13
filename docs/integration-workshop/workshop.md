# Test a unit across systems

{.lead}
In this 60-minute session you test units on the e-axle dyno, with a test executive, an MES and MATLAB working together, then trace each test through Nominal. Read [Before the workshop](pre-read.md) first.

By the end, you can:

- Trace a unit's test from the MES, through the test executive and the drivers, to Nominal and back.
- Find any step of a test from its event, and check a result against the data it came from.

## Safety first

Before anyone touches the dyno, your facilitator shows you where its E-stop is and what it does. Anyone may press it at any time, for any reason, without asking. Stay outside the dyno's guard while it's running.

The test executive is software, so it doesn't keep anyone safe. See the [Safety guide](../guides/safety.md#which-control-covers-which-failure).

## The system

Your facilitator walks everyone through the system before you split up. Each row is one connection between two pieces:

| From | To | What it sends |
| --- | --- | --- |
| MES | Test executive | The unit's part number, and its limits |
| Test executive | Drivers | Each step's setpoints |
| Drivers | Motor controllers and power supply | Commands, over the CAN bus and USB |
| Motor controllers and power supply | Drivers | Measurements, over the same links |
| Drivers | Nominal | Every measurement, as channels |
| Test executive | Nominal | A run for the unit, and an event for each step |
| Test executive | MATLAB | Each sweep test point's start and end times |
| Nominal | MATLAB | The DUT's current for that time |
| MATLAB | Test executive | The test point's mean current |
| Test executive | MES | The unit's result, and a link to its run |

## Groups and roles

Your facilitator splits you into two groups of up to five. One group starts at the dyno and the other at the analysis station, a laptop with MATLAB and the workbook. The groups swap halfway through.

At the dyno, each person takes one of these roles:

- **Operator:** starts the unit's test.
- **Reader:** reads each step aloud, including what you should see.
- **MES clerk:** opens the unit's record in the MES, before and after the test.
- **Data watcher:** reads out each step's event as it appears in the workbook.
- **Recorder:** writes down the group's prediction before each step, and what actually happened.

At the analysis station, work in pairs.

## At the dyno

Before each step marked *Predict*, agree as a group on what you expect to see, and have the recorder write it down.

1. Take a unit card from your facilitator. It has a serial number and a part number.
2. MES clerk: open the unit's record in the MES, and read out its status and its current limits.
3. *Predict:* the executive needs the unit's limits before it starts. What should it do if the MES doesn't answer?
4. Operator: start the unit's test with its serial number, as your facilitator shows you.
5. Data watcher: in the workbook, watch each step's event appear as the step ends. Read out its name and type.
6. *Predict:* will the test point at the highest speed and the third load step pass its current limit?
7. When the executive reports the unit's result, MES clerk: refresh the unit's record. Read out the result, and open the link to the run.
8. If there's time, test a second unit with the other part number. *Predict* first: will its result be the same?

% SCREENSHOT: the workbook during a unit's test, with step events above the speed and current plots

## At the analysis station

Work on the run your facilitator gives you: the other group's last unit, or a recorded run in the first rotation.

1. Open the run in the workbook. Find the event for one sweep test point, and copy its start and end times.
2. In MATLAB, read the DUT's current for that time, and compute its mean with Nominal's [MATLAB client](https://dev.nominal.io/matlab/):

   ```matlab
   client = nominal.Client.fromProfile();
   dyno = client.assetByRid("<the dyno's asset RID>");

   % The step event's start and end, from the workbook
   t0 = datetime("<start>", TimeZone="UTC");
   t1 = datetime("<end>", TimeZone="UTC");

   current = dyno.fetch("<DUT current channel>", t0, t1);  % a timetable
   mean(current{:, 1})
   ```

3. *Predict:* will your mean match the `mean_current_a` property on the step's event exactly?
4. Compare your mean with the event's property. Where they differ, work out why.
5. Find the sweep test point that came closest to its limit.

## If a piece is down

At the end, your facilitator asks both groups what happens to the stand, the data and the unit's result in each of these cases:

1. The MES doesn't answer when the operator starts a unit's test.
2. MATLAB stops responding during the sweep.
3. The test executive crashes in the middle of a step.

## Before you leave

Write one thing that worked and one thing that didn't on a card, and hand it to your facilitator.
