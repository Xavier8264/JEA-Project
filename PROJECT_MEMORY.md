# JEA Tabletop FLISR Trainer - Project Memory

Running memory for the Union University senior design project sponsored by Jackson
Energy Authority. Append-only by convention.

**How to use this file**

- New work gets a new timestamped entry at the BOTTOM. Do not rewrite old entries.
- Later entries may contradict earlier ones. That is expected and fine. When it
  happens, the newer entry wins, and it should say explicitly what it supersedes.
- Entries carry confidence markers, same convention the component reference uses:
  - `[V]` verified against a primary source (vendor doc, standard, direct JEA statement)
  - `[S]` standard industry practice, near-universal, not confirmed for JEA
  - `[I]` inference, could be wrong
- "Working directory" throughout means `c:\Users\jprun\Downloads\JEA Project`.

---

# Standing project facts

Snapshot as of the first entry below. Superseded by any later entry that contradicts it.

## People and roles

- **Zach Wadley** - JEA sponsor, ran the 8/27 kickoff. Owns scope, budget and approvals.
  Offered to buy materials directly on a JEA P-card or PO. Says to call, text or email
  any time rather than waiting. `[V]`
- **Michael** - JEA, the SEL / relaying / protection / communications expert. Did the 3D
  substation design work. Will be the technical resource on the RTAC. `[V]`
- **Dr. Schwintz / Dr. King** (names garbled in the transcript, spelled inconsistently) -
  UU faculty. Dr. King emphasized this must not be "just a construction project, building
  Legos"; he wants engineering backbone behind it. `[V]`
- Jordan Prunty is the user of this repo. Uses AutoCAD daily. `[V]`

## Sponsor intent, from the 8/27 kickoff transcript

- The deliverable is a **portable tabletop distribution automation trainer** that JEA will
  keep and reuse as an internal training tool. Not a one-off school project. `[V]`
- Must be liftable by two people. Zach: "it can't be 6 feet long and 3 feet wide," and
  floated "4 by 2 and a half, something that takes 2 people to pick it up." `[V]`
- Two sources, two substations, multiple reclosers that can operate and reconfigure,
  a normally open point in the middle. `[V]`
- Fault injection by **physical pushbutton on the board at each fault zone**, plus the
  same capability from the HMI. Plus a separate reset button off to the side. `[V]`
- Faults are **hard-coded scenarios per button**, not real current injection. Zach:
  "once you press that button, what it does in the RTAC more or less be hard-coded for
  each scenario." Do not build a real fault injection rig. `[V]`
- DER is confirmed in scope. Zach wants it as its own branch off the mainline with its
  own protective device so he can teach IEEE 1547 and anti-islanding. `[V]`
- A standalone industrial customer off a branch, with variable load, so they can get into
  power system analysis and voltage drop. `[V]`
- Underground focus. The trainer is fundamentally about pad-mount switchgear, "the big
  green boxes," which run about $25k per unit. That cost is the justification for the
  trainer existing at all. `[V]`
- Zach liked the above-ground LED strip lighting in the AI concept render, with wiring
  below the surface. He explicitly wants to see where the fault is and where power is
  being transferred to. `[V]`
- Someone floated per-feeder colors: "be really cool if you could add different feeds,
  have different colors, and then change it based on what feed is feeding." That is
  exactly the blue/green scheme now in the layout. `[V]`
- Present to JEA executive management / C-suite before the final academic presentation.
  Zach wants it to be a trial run for the team. `[V]`
- JEA will help build a bill of materials comparing overhead vs underground construction
  cost, with estimated man hours, as a teaching exercise about scope and cost. `[V]`
- **No GIS or real subdivision design data will be shared.** Asked directly about getting
  realistic subdivision designs, the answer was no. Street names off, nothing locatable.
  `[V]`

## Hardware

- **SEL-2240 Axion** already purchased, long lead time, expected around November. This is
  the brains. `[V]`
- Ordered with **32 digital inputs and 32 digital outputs**. More modules are possible but
  lead time is the risk, so flag any I/O growth early. Modules are cards that can be
  added later into pre-wired slots. `[V]`
- A metering module was ordered. Metering is AC. The I/O modules run 125 VDC or AC and are
  **per-input selectable**, so a mix is fine. `[V]`
- Input power is **120 VAC**, plug into a wall. Rectify/transform internally for whatever
  the LEDs and controls need. Zach: "128C [120 AC], for sure, for input power." `[V]`
- Zach also bought a spare lower-powered RTAC and an HMI license. Intent was to connect a
  computer rather than use the DisplayPort output, though he was unsure in the moment. `[V]`
- Programming is **ACSELERATOR RTAC (SEL-5033)**, IEC 61131. Zach describes it as "a
  variation of some C++," structured text rather than ladder. Ladder exists in the tool
  but Zach has never used it and cannot help there. He offered to send example projects.
  `[V]`
- Software is free but requires an account, possibly tied to a corporate email, so JEA
  will supply the executable via the shared drive. `[V]`
- Known gotcha: connecting to the RTAC is over Ethernet by IP. On a non-admin laptop the
  network adapter may not pull an IP in the right subnet automatically. Zach hits this
  himself. `[V]`

### SEL-2240 Axion physical dimensions `[V]`

Read directly out of `Axion Instruction Manual.pdf` / `Axion Panel Drawings.pdf`
(same document, 1282 pages), Section 2 Installation, Device Placement.

| Item | Value | Source |
|---|---|---|
| 10-slot **panel cutout** | **17.75 x 8.80 in** [450.9 x 223.5 mm] | Fig 2.2, Fig 2.4 |
| 10-slot panel-mount front panel / bezel | 19.76 x 9.61 in [501.9 x 244.1 mm] | Fig 2.2 |
| Depth behind panel | 7.00 in [177.9 mm] | Fig 2.2 |
| Module removal clearance | 0.61 in [15.4 mm] additional | Fig 2.2 |
| Mounting hole spacing | 18.31 in [465.1 mm] x 5.75 in [146.1 mm], 4x dia 0.25 | Fig 2.2 |
| 10-slot rack mount | 19.00 in wide, 8.72 in high, 6.90 in deep | Fig 2.1 |

**Important orientation note:** on the real chassis the **17.75 in dimension is the
WIDTH** (ten module slots side by side) and 8.80 in is the height. The manual states:
"The Axion must be mounted such that modules are vertical and have at least 0.5 inches
to the nearest solid surface above and below" (Section 2, Device Placement). Mounting
the unit flat into a tabletop lays the modules horizontal, which departs from that
instruction. Probably fine thermally at this duty, but it is an open question for SEL
or Michael and it is the kind of detail that scores points at a design review.

## Budget and procurement

- Roughly **$10,000** total. About $6,000 already consumed by the Axion / relay hardware.
  Several thousand remain. Zach: "I don't think money's gonna be [a problem]. If it's
  legit, we'll make it happen." `[V]`
- Purchasing goes through JEA. Send Zach a list; he buys it on a P-card or PO. `[V]`

## Schedule

- Kickoff 2026-08-27. `[V]`
- PDR with JEA: week of Oct 5. `[V, per SOW]`
- Winter break Dec 10 to Jan 7, no scheduled work. `[V, per SOW]`
- Target "done" first of March 2027 so the team is not stressed at the end. `[V]`
- Scholarship symposium mid-to-late March 2027 (date was uncertain in the meeting;
  someone said "March the 27th" and someone else said it got bumped earlier last year).
  `[I]` - needs confirming against the academic calendar.
- UU event / final demo day: **April 6, 2027**. `[V, per SOW]`

## Communication

- Weekly written update by email to JEA. Requested by the faculty advisor. `[V]`
- Meetings: bi-weekly Teams, roughly monthly in person, more as needed. Zach does not see
  a big need for frequent in-person meetings and said it is nothing for him to drive out
  to the lab. `[V]`
- File sharing: **Google Drive**. `[V]`

## Fabrication resources

- The lab has multiple new Bambu printers, including multicolor. `[V]`
- Roadways and grass could be vinyl wrap rather than printed. The SOW calls for a 2D
  plan-view graphic on vinyl as a panel backdrop. `[V]`
- Model train scale scenery (trees, figures) is available from hobby stores. `[V]`

---

# Log

## 2026-09-07 21:46 CDT - Physical layout design session

### What was asked

Produce a practical physical layout for the final product: a 4 ft x 4 ft model, built
from four 2 ft x 2 ft pieces. Mark out where every component, building and unit sits,
and importantly show where the isolation mechanisms and the other key FLISR components
land on the map.

Stated constraints from the user:

- 48 x 48 in overall, split into four 24 x 24 in pieces.
- PLC/HMI in the bottom right corner, "17.75 in tall by 8.8 in wide, flat on the table."
- Two distribution substations: one bottom left, one in the top right section.
- A normally open tie between them.
- Two residential sections, one small commercial customer, one industrial customer,
  one DER interconnection.
- A pond, as a deliberate wabi-sabi element.
- Conceptually the bottom half of `jea_power_delivery_oneline.png`, except the large
  commercial customer is replaced by a second residential section.

Stated build intent (context, not scope): the user is going to buy four 2x2 cardboard
sections, tape addressable LEDs along the power line routes, and wire an ESP32 to as
many pushbuttons as needed for manual fault injection. The animation is a break in the
middle of a line, green or blue depending on which substation is feeding, turning red,
then animating isolation and restoration from whichever substation now feeds the
customer. **The ESP32 LED logic is a different chat session and was explicitly out of
scope for this one.**

### Sources read this session

| File | What was taken from it |
|---|---|
| `jea_power_delivery_oneline.png` | The reference topology the layout renders in plan |
| `JEA Meeting Transcript 8.27.txt` | All the sponsor intent captured in Standing Facts above |
| `jea_oneline_component_reference.md` | Device inventory, the 5-class functional taxonomy, the FLISR sequence, the I/O math |
| `jea_power_delivery_oneline_reference.md` | Voltage tiers, cross-tie definitions |
| `JEA_Senior_Design_Scope_of_Work (1).docx` | Phase 2 deliverables, timeline, success criteria |
| `Table-top Trainer AI Concept.png` | The concept render. Source of the "JB = junction box" prop idea |
| `Axion Instruction Manual.pdf` | The dimensions table above |
| `JEA Prelim Layout.dxf` | Checked and set aside: it is a JEA drawing title block and utility legend template (layers STORM / WATER / ELECTRIC / SEWER / GAS), not a layout |

### Decisions taken, and why

Four questions were put to the user. All four came back with the recommended option.

1. **Deliverable format.** Interactive true-scale artifact plus a machine-readable spec
   file written into the working directory. Rationale: the artifact is for the PDR and
   for JEA; the spec file is the interface to the ESP32 session so it does not have to
   re-derive any geometry.
2. **PLC/HMI orientation.** 17.75 in wide east-west by 8.80 in deep north-south, long
   edge along the front. Rationale: matches the real chassis proportions, keeps the
   touchscreen and I/O facing the operator, and leaves a clean 24 x 12.3 in band across
   the top of the SE panel for the solar array. Note this means the user's original
   phrasing ("17.75 tall") was the chassis rotated 90 degrees; the layout uses the
   hardware's real orientation.
3. **LED chain topology.** Four independent chains, one per 2x2 panel, each with its own
   data pin and 5 V injection. Rationale: panels unplug independently, a bad panel does
   not kill the rest, and it matches the modular / suitcase build JEA discussed.
4. **Fault zone count.** Six backbone zones plus the DER as must-trip. 7 fault buttons
   plus a reset. Rationale: this is the inventory the existing component reference
   already sized against the Axion I/O, so the PDR story stays consistent.

### Mid-session correction from the user, and what changed

First draft of the plan treated the panel seams as a placement constraint and contorted
the composition to minimize LED crossings. The user rejected that:

> "i dont want you to give too much weight to where the seams are when it comes to
> placing components, in the end i want this to be a seampless table, one single piece,
> one single display. for example, the pond can expand across two panels. dont worry
> about the depth problem, i just want you to create clearance for that component, we
> will solve the depth problem in the real model. but then again, i do actually have to
> figure out how where to place the LED strips and how to wire them and how to get power
> between the panels. i want this to be a balance between logicstic wiring and aethetics"

The layout was redesigned around that. Consequences:

- Composition now drives placement. Four features straddle a seam **on purpose**: the
  legend band and Residential 2 cross x=24; the pond and Residential 1 cross y=24.
- The tie moved from (22, 33), where seam avoidance had pushed it, to **(26.5, 25.5)**,
  2.5 in northeast of true board center, which is where it belongs dramatically.
- The seam problem moved out of the composition and into an explicit wiring architecture
  (below).
- The under-board depth problem for the Axion was dropped to a one-line build note per
  the user's instruction. Surface clearance is still reserved on the drawing.

### The five design rules

These are the answer to "balance between logistics wiring and aesthetics."

- **R1. Composition ignores seams.** Terrain, water, roads and load areas cross panels
  wherever the scene wants. Individual props never straddle a seam; areas do.
- **R2. Every strip discontinuity gets a prop on top of it.** Corners, solder splices and
  seam breaks are covered by a junction box, a pull box, a pad-mount transformer, or a
  device. Real underground distribution puts hardware at exactly those points, so the
  wiring constraint becomes realism instead of a compromise. This is the rule that makes
  logistics and aesthetics agree. The AI concept render already hinted at it with its
  "JB = JUNCTION BOX" props.
- **R3. All wiring lives under the board.** Nothing above the surface but strip, props and
  buttons. Only grommet holes reach the top, and each one sits under a prop.
- **R4. One connector per panel.** Panels separate by unplugging four connectors at a hub
  under the center point. No LED data crosses a seam at all.
- **R5. Strip runs are straight polylines.** Roads may curve; the run beneath is faceted
  with a prop at each facet. Standard WS2812B strip does not bend in the plane of its own
  PCB, and pretending otherwise is how these builds go wrong.

### The layout as built

Coordinate system: origin at the SW corner, x east, y north, units inches.
Panels: Q1 NW, Q2 NE, Q3 SW, Q4 SE. Seams at x=24.0 and y=24.0.

**Keep-outs**

| Rect | SW | NE | Size |
|---|---|---|---|
| PLC panel cutout | (27.75, 2.00) | (45.50, 10.80) | 17.75 x 8.80 |
| PLC bezel | (26.75, 1.60) | (46.50, 11.20) | 19.75 x 9.60 |
| PLC keep-out (bezel + 0.5) | (26.25, 1.10) | (47.00, 11.70) | 20.75 x 10.60 |

**Scene areas**

| Area | SW | NE | Straddles |
|---|---|---|---|
| Legend / title block | (1.0, 0.8) | (25.5, 4.5) | x=24 |
| Substation A | (1.5, 5.5) | (12.0, 14.0) | no |
| Pond (organic blob) | (2.0, 18.1) | (10.5, 29.9) | y=24 |
| Residential 1 | (14.5, 13.5) | (23.5, 28.0) | y=24 |
| Residential 2 | (2.0, 32.0) | (26.5, 46.5) | x=24 |
| Small commercial | (28.5, 28.0) | (35.5, 34.5) | no |
| Substation B | (34.0, 36.5) | (46.0, 45.5) | no |
| Industrial customer | (40.0, 25.0) | (47.0, 34.0) | no |
| DER solar array | (35.0, 12.5) | (46.8, 20.5) | no |

**Devices** - 7 boundary devices creating 6 zones, plus the DER PCC

| Tag | Class | Panel | x | y | Represents | Bounds | Normal |
|---|---|---|---|---|---|---|---|
| `SUB_A_BKR` | interrupting | Q3 | 12.00 | 10.00 | R-MAG 15 kV + SEL-351S | Z1 | CLOSED |
| `DEV_A1` | interrupting | Q3 | 12.50 | 18.00 | Padmount SG, VCB way | Z1/Z2 | CLOSED |
| `DEV_A2` | interrupting | Q1 | 12.50 | 29.50 | Padmount SG, VCB way | Z2/Z3 | CLOSED |
| `TIE` | restoring | Q2 | 26.50 | 25.50 | Padmount SG, switch way | Z3/Z4 | **OPEN** |
| `DEV_B2` | interrupting | Q2 | 31.00 | 25.50 | Padmount SG, VCB way | Z4/Z5 | CLOSED |
| `DEV_B1` | interrupting | Q4 | 38.00 | 22.00 | Padmount SG, VCB way | Z5/Z6 | CLOSED |
| `SUB_B_BKR` | interrupting | Q2 | 38.00 | 36.50 | R-MAG 15 kV + SEL-351S | Z6 | CLOSED |
| `DER_PCC` | must-trip | Q4 | 34.00 | 21.00 | IEEE 1547 PCC recloser | DER | CLOSED |

Mainline reads as a shallow S from the SW corner to the NE corner:

```
SUB_A_BKR -Z1- DEV_A1 -Z2- DEV_A2 -Z3- TIE -Z4- DEV_B2 -Z5- DEV_B1 -Z6- SUB_B_BKR
                                      (N.O.)
                    DER_PCC hangs off Z5 as a must-trip branch
```

Laterals do the area coverage so the mainline stays one readable path. Every zone drops
a load, so every fault is visible from across the room:

| Zone | Source | Load it drops | Panels |
|---|---|---|---|
| Z1 | A | Residential 1 south, lateral L1a, 4 houses | Q3 |
| Z2 | A | Residential 1 north, lateral L1b, 4 houses | Q1, Q3 |
| Z3 | A | Residential 2, lateral L2, 16 houses | Q1, Q2 |
| Z4 | B | Small commercial, lateral L3 | Q2 |
| Z5 | B | DER branch, lateral L4 via DER_PCC | Q2, Q4 |
| Z6 | B | Industrial customer, lateral L5 | Q2, Q4 |

**Buttons** - 7 fault plus reset

| Tag | Zone | Panel | x | y |
|---|---|---|---|---|
| `FLT_Z1` | Z1 | Q3 | 10.00 | 15.80 |
| `FLT_Z2` | Z2 | Q3 | 11.00 | 21.00 |
| `FLT_Z3` | Z3 | Q1 | 20.00 | 31.20 |
| `FLT_Z4` | Z4 | Q2 | 28.30 | 27.20 |
| `FLT_Z5` | Z5 | Q4 | 35.50 | 23.40 |
| `FLT_Z6` | Z6 | Q2 | 36.50 | 32.50 |
| `FLT_DER` | DER | Q4 | 32.20 | 19.00 |
| `RESET` | - | Q4 | 25.00 | 14.00 |

Each button is asserted to sit 1.0 to 3.5 in off the run it faults, on the same panel as
that run, outside every structure footprint and outside the pond.

**Model scale** - nominal **1:220 (Z scale)** for terrain and structures, which makes the
board represent roughly 880 x 880 ft. Substation yards land near-correct at that scale
(a 10.5 x 8.5 in yard is about a real 150 x 120 ft 46/12.47 kV yard). Devices are
deliberately over-scaled to roughly 1:60 so they are visible and can carry an indicator
LED. Distances between devices are schematic, not scaled. N-scale (1:160) hobby scenery
will read about 37 percent large against 1:220 structures, acceptable for trees.
**This is a proposal, not a decision.** `[I]`

### Wiring architecture

- **Center hub at (24, 24)** where all four panels meet. ESP32, 5 V supply and fuse block
  mount under Q4 beside the PLC, where line power already enters. One umbilical per panel
  runs under the board to a hub block. Assembly is: set panels on their registration
  dowels, plug in four connectors.
- **No conductor crosses a seam on the top surface.** Each panel chain is electrically
  self-contained.
- **Per-panel connector**, identical on all four: pins 1-2 +5V (18 AWG, doubled),
  3-4 GND (doubled), 5 LED_DATA (330-470 ohm series resistor at the strip end),
  6 BTN_COM, 7-8 button lines. 1000 uF across 5V/GND at each injection point.
- **Known gap:** Q4 carries three buttons (FLT_Z5, FLT_DER, RESET) and needs one more
  line than an 8-pin shell provides. Either go to a 10-pin shell on all four panels, or
  fit an MCP23017 GPIO expander per panel and drop to 6 pins (5V, GND, DATA, SDA, SCL,
  spare). The expander is the better call if the button count ever grows past about 12.

**LED budget at 60 LED/m**

| Panel | Route in | Route px | House px | Load px | Device px | Chain px | Inject |
|---|---|---|---|---|---|---|---|
| Q3 SW | 35.1 | 54 | 8 | 0 | 2 | 64 | 1 |
| Q1 NW | 58.8 | 91 | 15 | 0 | 1 | **107** | **2** |
| Q2 NE | 38.4 | 58 | 1 | 5 | 3 | 67 | 1 |
| Q4 SE | 25.2 | 37 | 0 | 4 | 2 | 43 | 1 |
| **Board** | **157.5** | 240 | 24 | 9 | 8 | **281** | 5 |

Total route 157.5 in = 4.00 m. Q1 is the only panel over 100 pixels, so it gets two
injection points. Full-white worst case is about 16.9 A at 5 V, but the animation is
single-color at partial brightness: budget about 5 A and spec one 5 V / 10 A supply.
Per-edge pixel counts at 30/m and 144/m are in the spec file so the strip density can
still change without touching the geometry.

**Seam crossings** - five, graphical only

| # | Point | Run | Zone | Panels | Cover prop |
|---|---|---|---|---|---|
| 1 | (12.50, 24.00) | Z2 | Z2 | Q3 / Q1 | Junction box |
| 2 | (24.00, 29.50) | Z3 | Z3 | Q1 / Q2 | Junction box |
| 3 | (24.00, 43.50) | L2 | Z3 | Q1 / Q2 | Junction box |
| 4 | (31.00, 24.00) | Z5 | Z5 | Q2 / Q4 | Junction box |
| 5 | (38.00, 24.00) | Z6 | Z6 | Q4 / Q2 | Junction box |

Strip stops 0.4 in short of the seam on each side and resumes past it, an 0.8 in gap.

**Props** - 24 total, generated from the route geometry rather than placed by hand, one
over every corner, splice and seam break per rule R2. Build note: corner props must be
open-bottom shells, or the corner made with a solderless 3-pin corner connector and the
prop set beside it. A solid prop over a lit corner blocks light; a solid prop over a seam
break or a splice does not, because there is no pixel at that point.

### FLISR state model

Generalized so any zone can be faulted, rather than hard-coding one scenario. Chain is
dev0 SUB_A_BKR through dev6 SUB_B_BKR; zone k lies between dev k-1 and dev k.

For a fault in zone f:

- A side is f <= 3, B side is f >= 4.
- Source-side boundary device (the one that trips) = dev f-1 on the A side, dev f on the B side.
- Far-side boundary device (the one that opens to isolate) = dev f on the A side, dev f-1 on the B side.
- Zones that lose their source = f through 3 on the A side, 4 through f on the B side.
- On restore, the tie closes and the stranded healthy zones flip to the other source.

Steps modeled: Normal, Fault, Lockout, Isolate, Restore.

**Bug found and fixed while building this.** The first version closed the tie
unconditionally on the restore step. That is wrong for a fault in **Z3 or Z4**, the two
zones that border the tie. In those cases there is no healthy load stranded beyond the
faulted zone, and closing the tie would energize the fault from the other source. That is
precisely the failure the component reference warns about ("if your logic ever closes the
tie into an un-isolated fault, that is a design failure"). The tie now only closes when
there is something to restore, and the page calls that case out explicitly as the check
the RTAC logic has to make before it restores. **Carry this into the RTAC logic and into
the ESP32 animation.**

### Deliverables produced

| Thing | Where |
|---|---|
| Interactive true-scale plan view | https://claude.ai/code/artifact/5ba6ca32-14a6-4a20-a69f-95a37753a51c |
| Machine-readable layout spec | `jea_tabletop_layout_spec.md` (working directory) |
| Geometry generator + assertions | scratchpad `build_layout.py` |
| Spec emitter | scratchpad `emit_spec.py` |
| Page template + data injection | scratchpad `plan.tpl.html`, `plan.html` |

The artifact has layer toggles (TERRAIN, STRUCTURES, ELECTRIC, DEVICES, ZONES, BUTTONS,
WIRING, FABRICATION) with FABRICATION off by default so the default view reads as one
seamless scene. It also has a steppable FLISR sequence: pick a zone, walk the five steps,
watch Residential 2 flip from blue to green on restore.

**The scratchpad is session-temporary.** If `build_layout.py` matters going forward, copy
it into the working directory. Right now the geometry survives in
`jea_tabletop_layout_spec.md` and in the published artifact, both of which are complete.

### Verification actually performed

Twelve assertion groups run in the generator before any file is written. Not eyeballed:

1. No LED route vertex, button, device or house inside the PLC keep-out.
2. No route segment parallel to a seam within 0.5 in of it.
3. Every corner, splice and seam break has a prop or device within 0.5 in.
4. Every zone Z1-Z6 has at least one lateral and a documented load.
5. Device chain runs SUB_A_BKR to SUB_B_BKR with no gaps; each zone run starts and ends
   exactly on its two bounding devices.
6. No two scene areas overlap each other or the PLC keep-out.
7. Everything inside the 48 x 48 board.
8. Per-panel route lengths sum to the board total.
9. Exactly 5 seam crossings, all perpendicular.
10. No button inside a scene area or the pond; each 1.0 to 3.5 in from its own zone run
    and on the same panel as that run.
11. Houses clear both seams by 0.4 in, do not overlap each other, stay inside their own
    subdivision.
12. No house, device or edge vertex inside the pond; no two devices within 1.5 in.

Assertions 10 and 11 were added mid-session and immediately caught four real defects:
`FLT_Z1` was inside the Substation A fence, `FLT_Z4` was on the wrong panel, two
Residential 1 houses overran the subdivision edge by 0.1 in, and a Residential 2 house
straddled the x=24 seam. All fixed.

### Explicitly out of scope this session

- ESP32 firmware, FastLED code, animation timing, button debounce. Different session.
- RTAC / IEC 61131 logic.
- HMI screen design.
- Milsoft model.
- Bill of materials.
- Structural design of the box, hinges, handles, sub-frame.

### Open items, flagged not resolved

1. **Scale sign-off.** 1:220 is a proposal. Zach offered to send physical dimensions of
   the actual gear so devices can be scaled properly. Ask for those. The SOW lists
   "Determine a model scale for the design" as a Phase 2 deliverable, so this needs an
   answer before PDR.
2. **Axion mounting orientation.** Manual requires modules vertical with 0.5 in clearance
   above and below; flat panel-mount lays them horizontal. Question for SEL or Michael.
3. **Cutout structure.** A 17.75 x 8.80 in hole in a 24 in panel leaves only a 2.0 in
   bridge at the front edge. Do NOT cut the cardboard mockup, just mark the rectangle.
   The final panel needs a sub-frame there.
4. **Panel registration.** The seamless read depends entirely on it. Two dowel pins per
   seam or a shared sub-frame, plus vinyl artwork printed as four tiles with the image
   continuing across each joint.
5. **Connector pin count.** 8-pin shell is one short for Q4. Decide between a 10-pin
   shell and an I2C expander.
6. Carried forward from `jea_oneline_component_reference.md`, still unanswered by JEA:
   whether JEA or TVA owns the 161/46 kV transformers; whether JEA's 46 kV is actually a
   normally closed loop or radial per substation (this changes whether "two independent
   sources" is an honest claim); whether the two 161 kV delivery points are electrically
   independent on TVA's mesh; and whether the Viper-ST should be shown with an SEL-651R
   recloser control rather than the SEL-351S currently on the one-line.

### Judgment calls worth remembering

- The mainline is kept as **one readable path** with laterals doing area coverage, rather
  than snaking the mainline through every subdivision. That is both how real feeders work
  and what keeps the board legible at 4 ft.
- Residential 1 is fed by **two laterals in two different zones**, so half the subdivision
  drops on a Z1 fault and the other half on a Z2 fault. Better teaching than one lateral.
- The tie sits 2 in west of the x=24 seam with its downstream side crossing it, so the
  blue-to-green handoff on restore happens exactly at a panel boundary. That was
  deliberate.
- The pond is not just decoration. It occupies the west side of Q3/Q1 and forces the
  A feeder to route east out of the substation, which is a realistic constraint and gives
  the corridor between pond and subdivision a reason to exist.
- Roads carry every LED run, because Zach said underground primary runs "mostly along the
  roadways."

---

## 2026-09-07 21:56 CDT - Import: claude.ai project memory export (separate session, "Power Line Fault Control System")

### What this is

The user pasted a memory export from a **different Claude session/tool** (the claude.ai
project-memory feature, project id `019dbb5e-0528-766a-906b-8f8d1812fc0b`, project named
"Power Line Fault Control System"), covering the same JEA capstone from that session's
independent line of work, and asked for it to be folded into this file. This was not
generated in this working directory's session. It is transcribed here for continuity, not
verified against the source files in this session. Where it conflicts with the Standing
Facts above or the 2026-09-07 21:46 log entry, both are left standing per this file's own
rule: newer does not silently overwrite older, contradictions get flagged, the reader
decides which is current.

**Two contradictions worth flagging up front, in bold, before the detail:**

1. **PLC/HMI placement conflict.** The physical layout entry above (21:46 CDT) puts the
   SEL-2240 Axion flat on the tabletop in the SE corner, with a 17.75 x 8.80 in panel
   cutout, on the theory that surface clearance is what matters now and under-board depth
   is a later problem. This imported memory states flatly: **"The Axion chassis cannot
   fit within the table height envelope, it must be housed in a separate vertical
   relay panel module as a fifth transport piece."** If that is correct, the entire SE
   quadrant of the 21:46 layout (PLC keep-out, DER array position relative to it, the
   button cluster at FLT_Z5 / FLT_DER / RESET) needs to be redone around a **separate
   relay panel enclosure**, not a tabletop cutout, and the "fifth transport piece" framing
   also changes the portability story from "four panels" to "four panels plus a relay
   rack." This needs resolving before the layout in the artifact/spec file is treated as
   final. Not resolved here, just flagged.
2. **DI budget claim conflict.** This import states fault zone count is "constrained by
   the 6 DI budget for fault injection." `jea_oneline_component_reference.md` (read in
   the 21:46 session) explicitly corrects this exact belief: the SEL-2244-2 module
   provides 24 optoisolated DI, the SEL-2244-4 provides 32, and "the 6 DI budget is not
   a hardware limit... Digital outputs are your tight resource, at 16 per SEL-2244-3."
   Both claims are now on record. If "6 DI" was a hard sponsor-stated number from Zach
   (as opposed to an assumed constraint), that supersedes the component-reference
   analysis; if it was this project's own earlier assumption, the component reference is
   the correction. Worth a two-minute check against whichever session's history has the
   provenance.

Content below is transcribed from the export, organized under the export's own file
names, with `[stated]` markers preserved from the source (their marker for
self-reported/assumed fact, not independently verified by that session either).

### From index.md

- Project name in that tool: "Power Line Fault Control System." Description there:
  "Senior capstone with JEA: a tabletop FLISR distribution-automation demo trainer using
  SEL hardware."

### From overview.md

- **Team is three people, named:** Jordan Prunty (team lead, main point of contact),
  Gage, and Cody. Jordan holds primary responsibility for hardware, physical design, CAD
  and circuit work; PLC/firmware logic ownership sits with a teammate, described as an
  intentional split.
- **Faculty advisors named as Dr. Pingen and Dr. Schwindt.** This resolves the garbled
  "Dr. Schwintz / Dr. King" name pair carried in the Standing Facts section above from
  the 8/27 transcript audio. Treat "Pingen and Schwindt" as the more reliable transcription
  and "Schwintz / King" as the noisy one, pending confirmation.
- Sponsor mentor confirmed as Zach Wadley, PE, JEA. Preferred channel is email first, then
  in-person at the JEA plant, Teams as fallback.
- Deliverable framed as a 4 by 4 foot modular tabletop display, four 2 by 2 foot panels
  using 1 inch by 1 inch aluminum extrusion frames. The extrusion frame detail is new,
  not present in this session's sources.
- End users: new JEA hires to broader educational audiences.
- Domain area list given there matches this session's independent reading: generation to
  transmission to subtransmission to primary distribution to utilization, FLISR logic,
  SEL-2240 Axion, AcSELERATOR, SCADA concepts, addressable LEDs, ESP32, modular mechanical
  design.
- **Schedule gates, more granular than this session had:** long-lead POs by
  approximately 2026-11-06; a successful end-to-end FLISR run targeted for approximately
  2027-02-26; hard project completion approximately 2027-04-06 (matches the UU event /
  demo day date already on record). The window 2026-10-26 to 2026-11-20 is called out as
  the most overloaded stretch of the schedule.
- **Controller platform note:** confirmed as SEL-2240 Axion, not SEL RTAC, described as
  an important distinction to maintain. Worth noting the 8/27 transcript itself uses
  "RTAC" as the colloquial term for the Axion's automation-controller role throughout
  (Michael and Zach both say "RTAC" repeatedly when apparently describing the Axion
  platform), so this may be a terminology cleanup this session's team did after the
  kickoff rather than a contradiction of what JEA actually shipped. Keep both terms in
  mind when reading the transcript.
- Open backplane-slot question: whether RTAC and power coupler consume backplane slots,
  which decides 4-slot vs 10-slot chassis and therefore enclosure size. Directly relevant
  to the PLC-placement contradiction flagged above, since a 10-slot chassis is the one
  whose cutout dimensions (17.75 x 8.80 in) this session's layout already used.
- Open items for Zach, as tracked in that session: written confirmation on 120 VAC scope
  (mains to relay panel only, versus distributed across the tabletop); JEA PO turnaround
  time; vendor lead times on Axion/RTAC; whether the SEL-2240 and an RTAC module are
  separate purchases.
- **The 4x4 footprint is flagged there as Jordan's own assumption, not something Zach
  stated explicitly**, consistent with this session's treatment of the same footprint as
  an assumption in the 21:46 layout entry's Assumptions list.
- As of that session's snapshot (approximately first week of October prep for PDR): one
  line topology was the most time-sensitive open decision, with a recommended
  architecture of two distribution substations at opposite corners, radial feeders toward
  the middle, one normally-open tie in the middle, which is the same shape the 21:46
  layout entry independently arrived at and then dressed with real geometry, devices, and
  a wiring plan.
- Fault zone count noted there as four to six, undecided at that snapshot; this session's
  21:46 entry locked it at six backbone zones plus the DER, per this session's own user
  decision.
- DER confirmed in scope per SOW; industrial customer branch flagged unconfirmed in that
  session (this session's SOW reading did not flag the industrial branch as ambiguous,
  and the user's own 21:46 layout request explicitly included one industrial customer as
  a requirement, so treat industrial-branch scope as settled by the user's direct
  instruction in this session, regardless of that open item).
- A **parallel, separate concept** is tracked there: a 3D visualization / web-based
  gamified fault-response trainer, stack noted as Three.js, Vite, Cloudflare Pages, with a
  Blender to GLB export pipeline and a Blender MCP plugin setup pending. This has not come
  up anywhere in this session and may or may not still be active; flagging its existence
  in case it resurfaces.

### From design-decisions.md (locked/recommended in that session)

**LED architecture**

- WS2812B (5 V) recommended over WS2815 for short segmented runs.
- Recommended hybrid build: off-the-shelf WS2812B strip in routed channels under a
  frosted acrylic diffuser for line runs; small custom node PCBs for houses and key
  components; one custom panel-controller PCB per panel carrying an ESP32, a level
  shifter, a buck converter, and optocouplers, plus terminal blocks.
- Full-panel-scale custom PCBs were evaluated and rejected: they exceed JLCPCB's standard
  panel dimensions, carry flex-induced solder-joint cracking risk, and were premature
  before the topology was frozen. Small targeted custom boards were judged higher value
  than one large board per panel.
- **Important electrical distinction carried in that session and not yet reflected in
  this session's layout:** WS2812B is a shift-register architecture, so a hard power cut
  mid-chain causes downstream pixel data loss. Their stated fix is architectural: keep a
  separate, switched 24 VDC segment bus (driven by Axion DO contacts, representing
  whether that feeder segment is actually energized) fully independent from a
  permanently-powered 5 V LED layer. One ESP32 per panel senses which segments are
  energized via optocouplers reading the 24 V bus, and renders the animation state from
  that sensed input rather than from the LED power itself ever being switched. **This is
  a materially different electrical concept from anything specified in the 21:46 layout
  entry**, which assumed each panel's LED chain is just always-on 5 V and animated
  directly by the ESP32's own logic. If this segment-bus approach is still the design
  direction, the wiring architecture and connector pin count in the 21:46 entry (5 V,
  GND, DATA, button lines) need an additional 24 V sense pair per panel, and the harness
  section of `jea_tabletop_layout_spec.md` would need a revision pass.
- SEL-2244-3 DO contacts cited as unable to directly switch 5 V LED power: 0.75 A
  breaking capacity, 19.2 V minimum rating, which is exactly why the above segment-bus /
  sensing split exists rather than switching LED power directly off the Axion.

**Electrical architecture**

- Distribute 24 V to panels and buck down to 5 V locally at each panel, to avoid voltage
  drop over the run length.

**Mechanical**

- (Repeating the flagged contradiction above for completeness in this subsection) Axion
  chassis needs a separate vertical relay panel module, a fifth transport piece, because
  it does not fit the table height envelope.
- Star wiring topology back to the relay panel, recommended over daisy-chaining between
  panels.
- Seam registration: tapered dowel pins plus separate latches. This is compatible with,
  and slightly more specific than, the two dowel pins per seam or a shared sub-frame
  open item already listed in the 21:46 entry.
- **Connector spec: Neutrik XLR XX-series 4-pin, rated for over 1,000 mating cycles, for
  inter-panel connections.** The 4-pin count was chosen deliberately, and a 4-pin XLR
  also happens to avoid accidental mating with audio equipment. **This conflicts with the
  21:46 entry's harness design**, which specified a generic 8-pin connector (5V x2, GND
  x2, DATA, BTN_COM, BTN_1, BTN_2) per panel, later noting an 8th pin was already tight
  for Q4's three buttons. A 4-pin XLR cannot carry that many discrete signals unless the
  design multiplexes buttons onto fewer physical conductors (for example an I2C or
  single-wire bus rather than discrete GPIO per button, or moving button sensing onto
  each panel's own ESP32 rather than back to a central hub). The 21:46 entry already
  floated an MCP23017 I2C expander as an alternative if the button count grows past about
  12; a 4-pin XLR effectively forces that expander approach (or something equivalent)
  regardless of button count, since a 4-pin connector realistically carries 5V, GND, and
  a two-wire bus (I2C, or 1-wire data plus its return), not eight discrete lines.
- Connector choice was reached by calculating realistic service-life cycle count first,
  which eliminated Deutsch DT and Molex Mini-Fit Jr in favor of the Neutrik XLR.

### From domain-principles.md

- **Topology before geometry**, stated as a design principle: freeze the one-line fault
  zone topology before locking physical panel geometry or purchasing custom PCBs, and
  align module seams with protective/switching devices where possible. Note the 21:46
  layout entry deliberately does the opposite for aesthetics (rule R1, composition
  ignores seams) at the user's explicit direction in this session; these are not
  actually in conflict, they are answering different questions (electrical seam alignment
  vs visual composition seam alignment), but worth having both principles in view at once
  since they pull in different directions on where a device physically sits relative to a
  panel edge.
- Never conflate real power delivery (120 VAC to the Axion, low-voltage DC to the LEDs)
  with simulated feeder power flow (the blue/green/red animation state), stated there as
  a core design constraint. Consistent with everything in this session; worth keeping
  explicit since the segment-bus idea above is exactly this principle taken to its
  electrical conclusion (the LEDs are never actually carrying the power, they are
  driven by a sensed proxy of it).
- Tie point placement confirmed correct there: the normally-open tie belongs between two
  distribution feeders, never between GSU transformers, same conclusion independently
  documented in this session's `jea_power_delivery_oneline_reference.md`.
- Pad-mounted transformers are passive and cannot isolate faults; pad-mounted switchgear
  with VCB compartments is the real isolation device in underground FLISR, matches this
  session's component reference exactly.
- FLISR sequence as stated there matches this session's independently-built state model:
  fault, then the upstream interrupting device trips, then sectionalizing devices isolate
  the faulted segment during the dead interval, then the upstream device recloses
  restoring the healthy upstream section, then the normally-open tie closes restoring the
  healthy downstream section from the alternate source.
- Model the network as a graph (node/edge tables) for fault-simulation logic, not as
  Cartesian coordinates; coordinates are for visualization only, topology drives the
  computation. This is exactly the approach `build_layout.py` takes in this session (the
  adjacency graph in the spec file's section 5 is separate from the coordinate geometry
  used for drawing).
- Arriving at Zach meetings with specific, topology-grounded questions rather than
  open-ended ones was noted there as something that measurably compresses the timeline;
  positions Jordan as validating a decision rather than opening a discovery conversation.
  Worth applying to the open items list already on record in this file (owner question,
  DI budget provenance, PLC placement): bring those as closed-ended yes/no/which-one
  questions to Zach or Michael rather than open questions.

### From working-style-and-tools.md

**How the user wants to work, per that session (treat as still-current user preference
unless contradicted by behavior observed in this session):**

- Prefers to thoroughly discuss and plan before executing, deliberate, discussion-first
  collaboration before any building or coding. Consistent with this session's own
  experience: the user rejected the first draft of the physical layout plan and asked for
  a rework before any artifact was published, and the work went through Plan Mode with an
  explicit approval step before execution.
- Works through new domain material one topic at a time, methodically, and asks for
  explicit correction of misconceptions when they occur.
- Gives constraints incrementally and expects the assistant to manage the resulting
  logic, flag risks, and proactively surface important context without being asked.
  Consistent with how the four clarifying questions were handled in this session
  (recommended options first, with rationale) and with the 21:46 entry's practice of
  flagging contradictions rather than silently resolving them.
- Communication style: terse and directive, prefers concise responses with a clear
  recommendation over an exhaustive menu of options.
- **Wants to proceed directly to full-scale implementation without intermediate
  small-scale prototypes**, stated there as a preference that should not be revisited or
  re-litigated. Relevant if a future session is tempted to suggest a single-panel proof
  of concept before committing to all four.
- Cross-references guidance against datasheets and sponsor documents, and appreciates
  explicit confidence levels on inferences, matches this file's own confidence-marker
  convention and the component reference's confidence tagging, both already in use here.

**Tools and resources tracked there:**

- SEL hardware: SEL-2240 Axion, SEL-2244-2/4 (DI modules), SEL-2244-3 (DO modules),
  SEL-351S relay. SEL-2240 datasheet on file.
- Software: AcSELERATOR Diagram Builder / RTAC, LibreCAD (for the one-line diagram),
  Fusion 360 (CAD / 3D modeling), NetworkX (Python graph library, for the topology graph
  work), Milsoft LightTable (power flow modeling, described there as Zach's tool, matches
  the Milsoft references already in this session's SOW and component reference).
- Embedded/electronics: ESP32, WS2812B strips, 74HCT245 / 74AHCT125 logic-level shifters,
  optocouplers, Neutrik XLR XX-series connectors.
- Web stack for the parallel 3D/gamified trainer concept: Blender, Three.js, Vite, GitHub,
  Cloudflare Pages, GLB export pipeline, Blender MCP plugin (setup pending).
- Fabrication: JLCPCB for PCB fab, 1010-series aluminum extrusion, frosted acrylic
  diffuser.
- That session's project files were mounted at `/mnt/project`: scope of work document,
  kickoff transcript, a PowerPoint export, and a concept image, the same source family
  this session read directly from the working directory (the Scope of Work docx, the
  8/27 meeting transcript, the Tabletop Smart Grid REV2 pptx, and the AI concept png).

### Not included in the export, per its own footer

The export explicitly excluded account-level memory outside this project's subtree:
profile and preferences files, 16 other area files, 6 topic files, and 8 other project
subtrees (Plastination, Gantry, Rubik's Cube, Chess Robot, Portfolio, Robotic Arm, Atlas,
Wabtec) unrelated to this capstone. Noted here only so a future reader knows those exist
elsewhere and were deliberately not pulled in.

### Net effect on open items

Adds to the open-items list already on record:

7. **Resolve PLC/relay-panel form factor before treating the 21:46 physical layout as
   final.** Flat tabletop cutout (this session) versus separate vertical relay panel as
   a fifth transport piece (imported memory). These are not reconcilable without a
   decision; whichever is correct changes the SE quadrant of the layout materially.
8. **Resolve the 24V segment-bus / optocoupler-sensing LED architecture** against the
   simpler always-on-5V-chain-animated-directly-by-ESP32 architecture assumed in the
   21:46 harness design. Determines whether each panel needs a 24V sense pair in addition
   to 5V/GND/DATA/buttons.
9. **Resolve connector choice**: Neutrik XLR 4-pin (imported memory, chosen on cycle-life
   grounds) versus the generic 8-pin shell or MCP23017-expander 6-pin scheme in the 21:46
   entry. A 4-pin choice effectively mandates a bussed (I2C or similar) scheme for buttons
   and any sense lines, not discrete GPIO per signal.
10. **Confirm current team roster and faculty advisor spelling.** Gage and Cody as
    teammates, Dr. Pingen and Dr. Schwindt as advisors, against whatever this session's
    own conversation history or documents say, since this session had not previously
    captured teammate names at all and had the advisor names garbled from transcript
    audio.
11. **Check provenance of the 6 DI budget constraint.** Sponsor-stated hard number, or
    this project's own earlier working assumption that the component reference doc
    already argued against.

---

## 2026-09-10 00:20 CDT - Fault realism check, and locked decisions on buttons/fault points/overhead

### What was asked

User referenced the published artifact and re-read the 8/27 transcript to check two things:
whether "all underground" is something JEA actually specified, and whether a fault can
plausibly occur mid-cable underground with no junction box nearby, or whether the layout's
mid-line fault buttons are unrealistic. A second message then locked in specific button and
fault-point design decisions in response to that discussion.

### Findings, from re-reading the 8/27 transcript directly this session

- **Confirms the user's recollection** `[V]`: "There is not a single house in Jackson that
  is not overhead between somewhere between there and the substation." Zach named 2-3
  specialized industrial customers as the only fully-underground exceptions.
- **Correction flagged against this file's own Standing Facts.** The "Underground focus"
  bullet above (Sponsor intent, ~line 52) is tagged `[V]` but overclaims. What the
  transcript actually verifies is a pad-mount-switchgear focus and an underground
  subdivision example ("just think of it just like an underground subdivision"), not a JEA
  mandate that the whole board be modeled underground. JEA's own plan is to price the same
  one-line **both** overhead and underground as a teaching exercise about cost, which cuts
  against reading "underground focus" as an all-underground requirement. That bullet should
  be read as "underground SWITCHGEAR focus," not "all-underground topology," until reworded.
  Not reworded this session, flagged for a future pass.
- **Physics check, the user's core question.** `[S]`, standard industry knowledge, not
  JEA-specific: mid-cable faults with no junction box nearby are not rare underground, they
  are the dominant real-world failure mode (dig-ins, water treeing / insulation breakdown in
  aged XLPE or EPR, mechanical damage at bends). The user's working premise going in ("is it
  near impossible for a fault to occur mid-cable underground") was backwards; the layout's
  mid-line fault buttons are realistic, not a modeling shortcut. What IS genuinely different
  underground is permanence: underground faults are overwhelmingly permanent (no self-
  clearing arc), versus overhead's roughly 70-80% temporary-fault rate that clears on reclose.
- **Flagged, not acted on.** The published artifact's step-02 narration cites the overhead
  70-80% reclose-success statistic as the reason this trainer models permanent (underground-
  style) faults. Left as-is; no edit to the artifact was requested or made this session.

### Decisions locked in this chat

1. **Fault-injection buttons stay scattered**, positioned adjacent to the zone/run each one
   faults, not clustered into a legend panel. Assistant had proposed clustering near the
   legend for legibility; user rejected that, on two grounds: proximity to the faulted run is
   the more intuitive interaction and is already how the layout was built, and for the PDR
   pitch, demonstrating the harder-to-picture scattered design (versus the easy-to-imagine
   clustered one) is the stronger evidence the thing actually got built. `[V]` No layout
   change needed, this affirms the existing button table in section 6 of the spec.
2. **Fault location per button is FIXED, not randomized**: the point of fault is the closest
   point on that button's assigned run. Assistant had proposed randomizing the visible fault
   point within a zone on each press, to reinforce "the system resolves a fault to a segment,
   not a point." User rejected randomization: a small, finite, deterministic set of fault
   points is an intentional and acceptable simplification for a physical trainer, and it
   tracks Zach's own words better anyway ("once you press that button, what it does in the
   RTAC more or less be hard-coded for each scenario... injecting faults and seeing that,
   that's gonna be funky"). `[V]`
   - Checked against the actual button/device coordinates in the published layout: every
     button already sits roughly mid-zone, not snapped to a device, so fixing the fault point
     at "closest point on the run" does not visually collapse the fault onto a device and the
     segment-resolution lesson survives. `FLT_DER` sits closest to its device at about 2.7 in;
     worth an eyeball once built, not a blocker.
   - A build note surfaced while checking this: "closest point on the run" is ambiguous
     wherever the backbone bends near a button (flagged for Z3, Z5, Z6 in the prior session's
     design; confirmed by computing actual distances, below). Each button needs to bind to
     one explicit edge ID, not a geometric nearest-run lookup computed at build or render
     time. Added to `jea_tabletop_layout_spec.md` section 6, including a first-pass table of
     computed nearest edges and the two cases (`FLT_Z1`, `FLT_Z4`) that are genuine ties
     needing a human pick.
3. **Overhead mainline modeling is DEFERRED.** Staying all-underground for now. This is the
   user's own call, not something JEA resolved either way. Worth revisiting before the BOM
   exercise, since JEA's stated plan is to cost the same one-line both overhead and
   underground, and before/around a Standing Facts reword per the correction noted above.

### Not done this session

- No changes to the published artifact (`https://claude.ai/code/artifact/5ba6ca32-14a6-4a20-a69f-95a37753a51c`)
  or to any generator script. Only `PROJECT_MEMORY.md` and `jea_tabletop_layout_spec.md`
  were touched.
- Standing Facts "Underground focus" bullet not reworded, flagged above for later.
- Artifact step-02 narration (uses an overhead statistic to justify underground-modeled
  lockout) not fixed, flagged above for later.

---

## 2026-09-13 21:22 CDT - Arduino Uno FLISR firmware built from the REV1 DXF and tabulated Excel

Session ran from the evening of 2026-09-12 into 2026-09-13, over four user messages.

### What was asked

1. **Build complete Arduino code for the automated fault restoration system**, from three
   sources the user named:
   - Restoration logic: the published artifact
     `https://claude.ai/code/artifact/5ba6ca32-14a6-4a20-a69f-95a37753a51c`. The code must
     follow the same redirect logic.
   - Geometry: `Cardboard Layout REV1 backup_9.12.20.dxf`, full scale, inches.
   - Ground truth alongside the DXF: `JEA Cardboard Prototype Tabulated REV1.xlsx` (the user
     called it "...Tabulated.xlsx"; the file on disk carries REV1). It tabulates elements and
     nodes by x/y, lines by their two nodes, fault points as the point ON the run, and LED
     runs by pixel count, an Over flag, and From/To nodes.
   - Origin (0,0) is the bottom-left corner of the model in both files.
   - Requirements: every fault button pin listed at the top of the sketch so it can be
     changed; every LED run length listed at the top so a miscount can be fixed in one
     place; 60 LED/m.
   - User notes on the tabulation: all surface runs are exactly horizontal or vertical
     EXCEPT line 21, which is diagonal; lines 24 and 25 appear to jump nodes on purpose, so
     assume a wire jumper N28 -> N27 between them with 0 LEDs; nodes that should share an
     x or y but are slightly off are to be treated as exactly aligned.
2. User updated the Excel "to correct inter panel nodes": check what changed and adjust.
3. User confirmed N30 belongs at DEV_A2 (correct and adjust), and that LED run 1 is 9 px
   from N1 to N2 plus 8 px that extend south, 17 total.
4. Write this whole chat to memory. **Standing instruction from now on: for this project,
   always write session work into this file and reference it in future chats, without
   being asked.** Also saved as a Claude Code persistent memory at
   `C:\Users\jprun\.claude\projects\c--Users-jprun-Downloads-JEA-Project\memory\` so it
   loads automatically at the start of future sessions.

### Sources read this session

- The artifact, full raw HTML through the Artifact read action, including its `model()` and
  `narrate()` JavaScript. `[V]`
- `Cardboard Layout REV1 backup_9.12.20.dxf`, parsed with a throwaway Python group-code
  parser. Layers that matter: `Cardboard Layout REV0 v8_Sketch3` holds the 27 LINE entities
  of the electrical network; `...Sketch5` holds 8 CIRCLE r=0.50, the 7 fault buttons plus
  RESET; layer `0` holds the device blocks (LWPOLYLINE), all MTEXT labels, and the small
  breaker-symbol circles at Substation A. `[V]`
- `JEA Cardboard Prototype Tabulated REV1.xlsx` in the working directory, sheets Element,
  Node, Line, Fault, LED. Read at the start, then twice more as the user edited it. `[V]`
- A second copy of the same workbook at
  `C:\Users\jprun\OneDrive - Union University\JEA Tabletop Fault Simulator\Jordan Prunty\JEA Cardboard Prototype Tabulated REV1.xlsx`.
  The two copies have diverged; see node corrections below. `[V]`

### Reading the tabulation

**Element -> device.** Matched by position against the DXF device blocks and the artifact's
device schedule. `[V]`

| Element | Device | x, y (Excel) |
|---|---|---|
| E1 | SUB_A_BKR | 12.59, 9.12 |
| E2 | DEV_A1 | 12.59, 17.58 |
| E3 | DEV_A2 | 12.59, 29.38 |
| E4 | TIE, normally open | 26.55, 25.50 |
| E5 | DEV_B2 | 30.08, 25.50 |
| E7 | DEV_B1 | 38.10, 21.91 |
| E6 | SUB_B_BKR | 38.10, 37.44 |
| R1 | DER_PCC | 34.15, 20.65 |

- **E6 and E7 are numbered out of chain order.** Electrical order from Source A to Source B
  is E1, E2, E3, E4, E5, **E7, E6**. `[V]`
- E-points are markers near each block, not always its center. The SUB_A_BKR block spans
  y 9.4 to 10.5 (center 9.95, which is exactly N1's y); the DEV_B2 block spans x 30.5 to
  31.7. `[V]`

**Fault points and buttons.** The Fault sheet gives the point on the run; the DXF Sketch5
circles give the physical button. Every fault point lies between its zone's two bounding
devices, which independently confirms the device mapping above. `[V]`

| Fault | Point on run (Excel) | Button center (DXF) |
|---|---|---|
| Z1 | 12.59, 15.84 | 10.09, 15.85 |
| Z2 | 12.59, 21.05 | 11.11, 21.09 |
| Z3 | 20.10, 29.50 | 20.11, 31.27 |
| Z4 | 28.40, 25.50 | 28.40, 27.26 |
| Z5 | 35.60, 21.90 | 35.60, 23.50 |
| Z6 | 38.13, 32.55 | 36.60, 32.57 |
| DER | 34.10, 19.10 | 32.26, 19.07 |
| RESET | none | 26.46, 5.13 |

**"Line 21" and "lines 24 and 25" meant LED sheet IDs, not Line sheet IDs.** On the Line
sheet, L21 (N20 -> N22) is vertical and L24/L25 share a node. On the LED sheet, LED 21
(N13 -> N35) is the only diagonal surface run, and LED 24 ends at N28 while LED 25 starts at
N27. Both of the user's notes check out exactly under that reading. `[V]` for this session.
As a general rule, a numbered "line" in a lighting context probably means the LED sheet.
`[I]`

**The strip is ONE continuous data chain.** Every LED row's To node is the next row's From
node, the J1 jumper being the only jump. Rows with Over = 0 run back under the display to
reach a branch point, which is how the branching looks seamless on top. `[V]`

**Not lit:** the four DER solar stub laterals (Line sheet L23 to L26: N18 -> N19,
N20 -> N21, N22 -> N23, N24 -> N25) and the horizontal leg of the commercial lateral have no
LED rows. The DER feeder trunk and the commercial riser are lit. `[V]`

### The LED chain and zone mapping, as built

Generated from the final sketch tables and cross-checked row by row against the Excel LED
sheet: pixel counts and Over flags agree on all 31 rows. "Row" is the sketch table row;
"LED ID" is the Excel ID. `[V]`

| Row | LED ID | px | Over | From -> To | Strip index | Zone |
|---|---|---|---|---|---|---|
| 1 | 1 | 17 | 1 | N1 -> N2 | 0-16 | BUSA 8 px, then Z1 9 px |
| 2 | 2 | 17 | 1 | N2 -> N3 | 17-33 | Z1 |
| 3 | 3 | 17 | 0 | N3 -> N2 | 34-50 | hidden (under board) |
| 4 | 4 | 10 | 1 | N2 -> N4 | 51-60 | Z1 2 px, then Z2 8 px |
| 5 | 5 | 17 | 1 | N4 -> N5 | 61-77 | Z2 |
| 6 | 6 | 17 | 0 | N5 -> N4 | 78-94 | hidden (under board) |
| 7 | 7 | 2 | 1 | N4 -> N32 | 95-96 | Z2 |
| 8 | 8 | 9 | 1 | N32 -> N30 | 97-105 | Z2 |
| 9 | 9 | 6 | 1 | N30 -> N6 | 106-111 | Z3 |
| 10 | 10 | 8 | 1 | N6 -> N7 | 112-119 | Z3 |
| 11 | 11 | 11 | 1 | N7 -> N8 | 120-130 | Z3 |
| 12 | 12 | 14 | 1 | N8 -> N9 | 131-144 | Z3 |
| 13 | 13 | 28 | 1 | N9 -> N10 | 145-172 | Z3 |
| 14 | 14 | 26 | 0 | N10 -> N6 | 173-198 | hidden (under board) |
| 15 | 15 | 12 | 1 | N6 -> N33 | 199-210 | Z3 |
| 16 | 16 | 4 | 1 | N33 -> N11 | 211-214 | Z3 |
| 17 | 17 | 6 | 1 | N11 -> N12 | 215-220 | Z3 |
| 18 | 18 | 6 | 1 | N12 -> N13 | 221-226 | Z4 |
| 19 | 19 | 9 | 1 | N13 -> N14 | 227-235 | Z4 |
| 20 | 20 | 10 | 0 | N14 -> N13 | 236-245 | hidden (under board) |
| 21 | 21 | 3 | 1 | N13 -> N35 | 246-248 | Z4 1 px, then Z5 2 px |
| 22 | 22 | 22 | 0 | N35 -> N29 | 249-270 | hidden (under board) |
| 23 | 23 | 12 | 1 | N29 -> N27 | 271-282 | Z6 |
| 24 | 24 | 4 | 1 | N27 -> N28 | 283-286 | Z6 |
| 25 | J1 | 0 | 0 | N28 -> N27 | - | wire jumper, no pixels |
| 26 | 25 | 7 | 1 | N27 -> N34 | 287-293 | Z6 |
| 27 | 26 | 4 | 1 | N34 -> N26 | 294-297 | Z6 |
| 28 | 27 | 12 | 1 | N26 -> N16 | 298-309 | Z5 |
| 29 | 28 | 3 | 1 | N16 -> N35 | 310-312 | Z5 |
| 30 | 29 | 11 | 0 | N35 -> N17 | 313-323 | hidden (under board) |
| 31 | 30 | 13 | 1 | N17 -> N24 | 324-336 | Z5 2 px, then DER 11 px |

Totals: **337 px**. Visible 234: BUSA 8, Z1 28, Z2 36, Z3 89, Z4 16, Z5 19, Z6 27, DER 11.
Hidden 103. `[V]`

**Zone assignment rules used.** The protection chain is SUB_A_BKR, DEV_A1, DEV_A2, TIE,
DEV_B2, DEV_B1, SUB_B_BKR, and zone Zk lies between device k-1 and device k. A run belongs to
the zone between the devices on either side of it. A lateral belongs to the zone of the trunk
point it taps. The commercial lateral (LED 19) rises at x = 30.125, upstream of the DEV_B2
block, so it is Z4, matching the artifact's L3. The industrial lateral (LED 24) is Z6,
matching the artifact's L5. `[V]`

**Four runs cross a boundary partway and are split.** The first N pixels take the first zone
and the rest take the second. Split points were placed from DXF geometry at 60 LED/m, which
is 1.524 px per inch. `[V]`

| LED ID | Crosses | Geometry | Split |
|---|---|---|---|
| 1 | SUB_A_BKR at N1 | 8 px south of N1 inside the substation, then N1 -> N2 = 6.08 in | BUSA 8 / Z1 9 |
| 4 | DEV_A1 | N2 y 16.04 -> N4 y 22.52, device at about y 17.45, 21.7% along | Z1 2 / Z2 8 |
| 21 | DEV_B2 | diagonal from x 30.125 enters the device block about 39% along | Z4 1 / Z5 2 |
| 30 | DER_PCC | N17 y 21.93 -> N24 y 13.57, recloser at y 20.745, 14.2% along | Z5 2 / DER 11 |

No split is needed anywhere else, because every other device lands exactly on a node: DEV_A2
on the N30 corner between LED 8 (Z2) and LED 9 (Z3); the TIE at N12 between LED 17 and 18;
DEV_B1 at N26 between LED 26 and 27; SUB_B_BKR at N29, where LED 23 starts. `[V]`

### Node corrections this session

Supersedes the node coordinates first read at the start of this session.

| Node | Was | Now | Status |
|---|---|---|---|
| N32 | 26.55, 24 | 12.57, 24.0 | Fixed by user, in both Excel copies. `[V]` |
| N1 | 25.58, 9.95 | 12.57, 9.95 | Fixed by user in the **OneDrive copy only**. The newer working-directory copy still has 25.58. `[V]` |
| N30 | 21.58, 29.5 | 12.59, 29.51, the DEV_A2 corner | Confirmed by user. **Not yet written to either Excel copy.** `[V]` |

How these were found: a script compared each LED run's counted pixels against its
node-to-node distance at 60 LED/m. On the original coordinates, 23 of 30 runs landed within
+/-1.3 px, which is ordinary hand-count rounding. The 7 outliers pointed at bad coordinates:

- **N32:** LED 7 predicted 21.4 px against 2 counted. At x = 12.57 it predicts 2.2. The Z2
  trunk crosses the y = 24 seam at about x = 12.57, not 26.55.
- **N30:** with N32 already fixed, LED 8 predicted 16.1 px against 9 counted and LED 9
  predicted 8.3 against 6. At the DEV_A2 corner they predict 8.4 and 5.4. Two independent runs
  both landing within 0.6 px settled it before the user confirmed. DXF Sketch3 lines 7 and 8
  meet at exactly (12.586, 29.510).
- **N1:** its y matched the breaker block center, but its x was 13 in east, inside the RTAC
  cutout area. Once corrected, LED 1 measured only 9.3 px against 17 counted, which the
  user explained: the extra 8 px extend south.

All four inter-panel (seam) nodes are now correct: N32 (12.57, 24.0), N33 (24, 29.48),
N34 (38.13, 24), N35 (31.09, 24). `[V]`

### Decisions taken

User answers to four questions asked before any code was written:

1. **Board: Arduino Uno / Nano (ATmega328P).** `[V]` **Supersedes** the ESP32 assumption
   in the 2026-09-07 21:46 entry ("Carry this into the RTAC logic and into the ESP32
   animation", and HUB ESP32 + 5V in the artifact's wiring layer), at least for the cardboard
   prototype.
2. **Sequencing: auto-timed, with a manual step.** `[V]` Press a fault button to start that
   fault at step 01. Steps advance every 2.5 s. `AUTO_ADVANCE 0` turns the timer off for pure
   manual stepping.
   - **Deviation from the option as worded.** The option the user picked described RESET
     also acting as a manual step button. It was built instead so that pressing the **same
     fault button again** advances one step, a **different** fault button abandons the
     current fault and starts that one, and RESET only returns to NORMAL. That keeps RESET
     unambiguous. It is documented in the sketch header's OPERATION block but was not called
     out in chat until the memory-writing turn, where it was flagged to the user.
3. **Device status: separate discrete LEDs**, not the WS2812 strip. `[V]` Hardware conflict
   found and resolved: bicolor red + green for 8 devices is 16 pins, plus 8 buttons and 1 data
   line makes 25, and an Uno/Nano has about 18 usable with D0/D1 kept for USB serial.
   Delivered as `DEVICE_LED_MODE 1`: one pin per device, solid on = CLOSED, off = OPEN, slow
   blink = TRIPPED, fast blink = LOCKOUT. 17 pins used, A5 spare. `DEVICE_LED_MODE 2`, a green
   pin and a red pin per device, is in the sketch for a Mega 2560.
4. **DER fault: the PCC clears it alone.** `[V]` The artifact has a FAULT DER button, but its
   model only covers Z1 to Z6, so this was a new decision. Coordinated behavior: DER_PCC trips
   at step 01 and locks out at step 02, the DER branch shows red, and Z5 and the whole feeder
   stay energized. Nothing further to isolate and nothing stranded to restore. The teaching
   point is that a branch device clears its own fault without upstream tripping.
   Anti-islanding on a feeder fault is separate and unchanged from the artifact: whenever Z5
   is dead or faulted, DER_PCC trips.

Later in the session:

5. **LED run 1 is 17 px: 8 px south of N1, then 9 px N1 -> N2.** `[V]` N1 is the SUB_A_BKR
   location, so the southern 8 px are on the source side of the breaker. They are the
   substation bus and stay lit in the Source A color always, even through a Z1 lockout. New
   zone code `ZN_BUSA`. **Supersedes** the first build of this session, where all 17 px were
   Z1 and went dark with it.

### Firmware as built

**File:** `FLISR_Trainer/FLISR_Trainer.ino` in the working directory, 717 lines. Needs the
FastLED library.

**Top-of-file edit blocks,** in order:

1. Fault button pins, each with its DXF location in a comment.
2. Device LED pins and `DEVICE_LED_MODE`, each with its element location.
3. Strip: data pin, `NUM_LEDS`, type, color order, brightness, power cap, section colors.
4. LED segment table: a commented row-by-row map (run, length, over, from, to, zone, note),
   then five `PROGMEM` arrays of 31 entries each: `SEG_LEN`, `SEG_OVER`, `SEG_ZONE`,
   `SEG_SPLIT`, `SEG_ZONE2`. Notes on run 1 and on N30 sit under the table.
5. Timing and behavior, plus `SEGMENT_TEST_MODE`.

**Pin map, Uno** `[V]`

| Signal | Pin | Signal | Pin |
|---|---|---|---|
| FAULT Z1 | D2 | Strip data | D10 |
| FAULT Z2 | D3 | SUB_A_BKR LED | D11 |
| FAULT Z3 | D4 | DEV_A1 LED | D12 |
| FAULT Z4 | D5 | DEV_A2 LED | D13 (shares the onboard LED) |
| FAULT Z5 | D6 | TIE LED | A0 |
| FAULT Z6 | D7 | DEV_B2 LED | A1 |
| FAULT DER | D8 | DEV_B1 LED | A2 |
| RESET | D9 | SUB_B_BKR LED | A3 |
| | | DER_PCC LED | A4 |

Buttons wire from pin to GND with `INPUT_PULLUP`, so pressed reads LOW; 40 ms debounce.

**Behavior** `[V]`

- Colors: Source A blue `CRGB(0x1E,0x6B,0xFF)`, Source B green `CRGB(0x00,0xD0,0x50)`, fault
  red `CRGB(0xFF,0x18,0x10)`. De-energized is OFF rather than gray. Over = 0 pixels are always
  off. BUSA pixels are always Source A blue.
- The faulted section blinks red during steps 01 and 02 (350 ms) and holds solid red from
  step 03 on, as the work boundary.
- Brightness 80 of 255; FastLED soft power cap 5 V / 4000 mA.
- Strip refresh capped at 50 fps (`FRAME_INTERVAL_MS 20`); device LEDs update every loop pass.
- Serial monitor at 115200 prints the step, the fault, every zone's source, and every device's
  state on each change.
- `setup()` sums `SEG_LEN` and prints a loud mismatch warning if it does not equal `NUM_LEDS`.
  Fixing a count means changing that row and `NUM_LEDS`; nothing else moves, because pixel
  offsets are walked from the table at render time.
- `SEGMENT_TEST_MODE 1` lights each run alone in its own hue at boot, 1.2 s each, and prints its
  pixel index range, for checking counts against the physical board.

**FLISR model.** `computeModel()` is a direct port of the artifact's `model(f, st)`. For a
fault in zone f, the A side is f <= 3. The source-side device (index f-1 on the A side, f on
the B side) trips at step 01 and locks out at 02. The far-side device (f on A, f-1 on B) opens
at 03. At 04 the tie closes only if healthy zones are stranded past the fault, and those flip
to the other source. Faults in Z3 or Z4 border the tie, so nothing is restored and the tie
stays open, which is the correct answer. `[V]`

Step 04 outcomes, from the sketch model `[V]`:

| Fault | TIE | Restored from the other source | DER_PCC |
|---|---|---|---|
| Z1 | closed | Z2, Z3 from B | closed |
| Z2 | closed | Z3 from B | closed |
| Z3 | open | none | closed |
| Z4 | open | none | closed |
| Z5 | closed | Z4 from A | tripped (anti-islanding) |
| Z6 | closed | Z4, Z5 from A | closed |
| DER | open | none, feeder untouched | lockout |

### Judgment calls worth remembering

- **Zone assignment runs off chain order and pixel counts, not coordinates.** That is why the
  N32 and N1 corrections changed no code. Coordinates only matter where a device lands partway
  along a run and forces a split, which is why N30 mattered in principle.
- **J1 is a real 0-length row** in the tables, so the sketch matches the user's mental model
  and stays editable. It is Over = 0 and zone hidden, so any pixels later added there would
  stay dark, which is right for a wire jumper.
- **Tables and every serial string live in flash** (`PROGMEM`, `F()`), because the pixel
  buffer alone is 1011 of the Uno's 2048 bytes of SRAM.
- **Refresh is capped at 50 fps** because the AVR WS2812 driver disables interrupts while it
  clocks out data, about 10 ms per frame at 337 px. Refreshing flat out would leave interrupts
  off roughly half the time. `[S]`
- **`ZN_DER` is 7 and `ZN_BUSA` is 8, but `zoneState[]` holds only indices 0 to 6.**
  `colorForZone()` returns on both before indexing the array, with a comment saying so. Any
  future zone code above 6 must do the same.
- **`NUM_LEDS` is hard-coded, with a runtime check,** rather than computed at compile time,
  because a constexpr array on AVR risks being copied into SRAM. `[I]`

### Verification actually performed

1. **Compiled** with avr-g++ 7.3.0 for atmega328p, `-std=gnu++17 -Wall -Wextra`, against the
   real Arduino AVR core 1.8.8 and FastLED 3.10.5: zero warnings. Variants `DEVICE_LED_MODE 2`
   (atmega2560), `SEGMENT_TEST_MODE 1`, and `AUTO_ADVANCE 0` also compiled clean. `[V]`
2. **Linked the full firmware** and read `avr-size` on the final version: **flash 11,934 B
   (36.4%), SRAM 1,492 B (72.9%), 556 B free for stack.** The symbol table shows `leds[]` at
   1011 B, and all lookup tables (171 B) and every string in `.progmem.data`. `[V]`
3. **Logic cross-check against the artifact.** The artifact's `model()`, copied verbatim, ran
   in Node alongside a line-by-line JavaScript transliteration of `computeModel()`, for faults
   Z1 to Z6 at steps 00 to 04, comparing every zone and every device: **420 comparisons, 0
   mismatches.** `[V]` for logic equivalence, with one caveat: the C++ itself was never
   executed on a host, so the check is only as faithful as the transliteration.
   `computeModel()` was not edited after this check.
4. **Table invariants,** checked by extracting the arrays from the `.ino` text so the test
   cannot drift from the code: 31 rows in all five tables; lengths sum to `NUM_LEDS`; every
   split point lies inside its run; no unsplit row carries a stray second zone; every Over = 0
   row is marked hidden; every zone code above 6 returns before the array index. This caught
   one real defect: the J1 row was Over = 0 but zone Z6. Fixed. `[V]`
5. **Render simulation** of every fault at steps 01, 02, and 04, counting visible pixels by
   color. Normal is 161 blue and 73 green. Z1 at lockout: bus 8 px blue, Z1 red, Z2 and Z3
   dark. After restore, Z2 and Z3 turn green and the bus is still blue. `[V]`
6. **Not run on hardware.** Nothing in this sketch has touched a real Uno, strip, or button.

### Deliverables

| Thing | Where |
|---|---|
| Arduino sketch | `FLISR_Trainer/FLISR_Trainer.ino` (working directory) |
| This log entry | `PROJECT_MEMORY.md` |
| Persistent memory, standing instruction to use this file | `C:\Users\jprun\.claude\projects\c--Users-jprun-Downloads-JEA-Project\memory\jea-project-memory-file.md` |

The verification scripts (`verify.js`, the table checker, `build.sh`) lived in the session
scratchpad and are gone. The method is recorded above and the build recipe below.

### Environment notes for next time

- **Toolchain.** No `arduino-cli` and no host g++. The Arduino IDE is installed at
  `C:\Users\jprun\AppData\Local\Programs\Arduino IDE`. avr-g++ 7.3.0 is at
  `C:\Users\jprun\AppData\Local\Arduino15\packages\arduino\tools\avr-gcc\7.3.0-atmel3.6.1-arduino7\bin`,
  and AVR core 1.8.8 at `...\Arduino15\packages\arduino\hardware\avr\1.8.8` (variants
  `standard` and `mega`). An ESP32 core is also installed. Node v22 and Python 3.14 with
  openpyxl 3.1.5 are available. `[V]`
- **The Arduino sketchbook is OneDrive-redirected.** FastLED 3.10.5 is at
  `C:\Users\jprun\OneDrive\Documents\Arduino\libraries\FastLED`, not `Documents\Arduino`. `[V]`
- **FastLED 3.10.5 is a unity build.** To link by hand, use the core objects, only FastLED's
  `*+.cpp` amalgamation files plus `src.cpp`, and the sketch. Also compiling every individual
  FastLED `.cpp` gives duplicate symbols; linking only the individual files leaves
  `fl::memcpy` undefined. Needs `-std=gnu++17`. `[V]`
- **The Excel file locks while it is open.** A write fails with PermissionError and a
  `~$...xlsx` lock file appears. If the user says the workbook was updated but the hash has not
  changed, the edit is probably unsaved; also check the OneDrive copy. `[V]`
- The workbook is plain data (no charts, pivots, tables, or drawings), so an openpyxl edit is
  safe once Excel has closed it. `[V]`
- The file-safety hook blocks `rm` with a glob. Call `vault.ps1` from PowerShell, not bash,
  because bash strips the backslashes out of the path. `[V]`

### Open items, flagged not resolved

Continues the numbered open-items list already on record:

12. **Write N30 into the Excel:** `Node!B31` -> `12.59`, `Node!C31` -> `29.51`. Blocked this
    session because the workbook was open in Excel.
13. **Reconcile the two Excel copies.** The working-directory copy (saved 2026-09-13 00:17) is
    newer but still has the old N1 (25.58, 9.95); the OneDrive copy (saved 00:16) has the
    corrected N1 (12.57, 9.95). Pick a master before further edits.
14. **Recount LED runs 11 and 13.** LED 11 (N7 -> N8, RES-2 west): 11 counted, geometry says
    16.1 over 10.59 in. LED 13 (N9 -> N10, RES-2 top street): 28 counted, geometry says 31.5
    over 20.67 in. Every other surface run is within +/-1.3 px. LED 29 (N35 -> N17) reads 5.4 px
    long, but it runs under the board where the path is free, so it is probably fine.
    `SEGMENT_TEST_MODE 1` exists for this.
15. **Stray RESET label in the DXF** at (34.07, 18.31), beside FAULT DER, with no button circle
    near it. The real RESET is at (26.46, 5.13).
16. **Strip build and power notes, not yet acted on** `[S]`: inject 5 V about every 100 px on a
    337 px chain; put a 330 to 470 ohm series resistor on the data line at the first pixel; put
    a 1000 uF capacitor across 5 V and GND at the strip input.
17. **SRAM headroom is 556 B.** Fine for the current code. If features are added, cutting the
    serial narration is the first saving.
18. **Single chain versus per-panel chains.** The 2026-09-07 21:46 wiring architecture uses
    four independent chains, one per panel, so no LED data crosses a seam. The REV1
    tabulation, and this firmware, use one 337 px chain that crosses seams. That is right for
    the cardboard prototype. Whether the final build returns to per-panel chains is undecided.
    Interacts with open items 5, 8 and 9. `[I]`
19. **Where the FLISR logic lives in the final trainer.** Standing Facts say the SEL-2240 is
    the brains and fault scenarios are hard-coded in the RTAC. This sketch runs the whole
    FLISR model on the Arduino, standalone. That suits a prototype demo, but the final design
    needs a decision: keep a standalone model on the LED controller, or make the LED
    controller a display driven by RTAC outputs. Noticed while writing this entry; not
    discussed with the user. `[I]`

### Not done this session

- No changes to the published artifact, the DXF, or `jea_tabletop_layout_spec.md`.
- The Excel workbook was not modified. Its hash was confirmed unchanged after the blocked
  write, and the backup taken for that write was archived with `vault.ps1` (restore id
  `1c66ebfe`).
- No hardware test. No RTAC or IEC 61131 logic. No git commit.

---

## 2026-09-13 22:17 CDT - Test bench for FLISR_Trainer.ino, then FLISR_Trainer_REV1 with fault wave and restore fill animations

Separate session from the 21:22 entry, running in parallel with it this evening. This session
did not read this file until its last turn: the standing instruction to use it was saved by
the other session at 21:27, after this one had started. Checked afterwards: nothing built here
contradicts the entries above.

### What was asked

1. **Build a virtual environment to test `FLISR_Trainer/FLISR_Trainer.ino`**, based on the
   REV1 DXF and the plan set artifact (`https://claude.ai/code/artifact/5ba6ca32-14a6-4a20-a69f-95a37753a51c`).
   User's words: not a compiler and not a virtual Arduino, "just create an environment so that
   it operates EXACTLY as the code is written, nothing more, nothing less."
2. **Pin that bench**, and **create `FLISR_Trainer_REV1`**: a fault in the middle of a line
   should spread outward pixel by pixel until the area is red, then a trail animation should
   show the new source routing power.
   User answers to three clarifying questions: `[V]`
   - Wave look: **red spreads, no dark front.** Pixels go straight from their source color to red.
   - Wave reach: **everything that lost power.** The faulted section plus every stranded zone out
     to the open tie. At 03 ISOLATE the stranded zones drop to dark and only the fault stays red.
   - Restore: **plain fill from the tie.** No bright comet head.

### Sources read this session

- `FLISR_Trainer/FLISR_Trainer.ino` (717 lines), the plan set artifact's raw HTML including
  `model()`, the DXF through ezdxf 1.4.4, and all five xlsx sheets. `[V]`
- The xlsx was saved at 21:24 during this session. Re-read after: **working-directory copy now
  has N1 = (12.58, 9.95)** and N30 = (12.59, 29.51). Nothing else changed. `[V]`
- FastLED 3.10.5 source, for behavior the sketch depends on: `power_mgt.cpp.hpp` (power limiter),
  `FastLED.cpp.hpp` `show()`, `hsv2rgb.cpp.hpp` (`hsv2rgb_rainbow`), `fl/gfx/crgb_extra.cpp.hpp`
  (CRGB = CHSV routes to rainbow), `platforms/shared/scale8.h`, `fastled_config.h`
  (`FASTLED_SCALE8_FIXED 1`). `[V]`

### Part 1: the test bench

**What it is.** A self-contained HTML page. It shows the DXF drawn to scale, the 337-pixel strip
placed along the LED sheet runs, the 8 DXF buttons (hold to close the contact), the 8 device LED
pins, a serial monitor, and a pin/millis/power readout. Published and pinned:
`https://claude.ai/code/artifact/ab75a52c-dfae-444d-ad1e-06d14a08ed18`. `[V]`

**How exactness is kept.** `[V]`
- `FLISR_Trainer_Sim/firmware.js` is a line-for-line JS port of everything below "NOTHING BELOW
  HERE NEEDS EDITING", same function names, statement order and integer widths.
- `FLISR_Trainer_Sim/build_sim.py` extracts every `#define` and PROGMEM table from the .ino (with
  a small `#if/#else` evaluator), so config is never retyped. It sha256-hashes the logic section
  and refuses to build if that no longer matches the hash stored in the port.
- It also cross-checks the .ino against the xlsx and DXF: run From/To, lengths, button positions,
  element positions, nodes on DXF route lines.
- FastLED pieces the sketch relies on are ported from source: the power limiter (computed every
  frame; this sketch peaks near 7.6 W of the 20 W cap, so it never limits) and `hsv2rgb_rainbow`
  for SEGMENT_TEST_MODE.

**Modeling choices, stated on the page.** `[V]` as implemented, `[I]` as to hardware fidelity.
- Virtual millisecond clock; `delay()` in setup advances it; `loop()` runs once per ms;
  `show()` and Serial take zero time. A real Uno loops faster and `show()` blocks about 10 ms.
- Button contacts are timestamped, so a contact shorter than 41 ms is ignored, as the debounce
  code does. No mechanical bounce.
- Pixels show the `leds[]` buffer at the last `show()`. Brightness, color correction and
  dithering are not drawn.
- Pixels are evenly spaced on the straight From -> To node line; run 1 starts `SEG_SPLIT[0]` px
  south of N1. Under-board runs are drawn offset 0.45 in, behind a toggle. Device LEDs sit
  0.75 in right and 0.60 in up from their Element point, with a leader line.

### Part 2: FLISR_Trainer_REV1

**File:** `FLISR_Trainer_REV1/FLISR_Trainer_REV1.ino`, a full copy of `FLISR_Trainer.ino` with
additions. The original sketch is untouched. `[V]`

**New config blocks.** `[V]`
- `[4b]` `NUM_NODES 36`, `SEG_FROM[]` / `SEG_TO[]` node numbers per run, a tap table
  (`TAP_SEG 27`, `TAP_PX 7`, `TAP_NODE 17`: N17 sits 6.78 px along run 27, where the DER branch
  leaves the Z5 line), and `TIE_NODE 12`.
- `[4c]` `FAULT_SEG[]` / `FAULT_PX[]`: the run (array index, where J1 = 24) and pixel nearest
  each Fault sheet point: Z1 run 1 px 16, Z2 run 4 px 7, Z3 run 15 px 6, Z4 run 18 px 3,
  Z5 run 27 px 4, Z6 run 23 px 6 (exact tie with px 7), DER run 30 px 4. This honors the
  2026-09-10 decision that each button binds to an explicit run, not a runtime nearest lookup.
- `[5]` `ANIM_STEP_MS 30` (one pixel per 30 ms).

**Behavior.** `[V]`
- **01 FAULT:** red spreads from the fault pixel along the line through every zone that lost
  power, including the DER branch when it loses power, stopping at devices bordering live zones.
  Pixels ahead of the wave keep their NORMAL colors. After the wave, the faulted section blinks
  as before (350 ms) and the stranded zones hold solid red. The wave continues through 02 if the
  user presses ahead.
- **03 ISOLATE:** identical to FLISR_Trainer: stranded zones dark, fault solid red.
- **04 RESTORE:** if the tie closes, the new source color fills the restored zones outward from
  N12, pixel by pixel. For a Z6 fault the fill continues through N17 into the DER branch, since
  DER_PCC recloses at 04. Z3, Z4 and DER faults have no fill.
- **Auto-advance** waits for an animation to finish, then counts `STEP_INTERVAL_MS`.
- **Serial** banner reads `=== JEA Tabletop FLISR Trainer REV1 ===`. Everything else printed is
  identical to FLISR_Trainer.

**Design calls made without asking** `[I]`, cheap to change:
- Blinking after the wave applies to the faulted section only; stranded zones are solid red.
- The step timer restarts when an animation finishes, so each step shows for the full interval.
- 30 ms per pixel. The longest wave is the Z1 fault, about 2.6 s.

**How the animation runs on an Uno.** `[V]` Each run splits into pieces at its SEG_SPLIT and any
tap. When an animation starts, the sketch works out the pixel distance from the source to every
node and split point by repeated relaxation (uint8 `pointDist[67]`). Each frame, a pixel's
distance is its piece's end-point distance plus its offset along the piece. Extra SRAM is 79 B.
No per-pixel RAM array, which the Uno could not afford.

**REV1 bench:** `FLISR_Trainer_Sim/firmware_rev1.js` (port),
`python build_sim.py --sketch FLISR_Trainer_REV1`, published as
`https://claude.ai/code/artifact/e104d46c-45b6-412a-890d-59185b0d97d4`. Not pinned. `[V]`

### Verification actually performed

1. **Bench build checks.** FLISR_Trainer: 8 of 8 pass, 0 warnings. REV1: 12 of 12, including
   SEG_FROM/SEG_TO vs block [4], tap position, TIE_NODE vs E4, and each fault pixel being the
   nearest visible pixel to its Fault sheet point and in the right zone. `[V]`
2. **FLISR_Trainer port tests,** `node --test test_firmware.js`: 20 of 20 pass. They cover
   - exact boot serial text
   - all 6 zone faults x 5 steps against the artifact's `model()` copied verbatim
   - DER fault, pixel color counts, debounce edge (40 ms ignored, 41 ms counts), auto-advance
     timing, blink phase, device LED blink rates
   - FastLED limiter math on a full-white frame (72,302 mW -> brightness 69), rainbow hues,
     SEGMENT_TEST_MODE 1, DEVICE_LED_MODE 2
   Mutation check: 5 planted bugs, 5 caught, after tightening the blink-phase test, which
   first missed one. `[V]`
3. **REV1 port tests,** `node --test test_firmware_rev1.js`: 13 of 13 pass. For all 7 faults,
   every frame of the wave, hold, isolate and restore must match a BFS over an explicit pixel
   graph (a different algorithm from the sketch's) laid over the FLISR_Trainer port's frames at
   the same ms. Serial output must equal FLISR_Trainer's apart from the banner. Also tested:
   auto-advance timing (02 at wave end + 2500 ms), pressing ahead mid-wave, a new fault
   mid-wave, and RESET mid-wave. Mutation check: 6 planted bugs, 6 caught. `[V]`
4. **Port vs sketch structure.** All 26 functions in REV1's logic section exist in the port with
   identical call sequences, checked by script. Beyond that, port fidelity rests on review. `[V]`
5. **Compiled for Uno** with avr-gcc 7.3.0, AVR core 1.8.8, IDE-like flags (`-Os -flto
   -std=gnu++11`), FastLED built from `src/fl/build/*.cpp` only. `[V]` for these flags:
   - FLISR_Trainer: flash 9,176 B (28%), SRAM 1,439 B (70%)
   - REV1: flash 10,788 B (33%), SRAM 1,518 B (74%), 530 B free for stack
   - REV1 with `-Wall -Wextra`: 0 warnings
   These differ from the 21:22 entry's 11,934 / 1,492, which used `-std=gnu++17` and a different
   link set. The Arduino IDE's own numbers may differ slightly again. `[I]`
6. **One screenshot** of the REV1 bench mid-wave on a Z1 fault, zoomed at SUB_A_BKR: red
   upstream of N2, bus below the breaker still blue. `[V]`
7. **Not run on hardware.** Frame rate during a wave on a real Uno is unmeasured. `[I]`

### Findings

- **The FastLED install mixes two versions.** `src/` holds 136 `.cpp` files dated 2026-03-07 from
  an older FastLED, next to the 26 FastLED 3.10.5 unity files in `src/fl/build/` dated
  2026-07-28. `[V]`
  - Compiling the old files fails, e.g. `cled_controller.cpp` uses `m_pTail`, which 3.10.5
    renamed. `[V]`
  - The Arduino IDE compiles every `.cpp` under a library's `src/`, so an IDE upload of either
    sketch will likely fail until FastLED is reinstalled cleanly. `[I]`, strong, not tried in
    the IDE.
  - This explains the 21:22 entry's "compiling every individual FastLED .cpp gives duplicate
    symbols."
- **Two buttons in the same loop pass:** only the lower index is handled, and the other press is
  lost for good. `[V]`
- **Z6 restore:** DER_PCC goes from TRIPPED straight to CLOSED at 04 with no reconnect delay.
  Worth checking against the IEEE 1547 teaching story. `[I]`
- **The plan set artifact is older geometry:** RESET at (25, 14) and 281 px, vs REV1's
  (26.46, 5.13) and 337 px. `[V]`

### Deliverables

| Thing | Where |
|---|---|
| FLISR_Trainer bench (published, pinned) | `https://claude.ai/code/artifact/ab75a52c-dfae-444d-ad1e-06d14a08ed18`, source `FLISR_Trainer_Sim/FLISR_Trainer_Sim.html` |
| REV1 sketch | `FLISR_Trainer_REV1/FLISR_Trainer_REV1.ino` |
| REV1 bench (published) | `https://claude.ai/code/artifact/e104d46c-45b6-412a-890d-59185b0d97d4`, source `FLISR_Trainer_Sim/FLISR_Trainer_REV1_Sim.html` |
| Ports | `FLISR_Trainer_Sim/firmware.js`, `FLISR_Trainer_Sim/firmware_rev1.js` |
| Builder | `FLISR_Trainer_Sim/build_sim.py` (`--sketch FLISR_Trainer` or `FLISR_Trainer_REV1`), template `sim_template.html`, extracted config `sim_config.json` / `sim_config_rev1.json` |
| Tests | `FLISR_Trainer_Sim/test_firmware.js`, `FLISR_Trainer_Sim/test_firmware_rev1.js` |

The manual AVR build script (`avr_build.sh`) and mutation copies lived in the session scratchpad.
The recipe is in item 5 above.

### Open items, flagged not resolved

Continues the list above:

20. **Reinstall FastLED cleanly** before uploading either sketch: remove
    `C:\Users\jprun\OneDrive\Documents\Arduino\libraries\FastLED` and reinstall 3.10.5 from
    Library Manager. Not done here: it is outside the project and deleting library files needs
    the user.
21. **Upload REV1 to a real Uno** and watch the wave frame rate. The distance math adds render
    cost that was not measured on hardware. `[I]`
22. **SRAM headroom** is 530 B with REV1 under IDE-like flags. Supersedes the 556 B in item 17
    for REV1.
23. **Item 12 is done in the working-directory xlsx** (N30 = 12.59, 29.51). **Item 13 is
    narrower now:** the working copy has N1 x = 12.58, the OneDrive copy 12.57. `[V]` for the
    working copy.
24. **If node or LED tables change,** REV1's `SEG_FROM`, `SEG_TO`, tap and fault tables must
    follow. `build_sim.py --sketch FLISR_Trainer_REV1` checks all of them against the xlsx.
25. **DER_PCC reclose delay at Z6 restore:** decide whether the trainer should show an IEEE 1547
    enter-service wait. `[I]`

### Not done this session

- No changes to `FLISR_Trainer.ino`, the DXF, the xlsx, or the plan set artifact.
- The REV1 bench is not pinned (offered).
- No hardware test. No git commit.

---

## 2026-09-13 22:25 CDT - Pinned bench switched to REV1

User asked for REV1 pinned and REV0 not. Done: the REV1 bench
(`https://claude.ai/code/artifact/e104d46c-45b6-412a-890d-59185b0d97d4`) is pinned in the
claude.ai sidebar, and the FLISR_Trainer bench (`...ab75a52c-dfae-444d-ad1e-06d14a08ed18`) is
unpinned but still published. **Supersedes** the pin state in the 22:17 entry. `[V]`

---

## 2026-09-14 11:09 CDT - REV1 device status moved onto strip pixels (no discrete status LEDs exist)

### What was asked

User referenced `FLISR_Trainer_REV1/`, the tabulated REV1 xlsx, the REV1 bench artifact and the
plan set artifact, and clarified: **there are no separate status LEDs on the elements. The only
LEDs are the strip.** Asked whether the single strip pixel closest to each element could be that
element's status LED. `[V]`

**Supersedes** decision 3 of the 2026-09-13 21:22 entry ("Device status: separate discrete LEDs,
not the WS2812 strip"), and the DEVICE_LED_MODE 1/2 pin maps there, for REV1. Note the original
2026-09-07 plan set had already budgeted "device px" in the strip chain, so this returns to that
idea, using an existing line pixel instead of a dedicated one. `[V]`

### Sources read this session

- `PROJECT_MEMORY.md` (all), `FLISR_Trainer_REV1/FLISR_Trainer_REV1.ino` (all), all five xlsx
  sheets, both artifacts through the Artifact read action, and `build_sim.py`,
  `firmware_rev1.js`, `test_firmware_rev1.js`, `sim_template.html`. `[V]`
- xlsx unchanged since the 22:17 entry (N1 = 12.58, 9.95; N30 = 12.59, 29.51). `[V]`

### Which pixel, and why

Nearest pixel computed with the bench's own placement: each run's pixels are evenly spaced between
its From and To node, and run 1's first 8 px run south of N1. Measured against both the Element
sheet point and the DXF device symbol center. `[V]` for the computation, `[I]` for how well it
matches the physical strip.

- **E1 and E5 sit well off their DXF symbols:** E1 is 0.87 in south of the SUB_A_BKR block and E5
  is 1.04 in west of the DEV_B2 block (the block is centered on N15, 31.12, 25.53). `[V]`
- **Rule used:** of the two pixels on either side of the point where the device splits its two
  zones, take the one nearer the Element sheet point. This is the nearest pixel outright for six
  devices. `[I]` design call, made without asking, stated to the user.
- **The two exceptions:**
  - SUB_A_BKR: px 6 is nearer E1 (0.16 in vs 0.50 in), but it is inside the bus.
  - DEV_B2: run 18 px 5 is nearer E5 (0.21 in vs 0.36 in), but it is west of the commercial tap at
    N13, and DEV_B2 is electrically east of it.
- **Close calls (within 0.15 in of the other side):** DEV_A2, TIE, DEV_B1, DER_PCC.

| Device | Run (LED ID) | Array index | Pixel | Strip # | Zone side |
|---|---|---|---|---|---|
| SUB_A_BKR | 1 | 0 | 7 | 7 | BUSA |
| DEV_A1 | 4 | 3 | 2 | 53 | Z2 |
| DEV_A2 | 8 | 7 | 8 | 105 | Z2 |
| TIE | 18 | 17 | 0 | 221 | Z4 |
| DEV_B2 | 21 | 20 | 0 | 246 | Z4 |
| DEV_B1 | 27 | 27 | 0 | 298 | Z5 |
| SUB_B_BKR | 23 | 22 | 0 | 271 | Z6 |
| DER_PCC | 30 | 30 | 1 | 325 | Z5 |

None of these is a fault wave start pixel. `[V]`

### Sketch changes, `FLISR_Trainer_REV1.ino` (edited in place; REV1 = the cardboard revision)

- **Block [2] is now DEVICE STATUS PIXELS:** `NUM_DEVICES 8` (moved here from the logic section),
  `DEV_SEG[]` / `DEV_PX[]` (array index + pixel along the run, same convention as block [4c]),
  `COLOR_DEV_CLOSED` white `CRGB(0xFF,0xFF,0xFF)`, `COLOR_DEV_OPEN` amber `CRGB(0xFF,0xB0,0x00)`.
  The comment block carries the table above and the reasoning. `[V]`
- **Behavior:** CLOSED = solid white, OPEN = solid amber, TRIPPED = amber slow blink
  (`DEV_TRIP_BLINK_MS` 500), LOCKOUT = amber fast blink (`DEV_LOCK_BLINK_MS` 150). Same states and
  blink rates as the old mode 1. Setting `COLOR_DEV_OPEN` to black gives exactly the old mode-1
  on / off / blink look. `[V]` Color choice `[I]`: white and amber were picked because blue, green
  and red are already line colors.
- **render()** paints the 8 status pixels after the line, so they override the line color. The
  fault wave and restore fill still count those pixels as part of the line, so animation timing is
  unchanged. New helpers `colorForDevice()` and `stripIndex()`. `[V]`
- **setup()** prints `[!] <DEVICE>: DEV_SEG / DEV_PX is not a pixel on a visible run. See block [2].`
  for a bad entry, and nothing when the table is good, so serial output is otherwise unchanged. `[V]`
- **Removed:** `DEVICE_LED_MODE`, all `PIN_DEV*` defines, `DEV_PIN*` tables, `renderDeviceLeds()`,
  and the device `pinMode` setup. Pin budget is now 9 used (8 buttons + strip data); D11-D13 and
  A0-A5 spare. `[V]`
- `FLISR_Trainer/FLISR_Trainer.ino` (REV0) was **not** changed and still assumes discrete LEDs. `[V]`

### Bench changes

- `firmware_rev1.js`: ported the same changes; `PORTED_LOGIC_SHA256` now
  `a64b8de569437b5ddde18639ca16d69ae8fa1d365e93736195c566d5b81ecd0c`.
- `build_sim.py`: for a sketch with `DEV_SEG`, reads the pixel table instead of pins.
  - Fails on: a pixel not on a visible run, or two devices sharing a pixel.
  - Warns on: a pixel outside the device's two zones, not touching the device's other zone, more
    than 1 in from the Element point, or on a fault wave start.
  - REV0 path unchanged.
- `sim_template.html`: in pixel mode it draws a dashed ring on each status pixel with a label, and
  lists the 8 status pixels with their live `leds[]` value under Outputs. It adds DEV_CLOSED and
  DEV_OPEN to the key, and the probe names a device's status pixel. REV0 rendering is unchanged.
- `test_firmware_rev1.js`: every frame check now expects the status pixels from the device states
  printed on serial, plus 5 new tests:
  - NORMAL colors
  - table positions against hand-typed strip numbers
  - the Z1 trip / lockout blink phases, far-side open and tie close
  - DER fault
  - the bad-entry boot warning

### Verification actually performed

1. **Compiled for Uno** (avr-gcc 7.3.0, core 1.8.8, `-Os -flto -std=gnu++11`, FastLED
   `src/fl/build/*.cpp`), with `-Wall -Wextra`: **0 warnings.** A planted unused variable produced a
   warning, so warnings really were on. **Flash 10,898 B (33%), up 110 B; SRAM 1,518 B, unchanged.**
   The pre-change REV1 rebuilt with the same script gave 10,788 / 1,518, matching the 22:17 entry.
   `[V]`
2. **Bench builds:**
   - REV1: 12 of 12 checks, 0 warnings.
   - REV0: 8 of 8; `sim_config.json` byte-identical to before; GEOM equal as data (JSON key order
     only).
   `[V]`
3. **Build checks fed bad tables** (scratch copies):
   - Duplicate pixel and hidden run fail.
   - DEV_A1 moved into Z2, SUB_A_BKR at px 6, DEV_B2 at run 18 px 5, and DER_PCC on the fault start
     all warn.
   - The first version missed the DEV_B2 case, because a hidden return run at N13 counted as a zone
     change. Fixed so only the device's other zone counts. `[V]`
4. **Tests:** REV1 18 of 18, REV0 20 of 20. Two bugs in my own new test were found and fixed
   before it passed:
   - an infinite loop (loop bound re-read the advancing clock)
   - presses spaced inside the release debounce
   A guard assertion also caught an empty blink sample that had been passing vacuously. `[V]`
5. **Mutation check:** 8 planted bugs in the port (blink rates swapped, OPEN shows closed color,
   stripIndex off by one, override dropped, TRIPPED phase inverted, setup check `>` for `>=`, setup
   check ignores hidden runs, closed devices left at line color): **8 of 8 caught.** `[V]`
6. **Port vs sketch structure:** 27 functions in each, same names, same order. `[V]`
7. **One headless Chrome screenshot** of the REV1 bench at boot: 7 white status pixels, TIE amber,
   DEV_B2's pixel just past the commercial tap. `[V]`
8. **Not run on hardware.** Whether amber reads clearly against fault red on real WS2812B at
   brightness 80 is unverified. `[I]`

### Deliverables

| Thing | Where |
|---|---|
| Sketch | `FLISR_Trainer_REV1/FLISR_Trainer_REV1.ino` |
| REV1 bench, republished (version 2, same URL, still pinned) | `https://claude.ai/code/artifact/e104d46c-45b6-412a-890d-59185b0d97d4` |
| Bench sources | `FLISR_Trainer_Sim/` `firmware_rev1.js`, `build_sim.py`, `sim_template.html`, `test_firmware_rev1.js`, rebuilt `FLISR_Trainer_REV1_Sim.html`, `sim_config_rev1.json`, `FLISR_Trainer_Sim.html` |

Scratchpad only, gone after the session: `devpx.py` (nearest-pixel analysis), `avr_build.sh`,
`buildcheck.py`, `mutate.py`.

### Open items, flagged not resolved

Continues the list above:

26. **Check the status pixels on the physical board.** At step 00, 7 pixels should be white and the
    TIE pixel amber. Eyeball DEV_A2, TIE, DEV_B1 and DER_PCC first. To move one, change its
    `DEV_SEG` / `DEV_PX` entry in block [2].
27. **Amber vs fault red on real strip.** Tune `COLOR_DEV_OPEN` on hardware if they blur together.
    `[I]`
28. **REV0 sketch and bench still model discrete device LEDs.** Not changed, since the request named
    REV1. Decide whether REV0 should get the same change or be retired.
29. **REV0 bench local HTML was rebuilt but not republished.** It has no visible change, only inert
    template code and a build timestamp. `[V]`
30. **Plan set artifact untouched.** It still shows older geometry and the ESP32 hub (already noted
    in the 22:17 entry).
31. `FLISR_Trainer_Sim/__pycache__/build_sim.cpython-314.pyc` is tracked in git and changes every
    time `build_sim.py` runs. Consider untracking it.

### Not done this session

- No change to the xlsx, the DXF, `FLISR_Trainer.ino`, or the plan set artifact.
- No hardware test. No git commit.
- A stray empty file I created by mistake (`%TEMP%\claude_devpx.py`) was archived with `vault.ps1`
  (restore id `cbbbeb9b`).

---

## 2026-09-14 11:18 CDT - REV1: lost-power sections stay red until the restore fill eats them

### What was asked

User liked the status pixels. They described the fault sequence as:
1. red trail
2. faulted segment blinks
3. to-be-restored section goes off
4. green or blue trail restores

They asked to cut the third visual: the section that lost power should stay solid red and get
"eaten up" by the restore trail. Everything else unchanged. Framed as a simple `.ino` change. `[V]`

**Supersedes** the 22:17 entry's "03 ISOLATE: stranded zones dark" and "04 RESTORE: ... fills"
(which filled over dark pixels). The FLISR steps themselves are unchanged: step 03 still opens the
far-side device (its status pixel turns amber), and the faulted section stops blinking. `[V]`

### Change, `FLISR_Trainer_REV1.ino`

Two code lines plus comments:
- `colorForState()`: `ZS_DEAD` now returns `COLOR_FAULT` instead of `COLOR_DEAD`, so anything that
  lost power is solid red at 03 and 04.
- `colorForPixel()`: restore-fill pixels not yet reached return `COLOR_FAULT` instead of
  `COLOR_DEAD`.
- `COLOR_DEAD` is now used only for under-board runs, the blink-off phase, and blinking status
  pixels. Header, ANIMATIONS block and the `COLOR_DEAD` comment were updated to match. `[V]`

**Design call made without asking** `[I]`, cheap to change: on a **Z5 fault the DER branch** loses
power (anti-islanding trip) and is never restored, so it now stays solid red through 04 instead of
going dark. That follows the same rule ("red until power comes back"). It is the only lost-power
section that is neither faulted nor restored.

### Verification actually performed

1. **Compiled for Uno**, `-Wall -Wextra`, same recipe as the 11:09 entry: 0 warnings. **Flash
   10,894 B (4 B less), SRAM 1,518 B.** `[V]`
2. **Port** `firmware_rev1.js`: same two lines. `PORTED_LOGIC_SHA256` is now
   `f4235442ffa33dc1cc409120c166f2fd6d0d1acee6aaf7991c5d7ff979ad8af4`. `[V]`
3. **Tests** `test_firmware_rev1.js`:
   - At 03, lost zones are expected red.
   - At 04, restored pixels not yet reached are expected red, and still-unpowered zones stay red.
   - Results: REV1 18 of 18, REV0 20 of 20. `[V]`
4. **Mutation check:** reverting either line to the old dark behavior is caught (5 and 4 failing
   tests). `[V]`
5. **Bench build** 12 of 12, 0 warnings. Republished as version 3 at the same URL. `[V]`
6. Not run on hardware.

### Open items

No new numbered items. Items 26 to 31 from the 11:09 entry stand.

---

## 2026-09-14 20:11 CDT - xlsx LED sheet update audited: J1 is now a real run, IDs shifted; flagged before any code change

### What was asked

User updated `JEA Cardboard Prototype Tabulated REV1.xlsx` (saved 20:03): added a pixel length where the
0-length J1 jumper was, so no 0-length run remains and later LED IDs shift up by one; also changed several
run lengths "for reasons that are largely irrelevant." Instruction: look for inconsistencies in the
dimensions; **if any, flag them and the user will address them; if none, revise the FLISR Trainer code.**
Questions welcome. `[V]`

### Sources read this session

- `PROJECT_MEMORY.md` (header, standing facts, 2026-09-13 21:22 entry onward). `[V]`
- The xlsx, all five sheets, diffed against the committed version (git `8564e16`). `[V]`
- `FLISR_Trainer_REV1/FLISR_Trainer_REV1.ino` (all), `FLISR_Trainer_Sim/build_sim.py` (all). `[V]`
- `Cardboard Layout REV1 backup_9.12.20.dxf`, Sketch3 route lines and entities near Substation A, the
  industrial lateral and the RES-2 top street, via ezdxf. `[V]`

### What changed in the xlsx

Only the LED sheet. Element, Node, Line and Fault sheets have identical cell values to the commit. `[V]`

| LED ID (new) | Was | Now | Note |
|---|---|---|---|
| 1 | 17 | 14 | N1 -> N2 |
| 6 | 17 | 18 | hidden return |
| 8 | 9 | 8 | N32 -> N30 |
| 11 | 11 | 17 | resolves open item 14 for LED 11 (geometry 16.1) |
| 13 | 28 | 29 | still short of geometry, see below |
| 14 | 26 | 28 | hidden return |
| 17 | 6 | 7 | N11 -> N12 |
| 24 | 4 | 5 | industrial lateral |
| 25 (new) | J1, 0 px | 7 px, Over 0, N28 -> N27 | replaces the jumper |
| 26 - 31 | were 25 - 30 | same From/To/len/Over | ID shift only |

Totals: **352 px** (was 337), visible 239, hidden 113. Chain is still continuous (every To = next From). `[V]`
A new column F holds the bare text `note` on the LED 26 row (F27), no cell comment. `[V]`

**Array indices in the sketch do not move:** new LED 25 takes J1's slot at index 24, so SEG_FROM/SEG_TO,
TAP_SEG, DEV_SEG and FAULT_SEG stay valid and every run is now index = LED ID - 1. `[V]`

### Inconsistencies flagged to the user

1. **N28 x is 40.10 in the Node sheet; the DXF industrial lateral ends at (41.10, 29.04).** Every other
   visible-run node is within 0.09 in of its DXF endpoint (N1, N12 and the seam/tap nodes excepted, all
   explained). Likely a one-digit typo, like the old N1 25.58. At 41.10 the lateral is 2.97 in = 4.5 px, so
   LED 24's new 5 px fits; at 40.10 it is 3.0 px and 5 px overruns by 2. `[V]` for the numbers, `[I]` for
   typo. The bench's "node on a DXF route line" check cannot catch this: N28 at 40.10 still lies on the line.
2. **LED 13 (N9 -> N10, RES-2 top street) is 29 px; nodes and DXF both give about 20.6 in = 31.3 to
   31.5 px.** 2.5 px (about 1.5 in) short. Could be a real strip that stops short of the corners. `[V]` for
   numbers.
3. Minor, pre-existing, unchanged: LED 22 (hidden, N35 -> N29) is 22 px = 14.4 in, shorter than the 15.2 in
   straight line between its nodes, so it needs lead wire somewhere. `[V]` numbers, `[I]` wire.

### Questions asked

- LED 1 = 14 px: confirm **5 px south of N1 (bus) + 9 px N1 -> N2**, i.e. SEG_SPLIT[0] 8 -> 5. N1 -> N2 is
  fixed at 9.3 px, so that is the only consistent split. `[I]`
- What the `note` in LED!F27 is meant to say.
- Default stated: revise **REV1 only** (plus its bench); REV0 still models discrete LEDs that do not exist.

### Revision scope once cleared (not started)

- Sketch: SEG_LEN (9 values), NUM_LEDS 337 -> 352, block [4] doc table renumbered, SEG_SPLIT[0], header
  and comment pixel counts.
- **Two table entries now point past the end of their runs:** DEV_PX DEV_A2 = 8 on an 8 px run (valid
  0-7), and FAULT_PX Z1 = 16 on a 14 px run. Status and fault pixels need recomputing (SUB_A_BKR, DEV_A2,
  Z1 at least).
- SRAM: leds[] grows 45 B, so about 485 B free for stack, down from 530. `[I]` until compiled.
- Bench: rebuild, update hand-typed strip numbers in `test_firmware_rev1.js`, republish REV1 bench.

### Not done

No code, xlsx, DXF or bench changes. No git commit.

---

## 2026-09-14 20:48 CDT - FLISR_Trainer_REV2: REV1 copied and updated to the 352 px LED sheet; REV2 bench published and pinned

Follows the 20:11 entry. **Supersedes** its "Revision scope once cleared (not started)" section, and the
pin state in the 2026-09-13 22:25 entry (REV1 bench pinned).

### What was asked

User answers to the 20:11 flags and questions: `[V]`
- N28 x corrected in the xlsx. Re-read: now (41.10, 29.03); no other cell changed.
- LED 13 = 29 px is correct.
- LED 1 = 5 px south of N1 (Sub A bus) + 9 px N1 -> N2, as assumed.
- The `note` in LED!F27 is obsolete. It was left in the workbook; this session did not edit the xlsx.

Then: **copy REV1 to a new REV2, do not touch REV1, update the copy, update the artifact and repin it.**
Interpretation, stated to the user `[I]`: the REV2 bench is a new artifact (as REV1 was for REV0), it gets
the pin, and the REV1 bench is unpinned but stays published. REV0 was not touched.

### FLISR_Trainer_REV2/FLISR_Trainer_REV2.ino

A byte copy of REV1, then edited. The logic section differs from REV1 **only in the boot banner**
(`=== JEA Tabletop FLISR Trainer REV2 ===`); checked by diffing the two logic sections. `[V]`

Config changes: `[V]`
- `NUM_LEDS` 337 -> 352. `SEG_LEN` = 14,17,17,10,17,18,2,8,6,8, 17,14,29,28,12,4,7,6,9,10,
  3,22,12,5,7,7,4,12,3,11, 13.
- Index 24 is now LED 25 (7 px, Over 0, hidden) instead of J1. **Every run's array index is LED ID - 1.**
  SEG_OVER, SEG_ZONE, SEG_ZONE2, SEG_FROM, SEG_TO, TAP (index 27 px 7), TIE_NODE unchanged.
- `SEG_SPLIT[0]` 8 -> 5 (BUSA 5 px, then Z1 9 px). Other splits unchanged (index 3 = 2, 20 = 1, 30 = 2).
- New REV2 CHANGES block in the header; block [4] doc table renumbered (J1 row gone, 25 - 31); notes on
  run 1, N30 and run 13 updated; pixel counts in comments 337 -> 352.

Re-picked tables, computed with the bench's own pixel placement and the rules already written in blocks
[2] and [4c]: `[V]` computation, `[I]` physical fit

| Item | REV1 (index, px, strip) | REV2 (index, px, strip) | Why |
|---|---|---|---|
| Z1 fault start | 0, 16, 16 | **0, 13, 13** | run 1 is 14 px; px 13 is 0.15 in from the Fault sheet point |
| SUB_A_BKR status | 0, 7, 7 | **0, 4, 4** | last bus pixel before N1 |
| DEV_A2 status | 7, 8, 105 | **7, 7, 102** | run 8 is 8 px; old px 8 is past its end |
| TIE status | 17, 0, 221 | **16, 6, 227** | rule flip: run 17 px 6 is 0.275 in from E4, run 18 px 0 is 0.302 in. Run 17 grew 6 -> 7 px. Close call. |
| DEV_A1, DEV_B2, DEV_B1, SUB_B_BKR, DER_PCC | same index/px | strip 50, 253, 313, 278, 340 | shift only |
| Z2 - Z6, DER fault starts | same | strip 55, 211, 231, 317, 284, 343 | shift only |

REV1's pick for TIE (17, 0) still passes every bench check with 0 warnings, so either is valid; the board
decides. `[V]`

### Bench (FLISR_Trainer_Sim/)

- `build_sim.py`: added a `FLISR_Trainer_REV2` entry and a docstring note. No logic change.
- `firmware_rev2.js`: copy of `firmware_rev1.js`, banner changed, `PORTED_LOGIC_SHA256`
  `1bb43e0321657ddbce6d245b26fbfd68cf16c76f9cdd821da2647adc8a50bc43`.
- `test_firmware_rev2.js`: copy of the REV1 tests.
  - Hand-typed `DEV_STRIP` = 4, 50, 102, 227, 253, 313, 278, 340; banner and 352 checks; bad-entry table
    updated; identifiers renamed REV2 / CFG2 / r2.
  - **The REV0 reference now runs on the REV2 strip:** REV0's own config with NUM_LEDS and the SEG_*
    tables swapped for REV2's. The test first asserts every other define REV0 and REV2 share is identical.
- Built: `FLISR_Trainer_REV2_Sim.html`, `sim_config_rev2.json`.

### Verification actually performed

1. **Bench build** REV2: 12 of 12 checks, 0 warnings. All 31 rows match the xlsx on From/To, len and
   Over. `[V]`
2. **Tests:** REV2 18 of 18, REV1 18 of 18, REV0 20 of 20. `[V]`
3. **Mutation checks, config side.** REV1-era values planted in a scratch copy of the REV2 .ino, then
   built. 8 of 8 caught: `[V]`
   - fail: Z1 px 16, Z1 px 12 (valid pixel, not the nearest), DEV_A2 px 8, LED 17 len 6
   - warn: split 8, SUB_A_BKR px 7, NUM_LEDS 337, LED 25 Over 1
4. **Mutation check, test side.** TIE table moved back to (17, 0) in a scratch `sim_config_rev2.json`:
   15 of 18 REV2 tests fail. `[V]`
5. **Compiled for Uno.** The build script was rebuilt in the scratchpad: avr-gcc 7.3.0, core 1.8.8, IDE
   flags from `platform.txt` (`-Os -flto -std=gnu++11`), FastLED `src/fl/build/*.cpp`. `[V]`
   - Recipe check: REV1 reproduces the 11:18 entry exactly, flash 10,894 B / SRAM 1,518 B.
   - **REV2: 0 warnings with `-Wall -Wextra`, flash 10,894 B, SRAM 1,563 B, 485 B free.**
   - A planted unused variable produced 1 warning, so warnings were on.
6. **REV1 untouched:** md5 of `FLISR_Trainer_REV1.ino`, `firmware_rev1.js`, `test_firmware_rev1.js`,
   `sim_config_rev1.json`, `FLISR_Trainer_REV1_Sim.html` and `sim_template.html` all equal the hashes taken
   before any edit. `[V]`
7. **REV1 and REV0 benches can no longer be rebuilt against the xlsx.** Both fail with
   `run 25: .ino says N27->N34, xlsx says N28->N27`. Run in a scratch copy, so their built pages were not
   overwritten. `[V]`
8. **One headless Chrome screenshot** of the REV2 page before publishing:
   - 352 px, REV2 banner
   - 7 white status pixels, TIE amber at px 227
   - industrial lateral drawn out to x 41.10
   `[V]`
9. Not run on hardware.

### Deliverables

| Thing | Where |
|---|---|
| REV2 sketch | `FLISR_Trainer_REV2/FLISR_Trainer_REV2.ino` |
| REV2 bench, published and **pinned** | `https://claude.ai/artifact/UqFf6AK9WtKi7aw1s8myjj`, source `FLISR_Trainer_Sim/FLISR_Trainer_REV2_Sim.html` |
| REV1 bench, **unpinned**, still published | `https://claude.ai/code/artifact/e104d46c-45b6-412a-890d-59185b0d97d4` (the unpin result reported it as `https://claude.ai/artifact/Unc5QR4dM4g4VPegPFouwy`) |
| Bench sources | `build_sim.py` (edited), `firmware_rev2.js`, `test_firmware_rev2.js`, `sim_config_rev2.json` (new) |

Scratchpad only, gone after the session: `avr_build.sh` (recipe in item 5), `tables.py` (pick computation),
mutation copies.

### Open items, flagged not resolved

Continues the list:

32. **Pick one master xlsx per revision if old benches matter.** The shared LED sheet now matches only REV2,
    so REV0 and REV1 benches cannot be rebuilt (item 7 above). Their published pages still work.
33. **TIE status pixel changed sides** (now the last pixel of LED 17, on the Z3 side of N12). Add it to the
    item 26 board check. To go back: block [2], TIE `DEV_SEG` 17, `DEV_PX` 0.
34. Items 22 and 17 updated: SRAM headroom for REV2 is **485 B**.
35. `#Cardboard Layout REV1 backup_9.12.20.dxf` (the `#` copy) shows modified in git, mtime 20:41 today. This
    session did not write it, and the bench reads the non-`#` file. Probably an AutoCAD save. `[I]`
36. Item 20 is narrower: FastLED `src/` now holds 13 top-level `.cpp` files, all dated 2026-03-07, not 136.
    They are still old-version files, so an IDE upload may still fail until FastLED is reinstalled. `[V]`
    count and dates, `[I]` effect.
37. Items 28 and 31 stand: REV0 is still unretired, and `__pycache__/build_sim.cpython-314.pyc` changed again.

### Not done

- No change to REV1, REV0, the xlsx, either DXF, or the plan set artifact.
- No hardware test. No git commit.

---

## 2026-09-14 22:45 CDT - FastLED install cleaned: 631 leftover 3.10.3 files archived. The IDE compile then stops on a separate sketch bug in REV2 and REV1

### Request

"address the fastLED library problem" (items 20 and 36). The user also said:
- It is fine that the REV0 and REV1 benches cannot be rebuilt. REV2 is the only physical design now, and the
  REV0 and REV1 boards no longer exist. Item 32 closed.
- Leaving the `#` DXF alone was correct. Item 35 closed, no action.

### Diagnosis `[V]`

- **The IDE's download cache still has both versions.** `C:\Users\jprun\AppData\Local\Arduino15\staging\libraries`
  holds `FastLED-3.10.3.zip` (2026-03-07 21:39) and `FastLED-3.10.5.zip` (2026-07-28 09:02).
- **The install was all of 3.10.5 plus 631 files of 3.10.3.** 4,611 files:
  - All 3,980 files of the 3.10.5 zip were present and sha256-identical.
  - The 631 extras all matched the 3.10.3 zip by path and size. Content was confirmed after archiving.
  - 209 of the extras were OneDrive online-only placeholders (Offline + RecallOnDataAccess).
- **140 compilable leftovers** (.cpp/.c/.S) under `src/`, 13 of them at the top level. Item 36's "13, not 136"
  compared a top-level count with a recursive one. The recursive count never dropped. Item 36 was wrong.
- **55 FastLED folders had mtime 2026-07-28 18:39**, 9.5 h after the 09:02 install. `[I]`, medium: OneDrive put
  the 3.10.3 files the IDE had deleted back into the new install.
- **Correction to the toolchain note (21:22 entry):** the Arduino IDE is at `C:\Program Files\Arduino IDE`, not
  `AppData\Local\Programs`.
  - It bundles arduino-cli 1.4.1 at `resources\app\lib\backend\resources\arduino-cli.exe`, so "no arduino-cli"
    was wrong.
  - IDE config: `C:\Users\jprun\.arduinoIDE\arduino-cli.yaml`. Sketchbook `c:\Users\jprun\OneDrive\Documents\Arduino`.
  - IDE-equivalent compile: `arduino-cli compile --config-file <that yaml> --fqbn arduino:avr:uno --build-path <scratch> <sketch dir>`

### Reproduced before fixing `[V]`

1. **Unmodified REV2 fails in the sketch first,** before any library is compiled. 3 errors:
   `'Piece' has not been declared` / `'Piece' does not name a type`, at getPiece, distInPiece, colorForPixel.
   - The IDE inserts generated prototypes above the first function (`computeModel()`, .ino line 443).
   - `struct Piece` is declared later, at line 518.
2. **With the sketch problem out of the way, FastLED fails.** A scratch copy of REV2 with only the
   `struct Piece` line moved above `computeModel()` gives 1,172 errors, all inside FastLED:
   - old headers such as `src/fl/move.h` and `src/fl/type_traits.h` redefine types that 3.10.5 keeps in
     `src/fl/stl/`
   - old `src/cled_controller.cpp` is compiled too

### Fix

- **631 leftover files archived through `vault.ps1`,** as 511 entries: 39 folders that held only leftovers, plus
  472 files from mixed folders.
  - Reason on every entry: `FastLED 3.10.3 leftover mixed into the 3.10.5 install; breaks Arduino IDE compile (2026-09-14)`
  - Manifest: `C:\Users\jprun\.claude-vault\c-Users-jprun-Downloads-JEA Project\manifest.jsonl`
  - To undo: run `vault.ps1 restore <id>` for every manifest line with that reason.
- **The 3.10.5 files were not touched.** No reinstall was needed, because they already matched the IDE's own zip.
- Scripts `compare.py`, `archive_batch.ps1`, `verify_after.py`, `poll.py` lived in the scratchpad.

### Verification actually performed

1. **Install equals the 3.10.5 zip:** 3,980 of 3,980 files identical, 0 extra, 0 missing. 28 compilable files
   under `src/`. `[V]`
2. **Vault copies are complete:** 511 entries, 631 files, all sha256-equal to the 3.10.3 zip, none left as a
   placeholder. `[V]`
3. **Compiled with the IDE's arduino-cli, `--warnings all`:** `[V]`
   - Scratch REV2 with `Piece` moved: OK. Flash 10,894 B, SRAM 1,563 B, 485 B free. These equal the manual
     avr-gcc recipe from the 20:48 entry.
   - REV0 unmodified: OK. Flash 9,176 B, SRAM 1,439 B, 609 B free.
   - Both: 0 warnings from the sketch. 29 come from inside FastLED and 4 from the core's `new.cpp`. The IDE's
     default warning level hides them.
   - REV2 and REV1 unmodified: fail with the 3 `Piece` errors each, and nothing else.
4. **OneDrive recreated 19 empty folders** about 50 s after they were archived. Example: `src\fx` archived
   22:38:07, recreated 22:38:57. No files came back in a 16-sample poll from 22:40:30 to 22:45:32 (3,980 files,
   0 dated 2026-03-07, 0 online-only throughout). The empty folders hold no files, so nothing compiles from them.
   `[V]` for that window only.
5. **Not uploaded to a board.** The IDE GUI was not used. The CLI is the build engine the IDE runs.

### Open items, flagged not resolved

Items 20 and 36 are resolved. Item 32 closed by the user. Item 35 closed.

38. **REV2 and REV1 do not compile in the Arduino IDE** (reproduction step 1). `[V]`
    - Fix: move `struct Piece { uint8_t lo, hi, a, b; };` above `computeModel()`.
    - That line is in the logic section, so `PORTED_LOGIC_SHA256` in `firmware_rev2.js` must be updated and the
      bench rebuilt. The behavior is unchanged.
    - REV1 was left alone: the user said not to touch it.
    - Not done: not requested.
39. **OneDrive may put the leftovers back again,** as it apparently did on 2026-07-28, that time 9.5 h later.
    - Check: any FastLED file dated 2026-03-07, or a compile error naming `src/fl/move.h`.
    - Root cause `[I]`: the Arduino sketchbook lives in OneDrive, which fights the IDE's delete-then-install
      library updates.
40. **Compile checks should use arduino-cli from now on.** The manual avr-gcc recipe (11:18 and 20:48 entries)
    compiled the `.ino` as plain C++. It skips the IDE's prototype generation, so it could not catch item 38.

---

## 2026-09-15 - Item 38 fixed in REV2: struct Piece moved above the first function. REV2 bench build now blocked on its logic hash

Jordan hit the three `Piece` errors compiling REV2 in the Arduino IDE and asked for them to be addressed.
This is open item 38, fixed exactly as that item specified. REV1 was left alone, per the standing instruction.

### The mechanism

The `.ino` preprocessor writes the auto-generated function prototypes in just above the **first** function
definition in the sketch, `void computeModel()`. `struct Piece` was declared at .ino line 518, far below it, so
the three prototypes that take a `Piece &` were emitted against a type that did not exist yet. The generated
`.cpp` carries a `#line` directive per prototype pointing back at the corresponding **definition**, which is why
the IDE reported 521 / 563 / 699 (the definitions) rather than the insertion point. That is what made this look
like a contradiction: the struct is plainly above line 521 in the file you are reading. `[V]`

### The change

`FLISR_Trainer_REV2/FLISR_Trainer_REV2.ino`, one line moved, nothing else:

- `struct Piece { uint8_t lo, hi, a, b; };` moved from line 518 up to line 405, just after `SRC_IS_TIE` and
  above `computeModel()`. A comment there explains why it cannot live with the LINE WALKING block.
- The LINE WALKING banner gained a two-line pointer to the new location.

Behavior is unchanged. This is a declaration-order move only.

### Verification actually performed

arduino-cli is still not installed (item 40 asks for it), and no arduino-cli ships inside
`%LOCALAPPDATA%\Programs\Arduino IDE`. So the check was built to close the exact gap item 40 named: a script
that **emulates the prototype hoisting** (inserts all 27 prototypes above `computeModel()`, prepends
`#include <Arduino.h>`) and then runs avr-g++ `-fsyntax-only -std=gnu++11 -mmcu=atmega328p`, with the 1.8.8 core
and the installed FastLED on the include path.

1. **Reproduced against the HEAD copy of REV2:** the same 3 errors, at the same columns 37, 49 and 60, on the
   hoisted prototypes for `getPiece`, `distInPiece` and `colorForPixel`. Nothing else. `[V]`
2. **The fixed file passes:** exit 0, no errors. `[V]`
3. FastLED did **not** produce the 1,172-error wall from the 22:45 entry, so that cleanup is still holding.
   Only 2 warnings appeared, both unrelated: the `util/delay.h` "optimizations disabled" warning, which is an
   artifact of `-fsyntax-only` with no `-Os`, and a FastLED experimental-code `#warning`. `[V]`
4. **Not compiled to a binary and not uploaded.** `-fsyntax-only` produces no object file, so there are no new
   flash or SRAM figures. The 20:48 and 22:45 entries measured 10,894 B flash on a scratch copy with this same
   line moved, so the size is expected to be unchanged, but that is `[I]` for this file.

### Consequence, confirmed not fixed

The moved line sits below `NOTHING BELOW HERE NEEDS EDITING`, so it is inside the hashed logic section, as item
38 warned. `python build_sim.py --sketch FLISR_Trainer_REV2` now stops at the guard:

    .ino logic sha256 : bd1ebd379f75ce7aa460702cdb5ad551d6755fc58926ebb8000eb2a5f596b605
    port written for  : 1bb43e0321657ddbce6d245b26fbfd68cf16c76f9cdd821da2647adc8a50bc43

The guard fires before anything is written, so no bench file was touched. `firmware_rev2.js` needs no ported
logic change (a struct moving does not change behavior); it needs `PORTED_LOGIC_SHA256` set to the `bd1ebd37`
value and the bench rebuilt. Not done: not requested.

### Open items

Item 38 is resolved for REV2 and is now split:

38. **RESOLVED for REV2.** REV1 still does not compile in the Arduino IDE, same 3 errors, same cause, same
    one-line fix. Left alone deliberately: the user said not to touch REV1. `[V]`
41. **The REV2 bench will not build until `PORTED_LOGIC_SHA256` in `firmware_rev2.js` is bumped to
    `bd1ebd379f75ce7aa460702cdb5ad551d6755fc58926ebb8000eb2a5f596b605`** and the page rebuilt. The published and
    pinned `FLISR_Trainer_REV2_Sim.html` is stale by one declaration move, which does not affect what it
    simulates. `[V]`
40. **Still open, but partly mitigated.** The emulated-hoist script above does catch prototype-order bugs, which
    the plain avr-gcc recipe could not. A real arduino-cli is still the better answer.

---

## 2026-09-17 10:12 CDT - Question list for the 2026-09-22 JEA meeting

### What was asked

User is presenting the LED display to JEA on Tuesday 2026-09-22 (Zach, possibly Michael). They know two
things going in: the practical layout has a section that needs revision, and not all necessary components
are modeled. Asked for a comprehensive list of questions to ask JEA to make progress toward the real
(full-scale) trainer. No file output requested; delivered as chat text only.

### Sources read this session

`jea-project-memory-file.md` (the standing-instruction memory), this file (Standing Facts plus the full
log, all entries through the 2026-09-15 struct-Piece fix), `jea_oneline_component_reference.md` in full.
`[V]`

### What was produced

A ~33-question list, grouped: (A) section/topology layout, (B) components not yet modeled, (C) one-line
facts still open per the component reference section 8 (transformer ownership, 46 kV loop vs radial,
delivery-point independence, Viper-ST/SEL-651R pairing, industrial-branch scope), (D) Axion/RTAC hardware
form factor (mounting orientation, backplane slots, 120 VAC scope, laptop vs DisplayPort), (E) real device
dimensions for scale sign-off, (F) Milsoft/load-transfer data needs, (G) BOM overhead-vs-underground
exercise, (H) schedule/budget/procurement, (I) meeting logistics for the 22nd itself. Roughly a third
flagged `[T]` as Tuesday-priority because they unblock the layout revision or the missing-components list
directly. Did not invent new facts; every closed-ended question traces to an item already `[V]` or `[I]`
in this file or the component reference (open items 1-11 list above, and component reference section 8).
Delivered in chat only, not written to a new file. User was offered a trim-to-Tuesday-only version or a
printable checklist; not yet requested.

### Not done

No changes to any layout, spec, DXF, xlsx, or firmware file. No new file created for the question list
itself, per the no-unrequested-documents default; can be added on request.

---

## 2026-09-17 10:46 CDT - Working directory reorganized into numbered category folders

### What was asked

"Organize this JEA Project folder, don't delete anything, just organize it, ask me any questions, if
none, execute." No content changes implied or made. `[V]`

### Questions asked and answers

- Folder naming style: numbered prefixes (`01_`, `02_`, ...) so File Explorer sorts in workflow order.
  Chosen over plain names. `[V]`
- Whether to commit the reorg to git: yes, one commit, moves recorded as renames. `[V]`

### Sources read this session

`jea-project-memory-file.md` (standing instruction), this file's header and the 2026-09-15 / 09-17
entries, a full recursive listing of the working directory, `git ls-files` and `git status --porcelain`
(confirmed everything except this file was clean before starting), and `flisr-capstone-memory-export.md`
(header only, to confirm it is project-relevant memory content, not disposable). `[V]`

### New top-level layout

| Folder | Contents |
|---|---|
| `01_Admin_Meetings/` | JEA Contacts, meeting transcript/PDF, preliminary presentation, scope of work docx |
| `02_Planning/` | Gantt chart xlsx, `Gantt_Chart_PDFs/`, cardboard prototype tabulated xlsx |
| `03_OneLine_Diagram/` | one-line pdf/png/svg and both component reference `.md` files |
| `04_Cardboard_Layout/` | current DXFs (REV0, REV1), REV1/REV3 renders, layout spec, `Cardboard Layout Tiles/`, plus a `Backups/` subfolder for every `backup_*`, `.dxf~`, the `#`-prefixed autosave copy, and `JEA Prelim Layout.dxf(~)` |
| `05_Firmware/` | `FLISR_Trainer/`, `FLISR_Trainer_REV1/`, `FLISR_Trainer_REV2/`, `FLISR_Trainer_Sim/` moved in whole, untouched internally |
| `06_DXF_Tools/` | `tile_dxf.py`, `tile_dxf_text.py`, `test_tile_dxf.py`, `test_tile_dxf_text.py` |
| `07_Reference_Datasheets/` | `135187.pdf`, SEL-2240 datasheet/summary, Axion instruction manual and panel drawings |
| `08_Presentations_Concepts/` | REV2 pptx, AI concept render, UU Senior Design Concept dwg(~) |
| `09_Assets/` | Electrical symbol SVG icon set (folder + its source zip), the generic house `.jpg` reference image |

`PROJECT_MEMORY.md` and `flisr-capstone-memory-export.md` were deliberately left at the working-directory
root: the standing memory instruction names this exact path for `PROJECT_MEMORY.md`, and moving it would
have broken that reference for future sessions. `[V]`

**Judgment call, not asked `[I]`:** `#Cardboard Layout REV1 backup_9.12.20.dxf` was filed under `Backups/`
alongside its non-`#` twin. Item 35 (2026-09-14 22:45 entry) says leaving this file *alone* was correct
when the question was whether to touch its *content* — it was not, here, only relocated by `git mv`, byte
for byte. Flagging in case that reasoning does not extend to a location change.

### Cleanup done via the vault (archived, not deleted)

- `~$A_Senior_Design_Scope_of_Work (1).docx` and `~$Tabletop Smart Grid & Distribution Automation Trainer
  REV2.pptx` -- Office lock-file artifacts, both were tracked in git (accidentally committed while the
  real files were open), not real content. Restore ids `42c58a3b` / `c50f8c61`. `[V]`
- Root `__pycache__/` (5 `.pyc` files, including `prev_tile_dxf.cpython-314.pyc`, an orphan with no
  matching `.py` source anywhere in the tree) -- disposable bytecode cache; regenerates next time the
  `06_DXF_Tools` scripts run. Restore id `e3ce40b4`. `[V]`
- `FLISR_Trainer_Sim/__pycache__/` was left alone; it moved with its parent folder intact.

### Verification actually performed

1. `git status --porcelain` before starting showed only `PROJECT_MEMORY.md` modified; everything else was
   clean, so every file below was tracked and `git mv` was used throughout (not a plain filesystem move).
   `[V]`
2. All 57 planned `git mv` operations reported success; a `MISSING`/`FAILED` guard in the move script
   never fired. `[V]`
3. After the moves, `git add -A` plus `git status --porcelain` showed exactly: renames for every moved
   path (git's own similarity detection, no manual `-M` flag needed), 5 deletions for the archived
   `__pycache__` files, 2 deletions for the archived lock files, and the pre-existing `PROJECT_MEMORY.md`
   modification. No unexpected adds, deletes, or path collisions. `[V]`
4. Root directory listing after the move: exactly the 9 numbered folders plus the two memory `.md` files.
   `[V]`
5. Not verified: that every firmware/simulator internal relative path (e.g. anything in `build_sim.py` or
   the `.ino` sketches referencing sibling files by relative path) still resolves. Folders were moved as
   whole units with internal structure untouched, so relative references inside them should be unaffected,
   but this was reasoned, not executed/tested. `[I]`

### Deliverables

- New folder tree described above, committed. Commit message references this reorg.
- This log entry.

### Open items, flagged not resolved

Continues the list; items 26-27, 33-34, 37-41 stand unchanged.

42. **Firmware build tooling not re-tested after the move.** `05_Firmware/FLISR_Trainer_Sim/build_sim.py`
    and the arduino-cli emulated-hoist check (2026-09-15 entry) were not re-run from their new path. If
    either script uses a path relative to the old working directory rather than its own file location,
    it may need a working-directory argument going forward. `[I]`
43. **`135187.pdf` (`07_Reference_Datasheets/`) was filed by filename pattern only** -- its content was
    not opened this session (no PDF renderer available in this environment). If it turns out not to be a
    datasheet, it should move.

### Not done

No file content was changed, no file was deleted (two lock files and a stale pycache folder were archived
to the vault, fully recoverable), and no firmware/script logic was touched. Build/test tooling was not
re-run from the new paths (item 42).

---

## 2026-09-17 11:15 CDT - Implemented the "JEA FLISR Trainer" Claude Design page locally, fixed for the numbered-folder reorg

### What was asked

Import a Claude Design project (`https://claude.ai/design/p/8abb872b-fc8a-4b2a-a0d0-2c777e5ee9c9`, a
public landing page for the repo, meant to be reached by scanning a QR code on the physical table) via the
`DesignSync` MCP tool, and implement `JEA FLISR Trainer.dc.html` in this working directory. `[V]`

### Sources read this session

`jea-project-memory-file.md`, this file's header/Standing Facts and the 2026-09-15 / 09-17 10:12 / 09-17
10:46 entries, then via `DesignSync get_file` against project `8abb872b-fc8a-4b2a-a0d0-2c777e5ee9c9`: the
full `JEA FLISR Trainer.dc.html`, `github.md`, and the entire `_ds/industry-1e5685ad-.../` bundle
(`readme.md`, `_ds_manifest.json`, `styles.css`, `_ds_bundle.js`, `_adherence.oxlintrc.json`) and
`support.js`. `[V]`

### First blocker, resolved

`DesignSync` initially refused every call: "needs design-system authorization, and `/design-login` cannot
run in this non-interactive session." Told the user plainly rather than working around it. Jordan ran
`/design-login` from an interactive session on this machine; `get_project` then succeeded
(`type: PROJECT_TYPE_PROJECT`, `canEdit: true`, owner Jordan). `[V]`

### The complication: the design was authored against the pre-reorg flat layout

`JEA FLISR Trainer.dc.html` came back from the design project **fully authored already** -- hero, an
embedded `<iframe>` of the REV2 simulator, a "how it works" section built from the one-line SVG, and a
React-driven file browser covering all 61 repo files with links to
`https://github.com/Xavier8264/JEA-Project/blob/main/...`. It was not a stub. But every relative path in it
(`Cardboard Layout REV3.png`, `FLISR_Trainer_Sim/FLISR_Trainer_REV2_Sim.html`,
`jea_power_delivery_oneline.svg`, and all 61 file-browser entries) assumed the **flat pre-reorg root**, and
by the time this session got authorization, the 10:46 CDT reorg above had already moved every one of those
files into the numbered folders. Verified the git remote is in fact `Xavier8264/JEA-Project`, so the
file-browser's GitHub links were the right repo, just stale paths. `[V]`

### Decisions and why

- **Placed `JEA FLISR Trainer.dc.html`, `support.js`, and `_ds/industry-1e5685ad-.../` at the true
  repository root**, alongside `PROJECT_MEMORY.md` and `flisr-capstone-memory-export.md`, not inside a
  numbered folder. Reasoning: this file's own footer says "Scanned a QR code on the table? You're in the
  right place" -- it is the repo's public entry point, the same role `PROJECT_MEMORY.md` was deliberately
  kept at root for in the 10:46 entry. `[I]`, but consistent with that precedent.
- **Rewrote every relative path** (hero image, one-line SVG, both simulator links, the iframe `src`, the
  two footer "Start here" doc links, and all 61 entries in the embedded `GROUPS` file-browser data) to
  match the post-reorg tree, cross-checked against the reorg entry's own folder table. Left the two
  single-folder groups (`Simulator` -> `05_Firmware/FLISR_Trainer_Sim/`, `Electrical symbol icon set` ->
  `09_Assets/Electrical symbol SVG icon set/`) on the existing `ROOT_FOLDER`-prefix mechanism; the four
  groups whose files now span multiple numbered folders (Drawings & panel layout, Reference documents,
  Build & export scripts, Meetings & planning) got full repo-relative paths written directly into each file
  tuple instead, with the group `path` label listing the folders it now spans. No file was added to or
  removed from the original 61; file sizes/descriptions were carried over as authored, not re-measured.
  `[V]` for the mapping (checked against a fresh `find` of the actual tree), `[I]` that this was the
  intended fix rather than, say, re-flattening the repo -- not asked, so this was the smaller/safer of the
  two changes.
- **Did not write `github.md` locally.** It is the design tool's own sync bookkeeping (last-sync timestamp,
  a screen map) with no functional role in the page or the repo -- unlike `support.js`/`_ds/`, nothing
  references it. `[I]`
- **Did not push the corrected page back to the hosted Claude Design project.** The `DesignSync` write path
  (`finalize_plan`/`write_files`) exists but is scoped in its own tool description to design-system
  projects and an explicit user-reviewed plan; this project is `PROJECT_TYPE_PROJECT`, and overwriting the
  user's hosted design without being asked is a visible, external action outside what was requested.
  Flagging as a next step rather than doing it. Not done: not requested.

### Verification actually performed

1. `node --check` on `support.js`, `_ds_bundle.js`, and the extracted embedded `<script data-dc-script>`
   block: all three parse as valid JS. `[V]`
2. Regex-scanned every static `src=`/`href=` in the written `.dc.html` against the filesystem: all 6 local
   references (`./support.js`, the two `_ds/` files, the hero PNG, the one-line SVG, the simulator HTML)
   resolve; the one non-match was `{{ f.url }}`, a runtime template placeholder, not a real path. `[V]`
3. **Rendered in a real browser**, not just statically checked: installed `puppeteer-core` into the
   scratchpad (no bundled Chromium download -- pointed it at the existing
   `C:\Program Files\Google\Chrome\Application\chrome.exe`), served the working directory with
   `python -m http.server 8934`, and drove the page headlessly.
   - Initial load: hero, stat plate, and the embedded REV2 simulator iframe all rendered correctly styled
     (Barlow Condensed headings, blueprint corner marks, steel-accent duotone on the one-line image).
     Screenshot inspected directly. `[V]`
   - Console/network: exactly one error, `favicon.ico` 404 (confirmed against the `http.server` access log
     -- browser default request, not a page asset). Zero other console or `pageerror` events. `[V]`
   - The iframe's own document was inspected (not just "an iframe exists"): it resolved to
     `.../05_Firmware/FLISR_Trainer_Sim/FLISR_Trainer_REV2_Sim.html` and its body text read "FLISR Trainer
     REV2 Test Bench" -- the real simulator, not a blank or error frame. `[V]`
   - Clicked "Expand all" via a real DOM click (not simulated), then re-screenshotted: all 6 file-browser
     groups opened, all 61 files listed. `[V]`
   - Extracted the **runtime-rendered** `href` attributes (not the source template) for all 61
     file-browser links: every one starts with the expected
     `https://github.com/Xavier8264/JEA-Project/blob/main/` base, and spaces in filenames
     (e.g. `Cardboard Layout REV3.png`) are correctly percent-encoded in the live DOM. `[V]`
4. Killed the verification `http.server` process afterward (`Stop-Process` by PID, matched on the bound
   port) so nothing was left listening. `[V]`

### Deliverables

- `JEA FLISR Trainer.dc.html` (repo root) -- the implemented, path-corrected landing page.
- `support.js` (repo root) -- the DC/x-dc runtime (loads React/ReactDOM/Babel from unpkg at runtime; not
  bundled).
- `_ds/industry-1e5685ad-55b7-4b09-aebc-d9d638a0ee4d/` (repo root) -- `styles.css`, `_ds_bundle.js`,
  `_ds_manifest.json`, `readme.md`, `_adherence.oxlintrc.json` -- the "Industry" design system this page is
  built on.
- This log entry.
- Not yet committed to git -- left for the user, per the standing "don't commit unless asked" instruction.

### Open items, flagged not resolved

Continues the list; items 26-27, 33-34, 37-40, 42-43 stand unchanged. Item 41 (REV2 bench
`PORTED_LOGIC_SHA256`) is unrelated to this entry and still open.

44. **Not synced back to the hosted Claude Design project.** The corrected paths exist only in this working
    directory. If Jordan edits further in the Claude Design UI, it will still show the stale pre-reorg
    paths until someone pushes this version back (or re-derives it there). Ask before doing that -- it
    writes to a project visible outside this repo.
45. **File sizes and descriptions in the file browser are exactly as authored in the design**, not
    re-measured against the current files (e.g. `PROJECT_MEMORY.md` is listed as "124 KB" but has grown
    past that since -- this entry alone adds several KB). Cosmetic; paths (the functional part) were the
    only thing fixed.
46. **`github.md`'s own "Last sync" / screen-map bookkeeping was read but not carried locally** -- it is
    Claude Design's internal state, not repo content the page depends on. Flagging in case that judgment
    call was wrong.

### Not done

Did not push anything back to the hosted Claude Design project (item 44). Did not commit the new files to
git. Did not re-measure file sizes in the file-browser data (item 45). Did not add the three `.ino` firmware
sketches to the file browser's "Simulator" group -- they were absent from the design as authored and adding
them was not asked.

---

## 2026-09-17 12:00 CDT - Sensitive-information sweep

### What was asked

Search the working directory for potential sensitive information.

### Findings `[V]`

**Note on where this entry can be published:** this file is itself tracked in git and pushed to
`github.com/Xavier8264/JEA-Project`, which is confirmed **public** (`GET /repos/Xavier8264/JEA-Project` returns
`"private": false"`). Deliberately not repeating the actual PII below -- see the chat session (2026-09-17) for
the redacted-in-chat detail, or the two files themselves in git history, if it needs to be looked at again.

1. **`01_Admin_Meetings/JEA Contacts.docx` -- real JEA staff PII, currently live in git history.** Contains four
   named JEA employees with their titles, work emails (`@jaxenergy.com`) and phone numbers. The file was
   committed in `8b63a71` ("Organize JEA Project into numbered category folders") and is currently shown as
   `deleted` (unstaged) in the working tree per `git status` -- but that deletion has **not been committed or
   pushed**, so the file with full contact details is still present in the public repo's history and on
   `origin/main` right now. Deleting the working-copy file alone does not remove it from history or from GitHub.
2. **Presentation slide with sponsor contact info, currently committed and live.**
   `08_Presentations_Concepts/Tabletop Smart Grid & Distribution Automation Trainer REV2.pptx` has a slide
   containing Zach Wadley's `@jaxenergy.com` email and phone number. This is in the current HEAD and on
   `origin/main`, not just history. May be intentional (a contact slide for a real presentation) rather than a
   leak -- worth confirming with the user rather than assuming it should be scrubbed.
3. No other credential-class findings: no API keys, passwords, private keys, WiFi/IP secrets, or SSH/PGP key
   material anywhere in the tree (firmware, DXF tools, `_ds` design-system scaffold, sim HTML, xlsx/docx/pdf
   internals all checked). The only "password/secret/token" grep hits were false positives (CSS/design-system
   "token" terminology, template placeholder tokens in `build_sim.py`).
4. `jea_power_delivery_oneline_reference.md` states real utility statistics (JEA = Jackson Energy Authority,
   Madison County TN, ~35,000 customers, 29 substations, 53 transformers, 700+ mi distribution). Not
   classified, likely near what JEA publishes itself, but it is real named-utility infrastructure detail sitting
   in a public repo. No GPS/street-level/customer-address data found anywhere -- the "no GIS, nothing locatable"
   directive from the 8/27 kickoff (Standing Facts above) appears to have been honored everywhere except the
   two files above.

### Verification actually performed

- `git show 8b63a71:"01_Admin_Meetings/JEA Contacts.docx"` extracted and its `word/document.xml` parsed directly
  to confirm real names/emails/phones, not a template placeholder.
- `curl https://api.github.com/repos/Xavier8264/JEA-Project` confirmed `"private": false"` / `"visibility":
  "public"` unauthenticated -- i.e., actually publicly readable right now, not just "has a remote."
- pptx slide XML parsed directly (regex over `ppt/slides/slide*.xml`) for the email/phone hit, not inferred from
  a filename.
- Broad regex sweep (email, phone, `password|secret|api_key|token|credential|private_key`, PEM/SSH headers,
  AWS key prefix, WiFi/IP literals) run across every text-bearing file type in the tree, plus targeted
  extraction of docx/xlsx/pptx internal XML, which plain-text grep cannot see into.

### Open items, flagged not resolved

12. **Public PII exposure needs a decision from the user**, not just a local file deletion. Two options if the
    user wants it gone: (a) have GitHub scrub it (repo owner is `Xavier8264`, not this session's git identity,
    so this session cannot push a history rewrite there without being asked and without write access being
    confirmed), or (b) treat it as already public and just finish the local cleanup (commit the `JEA Contacts.docx`
    deletion, decide on the pptx slide) while accepting the exposure already happened. Not decided here --
    flagged for the user.
13. Confirm whether the pptx contact slide is intentional (a normal presentation contact slide) before treating
    it as a finding rather than a feature.

---

## 2026-09-20 22:48 CDT - "What is the next task?" Status review against the Gantt and SOW

### What was asked

"What is the next task in order to make progress in this project." Answered in chat only. No files changed
other than this entry.

### Sources read this session

`jea-project-memory-file.md`, this file (header, Standing Facts, every entry from 2026-09-14 22:45 on, plus a
grep of all numbered open items), `git log` / `git show --stat` for `064514b` and `0b68fcf`,
`02_Planning/JEA Project - Gantt Chart.xlsx` (Project schedule sheet, via openpyxl), the rev1 Gantt export
manifest, and the full text of `01_Admin_Meetings/JEA_Senior_Design_Scope_of_Work (1).docx`. `[V]`

### Findings `[V]` unless marked

- **Gantt, as of today:** "Design UI/UX" 2026-09-14 to 09-27 at 15%. "Prelimiary Design Review (PDR)" on
  **2026-09-30**. "Draft BOM & Budget Estimation" 10-01 to 10-11, "Get BOM Approved" 10-12, "Order and Receive
  Components" 10-13 to 10-27. Everything after that has no dates.
- **The PDR date conflicts.** The Gantt says 2026-09-30; the SOW timeline table and Standing Facts say the week
  of Oct 5. Not resolved.
- **The Gantt "ASSIGNED TO" column still holds Vertex42 template names** ("VanArsdel, Ltd.", "Gokce Aslan",
  "Hayden Cook", ...), not the real team. `[I]`, high: these are the template's stock names.
- **No requirements document exists in the repo.** The SOW's Phase 1 deliverable is "Requirements doc drafted"
  (functional requirements, success criteria, constraints). Grep of this file, the capstone export, and the
  two reference `.md` files found no such document. The SOW's own demo success criterion is: a repeatable
  fault -> isolation -> restoration sequence run live, plus a clear one-line and short explanation.
- **REV2 has never been run on the physical board, per this log.** Items 21, 26, 27 and 33 are still open. The
  2026-09-15 entry shows Jordan compiling REV2 in the IDE, so an upload may have happened since without being
  logged. `[I]`
- **Item 41 is still open:** `firmware_rev2.js` line 25 still carries `1bb43e03...`, not `bd1ebd37...`.
- **Item 12 is partly done:** commit `064514b` removed `JEA Contacts.docx` and changed the REV2 pptx. The
  history-rewrite decision is still open.
- **Numbering collision:** the 2026-09-17 12:00 entry numbered its open items 12 and 13, but 12 and 13 were
  already used in the 2026-09-13 21:22 entry. This entry refers to the new ones as "PII item 12/13". The next
  free number is 47.

### Recommendation given

1. **Before Tue 2026-09-22:** load REV2 onto the physical board and run all 7 faults (items 21, 26, 27, 33).
   Supporting task on the code side: close item 41 so the REV2 bench is a working fallback demo. Bring the
   `[T]` subset of the 2026-09-17 question list.
2. **Right after the meeting:** log the answers here, then revise the flagged layout section and add the
   unmodeled components.
3. **Before PDR:** draft the missing requirements doc, fix the PDR date, then start the BOM (due 10-11).

### Open items

47. **PDR date conflict:** the Gantt says 2026-09-30, the SOW says the week of Oct 5. Confirm with Zach on the 22nd.
48. **No requirements doc** (SOW Phase 1 deliverable). Needed for the PDR.
49. **Gantt "ASSIGNED TO" column holds template placeholder names.**

### Not done

No code, bench, xlsx, DXF or Gantt changes. Item 41 not touched. No git commit.

---

## 2026-09-20 22:58 CDT - PDR is Tue 2026-09-22. Gantt chart dates are no longer used for planning

### What Jordan said `[V]`

- **The PDR is 2026-09-22.** That is the Tuesday JEA meeting where the LED display is being shown.
- **Standing rule:** do not use the Gantt chart dates when planning. Treat its task list as a loose guide only.

### What this supersedes

- **Standing Facts, Schedule:** "PDR with JEA: week of Oct 5" is replaced by **2026-09-22**.
- **2026-09-17 10:12 entry:** it called the 9/22 meeting an LED display review. It is the PDR.
- **2026-09-20 22:48 entry:**
  - Its Gantt findings (dates, the 09-30 PDR) no longer drive planning.
  - Item 47 (PDR date conflict) is **closed**.
  - Item 49 (template names in the Gantt) is **closed**: it does not matter under the new rule.
  - The "before PDR" steps in its recommendation now fall before Tuesday. Item 48 (no requirements doc) stays
    open, but it is not a Tuesday blocker unless Jordan says it is.

### Rule recorded outside this file too

Saved as auto-memory `jea-gantt-low-weight.md` so future sessions apply it without being told again.

### Not done

No code, bench, xlsx, DXF or Gantt changes. No git commit.

---

## 2026-09-20 23:13 CDT - Cardboard prototype built and working on REV2. Requirements doc drafted for Jordan's review

### What Jordan reported `[V]`

- **The cardboard prototype is built.** Four 24 x 24 x 1 in cardboard panels. The printed layout DXF is taped
  on top. The strip runs follow the recorded LED order. `FLISR_Trainer_REV2` is uploaded to an Arduino Uno and
  powered from a PSU. **It worked on the first try**, apart from the compile error fixed on 2026-09-15 (item 38).
- **The physical model is the source of truth.** The team built the physical model first, then recorded it in
  the tabulated workbook (`02_Planning/JEA Cardboard Prototype Tabulated REV1.xlsx`).

### What this supersedes

- **2026-09-20 22:48 recommendation 1** (load REV2 onto the board before Tuesday): done.
- **Item 21** (upload to a real Uno): **closed.** Wave frame rate was not reported separately. `[I]` It looked
  acceptable, since Jordan called the run a success.
- **Items 26, 27, 33** (status pixel positions, amber vs red, TIE pixel side): not confirmed one by one. They
  stay open until Jordan says otherwise.
- **The framing in the 2026-09-13 21:22 and 2026-09-14 20:11 entries** that the DXF and xlsx are design inputs
  to check against each other. **The xlsx records the built board, so its pixel counts are correct by
  definition.** Earlier flags that a run is "short of geometry" (item 14, 20:11 flags 2 and 3) describe the
  drawing, not a board error. Node coordinate typos such as N28 x (20:11 flag 1) were not addressed. `[I]`
- **Item 48** (no requirements doc): **drafted**, pending Jordan's review.

### Deliverable: requirements doc

- Claude Doc "JEA FLISR Trainer - Requirements":
  `https://claude.ai/code/artifact/94a3732b-bc7f-4f85-8734-6e5d9f16ac03`. Private to Jordan until shared.
- **Sections:**
  1. Purpose and scope
  2. Where the project stands
  3. Stakeholders
  4. Functional requirements FR-1 to FR-23 (FR-19 to FR-23 are candidates only)
  5. Physical requirements PR-1 to PR-11
  6. Electrical and controls requirements ER-1 to ER-10, plus an I/O estimate
  7. HMI requirements HR-1 to HR-8
  8. Constraints C-1 to C-9
  9. Acceptance tests AC-1 to AC-8
  10. Assumptions A1 to A14, each with a Confirmed / Wrong / Unsure dropdown
  11. Seven open questions and an out-of-scope list
- Every row carries `[V]` / `[S]` / `[I]` and its source.
- One comment is anchored on A2. It asks whether the final LED controller only displays the Axion's decisions
  or keeps its own FLISR model.
- **Sources read for it:** this file (Standing Facts, the 2026-09-07 layout entry, the 2026-09-07 import, the
  2026-09-10, 2026-09-13 and REV2 entries), `flisr-capstone-memory-export.md`, the SOW docx,
  `jea_oneline_component_reference.md` sections 5 to 9, the REV2 `.ino` header and blocks [1] to [3], and a
  keyword grep of the 8/27 transcript.
- **Gantt dates were not used,** per the standing rule.

### Assumptions in the doc most likely to be wrong `[I]`

- A1: the 48 x 48 in footprint is acceptable to JEA.
- A2: the Axion makes every FLISR decision, and the LEDs only display them.
- A3: devices are props with a status pixel.
- A9: aluminum extrusion frames.
- A11: about $4,000 left.
- A13: team roster and advisor names.
- A14: acceptance time targets.

### Open items

No new numbers. The doc's Section 11 restates the existing open items for the full-scale design:

- Axion placement (item 7)
- the LED link and segment bus (item 8)
- the connector (items 5 and 9)
- single vs per-panel chain (item 18)
- where the logic lives (item 19)
- scale (item 1)

### Not done

- No code, bench, xlsx, DXF or Gantt changes.
- Item 41 not touched.
- No git commit.
- The doc is not exported to the repo or Google Drive.

---

## 2026-09-21 00:02 CDT - Corrections from Jordan applied to the requirements doc. Section J added to the PDR question list

### What Jordan said `[V]`

- **The board has no 3D models yet.** It has only the printed DXF.
- **Final build, current plan (not set in stone):** each panel has a 1 x 1 in aluminum extrusion perimeter and a
  thin wood base. 3D-printed ground, buildings and components go on top. The final product will not be cardboard.
- **Dr. Pingen is not a faculty advisor.** Team verified: Jordan, Cody and Gage.
- **Audiences:** high school students, college students and JEA technicians. The JEA executive presentation is
  a trial run that also serves as practice for the symposium.
- **Temporary-fault simulation:** Jordan is unsure, so it goes to the PDR questions, not the requirements.
- **Milsoft specifics are still largely unknown.**
- Jordan set **A11 to Confirmed** in the doc: about $4,000 remains for non-SEL hardware.

### What this supersedes

- **2026-09-07 21:56 import:**
  - "Faculty advisors are Dr. Pingen and Dr. Schwindt": Pingen is **wrong**. Schwindt is unconfirmed. `[I]`
  - "1 in aluminum extrusion frames": now a perimeter frame plus a wood base plus 3D-printed ground.
- **Item 10:** the team half is closed. Only the advisor's name and spelling stay open.
- **Requirements doc FR-22** (temporary-fault candidate): **removed**, moved to the PDR questions.

### PDR question document `[V]`

- **Location:** `C:\Users\jprun\OneDrive - Union University\Tuesday Meeting Questions.docx`, last saved
  2026-09-17 10:27. It is the 2026-09-17 10:12 chat list, saved by Jordan.
- **Its structure:**
  - Sections A to G, then I. H is gone (its abstractNum, numbered 28 to 30, is orphaned). `[I]` Jordan deleted H.
  - Questions are numbered straight through, one list per section, each list starting where the last ended.
- **Added section J, "Temporary faults and Milsoft scope",** at the end with 7 questions, numbered 34 to 40:
  - temporary faults worth teaching?
  - does JEA reclose on underground cable?
  - how would the operator choose a temporary fault?
  - which Milsoft outputs are needed?
  - which Milsoft tool and license, and who sets it up?
  - what goes in the Milsoft model?
  - when are results needed, and do they drive allowed transfers?
- **How it was built:** python-docx, cloning the section I heading and its last question, reusing numId 9 so the
  numbering continues. Script: scratchpad `add_section_j.py` (temporary).
- **Checks run:** `[V]`
  - The first 38 paragraphs, the trailing empty paragraph and sectPr are byte-identical to the original.
  - Other re-saved parts are C14N-identical. `[Content_Types].xml` has the same entries, reordered.
  - The new text is all ASCII.
  - **Not opened in Word** and no PDF render: no LibreOffice on this machine.
- **Pre-edit copy:** in the vault, `vault.ps1 restore 079238e6`.

### Requirements doc changes

Doc: `https://claude.ai/code/artifact/94a3732b-bc7f-4f85-8734-6e5d9f16ac03`

- **Section 2:** "not in the prototype" now says the board carries only the printed layout.
- **Section 3:**
  - Trainees row removed. New Audiences table: high school, college, JEA technicians, JEA executive
    management (trial run and symposium practice), UU symposium.
  - Advisor row is Dr. Schwindt only, marked `[I]` for name and spelling. Team marked `[V]`.
- **PR-10:** rewritten to the extrusion perimeter, wood base and 3D-printed ground plan.
- **PR-8** (the SOW's vinyl backdrop) now flags that the 3D-printed ground may replace it. `[I]` Not raised with
  Jordan yet.
- **A9 and A13:** reworded to match. **HR-6:** "trainees" changed to "audience".
- **AC-8:** pass condition changed to "to be defined with JEA", pointing to the PDR questions.

### Not done

No code, bench, xlsx, DXF or Gantt changes. No git commit. The OneDrive docx is outside the repo.

---

## 2026-09-21 19:24 CDT - FastLED cannot run on the Axion. Brain/display split settled on hardware grounds. Closes open item 19

### The question Jordan raised `[V]`

He had assumed the REV2 sketch could be dropped more or less intact into the PLC, and hit two
blockers at once: the sketch assumes one continuous LED strand, and the panel plan was "each
section's positive terminal to a digital pin on the PLC." He asked whether FastLED (or any
open-source equivalent) can be loaded into the Axion, or whether the PLC can only do discrete
on/off.

### Answer: no, on two independent grounds. Either one alone is fatal

**1. No runtime to host it.** The SEL-2241 RTAC exposes only an IEC 61131-3 logic engine
(Structured Text, Ladder Diagram, CFC) loaded through AcSELERATOR RTAC. No user C/C++ runtime,
no loadable libraries, no directly addressable GPIO. `[V]` 2240_DS_20130827_01.pdf p.4.
FastLED 3.10.4's `src/platforms/` targets are `avr, arm, esp, teensy, apollo3, apple, arduino,
wasm, win, posix, stub`. No PLC / IEC 61131 target exists. `[V]` read from the local
`FastLED-3.10.4` extract. This is not a FastLED gap; no LED library can target that runtime.

**2. The output hardware is an electromechanical relay.** This is the harder wall and it holds
even if item 1 were solved.

| SEL-2244-3 spec | Value | Datasheet page |
|---|---|---|
| Output type | Form A / Form B control outputs (relay contacts) | p.13 |
| Rated voltage range | 19.2 - 275 Vdc | p.32 |
| Pickup/Dropout time | <= 8 ms typical | p.32 |
| Cyclic capacity | 2.5 cycles/second | p.32 |
| Mechanical durability | 10 M no-load operations | p.32 |
| Breaking capacity @ 24 Vdc | 0.75 A, L/R = 40 ms | p.32 |

All `[V]` from `07_Reference_Datasheets/2240_DS_20130827_01.pdf`.

WS2812B needs 800 kHz NRZ, timing 250 / 625 / 375 ns. `[V]` FastLED
`src/chipsets.h:473`, `fl::TIMING_WS2812_800KHZ`.

Arithmetic, all `[V]` by computation from the two rows above:

- 8 ms dropout caps the contact at about 62 Hz square wave. 800 kHz / 62.5 Hz = **12,800x too slow.**
- Against the *rated* 2.5 cycles/sec it is **320,000x too slow.**
- REV2 is 352 px x 24 bits = 8,448 bits/frame. 10 M operations / 8,448 = 1,183 frames. At the
  sketch's 50 fps cap that is **about 24 seconds of contact life.** The module would be destroyed
  during the first animation.

**The "fast" module does not rescue it.** SEL-2244-5 Fast High-Current DO: pickup <= 12 us at
250 Vdc / 65 us at 19.2 Vdc, but **dropout is still <= 8 ms typical**, cyclic capacity
4 cycles/second. `[V]` p.33. It is fast at closing, not at toggling.

### Two corrections to the stated panel wiring plan `[V]`

1. **Three conductors, not two.** WS2812B is +5 V, GND, DIN. The 5 V rail is permanently on; DIN
   carries the signal. Switching +5 V per section is actively wrong: WS2812B is a shift register,
   each pixel regenerates data for the next, so cutting section 3 also kills 4 through 6. This
   restates and confirms the warning already at PROJECT_MEMORY.md line 637.
2. **An Axion DO is a dry contact, not a sourcing pin.** It does not output voltage; it makes or
   breaks a loop the user supplies. Different mental model from an Arduino GPIO. At 5 V it is also
   below the 19.2 V rated floor, where there is insufficient wetting current to break contact
   oxide film. `[S]` for the oxide mechanism; `[V]` for the 19.2 V floor.

### Architecture recommended, and why it is not a compromise

**Split brain from display.** Axion reads fault buttons on DI, runs the entire FLISR sequence in
IEC 61131, publishes state. ESP32 holds zero FLISR logic and only maps state to pixels; FastLED
lives there. **This is requirements-doc A2 and it closes open item 19** ("where the FLISR logic
lives"), on hardware grounds rather than preference.

**Link options, ranked as given to Jordan:**

1. **Modbus TCP over Ethernet (recommended).** RTAC carries Modbus preinstalled `[V]` p.6, p.11;
   SEL-2241 has two terminal-side Ethernet ports `[V]` p.29. ESP32 runs a Modbus TCP server.
   Whole trainer state in ~20 holding registers, one Cat5 run, zero I/O modules consumed.
   **Open:** `[I]` the datasheet says "Modbus" without breaking out client vs server. Confirm with
   Michael that the purchased firmware has the Modbus **client** enabled. Added to the PDR list
   candidates.
2. **Modbus RTU over RS-485.** Four serial ports, EIA-232/485 software selectable, 300-115200 bps
   `[V]` p.30. MAX485 on the ESP32. Same data model, electrically more robust.
3. **Hardwired DO into optocouplers** (the existing segment-bus concept from the 2026-09-07
   import). Costed honestly for the first time: 6 zones x 2 bits + DER + 8 devices x 2 bits =
   **29 bits, so two SEL-2244-3 modules** (16 DO each), real money plus two backplane slots. Its
   one genuine advantage is visible copper from PLC to board, which reads well in a training room.

**Considered and rejected on merit:** SEL-2245-3 DC Analog Output, 8 ch, +/-20.48 mA / +/-10.24 V,
1 ms step response `[V]` p.34. Could drive dumb analog RGB strip through a MOSFET stage and give
real color fades, but whole-section-only with no per-pixel chase, 13 W burden, costs a slot.
Bad trade against a $10 ESP32.

### Consequences for the REV2 sketch `[V]` structure read this session

`FLISR_Trainer_REV2.ino`, 1,029 lines, 352 px, 31 segments, 8 devices, 7 faults, one
`FastLED.addLeds` call on pin 10 at line 990. `renderStrip()` (around line 750) walks the segment
table into one flat `leds[]` then calls `FastLED.show()` once.

- **Moves to the Axion:** `computeModel()`, button reading, step sequencing.
- **Stays on the ESP32:** the 31-row segment table, `colorForPixel()`, `colorForDevice()`, the
  animations, FastLED setup.
- **New:** a register-map decoder writing `zoneState[]` and `devState[]`.
- **Recommended:** keep `computeModel()` behind `#define STANDALONE_MODE 1`. The Axion has a
  November lead time and a demoable board is needed before then.

**The "one continuous strand" problem is separate from the PLC question and is easy.** FastLED
supports parallel outputs natively: one `addLeds` per panel, its own pin, its own slice of
`leds[]`, and a single `FastLED.show()` drives all of them. Because `renderStrip()` already walks
the table into a flat buffer, this is roughly a 40-line change, not a rewrite. `[I]` medium, not
attempted. Do it on ESP32, not the Uno: 352 px already consumes 1,011 of the Uno's 2,048 bytes
of SRAM.

### PDR framing offered

Jordan's framing was that it would be "crazy" to get animation from a $10 AliExpress part but not
from a $6,000 professional PLC. Reframe rather than apologize: the Axion buys 30 A make trip-rated
contacts, IEEE C37.90 surge withstand, -40 to +85 C, 1 ms time-stamped SOE, EtherCAT determinism,
DNP3 and IEC 61850 `[V]` pp.4-6. Nothing in a substation requires bit-banging 800 kHz into a light
strip, so no protection controller is designed to. Real utility mimic boards and video walls use
exactly this split: RTU holds state, a dedicated display driver renders it. `[S]`

### Open items touched

- **Item 19 (where the FLISR logic lives): closed.** Axion decides, ESP32 renders. Forced by
  hardware, not preference.
- **Item 8 (LED link and segment bus): narrowed.** Recommendation is now Modbus over Ethernet or
  RS-485 rather than a wide DO/opto bus, with the 29-bit / two-module cost of the DO route
  quantified as the reason.
- **Item 18 (single vs per-panel chain): unblocked.** Per-panel chains via parallel `addLeds`,
  independent of the PLC decision.
- **New PDR question:** does the purchased RTAC firmware have the Modbus client enabled, and which
  transport does Michael prefer (TCP or RTU)?

### Not done

No code changes. No `.ino` edits. No DXF, xlsx or Gantt changes. Requirements doc not updated with
the A2 / item 19 closure. No git commit. Gantt dates not used, per the standing rule.

---

## 2026-09-21 20:55 CDT - Working directory reorganized. Root cleared of loose files, FastLED vendored out of git

### What moved `[V]` all verified by `ls` and `git status` after the fact

The numbered folder structure from commit `8b63a71` was intact. What was loose was the material
that accumulated at root since then. Three groups:

| Was | Now | Why |
|---|---|---|
| `JEA FLISR Trainer.dc.html`, `support.js`, `_ds/` | `08_Presentations_Concepts/JEA_FLISR_Trainer_Overview/` | One bundle, three files. The HTML loads `./support.js` and `_ds/.../styles.css` relatively, so they only work together. |
| `FastLED-3.10.4/FastLED-3.10.4/` | `05_Firmware/libraries/FastLED-3.10.4/` | Double-nested zip extract, flattened by one level. 93 MB. |
| `FastLED-3.10.4.zip` | `05_Firmware/libraries/FastLED-3.10.4.zip` | 38 MB. Redundant with the extract; kept for now, candidate to archive. |

`PROJECT_MEMORY.md` and `flisr-capstone-memory-export.md` deliberately stay at root. Root is now
those two files, `.gitignore`, and the nine numbered folders.

### One real break found and fixed `[V]`

The overview page was written assuming it sat at repo root. Besides the two bundle-relative refs
it also carried three project-root-relative ones:

- `03_OneLine_Diagram/jea_power_delivery_oneline.svg`
- `04_Cardboard_Layout/Cardboard Layout REV3.png`
- `05_Firmware/FLISR_Trainer_Sim/FLISR_Trainer_REV2_Sim.html` (twice: an `<iframe src>` and an `<a href>`)

Moving the file two levels deep silently broke all three. Each was prefixed with `../../` and all
six references were then re-checked on disk. All resolve. `[V]`

The second such bundle, `09_Assets/Electrical symbol SVG icon set/`, was checked and is genuinely
self-contained: its own `support.js`, no `_ds` reference, all icon paths local. Untouched.

### Git hygiene

- **`.gitignore` added** (the repo had none): `05_Firmware/libraries/`, `__pycache__/`, `*.pyc`,
  `Thumbs.db`, `desktop.ini`, `~$*`.
- **`build_sim.cpython-314.pyc` untracked** via `git rm --cached`. It was a committed Python build
  artifact. The file is still on disk, only the tracking is gone.
- **FastLED is out of git by design.** 131 MB of third-party source across 4,177 files.
  It is reference material for the ESP32 render side, not project source, and it was never tracked.

### Deliberately left alone

- The four `.dxf~` and one `.dwg~` AutoCAD autosaves that are tracked in git. They live in
  `04_Cardboard_Layout/Backups/` and one in `08_Presentations_Concepts/`. Jordan works in AutoCAD
  daily and may be keeping them on purpose. `[I]` Flagged, not touched.
- `09_Assets/Electrical symbol SVG icon set.zip` alongside its own extracted folder. Same
  zip-plus-extract duplication as FastLED, much smaller, and it is tracked.
- No README index was added at root. The overview page already serves that purpose.

### Path reference correction

The 2026-09-21 19:24 entry cites the FastLED source as the local `FastLED-3.10.4` extract, and
`src/chipsets.h:473` for the WS2812B timing. Those readings stand; the path is now
`05_Firmware/libraries/FastLED-3.10.4/src/chipsets.h`. The earlier entry is not rewritten,
per the append-only convention.

### Not done

No code changes. No `.ino`, DXF, xlsx or Gantt edits. No git commit; all of the above is staged or
untracked in the working tree for Jordan to review. Gantt dates not used, per the standing rule.

---

## 2026-09-23 20:26 CDT - JEA feedback on REV2: new feature asks, ESP32 board fixed, PLC-to-ESP32 link options assessed, custom PCB open task

### What Jordan reported `[V]`

The source meeting was not named. `[I]` Most likely the 2026-09-22 PDR.

- **JEA called the REV2 animation very good.**
- **New asks from JEA:**
  1. Run each scenario **with and without DA** (distribution automation).
  2. **Junction boxes at every 90 degree turn** of the lines. Physical model only; Jordan expects no code change.
  3. **Fuses at the base of each radial branch:** two on Residential 1, one per branch.
  4. **A recloser on Residential 2.**
  5. **Substation faults.** Each substation is source -> high-side breaker -> step-down transformer ->
     low-side breaker. Simulate a transformer fault (real-world cause: animal contact). Adds **two fault
     zones**. `[I]` One transformer per substation.
  6. **Fault buttons move to the bottom row** by the legend / RTAC, so nobody reaches across the table.
     **Status LEDs go where the buttons are drawn now** and blink when that fault is injected.
  7. **A toggle switch: all faults temporary or all permanent.** Permanent = 3 reclose attempts, then lockout,
     then FLISR. The current code skips the reclose attempts and goes straight to FLISR.
  8. **IEEE 1547 emphasized for the DER.**
  9. **PV as a third source:** its recloser connects it to the rest of the grid and it momentarily backfeeds to
     reduce outages. See the 1547 notes below; this conflicts with default anti-islanding.
- **ESP32 replaces the Uno** as the display controller, for storage and clock speed. Exact board defined below.
- **The microcontroller stays in the finished product,** because of the PLC animation constraint.
- **Custom PCB** (ESP32, LEDs, buttons): to discuss later. Open item 50.
- Jordan proposed two architectures and asked for feasibility, an explanation of PLC digital I/O vs hobby-board
  pins, and a third option:
  - **A:** two independent parallel systems driven by the same buttons, no communication after the input. V/I
    readings would come from a hidden load PCB whose parts stand in for customer loads. Its layout need not
    match the city, only behave like it.
  - **B:** one system. Buttons go only to the PLC, the PLC is the sole brain, and it drives the display devices
    and the ESP32 for the LEDs.

### ESP32 definition (standing fact)

**Whenever Jordan says "ESP32" on this project, it means exactly this board:** AITRIP ESP32 ESP-WROOM-32
ESP32-DevKitC-32 development board, **30 pin, USB-C**, WiFi + Bluetooth, dual core, bought as a 3-pack. `[V]`
Jordan's description.

- Jordan typed the USB chip as "CP2012". The Silicon Labs USB-UART on these boards is the **CP2102**. `[I]`
  high; confirm from the chip marking.
- Facts relied on, `[S]` from Espressif's published specs, not read this session:
  - ESP32-WROOM-32: dual-core Xtensa LX6 up to 240 MHz, 520 KB SRAM, 4 MB flash. The Uno has 2 KB SRAM.
  - **3.3 V logic. GPIO is not 5 V tolerant.**
  - 30-pin DevKit: GPIO 6-11 are the flash bus and are not broken out. GPIO 34-39 are input only with no
    internal pull-ups. GPIO 0, 2, 5, 12, 15 are strapping pins; avoid them for buttons.
  - **No Ethernet jack on this board.** The chip has an internal EMAC but needs an external PHY.
- `[V]` Local FastLED 3.10.4 source,
  `05_Firmware/libraries/FastLED-3.10.4/src/platforms/esp/32/drivers/rmt/rmt_4/channel_driver_rmt4.h:127-136`:
  RMT TX channels are 8 on the classic ESP32 (IDF < 4.4 path; IDF >= 4.4 uses
  `SOC_RMT_TX_CANDIDATES_PER_GROUP`). Enough for 4 panel chains plus a marker chain.
- `[S]` WS2812B data high threshold is 0.7 x VDD = 3.5 V at 5 V, so a 3.3 V data line is out of spec. Plan a
  74AHCT125-class level shifter per data line.
- Also saved as auto-memory `jea-esp32-board.md`, so every session loads it.

### What this supersedes

- **Standing Facts, Hardware, "per-input selectable" (line 77).** The RTAC manual says the DI voltage level is
  fixed per module, and since firmware R118 the AC/DC debounce mode applies to a whole module (Instruction
  Manual pp.615-617). `[V]` No practical impact: every input here will be 24 Vdc.
- **2026-09-10 00:20, decision 1 ("fault-injection buttons stay scattered").** Replaced by JEA's ask: buttons in
  the bottom row, blinking status LEDs at the old button positions.
- **2026-09-10 00:20, decision 3 (overhead deferred)** is not reversed, but item 56 reopens it.
- **2026-09-21 00:02, "temporary-fault simulation goes to the PDR questions."** Answered: JEA wants a temporary /
  permanent toggle. PDR Section J questions 34 and 36 are answered. Question 35 (does JEA reclose on
  underground cable) is not.
- **2026-09-21 19:24, link ranking.** Modbus TCP was ranked first on the assumption that the ESP32 had Ethernet.
  This board has none. **New ranking: Modbus RTU over RS-485 first**, W5500 Ethernet module + Modbus TCP
  second, WiFi rejected.
- **2026-09-21 19:24, open question "does the RTAC have the Modbus client".** Software support is verified. The
  RTAC supports Modbus RTU and Modbus/TCP, as client or server, on any serial or Ethernet port, and a client
  polls IEDs (manual pp.429-430). `[V]` The manual's device-count table lists the SEL-2241 at 120 Modbus
  clients/servers combined. `[V]` Residual risk that JEA's unit needs something enabled: `[I]` low.
- **2026-09-21 19:24, "keep `computeModel()` behind `#define STANDALONE_MODE 1`".** Now a runtime fallback
  (option C below), not a compile-time switch.
- **REV0-REV2 headers, "Target: Arduino Uno".** The next firmware revision targets the ESP32. REV2 on the Uno is
  untouched and stays the working demo.

### Constraint re-check: animation cannot run on the Axion. Holds

Re-read from `07_Reference_Datasheets/2240_DS_20130827_01.pdf` this session, not copied from the 09-21 entry:
`[V]`

- SEL-2244-3: pickup/dropout 8 ms typical, cyclic capacity 2.5 cycles/second, 10 M no-load operations (p.32).
- SEL-2244-5: pickup 12 to 65 us, dropout still 8 ms typical (p.33).
- WS2812B needs 800 kHz. The 09-21 arithmetic stands.
- "RTAC runs IEC 61131-3 only" (p.4) was not re-read this session; it rests on the 09-21 reading.

### Axion I/O facts read this session `[V]`

| Item | Value | Source |
|---|---|---|
| SEL-2244-4 | 32 DI, two groups of 16 share a common return; ratings 24 Vdc, 48 Vdc, 110 or 125 Vac/Vdc | DS Table 6 p.13; manual p.615 |
| SEL-2244-2 | 24 DI, 18 share a return plus 6 independent | manual p.615 |
| DI thresholds, 24 V rating | ON 15-30 Vdc, OFF below 10 Vdc; burden 8 mA at 24 V | DS pp.32-33 |
| DI voltage level | fixed per module | manual p.615 |
| DI processing | EtherCAT updates and time-stamps every 1 ms; logic task interval user-set, 4 ms to 1 s; pickup/dropout debounce timers set in software | manual pp.616-617 |
| DI insulation | 300 Vac rated, 5 kV impulse | DS pp.32-33 |
| SEL-2245-4 AC metering | 4 CT + 4 PT inputs with isolated returns; 0.05-22 A, 5-400 V | manual p.646 (TOC); DS Table 12 |
| SEL-2241 serial | 4 ports, EIA-232/EIA-485 software selectable, 300-115,200 bps, DB-9 female | DS p.30 |
| RTAC Modbus | RTU and TCP, client or server, any serial or Ethernet port; FC 01-06, 0F, 10, 11 | manual pp.429-430 |

`[I]` JEA's "32 digital inputs" is one SEL-2244-4 (the only 32-input DI module), and "32 digital outputs" is two
SEL-2244-3 (16 each). Not confirmed against the order. Item 59.

### PLC I/O vs hobby-board pins, as explained to Jordan

- **ESP32 pin:** a transistor on the chip. The chip supplies 3.3 V, code sets the direction, it toggles at MHz,
  and it has no isolation.
- **Axion DI:** an optoisolated input. It supplies nothing. The user supplies a wetting voltage (24 Vdc here)
  through the field contact. The 8 mA burden and the 15 V ON threshold are deliberate, for noise immunity and
  contact wetting. `[S]` for the purpose.
- **Axion DO:** a relay contact. It outputs no voltage; it closes a loop the user powers. It is built to energize
  trip coils, not to signal.
- **Rules that follow:** never wire an Axion point straight to an ESP32 pin. DO -> ESP32 goes through an
  optocoupler on the 24 V side. ESP32 -> DI needs a transistor or opto switching 24 V, because 3.3 V never
  reaches the 15 V ON threshold.

### Architecture options assessed

**A. Two parallel systems, same buttons. Electrically feasible, functionally rejected.**

- Input sharing is easy. 22 mm industrial pushbuttons take stacked contact blocks, so each button gets two
  isolated contacts: 24 V to the Axion, 3.3 V to the ESP32. `[S]` One contact wired to both would put 24 V on
  an ESP32 pin.
- **Fatal:** HMI fault injection is a kickoff requirement (Standing Facts, Sponsor intent). A fault started from
  the HMI reaches only the Axion, so the board would not show it.
- The LEDs show the ESP32's model, not the RTAC's. When JEA edits RTAC logic, the board and the HMI disagree and
  nothing detects it.
- Every mode switch (temp/perm, DA on/off) must be read identically by both, with no resync after a reboot or a
  reset.

**V/I data is a separate question from A vs B.** In either option, if the HMI shows amps and volts, they must
come from somewhere.

- The SEL-2245-4 is one metering point (4 CT + 4 PT), not one per zone.
- A hidden load PCB could push real current into it, but at one location only, with real AC power and heat
  inside a trainer that high school students use.
- Recommended, `[I]` medium: compute V/I in RTAC logic from a table per switching state, ideally from a Milsoft
  load flow (ties to PDR Section J). Optionally add one small real metered circuit to show real CT/PT wiring.

**B. Axion is the sole brain; ESP32 renders. Feasible, verified.**

- Buttons and switches -> Axion DI -> FLISR in IEC 61131. The RTAC, as Modbus client, writes about 25 holding
  registers to the ESP32 (the Modbus server) every ~100 ms: zone states, device states, step, fault ID, mode
  flags, heartbeat counter. `[I]` for the register count and poll rate.
- Link: RS-485 Modbus RTU. ESP32 UART plus a 3.3 V transceiver (MAX3485 / SP3485 class), 3 GPIO, to an RTAC DB-9
  serial port. No IP addressing, so it avoids the known RTAC subnet gotcha.

**C (third suggestion, recommended). B plus a runtime standalone fallback, "one brain at a time".**

- A second contact block on each button, read by the ESP32 through an I2C expander (MCP23017 class). The ESP32
  keeps REV2's `computeModel()`.
- RTAC heartbeat present: the ESP32 renders only the RTAC's registers. Its own model may run silently as a
  cross-check and flag disagreement, which helps while writing the IEC 61131 logic.
- Heartbeat missing for more than ~2 s: the ESP32 runs its own model and shows a visible STANDALONE marker.
- Why: the board can demo before the Axion arrives (November), it still works while JEA has the Axion pulled for
  reprogramming, and REV2's model becomes the reference to test the RTAC logic against.
- Cost: 12-16 extra contact blocks, one expander chip, firmware.

**D (mentioned, not recommended).** Buttons wired only to the ESP32; the RTAC polls them over Modbus (FC 02,
discrete inputs). It saves the 24 V field wiring, but it loses the real DI wiring JEA technicians should see and
makes the ESP32 a single point of failure for input.

### New asks: interpretation and impact

`[S]` unless marked.

- **With / without DA.**
  - DA = communications plus automated switching, here the RTAC's FLISR. Protection is local and works without
    DA: the upstream recloser still trips, recloses and locks out.
  - Without DA, everything past the locked-out device stays dark until a crew patrols (following faulted-circuit
    indicators), opens the isolating device, and closes the tie by hand. `[I]` Typically an hour or more.
  - With DA, healthy sections return within 5 minutes, which IEEE 1366 counts as a momentary interruption, not a
    sustained one, so they drop out of SAIDI / SAIFI.
  - Suggested: a DA ON/OFF selector plus an outage clock or customer-minutes counter.
  - Real reasons DA is off: hot-line tags, comms loss, storms, abnormal switching configurations.
  - DER anti-islanding does not depend on DA.
- **Temporary / permanent toggle.**
  - Temporary: trip, reclose, fault gone, a momentary blink, no FLISR.
  - Permanent: trip plus 3 recloses (4 operations to lockout), then FLISR or the crew.
  - Transformer faults ignore the toggle: differential (87T) trips go to a hand-reset lockout (86) and never
    reclose.
  - Reclosing on underground cable is usually disabled, so the narration must not claim that cable faults
    self-clear. Item 56.
- **1547 and reclosing.** The DER must cease to energize within 2 s of an unintentional island (1547-2018,
  clause 8.1, `[S]`, standard not read). The B-side first reclose interval has to exceed that, or the recloser
  closes onto a live, out-of-phase island. This falls straight out of adding the toggle.
- **PV third-source backfeed.**
  - It conflicts with 1547 default anti-islanding.
  - The legitimate version is an intentional island (1547-2018 clause 8.2, `[S]`). It needs utility agreement, a
    grid-forming inverter and storage; grid-following PV alone cannot hold voltage. Reconnection needs
    synchronizing.
  - Proposed: show both. Default: PV trips within 2 s and waits the enter-service delay (default 300 s, `[S]`)
    after the grid returns. Intentional island: PV plus storage picks up a stranded healthy section.
  - Interpretation to confirm with JEA. Item 54.
- **Substation transformer faults.**
  - Per substation: HV breaker (new device), transformer (new fault zone), LV breaker (the existing SUB_x_BKR).
    `[I]` One feeder per substation, so the LV main and the feeder breaker collapse into one device.
  - Fault -> 87T trips both breakers, 86 lockout -> the whole feeder goes dark -> FLISR moves the whole feeder
    across the tie, so tie capacity becomes the lesson.
  - Code: `ZN_BUSA` is "never dark" and must change. Physical: Sub B has no visible bus pixels (run 22 is hidden
    into N29). Item 53.
- **Res-1 fuses x2, Res-2 recloser.**
  - Locations, `[I]` from the REV2 run table: N2 at the head of run 2 (Res-1 south street, Z1), N4 at the head of
    run 5 (Res-1 north street, Z2), N6 at the head of run 10 (Res-2 lateral, Z3).
  - They only show anything if there are faults downstream of them: +3 zones, devices and buttons if added.
    Item 52.
  - With the temp toggle, fuse saving vs fuse blowing becomes demonstrable.
- **Buttons in the bottom row, blinking status LEDs at the old spots.**
  - Recommended: WS2812 pixels on one extra hidden chain, driven by the ESP32 so the blink syncs with the fault
    wave.
  - Alternative: Axion DO -> 24 V pilot lights. A 1 Hz blink is within the 2.5 cycles/s rating, and the relay
    click is audible. Item 57.
- **Junction boxes at 90 degree turns.**
  - No code change, agreed.
  - Caveat: some devices sit on corners. DEV_A2 is on the N30 corner (`[V]`, `.ino` note). DEV_B1 at N26 looks
    like a corner from the run directions (`[I]`). A box there must not cover the status pixel.
  - The boxes also hide strip corner joints. Pull boxes at sharp turns are realistic underground because of cable
    bend radius.

### DI estimate

9 fault buttons (Z1-Z6, DER, XFMR A, XFMR B) + reset + 2 selectors (temp/perm, DA on/off) = **12**. With lateral
faults, **15**. Fits one SEL-2244-4 with 17 or more spare. `[I]` for the button set.

### Verification actually performed

- **Read:** `jea-project-memory-file.md`, `jea-gantt-low-weight.md`, and this file (header, Standing Facts, the
  2026-09-10 entry, the REV2 entry, and every entry from 2026-09-20 22:48 on).
- **Also read:** `FLISR_Trainer_REV2.ino` lines 1-520, and a keyword grep of
  `jea_oneline_component_reference.md` (recloser, fuse, junction box).
- **PDF text:** extracted with `pdftotext -layout` from `2240_DS_20130827_01.pdf` and `Axion Instruction
  Manual.pdf` into the scratchpad, then read at the cited lines. Page numbers are printed page numbers.
- **FastLED:** RMT channel count read from the local source.
- **No code changed,** so no tests or compiles were run.

### Open items

50. **Custom PCB: ESP32, LED data outputs, button inputs.** To discuss later; Jordan will raise it. Likely
    contents:
    - ESP32 socket
    - 74AHCT125-class level shifting per strip data line
    - RS-485 transceiver
    - button and switch input conditioning
    - MCP23017 if option C
    - 5 V strip power entry and fusing

    Do not treat it as designed until Jordan starts it.
51. **Link transport.** RS-485 Modbus RTU recommended, W5500 + TCP second. Confirm Michael's preference.
52. **Lateral faults.** Add fault buttons behind the two Res-1 fuses and the Res-2 recloser (+3 zones, devices
    and buttons), or keep them display only?
53. **Substation pixels.** XFMR fault markers are needed in both substations, and Sub B needs visible bus
    pixels. The `ZN_BUSA` "never dark" rule must change.
54. **PV backfeed meaning.** An intentional island with storage (1547 clause 8.2), or something else? Confirm
    with JEA.
55. **JEA reclose settings, from Michael:** shots to lockout, intervals, fast/slow curves, fuse saving or fuse
    blowing.
56. **Temporary faults on an all-underground model.** Reclosing on cable is usually disabled. The narration must
    not say cable faults self-clear. Revisit the overhead mainline deferral (2026-09-10 decision 3).
57. **Fault location markers:** ESP32 pixels (recommended) or Axion DO pilot lights.
58. **V/I source:** a synthetic RTAC table from Milsoft (recommended) or a load PCB into the SEL-2245-4.
59. **Confirm the ordered I/O modules.** Inferred: one SEL-2244-4 (32 DI) and two SEL-2244-3 (16 DO each).
60. **The requirements doc is not updated** with any of this, nor with the 09-21 A2 / item 19 closure.
61. **Architecture choice.** Option C recommended; Jordan and the team decide.

### Not done

No code, `.ino`, bench, DXF, xlsx or requirements doc changes. No git commit. Gantt not used, per the standing
rule.

---

## 2026-09-23 21:19 CDT - 20:26 chat reply saved as a reference file

At Jordan's request, the chat reply from the 20:26 session was saved verbatim, with a short header, to
`02_Planning/2026-09-23 JEA Feedback and PLC-ESP32 Architecture.md`. It is the plain-language version of that
entry: I/O comparison table, options A / B / C, and the new JEA asks. The 20:26 entry stays the source of
record for citations, confidence markers and open items 50-61. No other changes. No git commit.

---

## 2026-09-24 10:32 CDT - "What is the next task?" after the PDR feedback

### What was asked

"What is the next task in terms of this project?" Answered in chat only. No files changed other than this entry.

### Sources read this session

`jea-project-memory-file.md`, `jea-gantt-low-weight.md`, `jea-esp32-board.md`, this file (header, Standing
Facts, every entry from 2026-09-20 22:48 on), the `05_Firmware` folder listing, and the task-name column of
`02_Planning/JEA Project - Gantt Chart.xlsx` (dates ignored, per the standing rule). `[V]`

### Recommendation given `[I]`, medium-high

1. **Next task: freeze the REV3 scope with Cody and Gage.** Decide item 61 (architecture, C recommended), item 52
   (lateral faults active or display only), item 53 (substation XFMR / Sub B bus pixels) and item 57 (fault
   markers). Reason: the BOM, the REV3 ESP32 firmware and the next layout DXF revision all depend on these.
   Option C adds contact blocks and an MCP23017 to the BOM; option B moves the FLISR model off the ESP32.
2. **Same day: send JEA the questions only they can answer**, folded into the weekly update email: items 51
   (link transport, Michael), 54 (PV backfeed meaning), 55 (reclose settings), 59 (ordered I/O modules), and
   PDR question 35 (reclosing on underground cable). Longest turnaround, so send first.
3. **Then two parallel tracks:** REV3 firmware and the BOM draft (the Gantt task list puts the BOM after the PDR;
   used as a loose guide only).
4. **Buildable today without any decision:** the straight REV2 -> ESP32 port. Per-panel parallel `addLeds`
   chains (item 18) and the ESP32 render path are needed in options B and C alike. Reclose / DA logic in
   `computeModel()` only pays off under option C, so hold it until item 61 is decided.

### Supersedes

The 2026-09-20 22:48 recommendation list. Its steps 1 and 2 are done (REV2 on the board, PDR held); step 3's
requirements doc exists but is stale (item 60).

### Open items

No new numbers. Still open and mentioned: 26, 27, 33, 41, 50-61.

### Not done

No code, `.ino`, DXF, xlsx, requirements doc or Gantt changes. No git commit. `PROJECT_MEMORY.md` and
`02_Planning/2026-09-23 JEA Feedback and PLC-ESP32 Architecture.md` were already uncommitted at session start.

---

## 2026-09-24 11:12 CDT - Jordan's decisions, Axion order decoded (DI module is 125 V), DER backfeed researched, PLC and V/I measurement explained

### What Jordan said `[V]`

- **Default to direct wired connections between components, not wireless.** Saved as auto-memory
  `jea-wired-connections-default.md`. Applied to item 51 below.
- **Ground the large majority of decisions in outside sources, and state every assumption.** Saved as auto-memory
  `ground-decisions-in-sources.md`.
- **Architecture option A (two parallel systems) is out.** Item 61 narrows to B or C.
- **Item 54, as JEA described it:** if a fault happens near the DER, the PV momentarily backfeeds power to the grid
  to restore power to customers who lost it. Jordan is not sure this is right and asked for research.
- **Parts list:** read `07_Reference_Datasheets/SEL-2240 Axion Node _ Summary _ Schweitzer Engineering Laboratories.pdf`.
- **Final version requirements:**
  - All fault injection buttons consolidated at the bottom of the board.
  - An LED inside each house, shining out through the windows, assuming the house model is open like that. Same
    logic as the strip LEDs.
  - Explore an LED on top of each pad-mount transformer and junction box.
  - **Hard constraint: a status LED at every fault point,** so the fault location is intuitive.
- **Faculty requirement (Jordan's professor): the PLC must read real values from actual points on the board.**
- **HMI:** the PLC has no built-in HMI. A laptop connects over Ethernet and its screen is the HMI.
- Jordan knows the ESP32 well and the PLC poorly. He asked how PLC inputs work, how the PLC works, and how current
  and voltage get read.

### Axion order decoded `[V]`

Source: the summary PDF, a selinc.com configurator printout dated 2026-09-02. Sales item **2240#CGVJ**, list price
**$2,965.25**. The PDF's text layer is font-garbled, so the three pages were rendered to PNG and read visually.

| Slot | Module | Option chosen |
|---|---|---|
| Backplane | SEL-2242 | Standard overlay, 19-inch panel mount (slots A-J) |
| A | Empty | "SEL-2241 RTAC Ordered Separately" |
| B | SEL-2243 Power Coupler | 125/250 Vdc or 120/240 Vac supply, 10/100BASE-T |
| C | SEL-2245-4 | 4CT/4PT AC Metering Module |
| D | SEL-2244-4 | 32 Digital Input, **125 Vdc/Vac** |
| E | SEL-2244-3 | 16 Digital Output, Form A |
| F | SEL-2244-3 | 16 Digital Output, Form A |
| G, H, I, J | None | 4 empty slots |

Consequences:

- **Item 59 closed.** The 2026-09-23 inference (one SEL-2244-4, two SEL-2244-3) is confirmed.
- **The DI module is rated 125 V, not 24 V.** SEL-2244-4, 125 V rating, `[V]` DS p.33:
  - DC signals: ON 100-135.5 Vdc, OFF below 75 Vdc.
  - AC signals: ON 85-150 Vac, OFF below 53 Vac.
  - Burden 2-6 mA. Max 150 Vpeak between inputs that share a common.
  - The 125 V option can be set per module to respond to AC or DC. With AC, neutral goes to the common terminal.
    Contact inputs must sit on the load side of an overcurrent device no larger than 8 A. Axion manual p.106.
  - Two banks of 16 inputs share common returns, and the voltage level is fixed per module. RTAC manual p.615.
  - Result: a button must switch 120 Vac or 125 Vdc into the DI, never 24 V. Item 62.
- **Web HMI status of the RTAC is unknown.** The summary's "Web Human Machine Interface: No" line sits under Slot A,
  which is empty because the RTAC was ordered separately, so it says nothing about the RTAC. `[I]` The RTAC's own
  order summary is not in the repo. Standing Facts say Zach bought an HMI license. Item 63.
- `07_Reference_Datasheets/135187.pdf` is the SEL-2240 Axion **Bay Controller** datasheet, the version with a 7-inch
  touchscreen. JEA's order is an Axion node with no touchscreen. `[V]`

### Item 51 closed: RS-485 Modbus RTU, point to point

Applied the wired-by-default preference. The link is a cable from an SEL-2241 serial port (EIA-232/485 software
selectable, DS p.30 per the 2026-09-23 entry) to an RS-485 transceiver on an ESP32 UART. Wired Ethernet through a
W5500 ranks second: it is wired, but it shares a network and is not direct. WiFi and Bluetooth stay off. Michael can
still be asked whether he prefers TCP, but RTU is now the default.

### Item 54 research: DER "backfeed" to restore customers

Sources read this session `[V]`:

- NREL and Sandia, "A Primer on the Unintentional Islanding Protection Requirement in IEEE Std 1547-2018"
  (Narang, Gonzalez, Ingram; OSTI 1862659; docs.nlr.gov/docs/fy22osti/77782.pdf). PDF pp.9-10, 14, 21-25.
- NREL, "Research Roadmap on Grid-Forming Inverters" (Lin et al.; docs.nlr.gov/docs/fy21osti/73476.pdf).
  PDF pp.13, 22.
- NREL, "Borrego Springs Community Microgrid" (Pratt; docs.nlr.gov/docs/fy19osti/74477.pdf). Slides 6-7, 15, 18.
- PNNL for NRECA, "IEEE 1547-2018" (Vartanian, 2018-10-31; cooperative.com). Slides 11-13, 26-27.
- IEEE PES ISGT 2024 tutorial proposal, "Implementing FLISR on Distribution Circuits with High DER Penetration"
  (Uluski, ESTA International; ieee-pes.org). PDF pp.1, 3.
- IEEE 1547-2018 itself was **not** read. Clause content comes from the NREL and PNNL documents that quote it.

Findings:

1. **By default the PV does the opposite of backfeeding.** If an upstream device opens and leaves the DER feeding an
   isolated section, clause 8.1.1 requires it to cease to energize and trip within 2 s. The time can be stretched to
   2-5 s by agreement (8.1.2). It then stays off for a return-to-service delay, 5 min by default. (Primer PDF p.14.)
2. **Why:** the island is a shock hazard for workers and the public who assume the lines are dead (primer 4.1).
   It can also damage motors and other equipment if a recloser closes it back in out of phase (primer 4.2).
3. **PV alone cannot hold customers up.** Typical PV inverters are grid-following. They act as current sources, need
   a phase-locked loop, and "cannot function without an externally regulated voltage." An island of only
   grid-following inverters "will not be capable of functioning autonomously." (Roadmap PDF pp.13, 22.)
4. **What is real: an intentional island, i.e. a microgrid (1547-2018 clause 8.2).** It is planned, has a defined
   boundary, and has voltage and frequency regulation controls. Transitions into it are scheduled (manual or
   dispatch) or unscheduled (automatic on abnormal grid conditions). (Vartanian slides 12-13.) It needs a
   grid-forming source (a battery inverter in grid-forming mode, or a generator), a boundary switch and a controller.
5. **Real utility case: SDG&E Borrego Springs.**
   - Solar, batteries and diesel carried 2,128 customers for about 5.5 h in a 2012 planned outage, and up to 1,056
     customers for more than 20 h during the September 2013 storms (slides 6-7).
   - In one island the diesel was the voltage and frequency master and the PV was not dispatched (slide 15).
   - NREL tested microgrid control functions running on an SEL RTAC (slide 18).
6. **FLISR with DER:** DER can free capacity for load transfers and can support islanded microgrids on isolated
   sections with no backup source. It also causes load masking and fault-location errors from its fault current.
   (IEEE PES tutorial pp.1, 3.)
7. **Reclosing fixes** for out-of-phase closing onto a live island: a reclose interval longer than 2 s, hot-line
   reclose blocking, or direct transfer trip (primer PDF p.25).

Interpretation `[I]`, medium: JEA's description is partly right.

- DER can restore stranded customers, but not for a moment: it carries them until the grid returns, then
  resynchronizes.
- It cannot be PV alone. It needs a grid-forming source such as a battery.
- It can only happen after the fault is isolated.
- By default the PV does the opposite and trips within 2 s.
- `[I]` low: the "momentary" part may be a mix-up with the DER's brief fault-current contribution during the fault,
  which is a nuisance, not a restoration.

Trainer proposal `[I]`, two DER modes:

- **Default (1547 anti-islanding):** fault -> DER trips within 2 s -> it waits the return-to-service delay
  (time-compressed on the trainer) after normal voltage returns.
- **Microgrid (only if JEA confirms):** after FLISR isolates the fault, a PV plus battery DER energizes an isolated
  healthy section that has no tie, with its recloser as the boundary switch. When the grid returns, it runs a sync
  check, then closes.

Item 54 stays open until JEA says which one they meant. Item 66.

### How current and voltage get into the PLC

- **AC path, what the order supports `[V]`:**
  - In a real substation, instrument transformers are the in-between parts. A CT steps current down to 1 A or 5 A
    nominal, and a PT/VT steps voltage down. Their outputs wire straight into the SEL-2245-4; no transducer is needed.
  - SEL-2245-4 ranges: 0.05-22 A (DS p.34) and 5-400 V line-to-neutral (DS p.35).
  - Accuracy is specified above 0.6 A and above 20 V (DS pp.34-35).
  - CT and PT ratio settings scale the readings to primary values (RTAC manual p.646).
  - 4 CT inputs and 4 PT inputs, each with an isolated return (RTAC manual p.646).
  - Values appear as tags such as `IA_FUND` and `VA_FUND` (RTAC manual p.865).
- **DC or anything else:**
  - A transducer outputs 4-20 mA or 0-10 V into an SEL-2245-2 DC analog input module: 16 inputs, +/-20 mA,
    +/-2 mA or +/-10 V (DS p.13 Table 8, p.33). `[V]`
  - **Not ordered.** Slots G-J are free for it.
- **Digital meter:** a panel meter with RS-485 Modbus, polled by the RTAC. It is wired. `[S]`
- **Proposal for the faculty requirement `[I]`, medium:**
  - A hidden low-voltage AC mini-grid with real resistive loads per feeder.
  - Axion DO contacts switch its branches the way the real breakers and reclosers would. SEL-2244-3 AC rating
    (DS p.32): 240 Vac rated operational voltage, 3 A continuous at 120 Vac. No minimum AC voltage is listed; the
    19.2 V floor is a DC rating.
  - The SEL-2245-4 measures up to 4 points: e.g. Feeder A head, Feeder B head, DER branch, industrial customer.
  - The kickoff's variable industrial load becomes a real current the PLC reads, and a FLISR transfer shows up as a
    real rise in Feeder B head current.
  - Assumptions:
    - A1: each current channel can serve as an independent single-phase point. Per-phase tags exist; use on
      unrelated circuits is unconfirmed.
    - A2: 24 Vac is acceptable for a high-school audience, and the SEL-2244-3 contacts switch it reliably at
      1-2 A resistive (no AC minimum is published, so confirm with Michael).
    - A3: about 0.6-2 A per measured branch, so 15-50 W of heat each.
  - Item 64.

### LEDs

- **House LEDs:** one WS2812-class pixel per house on a hidden ESP32 chain, mapped to the house's zone, same colors
  as the strip.
  - `[S]` Thin 3D-printed walls leak light, so a house needs a light-tight interior or thicker walls.
  - `[I]` Pre-wired pixel strings suit houses spaced apart.
- **Pad-mount transformer and junction box LEDs: there is a real device for this.** SEL's LINAM UGFI underground
  fault indicator `[V]` (selinc.com/products/LINAM-UGFI):
  - It is deployed on pad-mounted transformers, switchgear, sectionalizing cabinets and junction boxes.
  - It finds faults in the cable between enclosures.
  - It offers an LED display outside the enclosure.

  So an enclosure LED that flashes when fault current passed through it is realistic. It also teaches the no-DA
  scenario: the crew finds the fault between the last flashing indicator and the first dark one. Recommended `[I]`.
  Item 65.
- **Status LED at every fault point is a hard constraint.** Item 57's implementation choice (ESP32 pixel or Axion DO
  pilot light) stays open. ESP32 pixel is still the recommendation.

### PLC explained to Jordan (summary)

- **Hardware:**
  - The Axion is a backplane plus separate cards: RTAC CPU (SEL-2241: 533 MHz, 1024 MB ECC RAM, DS p.29),
    power coupler, and I/O cards.
  - The cards talk to the CPU over the EtherCAT backplane. All I/O updates deterministically, with 1 ms time
    stamps (DS pp.2, 5).
- **Program model:**
  - Logic runs in fixed task cycles: inputs are read, all IEC 61131 logic runs, outputs are written.
  - The cycle time is set by the user and locked to system time. Set the main cycle to at least 140% of the measured
    task time (RTAC manual p.160).
  - There is no `delay()`. Timers are function blocks. `[S]`
- **I/O:** DI and DO as in the 2026-09-23 entry, with the 125 V correction above.
- **HMI:**
  - The RTAC serves a web HMI. Screens are built in ACSELERATOR Diagram Builder (SEL-5035), loaded into the RTAC,
    and viewed from any browser on the Ethernet network, several people at once.
  - It is an ordered option (RTAC manual p.566).
  - The Live Data page can view and force tags for testing (p.566).

### What this supersedes

- **2026-09-23, "No practical impact: every input here will be 24 Vdc".** Wrong. The ordered DI module is 125 V.
  Also superseded: the 24 V threshold row as the one that applies, and "24 V to the Axion" in option A's
  stacked-contact note.
- **2026-09-23 option A:** rejected by Jordan. It was already "functionally rejected" there.
- **2026-09-23 item 51 ranking:** closed as RS-485 Modbus RTU.
- **2026-09-23 item 58** (synthetic V/I table recommended): superseded by item 64. The faculty requirement asks for
  real measured values. A synthetic table may still fill zones that have no metering point.
- **2026-09-23 item 59:** closed.
- **2026-09-24 10:32, the four team decisions:** item 61 is now B vs C only, and item 57 carries the hard constraint.

### Verification actually performed

- The summary PDF was rendered to PNG with PyMuPDF, and all 3 pages were read.
- `pdftotext` was run on `2240_DS_20130827_01.pdf`, `Axion Instruction Manual.pdf` and `135187.pdf`. The cited
  sections were read, and PDF page numbers were computed from form feeds.
- The five web sources were downloaded and their text extracted, then read at the cited pages. `nrel.gov` did not
  resolve, so the `docs.nlr.gov` copies were used.
- No code changed, so nothing was compiled or tested.

### Open items

Closed: 51, 59. Superseded: 58, by 64. Narrowed: 61 is now B or C. Updated: 57 carries the hard constraint.

62. **DI wetting voltage.** The ordered SEL-2244-4 is 125 V. Options:
    - (a) ask JEA whether the DI voltage option can still change to 24 Vdc;
    - (b) wet the inputs with fused 120 Vac, using buttons rated for 120 Vac;
    - (c) 24 V buttons driving interposing relays near the Axion, which switch 120 Vac into the DI;
    - (d) a 125 Vdc supply.

    Ask Zach and Michael before choosing. It also sets the isolation for any ESP32 contact into a DI.
63. **Does the SEL-2241 RTAC order include the Web HMI option?** The RTAC order summary is not in the repo.
64. **Real V/I measurement (faculty requirement).**
    - Evaluate the AC mini-grid plus SEL-2245-4 proposal.
    - Confirm with Michael that the channels can be used as independent single-phase points.
    - Choose the 4 measured points.
    - Decide whether an SEL-2245-2 is wanted in a free slot.
65. **House LEDs and enclosure (fault-indicator) LEDs.** Count houses, pad-mounts and junction boxes from the layout.
    Then set the pixel budget and chain routing.
66. **Item 54 questions for JEA:**
    - Was the PV backfeed meant as a microgrid with storage?
    - Does JEA run any intentional island today?
    - Which section should the DER pick up, and should the trainer show both modes?

### Not done

- No code, `.ino`, DXF, xlsx or requirements doc changes.
- No git commit.
- The IEEE 1547-2018 text itself was not read.
- The RTAC order summary was not found.

---

## 2026-09-24 11:45 CDT - Web sources saved locally as text, converter script, homework reading list

### What Jordan asked `[V]`

- Save the web pages used as sources locally.
- Write a quick Python script that converts them to text files, for lower token usage.
- Read those text files in the future for references.
- Write a homework reading file for Jordan. It should cover both the gathered local text files and online resources
  to deepen his understanding.

### Deliverables

- **`07_Reference_Datasheets/web_sources/`**
  - `sources.json`: manifest of the 6 sources behind the 11:12 entry (item 54 research, item 65 fault indicator).
  - `web_to_text.py`:
    - Downloads missing sources into `raw/`.
    - Converts PDFs with PyMuPDF (`=== page N ===` markers at page breaks) and HTML with BeautifulSoup.
    - Normalizes typographic characters to ASCII.
    - Writes `text/<id>.txt` with a source header, and `text/INDEX.txt`.
    - Options: `--refresh` re-downloads, `--only <id>` limits the run.
  - `raw/`: 5 PDFs plus 1 HTML page, 7.4 MB.
  - `text/`: about 290 KB total. The primer went from 1254 KB to 87 KB, and the Borrego slides from 2093 KB to 9 KB.
- **`07_Reference_Datasheets/HOMEWORK_READING.md`:** 7 parts (0-6).
  - Part 0 is the 9/23 architecture file.
  - Parts 1-6 cover PLC basics, V/I measurement, the RS-485 Modbus link, protection and FLISR, DER and 1547, and
    fault indicators.
  - Each part gives page-level pointers into local files and verified online links, plus "check yourself" questions.
- **Auto-memory `jea-web-sources-local.md`:** read the local `.txt` before re-fetching, and add every new web source
  to `sources.json`.

### Decisions and why

- **Script dependencies:** stdlib `urllib` for downloads, plus PyMuPDF 1.28.2, bs4 4.14.3 and lxml 6.0.2, all
  already installed `[V]`. `requests` was avoided because it prints a dependency-version warning on this machine
  `[V]`.
- **Downloads never overwrite a saved copy with junk.** The script checks for the `%PDF` magic bytes on PDFs and for
  bot-check markers (`_Incapsula_Resource` and others) on HTML.
- **selinc.com:** its bot protection answered curl with 307 and a block page, but urllib's download succeeded. The
  page's tab content, including the "junction boxes" sentence cited at 11:12, is only in a Next.js
  `__NEXT_DATA__` JSON block. The script therefore also extracts JSON "text" fields that are missing from the visible
  text, and appends them under an "embedded page data" marker.
- **Script source is pure ASCII:** the character map is keyed by code point (`0x2018: "'"`). The first draft used
  `\u` escapes, and the file tool wrote them out as literal UTF-8 characters. That was caught by a byte check and
  rewritten, and the output was re-verified byte-identical (md5) afterwards.

### Online resources on the list

Each one was checked on 2026-09-24 for an HTTP 200 and matching content. For the PDFs, the first page and table of
contents were read.

- Kuphaldt, *Lessons In Industrial Instrumentation* v2.33, ibiblio PDF, CC BY 4.0. Section page numbers came from
  the PDF's table of contents.
- AutomationDirect: "Sinking and Sourcing Concepts" and the PLC Handbook.
- PLC Academy Structured Text tutorial.
- Three SEL video portal pages (RTAC programs and function blocks; Quick Configuration; RTAC HMI with Diagram
  Builder). Confirmed through WebFetch.
- IPS "Current Transformers: The Basics."
- TI SLLA272 RS-485 Design Guide.
- Modbus over Serial Line V1.02 (modbus.org).
- emelianov/modbus-esp8266 on GitHub. Not tested on our board.
- G&W Electric recloser blog.
- DOE SGIG "Distribution Automation" report, 2016. Section 2.1 is PDF pp.21-30.
- TD World reliability metrics.
- **Left out:** control.com's HTML textbook returned 403 to automated checks, so the ibiblio PDF is used instead.
  Eaton's recloser page timed out. NOJA returned 429.

### Verification actually performed

- Ran `web_to_text.py`: 6 of 6 `[OK]`, exit code 0. A rerun used the saved copies and produced identical output.
- Failure paths tested:
  - An unknown `--only` id exits with code 1.
  - An HTTP 404 returns "no copy", and no file is created.
  - HTML returned in place of a PDF is rejected, and the saved copy is left unchanged.
  - The bot-check marker is detected.
- Spot check: primer text page 14 contains the 2 s clearing time and the 5 minute return-to-service delay, which
  matches the 11:12 citation. The SEL text contains the "junction boxes" sentence.
- Non-ASCII check: the script, the manifest and `HOMEWORK_READING.md` are pure ASCII. The text files keep 7
  accented letters in author names.
- Every local link in `HOMEWORK_READING.md` resolves.

### Open items

No new numbers.

### Not done

- The local SEL PDFs (datasheet, instruction manual) were not converted to text. The script handles web sources
  only. Doing this would cut the cost of re-reading the 1282-page manual; offered to Jordan.
- `raw/` is not in `.gitignore`: 7.4 MB of re-downloadable third-party files. Not changed; flagged.
- No git commit.

---

## 2026-09-24 11:54 CDT - SEL PDFs in the repo converted to text

Supersedes the 11:45 "Not done" item about the local SEL PDFs.

### What Jordan asked `[V]`

- "Convert the SEL PDFs already in the repo (datasheet and the 1,282-page Axion manual)".

### Sources read

- The five SEL PDFs in `07_Reference_Datasheets/`, inspected with PyMuPDF 1.28.2 for page count, bookmarks,
  metadata and text.
- `web_to_text.py` and `sources.json` from the 11:45 entry.

### Deliverables

- **New text files in `07_Reference_Datasheets/web_sources/text/`:**
  - `sel_2240_datasheet.txt`: from `2240_DS_20130827_01.pdf` (Date Code 20260320). 40 pages, 5.2 MB -> 84 KB.
  - `sel_2240_bay_controller_datasheet.txt`: from `135187.pdf` (Date Code 20250423). 28 pages, 4.1 MB -> 57 KB.
  - `sel_2240_instruction_manual.txt`: from `Axion Instruction Manual.pdf` (Date Code 20260320). 1282 pages,
    88.6 MB -> 2.7 MB. Starts with a 1763-line outline from the PDF bookmarks.
- **`sources.json`:** 3 new entries. They use a new `"local"` field in place of `"raw"`.
- **`web_to_text.py` changes:**
  - `"local"` entries are converted where they sit. They are never downloaded or copied into `raw/`, which avoids a
    second 90 MB copy.
  - Any PDF with bookmarks gets an `=== outline ===` block before page 1: one line per bookmark, a ". " prefix per nesting
    level, ending in `.. p.N` (PDF page). `clean()` strips leading spaces, so indentation could not be used.
  - Arrowhead and spot bullets (0x27A2-0x27A4, 0x2981) now map to `-`. The manual had about 3100 of them.
  - `INDEX.txt` shows the local path when an entry has no URL.
- **Side effect:** the outline block also added 15-27 lines to three existing texts (islanding primer, GFM roadmap,
  Borrego slides). Every other line in them is unchanged.

### Decisions and why

- **PyMuPDF kept over `pdftotext -layout`.** Compared on DS p.29 `[V]`:
  - PyMuPDF keeps each page column in reading order, but splits table rows into alternating label and value lines.
  - `pdftotext -layout` keeps table rows aligned, but interleaves the two page columns line by line.
  - PyMuPDF was chosen to match the existing script and its page markers. Tradeoff: a dense spec table may need a
    look at the PDF page to confirm which value belongs to which row.
- **Manual page numbers:** the printed page number equals the PDF page number. p.106 prints "106" `[V]`.
- **`Axion Panel Drawings.pdf` was not converted.** It is a re-saved copy of the instruction manual, not panel
  drawings `[V]`:
  - Text is identical on all 1282 pages.
  - Same 1763 bookmarks, same title and creation date.
  - Only the modification date (2026-09-02 15:39) and the md5 differ.
- **The order summary PDF was not converted.** Its font encoding is broken, and both PyMuPDF and `pdftotext` return
  garbage `[V]`. It needs OCR, and tesseract is not installed. The 11:12 entry read it by rendering the pages to PNG.
- **URL left blank for the 3 local entries.** Their download URLs are not known and were not guessed.

### Verification actually performed

- Ran `web_to_text.py`: 9 of 9 `[OK]`, exit code 0. A second run was byte-identical (md5).
- `git diff --numstat` on the existing texts: primer +27/-0, roadmap +15/-0, Borrego +27/-0. The other three are
  unchanged.
- Spot checks against pages cited in earlier entries, all found on the stated page:
  - DS p.29 "533 MHz", DS p.30 "115,200", DS p.32 "240 Vac".
  - Manual p.106 "shall not exceed 8 A", p.429 Modbus, p.615 SEL-2244-4, p.646 CT inputs.
- **DS p.4 check did not match the log's wording.** The 09-21 19:24 entry marks "no loadable libraries, no directly
  addressable GPIO" as `[V]` from DS p.4. Page 4 says the RTAC logic engine is IEC 61131-3 (ST, LD, CFC) edited in
  ACSELERATOR RTAC. It does not say "no loadable libraries" and does not mention GPIO. That part is an inference from
  p.4 and should carry `[I]`. Flagged only; item 19 was not reopened.
- A missing `"local"` file was tested against a scratch manifest: exit code 1, no text file written, and `INDEX.txt`
  shows MISSING.
- Non-ASCII: the script, manifest and `INDEX.txt` are pure ASCII. The manual text keeps 153 non-ASCII characters
  (French safety notes, diameter sign, dagger footnotes, angle sign). The datasheets keep 22 and 17.

### Open items

No new numbers.

### Not done

- The order summary PDF has no text copy. It needs OCR or a manual transcription.
- The duplicate `Axion Panel Drawings.pdf` was not archived or renamed. That is Jordan's call. Whether a real panel
  drawing set exists is unknown.
- `HOMEWORK_READING.md` still points to the PDFs, not to the new text files.
- No git commit.

---
