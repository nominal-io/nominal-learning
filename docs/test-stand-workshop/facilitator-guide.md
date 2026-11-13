# Facilitator guide

{.lead}
[Run a test on the stands](workshop.md) takes up to 10 people through one fluids panel and one e-axle dyno in 60 minutes. You need a second facilitator who knows the stands, so that each stand has one of you, and about 30 minutes to prepare.

## Two days before

Send everyone [Before the workshop](pre-read.md) and ask them to read it.

## Before the session

1. Check the fluids panel: power on, E-stop released, and the panel reaching about 85 psig on `p_1`. Then press the E-stop and confirm that the vent opens and `p_1` falls. Reset it, and leave `p_1` at 0 psig for the first group.
2. Check the dyno: the control app connects, the guard is closed, and the E-stop works.
3. In the dyno's control app, check that the **Stand Control** script on the **MANUAL** tab isn't running. Only one script can control the stand at a time.
4. On the **AUTO** tab, start the **Procedure** script under **RUN**. Wait for **Logs** to show "Stand built, press Start to run the procedure".
5. Confirm that both stands' channels are streaming to Nominal.
6. Open the workbook for "Find it in the data" on a screen for each group.
7. Pick a `v_2` command for the flow control step.
8. Split everyone into two groups of up to five, and decide which group starts at which stand.
9. Agree with the second facilitator on which stand each of you runs, and on a signal for "stop and look at the stand".

## Timing

| Time | Part | Notes |
| ---: | --- | --- |
| 0:00 | Safety and groups | Everyone together. Show each E-stop and press it. Form the two groups and assign the first roles. |
| 0:08 | First rotation | One group at each stand. The dyno group selects **Start** by 0:12. |
| 0:27 | Swap | Hand over each stand, as in the next section. |
| 0:29 | Second rotation | The dyno group selects **Start** by 0:33. |
| 0:47 | Find it in the data | Each group answers the three questions in the workbook. |
| 0:55 | Cards | Collect them before people leave. |

With the default inputs, a dyno run takes 4 to 7 minutes from **Start** to the cool-down, where the group aborts it. Most of the variation is the warm-up, which waits up to 3 minutes for the DUT to reach 35 °C.

If you fall behind, shorten the flow control branch first. Keep the proof and leak branch whole, because the data part depends on it.

## Hand over a stand

If a dyno run is still going 2 minutes before the end of a rotation, have the group select **Abort**.

At the swap, check each stand before the incoming group starts:

- **Fluids panel:** the outgoing group has finished Shut down, and `p_1` reads 0 psig.
- **Dyno:** **Logs** doesn't show "Stand closed" after the last run. If it does, restart the **Procedure** script, as in "When something goes wrong" below.

## Running it

At each *Predict* step, ask for one answer from the group, and wait until the recorder writes it down before anyone sends the command. Don't tell them the answer first.

Ask each question below at the point it names. Correct any wrong answers before moving on.

- **After start up:** "The compressor stopped. Is the system off?" No: it's holding pressure at the regulator's setpoint. If someone says yes, they may think the compressor is the only source of pressure.
- **After proof and leak:** "`p_2` dropped a little after you sealed the vessel. Did it fail?" It depends on the allowed leak rate. A leak check compares the drop with a limit, so a drop on its own isn't a failure.
- **After the dyno:** "Who stopped the motors when you selected **Abort**: the app or the E-stop?" The app, which commanded every motor to zero. The E-stop is a separate hardware path that works without the app.

## Answers to the pre-read

1. `fm_1`, the flow meter. `v_2` is the command, not the measurement.
2. Not necessarily. Under load, a motor can fall a little short of its command. The dyno's sequence accepts up to 50 RPM of difference. It aborts the run if the DUT doesn't get that close within 15 seconds of the end of each speed ramp.
3. The E-stop. Pressing it, or losing power, opens the normally open vent valve and releases the pressure, with no software involved.

## When something goes wrong

- **Anyone feels unsafe, or a stand behaves unexpectedly:** press the E-stop first, then work out why.
- **The dyno's run stops early:** read **Logs** for the reason. If it shows "Stand closed" after the run, the **Procedure** script has stopped, which it does after a trip or an error. Start it again, and wait for "Stand built, press Start to run the procedure" before the group selects **Start**.
- **A stand is down before the session:** run its part as a walkthrough at the stand, and use a recorded run for "Find it in the data".
- **Data isn't reaching Nominal:** carry on with the stands, and use a recorded run for the data part.

## After the session

Read the cards the same day. Note what was too fast, too slow or confusing, and change the session or the pre-read for the next group.
