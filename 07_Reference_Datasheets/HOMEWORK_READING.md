# Homework Reading: PLC, Measurement, Comms, Protection, DER

Written 2026-09-24 for Jordan. The parts are in order; each one builds on the one before.

- **Local** means a file in this repo. The `.txt` files in `web_sources/text/` are plain-text copies of the web
  pages used as sources for the project log. Lines like `=== page 14 ===` mark PDF page breaks.
- Page numbers below are **PDF page numbers**: what your PDF viewer shows, which can differ from the number printed
  on the page.
- **Online** links were all checked on 2026-09-24.
- To refresh the local copies or add a source: add an entry to `web_sources/sources.json`, then run
  `python 07_Reference_Datasheets/web_sources/web_to_text.py`.

---

## Part 0. What we already worked out

- Local: [2026-09-23 JEA Feedback and PLC-ESP32 Architecture.md](../02_Planning/2026-09-23%20JEA%20Feedback%20and%20PLC-ESP32%20Architecture.md).
  The plain-language version of the 9/23 session: PLC I/O vs ESP32 pins, and options A / B / C.
- **Two things changed since:**
  - Option A is out.
  - The ordered input module is **125 V, not 24 V**.

  Both are recorded in the 2026-09-24 11:12 entry of `PROJECT_MEMORY.md`.

---

## Part 1. How a PLC works (mapped onto what you know from the ESP32)

**Online**

1. **Kuphaldt, *Lessons In Industrial Instrumentation*, v2.33.** Free, CC BY 4.0, a 103 MB PDF:
   <https://www.ibiblio.org/kuphaldt/socratic/sinst/book/liii.pdf>
   - Chapter "Programmable Logic Controllers," PDF pp.794-889. Read these sections first:
     - "Input/Output (I/O) capabilities," p.804
     - "Logic programming," p.816
   - Then:
     - "Human-Machine Interfaces," p.878
     - "How to teach yourself PLC programming," p.884
   - Optional background: "Relay control systems," p.776. It explains why ladder logic looks the way it does.
2. **AutomationDirect, "Sinking and Sourcing Concepts"** (2 pages):
   <https://cdn.automationdirect.com/static/specs/sinksource.pdf>
   Why a PLC input needs you to supply the voltage, and what a "common" is. Our SEL-2244-4 has two banks of 16
   inputs, and each bank shares one common.
3. **PLC Academy, Structured Text tutorial:** <https://www.plcacademy.com/structured-text-tutorial/>
   Structured Text is the IEC 61131-3 language closest to C. The RTAC runs IEC 61131-3 logic.
4. **SEL video portal** (free, official):
   - [ACSELERATOR RTAC: Programs, Functions, and Function Blocks, Part 1](https://video.selinc.com/support/detail/video/1813728421824293278/acselerator-rtac:-programs-functions-and-function-blocks-part-1).
     How RTAC code is organized. The series has three parts.
   - [ACSELERATOR RTAC: Quick Configuration](https://video.selinc.com/support/detail/video/1828488757789994375/acselerator-rtac:-quick-configuration).
     Building an RTAC project in under 15 minutes.
   - [How to Use the RTAC HMI, Part 1: ACSELERATOR Diagram Builder Overview](https://video.selinc.com/support/detail/video/5759029209001/how-to-use-the-rtac-hmi-part-1:-acselerator-diagram-builder%E2%84%A2-overview).
     How the HMI screens you view on the laptop get built.
5. **Optional: AutomationDirect, "Practical Guide to Programmable Logic Controllers"** (PLC Handbook), a broad free
   intro: <https://cdn.automationdirect.com/static/eBooks/PLC%20Handbook.pdf>

**Local** (SEL documents for the exact hardware JEA bought)

- [SEL-2240 Axion Node Summary](SEL-2240%20Axion%20Node%20_%20Summary%20_%20Schweitzer%20Engineering%20Laboratories.pdf):
  the order, showing which module sits in which slot.
- [2240_DS_20130827_01.pdf](2240_DS_20130827_01.pdf) (datasheet):
  - p.32: SEL-2244-3 relay outputs
  - p.33: SEL-2244-4 input thresholds (the 125 V row is ours), and the SEL-2245-2 analog inputs
  - pp.34-35: SEL-2245-4 AC metering
- [Axion Instruction Manual.pdf](Axion%20Instruction%20Manual.pdf):
  - p.106: input wiring rules (fusing, AC neutral to common)
  - p.160: task cycle time
  - p.566: web HMI
  - pp.615-617: input module and debounce
  - p.646: AC metering module settings

**Check yourself**

- Why will a button that switches 24 V never turn on our input module?
- What does "dry contact" mean for an Axion output? Why can't it drive a WS2812 strip?
- What happens, in order, during one RTAC task cycle?
- Where does the HMI actually run: on the laptop or in the RTAC?

---

## Part 2. How current and voltage get into the PLC (the professor's requirement)

**Online**

1. **IPS, "Current Transformers: The Basics"** (2 pages): <https://docs.ips.us/docs/W1003290.pdf>
2. **Kuphaldt** (same PDF as Part 1):
   - "Introduction to power system automation," p.1927
   - "Single-line electrical diagrams," p.1947
   - "Circuit breakers and disconnects," p.1953
   - "Electrical sensors," p.1975: potential transformers and current transformers

**Local**

- Datasheet pp.34-35: SEL-2245-4 ranges, 0.05-22 A and 5-400 V.
- Manual p.646: CT and PT ratio settings.

**Check yourself**

- A 600:5 CT has 300 A on its primary. What current reaches the SEL-2245-4, and what CT ratio would you enter?
- The proposed mini-grid measures only 4 points. Why only 4, and which 4 would you pick?

---

## Part 3. The RTAC-to-ESP32 link (item 51: RS-485 Modbus RTU)

**Online**

1. **TI, "The RS-485 Design Guide"** (SLLA272, 9 pages): <https://www.ti.com/lit/pdf/slla272>
   Covers termination, failsafe biasing, and grounding and isolation.
2. **Modbus.org, "MODBUS over Serial Line Specification and Implementation Guide V1.02":**
   <https://www.modbus.org/file/secure/modbusoverserial.pdf>
   - Data link layer (RTU framing): from p.7
   - Physical layer (wiring): from p.20
3. **Kuphaldt:**
   - "EIA/TIA-232, 422, and 485 networks," p.1078
   - "Modbus," p.1135
4. **Candidate ESP32 library:** [emelianov/modbus-esp8266](https://github.com/emelianov/modbus-esp8266).
   It runs Modbus RTU on the ESP32 as a server (slave). Not yet tested on our board.

**Check yourself**

- Where do the two 120-ohm terminating resistors go?
- In our design, which device is the Modbus client (master), and which is the server (slave)?

---

## Part 4. Distribution protection, FLISR, and "with and without DA"

**Online**

1. **G&W Electric, "What Causes an Electrical Recloser to Trip?":**
   <https://www.gwelectric.com/blog/2025/12/10/blog-why-electrical-reclosers-trip/>
   Short read: temporary vs permanent faults, and reclose attempts before lockout. It covers overhead lines only.
2. **Kuphaldt:**
   - "Introduction to protective relaying," p.2016
   - "Instantaneous and time-overcurrent (50/51) protection," p.2027
   - "Differential (87) current protection," p.2035. This is the transformer fault JEA asked for.
   - "Auxiliary and lockout (86) relays," p.2080
3. **US DOE, "Distribution Automation: Results from the Smart Grid Investment Grant Program"** (2016, 115 pages):
   <https://www.energy.gov/sites/prod/files/2016/11/f34/Distribution%20Automation%20Summary%20Report_09-29-16.pdf>
   - Section 2.1, "Remote Fault Location, Isolation, and Service Restoration": PDF pp.21-30
   - Chapter 5, "Integration of Distributed Energy Resources": p.76
4. **TD World, "Understanding Distribution Reliability Metrics":**
   <https://www.tdworld.com/overhead-distribution/article/21157348/understanding-distribution-reliability-metrics>
   SAIDI, SAIFI, MAIFI and IEEE 1366: the numbers that show why DA matters.

**Local**

- [ieee_pes_der_flisr_tutorial.txt](web_sources/text/ieee_pes_der_flisr_tutorial.txt), pp.1-3: the outline of a
  4-hour FLISR tutorial. Use it as a checklist of topics.

**Check yourself**

- How does restoring healthy sections within 5 minutes change SAIDI?
- After a transformer differential trip, what does the 86 lockout relay do? Why doesn't the breaker reclose?

---

## Part 5. DER, IEEE 1547, and the PV "backfeed" question (item 54)

All local text copies. These are the sources behind the item 54 findings.

1. [nrel_islanding_primer.txt](web_sources/text/nrel_islanding_primer.txt):
   - pp.9-10: what an island is
   - p.14: the 2 s rule and the 5 min return-to-service delay
   - p.21: worker safety
   - pp.23-25: out-of-phase reclosing, and the fixes
2. [nrel_gfm_roadmap.txt](web_sources/text/nrel_gfm_roadmap.txt):
   - p.13: why grid-following PV cannot hold an island
   - pp.21-22: grid-forming vs grid-following
3. [pnnl_nreca_1547_vartanian.txt](web_sources/text/pnnl_nreca_1547_vartanian.txt):
   - slides 11-13: intentional islands
   - slides 26-27: rules for an island leaving the grid
4. [nrel_borrego_springs.txt](web_sources/text/nrel_borrego_springs.txt):
   - slides 5-7: real outages carried by a microgrid
   - slide 15: which source held voltage and frequency
   - slide 18: an SEL RTAC used as a microgrid controller in testing

**Check yourself**

- Under default 1547 settings, what does the PV do when the upstream recloser opens?
- Besides PV, what would the trainer's DER need in order to pick up a stranded section?

---

## Part 6. Fault indicators (the junction box and pad-mount LEDs)

- Local: [sel_linam_ugfi.txt](web_sources/text/sel_linam_ugfi.txt).
  Online: <https://selinc.com/products/LINAM-UGFI/>
- This is the real device the enclosure LEDs would imitate. The sentence listing where it gets installed
  (pad-mounted transformers, switchgear, sectionalizing cabinets, junction boxes) is near the bottom of the text
  file, under "embedded page data."

**Check yourself**

- Without DA, how does a crew use these indicators to find an underground fault?

---

## Notes

- control.com (the HTML edition of Kuphaldt) and eaton.com blocked automated link checks. The Kuphaldt links above go
  to the ibiblio PDF instead, and Eaton's recloser page was left out.
- The IEEE 1547-2018 standard itself is paywalled and was not read. The Part 5 sources quote it.
