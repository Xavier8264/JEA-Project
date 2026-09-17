# JEA power delivery one-line: topology and voltage reference

Companion text for `jea_power_delivery_oneline.png` / `.pdf`. This file exists so the
diagram's content is retrievable by project knowledge search, which cannot read images.

JEA = Jackson Energy Authority, Madison County, Tennessee. A TVA local power company
(LPC). NOT Jacksonville Electric Authority. Serves ~35,000 customers across 29
substation locations, 53 power transformers, 700+ miles of distribution and
transmission line.

---

## Voltage tiers, generation to service

| Tier | Voltage | Owner | Notes |
|---|---|---|---|
| Generation | 13.8 - 24 kV | TVA | Generator terminal voltage |
| Step-up (GSU) | to 161 kV or 500 kV | TVA | Generator step-up transformer at plant |
| Transmission | 161 kV, 500 kV (also 230, 69) | TVA | Meshed network, not radial |
| Delivery point | 161 kV | TVA/JEA boundary | Metering point, ownership boundary |
| Subtransmission | 46 kV | JEA | Typical LPC value is 69 kV; JEA is 46 kV |
| Primary distribution | 12,470Y/7,200 V | JEA | ANSI standard nominal. 7,200 V line-to-neutral |
| Utilization | 600 V and below | Customer | See customer table below |

TVA does NOT operate 345 kV. Any diagram showing 345 kV is not TVA territory.

## Customer service voltage classes (ANSI C84.1)

| Customer type | Service voltage | Configuration | Fed from |
|---|---|---|---|
| Residential | 120/240 V | 1-phase, 3-wire, center-tapped | Pole-top or pad-mount xfmr on 12.47 kV lateral |
| Small commercial | 208Y/120 V, or 120/240 V | 3-phase 4-wire wye, or 1-phase | 12.47 kV lateral |
| Large commercial, school, office | 480Y/277 V | 3-phase 4-wire wye | 12.47 kV lateral; 277 V used for lighting |
| Light industrial | 480Y/277 V or 480 V | 3-phase | 12.47 kV lateral |
| Large industrial | 12,470Y/7,200 V primary | Customer-owned step-down | Feeder tap or substation |
| Very large industrial | 46 kV or 161 kV | Customer substation | Subtransmission or transmission direct |
| Large in-plant motors | 4,160 V or 13.8 kV | 3-phase | Customer's own medium-voltage system |

Common error to avoid: "440 V" and "220/440 V" are NOT ANSI C84.1 nominal system
voltages. The correct three-phase low-voltage nominals are 208Y/120, 240, 480Y/277,
480, and 600. 440 V appears in C84.1 only as a Range B utilization limit under a
480 V nominal system. 460 V is the NEMA motor nameplate rating for a 480 V system.
Zach Wadley's office building is 277/480 V.

---

## Cross-ties, by tier

1. Transmission interconnection. TVA network is meshed and tied to neighboring
   utilities and other LPCs. Context only, not in trainer scope.
2. Subtransmission loop tie, 46 kV, NORMALLY CLOSED. Two TVA delivery points feed
   one loop that serves multiple distribution substations. Not in trainer scope.
   CONFIDENCE LOW: loop configuration is inferred from standard practice, not
   confirmed for JEA's actual 46 kV system.
3. Distribution feeder tie, 12.47 kV, NORMALLY OPEN. Between a feeder from
   Distribution Sub A and a feeder from Distribution Sub B. This is the FLISR
   restoration path and the only tie in the tabletop trainer.
4. Substation bus tie breaker, NORMALLY OPEN. Inside a two-transformer substation.
   Backs up a failed transformer within the same substation. This tie belongs
   between distribution buses, NOT between GSU transformers.

Key principle: the distribution system is physically looped but operationally
radial. Feeders are built to reach each other and then deliberately held open at a
tie point. Closing that tie after fault isolation is the "R" in FLISR.

---

## Feeder devices shown on the diagram

- Substation feeder breaker (RMAG 15 kV class), with SEL-351S relay
- Recloser (Viper ST) for overhead sections
- Pad-mounted switchgear with VCB compartments, for underground sectionalizing
- Voltage regulator
- Distribution transformer, pole-top (overhead) or pad-mounted (underground)
- DER interconnection point, inverter-coupled, governed by IEEE 1547 anti-islanding

Pad-mounted transformers are passive and cannot isolate faults. Pad-mounted
switchgear is the isolation device in underground FLISR.

---

## Open questions flagged on this diagram

- Does JEA own the 161/46 kV transformers, or does TVA? The diagram assumes the
  delivery point is the ownership boundary. Needs Zach confirmation.
- Is JEA's 46 kV subtransmission actually looped or radial per substation? If
  radial, the "two independent sources" framing on the tabletop is weaker and
  should be reframed as two feeders off different distribution substations.
- The diagram is single-line throughout. Demonstrating single-phase lateral fusing
  or unbalanced fault behavior would require a three-line version of the feeder tier.
