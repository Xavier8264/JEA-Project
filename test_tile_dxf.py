"""
Unit tests for tile_dxf.py

Run:  python -m unittest -v test_tile_dxf
"""

import math
import os
import tempfile
import unittest

import numpy as np

import tile_dxf as T


HERE = os.path.dirname(os.path.abspath(__file__))
REAL_DXF = os.path.join(HERE, "Cardboard Layout REV1 backup_9.9_14.dxf")


class TestColumnLabels(unittest.TestCase):
    def test_single_letters(self):
        self.assertEqual(T.col_label(0), "A")
        self.assertEqual(T.col_label(1), "B")
        self.assertEqual(T.col_label(5), "F")
        self.assertEqual(T.col_label(25), "Z")

    def test_beyond_z(self):
        self.assertEqual(T.col_label(26), "AA")
        self.assertEqual(T.col_label(27), "AB")
        self.assertEqual(T.col_label(51), "AZ")
        self.assertEqual(T.col_label(52), "BA")


class TestTileCount(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(T.n_tiles(48.0, 8.5), 6)
        self.assertEqual(T.n_tiles(48.0, 11.0), 5)

    def test_exact_multiple_adds_no_sliver(self):
        self.assertEqual(T.n_tiles(44.0, 11.0), 4)
        self.assertEqual(T.n_tiles(17.0, 8.5), 2)

    def test_float_slack(self):
        # 47.99999999999999 must not round up to an extra row.
        self.assertEqual(T.n_tiles(44.0000000001, 11.0), 4)
        self.assertEqual(T.n_tiles(47.99999999999999, 11.0), 5)

    def test_minimum_one(self):
        self.assertEqual(T.n_tiles(0.001, 8.5), 1)


class TestGrid48x48(unittest.TestCase):
    """The spec self-check case: a 48 x 48 in model."""

    def setUp(self):
        self.g = T.Grid((0.0, 0.0, 48.0, 48.0), 8.5, 11.0)

    def test_six_columns_a_through_f(self):
        self.assertEqual(self.g.n_cols, 6)
        labels = [T.col_label(c) for c in range(self.g.n_cols)]
        self.assertEqual(labels, ["A", "B", "C", "D", "E", "F"])

    def test_five_rows(self):
        self.assertEqual(self.g.n_rows, 5)

    def test_thirty_pages(self):
        self.assertEqual(self.g.n_pages, 30)

    def test_last_column_kept_at_5_500(self):
        self.assertAlmostEqual(self.g.last_col_keep, 5.5, places=9)
        self.assertTrue(self.g.col_partial)
        self.assertEqual("%.3f" % self.g.last_col_keep, "5.500")

    def test_last_row_kept_at_4_000(self):
        self.assertAlmostEqual(self.g.last_row_keep, 4.0, places=9)
        self.assertTrue(self.g.row_partial)
        self.assertEqual("%.3f" % self.g.last_row_keep, "4.000")

    def test_column_widths(self):
        self.assertEqual(
            ["%.3f" % w for w in self.g.col_widths()],
            ["8.500", "8.500", "8.500", "8.500", "8.500", "5.500"],
        )

    def test_row_heights(self):
        self.assertEqual(
            ["%.3f" % h for h in self.g.row_heights()],
            ["11.000", "11.000", "11.000", "11.000", "4.000"],
        )

    def test_partial_page_count(self):
        # last column (5 pages) + last row (6 pages) - shared corner = 10
        self.assertEqual(self.g.n_partial(), 10)


class TestPageNaming(unittest.TestCase):
    """Row 1 is the BOTTOM row. This is intentionally not spreadsheet order."""

    def setUp(self):
        self.g = T.Grid((0.0, 0.0, 48.0, 48.0), 8.5, 11.0)

    def test_a1_is_bottom_left(self):
        self.assertEqual(self.g.page_id(0, 0), "A1")
        self.assertEqual(self.g.page_origin(0, 0), (0.0, 0.0))

    def test_b1_is_right_of_a1(self):
        ax, ay = self.g.page_origin(0, 0)
        bx, by = self.g.page_origin(1, 0)
        self.assertEqual(self.g.page_id(1, 0), "B1")
        self.assertAlmostEqual(bx - ax, 8.5)
        self.assertAlmostEqual(by, ay)

    def test_a2_is_above_a1(self):
        ax, ay = self.g.page_origin(0, 0)
        cx, cy = self.g.page_origin(0, 1)
        self.assertEqual(self.g.page_id(0, 1), "A2")
        self.assertAlmostEqual(cx, ax)
        self.assertAlmostEqual(cy - ay, 11.0)

    def test_top_right_is_f5(self):
        self.assertEqual(self.g.page_id(self.g.n_cols - 1, self.g.n_rows - 1), "F5")

    def test_page_order_bottom_row_first(self):
        order = [self.g.page_id(c, r) for c, r in self.g.pages()]
        self.assertEqual(order[:6], ["A1", "B1", "C1", "D1", "E1", "F1"])
        self.assertEqual(order[6:12], ["A2", "B2", "C2", "D2", "E2", "F2"])
        self.assertEqual(order[-1], "F5")
        self.assertEqual(len(order), 30)

    def test_corner_page_is_partial_both_ways(self):
        kw, kh = self.g.keep_size(5, 4)
        self.assertAlmostEqual(kw, 5.5)
        self.assertAlmostEqual(kh, 4.0)


class TestTiling(unittest.TestCase):
    """Covered rects must tile the bbox with no gaps and no overlap."""

    def _check(self, bbox, sw=8.5, sh=11.0):
        g = T.Grid(bbox, sw, sh)
        rects = []
        area = 0.0
        for col, row in g.pages():
            px, py = g.page_origin(col, row)
            cx1 = min(px + sw, g.x1)
            cy1 = min(py + sh, g.y1)
            self.assertGreater(cx1, px)
            self.assertGreater(cy1, py)
            rects.append((px, py, cx1, cy1))
            area += (cx1 - px) * (cy1 - py)

        self.assertAlmostEqual(area, g.width * g.height, places=6)

        for i in range(len(rects)):
            ax0, ay0, ax1, ay1 = rects[i]
            for j in range(i + 1, len(rects)):
                bx0, by0, bx1, by1 = rects[j]
                ox = min(ax1, bx1) - max(ax0, bx0)
                oy = min(ay1, by1) - max(ay0, by0)
                self.assertFalse(ox > 1e-9 and oy > 1e-9,
                                 "overlap between rect %d and %d" % (i, j))

        self.assertAlmostEqual(min(r[0] for r in rects), g.x0)
        self.assertAlmostEqual(min(r[1] for r in rects), g.y0)
        self.assertAlmostEqual(max(r[2] for r in rects), g.x1)
        self.assertAlmostEqual(max(r[3] for r in rects), g.y1)

    def test_48x48(self):
        self._check((0.0, 0.0, 48.0, 48.0))

    def test_exact_multiple(self):
        self._check((0.0, 0.0, 17.0, 22.0))

    def test_offset_origin(self):
        self._check((-13.25, 7.125, 20.5, 33.875))

    def test_smaller_than_one_sheet(self):
        self._check((0.0, 0.0, 3.0, 4.0))


class TestClipping(unittest.TestCase):
    def test_segment_fully_inside(self):
        segs = np.array([[1.0, 1.0, 2.0, 2.0]])
        out = T.clip_segments_to_rect(segs, 0, 0, 10, 10)
        self.assertEqual(out.shape[0], 1)
        np.testing.assert_allclose(out[0], segs[0])

    def test_segment_fully_outside(self):
        segs = np.array([[20.0, 20.0, 30.0, 30.0]])
        out = T.clip_segments_to_rect(segs, 0, 0, 10, 10)
        self.assertEqual(out.shape[0], 0)

    def test_segment_crossing_is_trimmed(self):
        segs = np.array([[-5.0, 5.0, 5.0, 5.0]])
        out = T.clip_segments_to_rect(segs, 0, 0, 10, 10)
        self.assertEqual(out.shape[0], 1)
        self.assertAlmostEqual(out[0][0], 0.0)
        self.assertAlmostEqual(out[0][2], 5.0)

    def test_axis_parallel_outside_rejected(self):
        # Horizontal line above the rect: parallel to top/bottom, must reject.
        segs = np.array([[1.0, 50.0, 9.0, 50.0]])
        out = T.clip_segments_to_rect(segs, 0, 0, 10, 10)
        self.assertEqual(out.shape[0], 0)

    def test_axis_parallel_inside_kept(self):
        segs = np.array([[-1.0, 5.0, 11.0, 5.0]])
        out = T.clip_segments_to_rect(segs, 0, 0, 10, 10)
        self.assertEqual(out.shape[0], 1)
        self.assertAlmostEqual(T.segment_length(out), 10.0)

    def test_length(self):
        segs = np.array([[0.0, 0.0, 3.0, 4.0]])
        self.assertAlmostEqual(T.segment_length(segs), 5.0)

    def test_length_of_empty(self):
        self.assertEqual(T.segment_length(np.zeros((0, 4))), 0.0)


class TestGeometryHelpers(unittest.TestCase):
    def test_bbox(self):
        polys = [np.array([[0.0, 0.0], [1.0, 5.0]]),
                 np.array([[-2.0, 3.0], [4.0, 1.0]])]
        self.assertEqual(T.compute_bbox(polys), (-2.0, 0.0, 4.0, 5.0))

    def test_bbox_empty(self):
        self.assertIsNone(T.compute_bbox([]))

    def test_to_segments(self):
        polys = [np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 1.0]])]
        segs = T.to_segments(polys)
        self.assertEqual(segs.shape, (2, 4))
        self.assertAlmostEqual(T.segment_length(segs), 2.0)

    def test_scale_mm_to_inches(self):
        polys = [np.array([[0.0, 0.0], [25.4, 50.8]])]
        out = T.scale_polylines(polys, 1.0 / 25.4)
        np.testing.assert_allclose(out[0], [[0.0, 0.0], [1.0, 2.0]])


class TestSheetParsing(unittest.TestCase):
    def test_valid(self):
        self.assertEqual(T.parse_sheet("8.5x11"), (8.5, 11.0))
        self.assertEqual(T.parse_sheet("11 x 17"), (11.0, 17.0))

    def test_invalid(self):
        import argparse
        for bad in ("8.5", "axb", "8.5x", "-1x11", "0x11"):
            with self.assertRaises(argparse.ArgumentTypeError):
                T.parse_sheet(bad)


class TestExactOneToOneScale(unittest.TestCase):
    def test_axes_fill_figure_and_map_inches_to_inches(self):
        fig, ax = T.new_sheet(8.5, 11.0, 3.25, 7.5)
        try:
            self.assertEqual(tuple(fig.get_size_inches()), (8.5, 11.0))
            self.assertEqual(ax.get_position().bounds, (0.0, 0.0, 1.0, 1.0))
            self.assertEqual(ax.get_xlim(), (3.25, 11.75))
            self.assertEqual(ax.get_ylim(), (7.5, 18.5))
            # One data inch must be exactly one figure inch on both axes.
            p0 = ax.transData.transform((3.25, 7.5))
            p1 = ax.transData.transform((4.25, 8.5))
            dpi = fig.dpi
            self.assertAlmostEqual((p1[0] - p0[0]) / dpi, 1.0, places=9)
            self.assertAlmostEqual((p1[1] - p0[1]) / dpi, 1.0, places=9)
        finally:
            import matplotlib.pyplot as plt
            plt.close(fig)


@unittest.skipUnless(os.path.isfile(REAL_DXF), "input DXF not present")
class TestRealDxf(unittest.TestCase):
    """Spec self-check 1, against the actual input file."""

    @classmethod
    def setUpClass(cls):
        import ezdxf
        doc = ezdxf.readfile(REAL_DXF)
        polys, cls.skipped, cls.kept = T.load_geometry(doc, T.FLATTEN_TOL)
        factor, cls.unit_note = T.resolve_units(doc, "auto", T.compute_bbox(polys))
        cls.polys = T.scale_polylines(polys, factor)
        cls.bbox = T.compute_bbox(cls.polys)
        cls.grid = T.Grid(cls.bbox, 8.5, 11.0)

    def test_units_are_inches(self):
        self.assertIn("$INSUNITS=1", self.unit_note)

    def test_model_is_48_by_48(self):
        self.assertAlmostEqual(self.grid.width, 48.0, places=6)
        self.assertAlmostEqual(self.grid.height, 48.0, places=6)

    def test_grid_matches_spec_selfcheck(self):
        self.assertEqual(self.grid.n_cols, 6)
        self.assertEqual(self.grid.n_rows, 5)
        self.assertEqual(self.grid.n_pages, 30)
        self.assertEqual(T.col_label(self.grid.n_cols - 1), "F")
        self.assertEqual("%.3f" % self.grid.last_col_keep, "5.500")
        self.assertEqual("%.3f" % self.grid.last_row_keep, "4.000")

    def test_unsupported_entities_are_reported_not_dropped(self):
        # MTEXT / POINT / HATCH must be counted, never silently discarded.
        self.assertGreater(sum(self.skipped.values()), 0)
        for t in ("MTEXT", "POINT", "HATCH"):
            self.assertIn(t, self.skipped)

    def test_geometry_was_flattened(self):
        self.assertGreater(len(self.polys), 0)
        for t in ("LINE", "LWPOLYLINE", "CIRCLE", "SPLINE"):
            self.assertIn(t, self.kept)


@unittest.skipUnless(os.path.isfile(REAL_DXF), "input DXF not present")
class TestRenderedPdf(unittest.TestCase):
    """Spec self-check 2: every MediaBox exactly 612 x 792 pt."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="tiledxf_")
        cls.pdf = os.path.join(cls.tmp, "out.pdf")
        rc = T.main([REAL_DXF, "-o", cls.pdf])
        cls.rc = rc

    def test_exit_code_zero(self):
        self.assertEqual(self.rc, 0)

    def test_pdf_exists(self):
        self.assertTrue(os.path.isfile(self.pdf))

    def test_page_count_is_index_plus_tiles(self):
        from pypdf import PdfReader
        self.assertEqual(len(PdfReader(self.pdf).pages), 31)

    def test_every_mediabox_is_612_by_792(self):
        from pypdf import PdfReader
        for i, page in enumerate(PdfReader(self.pdf).pages):
            w = float(page.mediabox.width)
            h = float(page.mediabox.height)
            self.assertAlmostEqual(w, 612.0, places=2, msg="page %d width" % (i + 1))
            self.assertAlmostEqual(h, 792.0, places=2, msg="page %d height" % (i + 1))

    def test_manifest_written_and_lists_every_page(self):
        mpath = os.path.splitext(self.pdf)[0] + "_manifest.txt"
        self.assertTrue(os.path.isfile(mpath))
        with open(mpath, "r", encoding="ascii") as fh:
            text = fh.read()
        for pid in ("A1", "B1", "F1", "A5", "F5"):
            self.assertIn(pid, text)
        self.assertIn("5.500", text)
        self.assertIn("4.000", text)

    def test_manifest_is_pure_ascii(self):
        mpath = os.path.splitext(self.pdf)[0] + "_manifest.txt"
        with open(mpath, "rb") as fh:
            raw = fh.read()
        raw.decode("ascii")  # raises if any non-ASCII byte slipped in


class TestAnnotationsStayInKeepRegion(unittest.TestCase):
    """
    Regression guard: on a partial page every annotation must sit inside the
    KEEP region, otherwise it lands past a CUT line and is thrown away.
    The top-right corner page is partial on both axes, so it is the strict case.
    """

    def _texts_on_page(self, grid, polys, col, row):
        import matplotlib.pyplot as plt
        captured = {}

        class Shim(object):
            def savefig(self, fig):
                ax = fig.axes[0]
                captured["items"] = [
                    (t.get_text(), t.get_position()) for t in ax.texts
                ]

        shim = Shim()
        T.draw_page(shim, grid, polys, (col, row), 31, "src.dxf", None)
        plt.close("all")
        return captured["items"]

    def setUp(self):
        self.grid = T.Grid((0.0, 0.0, 48.0, 48.0), 8.5, 11.0)
        # A single polyline is enough; this test is about annotation placement.
        self.polys = [np.array([[0.0, 0.0], [48.0, 48.0]])]

    def _assert_inside_keep(self, col, row):
        g = self.grid
        px, py = g.page_origin(col, row)
        kw, kh = g.keep_size(col, row)
        x_hi = px + min(g.sheet_w, kw)
        y_hi = py + min(g.sheet_h, kh)
        for text, (x, y) in self._texts_on_page(g, self.polys, col, row):
            self.assertGreaterEqual(x, px, "%r left of sheet" % text)
            self.assertGreaterEqual(y, py, "%r below sheet" % text)
            self.assertLessEqual(
                x, x_hi, "%r at x=%.3f is past the vertical cut at %.3f"
                % (text, x, x_hi))
            self.assertLessEqual(
                y, y_hi, "%r at y=%.3f is past the horizontal cut at %.3f"
                % (text, y, y_hi))

    def test_corner_page_f5_partial_both_axes(self):
        self._assert_inside_keep(5, 4)

    def test_last_column_page_f1(self):
        self._assert_inside_keep(5, 0)

    def test_last_row_page_c5(self):
        self._assert_inside_keep(2, 4)

    def test_interior_page_b2(self):
        self._assert_inside_keep(1, 1)

    def test_corner_page_actually_has_both_cut_labels(self):
        texts = [t for t, _ in self._texts_on_page(self.grid, self.polys, 5, 4)]
        self.assertIn("CUT AT 5.500 in", texts)
        self.assertIn("CUT AT 4.000 in", texts)
        self.assertEqual(texts.count("CUT"), 2)


class TestSourceIsAscii(unittest.TestCase):
    def test_tool_source_is_ascii(self):
        for name in ("tile_dxf.py", "test_tile_dxf.py"):
            p = os.path.join(HERE, name)
            with open(p, "rb") as fh:
                fh.read().decode("ascii")


if __name__ == "__main__":
    unittest.main(verbosity=2)
