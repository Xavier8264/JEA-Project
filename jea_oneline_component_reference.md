# JEA Power Delivery One-Line: Exhaustive Component Reference

**Purpose:** component-by-component breakdown of the JEA power delivery one-line, the practical distinctions between delivery points and the various substation types, and a mapping of which devices actually participate during a fault.

**Sources used:** `jea_power_delivery_oneline_reference.md`, `jea_power_delivery_oneline.png`, `JEA_Preliminary_Presentation.txt` (Zach Wadley's PDR deck narration), `JEA_Senior_Design_Scope_of_Work.docx`, `JEA_Meeting_Transcript_8_27.txt`, SEL-2240 Axion data sheet, plus vendor documentation for the ABB R-MAG and G&W Viper-ST.

**Confidence convention used throughout:**
- **[V]** Verified against a primary source (vendor datasheet, standard, or a direct JEA statement in the project files).
- **[S]** Standard industry practice, near-universally true, but not confirmed for JEA specifically.
- **[I]** Inference. Could be wrong. Flagged for Zach.

---

## 0. Read this first: the framing trap

There are two different questions that look like one question.

**Question A: how many protection and isolation mechanisms exist on JEA's real system between TVA generation and a customer meter?**
Answer: roughly five nested layers, spanning four ownership tiers, involving on the order of a dozen distinct device types.

**Question B: how many fault isolation mechanisms will exist in the tabletop trainer?**
Answer: whatever you decide, bounded by table area, digital output count, and demo legibility. The real one-line does not set this number.

The trainer models **one tier only**: 12,470Y/7,200 V primary distribution. Everything at 46 kV and above is context you narrate, not hardware you build. Confusing the two produces either a bloated build or a false sense that the design is "already specified" by JEA. It is not. Section 7 answers Question B with a concrete count.

A second distinction that matters more than most people realize: **"isolation device" is not one category.** There are five functional roles, and lumping them together will corrupt your I/O math and your FLISR logic. Section 5 defines them.

---

## 1. Voltage tiers, end to end

| Tier | Voltage | Owner | Configuration | Conf. |
|---|---|---|---|---|
| Generation (generator terminals) | 13.8 to 24 kV | TVA | 3-phase | [S] |
| Generator step-up (GSU) output | 161 kV or 500 kV | TVA | 3-phase | [S] |
| Bulk transmission | 500 kV, 161 kV (also 115, 69) | TVA | Meshed, NOT radial | [V] |
| Delivery point | 161 kV | TVA / JEA boundary | Metering and ownership demarcation | [V] |
| Subtransmission | 46 kV | JEA | Loop or radial, unconfirmed | [V] voltage, [I] config |
| Primary distribution | 12,470Y/7,200 V | JEA | Physically looped, operationally radial | [V] |
| Utilization / service | 600 V and below | Customer | See Section 4.7 | [V] |

**Notes on the tiers:**

- 7,200 V is the line-to-neutral value of a 12,470 V line-to-line wye system. 12470 / sqrt(3) = 7200. A single-phase lateral serving houses runs at 7.2 kV against neutral, not 12.47 kV. This matters for the trainer: if you ever render a single-phase lateral, it is one hot conductor plus neutral, not three. [V]
- JEA operating 46 kV subtransmission is unusual. Zach states directly that the more common LPC value is 69 kV and that JEA's is 46 kV. [V]
- TVA does not operate 345 kV. If any reference diagram shows 345 kV, it is not TVA territory and should be corrected. [S]
- JEA system scale: approximately 35,000 customers, 29 substation locations, 53 power transformers, 700+ miles of distribution and transmission line, roughly $300M in plant before depreciation. [V]

---

## 2. Component catalog: generation and transmission tier

These are context only. None of them appear in the trainer. They exist so that a trainee understands where the power on the tabletop comes from.

### 2.1 Generating unit
- **Function:** converts thermal, nuclear, or hydro energy into 3-phase AC at 13.8 to 24 kV.
- **Looks like:** a synchronous generator with an exciter, physically a cylinder tens of feet long inside a turbine hall. Not a field-visible object.
- **Owner:** TVA. TVA serves roughly 100+ LPCs across Tennessee, Kentucky, Virginia, Georgia, Alabama, Mississippi, and North Carolina. [V]
- **In play during a distribution fault:** no. A 12.47 kV fault is electrically invisible at the generator.

### 2.2 Generator step-up transformer (GSU)
- **Function:** steps generator terminal voltage (about 20 kV) up to transmission voltage (161 kV or 500 kV). One transformer per unit, delta-wye typically.
- **Looks like:** a large oil-filled tank with radiator banks and tall porcelain or composite bushings on top, sited immediately adjacent to the generator building.
- **Key point for your one-line:** a GSU is a *dedicated, unit-connected* transformer. There is no tie between GSUs. Your reference notes already flag this correctly. A bus tie belongs between distribution buses, never between GSU transformers. [V, confirmed correct in prior review]
- **In play during a distribution fault:** no.

### 2.3 Transmission line (161 kV / 500 kV)
- **Function:** bulk power transfer.
- **Looks like:** steel lattice or tubular steel towers, bundled ACSR conductor, 75 to 200 ft rights of way (500 kV typically 175 to 200 ft). [V]
- **Critical structural property:** the transmission network is **meshed**, not radial. Power can reach any point by multiple paths. This is the single biggest topological difference between transmission and distribution, and it is why transmission uses distance and differential protection rather than time-overcurrent coordination.
- **In play during a distribution fault:** no, except as an infinite-source assumption for fault current calculation.

### 2.4 Transmission interconnection (cross-tie 1 on the diagram)
- **Function:** ties TVA's network to neighboring utilities and to other LPCs.
- **Practical significance:** it is why "loss of a single source" almost never means "loss of all power" at transmission level.
- **In trainer scope:** no.

---

## 3. The delivery point and the substation family: distinctions

This is the section where the current one-line diagram is weakest, so read it carefully.

### 3.1 The core distinction

**A delivery point is a commercial and ownership concept. A substation is a physical facility.** They are not the same category of thing, and drawing them as two adjacent boxes on a one-line implies they are two separate sites, which is probably wrong.

In standard TVA practice, the delivery point is a **defined electrical point** (typically the low side of TVA's metering, at the interface) that sits *inside* a physical substation. TVA owns and operates the transmission side and the metering; the LPC owns from the demarcation outward. [S, ownership boundary location varies by delivery point]

**Open item for Zach, and it is the most consequential unresolved item on the diagram:** at JEA's 161 kV delivery points, is the 161/46 kV power transformer TVA-owned or JEA-owned? Both arrangements exist across TVA's LPC fleet. The answer determines whether "TVA delivery point" and "161/46 kV substation" are one box or two on your final one-line. [I]

### 3.2 Terminology error in the current diagram

The diagram labels the 161/46 kV facilities **"Switching substation A"** and **"Switching substation B."** This is wrong terminology and Zach will catch it.

- A **switching station** (or switchyard) contains breakers, buses, and disconnects but **no power transformer**. Its job is to reconfigure connections at a single voltage.
- A facility that transforms 161 kV to 46 kV is a **step-down substation**, or in this context a **subtransmission source substation**.

Recommended relabel: **"161/46 kV source substation A / B."**

### 3.3 Comparison table: the four station types on this system

| Attribute | TVA delivery point | JEA 161/46 kV source substation | JEA 46/12.47 kV distribution substation | Customer substation |
|---|---|---|---|---|
| **Primary function** | Ownership and revenue metering boundary | Bulk step-down to subtransmission | Step-down to primary distribution; feeder origination and protection | Customer-owned step-down for large loads |
| **Voltage in / out** | 161 kV in / 161 kV out (a point, not a transformation) | 161 kV / 46 kV | 46 kV / 12,470Y/7,200 V | 46 kV or 161 kV / customer utilization |
| **Contains a power transformer?** | Not by definition; the adjacent transformer may be TVA's or JEA's | Yes | Yes (53 across 29 sites) | Yes |
| **Revenue metering present?** | **Yes, this is the defining feature.** TVA bills JEA on demand and energy here | No | No | Yes, customer meter |
| **Owner of the equipment** | TVA up to the demarcation, JEA beyond | JEA (assumed) [I] | JEA | Customer |
| **Who operates it** | TVA transmission operations | JEA | JEA distribution operations / SCADA | Customer |
| **Typical protection** | TVA transmission relaying: line differential, distance (21), breaker failure | Transformer differential (87T), high-side interrupting device, low-side 46 kV breaker | Transformer differential, LTC control, **feeder breakers with SEL-351S relays** | Customer main breaker, primary fusing |
| **Voltage regulation** | None | Possibly | **Yes, LTC on the transformer.** JEA sets LTC on a 120 V base at about 123.5 V | Customer's problem |
| **Count on JEA's system** | 2 shown on the diagram; likely more system-wide | Small number (2 shown) | 29 substation locations | A few; Zach cites 2 or 3 all-underground industrial customers |
| **SCADA / automation** | TVA's system | JEA SCADA | JEA SCADA, and 4 or 5 existing distribution automation schemes | Rarely |
| **In trainer scope?** | No, narration only | No, narration only | **YES. These are your two sources.** | Unconfirmed, see Section 8 |

### 3.4 Delivery point A vs delivery point B

Both are 161 kV metering and ownership boundaries. The distinction that matters for FLISR is **electrical independence**: two delivery points fed from genuinely different points on TVA's meshed transmission network give JEA true source diversity. Two delivery points tapped off the same 161 kV line do not.

This is not confirmed for JEA. **[I]** Ask Zach. It affects how you narrate the trainer: "two independent sources" is a strong claim.

### 3.5 The 46 kV subtransmission tie (cross-tie 2 on the diagram)

- **Stated as:** normally **closed**, two delivery points feeding one loop that serves multiple distribution substations.
- **Confidence: LOW [I].** This is inferred from standard practice, not confirmed for JEA.
- **Why it matters:** if JEA's 46 kV is actually radial per substation, then your two tabletop "sources" are not two independent grid entries. They are two feeders off two different distribution substations that happen to share upstream infrastructure. That is still a perfectly valid and realistic FLISR demonstration, but the narration has to change from "two independent sources" to "an alternate source path."
- **Contrast with the distribution tie:** the 46 kV tie is normally **closed** (a genuine loop). The 12.47 kV tie is normally **open**. This closed vs open distinction is the single most important conceptual point in the whole one-line and should be visually obvious on the tabletop.

### 3.6 Distribution substation A vs distribution substation B

For trainer purposes these are functionally identical: 46 kV in, 12,470Y/7,200 V out, feeder breakers on the low side. The distinction is **positional and operational**, not electrical:

- **Sub A** is the normal source for Feeder 1 and everything upstream of the open tie on the A side.
- **Sub B** is the normal source for Feeder 2, and is the **alternate source** for the A-side load downstream of an isolated fault.
- The roles reverse if the fault occurs on the B feeder. Both subs must be able to play both roles. Your FLISR logic must be symmetric.

---

## 4. Component catalog: distribution tier (the tier you are building)

### 4.1 Substation power transformer (46 kV to 12,470Y/7,200 V)
- **Function:** voltage transformation, and it establishes the grounding reference for the distribution system (delta high side, grounded-wye low side is typical). [S]
- **Looks like:** oil-filled tank, radiators, three high-side bushings, three low-side bushings plus a neutral bushing, a conservator or nitrogen blanket, a gauge panel, and an LTC compartment bolted to one side.
- **Load Tap Changer (LTC):** a motor-driven mechanism that changes transformer turns ratio under load to hold constant secondary voltage as feeder load varies. JEA sets theirs on a 120 V base at about **123.5 V**. [V] Zach cited an example substation transformer showing 122.7 V at the LTC with total connected capacity around 18 MVA. [V]
- **Fault role: PASSIVE.** A transformer cannot isolate a fault. It carries through-fault current and it is protected *by* other devices (differential relay, high-side interrupting device). Do not represent it as a switching device on the trainer.

### 4.2 Substation feeder circuit breaker (ABB R-MAG, 15 kV class)
- **Function:** the origination point and primary protection for one distribution feeder. Zach calls it "the last line of protection," meaning the last device that should trip before a failure propagates into the substation itself. [V]
- **Physical description:** a dead-tank outdoor breaker. Rectangular weatherproof steel housing at ground level, **six bushings on top, three in and three out**. Vacuum interrupters inside, one per phase, encapsulated in solid insulating material. [V]
- **Actuation:** magnetic actuator, not a spring-charged mechanism. **One moving part.** No gas, no oil for interruption. [V, ABB]
- **Ratings (ABB R-MAG family):** 15.5 / 27 / 38 kV classes, up to 3,700 A continuous, up to 40 kA interrupting. Magnetic actuator rated 100,000 operations at 15 to 27 kV; vacuum interrupters rated 30,000 full-load operations. [V, ABB]
- **Brains:** it does not decide anything on its own. An external relay (SEL-351S) reads the CTs and commands trip and close.
- **Fault role: INTERRUPTING.** It breaks fault current.

### 4.3 SEL-351S protection system relay
- **Function:** the decision-making element. Reads current from CTs and voltage from PTs, applies time-overcurrent and instantaneous elements, decides whether to trip, how fast, whether to reclose, and whether to go to lockout. Zach: "the brains of the operation." [V]
- **Looks like:** a rack- or panel-mounted rectangular black box in a substation control house, with an LCD, front-panel targets, and a serial/Ethernet port. Not a field-visible object.
- **Key behaviors to demonstrate:**
  - **Time-overcurrent (51):** the closer the fault and the higher the current, the faster the trip.
  - **Instantaneous (50):** no intentional delay for very high current.
  - **Reclose:** after a trip, wait a dead interval, then reclose. Most distribution faults are temporary (tree branch, animal, lightning flashover) and clear during the dead interval.
  - **Lockout:** after a configured number of unsuccessful reclose attempts, stop trying and stay open. This is a permanent fault.
- **Fault role: SENSING and DECIDING.** It does not itself interrupt anything.

### 4.4 Line recloser (G&W Viper-ST)
- **Function:** identical in principle to the substation breaker, relocated out onto the line. Provides overcurrent protection and reclosing for a section of feeder, so that a fault downstream of the recloser does not require the substation breaker to trip the whole feeder.
- **Physical description:** a compact solid-dielectric device with **six bushings (three in, three out)** and **three vacuum interrupters**, one per phase, epoxy-encapsulated inside an aluminum casting. Pole-mounted on a bracket, roughly the size of a large suitcase. Includes a **manual trip handle** with a true mechanical block, and a mechanical position indicator. [V, G&W]
- **Sensing:** up to 6 internal voltage sensors and 3 dual-ratio current transformers built into the device. Dead-tank construction. [V, G&W]
- **Actuation:** magnetic actuator, capable of operating on battery backup when AC source power is lost. This matters: **a recloser can still open and close on a de-energized line**, which is exactly what FLISR requires. [V, G&W]
- **Ratings:** through 38 kV (newer catalogs to 40.5 kV), 800 A continuous, 12.5 kA symmetrical interrupting (16 kA option up to 27 kV). [V, G&W]
- **Independent pole operation:** the Viper-ST can be configured for 1-phase trip / 1-phase lockout, 1-phase trip / 3-phase lockout, or 3-phase trip / 3-phase lockout. [V, G&W]
- **Control:** the Viper-ST is normally paired with an **SEL-651R recloser control**, not an SEL-351S. [V, G&W] The presentation shows a 351S alongside the Viper, which may be a simplification for teaching. Worth confirming with Zach so your one-line does not label a pole-top control with a substation relay part number. **[I]**
- **Fault role: INTERRUPTING.** Full fault-current interrupting capability.

### 4.5 Pad-mounted switchgear (G&W, the device Zach cares most about)
- **Function:** the primary sectionalizing and switching device in **underground** distribution. This is the device the trainer is fundamentally about, because JEA's stated ask is a scaled model of an **underground** distribution system.
- **External appearance:** "a big green square." A locked, tamper-resistant steel enclosure on a concrete pad, roughly refrigerator-sized or larger. Indistinguishable from a pad-mount transformer to a layperson, which is exactly why the trainer needs to teach the difference. [V]
- **Internal construction:** typically **four compartments** around a common bus. An incoming feeder cable lands in one compartment, hits a **uniform busway**, and the bus feeds out in the other directions. [V]
- **Compartment types, and this is the crucial distinction:**
  - **Switch ways (load-break switches):** manually operated, open and close only. Zach's word for them is *"dumb."* No fault-current interrupting, no automation, no decision-making. [V]
  - **VCB ways (vacuum circuit breaker):** **controllable.** Can open and close based on fault current, SCADA commands, relay logic, or local pushbuttons. These are the smart, automation-capable compartments. [V]
- **Example configuration cited:** a "two-switch, two-VCB" unit, meaning two dumb switch ways and two controllable breaker ways. [V]
- **Cost:** roughly **$25,000 per unit.** [V] This is the direct justification for the trainer existing at all: JEA cannot leave $150k to $200k of real gear sitting in a classroom.
- **Where JEA has these:** downtown Jackson, Van Drive, and across Union University's campus (two units on campus). [V]
- **Field automation package:** motor operators, relays, and communications back to a SCADA master station. [V]
- **Fault role: SECTIONALIZING (switch ways) and INTERRUPTING (VCB ways).** This one physical enclosure contains devices from two different functional classes, and that distinction must survive into your trainer representation. A pad-mount switchgear icon on the tabletop is ambiguous unless you show which ways are switched and which are VCB.

### 4.6 Voltage regulator
- **Function:** holds voltage within ANSI Range A along a long feeder as load varies. Compensates for the voltage drop between the substation and the far end.
- **Looks like:** a single-phase pole-mounted oil-filled cylinder (three of them for a three-phase bank) with a control cabinet, or a three-phase pad-mounted unit. Physically similar to a distribution transformer but with a tap-changer control box.
- **Fault role: PASSIVE.** It cannot isolate. It does experience a voltage collapse during a fault and will attempt to correct, which is a secondary effect not worth modeling.
- **Trainer relevance:** low priority. Good as a labeled 3D-printed prop with a static LED; not a control point.

### 4.7 Distribution transformer

**Single-phase pole-top or pad-mount** (the residential unit, "the one everybody plays on in the subdivisions"):
- **Primary side:** 2 bushings (incoming and outgoing, so the transformer loops in and out of the primary run). [V]
- **Secondary side:** 3 bushings, being 2 phase-to-ground plus 1 neutral. This is the center-tapped 120/240 V arrangement. [V]
- **Serves:** typically 4 to 8 residences per transformer.

**Three-phase pad-mounted:**
- **Primary side:** 6 bushings, 3 in and 3 out. [V]
- **Secondary side:** 4 studs, being 3 phase plus neutral. [V]
- **Serves:** 208Y/120 V or 480Y/277 V commercial loads.

**Fault role: PASSIVE, and this is the single most-missed point in the whole subject.** A pad-mounted transformer cannot isolate a fault. It looks exactly like pad-mounted switchgear from the road. A trainee who cannot tell them apart will misread every underground one-line they ever see. **Build the trainer so this distinction is visually explicit.**

### 4.8 Fuse / fused cutout (lateral protection)
- **Function:** one-shot overcurrent protection for a single-phase lateral or a tap. Melts and drops open on fault current. Requires a truck roll to replace.
- **Looks like:** a porcelain or polymer tube on a pole-mounted bracket, hinged so it swings down visibly when blown. A lineman can see a blown cutout from the road, which is its main diagnostic value.
- **Fault role: INTERRUPTING but NOT RESTORABLE and NOT CONTROLLABLE.** It has no communications, no status reporting, and no reclose capability.
- **Why it matters conceptually:** the fuse is the antithesis of FLISR. It isolates, but it converts every fault into a manual, hours-long outage. Every dollar spent on reclosers and switchgear is a bet against the fuse. Consider representing at least one fused lateral on the tabletop specifically as the "before" case.
- **The coordination question:** "fuse saving" (recloser trips fast to give a temporary fault a chance to clear before the fuse melts) vs "fuse blowing" (let the fuse operate). Worth one sentence in your demo script; not worth modeling.

### 4.9 Normally-open tie switch (cross-tie 3, the FLISR restoration path)
- **Function:** connects the far end of Feeder 1 to the far end of Feeder 2. Held **open** in normal operation.
- **Looks like:** either a pole-top switch or, in underground, a switch or VCB way inside a pad-mount switchgear enclosure. It is not a distinct device type; it is a **role** assigned to an ordinary switching device by virtue of where it sits and how it is normally operated.
- **Governing principle:** the distribution system is **built physically looped but operated radially**. Feeders are constructed to reach each other and then deliberately held open at a tie point. Closing that tie after isolation is the "R" in FLISR. [V]
- **Why radial operation:** radial gives simple, coordinated, unidirectional overcurrent protection and predictable fault current. A closed distribution loop would need directional or differential protection at every device and would multiply cost.
- **Fault role: RESTORING.** It never interrupts fault current in a correct FLISR sequence. It closes only after the fault is already isolated. If your logic ever closes the tie into an un-isolated fault, that is a design failure worth demonstrating deliberately as a "what not to do."

### 4.10 Substation bus tie breaker (cross-tie 4)
- **Function:** inside a two-transformer distribution substation, connects the two low-side buses. Normally **open** with a split bus.
- **Purpose:** backs up a failed transformer *within the same substation*. If Transformer 1 fails, the bus tie closes and Transformer 2 carries both buses.
- **Distinction from the feeder tie:** the bus tie is intra-substation and covers *equipment* failure. The 12.47 kV feeder tie is inter-substation and covers *line* faults. Different problems, different scopes, both normally open.
- **In trainer scope:** probably not, unless you want to teach transformer contingency as a second scenario. It adds two devices and one more mental model. Recommend leaving it out of v1.

### 4.11 DER interconnection (solar, inverter-coupled)
- **Function:** customer- or utility-owned generation tied into the distribution feeder through its own protective device. Introduces **bidirectional power flow**, which breaks the assumption that current always flows away from the substation.
- **Looks like:** a PV array plus an inverter, an AC disconnect, and a utility-required interconnection recloser or breaker at the point of common coupling.
- **Governing standard: IEEE 1547.** The behavior to demonstrate is **anti-islanding**: when the utility source is lost, the DER must detect the loss of voltage and open, so that it does not backfeed a de-energized, faulted line and injure a lineman working on it. [V, and Zach specifically wants this taught]
- **Fault role: MUST TRIP, not isolate.** The DER is not part of the isolation strategy. It is a hazard that the isolation strategy has to account for. Structurally: **the DER branch must go dark whenever its host segment goes dark**, and it must do so *before* any crew is assumed to be on the line.
- **Confirmed in scope** per the Scope of Work: an alternate source (DER) tied into the backbone through its own protective device, to introduce bidirectional flow and demonstrate IEEE 1547. [V]

### 4.12 Load lateral, service drop, meter, main panel
- **Meter:** revenue metering at the customer. Passive.
- **Main panel:** customer-side overcurrent protection. Outside utility scope entirely.
- **Trainer role:** these are your **outage indicators**. Their only function on the tabletop is to be lit or dark, which is what makes the FLISR value proposition legible to a non-engineer. Per the Scope of Work, load laterals get status indicators, variable load, and test points, potentially represented by 3D-printed houses.

### 4.13 Customer service voltage classes (context, ANSI C84.1)

| Customer type | Service voltage | Configuration |
|---|---|---|
| Residential | 120/240 V | 1-phase, 3-wire, center-tapped |
| Small commercial | 208Y/120 V or 120/240 V | 3-phase 4-wire wye, or 1-phase |
| Large commercial, school, office | 480Y/277 V | 3-phase 4-wire wye; 277 V for lighting |
| Light industrial | 480Y/277 V or 480 V | 3-phase |
| Large industrial | 12,470Y/7,200 V primary | Customer-owned step-down |
| Very large industrial | 46 kV or 161 kV | Customer substation |
| Large in-plant motors | 4,160 V or 13.8 kV | Customer medium-voltage system |

**Common error to avoid:** "440 V" and "220/440 V" are not ANSI C84.1 nominal system voltages. The correct three-phase low-voltage nominals are 208Y/120, 240, 480Y/277, 480, and 600. 440 V appears in C84.1 only as a Range B utilization limit under a 480 V nominal system. 460 V is the NEMA motor nameplate rating for a 480 V system.

---

## 5. Functional role taxonomy: the five classes

Stop calling everything an "isolation device." There are five distinct roles, and a device's role determines its I/O footprint, its LED behavior, and its position in the FLISR sequence.

| Class | Definition | Can break fault current? | Controllable? | Devices in this class |
|---|---|---|---|---|
| **1. Sensing / deciding** | Measures current and voltage, applies protection logic, issues commands | No | n/a | CTs, PTs, voltage sensors, SEL-351S, SEL-651R, transformer differential relay |
| **2. Interrupting** | Breaks fault current on command or autonomously | **Yes** | Yes | Substation feeder breaker (R-MAG), line recloser (Viper-ST), VCB ways in pad-mount switchgear |
| **3. Sectionalizing / isolating** | Opens to create an isolation boundary, generally on a de-energized or load-only circuit | **No** (load-break only, or no-load only) | Sometimes | Load-break switch ways in pad-mount switchgear, motor-operated line switches, air-break disconnects |
| **4. Restoring** | A normally-open point closed to re-energize an isolated healthy section from an alternate source | No (should never see fault current) | Yes | 12.47 kV feeder tie switch, substation bus tie breaker |
| **5. Passive / must-trip** | Cannot isolate anything. Either purely passive, or a source that must be removed | No | No (passive) / Yes (DER) | Transformers, conductors, arresters, regulators, meters, and the DER (which is "must trip," not "isolating") |

**Sixth category worth naming: one-shot protection.** The fused cutout interrupts fault current but cannot be controlled, reclosed, or reported. It occupies a category of its own and is best treated as the anti-pattern the whole project is arguing against.

**Terminology footnote:** a classical **sectionalizer** is a specific device that counts upstream interrupter operations and opens during a dead interval, with no fault-interrupting capability of its own. JEA's approach uses communicating devices making coordinated decisions, not counting sectionalizers. Do not use the word "sectionalizer" loosely in your PDR or Zach will interpret it as the specific device.

---

## 6. What is actually in play during a fault

### 6.1 Fault location determines which layers participate

For a **fault on a 12.47 kV feeder** (the only fault type the trainer models), here is the full set of participants, in coordination order:

| Order | Device | Role | What it does | Normally operates? |
|---|---|---|---|---|
| 1 | Lateral fuse (if fault is on a fused lateral) | One-shot interrupting | Melts, drops open. Fault cleared, lateral dark until a truck arrives | Only if fault is on that lateral |
| 2 | Nearest upstream recloser or VCB way | Interrupting | Sees fault current, trips, attempts reclose, goes to lockout on a permanent fault | Yes, if one exists upstream of the fault |
| 3 | Substation feeder breaker (R-MAG + SEL-351S) | Interrupting | Sees fault current, trips. The backstop for the entire feeder | Yes, if no downstream device cleared it first |
| 4 | Downstream device that did **not** see fault current | Sectionalizing | Reports "no fault current here." Combined with upstream reports, this **localizes** the fault to the segment between the two. Then opens during the dead interval | Yes, this is the "L" and "I" in FLISR |
| 5 | Normally-open tie switch | Restoring | Confirms it saw nothing, closes, backfeeds the healthy downstream section from the alternate source | Yes, this is the "SR" in FLISR |
| 6 | DER interconnection device | Must-trip | Detects loss of utility voltage, opens per IEEE 1547 anti-islanding | Yes, if the DER is on the de-energized section |
| 7 | Substation transformer low-side / high-side device | **Backup** interrupting | Only if the feeder breaker fails to clear. Breaker-failure backup | **No.** Failure case only |
| 8 | 46 kV subtransmission protection | Remote backup | Only if substation protection fails entirely | **No.** Deep failure case only |

**Rows 7 and 8 are the honest answer to "are the upper tiers in play."** They are, but only as backup protection that should never operate. If your one-line shows them as active FLISR participants, that is wrong. If it shows them as absent entirely, that is also slightly wrong. Best treatment: narrate them as "the layers above that should never have to act."

### 6.2 The FLISR sequence, device by device

Using the topology in your design notes (two distribution substations, radial feeders meeting at a normally-open tie):

```
NORMAL STATE
  Sub A breaker  : CLOSED  -> Feeder 1 energized to the tie
  Sub B breaker  : CLOSED  -> Feeder 2 energized to the tie
  Mid-line devs  : CLOSED
  Tie switch     : OPEN
  All loads      : ENERGIZED

t=0   FAULT on Feeder 1, in the segment between device D1 and device D2

t+cycles   D1 (upstream of fault) sees fault current -> TRIPS
           Everything downstream of D1 on Feeder 1 goes dark
           D2 (downstream of fault) sees NO fault current
           [Note: which device trips first depends on coordination.
            If no mid-line device exists upstream, the Sub A breaker trips
            and the ENTIRE feeder goes dark. That difference is the
            whole argument for mid-line devices.]

t+dead interval   D1 attempts RECLOSE
           Permanent fault -> D1 trips again -> after N attempts, LOCKOUT
           [Temporary fault -> reclose succeeds, no FLISR needed.
            Demonstrate this case too. It is roughly 70-80% of real faults.]

FAULT LOCATION
           Controller compares: D1 saw fault current, D2 did not
           -> Fault is BETWEEN D1 and D2. Segment identified.

ISOLATION
           D2 OPENS (it is now on a de-energized line, so no
           interruption duty). Faulted segment now bounded by
           D1 open and D2 open.

           DER on the de-energized side OPENS per IEEE 1547.

RESTORATION (upstream)
           D1 stays OPEN (it borders the fault).
           Everything from Sub A to D1 was already restored when
           the fault cleared, or never lost.

RESTORATION (downstream)
           Tie switch CLOSES.
           Section from D2 to the tie is now backfed from Sub B.
           Loads restored. New open point is at D1/D2.

FINAL STATE
           Faulted segment: DE-ENERGIZED and BOUNDED
           All other load: ENERGIZED
           Sub B now carries its own feeder plus the transferred section
           -> this is why loading analysis (Milsoft) is required.
              You cannot transfer load you do not have ampacity for.

RETURN TO NORMAL (after crew repairs the fault)
           Tie switch OPENS, D2 CLOSES, D1 CLOSES.
           System back to the normal state above.
```

### 6.3 Devices that operate per fault event

Out of every device on the system, a single FLISR event involves:

- **1 interrupting operation** (the upstream device that clears the fault)
- **1 sectionalizing operation** (the downstream device that bounds it)
- **1 restoring operation** (the tie closes)
- **0 or 1 must-trip operation** (the DER, only if it is on the affected section)

**Three to four device operations per event.** That is the number a trainee needs to internalize. Everything else on the table stays put.

---

## 7. How many isolation mechanisms will be in your final design

Direct answer, based on the topology already recommended in your design notes (two distribution substations at opposite corners, radial feeders meeting in the middle at a normally-open tie, plus a DER branch).

### 7.1 Recommended device inventory

| # | Device | Class | Represents | Fault-injection segments it bounds |
|---|---|---|---|---|
| 1 | Sub A feeder breaker | Interrupting | R-MAG + SEL-351S | S1 (upstream side) |
| 2 | Device A1 | Interrupting | Pad-mount switchgear VCB way | S1 / S2 |
| 3 | Device A2 | Interrupting | Pad-mount switchgear VCB way | S2 / S3 |
| 4 | **Tie** | Restoring | Switchgear switch or VCB way | S3 / S4 |
| 5 | Device B2 | Interrupting | Pad-mount switchgear VCB way | S4 / S5 |
| 6 | Device B1 | Interrupting | Pad-mount switchgear VCB way | S5 / S6 |
| 7 | Sub B feeder breaker | Interrupting | R-MAG + SEL-351S | S6 (upstream side) |
| 8 | DER interconnection device | Must-trip | IEEE 1547 PCC recloser | DER branch |

### 7.2 The counts

| Metric | Count |
|---|---|
| **Isolation boundary devices** (can create an open point on the backbone) | **7** |
| Of which: interrupting class | 6 |
| Of which: restoring class | 1 |
| Must-trip devices (DER) | 1 |
| **Total controllable devices** | **8** |
| **Isolatable segments (fault zones) on the backbone** | **6** |
| Segments including the DER branch | 7 |
| **Devices that operate in any single FLISR event** | **3 to 4** |

**7 isolation devices creating 6 fault zones.** Six devices in series along a two-source backbone always yields exactly six segments when you include the two source-side segments, so this is internally consistent and worth stating that way in your PDR: "N devices, N-1 interior segments plus 2 source segments." Sanity check: 7 devices in a line create 6 gaps between them, and each gap is a segment. Consistent. [computed here]

### 7.3 I/O implications, and a correction

With 8 controllable devices:

| Signal type | Count | Module | Notes |
|---|---|---|---|
| Trip + close outputs, two-coil scheme | 16 DO | SEL-2244-3 (16 DO) | **Exactly full. Zero spare.** |
| Trip + close outputs, latching scheme | 8 DO | SEL-2244-3 | 8 spare |
| Device position status | 8 DI | SEL-2244-2 (24 DI) | |
| Fault-injection pushbuttons | 6 DI | same module | |
| Mode / reset / HMI-local inputs | ~4 DI | same module | |
| **DI subtotal** | **~18 of 24** | one SEL-2244-2 | 6 spare |

**Correction to a prior assumption in your notes:** the "6 DI budget" is not a hardware limit. The SEL-2244-2 provides **24** optoisolated dry-contact inputs, and the SEL-2244-4 provides **32**. [V, SEL] Up to nine of either may be installed in a node. **Digital outputs are your tight resource**, at 16 per SEL-2244-3. Budget your design against DO, and either specify two DO modules or use single-coil latching relays for the tabletop switching devices.

**If you want more fault zones, the constraint is not I/O.** It is (a) table area and visual legibility at 4 ft by 4 ft, and (b) demo runtime. Six zones is a reasonable pedagogical number. Justify it that way in the PDR, not as an I/O limit, because Zach will know the Axion's I/O capacity.

### 7.4 What you can add without changing the count

These add realism and teaching value with **zero** additional control I/O, because they are passive or one-shot:

- Fused laterals (3D-printed cutouts, static LED, no control)
- Distribution transformers (pole-top and pad-mount, both types, deliberately shown next to a pad-mount switchgear so the visual confusion is teachable)
- Voltage regulator (labeled prop)
- Load houses (indicator LEDs driven by the segment energization layer, not by the Axion)

---

## 8. Errors and open items in the current one-line

| # | Item | Severity | Confidence | Action |
|---|---|---|---|---|
| 1 | "Switching substation A/B" labels a facility that transforms 161/46 kV. A switching station has no transformer | **High** (terminology error a utility engineer will catch) | [V] | Relabel to "161/46 kV source substation" |
| 2 | Delivery point and 161/46 substation drawn as separate boxes, implying separate sites | Medium | [I] | Confirm with Zach whether they are one facility with an internal ownership boundary |
| 3 | Ownership of the 161/46 kV transformer (TVA or JEA) unresolved | Medium | [I] | Zach |
| 4 | 46 kV configuration assumed to be a normally-closed loop | **High** for narration | [I], LOW confidence | Zach. If radial, reframe "two independent sources" as "two feeders off different substations" |
| 5 | Two delivery points assumed electrically independent on TVA's mesh | Medium | [I] | Zach |
| 6 | Viper-ST shown with an SEL-351S; the standard pairing is an SEL-651R recloser control | Low, but it is a part-number error on a diagram going to a utility | [I] | Zach, or relabel generically as "recloser control" |
| 7 | Diagram is single-line throughout. Single-phase lateral fusing and unbalanced fault behavior cannot be shown | Low for v1 | [V] | Accept. Note the limitation in the report |
| 8 | Pad-mount switchgear shown as a single icon; switch ways vs VCB ways not distinguished | Medium (this is the central teaching point) | [V] | Add compartment detail on at least one unit |
| 9 | Industrial customer branch: in scope or not? | Medium (affects device count) | [I] | Zach. DER is confirmed in scope per SOW; the industrial branch is not |

---

## 9. Adjacent issues, listed rather than expanded

1. **Load transfer ampacity.** The SOW requires a Milsoft power system analysis pass. The reason is in the FLISR sequence: after restoration, Sub B carries its own load plus the transferred section. If that exceeds conductor or transformer ampacity, FLISR is not a valid candidate for that circuit. Zach said this directly. Your trainer should probably have a way to show a "transfer blocked, insufficient capacity" outcome, because that is a real operating constraint and it is a good teaching moment.
2. **Temporary vs permanent faults.** Roughly 70 to 80 percent of overhead distribution faults are temporary and clear on reclose, with no FLISR needed. Underground faults are overwhelmingly permanent. Since JEA asked for an **underground** trainer specifically, the reclose-succeeds case may deserve less emphasis than the reclose-fails case. Worth a design decision.
3. **The trainer is underground but Zach notes there is not a single house in Jackson that is not fed overhead somewhere between the substation and the meter.** Your one-line will be a hybrid in reality. Decide deliberately how much overhead to represent.
4. **Naming devices.** Give every device a permanent tag (SUB_A_BKR, DEV_A1, TIE_1, DER_1) now, before the RTAC tag structure is built. Renaming later touches the logic, the HMI, the LED map, the wiring labels, and the as-built one-line simultaneously.
5. **Model the topology as a graph, not coordinates.** Node and edge tables, per the existing design principle. Fault-zone membership is a graph traversal, not a geometry problem.
6. **The bus tie breaker (cross-tie 4) is a second, separable scenario.** Deliberately excluded from the count above. Revisit only if v1 has schedule margin.
