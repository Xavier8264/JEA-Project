# JEA Tabletop FLISR Trainer: Physical Layout Spec

Machine-readable companion to the layout plan view. Generated from `build_layout.py`;
every table below is emitted from the same geometry the drawing renders, so the two
cannot drift apart. All coordinates are inches, origin at the SW corner of the board,
x east, y north. Board is 48.0 x 48.0.

This file is the interface to the ESP32 animation session. It carries the topology
graph, the strip geometry, the pixel budget and the harness pinout. It does not carry
animation logic.

## 1. Board and panels

| | |
|---|---|
| Board | 48.0 x 48.0 in |
| Panels | four 24 x 24, seams at x=24.0 and y=24.0 |
| Panel names | Q1 NW, Q2 NE, Q3 SW, Q4 SE |
| Strip gap at a seam | 0.4 in each side, 0.8 in total |
| Nominal terrain scale | 1:220; the board represents about 880 x 880 ft |
| Device scale | over-scaled to about 1:60 so each can carry an indicator LED |

### PLC / HMI keep-out (SEL-2240 10-slot panel mount)

| Rect | SW | NE | Size |
|---|---|---|---|
| Panel cutout | (27.75, 2.00) | (45.50, 10.80) | 17.75 x 8.80 |
| Bezel | (26.75, 1.60) | (46.50, 11.20) | 19.75 x 9.60 |
| Keep-out, bezel + 0.5 | (26.25, 1.10) | (47.00, 11.70) | 20.75 x 10.60 |

Cutout is 17.75 x 8.80, verified against Axion instruction manual Figures 2.2 and 2.4.
Nothing above the board (strip, prop, button or device) enters the keep-out rect.

## 2. Devices

| Tag | Class | Panel | x | y | Represents | Bounds | Normal |
|---|---|---|---|---|---|---|---|
| `SUB_A_BKR` | interrupting | Q3 | 12.00 | 10.00 | R-MAG 15 kV + SEL-351S | Z1 | CLOSED |
| `DEV_A1` | interrupting | Q3 | 12.50 | 18.00 | Padmount SG, VCB way | Z1/Z2 | CLOSED |
| `DEV_A2` | interrupting | Q1 | 12.50 | 29.50 | Padmount SG, VCB way | Z2/Z3 | CLOSED |
| `TIE` | restoring | Q2 | 26.50 | 25.50 | Padmount SG, switch way | Z3/Z4 | OPEN |
| `DEV_B2` | interrupting | Q2 | 31.00 | 25.50 | Padmount SG, VCB way | Z4/Z5 | CLOSED |
| `DEV_B1` | interrupting | Q4 | 38.00 | 22.00 | Padmount SG, VCB way | Z5/Z6 | CLOSED |
| `SUB_B_BKR` | interrupting | Q2 | 38.00 | 36.50 | R-MAG 15 kV + SEL-351S | Z6 | CLOSED |
| `DER_PCC` | must-trip | Q4 | 34.00 | 21.00 | IEEE 1547 PCC recloser | DER | CLOSED |

Mainline order, source to source:

```
SUB_A_BKR -Z1- DEV_A1 -Z2- DEV_A2 -Z3- TIE -Z4- DEV_B2 -Z5- DEV_B1 -Z6- SUB_B_BKR
                                      (N.O.)
                    DER_PCC hangs off Z5 as a must-trip branch
```

## 3. Zones

| Zone | Bounded by | Normal source | Load it drops | Panels it spans |
|---|---|---|---|---|
| Z1 | `SUB_A_BKR` / `DEV_A1` | A | RES_1 south (L1a) | Q3 |
| Z2 | `DEV_A1` / `DEV_A2` | A | RES_1 north (L1b) | Q1, Q3 |
| Z3 | `DEV_A2` / `TIE` | A | RES_2 (L2) | Q1, Q2 |
| Z4 | `TIE` / `DEV_B2` | B | SMALL_COMM (L3) | Q2 |
| Z5 | `DEV_B2` / `DEV_B1` | B | DER branch (L4, via DER_PCC) | Q2, Q4 |
| Z6 | `DEV_B1` / `SUB_B_BKR` | B | INDUSTRIAL (L5) | Q2, Q4 |

## 4. Edges (LED strip geometry)

One row per continuous strip run. Runs `Z*` are mainline, `L*` are laterals. An edge
never crosses a seam: any run that does is already split into two edges with the 0.4 in
gap applied. Pixel counts are per edge at three strip densities.

| Edge | Run | Zone | Src | Panel | From | To | in | px 30/m | px 60/m | px 144/m |
|---|---|---|---|---|---|---|---|---|---|---|
| `E01` | Z1 | Z1 | A | Q3 | (12.00, 10.00) | (12.50, 10.00) | 0.50 | 0 | 1 | 2 |
| `E02` | Z1 | Z1 | A | Q3 | (12.50, 10.00) | (12.50, 18.00) | 8.00 | 6 | 12 | 29 |
| `E03` | L1a | Z1 | A | Q3 | (12.50, 16.00) | (16.00, 16.00) | 3.50 | 3 | 5 | 13 |
| `E04` | L1a | Z1 | A | Q3 | (16.00, 16.00) | (23.00, 16.00) | 7.00 | 5 | 11 | 26 |
| `E05` | Z2 | Z2 | A | Q3 | (12.50, 18.00) | (12.50, 23.60) | 5.60 | 4 | 9 | 20 |
| `E06` | Z2 | Z2 | A | Q1 | (12.50, 24.40) | (12.50, 29.50) | 5.10 | 4 | 8 | 19 |
| `E07` | L1b | Z2 | A | Q3 | (12.50, 22.50) | (16.00, 22.50) | 3.50 | 3 | 5 | 13 |
| `E08` | L1b | Z2 | A | Q3 | (16.00, 22.50) | (23.00, 22.50) | 7.00 | 5 | 11 | 26 |
| `E09` | Z3 | Z3 | A | Q1 | (12.50, 29.50) | (23.60, 29.50) | 11.10 | 8 | 17 | 41 |
| `E10` | Z3 | Z3 | A | Q2 | (24.40, 29.50) | (26.50, 29.50) | 2.10 | 2 | 3 | 8 |
| `E11` | Z3 | Z3 | A | Q2 | (26.50, 29.50) | (26.50, 25.50) | 4.00 | 3 | 6 | 15 |
| `E12` | L2 | Z3 | A | Q1 | (16.00, 29.50) | (16.00, 34.50) | 5.00 | 4 | 8 | 18 |
| `E13` | L2 | Z3 | A | Q1 | (16.00, 34.50) | (5.50, 34.50) | 10.50 | 8 | 16 | 38 |
| `E14` | L2 | Z3 | A | Q1 | (5.50, 34.50) | (5.50, 43.50) | 9.00 | 7 | 14 | 33 |
| `E15` | L2 | Z3 | A | Q1 | (5.50, 43.50) | (23.60, 43.50) | 18.10 | 14 | 28 | 66 |
| `E16` | L2 | Z3 | A | Q2 | (24.40, 43.50) | (26.00, 43.50) | 1.60 | 1 | 2 | 6 |
| `E17` | Z4 | Z4 | B | Q2 | (26.50, 25.50) | (31.00, 25.50) | 4.50 | 3 | 7 | 16 |
| `E18` | L3 | Z4 | B | Q2 | (30.00, 25.50) | (30.00, 31.00) | 5.50 | 4 | 8 | 20 |
| `E19` | L3 | Z4 | B | Q2 | (30.00, 31.00) | (34.50, 31.00) | 4.50 | 3 | 7 | 16 |
| `E20` | Z5 | Z5 | B | Q2 | (31.00, 25.50) | (31.00, 24.40) | 1.10 | 1 | 2 | 4 |
| `E21` | Z5 | Z5 | B | Q4 | (31.00, 23.60) | (31.00, 22.00) | 1.60 | 1 | 2 | 6 |
| `E22` | Z5 | Z5 | B | Q4 | (31.00, 22.00) | (38.00, 22.00) | 7.00 | 5 | 11 | 26 |
| `E23` | L4 | Z5 | B | Q4 | (34.00, 22.00) | (34.00, 21.00) | 1.00 | 1 | 2 | 4 |
| `E24` | L4 | Z5 | B | Q4 | (34.00, 21.00) | (34.00, 13.00) | 8.00 | 6 | 12 | 29 |
| `E25` | L4a | Z5 | B | Q4 | (34.00, 13.50) | (35.50, 13.50) | 1.50 | 1 | 2 | 5 |
| `E26` | L4b | Z5 | B | Q4 | (34.00, 15.50) | (35.50, 15.50) | 1.50 | 1 | 2 | 5 |
| `E27` | L4c | Z5 | B | Q4 | (34.00, 17.50) | (35.50, 17.50) | 1.50 | 1 | 2 | 5 |
| `E28` | L4d | Z5 | B | Q4 | (34.00, 19.50) | (35.50, 19.50) | 1.50 | 1 | 2 | 5 |
| `E29` | Z6 | Z6 | B | Q4 | (38.00, 22.00) | (38.00, 23.60) | 1.60 | 1 | 2 | 6 |
| `E30` | Z6 | Z6 | B | Q2 | (38.00, 24.40) | (38.00, 36.50) | 12.10 | 9 | 18 | 44 |
| `E31` | L5 | Z6 | B | Q2 | (38.00, 29.00) | (41.00, 29.00) | 3.00 | 2 | 5 | 11 |

Total route length 157.5 in (4.00 m).

## 5. Adjacency graph

Segment energization is a graph traversal, not a geometry problem. Nodes are devices
and load points; an edge is energized when a closed path exists from either source.

```
SOURCE_A --- SUB_A_BKR
SUB_A_BKR -- DEV_A1     zone Z1   taps L1a -> RES_1 south, 4 houses
DEV_A1 ----- DEV_A2     zone Z2   taps L1b -> RES_1 north, 4 houses
DEV_A2 ----- TIE        zone Z3   taps L2  -> RES_2, 16 houses
TIE ~~~~~~~~ DEV_B2     zone Z4   taps L3  -> SMALL_COMM     [TIE NORMALLY OPEN]
DEV_B2 ----- DEV_B1     zone Z5   taps L4  -> DER_PCC -> array, 4 rows
DEV_B1 ----- SUB_B_BKR  zone Z6   taps L5  -> INDUSTRIAL
SUB_B_BKR -- SOURCE_B
```

Normal state: every device CLOSED except TIE. Z1 to Z3 fed from A (blue), Z4 to Z6 fed
from B (green). After isolation the TIE closes and the open point moves to the faulted
zone boundary, so a segment source color is a function of topology, never a constant.

## 6. Fault-injection buttons

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

Each button sits 1.0 to 3.5 in off the run it faults, on the same panel as that run,
and outside every structure footprint and the pond. Asserted in the generator, not
eyeballed.

### Fault-point determinism

Decided 2026-09-10: the visible fault point is **fixed per button, not randomized**,
defined as the closest point on that button's assigned run. A small, finite set of
deterministic fault points is an intentional simplification, not a shortcut, and matches
Zach's stated intent that each button drive a hard-coded RTAC scenario rather than a real
injected fault.

"Closest point on the run" is ambiguous wherever a backbone bends near a button, so each
button must bind to **one explicit edge ID**, decided once and hard-coded into whatever
regenerates this file, never computed as a nearest-point-to-any-edge lookup at build or
render time. Below is a first-pass table, computed directly from the section 2/4 geometry
above (not from original design intent, since the generator that built this layout did not
survive in the working directory past its original session):

| Button | Nearest edge | Run | Distance in | Note |
|---|---|---|---|---|
| `FLT_Z1` | E02 | Z1 | 2.50 | Tied with `E03` (L1a) at 2.51 in, effectively the same point. Pick one. |
| `FLT_Z2` | E05 | Z2 | 1.50 | Clear |
| `FLT_Z3` | E09 | Z3 | 1.70 | Clear |
| `FLT_Z4` | E17 or E18 | Z4 / L3 | 1.70 | Exact tie, sits right at the Z4/L3 elbow. Pick one. |
| `FLT_Z5` | E22 | Z5 | 1.40 | Clear; `E23`/`E24` (the L4 branch) sit 2.0-2.8 in away |
| `FLT_Z6` | E30 | Z6 | 1.50 | Clear |
| `FLT_DER` | E24 | L4 | 1.80 | No edge is actually tagged zone `DER`: the DER branch edges (`E23`-`E28`) are tagged zone Z5, since they hang off Z5's boundary devices. `FLT_DER` has to bind to the L4 branch by run name, not by a zone-string match. |

`FLT_Z1` and `FLT_Z4` are genuine ties, not close calls, and need a human pick rather than
a formula. Whoever rebuilds the generator should hard-code all eight bindings as data, not
re-derive them geometrically.

## 7. Per-panel LED budget and harness

| Panel | Route in | Route px | House px | Load px | Device px | Chain px | 5V inject |
|---|---|---|---|---|---|---|---|
| Q3 | 35.1 | 54 | 8 | 0 | 2 | **64** | 1 |
| Q1 | 58.8 | 91 | 15 | 0 | 1 | **107** | 2 |
| Q2 | 38.4 | 58 | 1 | 5 | 3 | **67** | 1 |
| Q4 | 25.2 | 37 | 0 | 4 | 2 | **43** | 1 |
| **Board** | **157.5** | 240 | 24 | 9 | 8 | **281** | |

Counts are at 60 LED/m. Per-edge counts at 30/m and 144/m are in section 4, so the
strip choice can change without touching the layout.

Q1 exceeds 100 pixels and gets two injection points; the others get one. At 60 mA per
pixel a full-white board would draw about 16.9 A, but the animation is single-color at
partial brightness: budget about 5 A and specify one 5 V / 10 A supply.

### Per-panel connector, identical on all four panels

| Pin | Signal | Note |
|---|---|---|
| 1 | +5V | 18 AWG |
| 2 | +5V | doubled for current |
| 3 | GND | 18 AWG |
| 4 | GND | doubled |
| 5 | LED_DATA | 330 to 470 ohm series resistor at the strip end |
| 6 | BTN_COM | button common return |
| 7 | BTN_1 | |
| 8 | BTN_2 | |

Q4 carries three buttons (FLT_Z5, FLT_DER, RESET) and needs one more line than an
8-pin shell provides. Either go to a 10-pin shell on all four panels, or fit an
MCP23017 GPIO expander per panel and drop to 6 pins (5V, GND, DATA, SDA, SCL, spare).
The expander is the better choice if the button count grows past about 12.

### Center hub

All four panels meet at (24, 24). ESP32, 5 V supply and fuse block mount under Q4
beside the PLC where line power already enters. One umbilical per panel runs under the
board to a hub block at the center point. Assembly is: set panels on their registration
dowels, plug in four connectors.

**No conductor crosses a seam on the top surface.** Each panel chain is electrically
self-contained; the only inter-panel wiring is the four umbilicals underneath.

## 8. Seam crossings, graphical only

| # | Point | Run | Zone | Cover prop |
|---|---|---|---|---|
| 1 | (12.50, 24.00) | Z2 | Z2 | junction box |
| 2 | (24.00, 29.50) | Z3 | Z3 | junction box |
| 3 | (24.00, 43.50) | L2 | Z3 | junction box |
| 4 | (31.00, 24.00) | Z5 | Z5 | junction box |
| 5 | (38.00, 24.00) | Z6 | Z6 | junction box |

## 9. Props over discontinuities

Design rule R2: every strip corner, splice and seam break is covered by a prop, because
real underground distribution puts a junction box or a pull box at exactly those points.
24 props, generated from the route geometry rather than placed by hand.

| x | y | Kind | Reason |
|---|---|---|---|
| 12.50 | 10.00 | junction_box | strip corner / splice (Z1) |
| 34.00 | 13.50 | junction_box | lateral tap (L4a) |
| 34.00 | 15.50 | junction_box | lateral tap (L4b) |
| 12.50 | 16.00 | junction_box | lateral tap (L1a) |
| 16.00 | 16.00 | junction_box | strip corner / splice (L1a) |
| 34.00 | 17.50 | junction_box | lateral tap (L4c) |
| 34.00 | 19.50 | junction_box | lateral tap (L4d) |
| 31.00 | 22.00 | junction_box | strip corner / splice (Z5) |
| 34.00 | 22.00 | junction_box | lateral tap (L4) |
| 12.50 | 22.50 | junction_box | lateral tap (L1b) |
| 16.00 | 22.50 | junction_box | strip corner / splice (L1b) |
| 12.50 | 24.00 | junction_box | seam break (Z2) |
| 31.00 | 24.00 | junction_box | seam break (Z5) |
| 38.00 | 24.00 | junction_box | seam break (Z6) |
| 30.00 | 25.50 | junction_box | lateral tap (L3) |
| 38.00 | 29.00 | junction_box | lateral tap (L5) |
| 16.00 | 29.50 | junction_box | lateral tap (L2) |
| 24.00 | 29.50 | junction_box | seam break (Z3) |
| 26.50 | 29.50 | junction_box | strip corner / splice (Z3) |
| 30.00 | 31.00 | junction_box | strip corner / splice (L3) |
| 5.50 | 34.50 | junction_box | strip corner / splice (L2) |
| 16.00 | 34.50 | junction_box | strip corner / splice (L2) |
| 5.50 | 43.50 | junction_box | strip corner / splice (L2) |
| 24.00 | 43.50 | junction_box | seam break (L2) |

Corner props must be open-bottom shells, or the corner made with a solderless 3-pin
corner connector and the prop set beside it. A solid prop over a lit corner blocks
light; a solid prop over a seam break or a splice does not, because there is no pixel
at that point.

## 10. Scene areas

| Area | SW | NE | Straddles a seam |
|---|---|---|---|
| Legend / title block | (1.0, 0.8) | (25.5, 4.5) | yes, x=24 |
| Distribution Sub A | (1.5, 5.5) | (12.0, 14.0) | no |
| Residential 1 | (14.5, 13.5) | (23.5, 28.0) | yes, y=24 |
| Residential 2 | (2.0, 32.0) | (26.5, 46.5) | yes, x=24 |
| Small commercial | (28.5, 28.0) | (35.5, 34.5) | no |
| Distribution Sub B | (34.0, 36.5) | (46.0, 45.5) | no |
| Industrial customer | (40.0, 25.0) | (47.0, 34.0) | no |
| DER solar array | (35.0, 12.5) | (46.8, 20.5) | no |
| Pond | (2.0, 18.1) | (10.5, 29.9) | yes, y=24 |

Four features cross a seam by intent so the board reads as one continuous scene rather
than a grid of four boards. Individual props never straddle a seam; areas do.

## 11. Open items

1. Scale sign-off. 1:220 is a proposal. Zach offered physical dimensions of the actual
   gear so devices can be scaled properly.
2. Axion mounting orientation. The manual requires modules vertical with 0.5 in
   clearance above and below; flat panel-mount lays them horizontal. Worth a question
   to SEL or Zach.
3. Cutout structure. A 17.75 x 8.80 hole leaves a 2.0 in bridge at the front edge. Do
   not cut the cardboard mockup, just mark it.
4. Panel registration. The seamless read depends on it: two dowel pins per seam or a
   shared sub-frame, plus vinyl artwork printed as four tiles with the image continuing
   across each joint.
