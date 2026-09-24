# JEA Feedback and PLC-ESP32 Architecture (2026-09-23)

Saved from a Claude Code chat on 2026-09-23 for future reference. The full log, with sources and confidence
markers, is the `2026-09-23 20:26 CDT` entry in `PROJECT_MEMORY.md` (open items 50-61).

---

I logged everything to PROJECT_MEMORY.md as one new entry at the bottom, with open items 50-61. The ESP32 model and the custom PCB task (item 50) are in there. The ESP32 definition is also saved as a separate memory that loads every session, so "ESP32" will always mean the AITRIP 30-pin USB-C board.

**Short answer:**
- **PLC constraint:** it holds, so the ESP32 stays in the final product.
- **Option A:** can be wired, but it breaks a JEA requirement.
- **Option B:** works, and I checked it in the manual.
- **Third option:** Option B plus a fallback. That's my recommendation.

## The constraint still holds (high confidence)

I re-read the datasheet this time instead of trusting my old notes. The Axion's outputs are mechanical relays. They take 8 ms to open, are rated for 2.5 switching cycles a second, and last 10 million operations (datasheet pp.32-33). The LED strips need an 800 kHz data signal, so the PLC can't drive them.

## How PLC inputs and outputs differ from ESP32 pins

On the ESP32, a pin is a logic signal on the chip itself. On the Axion, each input or output is one terminal of a circuit that you wire and power yourself.

| | ESP32 pin | Axion input (32-input module) | Axion output (16-output module) |
|---|---|---|---|
| What it is | a transistor on the chip | an isolated optical input | a relay contact (a mechanical switch) |
| Who supplies the voltage | the chip, 3.3 V | you, usually a separate 24 Vdc supply | you, a supply and load wired through the contact |
| On/off | about 2.5 V / 0.8 V | on at 15-30 V, off below 10 V, draws 8 mA | closed or open |
| Speed | millions of times a second | checked every 1 ms, with an adjustable delay to ignore switch bounce | 8 ms to move |
| Direction | set in code | input only | output only |
| Protection | none, and 5 V will damage it | rated 300 V, withstands 5 kV spikes | surge protection across the contacts |

The Axion columns come from the datasheet and manual pp.615-617. The ESP32 column is standard spec; I didn't read Espressif's datasheet this session.

What this means in practice:
- **Wiring a button to the Axion:** the 24 V supply runs through the button to the input terminal, and the return wire goes back to the supply. No pull-up resistors and no debounce code.
- **Never connect an Axion terminal straight to an ESP32 pin.**
  - Axion output to ESP32: go through an optocoupler on the 24 V side.
  - ESP32 to Axion input: use a transistor or optocoupler to switch 24 V. 3.3 V never reaches the 15 V "on" level.
- **One correction to what we logged at kickoff:** the input voltage is set per module, not per input. It doesn't affect us, since everything will be 24 V.

## Option A: two separate systems driven by the same buttons

**The wiring is easy.** Industrial 22 mm pushbuttons accept stacked contact blocks. Each button gets two isolated contacts, one at 24 V for the Axion and one at 3.3 V for the ESP32. Using one contact for both would put 24 V on an ESP32 pin.

**It fails on function:**
1. **HMI fault injection breaks it.** Zach asked for this at kickoff. A fault started from the HMI only reaches the Axion, so the board never shows it. This alone rules Option A out.
2. **The LEDs would show the ESP32's decisions, not the RTAC's.** The trainer exists so JEA can watch and edit RTAC logic. The first time someone edits that logic, the board and HMI disagree and nothing catches it.
3. **The two new switches double the risk of drifting apart.** Both systems must read the temporary/permanent and DA on/off switches the same way. If one side reboots or resets, they fall out of step.

**The voltage and current readings are a separate question.** You need them in either option. The metering module has 4 current and 4 voltage inputs, which is one metering point, not one per zone. A hidden load board could push real current into it, but only at one location, and it puts live AC power and heat inside a table that high school students touch.

I'd compute the readings in the RTAC from a table of values for each switching state, ideally from a Milsoft load flow. That links up with the Milsoft questions in section J of the PDR question list. Medium confidence.

## Option B: the Axion is the only brain

This works, and the manual confirms it. The RTAC can run Modbus over serial (RTU) or Ethernet (TCP), and it can poll other devices for data (manual pp.429-430).

Buttons and switches go into Axion inputs. The FLISR logic runs in the RTAC. About every 100 ms, the RTAC writes about 25 values to the ESP32 (zone states, device states, step, and a heartbeat counter), and the ESP32 animates them.

**There's one catch with your board:** it has no Ethernet jack. My Sept 21 recommendation (Modbus over Ethernet) assumed it did. The new order:
1. **Modbus RTU over RS-485 (recommended).** It needs about a $2 RS-485 chip and 3 ESP32 pins, wired to one of the RTAC's four serial ports (datasheet p.30). There are no IP addresses, so it avoids the subnet problem Zach already runs into.
2. **An add-on Ethernet module (W5500) with Modbus TCP.** It works, but takes more parts and pins.
3. **WiFi:** no. The RTAC has no WiFi, and it would add an access point to a control demo.

## Third option: Option B plus a standalone fallback

Only one brain drives the display at any time:
- Each button gets the second contact block anyway, and the ESP32 reads the buttons through an input expander chip (MCP23017).
- The ESP32 keeps the REV2 FLISR logic.
- **While the RTAC heartbeat is present,** the ESP32 displays only what the RTAC sends. It can also run its own logic quietly and flag any disagreement, which helps while you write the RTAC code.
- **If the heartbeat is gone for about 2 seconds,** the ESP32 switches to its own logic and lights a visible STANDALONE marker.

**Why it's worth it:**
- You can demo before the Axion arrives in November.
- The board still works while JEA has the Axion out for reprogramming.
- The REV2 logic becomes the reference to test the RTAC code against.

**Cost:** 12-16 extra contact blocks, one chip, and some firmware.

I'd skip a fourth variant: wiring the buttons only to the ESP32 and having the RTAC read them over Modbus. It saves wiring, but loses the real input wiring a JEA technician should see.

## The new JEA requests

- **With and without DA:**
  - Without DA, protection still works. The upstream recloser still trips, recloses and locks out. What's lost is the automatic locate, isolate and restore.
  - Every section past the fault stays dark until a crew finds the fault, opens the switches and closes the tie by hand. That typically takes an hour or more (estimate).
  - With DA, healthy sections are back within 5 minutes. IEEE 1366 counts that as a momentary outage, so it drops out of the SAIDI and SAIFI reliability numbers.
  - I'd add an outage clock to make the difference visible.
  - The DER's shutdown when the grid goes dead (anti-islanding) never depends on DA.
- **Temporary/permanent switch:**
  - Transformer faults ignore it. Those trips lock out and never reclose.
  - Utilities usually don't reclose on underground cable, so the narration shouldn't claim cable faults clear themselves. This reopens the overhead-mainline question we put off on Sept 10.
- **IEEE 1547 and reclosing:** the DER must stop feeding the grid within 2 seconds of being islanded. The Sub B recloser's first reclose delay has to be longer than that, or it closes onto an out-of-sync island. That's a real lesson that comes free with the switch.
- **PV backfeed:** this is exactly what IEEE 1547's default anti-islanding rule forbids.
  - The allowed version is a planned island. It needs the utility's agreement, an inverter that can hold voltage on its own, and a battery. PV alone can't hold voltage.
  - I'd show both: the default (PV trips, then waits about 5 minutes after power returns) and the planned island. JEA needs to confirm that's what they meant.
- **Transformer faults:**
  - Each substation gets a new high-side breaker. The existing substation breaker becomes the low-side breaker.
  - A transformer fault takes out the whole feeder, and FLISR has to move all of it across the tie, so tie capacity becomes the lesson.
  - Two physical/code changes: the Sub A bus is coded to never go dark, and that has to change. Sub B has no visible bus LEDs, so some need adding.
- **Fuses and the Residential 2 recloser:** they only do something visible if there's a fault past them. Adding those faults means 3 more zones, devices and buttons.
- **Blinking fault markers at the old button spots:** I'd make them LED pixels on one extra hidden strip run by the ESP32, so the blink lines up with the fault animation. This replaces the Sept 10 "buttons stay scattered" decision.
- **Junction boxes:** you're right that the code doesn't change. Don't cover the status pixel where a device sits on a corner:
  - DEV_A2 is on the N30 corner (confirmed in the code notes).
  - DEV_B1 at N26 looks like a corner too, but I'm inferring that from the run directions.
- **Input count:** about 12 inputs total, or 15 with the fuse/recloser faults. The 32-input module has plenty of room.

**ESP32 migration:**
- The strip data line needs a 74AHCT125 level shifter, since 3.3 V is below the strip's 3.5 V threshold.
- FastLED can drive up to 8 strips in parallel on this chip, which is enough for 4 panels plus the marker strip.
- You typed CP2012 for the USB chip. I logged it as CP2102, the usual Silicon Labs part; check the marking on the chip.

## Questions only you or JEA can answer
1. Should the fuses and the Residential 2 recloser get their own fault buttons, or be display only?
2. Does the PV backfeed mean a planned island with a battery, or something else?
3. For Michael: how many reclose attempts, how long between them, and does he prefer RS-485 or Ethernet?

I didn't change any code or the requirements doc, and I didn't make a git commit. PROJECT_MEMORY.md is modified but not committed. If Cody and Gage would find it useful, I can turn the I/O explanation and option comparison into a page for them.
