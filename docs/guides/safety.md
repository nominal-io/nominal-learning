# Safety

{.lead}
A test stand stores energy that can hurt people and destroy hardware. Hardware that works without software keeps people safe, and the control software protects the equipment.

## Two kinds of safety

{gloss}`Human safety` protects people. {gloss}`Machine safety` protects the stand and its DUT from damage.

- Human safety comes from hardware that works without software: {gloss}`fail-safe` wiring, the {gloss}`E-stop`, {gloss}`guards <guard>` and {gloss}`interlocks <interlock>`. Procedures, training and protective equipment add to it.
- Machine safety comes from the control software. It limits commands to a safe range, and it {gloss}`trips <trip>` the stand when a measurement leaves its allowed range.

Software can't keep people safe, because it can stall, crash, or lose its connection to the hardware, and software that has stopped can't stop anything else. The exception is a certified safety controller, described in [Safety controllers](#safety-controllers) below.

Safety standards use "safety of machinery" for protecting people from a machine's hazards, so read it as human safety when you meet it there.[^idec-12100]

## Hazards on a test stand

A {gloss}`hazard` is a source of possible harm. Risk combines how severe the harm would be with how likely it is, and reducing risk means reducing either one or both.[^idec-12100]

The hazards depend on the stand. Compare a fluids panel, which runs compressed air through valves and a proof and leak vessel, with an e-axle {gloss}`dyno <dynamometer>`, where a motor drives the e-axle under test and a load motor on each side brakes it:

| Hazard | Fluids panel | E-axle dyno |
| --- | --- | --- |
| Stored pressure | Compressed air in the supply line, up to about 85 psig, and in the proof and leak vessel | None |
| Moving parts | The air-driven slide | The spinning axle and the load motors |
| Stored motion | None | The axle keeps turning after its power is removed |
| Electrical energy | Control power and wiring | The 48 V DC bus, which the load motors also feed when they brake |

## The hierarchy of controls

A {gloss}`hazard control` is anything that reduces a hazard's risk. NIOSH ranks five kinds of hazard control from most to least effective, and OSHA recommends choosing them in that order:[^niosh-hoc][^osha-hpc]

1. **Elimination** removes the hazard. On these two stands, that means running a check with the fluids panel vented, or testing control software against a simulated stand instead of the hardware.
2. **Substitution** replaces the hazard with a smaller one. Test at the lowest pressure or speed that answers your question. The proof and leak branch fills its vessel to about 72 psig, below the 85 psig supply.
3. **Engineering controls** keep people away from the hazard: the E-stop, fail-safe valves, guards and interlocks.
4. **Administrative controls** change how people work: procedures, training, a safety briefing, and lockout/tagout.
5. **Personal protective equipment (PPE)** is worn to reduce exposure, such as safety glasses. Use it with the other controls, not instead of them.

Where no single control protects people enough, combine them. A control mustn't add a hazard of its own, such as hearing protection that stops someone hearing an alarm.[^osha-hpc]

Software trips aren't on this list. They protect the equipment, not people.

## Engineering controls

### Fail-safe design

A fail-safe design puts the stand in its safe state when something fails, such as a power loss or a broken wire. Make the running state the one that needs power. Then losing power, for any reason, puts the stand back in its safe state.

The fluids panel's main vent valve, `v_1`, works this way. It's {gloss}`normally open <normally open>`: it needs power to stay closed and hold pressure. Press the E-stop, lose power, or cut the valve's wire, and it opens and releases the air.

### Emergency stop

An E-stop stops the stand through hardware, without software. Pressing it removes power from the actuators, and the stand stays stopped until someone resets the E-stop by releasing the button.[^idec-13850]

An E-stop is a complementary protective measure: it backs up guards and other controls, and doesn't replace them.[^idec-13850] It's for emergencies, when someone has already seen a problem.

IEC 60204-1 defines three ways a machine can stop, and an E-stop has to use category 0 or 1:[^idec-60204]

| Stop category | What happens |
| --- | --- |
| 0 | Power is removed from the actuators at once. |
| 1 | The machine makes a controlled stop with power available, then power is removed. |
| 2 | The machine makes a controlled stop, and power stays available afterwards. |

The dyno's **Abort** button isn't an E-stop. It's a software stop, so it works only while the control software runs.

### Guards and interlocks

A guard is a physical barrier between people and a hazard. OSHA requires guarding against hazards such as rotating parts, and requires that the guard isn't a hazard itself.[^osha-1910-212] The dyno has a guard around its moving parts.

An interlock checks a condition before it allows an action, or stops the stand when the condition changes. An interlocked guard has a switch that stops the machine when the guard opens. A hardware interlock, wired fail-safe, is an engineering control for human safety. A software interlock protects only the machine.

### Safety controllers

A safety controller is hardware built and certified to carry out safety functions, such as removing power when an E-stop is pressed or a guard opens. A safety relay does one fixed function. A safety PLC is programmable.

ISO 13849-1 rates how reliably the safety-related parts of a control system perform a safety function, as a performance level (PL) from PL a, the lowest, to PL e, the highest. Each level is a band of probability of a dangerous failure per hour. A risk assessment sets the required level, PLr, that a machine's safety function has to reach. IEC 62061 rates the same thing as a safety integrity level (SIL).[^sick-pl]

Ordinary control software, such as a Python program that runs a stand, has no such rating.

## Administrative controls

Administrative controls depend on people following them, so they back up engineering controls. On a test stand, they can include:

- A safety briefing, where everyone is shown each E-stop.
- A rule that anyone may press an E-stop without asking.
- An E-stop test before each session.

### Lockout/tagout

Lockout/tagout (LOTO) protects people working on a machine from it starting unexpectedly, or releasing stored energy, while they work.[^osha-1910-147] OSHA's regulation sets the order of the steps:[^osha-1910-147]

1. Prepare for shutdown.
2. Shut the machine down.
3. Isolate it from every energy source.
4. Put a lock or tag on each energy isolating device.
5. Relieve, disconnect or restrain any stored energy.
6. Verify the isolation before starting work.

On the fluids panel, step 5 means venting the air until `p_1` and `p_2` read 0 psig. On the dyno, it means waiting until the axle has stopped turning.

Pressing an E-stop isn't lockout. Anyone can release it.

## Machine safety

The dyno protects its hardware in four ways, three in the control software and one in the motor controllers:

- **Command limits.** Each command is clamped to its channel's range before it's sent. Ask the DUT for 50 A and it gets its 35 A maximum.
- **Trips.** Every measured channel has an allowed range, such as up to 100 °C for each motor's temperature. If a measurement leaves its range while the stand runs, the software commands every motor to zero and turns off the power supply. It won't run again until every measurement is back in range.
- **A software interlock.** The software sends motor commands only in its RUNNING, STOPPING and TRIP_STOPPING states.
- **A watchdog in the hardware.** The software resends every motor command about 16 times a second. A motor controller that hears nothing for half a second stops driving its motor, so crashed software can't leave a motor running.

## Which control covers which failure

| Failure | What protects against it | Kind of safety |
| --- | --- | --- |
| A command asks for more than a channel allows | A command limit in the control software | Machine safety |
| A measurement leaves its allowed range | A trip in the control software | Machine safety |
| The control software crashes or loses its connection | A watchdog in the hardware, such as in the dyno's motor controllers | Machine safety |
| Power is lost | Fail-safe hardware, such as the fluids panel's normally open vent valve | Human safety |
| A person is in danger, or a stand does something unexpected | The E-stop, wired fail-safe | Human safety |
| A person could reach a moving or pressurized part | Guards and interlocks | Human safety |
| Someone works on the stand | Lockout/tagout | Human safety |

## Worked example: the control software crashes mid-sweep

The dyno is partway through its speed sweep, with the DUT at 1,000 RPM and both load motors braking, when the control software crashes.

Motor commands stop arriving, and within half a second each motor controller's watchdog stops driving its motor. The axle coasts down. No trip runs, because the software that runs trips has stopped. Nothing turns off the power supply, which holds its setpoint on its own, so the 48 V bus stays live. The guard keeps people away from the coasting axle, and if anyone is at risk, the E-stop removes power through hardware, whether or not the software runs.

Before running again, find out why the software crashed, and check the stand.

## Further reading

- OSHA, [Machine Guarding eTool](https://www.osha.gov/etools/machine-guarding), on recognizing and controlling amputation hazards.
- OSHA, [29 CFR 1910.147, The control of hazardous energy (lockout/tagout)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147), the full regulation.
- NIOSH, [Hierarchy of Controls](https://www.cdc.gov/niosh/hierarchy-of-controls/about/index.html).
- NASA, [NASA-STD-8719.17, Ground-Based Pressure Vessels and Pressurized Systems](https://standards.nasa.gov/standard/NASA/NASA-STD-871917), for pressure systems.
- IDEC, [summaries of the machinery safety standards](https://www.idec.com/en-eu/solutions/safety/law/iso-iec/iso12100), including ISO 12100, ISO 13850 and IEC 60204-1.

## References

[^idec-12100]: IDEC, ["Basic Safety Standard: ISO 12100"](https://www.idec.com/en-eu/solutions/safety/law/iso-iec/iso12100). Retrieved 2026-11-12.
[^niosh-hoc]: NIOSH, ["About Hierarchy of Controls"](https://www.cdc.gov/niosh/hierarchy-of-controls/about/index.html). Retrieved 2026-11-12.
[^osha-hpc]: OSHA, ["Hazard Prevention and Control"](https://www.osha.gov/safety-management/hazard-prevention), Recommended Practices for Safety and Health Programs. Retrieved 2026-11-12.
[^idec-13850]: IDEC, ["ISO 13850"](https://www.idec.com/en-eu/solutions/safety/law/iso-iec/iso13850), on the safety requirements for emergency stop devices. Retrieved 2026-11-12.
[^idec-60204]: IDEC, ["IEC 60204-1"](https://www.idec.com/en-ca/solutions/safety/law/iso-iec/iec60204), on stop categories and the emergency stop function. Retrieved 2026-11-12.
[^osha-1910-212]: OSHA, [29 CFR 1910.212, General requirements for all machines](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.212). Retrieved 2026-11-12.
[^sick-pl]: SICK, ["What are performance levels?"](https://www.sick.com/us/en/blog/what-are-performance-levels/w/blog-safety-standard-performance-levels), 2022. Retrieved 2026-11-12.
[^osha-1910-147]: OSHA, [29 CFR 1910.147, The control of hazardous energy (lockout/tagout)](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.147). Retrieved 2026-11-12.
