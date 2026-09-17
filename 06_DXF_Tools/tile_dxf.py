"""
tile_dxf.py - Split a 2D DXF into 8.5 x 11 in tiles and emit a multi-page PDF
for full-scale (1:1) printing.

Sheets are rendered at true model position across the ENTIRE sheet. Nothing is
inset, blanked, scaled or reflowed for printer margins. The grid pitch is the
full sheet size, so printed sheets butt edge to edge with no overlap and no
trimming. Whatever falls inside the printer physical unprintable border is
clipped by the printer; the advisory loss report says how much that is.

Usage:
    python tile_dxf.py INPUT.dxf [-o OUTPUT.pdf] [--units in|mm|auto]
                       [--sheet 8.5x11] [--dry-run]
"""

import argparse
import math
import os
import sys
from collections import Counter

import numpy as np
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.collections import LineCollection

import ezdxf
from ezdxf import disassemble, path as ezpath


# ============================== CONFIG ==============================

SHEET_W = 8.5                  # inches, portrait
SHEET_H = 11.0
DXF_UNITS = "auto"             # "auto" | "in" | "mm"
SAFE_INSET = 0.25              # annotation keepout from sheet edge, geometry only
FLATTEN_TOL = 0.005            # inches, arc/spline chord tolerance
LINE_WIDTH = 0.5               # points
ASSUMED_UNPRINTABLE = 0.12     # advisory only, used in the loss report

# ====================================================================

# Entities that carry no fabrication linework we can flatten reliably.
# NOTE: ezdxf >= 1.4 make_path() will accept HATCH, but it returns only the
# FIRST boundary path, so a multi-boundary hatch would be silently truncated.
# HATCH is skipped by policy and reported, never silently dropped.
SKIP_TYPES = frozenset(
    {"TEXT", "MTEXT", "HATCH", "DIMENSION", "POINT", "ATTRIB", "ATTDEF", "LEADER"}
)

# Guard against a user matplotlibrc that would silently rescale the output.
plt.rcParams["savefig.bbox"] = "standard"
plt.rcParams["savefig.pad_inches"] = 0.0
plt.rcParams["figure.autolayout"] = False

# Matplotlib decimates any path with >= 128 vertices using a display-dpi based
# threshold, which silently drops vertices from long flattened splines. Measured
# on the reference drawing that cost up to 0.0013 in of shape fidelity. The only
# accuracy knob here must be FLATTEN_TOL, so turn the hidden second stage off.
plt.rcParams["path.simplify"] = False

EPS = 1e-9          # float slack for tile-count rounding
PARTIAL_EPS = 1e-6  # below this a "partial" tile is really a full tile

INSUNITS_TO_INCH = {1: 1.0, 4: 1.0 / 25.4}
INSUNITS_NAME = {1: "inches", 4: "millimeters"}


# ------------------------------- grid naming -------------------------------

def col_label(index):
    """0 -> A, 25 -> Z, 26 -> AA, 27 -> AB (bijective base 26)."""
    out = ""
    n = index + 1
    while n > 0:
        n, rem = divmod(n - 1, 26)
        out = chr(ord("A") + rem) + out
    return out


def n_tiles(extent, pitch):
    """Tile count with float slack, so 44.0000000001 in does not add a sliver page."""
    return max(1, int(math.ceil(extent / pitch - EPS)))


# ------------------------------- geometry ----------------------------------

def load_geometry(doc, tol):
    """
    Flatten every renderable modelspace entity ONCE into world-coordinate
    polylines. Returns (polylines, skipped_counter, kept_counter).

    polylines: list of (N, 2) float arrays, N >= 2, in raw DXF units.
    """
    msp = doc.modelspace()
    polylines = []
    skipped = Counter()
    kept = Counter()

    for entity in disassemble.recursive_decompose(msp):
        etype = entity.dxftype()
        if etype in SKIP_TYPES:
            skipped[etype] += 1
            continue
        try:
            p = ezpath.make_path(entity)
        except (TypeError, ValueError) as exc:
            skipped["%s (%s)" % (etype, type(exc).__name__)] += 1
            continue

        subs = p.sub_paths() if hasattr(p, "sub_paths") else [p]
        added = 0
        for sub in subs:
            verts = [(v.x, v.y) for v in sub.flattening(tol)]
            if len(verts) < 2:
                continue
            polylines.append(np.asarray(verts, dtype=float))
            added += 1
        if added:
            kept[etype] += 1
        else:
            skipped["%s (degenerate)" % etype] += 1

    return polylines, skipped, kept


def scale_polylines(polylines, factor):
    if factor == 1.0:
        return polylines
    return [p * factor for p in polylines]


def compute_bbox(polylines):
    if not polylines:
        return None
    mins = np.array([p.min(axis=0) for p in polylines]).min(axis=0)
    maxs = np.array([p.max(axis=0) for p in polylines]).max(axis=0)
    return float(mins[0]), float(mins[1]), float(maxs[0]), float(maxs[1])


def to_segments(polylines):
    """Explode polylines into an (M, 4) array of x0, y0, x1, y1 segments."""
    chunks = [np.hstack([p[:-1], p[1:]]) for p in polylines]
    if not chunks:
        return np.zeros((0, 4), dtype=float)
    return np.vstack(chunks)


# ------------------------------- units -------------------------------------

def resolve_units(doc, cli_units, bbox_raw):
    """
    Returns (scale factor converting raw DXF units to inches, description).
    Exits with a loud warning if units are unresolvable.
    """
    if cli_units in ("in", "mm"):
        factor = 1.0 if cli_units == "in" else 1.0 / 25.4
        return factor, "forced by --units %s" % cli_units

    insunits = doc.header.get("$INSUNITS", 0)
    if insunits in INSUNITS_TO_INCH:
        return (
            INSUNITS_TO_INCH[insunits],
            "$INSUNITS=%d (%s)" % (insunits, INSUNITS_NAME[insunits]),
        )

    x0, y0, x1, y1 = bbox_raw
    print("")
    print("!" * 70)
    print("[!] CANNOT RESOLVE DRAWING UNITS")
    print("!" * 70)
    if insunits == 0:
        print("[!] $INSUNITS is 0 (unitless) or unset in this DXF.")
    else:
        print("[!] $INSUNITS is %d, which this tool does not map." % insunits)
        print("[!] Only 1 (inches) and 4 (millimeters) are handled.")
    print("[!] Raw bounding box, in UNKNOWN units:")
    print("[!]     min  = (%.6f, %.6f)" % (x0, y0))
    print("[!]     max  = (%.6f, %.6f)" % (x1, y1))
    print("[!]     size = %.6f wide x %.6f tall" % (x1 - x0, y1 - y0))
    print("[!]")
    print("[!] A wrong unit guess silently destroys 1:1 scale, so this tool")
    print("[!] will not guess. Re-run with an explicit unit:")
    print("[!]     --units in     (raw numbers above are inches)")
    print("[!]     --units mm     (raw numbers above are millimeters)")
    print("!" * 70)
    sys.exit(2)


# ------------------------------- grid --------------------------------------

class Grid(object):
    """Page grid whose pitch is the FULL sheet size. Origin = bbox min corner."""

    def __init__(self, bbox, sheet_w, sheet_h):
        self.x0, self.y0, self.x1, self.y1 = bbox
        self.sheet_w = sheet_w
        self.sheet_h = sheet_h
        self.width = self.x1 - self.x0
        self.height = self.y1 - self.y0
        self.n_cols = n_tiles(self.width, sheet_w)
        self.n_rows = n_tiles(self.height, sheet_h)

        # Kept (in-model) size of the final column / row.
        self.last_col_keep = self.width - (self.n_cols - 1) * sheet_w
        self.last_row_keep = self.height - (self.n_rows - 1) * sheet_h
        self.col_partial = self.last_col_keep < sheet_w - PARTIAL_EPS
        self.row_partial = self.last_row_keep < sheet_h - PARTIAL_EPS

    @property
    def n_pages(self):
        return self.n_cols * self.n_rows

    def page_origin(self, col, row):
        """Model coords of the sheet bottom-left corner."""
        return self.x0 + col * self.sheet_w, self.y0 + row * self.sheet_h

    def page_id(self, col, row):
        return "%s%d" % (col_label(col), row + 1)

    def is_last_col(self, col):
        return col == self.n_cols - 1 and self.col_partial

    def is_last_row(self, row):
        return row == self.n_rows - 1 and self.row_partial

    def keep_size(self, col, row):
        """How much of this sheet is real model content, in inches."""
        kw = self.last_col_keep if self.is_last_col(col) else self.sheet_w
        kh = self.last_row_keep if self.is_last_row(row) else self.sheet_h
        return kw, kh

    def pages(self):
        """Bottom row first, left to right within each row."""
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                yield col, row

    def col_widths(self):
        return [
            self.last_col_keep if c == self.n_cols - 1 else self.sheet_w
            for c in range(self.n_cols)
        ]

    def row_heights(self):
        return [
            self.last_row_keep if r == self.n_rows - 1 else self.sheet_h
            for r in range(self.n_rows)
        ]

    def n_partial(self):
        n = 0
        for col, row in self.pages():
            kw, kh = self.keep_size(col, row)
            if kw < self.sheet_w - PARTIAL_EPS or kh < self.sheet_h - PARTIAL_EPS:
                n += 1
        return n


# ------------------------------- clipping ----------------------------------

def clip_segments_to_rect(segs, xmin, ymin, xmax, ymax):
    """
    Liang-Barsky clip of an (M, 4) segment array to a rectangle.
    Returns the clipped (K, 4) array. Vectorized over all segments.
    """
    if segs.shape[0] == 0:
        return segs

    x0, y0, x1, y1 = segs[:, 0], segs[:, 1], segs[:, 2], segs[:, 3]
    dx = x1 - x0
    dy = y1 - y0

    t0 = np.zeros(segs.shape[0])
    t1 = np.ones(segs.shape[0])
    alive = np.ones(segs.shape[0], dtype=bool)

    for p, q in ((-dx, x0 - xmin), (dx, xmax - x0), (-dy, y0 - ymin), (dy, ymax - y0)):
        parallel = p == 0
        # Parallel to this edge and outside the slab -> reject outright.
        alive &= ~(parallel & (q < 0))

        with np.errstate(divide="ignore", invalid="ignore"):
            r = np.where(parallel, 0.0, q / np.where(parallel, 1.0, p))

        entering = (~parallel) & (p < 0)
        leaving = (~parallel) & (p > 0)
        t0 = np.where(entering, np.maximum(t0, r), t0)
        t1 = np.where(leaving, np.minimum(t1, r), t1)
        alive &= t0 <= t1

    if not alive.any():
        return np.zeros((0, 4), dtype=float)

    a = alive
    out = np.empty((int(a.sum()), 4), dtype=float)
    out[:, 0] = x0[a] + dx[a] * t0[a]
    out[:, 1] = y0[a] + dy[a] * t0[a]
    out[:, 2] = x0[a] + dx[a] * t1[a]
    out[:, 3] = y0[a] + dy[a] * t1[a]
    return out


def segment_length(segs):
    if segs.shape[0] == 0:
        return 0.0
    return float(np.hypot(segs[:, 2] - segs[:, 0], segs[:, 3] - segs[:, 1]).sum())


# ------------------------------- page drawing ------------------------------

def new_sheet(sheet_w, sheet_h, x0, y0):
    """
    Exact 1:1 sheet: axes fill the whole figure and the data range equals the
    sheet size in inches, so one data inch is exactly one figure inch.
    Never autoscale / tight_layout / bbox_inches='tight' on this figure.
    """
    fig = plt.figure(figsize=(sheet_w, sheet_h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(x0, x0 + sheet_w)
    ax.set_ylim(y0, y0 + sheet_h)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def draw_page(pdf, grid, polylines, page_index, total_pages, source_name, args):
    col, row = page_index
    px, py = grid.page_origin(col, row)
    sw, sh = grid.sheet_w, grid.sheet_h
    pid = grid.page_id(col, row)

    fig, ax = new_sheet(sw, sh, px, py)

    # --- geometry: one LineCollection, clipped at the sheet boundary --------
    if polylines:
        lc = LineCollection(
            polylines,
            linewidths=LINE_WIDTH,
            colors="black",
            capstyle="round",
            joinstyle="round",
            clip_on=True,
            zorder=1,
        )
        ax.add_collection(lc)

    # --- annotation frame: inside the safe inset AND inside the keep region -
    keep_w, keep_h = grid.keep_size(col, row)
    ann_x0 = px + SAFE_INSET
    ann_y0 = py + SAFE_INSET
    ann_x1 = px + min(sw, keep_w) - SAFE_INSET
    ann_y1 = py + min(sh, keep_h) - SAFE_INSET
    mid_x = 0.5 * (ann_x0 + ann_x1)
    mid_y = 0.5 * (ann_y0 + ann_y1)
    room = ann_x1 > ann_x0 and ann_y1 > ann_y0

    # --- cut lines on partial pages, drawn above geometry -------------------
    # Cut text runs along the KEEP extent, not the sheet extent. On the corner
    # page both keeps are short, so sheet-fraction placement would drop these
    # labels past the other cut line and they would be thrown away.
    def clamp(v, lo, hi):
        return min(max(v, lo), hi)

    if grid.is_last_col(col):
        x_cut = px + grid.last_col_keep
        ax.plot(
            [x_cut, x_cut], [py, py + sh],
            linestyle=(0, (6, 4)), linewidth=0.75, color="black",
            clip_on=False, zorder=4,
        )
        tx = max(x_cut - 0.10, px + 0.08)
        span = min(sh, keep_h)
        ax.text(tx, clamp(py + span * 0.33, ann_y0, ann_y1), "CUT",
                rotation=90, fontsize=7, ha="right", va="center",
                color="black", zorder=7)
        ax.text(tx, clamp(py + span * 0.66, ann_y0, ann_y1),
                "CUT AT %.3f in" % grid.last_col_keep, rotation=90,
                fontsize=6.5, ha="right", va="center", color="black", zorder=7)

    if grid.is_last_row(row):
        y_cut = py + grid.last_row_keep
        ax.plot(
            [px, px + sw], [y_cut, y_cut],
            linestyle=(0, (6, 4)), linewidth=0.75, color="black",
            clip_on=False, zorder=4,
        )
        ty = max(y_cut - 0.10, py + 0.08)
        span = min(sw, keep_w)
        ax.text(clamp(px + span * 0.33, ann_x0, ann_x1), ty, "CUT",
                rotation=0, fontsize=7, ha="center", va="top",
                color="black", zorder=7)
        ax.text(clamp(px + span * 0.66, ann_x0, ann_x1), ty,
                "CUT AT %.3f in" % grid.last_row_keep, rotation=0,
                fontsize=6.5, ha="center", va="top", color="black", zorder=7)

    # --- annotations, all drawn after geometry ------------------------------
    if room:
        ax.text(ann_x0, ann_y0, pid, fontsize=14,
                fontweight="bold", ha="left", va="bottom", zorder=7)

        if col > 0:
            ax.text(ann_x0, mid_y, "<- %s" % grid.page_id(col - 1, row),
                    fontsize=8, ha="left", va="center", zorder=7)
        if col < grid.n_cols - 1:
            ax.text(ann_x1, mid_y, "%s ->" % grid.page_id(col + 1, row),
                    fontsize=8, ha="right", va="center", zorder=7)
        if row < grid.n_rows - 1:
            ax.text(mid_x, ann_y1, "%s ^" % grid.page_id(col, row + 1),
                    fontsize=8, ha="center", va="top", zorder=7)
        if row > 0:
            ax.text(mid_x, ann_y0, "%s v" % grid.page_id(col, row - 1),
                    fontsize=8, ha="center", va="bottom", zorder=7)

        ax.text(ann_x1, ann_y0 + 0.18,
                "%s   page %d of %d" % (source_name, page_index_num(grid, col, row) + 1,
                                        total_pages),
                fontsize=5.5, ha="right", va="bottom", color="0.25", zorder=7)

    pdf.savefig(fig)
    plt.close(fig)


def page_index_num(grid, col, row):
    """Sequential position of this page in the PDF, index page excluded."""
    return row * grid.n_cols + col + 1  # +1 because the index page is page 1


# ------------------------------- index page --------------------------------

def draw_index_page(pdf, grid, polylines, source_name, total_pages, unit_note):
    fig, ax = new_sheet(SHEET_W, SHEET_H, 0.0, 0.0)

    ax.text(SHEET_W / 2.0, 10.62, "TILED FULL-SCALE TEMPLATE - ASSEMBLY INDEX",
            fontsize=13, fontweight="bold", ha="center", va="center")
    ax.text(SHEET_W / 2.0, 10.40, source_name, fontsize=7.5, ha="center",
            va="center", color="0.25")

    # ---- overview: model scaled to fit, with the page grid overlaid --------
    ov_x0, ov_y0, ov_x1, ov_y1 = 0.45, 4.70, 8.05, 10.22
    grid_w = grid.n_cols * grid.sheet_w
    grid_h = grid.n_rows * grid.sheet_h
    s = min((ov_x1 - ov_x0) / grid_w, (ov_y1 - ov_y0) / grid_h)
    off_x = ov_x0 + 0.5 * ((ov_x1 - ov_x0) - grid_w * s)
    off_y = ov_y0 + 0.5 * ((ov_y1 - ov_y0) - grid_h * s)

    def mx(x):
        return off_x + (x - grid.x0) * s

    def my(y):
        return off_y + (y - grid.y0) * s

    if polylines:
        scaled = [np.column_stack([mx(p[:, 0]), my(p[:, 1])]) for p in polylines]
        ax.add_collection(
            LineCollection(scaled, linewidths=0.28, colors="0.15", zorder=2)
        )

    # page cell boundaries
    cell_segs = []
    for c in range(grid.n_cols + 1):
        x = off_x + c * grid.sheet_w * s
        cell_segs.append([(x, off_y), (x, off_y + grid_h * s)])
    for r in range(grid.n_rows + 1):
        y = off_y + r * grid.sheet_h * s
        cell_segs.append([(off_x, y), (off_x + grid_w * s, y)])
    ax.add_collection(
        LineCollection(cell_segs, linewidths=0.5, colors="0.55", zorder=3)
    )

    # model bbox outline
    ax.add_collection(
        LineCollection(
            [[(mx(grid.x0), my(grid.y0)), (mx(grid.x1), my(grid.y0)),
              (mx(grid.x1), my(grid.y1)), (mx(grid.x0), my(grid.y1)),
              (mx(grid.x0), my(grid.y0))]],
            linewidths=0.8, colors="black", linestyles="dashed", zorder=4,
        )
    )

    cell_font = max(3.5, min(9.0, 34.0 * s))
    for col, row in grid.pages():
        cx = off_x + (col + 0.5) * grid.sheet_w * s
        cy = off_y + (row + 0.5) * grid.sheet_h * s
        ax.text(cx, cy, grid.page_id(col, row), fontsize=cell_font,
                fontweight="bold", ha="center", va="center", color="0.55",
                zorder=5)

    ax.text(off_x, off_y - 0.15,
            "Grid overlay: each cell is one printed sheet. Dashed outline = model extents.",
            fontsize=6, ha="left", va="top", color="0.35")

    # ---- 1.000 in calibration square (drawn in true inches) ----------------
    cal_x, cal_y = 0.45, 3.05
    ax.add_collection(
        LineCollection(
            [[(cal_x, cal_y), (cal_x + 1.0, cal_y), (cal_x + 1.0, cal_y + 1.0),
              (cal_x, cal_y + 1.0), (cal_x, cal_y)]],
            linewidths=1.0, colors="black", zorder=4,
        )
    )
    ax.text(cal_x + 0.5, cal_y + 0.5, "1.000 in\nSQUARE", fontsize=6.5,
            ha="center", va="center", linespacing=1.4)
    ax.text(cal_x + 0.5, cal_y - 0.10, "1.000 in", fontsize=6.5, ha="center",
            va="top")
    ax.text(cal_x + 1.10, cal_y + 0.5, "1.000 in", fontsize=6.5, rotation=90,
            ha="left", va="center")
    ax.text(cal_x, cal_y + 1.14,
            "CALIBRATION: measure this square before the full run.",
            fontsize=6.5, fontweight="bold", ha="left", va="bottom")

    # ---- text block --------------------------------------------------------
    tx = 1.85
    ty = 4.05
    lh = 0.170
    lines = [
        ("Model size:  %.3f x %.3f in" % (grid.width, grid.height), True),
        ("Grid:        %d cols (A-%s) x %d rows (1-%d)"
         % (grid.n_cols, col_label(grid.n_cols - 1), grid.n_rows, grid.n_rows), False),
        ("Tile pages:  %d   (plus this index page = %d total)"
         % (grid.n_pages, total_pages), False),
        ("Units:       %s" % unit_note, False),
        ("Partial:     %d of %d pages are partial" % (grid.n_partial(), grid.n_pages),
         False),
    ]
    if grid.col_partial:
        lines.append(("  last column %s kept at %.3f in wide"
                      % (col_label(grid.n_cols - 1), grid.last_col_keep), False))
    else:
        lines.append(("  last column is full width", False))
    if grid.row_partial:
        lines.append(("  last row %d kept at %.3f in tall"
                      % (grid.n_rows, grid.last_row_keep), False))
    else:
        lines.append(("  last row is full height", False))
    lines.append(("Order: A1 is bottom-left. Row 1 is the BOTTOM row.", True))

    for text, bold in lines:
        ax.text(tx, ty, text, fontsize=7.2, family="monospace",
                fontweight="bold" if bold else "normal", ha="left", va="top")
        ty -= lh

    # ---- printing instructions --------------------------------------------
    iy = 2.46
    ax.plot([0.45, 8.05], [2.66, 2.66], linewidth=0.8, color="black")
    ax.text(0.45, iy, "PRINT AT 100% / ACTUAL SIZE", fontsize=11,
            fontweight="bold", ha="left", va="top")
    iy -= 0.32
    for line in [
        "Do NOT use 'Fit to Page'.",
        "Do NOT use 'Shrink to Printable Area' or 'Scale to Fit'.",
        "Do NOT use borderless mode. It enlarges the image 2 to 5 percent",
        "    and destroys 1:1 scale.",
        "Set page size to Letter 8.5 x 11 in, portrait.",
    ]:
        ax.text(0.55, iy, line, fontsize=8.5, fontweight="bold", ha="left", va="top")
        iy -= 0.205

    iy -= 0.10
    for line in [
        "Verify the 1.000 in calibration square above with a ruler before",
        "printing the remaining pages.",
        "Sheets butt edge to edge. Do not overlap and do not trim, except",
        "along the dashed CUT lines on the last column and last row.",
        "Assemble bottom row first: A1, B1, C1 ... then A2, B2, C2 ...",
    ]:
        ax.text(0.55, iy, line, fontsize=7.5, ha="left", va="top", color="0.15")
        iy -= 0.175

    pdf.savefig(fig)
    plt.close(fig)


# ------------------------------- reports -----------------------------------

def print_skip_report(skipped, kept):
    total_kept = sum(kept.values())
    print("[OK] flattened %d entities into renderable paths" % total_kept)
    for etype, n in sorted(kept.items()):
        print("       %-12s %6d" % (etype, n))
    if not skipped:
        print("[OK] no entities skipped")
        return
    total = sum(skipped.values())
    print("")
    print("[!] WARNING: %d entities were SKIPPED and are NOT in the PDF:" % total)
    for etype, n in sorted(skipped.items()):
        print("[!]      %-22s %6d" % (etype, n))
    print("[!] These carry no flattenable outline (text, points, fills, dims).")
    print("[!] If any of them is real fabrication geometry, convert it to")
    print("[!] lines/polylines in CAD and re-run. Do not assume it printed.")


def dry_run_report(grid, source_name, unit_note):
    print("")
    print("=" * 62)
    print("GRID PLAN (dry run, nothing rendered)")
    print("=" * 62)
    print("Source      : %s" % source_name)
    print("Units       : %s" % unit_note)
    print("Model bbox  : (%.4f, %.4f) -> (%.4f, %.4f)"
          % (grid.x0, grid.y0, grid.x1, grid.y1))
    print("Model size  : %.4f x %.4f in" % (grid.width, grid.height))
    print("Sheet       : %.3f x %.3f in (grid pitch = full sheet)"
          % (grid.sheet_w, grid.sheet_h))
    print("Grid        : %d cols x %d rows" % (grid.n_cols, grid.n_rows))
    print("Tile pages  : %d  (+1 index page = %d pages in the PDF)"
          % (grid.n_pages, grid.n_pages + 1))
    print("")
    print("Column widths (left to right):")
    for c, w in enumerate(grid.col_widths()):
        flag = "  <- PARTIAL, cut at %.3f in" % w if w < grid.sheet_w - PARTIAL_EPS else ""
        print("    %-4s %8.3f in%s" % (col_label(c), w, flag))
    print("")
    print("Row heights (bottom to top):")
    for r, h in enumerate(grid.row_heights()):
        flag = "  <- PARTIAL, cut at %.3f in" % h if h < grid.sheet_h - PARTIAL_EPS else ""
        print("    %-4d %8.3f in%s" % (r + 1, h, flag))
    print("")
    print("Partial pages: %d of %d" % (grid.n_partial(), grid.n_pages))
    print("Page order   : index, then A1 B1 C1 ... (bottom row first)")
    print("=" * 62)


def write_manifest(mpath, grid, source_name, unit_note, loss_rows):
    lines = []
    lines.append("TILE MANIFEST")
    lines.append("=" * 72)
    lines.append("Source        : %s" % source_name)
    lines.append("Units         : %s" % unit_note)
    lines.append("Sheet         : %.3f x %.3f in" % (grid.sheet_w, grid.sheet_h))
    lines.append("Model bbox    : (%.4f, %.4f) -> (%.4f, %.4f)"
                 % (grid.x0, grid.y0, grid.x1, grid.y1))
    lines.append("Model size    : %.4f x %.4f in" % (grid.width, grid.height))
    lines.append("Grid          : %d cols x %d rows = %d tile pages"
                 % (grid.n_cols, grid.n_rows, grid.n_pages))
    lines.append("")
    lines.append("SHEET RECT  = model rectangle the printed sheet spans (full pitch).")
    lines.append("COVERED RECT= that rectangle clipped to the model bbox. The COVERED")
    lines.append("              rects tile the bbox exactly: no gaps, no overlap.")
    lines.append("")
    header = ("%-6s %-6s %-37s %-37s %s"
              % ("PAGE", "PDFPG", "SHEET RECT (x0,y0)-(x1,y1)",
                 "COVERED RECT (x0,y0)-(x1,y1)", "KEPT WxH"))
    lines.append(header)
    lines.append("-" * len(header))

    for col, row in grid.pages():
        px, py = grid.page_origin(col, row)
        sx1, sy1 = px + grid.sheet_w, py + grid.sheet_h
        cx1, cy1 = min(sx1, grid.x1), min(sy1, grid.y1)
        kw, kh = grid.keep_size(col, row)
        lines.append(
            "%-6s %-6d (%9.4f,%9.4f)-(%9.4f,%9.4f) (%9.4f,%9.4f)-(%9.4f,%9.4f) %.3f x %.3f"
            % (grid.page_id(col, row), page_index_num(grid, col, row) + 1,
               px, py, sx1, sy1, px, py, cx1, cy1, kw, kh)
        )

    lines.append("")
    lines.append("=" * 72)
    lines.append("ADVISORY LOSS REPORT (informational only)")
    lines.append("=" * 72)
    lines.append("Linework lying within %.3f in of a sheet edge, which a typical"
                 % ASSUMED_UNPRINTABLE)
    lines.append("printer will clip. This is NOT an error: butted sheets lose a thin")
    lines.append("strip at every seam. Corner geometry counts toward two edges.")
    lines.append("")
    hdr2 = "%-6s %10s %10s %10s %10s %10s" % ("PAGE", "LEFT in", "RIGHT in",
                                              "BOTTOM in", "TOP in", "SEGS")
    lines.append(hdr2)
    lines.append("-" * len(hdr2))
    for r in loss_rows:
        if r["total"] <= 0.0:
            continue
        lines.append("%-6s %10.3f %10.3f %10.3f %10.3f %10d"
                     % (r["pid"], r["left"], r["right"], r["bottom"], r["top"],
                        r["segs"]))
    lines.append("")

    with open(mpath, "w", encoding="ascii") as fh:
        fh.write("\n".join(lines) + "\n")
    return mpath


def compute_loss(grid, segments):
    """Length of linework within ASSUMED_UNPRINTABLE of each sheet edge."""
    u = ASSUMED_UNPRINTABLE
    rows = []
    for col, row in grid.pages():
        px, py = grid.page_origin(col, row)
        sw, sh = grid.sheet_w, grid.sheet_h
        onpage = clip_segments_to_rect(segments, px, py, px + sw, py + sh)
        bands = {
            "left": (px, py, px + u, py + sh),
            "right": (px + sw - u, py, px + sw, py + sh),
            "bottom": (px, py, px + sw, py + u),
            "top": (px, py + sh - u, px + sw, py + sh),
        }
        rec = {"pid": grid.page_id(col, row), "segs": 0}
        nseg = 0
        for name, (a, b, c, d) in bands.items():
            clipped = clip_segments_to_rect(onpage, a, b, c, d)
            rec[name] = segment_length(clipped)
            nseg += clipped.shape[0]
        rec["segs"] = nseg
        rec["total"] = rec["left"] + rec["right"] + rec["bottom"] + rec["top"]
        rows.append(rec)
    return rows


def print_loss_summary(rows):
    tot = {k: sum(r[k] for r in rows) for k in ("left", "right", "bottom", "top")}
    nseg = sum(r["segs"] for r in rows)
    grand = sum(tot.values())
    print("")
    print("--- ADVISORY LOSS REPORT (informational) ---")
    print("Linework within %.3f in of a sheet edge, likely clipped by the printer:"
          % ASSUMED_UNPRINTABLE)
    print("    left  %9.3f in     right %9.3f in" % (tot["left"], tot["right"]))
    print("    bottom%9.3f in     top   %9.3f in" % (tot["bottom"], tot["top"]))
    print("    total %9.3f in across %d segment pieces" % (grand, nseg))
    worst = sorted(rows, key=lambda r: -r["total"])[:5]
    worst = [w for w in worst if w["total"] > 0]
    if worst:
        print("    worst pages: " + ", ".join("%s (%.2f in)" % (w["pid"], w["total"])
                                              for w in worst))
    print("    Not an error. Butted sheets always lose a thin strip at each seam.")


# ------------------------------- verification ------------------------------

def verify_pdf(pdf_path, expected_pages):
    """Every MediaBox must be exactly 612 x 792 pt (8.5 x 11 in at 72 dpi)."""
    try:
        from pypdf import PdfReader
    except ImportError:
        print("[!] pypdf not installed, skipping MediaBox verification")
        return True

    want_w = SHEET_W * 72.0
    want_h = SHEET_H * 72.0
    reader = PdfReader(pdf_path)
    print("")
    print("--- PDF MEDIABOX VERIFICATION (want %.0f x %.0f pt) ---"
          % (want_w, want_h))
    ok_all = True
    if len(reader.pages) != expected_pages:
        print("[X] page count %d, expected %d" % (len(reader.pages), expected_pages))
        ok_all = False
    for i, page in enumerate(reader.pages):
        box = page.mediabox
        w = float(box.width)
        h = float(box.height)
        ok = abs(w - want_w) < 0.01 and abs(h - want_h) < 0.01
        ok_all = ok_all and ok
        print("%s page %3d  %.2f x %.2f pt" % ("[OK]" if ok else "[X] ", i + 1, w, h))
    print("%s all %d pages" % ("[OK]" if ok_all else "[X] ", len(reader.pages)))
    return ok_all


def verify_tiling(grid):
    """COVERED rects must tile the bbox with no gaps and no overlap."""
    print("")
    print("--- TILING VERIFICATION ---")
    rects = []
    area = 0.0
    for col, row in grid.pages():
        px, py = grid.page_origin(col, row)
        cx1 = min(px + grid.sheet_w, grid.x1)
        cy1 = min(py + grid.sheet_h, grid.y1)
        rects.append((px, py, cx1, cy1))
        area += (cx1 - px) * (cy1 - py)

    want_area = grid.width * grid.height
    area_ok = abs(area - want_area) < 1e-6
    print("%s covered area %.6f vs bbox area %.6f"
          % ("[OK]" if area_ok else "[X] ", area, want_area))

    overlap = 0
    for i in range(len(rects)):
        ax0, ay0, ax1, ay1 = rects[i]
        for j in range(i + 1, len(rects)):
            bx0, by0, bx1, by1 = rects[j]
            ox = min(ax1, bx1) - max(ax0, bx0)
            oy = min(ay1, by1) - max(ay0, by0)
            if ox > 1e-9 and oy > 1e-9:
                overlap += 1
    print("%s %d overlapping pairs" % ("[OK]" if overlap == 0 else "[X] ", overlap))

    bx0 = min(r[0] for r in rects)
    by0 = min(r[1] for r in rects)
    bx1 = max(r[2] for r in rects)
    by1 = max(r[3] for r in rects)
    ext_ok = (abs(bx0 - grid.x0) < 1e-9 and abs(by0 - grid.y0) < 1e-9
              and abs(bx1 - grid.x1) < 1e-9 and abs(by1 - grid.y1) < 1e-9)
    print("%s union extents match bbox" % ("[OK]" if ext_ok else "[X] "))
    ok = area_ok and overlap == 0 and ext_ok
    print("%s tiling: no gaps, no overlap" % ("[OK]" if ok else "[X] "))
    return ok


# ------------------------------- cli ---------------------------------------

def parse_sheet(text):
    parts = text.lower().replace(" ", "").split("x")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("sheet must look like 8.5x11")
    try:
        w, h = float(parts[0]), float(parts[1])
    except ValueError:
        raise argparse.ArgumentTypeError("sheet must look like 8.5x11")
    if w <= 0 or h <= 0:
        raise argparse.ArgumentTypeError("sheet dimensions must be positive")
    return w, h


def build_parser():
    p = argparse.ArgumentParser(
        prog="tile_dxf.py",
        description="Split a 2D DXF into letter-size tiles for 1:1 printing.",
    )
    p.add_argument("input", help="input DXF file")
    p.add_argument("-o", "--output", default=None, help="output PDF path")
    p.add_argument("--units", choices=["in", "mm", "auto"], default=DXF_UNITS,
                   help="override drawing units (default: auto from $INSUNITS)")
    p.add_argument("--sheet", type=parse_sheet, default=None,
                   help="sheet size in inches, e.g. 8.5x11")
    p.add_argument("--dry-run", action="store_true",
                   help="print the grid plan and exit without rendering")
    return p


def main(argv=None):
    global SHEET_W, SHEET_H

    args = build_parser().parse_args(argv)

    if args.sheet:
        SHEET_W, SHEET_H = args.sheet

    if not os.path.isfile(args.input):
        print("[X] input not found: %s" % args.input)
        return 2

    source_name = os.path.basename(args.input)
    print("[..] reading %s" % source_name)
    try:
        doc = ezdxf.readfile(args.input)
    except (IOError, ezdxf.DXFError) as exc:
        print("[X] cannot read DXF: %s" % exc)
        return 2

    polylines_raw, skipped, kept = load_geometry(doc, FLATTEN_TOL)
    if not polylines_raw:
        print("[X] no renderable geometry found in modelspace")
        print_skip_report(skipped, kept)
        return 2

    bbox_raw = compute_bbox(polylines_raw)
    factor, unit_note = resolve_units(doc, args.units, bbox_raw)

    # Flatten tolerance was applied in raw units; if the drawing is in mm the
    # effective chord tolerance tightens after scaling, which is harmless.
    polylines = scale_polylines(polylines_raw, factor)
    bbox = compute_bbox(polylines)

    print("[OK] units: %s (scale to inches = %.6f)" % (unit_note, factor))
    print_skip_report(skipped, kept)

    grid = Grid(bbox, SHEET_W, SHEET_H)

    if args.dry_run:
        dry_run_report(grid, source_name, unit_note)
        return 0

    out_pdf = args.output
    if out_pdf is None:
        out_pdf = os.path.splitext(args.input)[0] + "_tiled.pdf"
    manifest_path = os.path.splitext(out_pdf)[0] + "_manifest.txt"

    total_pages = grid.n_pages + 1
    print("")
    print("[..] rendering %d pages (index + %d tiles) -> %s"
          % (total_pages, grid.n_pages, os.path.basename(out_pdf)))

    with PdfPages(out_pdf) as pdf:
        draw_index_page(pdf, grid, polylines, source_name, total_pages, unit_note)
        for col, row in grid.pages():
            draw_page(pdf, grid, polylines, (col, row), total_pages,
                      source_name, args)
    print("[OK] wrote %s" % out_pdf)

    segments = to_segments(polylines)
    loss_rows = compute_loss(grid, segments)
    write_manifest(manifest_path, grid, source_name, unit_note, loss_rows)
    print("[OK] wrote %s" % manifest_path)

    pdf_ok = verify_pdf(out_pdf, total_pages)
    tile_ok = verify_tiling(grid)
    print_loss_summary(loss_rows)

    print("")
    if pdf_ok and tile_ok:
        print("[OK] done. Print at 100% / Actual Size. Not Fit to Page.")
        return 0
    print("[X] done with verification failures, see above")
    return 1


if __name__ == "__main__":
    sys.exit(main())
