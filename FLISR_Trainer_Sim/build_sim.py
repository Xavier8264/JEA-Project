"""
build_sim.py - builds a FLISR Trainer test bench page for one sketch.

Reads the three ground-truth files named in the sketch header and writes one
self-contained HTML page:

  <sketch>/<sketch>.ino                        config + tables (extracted, not retyped)
  Cardboard Layout REV1 backup_9.12.20.dxf     board drawing, button positions
  JEA Cardboard Prototype Tabulated REV1.xlsx  node, element, fault and LED run coordinates

Each sketch's logic is ported by hand (firmware.js, firmware_rev1.js). This
script hashes the logic section of the .ino and refuses to build if it no
longer matches the hash that port was written against.

Usage:  python build_sim.py                          (FLISR_Trainer)
        python build_sim.py --sketch FLISR_Trainer_REV1
"""

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime
from pathlib import Path

import ezdxf
from ezdxf import path as dxfpath
import openpyxl

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
DXF = PROJECT / "Cardboard Layout REV1 backup_9.12.20.dxf"
XLSX = PROJECT / "JEA Cardboard Prototype Tabulated REV1.xlsx"
TEMPLATE = HERE / "sim_template.html"

SKETCHES = {
    "FLISR_Trainer":      {"port": "firmware.js",      "out": "FLISR_Trainer_Sim.html",
                           "cfg": "sim_config.json",      "title": "FLISR Trainer Test Bench"},
    "FLISR_Trainer_REV1": {"port": "firmware_rev1.js", "out": "FLISR_Trainer_REV1_Sim.html",
                           "cfg": "sim_config_rev1.json", "title": "FLISR Trainer REV1 Test Bench"},
}
INO = FIRMWARE = OUT = CFG_OUT = None       # set from --sketch in main()
TITLE = ""

LOGIC_MARKER = "NOTHING BELOW HERE NEEDS EDITING"
BOARD_IN = 48.0
PITCH_IN = (1000.0 / 60.0) / 25.4       # 60 LED/m, per the .ino header
HIDDEN_OFFSET_IN = 0.45                 # display offset for under-board runs
DEVICE_LED_OFFSET_IN = (0.75, 0.60)     # display offset from element point
UNO_ANALOG = {f"A{i}": 14 + i for i in range(6)}

warnings = []
checks = []


def warn(msg):
    warnings.append(msg)
    print("[!] " + msg)


def ok(msg):
    checks.append(msg)
    print("[OK] " + msg)


def fail(msg):
    print("[X] " + msg)
    sys.exit(1)


# --------------------------------------------------------------------------
# .ino
# --------------------------------------------------------------------------
def normalize(text):
    return "\n".join(l.rstrip() for l in text.replace("\r\n", "\n").split("\n"))


def int_literal(tok):
    tok = tok.strip()
    m = re.fullmatch(r"(0[xX][0-9a-fA-F]+|\d+)[uUlL]*", tok)
    if not m:
        raise ValueError(tok)
    return int(m.group(1), 0)


def strip_comments(src):
    src = re.sub(r"/\*.*?\*/", " ", src, flags=re.S)
    src = re.sub(r"/\*.*\Z", " ", src, flags=re.S)       # unterminated tail
    return re.sub(r"//[^\n]*", "", src)


def parse_ino():
    raw = INO.read_text(encoding="utf-8")
    cut = raw.find(LOGIC_MARKER)
    if cut < 0:
        fail(f"marker '{LOGIC_MARKER}' not found in {INO.name}")
    config_src, logic_src = raw[:cut], raw[cut:]
    logic_sha = hashlib.sha256(normalize(logic_src).encode("utf-8")).hexdigest()

    defines, pin_labels = {}, {}
    stack = []                                  # one entry per open #if
    body = []

    def active():
        return stack[-1]["on"] if stack else True

    def value(tok):
        tok = tok.strip()
        m = re.fullmatch(r"CRGB\(\s*([^,]+),\s*([^,]+),\s*([^)]+)\)", tok)
        if m:
            return [int_literal(x) for x in m.groups()]
        try:
            return int_literal(tok)
        except ValueError:
            pass
        if tok in UNO_ANALOG:
            return UNO_ANALOG[tok]
        if tok in defines:
            return defines[tok]
        if re.fullmatch(r"[A-Za-z_]\w*", tok):
            return tok
        fail(f"cannot read #define value '{tok}'")

    def cond(expr):
        expr = expr.strip()
        m = re.fullmatch(r"(\w+)\s*(==|!=)\s*(\w+)", expr)
        if m:
            a, op, b = defines.get(m.group(1), 0), m.group(2), value(m.group(3))
            return (a == b) if op == "==" else (a != b)
        m = re.fullmatch(r"(!?)\s*(\w+)", expr)
        if m:
            v = bool(defines.get(m.group(2), 0))
            return (not v) if m.group(1) else v
        fail(f"cannot evaluate #if {expr}")

    for line in strip_comments(config_src).split("\n"):
        s = line.strip()
        if s.startswith("#if"):
            parent = active()
            c = cond(s[3:])
            stack.append({"parent": parent, "cond": c, "on": parent and c})
            continue
        if s.startswith("#else"):
            top = stack[-1]
            top["on"] = top["parent"] and not top["cond"]
            continue
        if s.startswith("#endif"):
            stack.pop()
            continue
        if not active():
            continue
        m = re.match(r"#define\s+(\w+)\s+(.+)$", s)
        if m:
            name, tok = m.group(1), m.group(2).strip()
            defines[name] = value(tok)
            if tok in UNO_ANALOG:
                pin_labels[defines[name]] = tok
            continue
        if s.startswith("#"):
            continue
        body.append(line)

    code = "\n".join(body)
    tables = {}
    for m in re.finditer(r"const\s+uint8_t\s+(\w+)\s*\[\s*(\w+)\s*\]\s*PROGMEM\s*=\s*\{(.*?)\}\s*;",
                         code, flags=re.S):
        name, size_tok, items = m.groups()
        size = value(size_tok)
        vals = [value(x) for x in items.split(",") if x.strip()]
        if len(vals) > size:
            fail(f"{name} has {len(vals)} initializers for size {size}; the sketch would not compile")
        if len(vals) < size:
            warn(f"{name} has {len(vals)} initializers for size {size}; C fills the rest with 0")
            vals += [0] * (size - len(vals))
        tables[name] = vals

    for t in ("SEG_LEN", "SEG_OVER", "SEG_ZONE", "SEG_SPLIT", "SEG_ZONE2"):
        if t not in tables:
            fail(f"table {t} not found in {INO.name}")

    # the documentation table in block [4]: "#  len over from  to  zone  note"
    doc_rows = []
    for m in re.finditer(r"^\s*\*\s+(\d+|J\d+)\s+(\d+)\s+([01])\s+(N\d+)\s+(N\d+)\s+(\S.*?)\s*$",
                         config_src.replace("\r\n", "\n"), flags=re.M):
        doc_rows.append({"id": m.group(1), "len": int(m.group(2)), "over": int(m.group(3)),
                         "from": m.group(4), "to": m.group(5), "note": m.group(6)})

    btn_doc = {m.group(1): (float(m.group(2)), float(m.group(3)))
               for m in re.finditer(r"(FAULT Z\d|FAULT DER|RESET)\s+\(\s*([\d.]+),\s*([\d.]+)\)", config_src)}
    dev_doc = {m.group(1): (m.group(2), float(m.group(3)), float(m.group(4)))
               for m in re.finditer(r"\b([ER]\d)\s+(\w+)\s+\(\s*([\d.]+),\s*([\d.]+)\)", config_src)}

    return {"defines": defines, "tables": tables, "pin_labels": pin_labels, "logic_sha": logic_sha,
            "doc_rows": doc_rows, "btn_doc": btn_doc, "dev_doc": dev_doc}


# --------------------------------------------------------------------------
# xlsx
# --------------------------------------------------------------------------
def parse_xlsx():
    wb = openpyxl.load_workbook(XLSX, data_only=True)

    def rows(sheet):
        it = wb[sheet].iter_rows(values_only=True)
        next(it)
        return [r for r in it if r and r[0] is not None]

    nodes = {r[0]: (float(r[1]), float(r[2])) for r in rows("Node")}
    elements = {r[0]: (float(r[1]), float(r[2])) for r in rows("Element")}
    leds = [{"id": str(r[0]), "len": int(r[1]), "over": int(r[2]), "from": r[3], "to": r[4]}
            for r in rows("LED")]
    faults = {r[0]: (float(r[1]), float(r[2])) for r in rows("Fault")}
    return nodes, elements, leds, faults


# --------------------------------------------------------------------------
# DXF
# --------------------------------------------------------------------------
def r3(v):
    return round(v, 3)


def fy(y):
    return r3(BOARD_IN - y)


def parse_dxf():
    doc = ezdxf.readfile(DXF)
    msp = doc.modelspace()
    ext = doc.header.get("$EXTMAX", (0, 0, 0))
    if abs(ext[0] - BOARD_IN) > 0.01 or abs(ext[1] - BOARD_IN) > 0.01:
        warn(f"DXF $EXTMAX is {ext[0]:.2f} x {ext[1]:.2f}, expected a {BOARD_IN} in board")

    ink, route, fills, circles, texts = [], [], [], [], []
    button_circles, labels, route_segs, boxes = [], [], [], []

    def poly_d(pts, close=False):
        pts = [(r3(p[0]), fy(p[1])) for p in pts]
        if len(pts) < 2:
            return ""
        d = f"M{pts[0][0]} {pts[0][1]}" + "".join(f"L{x} {y}" for x, y in pts[1:])
        return d + ("Z" if close else "")

    for e in msp:
        t, layer = e.dxftype(), e.dxf.layer
        if t == "POINT":
            continue
        if t == "CIRCLE" and layer.endswith("Sketch5"):
            c = e.dxf.center
            button_circles.append((c.x, c.y, e.dxf.radius))
            continue
        if t == "LINE":
            a, b = e.dxf.start, e.dxf.end
            seg = poly_d([a, b])
            if layer.endswith("Sketch3"):
                route.append(seg)
                route_segs.append(((a.x, a.y), (b.x, b.y)))
            else:
                ink.append(seg)
        elif t in ("LWPOLYLINE", "SPLINE"):
            p = dxfpath.make_path(e)
            closed = t == "LWPOLYLINE" and e.closed
            pts = list(p.flattening(0.004))
            ink.append(poly_d(pts, close=closed))
            if closed:
                xs, ys = [q[0] for q in pts], [q[1] for q in pts]
                boxes.append((min(xs), min(ys), max(xs), max(ys)))
        elif t == "CIRCLE":
            c = e.dxf.center
            circles.append([r3(c.x), fy(c.y), r3(e.dxf.radius)])
        elif t == "HATCH":
            for p in dxfpath.from_hatch(e):
                fills.append(poly_d(list(p.flattening(0.004)), close=True))
        elif t == "MTEXT":
            ins, h = e.dxf.insert, e.dxf.char_height
            lines = e.plain_text(split=True)
            texts.append([r3(ins.x), fy(ins.y), r3(h), e.dxf.attachment_point, lines])
            if h >= 0.1:
                labels.append((" ".join(lines).strip(), ins.x, ins.y, h, e.dxf.get("width", 0.0)))
        else:
            warn(f"DXF entity {t} on layer {layer} not drawn")

    return {"ink": "".join(ink), "route": "".join(route), "fill": "".join(fills),
            "circles": circles, "texts": texts}, button_circles, labels, route_segs, boxes


# --------------------------------------------------------------------------
# cross-checks and geometry
# --------------------------------------------------------------------------
def dist_to_segment(p, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return math.dist(p, (ax + t * dx, ay + t * dy))


def main():
    global INO, FIRMWARE, OUT, CFG_OUT, TITLE
    ap = argparse.ArgumentParser(description="Build a FLISR Trainer test bench page.")
    ap.add_argument("--sketch", default="FLISR_Trainer", choices=sorted(SKETCHES))
    args = ap.parse_args()
    sk = SKETCHES[args.sketch]
    INO = PROJECT / args.sketch / f"{args.sketch}.ino"
    FIRMWARE, OUT, CFG_OUT, TITLE = HERE / sk["port"], HERE / sk["out"], HERE / sk["cfg"], sk["title"]
    print(f"building {OUT.name} from {INO.name}\n")

    ino = parse_ino()
    D, T = ino["defines"], ino["tables"]
    nodes, elements, led_sheet, fault_sheet = parse_xlsx()
    drawing, button_circles, labels, route_segs, boxes = parse_dxf()

    # ---- the port must match the logic it was written against ----------
    fw_src = FIRMWARE.read_text(encoding="utf-8")
    m = re.search(r"PORTED_LOGIC_SHA256\s*=\s*'([0-9a-f]+|[^']*)'", fw_src)
    ported = m.group(1) if m else ""
    if ported != ino["logic_sha"]:
        fail(f"The logic section of {INO.name} changed since {FIRMWARE.name} was ported.\n"
             f"    .ino logic sha256 : {ino['logic_sha']}\n"
             f"    port written for  : {ported}\n"
             f"    Update {FIRMWARE.name} to match the new logic, then set PORTED_LOGIC_SHA256.")
    ok(f"{FIRMWARE.name} matches the .ino logic section (sha256 {ino['logic_sha'][:12]})")

    # ---- every define the port reads must exist --------------------------
    used = set(re.findall(r"\bD\.([A-Z][A-Z0-9_]*)", fw_src))
    mode = D.get("DEVICE_LED_MODE")
    skip = ("PIN_DEVG_", "PIN_DEVR_") if mode == 1 else ("PIN_DEV_",)
    missing = sorted(n for n in used if n not in D and not n.startswith(skip))
    if missing:
        fail(f"defines read by {FIRMWARE.name} but not found in the .ino: " + ", ".join(missing))
    missing_t = sorted(n for n in set(re.findall(r"\bT\.([A-Z][A-Z0-9_]*)", fw_src)) if n not in T)
    if missing_t:
        fail(f"tables read by {FIRMWARE.name} but not found in the .ino: " + ", ".join(missing_t))
    ok(f"{len(used)} config values and {len(T)} tables extracted from the .ino")

    nseg = D["NUM_SEGMENTS"]
    total = sum(T["SEG_LEN"])
    if total != D["NUM_LEDS"]:
        warn(f"SEG_LEN sums to {total} but NUM_LEDS is {D['NUM_LEDS']}. The sketch prints a MISMATCH at boot.")
    else:
        ok(f"SEG_LEN sums to NUM_LEDS = {total}")

    # ---- segment rows: .ino doc table vs arrays vs xlsx LED sheet --------
    rows = ino["doc_rows"]
    if len(rows) != nseg:
        fail(f"block [4] documents {len(rows)} runs, NUM_SEGMENTS is {nseg}")
    for s, r in enumerate(rows):
        if r["len"] != T["SEG_LEN"][s] or r["over"] != T["SEG_OVER"][s]:
            warn(f"run {r['id']}: block [4] comment says len {r['len']} over {r['over']}, "
                 f"arrays say len {T['SEG_LEN'][s]} over {T['SEG_OVER'][s]}. Arrays are what runs.")
    sheet = {r["id"]: r for r in led_sheet}
    for r in rows:
        if r["id"].startswith("J"):
            continue
        x = sheet.get(r["id"])
        if not x:
            fail(f"run {r['id']} is in the .ino but not in the xlsx LED sheet")
        if (x["from"], x["to"]) != (r["from"], r["to"]):
            fail(f"run {r['id']}: .ino says {r['from']}->{r['to']}, xlsx says {x['from']}->{x['to']}")
        if (x["len"], x["over"]) != (r["len"], r["over"]):
            warn(f"run {r['id']}: xlsx LED sheet says len {x['len']} over {x['over']}, .ino says "
                 f"len {r['len']} over {r['over']}")
    ok(f"{nseg} runs agree on From/To between the .ino and the xlsx LED sheet")

    for nid in {r["from"] for r in rows} | {r["to"] for r in rows}:
        if nid not in nodes:
            fail(f"node {nid} used by the segment table is not in the xlsx Node sheet")

    # DXF route lines stop at the edge of a device symbol, so a node inside a
    # small closed box (a symbol) counts as on the route.
    far_nodes, in_symbol = [], []
    for nid in sorted({r[k] for r in rows if r["over"] for k in ("from", "to")}, key=lambda n: int(n[1:])):
        x, y = nodes[nid]
        d = min(dist_to_segment((x, y), a, b) for a, b in route_segs)
        if d <= 0.15:
            continue
        if any(bx0 <= x <= bx1 and by0 <= y <= by1 and bx1 - bx0 < 2 and by1 - by0 < 2
               for bx0, by0, bx1, by1 in boxes):
            in_symbol.append(nid)
        else:
            far_nodes.append(f"{nid} {d:.2f} in")
    if far_nodes:
        warn("visible-run nodes more than 0.15 in from any DXF route line: " + ", ".join(far_nodes))
    else:
        extra = f" ({', '.join(in_symbol)} inside a DXF device symbol)" if in_symbol else ""
        ok("every visible-run node sits on a DXF route line" + extra)

    # ---- pixel positions ------------------------------------------------
    pixels, runs = [], []
    for s, r in enumerate(rows):
        n = T["SEG_LEN"][s]
        a, b = nodes[r["from"]], nodes[r["to"]]
        over = T["SEG_OVER"][s]
        if s == 0 and T["SEG_SPLIT"][0]:
            # NOTE on run 1 in the .ino: the strip begins SEG_SPLIT[0] px south
            # of N1 inside Substation A, runs north through N1 and on to N2.
            lead = T["SEG_SPLIT"][0]
            start = (a[0], a[1] - lead * PITCH_IN)
            pieces = [(start, a, lead), (a, b, n - lead)]
        else:
            pieces = [(a, b, n)]

        run_pieces = []
        for pa, pb, k in pieces:
            dx, dy = pb[0] - pa[0], pb[1] - pa[1]
            L = math.hypot(dx, dy) or 1.0
            ox, oy = (0.0, 0.0) if over else (-dy / L * HIDDEN_OFFSET_IN, dx / L * HIDDEN_OFFSET_IN)
            ang = r3(-math.degrees(math.atan2(dy, dx)))
            run_pieces.append([r3(pa[0] + ox), fy(pa[1] + oy), r3(pb[0] + ox), fy(pb[1] + oy)])
            for i in range(k):
                t = (i + 0.5) / k
                pixels.append([r3(pa[0] + dx * t + ox), fy(pa[1] + dy * t + oy), s, ang])
        runs.append({"id": r["id"], "from": r["from"], "to": r["to"], "note": r["note"],
                     "over": over, "pieces": run_pieces})
    if len(pixels) != total:
        fail(f"placed {len(pixels)} pixels, table holds {total}")
    ok(f"placed {len(pixels)} pixels along the LED sheet runs")

    # ---- buttons: DXF Sketch5 circles, named by the nearest label ---------
    btn_defs = [("FAULT Z1", "PIN_BTN_FAULT_Z1"), ("FAULT Z2", "PIN_BTN_FAULT_Z2"),
                ("FAULT Z3", "PIN_BTN_FAULT_Z3"), ("FAULT Z4", "PIN_BTN_FAULT_Z4"),
                ("FAULT Z5", "PIN_BTN_FAULT_Z5"), ("FAULT Z6", "PIN_BTN_FAULT_Z6"),
                ("FAULT DER", "PIN_BTN_FAULT_DER"), ("RESET", "PIN_BTN_RESET")]
    names = {n for n, _ in btn_defs}
    cand = [l for l in labels if l[0] in names]
    buttons = []
    used_labels = set()
    for cx, cy, rad in button_circles:
        best = min(cand, key=lambda l: math.dist((cx, cy), (l[1] + l[4] / 2, l[2] - l[3] / 2)))
        if best[0] in used_labels:
            fail(f"two DXF button circles match the label '{best[0]}'")
        used_labels.add(best[0])
        buttons.append((best[0], cx, cy, rad))
    if used_labels != names:
        fail(f"DXF buttons found for {sorted(used_labels)}, expected {sorted(names)}")
    order = {n: i for i, (n, _) in enumerate(btn_defs)}
    buttons.sort(key=lambda b: order[b[0]])
    btn_out = []
    for (label, cx, cy, rad), (_, define) in zip(buttons, btn_defs):
        doc = ino["btn_doc"].get(label)
        if doc and math.dist(doc, (cx, cy)) > 0.05:
            warn(f"{label}: .ino header says {doc}, DXF circle is at ({cx:.2f}, {cy:.2f})")
        btn_out.append({"label": label, "pin": D[define], "define": define,
                        "x": r3(cx), "y": fy(cy), "r": r3(rad)})
    ok("8 buttons found in the DXF and matched to their pins")

    # ---- device LEDs: Element sheet positions, names from block [2] ------
    dev_order = ["SUB_A_BKR", "DEV_A1", "DEV_A2", "TIE", "DEV_B2", "DEV_B1", "SUB_B_BKR", "DER_PCC"]
    by_name = {v[0]: (eid, v[1], v[2]) for eid, v in ino["dev_doc"].items()}
    devices = []
    for d, name in enumerate(dev_order):
        if name not in by_name:
            fail(f"device {name} not listed in block [2] of the .ino")
        eid, dx_, dy_ = by_name[name]
        if eid not in elements:
            fail(f"element {eid} ({name}) not in the xlsx Element sheet")
        ex, ey = elements[eid]
        if math.dist((ex, ey), (dx_, dy_)) > 0.02:
            warn(f"{eid} {name}: .ino says ({dx_}, {dy_}), xlsx Element sheet says ({ex}, {ey})")
        if mode == 1:
            pins = [D["PIN_DEV_" + name]]
        else:
            pins = [D["PIN_DEVG_" + name], D["PIN_DEVR_" + name]]
        devices.append({"name": name, "element": eid, "pins": pins,
                        "ex": r3(ex), "ey": fy(ey),
                        "x": r3(ex + DEVICE_LED_OFFSET_IN[0]), "y": fy(ey + DEVICE_LED_OFFSET_IN[1])})
    ok("8 device LEDs placed at their Element sheet positions")

    # ---- REV1 animation tables (only when the sketch has them) ------------
    run_start = [sum(T["SEG_LEN"][:s]) for s in range(nseg)]
    if "SEG_FROM" in T:
        for s, r in enumerate(rows):
            have = (T["SEG_FROM"][s], T["SEG_TO"][s])
            if have != (int(r["from"][1:]), int(r["to"][1:])):
                fail(f"run {r['id']}: SEG_FROM/SEG_TO say N{have[0]} -> N{have[1]}, "
                     f"block [4] says {r['from']} -> {r['to']}")
        if max(T["SEG_FROM"] + T["SEG_TO"]) >= D["NUM_NODES"]:
            fail("SEG_FROM / SEG_TO use a node number >= NUM_NODES")
        ok("SEG_FROM / SEG_TO match the From and To node of every run")
    if "TAP_SEG" in T:
        for t in range(D["NUM_TAPS"]):
            s, px, nid = T["TAP_SEG"][t], T["TAP_PX"][t], f"N{T['TAP_NODE'][t]}"
            r, n = rows[s], T["SEG_LEN"][s]
            a, b = nodes[r["from"]], nodes[r["to"]]
            off = dist_to_segment(nodes[nid], a, b)
            along = math.dist(a, nodes[nid]) / math.dist(a, b) * n
            if off > 0.1 or not (0 < px < n) or abs(along - px) > 0.5:
                fail(f"tap {nid}: {off:.2f} in off run {r['id']}, {along:.2f} px along it, TAP_PX is {px}")
            ok(f"tap {nid} sits {along:.2f} px along run {r['id']}, so TAP_PX {px} is right")
    if "TIE_NODE" in D:
        eid = by_name["TIE"][0]
        tie_node = f"N{D['TIE_NODE']}"
        d = math.dist(nodes[tie_node], elements[eid])
        if d > 0.05:
            fail(f"TIE_NODE {tie_node} is {d:.2f} in from {eid} TIE")
        ok(f"TIE_NODE {tie_node} is the {eid} TIE location")
    if "FAULT_SEG" in T:
        names = ["Fault Z1", "Fault Z2", "Fault Z3", "Fault Z4", "Fault Z5", "Fault Z6", "Fault DER"]
        zones = [D["ZN_Z1"], D["ZN_Z2"], D["ZN_Z3"], D["ZN_Z4"], D["ZN_Z5"], D["ZN_Z6"], D["ZN_DER"]]
        visible = [(i, p) for i, p in enumerate(pixels) if T["SEG_OVER"][p[2]]]
        for f, name in enumerate(names):
            if name not in fault_sheet:
                fail(f"'{name}' is not in the xlsx Fault sheet")
            s, px = T["FAULT_SEG"][f], T["FAULT_PX"][f]
            if not T["SEG_OVER"][s] or px >= T["SEG_LEN"][s]:
                fail(f"{name}: FAULT_SEG {s} / FAULT_PX {px} is not a visible pixel")
            dists = {i: math.dist(fault_sheet[name], (p[0], BOARD_IN - p[1])) for i, p in visible}
            best = min(dists, key=dists.get)
            if dists[run_start[s] + px] > dists[best] + 0.02:
                bs = pixels[best][2]
                fail(f"{name}: nearest pixel is run {rows[bs]['id']} pixel {best - run_start[bs]}, "
                     f"the table says run {rows[s]['id']} pixel {px}")
            split = T["SEG_SPLIT"][s]
            zone = T["SEG_ZONE2"][s] if split and px >= split else T["SEG_ZONE"][s]
            if zone != zones[f]:
                fail(f"{name}: run {rows[s]['id']} pixel {px} is in zone code {zone}, expected {zones[f]}")
        ok("7 fault locations are the pixel nearest their Fault sheet point, in the right zone")

    # ---- pin labels -----------------------------------------------------
    labels_out = {}
    for p in [b["pin"] for b in btn_out] + [p for dv in devices for p in dv["pins"]] + [D["LED_DATA_PIN"]]:
        labels_out[str(p)] = ino["pin_labels"].get(p, f"D{p}")

    cfg = {"defines": D, "tables": T}
    geom = {"board": BOARD_IN, "pitch": r3(PITCH_IN), "drawing": drawing, "pixels": pixels, "runs": runs,
            "buttons": btn_out, "devices": devices, "pinLabels": labels_out}
    meta = {"built": datetime.now().strftime("%Y-%m-%d %H:%M"), "title": TITLE,
            "ino": INO.name, "dxf": DXF.name, "xlsx": XLSX.name,
            "logicSha": ino["logic_sha"], "checks": checks, "warnings": warnings}

    def js(name, obj):                  # safe inside a <script> element
        return f"const {name} = " + json.dumps(obj, separators=(",", ":")).replace("</", "<\\/") + ";"

    html = TEMPLATE.read_text(encoding="utf-8")
    for token, payload in (("{{TITLE}}", TITLE), ("{{SKETCH}}", INO.name)):
        if token not in html:
            fail(f"template must contain {token}")
        html = html.replace(token, payload)
    for token, payload in (("/*__CFG__*/", js("CFG", cfg)),
                           ("/*__GEOM__*/", js("GEOM", geom)),
                           ("/*__META__*/", js("META", meta)),
                           ("/*__FIRMWARE__*/", fw_src)):
        if html.count(token) != 1:
            fail(f"template must contain {token} exactly once")
        html = html.replace(token, payload)
    OUT.write_text(html, encoding="utf-8")

    CFG_OUT.write_text(json.dumps(cfg, indent=1), encoding="utf-8")
    print(f"\nwrote {OUT.name} ({len(html) / 1024:.0f} KB) and {CFG_OUT.name}")
    print(f"{len(checks)} checks passed, {len(warnings)} warnings")


if __name__ == "__main__":
    main()
