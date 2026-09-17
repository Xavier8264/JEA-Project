"""
tile_dxf_text.py - Same 1:1 tiled letter-size output as tile_dxf.py, but the
drawing's MTEXT / TEXT labels are converted to real vector outlines and printed
with the geometry.

Why a second script: tile_dxf.py is frozen. This one imports it and replaces
ONLY the geometry-loading step. Everything downstream (grid, page rendering,
manifest, MediaBox / tiling verification, loss report) is the already-verified
code from tile_dxf.py, so the two tools cannot drift apart.

How the text gets in:
    MTEXT -> MTextExplode  -> TEXT      (handles \\P line breaks, columns)
    TEXT  -> text2path     -> Path      (real glyph outlines, world coords)
    Path  -> flattening()  -> polyline  (same vertex-list form as every entity)
Once text is a polyline it is indistinguishable from drawing linework, so it
tiles, clips at sheet edges and verifies exactly like the rest.

Note ezdxf.path.make_path() cannot do this: it raises
"unsupported DXF type: MTEXT". text2path is a separate addon and needs TEXT,
not MTEXT, which is why the explode step comes first.

Usage:
    python tile_dxf_text.py INPUT.dxf [-o OUTPUT.pdf] [--units in|mm|auto]
                            [--sheet 8.5x11] [--dry-run] [--no-text]
"""

import argparse
import os
import sys
from collections import Counter

import numpy as np

import ezdxf
from ezdxf import disassemble, path as ezpath
from ezdxf.addons import MTextExplode, text2path

import tile_dxf as base
from tile_dxf import (
    FLATTEN_TOL,
    Grid,
    col_label,
    compute_bbox,
    scale_polylines,
    to_segments,
)


# ============================== CONFIG ==============================

# Advisory only. Text shorter than this prints too small to read at 1:1 and is
# almost always a mistake in the source drawing rather than an intent.
MIN_TEXT_HEIGHT = 0.05         # inches

# ====================================================================

# Entities text2path handles directly.
TEXT_TYPES = frozenset({"TEXT", "ATTRIB", "ATTDEF"})

# Still nothing we can turn into fabrication linework. MTEXT is deliberately
# NOT here: it is exploded to TEXT before decomposition. Any MTEXT that somehow
# survives will fail make_path() and be reported, never silently dropped.
SKIP_TYPES = frozenset({"HATCH", "DIMENSION", "POINT", "LEADER"})


def _flatten_path(p, tol, out):
    """Append every sub-path of p to out as an (N, 2) array. Returns count."""
    added = 0
    for sub in (p.sub_paths() if hasattr(p, "sub_paths") else [p]):
        verts = [(v.x, v.y) for v in sub.flattening(tol)]
        if len(verts) < 2:
            continue
        out.append(np.asarray(verts, dtype=float))
        added += 1
    return added


def load_geometry_with_text(doc, tol, include_text=True):
    """
    Flatten modelspace to world-coordinate polylines, text included.

    Returns (polylines, skipped, kept, text_items, n_exploded) where
    text_items is a list of (raw_char_height, string) for the tiny-text report
    and n_exploded is how many MTEXT entities were burst into TEXT.

    Vertices are in RAW DXF units; the caller scales to inches, exactly as
    tile_dxf.py does, so one scale factor covers geometry and text alike.
    """
    msp = doc.modelspace()

    n_exploded = 0
    if include_text:
        mtexts = msp.query("MTEXT")  # snapshot, safe to destroy while iterating
        if len(mtexts):
            with MTextExplode(msp) as xpl:
                for mt in mtexts:
                    xpl.explode(mt)
            n_exploded = len(mtexts)

    polylines = []
    skipped = Counter()
    kept = Counter()
    text_items = []

    for entity in disassemble.recursive_decompose(msp):
        etype = entity.dxftype()

        if etype in SKIP_TYPES:
            skipped[etype] += 1
            continue

        if etype in TEXT_TYPES:
            if not include_text:
                skipped[etype] += 1
                continue
            try:
                paths = text2path.make_paths_from_entity(entity)
            except Exception as exc:  # font missing, unmappable glyph, etc.
                skipped["%s (text2path %s)" % (etype, type(exc).__name__)] += 1
                continue
            added = 0
            for p in paths:
                added += _flatten_path(p, tol, polylines)
            if added:
                kept[etype] += 1
                text_items.append(
                    (float(getattr(entity.dxf, "height", 0.0) or 0.0),
                     str(getattr(entity.dxf, "text", "")))
                )
            else:
                # A space-only or zero-height string yields no contour.
                skipped["%s (no outline)" % etype] += 1
            continue

        try:
            p = ezpath.make_path(entity)
        except (TypeError, ValueError) as exc:
            skipped["%s (%s)" % (etype, type(exc).__name__)] += 1
            continue

        if _flatten_path(p, tol, polylines):
            kept[etype] += 1
        else:
            skipped["%s (degenerate)" % etype] += 1

    return polylines, skipped, kept, text_items, n_exploded


def print_text_report(kept, text_items, n_exploded, factor, include_text):
    if not include_text:
        print("[!] --no-text given: TEXT and MTEXT were skipped, as in tile_dxf.py")
        return
    n_text = sum(kept[t] for t in TEXT_TYPES if t in kept)
    print("[OK] text: %d MTEXT exploded -> %d TEXT converted to vector outlines"
          % (n_exploded, n_text))

    tiny = [(h * factor, s) for h, s in text_items if h * factor < MIN_TEXT_HEIGHT]
    if tiny:
        print("[!] %d text item(s) below %.3f in tall. These print too small to"
              % (len(tiny), MIN_TEXT_HEIGHT))
        print("[!] read at 1:1 and are probably a mistake in the source drawing:")
        for h, s in sorted(tiny)[:10]:
            print("[!]      %.4f in  %r" % (h, s[:40]))


def build_parser():
    p = argparse.ArgumentParser(
        prog="tile_dxf_text.py",
        description="Tile a 2D DXF into letter sheets for 1:1 printing, "
                    "with MTEXT/TEXT rendered as vector outlines.",
    )
    p.add_argument("input", help="input DXF file")
    p.add_argument("-o", "--output", default=None, help="output PDF path")
    p.add_argument("--units", choices=["in", "mm", "auto"], default="auto",
                   help="override drawing units (default: auto from $INSUNITS)")
    p.add_argument("--sheet", type=base.parse_sheet, default=None,
                   help="sheet size in inches, e.g. 8.5x11")
    p.add_argument("--dry-run", action="store_true",
                   help="print the grid plan and exit without rendering")
    p.add_argument("--no-text", action="store_true",
                   help="skip text, reproducing tile_dxf.py output")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    include_text = not args.no_text

    # draw_index_page() and verify_pdf() read these module globals.
    if args.sheet:
        base.SHEET_W, base.SHEET_H = args.sheet
    sheet_w, sheet_h = base.SHEET_W, base.SHEET_H

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

    polys_raw, skipped, kept, text_items, n_exploded = load_geometry_with_text(
        doc, FLATTEN_TOL, include_text
    )
    if not polys_raw:
        print("[X] no renderable geometry found in modelspace")
        base.print_skip_report(skipped, kept)
        return 2

    bbox_raw = compute_bbox(polys_raw)
    factor, unit_note = base.resolve_units(doc, args.units, bbox_raw)

    polylines = scale_polylines(polys_raw, factor)
    bbox = compute_bbox(polylines)

    print("[OK] units: %s (scale to inches = %.6f)" % (unit_note, factor))
    base.print_skip_report(skipped, kept)
    print_text_report(kept, text_items, n_exploded, factor, include_text)

    grid = Grid(bbox, sheet_w, sheet_h)

    if args.dry_run:
        base.dry_run_report(grid, source_name, unit_note)
        return 0

    out_pdf = args.output
    if out_pdf is None:
        suffix = "_tiled_text.pdf" if include_text else "_tiled_notext.pdf"
        out_pdf = os.path.splitext(args.input)[0] + suffix
    manifest_path = os.path.splitext(out_pdf)[0] + "_manifest.txt"

    total_pages = grid.n_pages + 1
    print("")
    print("[..] rendering %d pages (index + %d tiles) -> %s"
          % (total_pages, grid.n_pages, os.path.basename(out_pdf)))

    from matplotlib.backends.backend_pdf import PdfPages
    with PdfPages(out_pdf) as pdf:
        base.draw_index_page(pdf, grid, polylines, source_name, total_pages,
                             unit_note)
        for col, row in grid.pages():
            base.draw_page(pdf, grid, polylines, (col, row), total_pages,
                           source_name, args)
    print("[OK] wrote %s" % out_pdf)

    segments = to_segments(polylines)
    loss_rows = base.compute_loss(grid, segments)
    base.write_manifest(manifest_path, grid, source_name, unit_note, loss_rows)
    with open(manifest_path, "a", encoding="ascii") as fh:
        fh.write("=" * 72 + "\n")
        fh.write("TEXT RENDERING\n")
        fh.write("=" * 72 + "\n")
        if include_text:
            n_text = sum(kept[t] for t in TEXT_TYPES if t in kept)
            fh.write("%d MTEXT exploded to %d TEXT, converted to vector outlines\n"
                     % (n_exploded, n_text))
            fh.write("via ezdxf MTextExplode + text2path, flattened at %.3f in.\n"
                     % FLATTEN_TOL)
            fh.write("Outlines are stroked linework, not filled glyphs.\n")
        else:
            fh.write("Text was skipped (--no-text).\n")
    print("[OK] wrote %s" % manifest_path)

    pdf_ok = base.verify_pdf(out_pdf, total_pages)
    tile_ok = base.verify_tiling(grid)
    base.print_loss_summary(loss_rows)

    print("")
    if pdf_ok and tile_ok:
        print("[OK] done. Print at 100% / Actual Size. Not Fit to Page.")
        return 0
    print("[X] done with verification failures, see above")
    return 1


if __name__ == "__main__":
    sys.exit(main())
