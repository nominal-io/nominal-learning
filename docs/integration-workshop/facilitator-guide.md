# Facilitator guide

{.lead}
[Test a unit across systems](workshop.md) takes up to 10 people through one e-axle dyno, connected to a test executive, an MES and MATLAB, in 60 minutes. You need a second facilitator for the analysis station, and about 45 minutes to prepare.

## What the session needs

Beyond the dyno and its drivers, the session needs these pieces:

- **The test executive:** a Python program on the dyno's computer. It takes a serial number, gets the unit's record from the MES, and opens a run on the dyno's asset. It then runs the dyno's steps through the drivers, and creates an event for each step. It calls the MATLAB function after each sweep test point, and sends the result and the run's link to the MES at the end.
- **The MATLAB function:** the executive calls it through the [MATLAB Engine API for Python](https://www.mathworks.com/help/matlab/matlab-engine-for-python.html). It takes a test point's start and end times, reads the DUT's current for that time from Nominal, and returns its mean.
- **The stand-in MES:** a small web service on your laptop, with a page for each unit. Each unit's record holds its serial number, part number, status, current limits and result.
- **Unit cards:** at least four, each with a serial number and a part number, split across two part numbers. Set one part number's limits above the axle's mean current at every test point, and the other's below it at one or more test points, using a recorded run. Then some units pass and some fail.
- **The analysis station:** a laptop with MATLAB, Nominal's MATLAB client, and a profile that can read the dyno's data.
- **A recorded run** of a unit's test, for the first rotation's analysis group.

The executive records each unit's result when the regen step ends. The cool-down that follows isn't part of the result.

## Two days before

Send everyone [Before the workshop](pre-read.md) and ask them to read it.

## Before the session

1. Check the dyno: the guard is closed, the E-stop works, and its drivers stream to Nominal.
2. Check that nothing else is controlling the dyno. Only one program can control it at a time.
3. Start the stand-in MES, and reset every unit's record to untested.
4. Test one unit end to end. Check that its step events appear in the workbook, that its sweep events have a mean current, and that its MES record shows the result and a link to the run.
5. Reset that unit's record.
6. On the analysis station, check that the MATLAB example in the workshop reads the recorded run's DUT current. Fill in the dyno's asset RID and the DUT current channel's name in the example, or have them ready to hand out.
7. Open the workbook on a screen at the dyno, and on the analysis station.
8. Split everyone into two groups of up to five, and decide which group starts at which station.

## Timing

| Time | Part | Notes |
| ---: | --- | --- |
| 0:00 | Safety and the system | Everyone together. Show the E-stop and press it. Walk through the table in "The system", pointing at each piece. |
| 0:10 | First rotation | One group at the dyno, one at the analysis station. The dyno group starts its first unit by 0:14. |
| 0:30 | Swap | The analysis group takes the dyno group's last run. |
| 0:32 | Second rotation | The dyno group starts its first unit by 0:36. |
| 0:50 | If a piece is down | Everyone together. Ask the three questions, as in the next section. |
| 0:57 | Cards | Collect them before people leave. |

With the dyno's default inputs, a unit's test takes 4 to 7 minutes. Most of the variation is the warm-up, which waits up to 3 minutes for the DUT to reach 35 °C. A group that's fast can test a second unit.

## Running it

At each *Predict* step, ask for one answer from the group, and wait until the recorder writes it down. Don't tell them the answer first.

Ask each question below at the point it names. Correct any wrong answers before moving on.

- **When the first step event appears:** "Why does the event appear when the step ends, not when it starts?" The executive creates each event once it knows the step's end and whether the step passed.
- **When the MES record updates:** "Where does the link in the MES record go, and who put it there?" To the unit's run in Nominal. The executive sent it, with the result.
- **At the analysis station:** "Your mean differs from the event's a little. Is one of them wrong?" Not necessarily. A small difference can come from a slightly different time window, because the times copied from the workbook are rounded.

## If a piece is down

Ask what happens to the stand, the data and the unit's result in each case. Good answers include:

1. **The MES doesn't answer.** The executive shouldn't start: without the unit's record, it has no limits to test against, and nowhere to send the result.
2. **MATLAB stops responding.** The measurements are already in Nominal, so nothing is lost. The executive should stop the motors, mark the step's event as an error, and record no pass for the unit. The analysis can be run again later from the data in Nominal.
3. **The executive crashes mid-step.** Each motor controller stops its motor half a second after its last command. The drivers run in the executive's process, so the channels stop too. The unit's run has no end, and the step that was running has no event. The MES record still shows the unit as in test, so nobody can mistake it for a pass.

## Answers to the pre-read

1. The drivers. They stream the channels. The executive is working, because its step events arrive.
2. In the MES. The executive gets the limits from the MES for each unit, so a change there applies to the next unit tested.
3. The function may be reading the wrong time window, such as local times treated as UTC, which moves the window away from the test. It may also be reading the wrong channel.

## When something goes wrong

- **Anyone feels unsafe, or the dyno behaves unexpectedly:** press the E-stop first, then work out why.
- **A unit's test stops early:** read the executive's last step event, and its log, for the reason. Reset the unit's MES record before testing it again.
- **The MES or MATLAB is down before the session:** run the dyno part as a walkthrough with the recorded run, and use the "If a piece is down" questions to discuss it.
- **Data isn't reaching Nominal:** carry on at the dyno, and use the recorded run at the analysis station.

## After the session

Read the cards the same day. Note what was too fast, too slow or confusing, and change the session or the pre-read for the next group.
