# Run a test on the stands

{.lead}
In this 60-minute session you operate the fluids panel and the e-axle dyno, then find what happened in the data. Read [Before the workshop](pre-read.md) first.

By the end, you can:

- Trace a step from the command you send, through the actuator it moves, to the sensor and channel that measure the result.
- Predict how a measurement responds to a command, then check your prediction against the recorded data.

## Safety first

Before anyone touches a stand, your facilitator shows you where each E-stop is and what it does. Anyone may press an E-stop at any time, for any reason, without asking. Stay outside the dyno's guard while it's running, and keep hands off the fluids panel's moving slide.

## Groups and roles

Your facilitator splits you into two groups of up to five. One group starts at the fluids panel and the other at the dyno, and the groups swap stands halfway through. Start with the section for your stand.

In your group, each person takes one of these roles. Rotate roles each time you start a new set of steps, such as Start up on the fluids panel.

- **Operator:** sends the commands.
- **Reader:** reads each step aloud, including what you should see.
- **Data watcher:** reads out the channel values from the screen.
- **Recorder:** writes down the group's prediction before each step, and what actually happened.
- **Timekeeper:** writes down the clock time when you seal the vessel, select **Start** and select **Abort**. Both groups' runs land on the same channels, so these times are how you find yours in the data.

## Fluids panel

Before each step marked *Predict*, agree as a group on what you expect to see, and have the recorder write it down.

### Start up

1. Check that the E-stop isn't pressed and that `p_1` reads 0 psig. If not, stop and tell your facilitator.
2. Turn on the compressor, `pump_1`.
3. Turn on the main vent valve, `v_1`. The valve closes, which lets the system hold pressure.
4. *Predict:* what does the supply pressure, `p_1`, do now, and when does the compressor stop?
5. Watch `p_1` until the compressor turns off. It stops at the regulator's setpoint of about 85 psig.

### Flow control

1. *Predict:* if you open the proportional valve `v_2` a little, what do the float gauge and the flow meter `fm_1` do?
2. Command `v_2` to a value your facilitator gives you.
3. Watch the float gauge on the panel, and `fm_1` on the screen.
4. Command `v_2` to 0%.

### Linear actuation

1. *Predict:* which position switch, `sw_1` or `sw_2`, changes when the slide extends?
2. Turn on `v_3`. The slide extends, and `sw_2` reads high.
3. Turn off `v_3`. The slide retracts, and `sw_1` reads high.

### Proof and leak

This branch runs a leak check: fill a vessel, seal it, and measure how fast it loses pressure.

1. Check that `v_5` is off. This valve is normally open, so off means air can flow into the vessel.
2. Command the pressure regulator `pr_2` to 50%, which is about 72 psig.
3. Watch the vessel pressure, `p_2`, rise until it's steady.
4. *Predict:* what does `p_2` do when you seal the vessel?
5. Turn on `v_5` to close it, and watch `p_2` for about a minute.
6. Command `pr_2` to 0%. You may hear the regulator venting.

### Shut down

1. Check that `v_2`, `v_3`, `pr_2` and `v_5` are all back off or at 0%.
2. Turn off `pump_1`.
3. Turn off `v_1`. The vent valve opens, and `p_1` falls to 0 psig.
4. Leave everything off. The next group starts up from here.

Your facilitator drains the compressor's tank after the session.

## E-axle dyno

The dyno runs an automated sequence: a warm-up, then a speed sweep at each of three load steps, then a regen step and a cool-down. In the regen step, the load motors push the axle instead of braking it, and the DUT brakes against them.

1. In the dyno's control app, open the **AUTO** tab. In the **SWEEP & REGEN** panel, find the sweep's speeds in **Sweep Start DUT Speed**, **Sweep Stop DUT Speed** and **Sweep DUT Speed Step**, and the loads in **Load Step 1** to **Load Step 3**. Don't change any inputs, because the other group runs with them too.
2. *Predict:* the sweep runs every speed at load step 1, then again at load steps 2 and 3. At the same speed, how does the DUT's current change from one load step to the next?
3. Under **RUN**, select **Start**. **Logs** shows "Starting procedure, 18 steps". If it doesn't, tell your facilitator.
4. Watch the **Line Plot** and **TEMPERATURE** panels, and the messages in **Logs**. The warm-up holds one speed until the DUT reaches 35 °C, or for up to 3 minutes.
5. When **Logs** shows "Step 18/18", the start of the cool-down, select **Abort**. The app commands every motor to zero, and the plots pause for up to 10 seconds while it waits for the motors to stop. Read what **Logs** reports.

% SCREENSHOT: the dyno control app during the sweep, with the panels above in view

## Find it in the data

Your facilitator opens a workbook with the data from your session. Use your timekeeper's times to find your group's runs.

1. Find the moment you sealed the vessel in the proof and leak branch. How much did `p_2` drop in the minute after?
2. Find the same speed in load steps 1 and 2. Did the DUT's current change the way you predicted?
3. Find the abort. How long did the DUT take to stop?

Compare each answer with the recorder's notes. Where your prediction was wrong, work out why with your group.

## Before you leave

Write one thing that worked and one thing that didn't on a card, and hand it to your facilitator.
