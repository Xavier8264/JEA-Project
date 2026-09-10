# Power Line Fault Control System — Project Memory Export

Export date: 2026-09-07
Project ID: `019dbb5e-0528-766a-906b-8f8d1812fc0b`
Scope: all memory files stored under this project's subtree (5 files)
Note: content is verbatim from memory. Unicode arrows normalized to `->`.

---

## 1. index.md

```yaml
name: "Power Line Fault Control System"
description: "Power Line Fault Control System — Senior capstone with JEA: a tabletop FLISR distribution-automation demo trainer using SEL hardware."
```

---

## 2. overview.md

*Description: FLISR tabletop trainer capstone — purpose, team, deliverable, domain scope, and current state as of PDR prep*
*Aliases: FLISR trainer, JEA capstone, FLISR demo table*

- [stated] Jordan Prunty is a university student and team lead on a senior capstone project in partnership with JEA (Jackson Energy Authority, Madison County TN — a TVA local power company, NOT Jacksonville Electric Authority)
- [stated] JEA voltage classes: TVA transmission 161 kV-500 kV -> JEA subtransmission 46 kV -> JEA primary distribution 12,470Y/7,200 V; JEA serves ~35,000 customers, 29 substations, 53 power transformers, 700+ miles of line
- [stated] The project builds a physical tabletop FLISR (Fault Location, Isolation, and Service Restoration) demonstration trainer for underground distribution systems
- [stated] Team is three people: Jordan (main point of contact), Gage, and Cody
- [stated] Industry mentor is Zach Wadley, PE, at JEA; preferred first communication channel is email, with in-person meetings at the JEA plant and Teams as fallback
- [stated] Faculty advisors are Dr. Pingen and Dr. Schwindt
- [stated] Deliverable is a 4'x4' modular tabletop display — four 2'x2' panels using 1"x1" aluminum extrusion frames
- [stated] The display physically demonstrates distribution automation concepts, specifically FLISR logic, using SEL hardware, addressable LEDs, and 3D-printed scale components
- [stated] End users range from new JEA hires to broader educational audiences
- [stated] Success means a working, aesthetically polished demo that correctly demonstrates fault injection, isolation, and service restoration sequences
- [stated] Jordan holds primary responsibility for hardware, physical design, CAD, and circuit work; teammate ownership of PLC/firmware logic is an intentional split
- [stated] Key domain areas: power distribution topology (generation -> transmission -> subtransmission -> primary distribution -> utilization), FLISR logic, SEL-2240 Axion platform, AcSELERATOR, distribution automation, SCADA concepts, addressable LED control, embedded systems (ESP32), and modular mechanical design
- [stated] Schedule gates: long-lead POs by ~11/6/26; successful end-to-end FLISR run by ~2/26/27; hard project completion ~4/6/27 (UU event)
- [stated] The 10/26-11/20 window is the most overloaded stretch of the schedule

### Current state (as of PDR prep, ~first week of October)
- [stated] One-line topology is the most time-sensitive unresolved decision ahead of PDR (approximately first week of October) — this is the current critical path item
- [stated] Recommended topology architecture: two distribution substations at opposite corners, each feeding a radial feeder toward the middle, with a normally-open tie switch where the feeders meet
- [stated] Four to six isolatable fault zones total, constrained by the 6 DI budget for fault injection
- [stated] Controller platform confirmed as SEL-2240 Axion (not SEL RTAC — an important distinction to maintain)
- [stated] Open item: whether RTAC and power coupler consume backplane slots, which determines 4-slot vs. 10-slot chassis and enclosure size
- [stated] Open items requiring Zach confirmation: written confirmation on 120VAC scope (mains to relay panel only vs. distributed on tabletop); JEA PO turnaround time; vendor lead times on Axion/RTAC controllers; whether SEL-2240 and RTAC are separate purchases
- [stated] Confirm the 4'x4' footprint with Zach — it is Jordan's assumption, not explicitly stated in sponsor documents

### On the horizon
- [stated] Finalize one-line topology before PDR
- [stated] Complete I/O math once topology is frozen — map switch positions and control signals to SEL-2244-2/4 DI modules and SEL-2244-3 DO modules
- [stated] Resolve total switchable segment count, which gates the I/O budget and PSU spec
- [stated] Clarify whether industrial customer branch and DER integration are in scope for v1 — DER confirmed in-scope per SOW; industrial branch unconfirmed
- [stated] Resolve load lateral representation approach, undecided alongside fault zone count
- [stated] Get started in AcSELERATOR RTAC software ahead of hardware availability — build project, import I/O module templates, draft tag structure
- [stated] A 3D visualization / web-based gamified fault-response trainer is a parallel concept being explored (Three.js, Vite, Cloudflare Pages stack; Blender -> GLB export pipeline; Blender MCP plugin setup pending)

---

## 3. design-decisions.md

*Description: Locked and recommended technical decisions — LED architecture, electrical layout, mechanical/connectors — with rationale and rejected options*

### LED architecture
- [stated] WS2812B (5V) recommended over WS2815 for short segmented runs
- [stated] Recommended hybrid approach: off-the-shelf WS2812B strip in routed channels under frosted acrylic diffuser for line runs; small custom node PCBs for houses and key components; one custom panel controller PCB per panel (ESP32, level shifter, buck converter, optocouplers, terminal blocks)
- [stated] Full-panel custom PCBs were evaluated and rejected — they exceed JLCPCB standard dimensions, carry flex risk, and are premature before topology freeze
- [stated] PCBs at full 2'x2' panel scale exceed standard fab machine envelopes and introduce flex-induced solder joint cracking; small targeted custom boards are higher value
- [stated] WS2812B shift-register architecture means hard power cuts mid-chain cause downstream data loss — this is the architectural reason for the separate segment bus approach

### Electrical architecture
- [stated] Separate the switched 24VDC segment bus (driven by Axion DO contacts) from the permanently powered 5V LED layer
- [stated] One ESP32 per panel senses segment energization via optocouplers and renders animations
- [stated] Distribute 24V to panels and buck down to 5V locally to avoid voltage drop
- [stated] SEL-2244-3 DO contacts cannot directly switch 5V LED power — 0.75A breaking capacity, 19.2V minimum rating

### Mechanical
- [stated] The Axion chassis cannot fit within the table height envelope — it must be housed in a separate vertical relay panel module as a fifth transport piece
- [stated] Star wiring topology back to the relay panel recommended over daisy-chaining
- [stated] Tapered dowel pins plus separate latches for seam registration
- [stated] Neutrik XLR XX-series 4-pin connectors specified for inter-panel connections — rated >1,000 mating cycles, and 4-pin avoids accidental audio equipment mating
- [stated] Calculating realistic service life cycle count before choosing connectors eliminated Deutsch DT and Molex Mini-Fit Jr in favor of Neutrik XLR

---

## 4. domain-principles.md

*Description: FLISR and distribution-automation domain knowledge plus design principles that would be costly to relearn*

- [stated] Topology before geometry: finalize the one-line fault zone topology before locking physical panel geometry or purchasing custom PCBs; module seams should align with protective/switching devices
- [stated] Simulated vs. real power: never conflate real power delivery (120VAC for Axion, low-voltage DC for LEDs) with simulated feeder power flow — this is a core design constraint
- [stated] Tie point placement: the normally-open tie point belongs between two distribution feeders, not between GSU transformers (confirmed correct against a teammate's proposal)
- [stated] Pad-mounted transformers are passive and cannot isolate faults; pad-mounted switchgear with VCB compartments is the core isolation device in underground FLISR
- [stated] FLISR sequence: fault -> upstream interrupting device trips -> sectionalizing devices isolate faulted segment during dead interval -> upstream device recloses (restoring healthy upstream section) -> normally-open tie switch closes (restoring healthy downstream section from alternate source)
- [stated] Graph over Cartesian: model the network as a graph (node/edge tables) rather than coordinates for fault simulation logic — physical coordinates are for visualization only; topology drives computation
- [stated] Preparation compresses timeline: arriving at Zach meetings with specific, topology-grounded questions rather than general ones positions Jordan as decision-validator rather than discovery-seeker

---

## 5. working-style-and-tools.md

*Description: How Jordan wants to work in this project, plus the hardware, software, and fabrication stack in use*

### Ways of working
- [stated] Prefers to thoroughly discuss and plan before executing — deliberate, discussion-first collaboration before any building or coding
- [stated] Works methodically and one topic at a time when learning new domain material; requests corrections of misconceptions explicitly
- [stated] Provides constraints incrementally and expects Claude to manage logic, flag risks, and surface important context proactively without being asked
- [stated] Communication style is terse and directive; prefers concise responses with clear recommendations over exhaustive option lists
- [stated] Wants to proceed directly to full-scale implementation without intermediate small-scale prototypes — this preference should be respected without revisiting
- [stated] Cross-references guidance against datasheets and sponsor documents; appreciates explicit confidence levels on inferences

### Tools & resources
- [stated] SEL hardware: SEL-2240 Axion, SEL-2244-2/4 (DI modules), SEL-2244-3 (DO modules), SEL-351S relay; SEL-2240 datasheet available in project files
- [stated] Software: AcSELERATOR Diagram Builder/RTAC, LibreCAD (one-line diagram), Fusion 360 (CAD/3D modeling), NetworkX (Python graph library), Milsoft LightTable (power flow modeling — Zach's tool)
- [stated] Embedded/electronics: ESP32, WS2812B LED strips, 74HCT245/74AHCT125 logic-level shifters, optocouplers, Neutrik XLR XX-series connectors
- [stated] Web stack for the parallel 3D/gamified trainer concept: Blender, Three.js, Vite, GitHub, Cloudflare Pages, GLB export, Blender MCP plugin (setup pending)
- [stated] Fabrication: JLCPCB (PCB fab), 1010-series aluminum extrusion, frosted acrylic diffuser
- [stated] Project files are at `/mnt/project` — scope of work `.docx`, kickoff transcript, PowerPoint export, concept image `.png`

---

## Not included in this export

The following memory exists at the account level, outside this project's subtree, and was not included:

- `/profile.md` (identity)
- `/preferences.md` (global response preferences)
- 16 other `/areas/` files and 6 `/topics/` files
- 8 other project subtrees (Plastination, Gantry, Rubik's Cube, Chess Robot, Portfolio, Robotic Arm, Atlas, Wabtec)
