# Systems engineering

{.lead}
Systems engineering keeps a system's parts working together, by stating what the system has to do, how its parts connect, and how it can fail. Each of these feeds [test design](test-design.md).

## Requirements

A {gloss}`requirement` states what a system has to do or be, not how to do it. Requirements use a fixed vocabulary:[^nasa-requirements]

- **Shall** marks a requirement.
- **Will** marks a fact or a statement of purpose.
- **Should** marks a goal.

### What makes a good requirement

NASA's checklist for a good requirement includes these:[^nasa-requirements]

- **One thought.** Each statement says one thing, so it passes or fails as one.
- **What, not how.** It states the need, and leaves the design open.
- **Verifiable.** Someone can test, demonstrate, inspect or analyze the system to show it meets the requirement. Words like "flexible", "robust" and "user-friendly" can't be verified.
- **Traceable.** It links to the higher-level requirement it comes from.
- **Reasoned.** It records its rationale, including any assumptions.

### Worked example: a requirement for a dyno

Take an e-axle {gloss}`dyno <dynamometer>`, where a motor drives the e-axle under test and a load motor on each side brakes it. A first draft of a requirement for it:

> The stand shall hold speed well under load.

"Well" can't be verified, and the statement doesn't say which speeds or which loads. A better version, using the numbers from the dyno's sequence:

> The stand shall hold the DUT's speed within 50 RPM of its setpoint, for setpoints from 500 to 1,500 RPM and load torques up to 1.25 Nm, within 15 s of each setpoint change.

- **Rationale:** the sweep's data is valid only once the speed has settled.
- **Verification method:** test. The sequence checks this itself at every test point, and aborts if the speed doesn't settle in time.

### Templates for requirements

The Easy Approach to Requirements Syntax (EARS) constrains requirements to a few patterns, each with a keyword. The general form is "While <precondition>, when <trigger>, the <system> shall <response>."[^ears]

| Pattern | Keyword | Example for the dyno |
| --- | --- | --- |
| Ubiquitous | None | The stand shall limit each motor command to its channel's range. |
| State-driven | While | While the stand is armed and not running, the stand shall not send motor commands. |
| Event-driven | When | When the operator selects **Abort**, the stand shall command every motor to zero. |
| Optional feature | Where | Where a torque sensor is fitted, the stand shall record shaft torque. |
| Unwanted behavior | If … then | If a motor's temperature exceeds 100 °C while the stand is running, then the stand shall command every motor to zero and turn off the power supply. |
| Complex | A combination | While the stand is running, when a measurement leaves its allowed range, the stand shall trip. |

### Fewer, stronger requirements

More requirements don't make a better specification: "One hundred well-defined requirements are better than 100,000 minor ones."[^flow-1] Separate the hard requirements, set by the outside world, from internal design criteria that a team can change as it learns. Requirements guide the design, and the design also informs the requirements.[^flow-1] Give each requirement one owner.[^flow-2]

### Traceability

{gloss}`Traceability` links each requirement to the requirement it came from, to the requirements it was split into, and to the tests that check it. NASA calls the first two bidirectional traceability: being able to trace any requirement both to its parent and to its children.[^nasa-glossary]

Linking each requirement to its test, with the test's pass or fail history, turns a failed test into a flag on the requirement it checks, and a signal to that requirement's owner.[^flow-3] Nominal's checklists can serve as the test end of that link: link each check to the requirement it tests, and it runs on every run's data.

## Interfaces

An interface is where two parts of a system meet: mechanically, electrically, or in software and data.

### Interface control documents

An {gloss}`interface control document (ICD) <interface control document>` records an interface, so both sides build to the same definition. NASA treats interface management as crucial to a project, and the ICD as the record of each interface and its approved changes.[^nasa-interfaces]

An ICD covers what each side needs to know:

- **Physical.** Connectors, pinouts, mounting and cable lengths.
- **Electrical.** Supply voltages, signal types and ranges, and grounding.
- **Data.** The protocol, message formats, units, ranges, rates and timing.
- **Behavior.** What happens at startup, on a fault, and when a message stops arriving.
- **Ownership.** Who owns each side, and how a change is agreed.

Define interfaces early, mark the tentative parts as tentative, and make each one a testable contract: "If you can't test an interface, it doesn't really exist."[^flow-3]

### Worked example: the dyno's DUT motor controller

An ICD for the connection between the dyno's software and its DUT motor controller would hold rows like these:

| Item | Definition |
| --- | --- |
| Link | CAN bus, shared with the two load motor controllers |
| Node ID | 0 |
| Commands | A speed in mechanical RPM, from −3,000 to 3,000, or a current in A, from −35 to 35 |
| Units | The software sends mechanical RPM. The controller converts it to electrical RPM, using the motor's 4 pole pairs. |
| Command rate | About 16 commands a second. The controller stops driving the motor if no command arrives for half a second. |
| Telemetry | Speed in RPM, motor current in A, and motor temperature in °C |
| Fault values | A temperature at or below 0 °C means a missing or broken sensor, not a real temperature. |

Every row is something one side assumes about the other. A units mismatch is easy to miss: if one side used electrical RPM and the other mechanical RPM, every speed would be off by a factor of 4.

A stand's channel list is an ICD for its data. It gives each channel's name, units, range and rate, so the stand and everything that reads its data agree on what each channel means.

## Failure mode and effects analysis

A {gloss}`failure mode and effects analysis (FMEA) <failure mode and effects analysis>` lists each way each part of a system can fail, what happens as a result, and how the failure is prevented or detected. A risk assessment starts from hazards. An FMEA starts from failures.

The classic FMEA scores each failure mode from 1 to 10 for severity, occurrence and detection, and multiplies them into a risk priority number (RPN). The AIAG & VDA FMEA handbook, used in the automotive industry, replaces the RPN with an action priority (AP) of high, medium or low, and lays out a seven-step approach.[^aiag-fmea]

There are several kinds of FMEA:

- **Design FMEA (DFMEA)** analyzes how a product's design can fail.
- **Process FMEA (PFMEA)** analyzes how a manufacturing or assembly process can fail, and produce a bad part.
- **FMEA for monitoring and system response (FMEA-MSR)** analyzes how well a product's diagnostics detect a failure in use, and put it in a safe state. The AIAG & VDA handbook added it.[^aiag-fmea]
- **FMECA**, failure mode, effects and criticality analysis, also ranks each failure mode's criticality. It comes from the US military standard MIL-STD-1629A.

### Worked example: FMEA rows for two stands

These rows cover the dyno and a fluids panel, which runs compressed air through valves and pressure transducers:

| Part | Failure mode | Effect | Prevention or detection |
| --- | --- | --- | --- |
| Fluids panel vent valve, `v_1` | Stuck closed | Pressing the E-stop doesn't release the pressure | Press the E-stop and check that `p_1` falls before every session |
| Fluids panel pressure transducer, `p_1` | Broken wire | The loop current falls to 0 mA | A reading below 4 mA shows a fault rather than a believable pressure |
| Dyno CAN cable | Unplugged mid-run | Commands and telemetry stop | Each motor controller stops its motor after half a second without a command |
| Dyno motor temperature sensor | Disconnected | The reading falls to 0 °C or below | The software treats it as a fault, and trips |

Each entry in the last column is a claim that needs evidence. The E-stop check is a test, run every session. The others need a test that unplugs, disconnects or breaks something on purpose and shows the stand responds. That's how an FMEA feeds [test design](test-design.md).

## Further reading

- NASA, [Systems Engineering Handbook](https://www.nasa.gov/reference/systems-engineering-handbook/), free online.
- NASA, [Appendix C: How to Write a Good Requirement](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/).
- A. Mavin, [EARS: the Easy Approach to Requirements Syntax](https://alistairmavin.com/ears/).
- Flow Engineering, [The Iterative Systems Engineering Handbook, Volume III: In Practice](https://www.flowengineering.com/handbook/iterative-systems-engineering/volume-3).

## References

[^nasa-requirements]: NASA, ["Appendix C: How to Write a Good Requirement"](https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/), NASA Systems Engineering Handbook. Retrieved 2026-11-12.
[^ears]: A. Mavin, ["EARS: the Easy Approach to Requirements Syntax"](https://alistairmavin.com/ears/). Retrieved 2026-11-12.
[^flow-1]: Flow Engineering, ["The Iterative Systems Engineering Handbook, Volume I: Introduction & Culture"](https://www.flowengineering.com/handbook/iterative-systems-engineering/volume-1). Retrieved 2026-11-12.
[^flow-2]: Flow Engineering, ["The Iterative Systems Engineering Handbook, Volume II: Leadership in Agile"](https://www.flowengineering.com/handbook/iterative-systems-engineering/volume-2). Retrieved 2026-11-12.
[^nasa-glossary]: NASA, ["Appendix B: Glossary"](https://www.nasa.gov/reference/appendix-b-glossary/), NASA Systems Engineering Handbook. Retrieved 2026-11-12.
[^flow-3]: Flow Engineering, ["The Iterative Systems Engineering Handbook, Volume III: In Practice"](https://www.flowengineering.com/handbook/iterative-systems-engineering/volume-3). Retrieved 2026-11-12.
[^nasa-interfaces]: NASA, ["6.3 Interface Management"](https://www.nasa.gov/reference/6-3-interface-management/), NASA Systems Engineering Handbook. Retrieved 2026-11-12.
[^aiag-fmea]: AIAG, ["New AIAG & VDA FMEA Handbook and Trainings Available!"](https://blog.aiag.org/new-aiag-vda-fmea-handbook-and-trainings-available), 2019-06-13. Retrieved 2026-11-12.
