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
