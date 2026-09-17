"""
Unit tests for tile_dxf_text.py (the text-rendering variant).

Run:  python -m unittest -v test_tile_dxf_text

These assume tile_dxf.py is frozen and already covered by test_tile_dxf.py;
what is tested here is only the text pipeline and the guarantee that the two
tools agree when text is disabled.
"""

import os
import tempfile
import unittest

import ezdxf
import numpy as np

import tile_dxf as base
import tile_dxf_text as X


HERE = os.path.dirname(os.path.abspath(__file__))
REAL_DXF = os.path.join(HERE, "Cardboard Layout REV1 backup_9.9_15.dxf")


def fresh_doc():
    """load_geometry_with_text() explodes MTEXT in place, so never share a doc."""
    return ezdxf.readfile(REAL_DXF)


@unittest.skipUnless(os.path.isfile(REAL_DXF), "input DXF not present")
class TestTextPipeline(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        doc = fresh_doc()
        cls.n_mtext_before = len(doc.modelspace().query("MTEXT"))
        (cls.polys, cls.skipped, cls.kept,
         cls.text_items, cls.n_exploded) = X.load_geometry_with_text(
            doc, base.FLATTEN_TOL, True)
        cls.bbox = base.compute_bbox(cls.polys)
        cls.grid = base.Grid(cls.bbox, 8.5, 11.0)

    def test_all_mtext_exploded(self):
        self.assertEqual(self.n_mtext_before, 25)
        self.assertEqual(self.n_exploded, 25)

    def test_mtext_became_text_outlines(self):
        self.assertEqual(self.kept["TEXT"], 52)

    def test_no_text_type_is_skipped(self):
        for key in self.skipped:
            self.assertNotIn("MTEXT", key)
            self.assertNotIn("TEXT", key)

    def test_hatch_and_point_still_skipped(self):
        self.assertEqual(self.skipped["HATCH"], 17)
        self.assertEqual(self.skipped["POINT"], 6)

    def test_geometry_entities_unchanged_from_frozen_tool(self):
        geo, _, kept_base = base.load_geometry(fresh_doc(), base.FLATTEN_TOL)
        for etype in ("LINE", "LWPOLYLINE", "CIRCLE", "SPLINE"):
            self.assertEqual(self.kept[etype], kept_base[etype], etype)

    def test_text_adds_vertices(self):
        geo, _, _ = base.load_geometry(fresh_doc(), base.FLATTEN_TOL)
        n_geo = sum(len(p) for p in geo)
        n_all = sum(len(p) for p in self.polys)
        self.assertGreater(n_all, n_geo)

    def test_tiny_text_is_detected(self):
        tiny = [(h, s) for h, s in self.text_items if h < X.MIN_TEXT_HEIGHT]
        self.assertTrue(tiny, "the 0.010 in RESET label should be flagged")
        self.assertIn("RESET", [s for _, s in tiny])


@unittest.skipUnless(os.path.isfile(REAL_DXF), "input DXF not present")
class TestGridIsUnchangedByText(unittest.TestCase):
    """Text must not enlarge the bbox, or the page layout would shift."""

    @classmethod
    def setUpClass(cls):
        cls.geo, _, _ = base.load_geometry(fresh_doc(), base.FLATTEN_TOL)
        cls.all_, _, _, _, _ = X.load_geometry_with_text(
            fresh_doc(), base.FLATTEN_TOL, True)

    def test_bbox_identical(self):
        a = base.compute_bbox(self.geo)
        b = base.compute_bbox(self.all_)
        for va, vb in zip(a, b):
            self.assertAlmostEqual(va, vb, places=9)

    def test_grid_still_6x5_30_pages(self):
        g = base.Grid(base.compute_bbox(self.all_), 8.5, 11.0)
        self.assertEqual(g.n_cols, 6)
        self.assertEqual(g.n_rows, 5)
        self.assertEqual(g.n_pages, 30)
        self.assertEqual("%.3f" % g.last_col_keep, "5.500")
        self.assertEqual("%.3f" % g.last_row_keep, "4.000")

    def test_text_lies_inside_geometry_bbox(self):
        gb = base.compute_bbox(self.geo)
        tb = base.compute_bbox(self.all_)
        self.assertGreaterEqual(tb[0], gb[0] - 1e-9)
        self.assertGreaterEqual(tb[1], gb[1] - 1e-9)
        self.assertLessEqual(tb[2], gb[2] + 1e-9)
        self.assertLessEqual(tb[3], gb[3] + 1e-9)


@unittest.skipUnless(os.path.isfile(REAL_DXF), "input DXF not present")
class TestNoTextMatchesFrozenTool(unittest.TestCase):
    def test_no_text_gives_same_polylines_as_base(self):
        geo, _, kept_base = base.load_geometry(fresh_doc(), base.FLATTEN_TOL)
        alt, _, kept_alt, items, n_ex = X.load_geometry_with_text(
            fresh_doc(), base.FLATTEN_TOL, False)
        self.assertEqual(n_ex, 0)
        self.assertEqual(items, [])
        self.assertEqual(len(alt), len(geo))
        self.assertAlmostEqual(
            sum(len(p) for p in alt), sum(len(p) for p in geo))
        for etype in ("LINE", "LWPOLYLINE", "CIRCLE", "SPLINE"):
            self.assertEqual(kept_alt[etype], kept_base[etype], etype)


@unittest.skipUnless(os.path.isfile(REAL_DXF), "input DXF not present")
class TestRenderedPdf(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp(prefix="tiledxftext_")
        cls.pdf = os.path.join(cls.tmp, "out.pdf")
        cls.rc = X.main([REAL_DXF, "-o", cls.pdf])

    def test_exit_code_zero(self):
        self.assertEqual(self.rc, 0)

    def test_31_pages_all_letter_size(self):
        from pypdf import PdfReader
        pages = PdfReader(self.pdf).pages
        self.assertEqual(len(pages), 31)
        for i, page in enumerate(pages):
            self.assertAlmostEqual(float(page.mediabox.width), 612.0, places=2,
                                   msg="page %d" % (i + 1))
            self.assertAlmostEqual(float(page.mediabox.height), 792.0, places=2,
                                   msg="page %d" % (i + 1))

    def test_manifest_records_text_rendering(self):
        mpath = os.path.splitext(self.pdf)[0] + "_manifest.txt"
        self.assertTrue(os.path.isfile(mpath))
        with open(mpath, "r", encoding="ascii") as fh:
            text = fh.read()
        self.assertIn("TEXT RENDERING", text)
        self.assertIn("25 MTEXT exploded to 52 TEXT", text)
        self.assertIn("A1", text)

    def test_text_pdf_has_more_linework_than_no_text_pdf(self):
        import re
        from pypdf import PdfReader
        plain = os.path.join(self.tmp, "plain.pdf")
        X.main([REAL_DXF, "--no-text", "-o", plain])

        def ops(p):
            n = 0
            for pg in PdfReader(p).pages:
                d = pg.get_contents().get_data().decode("latin-1")
                n += len(re.findall(r"([-\d.]+) ([-\d.]+) (m|l)\b", d))
            return n

        self.assertGreater(ops(self.pdf), ops(plain))


class TestSourceIsAscii(unittest.TestCase):
    def test_ascii_only(self):
        for name in ("tile_dxf_text.py", "test_tile_dxf_text.py"):
            with open(os.path.join(HERE, name), "rb") as fh:
                fh.read().decode("ascii")


if __name__ == "__main__":
    unittest.main(verbosity=2)
