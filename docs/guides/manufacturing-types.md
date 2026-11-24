# Manufacturing types

{.lead}
Manufacturing comes in three types: discrete, batch and continuous. Each gives its product a different kind of identity, so each needs a different way to link a test result to what was tested.

## Discrete, batch and continuous

NIST describes the three types this way:[^nist-82r2]

- **Discrete** manufacturing carries out "a series of steps on a single device to create the end product", such as assembling electronic and mechanical parts, or machining parts. Each unit "maintains its unique identity" as it moves between workstations.[^nist-discrete]
- **Batch** processes "have distinct processing steps, conducted on a quantity of material", with a distinct start and end. Food manufacturing is a typical example.
- **Continuous** processes "run continuously, often with transitions to make different grades of a product", as in a refinery or a chemical plant's distillation.

Each type gives its product a different identity, and test results follow that identity:

| | Discrete | Batch | Continuous |
| --- | --- | --- | --- |
| The product | Separate units | A quantity of material made together | A stream with no natural breaks |
| Identified by | A serial number on each unit | A batch or lot number | A window of time or quantity, or the coil or reel it's wound onto |
| Examples | An e-axle, a pressure vessel | Food, drugs, chemicals | Refined fuel, rolled aluminum sheet |
| A test result belongs to | One unit | The batch, through samples taken from it | A stretch of time or length of the product |

US drug regulations show the difference in their definitions. A batch is a quantity "produced according to a single manufacturing order during the same cycle of manufacture." For a continuous process, a lot is instead "a specific identified amount produced in a unit of time or quantity".[^cfr-210-3]

Many factories mix the types: "Some facilities are a hybrid of discrete and process-based manufacturing."[^nist-82r2] The same product can be made by batch or by continuous processes.[^chappell]

## ISA-95: one model for all three

{gloss}`ISA-95`, published internationally as IEC 62264, is the standard for connecting a factory's control systems to its business systems. It uses the same object models for all three types, for equipment, physical assets and materials,[^opc-10030-material] and for the tests of each.[^b2mml-test] Where the types differ, ISA-95 changes the names of the lowest levels of equipment:[^opc-10030]

| Type | Lowest equipment levels |
| --- | --- |
| Discrete | Production lines and work cells |
| Batch | Process cells, and the units in them |
| Continuous | Production units, and the units in them |

So the three types can share one data model. What differs is the identity each test result is keyed to.

### Levels

ISA-95 splits a factory's systems into five levels:[^opc-10030-levels]

| Level | What it covers |
| --- | --- |
| 0 | The physical process |
| 1 | Sensors and actuators |
| 2 | Automation and control systems, such as PLCs, which respond in under a second |
| 3 | Manufacturing operations management, including quality assurance and laboratory functions, on timescales from days down to seconds |
| 4 | Business planning and logistics, on timescales from months to days |

A test stand spans levels 1 to 3. Its sensors and actuators are level 1, its controller and {gloss}`DAQ <Data acquisition (DAQ)>` are level 2, and the test results it reports for each unit feed level 3. ISA-95 names "quality tests and test labs" as one of four parts of an organization that level 3 coordinates, with production, inventory and maintenance.[^opc-10030-ops] The {gloss}`MES <Manufacturing execution system (MES)>` is level 3 software.

### Material lots

ISA-95 describes material at three levels: a class identifies a material "without regard to the source", a definition identifies it from a specific vendor or source, and a {gloss}`lot` "identifies actual material, its location and quantity".[^opc-10030-ops] A sublot gives finer tracking within a lot, such as one of the ten barrels a lot arrived in.[^opc-10030-material]

A lot can be "assembled from other Material Lots and/or Material Sublots", so lots form a tree from raw material to finished product. ISA-95 names the purpose: "to trace all materials used in the manufacture of a product to aide in quality analysis and product recalls."[^opc-10030-material]

### Equipment and physical assets

ISA-95 separates a piece of equipment, which is a role, from the physical asset that fills it. Its example: temperature transmitter TT-101 has serial number X2 one day. The next day it's swapped for an identical transmitter, X3, which then becomes TT-101.[^opc-10030-ops] ISA-95's OPC UA model keeps a history of which physical asset filled each role, and when, so you can find every physical asset that served as a piece of equipment.[^opc-10030-assets]

A test stand works the same way. The stand's pressure channel, `p_1`, is a role. The transducer behind it has a serial number, and it gets sent out for {gloss}`calibration` and replaced. Record which serial number filled `p_1` during each test, and you can trace any result back to the instrument that measured it.

## How test data attaches

ASAM ODS, a standard for storing test data, says test data "can only be understood and applied correctly" if you know where the data is, what was tested, what test equipment was used, which test was performed, and when.[^asam-ods] What changes between the types is the answer to "what was tested".

### Discrete: one record per unit

In discrete manufacturing, each unit has its own test record. The IPC Connected Factory Exchange standard, for example, reports test results with each unit's identifier, every measured value, its limits, and a pass or fail.[^ipc-cfx] An end-of-line test produces one such record for every unit. See [Test design](test-design.md#two-questions-a-test-can-answer).

Fast discrete lines can still need time windows. Where high-speed machines assemble components, SAP's manufacturing software tracks the material and every unit that passed through the machine over time, rather than unit by unit.[^sap-time-genealogy]

### Batch: samples stand in for the batch

A batch is meant to be uniform, so you test samples and judge the whole batch from them. In acceptance sampling, "a sample should be picked at random from the lot, and on the basis of information that was yielded by the sample, a decision should be made regarding the disposition of the lot."[^nist-sampling]

Each result then belongs to the batch. MESA's batch production record schema stores samples, the tests run on each sample, and their results, with the equipment and physical asset that ran each test.[^batchml] US drug regulations require each batch's record to include the equipment used, the in-process and laboratory results, and any sampling performed.[^cfr-211-188]

### Continuous: time first, then length

A continuous line records its data against time. To know which part of the product a measurement describes, you convert time to position. In aluminum sheet production, machines record data "in a time-based manner", and the work is to "assign the time-based records to the related section of the alloy sheet (length-based)."[^haidenthaler] Thickness profiles and surface defects "require length-related assignment".[^ascospeed]

Position comes from measuring how fast the material moves, so speed errors become position errors. For a 3,000 m coil, a ±1% error in measured length puts a defect anywhere within ±30 m.[^ascospeed]

The identity of a continuous product is defined after the fact. In continuous drug manufacturing, a batch can be defined by the quantity of material in or out, or by "run time at a defined mass flow rate". Knowing how material moves through the process "allows input materials to be traced throughout production."[^ich-q13]

## Genealogy

{gloss}`Genealogy` is the record of what went into each product, and what each material and machine went into. Trace it in two directions:

- **Backward**, from a finished product to its materials, and to the equipment that made and tested it.
- **Forward**, from a material lot or a piece of equipment to every product it touched.

Both directions use the same links. Store, for each product, the identities of what went into it and what tested it, and you can answer either question. A US drug lot number is defined by exactly this: the identifier "from which the complete history of the manufacture, processing, packing, holding, and distribution" can be determined.[^cfr-210-3]

## In Nominal

Nominal's data model describes physical things as [assets](https://dev.nominal.io/platform/reference/glossary/#asset), and an asset can be "a device/unit under test (DUT/UUT) or the reverse, a test station or harness." A {gloss}`run` is "a labeled time range", and properties are key-value pairs such as a serial number.[^nominal-data-model]

Each type maps onto those:

- **Discrete units tested on a production line.** Use one dataset for each tester or for the whole line, and tag every point with its unit and its tester. Each unit's asset then filters the dataset to its own data, and you can review everything one tester gathered.[^nominal-tagged]
- **Components that move between systems.** Tag each component's data with both its own identifier and its system's, so each has a history across every system it's been in.[^nominal-assemblies]
- **Batches and continuous lots.** Record the batch or lot number as a property. For a continuous line, a run can mark the span of time that became one coil or one lot.

## Worked example: tracing an e-axle

Suppose an e-axle {gloss}`dyno <dynamometer>` tests e-axles in production. An e-axle is discrete, with a serial number. It's also made from materials of the other types, so its genealogy mixes all three:

| Input | Type | Identified by |
| --- | --- | --- |
| The e-axle | Discrete | Its serial number |
| The gear oil in its gearbox | Batch | The oil's lot number |
| The steel its motor's laminations were stamped from | Continuous | The coil, and where along it the laminations came from |
| The dyno that tested it, and each instrument on the dyno | Physical assets | Their serial numbers, during the run |

Three questions show what the records have to hold:

1. **An e-axle fails its dyno test. What went into it?** Look up the oil lot, the coil and the instruments on its record. This is a backward trace.
2. **An oil lot fails its lab test after shipping. Which e-axles contain it?** Find every e-axle whose record names that lot. This is a forward trace, and it needs the same link as the first question, read the other way.
3. **The instrument measuring the dyno's bus current is found out of calibration. Which results does that affect?** Find its last good calibration, then every e-axle tested on the dyno while that instrument filled the bus current role.

In Nominal, give each e-axle an asset, with its serial number, oil lot and coil as properties. Tag the dyno's data with the e-axle's serial number and the dyno's identifier, and add a run for each test. Give each run a property for each instrument's serial number, so every test's record names the instruments that measured it.

## Further reading

- OPC Foundation, [OPC 10030: OPC UA for ISA-95 Common Object Model](https://reference.opcfoundation.org/specs/OPC-10030/4.2.2), a public summary of the ISA-95 models.
- MESA International, [B2MML and BatchML](https://github.com/MESAInternational/B2MML-BatchML), XML schemas that implement ISA-95 and ISA-88.
- ICH, [Q13: Continuous Manufacturing of Drug Substances and Drug Products](https://database.ich.org/sites/default/files/ICH_Q13_Step4_Guideline_2022_1116.pdf), on batches and traceability in continuous manufacturing.
- NIST/SEMATECH, [e-Handbook of Statistical Methods: Acceptance sampling](https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc21.htm).
- Nominal, [Data model core concepts](https://dev.nominal.io/platform/data-model/), with approaches for long-lived units, production testers and nested assets.

## References

[^nist-82r2]: K. Stouffer et al., NIST, ["Guide to Industrial Control Systems (ICS) Security"](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-82r2.pdf), SP 800-82 Rev. 2, section 2.2.1, May 2015. Superseded by Rev. 3. Retrieved 2026-11-19.
[^nist-discrete]: NIST, ["Discrete process"](https://csrc.nist.gov/glossary/term/discrete_process), CSRC glossary, from SP 800-82r3. Retrieved 2026-11-19.
[^cfr-210-3]: US Code of Federal Regulations, [21 CFR 210.3, Definitions](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-210/section-210.3), paragraphs (b)(2), (b)(10) and (b)(11). Retrieved 2026-11-19.
[^chappell]: D. Chappell, Procter & Gamble, ["Batch Techniques Benefit Continuous Processes"](https://www.controlglobal.com/articles/2003/181), *Control*, 2003-09-04. Retrieved 2026-11-19.
[^opc-10030]: OPC Foundation, ["OPC 10030: OPC UA for ISA-95 Common Object Model"](https://reference.opcfoundation.org/specs/OPC-10030/7.4.1), version 1.00, section 7.4.1, 2013-11-06. Retrieved 2026-11-19.
[^b2mml-test]: MESA International, `B2MML-OperationsTest.xsd` in [B2MML-BatchML](https://github.com/MESAInternational/B2MML-BatchML), version 0701, based on ANSI/ISA-95.00.02-2018. Retrieved 2026-11-19.
[^opc-10030-levels]: OPC Foundation, ["OPC 10030: OPC UA for ISA-95 Common Object Model"](https://reference.opcfoundation.org/specs/OPC-10030/4.2.3), version 1.00, section 4.2.3. Retrieved 2026-11-19.
[^opc-10030-ops]: OPC Foundation, ["OPC 10030: OPC UA for ISA-95 Common Object Model"](https://reference.opcfoundation.org/specs/OPC-10030/4.2.2), version 1.00, section 4.2.2. Retrieved 2026-11-19.
[^opc-10030-material]: OPC Foundation, ["OPC 10030: OPC UA for ISA-95 Common Object Model"](https://reference.opcfoundation.org/specs/OPC-10030/4.2.4), version 1.00, section 4.2.4. Retrieved 2026-11-19.
[^opc-10030-assets]: OPC Foundation, ["OPC 10030: OPC UA for ISA-95 Common Object Model"](https://reference.opcfoundation.org/specs/OPC-10030/8.2.3.1), version 1.00, section 8.2.3.1. Retrieved 2026-11-19.
[^asam-ods]: ASAM, ["ASAM ODS"](https://www.asam.net/standards/detail/ods/wiki/), standard wiki. Retrieved 2026-11-19.
[^ipc-cfx]: IPC, ["UnitsTested"](https://ipcconnectedfactoryexchange.github.io/CFX/html/T_CFX_Production_TestAndInspection_UnitsTested.htm), IPC-CFX (IPC-2591) SDK reference. Retrieved 2026-11-19.
[^sap-time-genealogy]: SAP, ["Time-Based Genealogy"](https://help.sap.com/saphelp_me60/helpdata/EN/57/1880d833eb4789a3fdf9f2bbb58ab4/content.htm), SAP ME 6.0 documentation. Retrieved 2026-11-19.
[^nist-sampling]: NIST/SEMATECH, ["What is Acceptance Sampling?"](https://www.itl.nist.gov/div898/handbook/pmc/section2/pmc21.htm), e-Handbook of Statistical Methods, section 6.2.1. Retrieved 2026-11-19.
[^batchml]: MESA International, BatchML Batch Production Record schema and documentation in [B2MML-BatchML](https://github.com/MESAInternational/B2MML-BatchML), schema version 0701, based on ANSI/ISA-88.00.04. Retrieved 2026-11-19.
[^cfr-211-188]: US Code of Federal Regulations, [21 CFR 211.188, Batch production and control records](https://www.ecfr.gov/current/title-21/chapter-I/subchapter-C/part-211/subpart-J/section-211.188). Retrieved 2026-11-19.
[^haidenthaler]: Haidenthaler et al., ["Proper Material Tracking for a Continuous Aluminum Production Process"](https://www.scientific.net/KEM.968.153), *Key Engineering Materials* 968, 153–160, 2023, abstract. Retrieved 2026-11-19.
[^ascospeed]: Christofori, Füßer and Gorzny, ["Certified material tracking with ASCOspeed"](https://tb-sensor.com/assets/fachartikel-aluminium-2021-04.pdf), *ALUMINIUM* 97, 4/2021. Retrieved 2026-11-19.
[^ich-q13]: ICH, ["Q13: Continuous Manufacturing of Drug Substances and Drug Products"](https://database.ich.org/sites/default/files/ICH_Q13_Step4_Guideline_2022_1116.pdf), Step 4, sections 2.2 and 3.1.6, 2022-11-16. Retrieved 2026-11-19.
[^nominal-data-model]: Nominal, ["Data model core concepts"](https://dev.nominal.io/platform/data-model/). Retrieved 2026-11-19.
[^nominal-tagged]: Nominal, ["Using a single dataset for many identical assets"](https://dev.nominal.io/platform/data-model/organization/tagged-data/). Retrieved 2026-11-19.
[^nominal-assemblies]: Nominal, ["Complex and nested assets"](https://dev.nominal.io/platform/data-model/organization/assemblies/). Retrieved 2026-11-19.
