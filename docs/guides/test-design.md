# Test design

{.lead}
A test answers one question: does this design work, or was this unit built right? The answer decides how often you test, on which units, and how hard.

## Two questions a test can answer

A test can answer one of two questions:

- **Does this design work?** You test a design once per version, on a few representative units, to show it meets its requirements with margin. This guide calls that **design testing**.
- **Was this unit built right?** You test every unit you build, to catch the ones that came out wrong. This guide calls that **production testing**.

The same stand can run both, but the tests are different:

| | Design testing | Production testing |
| --- | --- | --- |
| Question | Does this design meet its requirements, with margin? | Was this unit built correctly? |
| How often | Once per design version | On every unit |
| On what | A few representative units | Every unit that ships |
| Conditions | Beyond expected use, to show margin | Normal use, plus screens for build defects |
| Damage | Can wear out or destroy the unit | Mustn't harm a good unit |
| Time | Hours to months | Seconds to minutes per unit |
| Result | Characterization data and margins | Pass or fail for each unit, and trends across units |
| Industry names | Qualification, design validation test (DVT) | Acceptance test, end-of-line (EOL) test |

NASA's spacecraft testing shows the split. Acceptance activities "are performed on each of the flight units as they are manufactured".[^nasa-verification] Qualification uses dedicated hardware tested "to verify the design, demonstrate margin, and validate an acceptance test program".[^gevs] The margins differ too: in thermal testing, qualification goes 15 °C beyond the highest allowable flight temperature, and acceptance only 5 °C.[^gevs]

A production test looks for build defects, so it can stress a unit on purpose to reveal them. NASA uses random vibration "to detect bad solder joints, loose or missing fasteners, improperly mounted parts".[^gevs] Those are defects of one unit, not of the design.

NASA Goddard's default is protoflight testing, which combines the two: one unit is tested at reduced qualification levels, then flown. Its thermal margin, 10 °C, sits between the other two.[^gevs]

You'll also meet the terms verification and validation, which NASA frames as "Was the end product realized right?" and "Was the right end product realized?".[^nasa-verification] They appear in names such as DVT and "verification matrix". This guide says design testing and production testing instead, because the two words are easy to mix up.

## The golden unit

A golden unit is a unit known to be good, kept as a reference. Production test teams use one to develop and debug tests, and to check that a new test script works before it judges real units.[^keysight-golden]

A golden unit has limits. Its performance can degrade over time, for example from contamination, and there's no clear rule for how close to perfect a unit has to be to count as golden.[^keysight-golden] Check it against its own history, and retire it when it drifts.

Keep a known-bad unit too. A test that passes the golden unit shows only that the test can pass a unit. A test that fails a known-bad unit shows that it can fail one.

## Development phases

Hardware companies name the phases of a product's development after the tests in each one:[^formlabs]

1. **Engineering validation test (EVT).** Early units, made with high-precision processes, to build confidence that the design works.
2. **Design validation test (DVT).** Units made the way production will make them, to show the design can be manufactured at scale and passes its tests. Typically 50 to 200 units.
3. **Production validation test (PVT).** The last phase before mass production, to show the production line meets its targets. The production jigs, fixtures and test stands have to be in place and validated.
4. **Mass production (MP).** The focus moves to yield, cost and scale.

Design testing happens in EVT and DVT. The production test stands are built and proven in PVT, and production testing runs on every unit from then on.

## The V-model

The V-model, or Vee, lays out a project as a V. Down the left side, requirements are split into a system design, then subsystems, then components. Up the right side, the parts are built, integrated and tested, and each level on the right is tested against the specification from the same level on the left:[^fhwa-vee]

```text
Requirements ───────────────────────────── System acceptance test
   System design ───────────────────── System test
      Subsystem design ───────────── Subsystem test
         Component design ──────── Component test
                         Build
```

Testing goes bottom up, from components to subsystems to the whole system.[^fhwa-vee] Each requirement's test method is chosen as the requirement is written, not after the system is built.[^fhwa-vee]

A single V for a whole project means finding integration problems at the end. Teams that iterate run many small Vs instead, each a short design, build and test loop.[^flow-3] They also test early and continuously, with the in-the-loop methods below, rather than once at the end.[^flow-2]

## Testing before the hardware is ready: MiL, SiL, PiL and HiL

A controller can be tested long before the system it controls exists, by simulating the rest of the loop. The system being controlled is called the plant. Each stage makes one more part real:

| Stage | The controller is | The plant is | What it catches |
| --- | --- | --- | --- |
| Model-in-the-loop (MiL) | A model | A model | Mistakes in the control design itself[^ni-hil] |
| Software-in-the-loop (SiL) | Code, running as a separate process on a desktop computer | A model | Differences between the model and the code, found by comparing their results[^mathworks-sil] |
| Processor-in-the-loop (PiL) | Code, running on the target processor | A model | Differences from the target's compiler and arithmetic, and execution time, which PiL measures[^mathworks-pil] |
| Hardware-in-the-loop (HiL) | The real controller hardware, with its real inputs and outputs | A model, running in real time on a test system | Timing, wiring and signal problems, and the controller's response to faults[^mathworks-hil] |

In HiL, the plant model runs in real time, so the controller sees realistic timing.[^mathworks-hil] After HiL comes testing on the real system, on a test stand such as an e-axle {gloss}`dyno <dynamometer>`.

In HiL, only the controller is real, so faults that would damage the plant are safe to apply: a short that would destroy a real motor is an input to the plant model. HiL can start before the whole system exists, and it repeats edge cases and faults exactly.[^ni-hil]

The dyno's own control software is tested close to SiL. Its tests run the stand's state machine against fake motor controllers and a fake power supply, on a laptop, before the software ever drives a motor. The fakes are simple stand-ins, not a full plant model.

## Where tests come from

### Requirements

Each requirement names how it will be checked: by test, analysis, demonstration or inspection.[^nasa-verification] Each requirement checked by test needs at least one test case, and a review should ask whether every requirement traces to one.[^fhwa-vee] NASA records the results in a requirements compliance or verification matrix, which keeps the link between each requirement and its results.[^nasa-verification] See [Systems engineering](systems-engineering.md) for writing requirements.

### Failure modes

An FMEA lists how each part can fail, and how each failure is prevented or detected. Each prevention or detection measure is a claim that needs a test. A design FMEA leads to design tests that cause each failure on purpose, such as unplugging a sensor to show the stand trips. A process FMEA leads to production tests that catch each build defect, such as a missing seal. See the [FMEA example](systems-engineering.md#worked-example-fmea-rows-for-two-stands).

### Limits on what you can test

Some requirements can't be tested the way they're written, or not at a cost that makes sense:

- **What you can measure.** The dyno has no torque sensor, so a requirement on shaft torque needs a sensor added, or an analysis from motor current.
- **What's safe to do.** Design tests can push a unit to failure. Production tests mustn't damage a good unit.
- **Time and cost.** A production test that takes an hour per unit sets the production rate.
- **Access.** Some points can only be tested before assembly closes them up.

## Designing a test

A test applies a {gloss}`stimulus <stimulus and response>` to the DUT and measures its response. To design one, decide:

1. **The question.** Design or production, and which requirement or failure mode.
2. **The stimulus.** What you apply, at what levels, and in what order.
3. **The response.** Which channels you record, at what rate and accuracy. See [Measurement quality](measurement-quality.md).
4. **The criteria.** For a pass or fail test, the limits. For a characterization, the data you need.
5. **The conditions.** Temperature, warm-up, and the {gloss}`steady state` you wait for before you record.

### Design of experiments

When several inputs matter, plan the test points in advance. Design of experiments (DOE) is a method for choosing those test points.[^nist-doe]

The dyno's sequence is a simple planned experiment. It has two inputs, speed and load. It runs every combination of 5 speeds and 3 loads, 15 test points in all, which is called a full factorial. With more inputs, a full factorial grows fast, and DOE gives smaller designs that still separate each input's effect. [Statistical analysis and DOE](statistical-analysis.md#design-of-experiments) covers those designs, and how to randomize, replicate and block the dyno's test points.

### Worked example: one requirement, two tests

The fluids panel's proof and leak branch fills a vessel, seals it, and watches its pressure fall. Suppose the vessel has this requirement:

> The vessel shall lose no more than 1 psig in 60 s, after being filled to 72 psig and sealed.

The design test and the production test both use that procedure, but answer different questions:

| | Design test | Production test |
| --- | --- | --- |
| Units | A few vessels from the first build | Every vessel |
| Conditions | Several fill pressures and temperatures, to find the margin | 72 psig at room temperature |
| Duration | Long holds, to see the full leak curve | 60 s |
| Result | The leak rate against pressure and temperature, and the margin to 1 psig | Pass or fail for each vessel, with its pressure drop |

Run the production test on a golden vessel and on a known leaky one before you trust it. Then, across every vessel tested, watch the trend of the pressure drop: a slow rise across many passing units warns of a process problem before units start to fail.

## Further reading

- NASA, [5.3 Product Verification](https://www.nasa.gov/reference/5-3-product-verification/), NASA Systems Engineering Handbook.
- NASA, [GSFC-STD-7000B, General Environmental Verification Standard (GEVS)](https://standards.nasa.gov/sites/default/files/standards/GSFC/B/0/gsfc-std-7000b_signature_cycle_04_28_2021_fixed_links.pdf), for qualification, protoflight and acceptance testing of spacecraft.
- US Federal Highway Administration, [Systems Engineering for ITS: Integration and System Verification](https://ops.fhwa.dot.gov/seits/sections/section3/3_3_9.html), on the V-model.
- NI, [What Is Hardware-in-the-Loop (HIL)?](https://www.ni.com/en/solutions/transportation/hardware-in-the-loop/what-is-hardware-in-the-loop-.html), on MiL, SiL and HiL.
- NIST/SEMATECH, [e-Handbook of Statistical Methods: Process Improvement](https://www.itl.nist.gov/div898/handbook/pri/section1/pri11.htm), on design of experiments.

## References

[^nasa-verification]: NASA, ["5.3 Product Verification"](https://www.nasa.gov/reference/5-3-product-verification/), NASA Systems Engineering Handbook. Retrieved 2026-11-12.
[^gevs]: NASA Goddard Space Flight Center, ["GSFC-STD-7000B: General Environmental Verification Standard (GEVS)"](https://standards.nasa.gov/sites/default/files/standards/GSFC/B/0/gsfc-std-7000b_signature_cycle_04_28_2021_fixed_links.pdf), 2021. Retrieved 2026-11-12.
[^keysight-golden]: Keysight Technologies, ["Identify Potential Golden Units using Part Average Testing and Process Capability Index Technique"](https://www.keysight.com/us/en/assets/3121-1439/white-papers/Identify-Potential-Golden-Units-using-Part-Average-Testing-and-Process-Capability-Index-Technique.pdf), white paper 3121-1439. Retrieved 2026-11-12.
[^formlabs]: Formlabs, ["Validation Testing in Product Development: From POC to EVT, DVT, PVT, and Mass Production"](https://formlabs.com/global/blog/validation-testing-product-development-poc-evt-dvt-pvt-mp/). Retrieved 2026-11-12.
[^fhwa-vee]: US Federal Highway Administration, ["3.3.9 Integration and System Verification"](https://ops.fhwa.dot.gov/seits/sections/section3/3_3_9.html), Systems Engineering for Intelligent Transportation Systems. Retrieved 2026-11-12.
[^flow-3]: Flow Engineering, ["The Iterative Systems Engineering Handbook, Volume III: In Practice"](https://www.flowengineering.com/handbook/iterative-systems-engineering/volume-3). Retrieved 2026-11-12.
[^flow-2]: Flow Engineering, ["The Iterative Systems Engineering Handbook, Volume II: Leadership in Agile"](https://www.flowengineering.com/handbook/iterative-systems-engineering/volume-2). Retrieved 2026-11-12.
[^ni-hil]: NI, ["What Is Hardware-in-the-Loop (HIL)?"](https://www.ni.com/en/solutions/transportation/hardware-in-the-loop/what-is-hardware-in-the-loop-.html), updated 2026-08-04. Retrieved 2026-11-12.
[^mathworks-sil]: MathWorks, ["Software-in-the-Loop Simulation"](https://www.mathworks.com/help/ecoder/software-in-the-loop-sil-simulation.html), Embedded Coder documentation. Retrieved 2026-11-12.
[^mathworks-pil]: MathWorks, ["Processor-in-the-Loop Simulation"](https://www.mathworks.com/help/ecoder/processor-in-the-loop.html), Embedded Coder documentation. Retrieved 2026-11-12.
[^mathworks-hil]: MathWorks, ["What Is Hardware-in-the-Loop (HIL)?"](https://www.mathworks.com/discovery/hardware-in-the-loop-hil.html). Retrieved 2026-11-12.
[^nist-doe]: NIST/SEMATECH, ["What is experimental design?"](https://www.itl.nist.gov/div898/handbook/pri/section1/pri11.htm), e-Handbook of Statistical Methods, section 5.1.1. Retrieved 2026-11-12.
