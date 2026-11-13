# Before the workshop

{.lead}
In the integration workshop, you test units on the e-axle dyno with several programs working together, then trace each test through them. Read this first. It takes about 10 minutes, and builds on the [test stand workshop's pre-read](../test-stand-workshop/pre-read.md).

## A test system is more than one program

On most stands, Nominal is one program among several. Each does one job, and passes what it knows to the next. In the workshop, five pieces work together:

| Piece | What it does | In the workshop |
| --- | --- | --- |
| {gloss}`Drivers <driver>` | Talk to the instruments, and stream every measurement to Nominal | Python, with [instro](https://dev.nominal.io/instro/), Nominal's open-source library for test equipment: one driver for each motor controller, and one for the power supply |
| {gloss}`Test executive` | Runs the test's steps in order, through the drivers, and decides whether the unit passed | A Python program that runs in the background on the dyno's computer |
| Analysis | Computes a result from a step's data | A MATLAB function that the executive calls after each test point |
| {gloss}`MES <manufacturing execution system>` | Tracks each unit through production: what to test it against, and whether it passed | A stand-in service on the facilitator's laptop |
| Nominal | Stores the measurements, the steps and the results on one timeline | The dyno's asset, with a {gloss}`run` for each unit tested |

## What each piece tells Nominal

Each piece sends Nominal a different kind of record:

- **Channels**, from the drivers: each measurement, with the time it was taken.
- **A run** for each unit, from the executive: the time from the start of the unit's test to its end, with the unit's serial number and part number as properties, and a link to its record in the MES.
- **{gloss}`Events <event>`**, from the executive: one for each step, from the step's start to its end. The event's type shows whether the step passed, and its properties hold the step's setpoints and results.

This is how the executive creates them, with Nominal's [Python client](https://dev.nominal.io/python/):

```python
from datetime import datetime, timezone
from nominal.core import EventType, NominalClient

client = NominalClient.from_profile("default")
dyno = client.get_asset("<the dyno's asset RID>")

# One run per unit, left open until the unit's test ends
run = client.create_run(
    serial_number,
    start=datetime.now(timezone.utc),
    end=None,
    properties={"serial_number": serial_number, "part_number": part_number},
    links=[mes_record_url],
    assets=[dyno],
)

# One event per step, created when the step ends
dyno.create_event(
    "Step 9: sweep at 1000 RPM, load step 2",
    EventType.SUCCESS,  # EventType.ERROR if the step failed
    start=step_start,
    duration=step_end - step_start,
    properties={"mean_current_a": 2.1, "limit_a": 2.5},
)

run.update(end=datetime.now(timezone.utc))
```

Each kind of record answers a different question:

| Question | Where the answer is |
| --- | --- |
| What was the DUT's speed at 12:04:31? | The DUT's speed channel |
| When did the sweep's second load step start? | That step's event |
| Which unit was on the stand at 12:04? | The run that covers 12:04, by its serial number |
| Did a unit pass? | Its record in the MES, and the types of its run's step events |

## One owner for each fact

Give each fact one owner, and have the other pieces ask that owner for it:

- The MES owns each unit's record: its part number, its limits, and its result.
- The executive owns the sequence: which step runs when, and whether it passed.
- Nominal holds the data: every measurement, step and result, on one timeline.

If the limits were also written into the executive's code, changing a limit in the MES would leave the executive testing against the old one.

## Time is the common key

Nominal lines up channels, events and runs by their timestamps. Each piece stamps what it sends with the time it happened, in UTC. If two computers' clocks disagree, an event can appear before the speed change it marks. In the workshop, the drivers, the executive and MATLAB all run on the dyno's computer, so they share one clock.

## The test for one unit

1. The operator enters the unit's serial number.
2. The executive asks the MES for the unit's record: its part number, and the limit on the DUT's current at each test point.
3. The executive opens a run for the unit, then runs the dyno's steps through the drivers: a warm-up, a speed {gloss}`sweep` at three loads, and a {gloss}`regen` step.
4. After each sweep test point, the executive calls the MATLAB function with the test point's start and end times. The function reads the DUT's current for that time from Nominal, and returns its mean. The executive compares the mean with the limit, and creates the step's event.
5. When the last step ends, the executive ends the run, and sends the result and a link to the run to the MES.

The units in the workshop are all the same physical axle. Serial numbers stand in for different units. Two part numbers have different limits, so the same axle can pass as one part number and fail as the other.

## Check yourself

Answers are in the [facilitator guide](facilitator-guide.md).

1. Step events appear in the workbook, but the DUT's speed channel has no data. Which piece do you check first?
2. A part number's current limit needs to change. Where do you change it?
3. The MATLAB function returns a mean current of 0 A for every test point, but the workbook shows current flowing. What could be wrong?
