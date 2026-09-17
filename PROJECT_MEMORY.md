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
