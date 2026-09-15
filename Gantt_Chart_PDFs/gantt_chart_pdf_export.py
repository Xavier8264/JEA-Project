"""
Exports "JEA Project - Gantt Chart.xlsx" (Vertex42 Simple Gantt Chart template,
sheet "Project schedule") into a single landscape, multi-page PDF that tiles
the full project timeline left-to-right across its pages -- print it and lay
the pages out in order to see the whole schedule as one continuous chart.

Only page 1 carries the task-name column; every later page hands that space
over to more timeline, at the same inches-per-day scale as page 1, so the
date gridlines line up in size (not necessarily in absolute position -- see
MARGIN_LEFT_IN/MARGIN_RIGHT_IN below) when pages are placed side by side.
Standard printers can't print to the paper edge, so trim each page's blank
side margin before taping for a seamless join.

Usage (from this folder, or anywhere):
    python gantt_chart_pdf_export.py
    python gantt_chart_pdf_export.py --weeks-per-page 4 --page-size tabloid

Every run is treated as a new revision: the script looks at the PDFs already
sitting in this folder, bumps the revision number by one, and writes a new
file named:

    gantt_chart_rev<N>_<M.D.YY>_<HH>.pdf

e.g. gantt_chart_rev0_9.14.26_11.pdf  (rev 0, Sep 14 '26, exported at 11:00)

A matching "..._manifest.txt" is written alongside it listing what date range
each page covers, so old revisions stay untouched and browsable.
"""

import argparse
import re
import sys
import warnings
from datetime import date, datetime, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import openpyxl
from matplotlib.backends.backend_pdf import PdfPages

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_XLSX = SCRIPT_DIR.parent / "JEA Project - Gantt Chart.xlsx"
SHEET_NAME = "Project schedule"
HEADER_ROW = 5
FIRST_DATA_ROW = 8
STOP_MARKER = "insert new rows"

PAGE_SIZES_IN = {
    "letter": (11.0, 8.5),
    "tabloid": (17.0, 11.0),
}

COLOR_PHASE_BAND = "#dbe5f1"
COLOR_ROW_ALT = "#f7f7f7"
COLOR_BAR_REMAINING = "#d9d9d9"
COLOR_BAR_DONE = "#4472c4"
COLOR_WEEKEND = "#eef0f2"
COLOR_GRID_MAJOR = "#a6a6a6"
COLOR_GRID_MINOR = "#e3e3e3"

LABEL_COL_IN = 3.0    # task-name column width, page 1 only
MARGIN_LEFT_IN = 0.35  # left of label column on page 1 / left of chart on later pages
MARGIN_RIGHT_IN = 0.25
MARGIN_TOP_IN = 1.15   # title + subtitle band, same on every page
MARGIN_BOTTOM_IN = 0.55


def page_layout(fig_w, fig_h, with_label):
    chart_h_in = fig_h - MARGIN_TOP_IN - MARGIN_BOTTOM_IN
    chart_left_in = MARGIN_LEFT_IN + (LABEL_COL_IN if with_label else 0.0)
    chart_w_in = fig_w - chart_left_in - MARGIN_RIGHT_IN
    chart_rect = (chart_left_in / fig_w, MARGIN_BOTTOM_IN / fig_h, chart_w_in / fig_w, chart_h_in / fig_h)
    label_rect = (MARGIN_LEFT_IN / fig_w, MARGIN_BOTTOM_IN / fig_h, LABEL_COL_IN / fig_w, chart_h_in / fig_h) if with_label else None
    return chart_rect, label_rect, chart_w_in


class ScheduleRow:
    def __init__(self, kind, name, assigned=None, progress=None, start=None, end=None):
        self.kind = kind  # "phase" or "task"
        self.name = name
        self.assigned = assigned
        self.progress = progress
        self.start = start
        self.end = end


def resolve_xlsx_path(explicit):
    if explicit:
        p = Path(explicit)
        if not p.exists():
            sys.exit(f"[X] --xlsx path does not exist: {p}")
        return p
    if DEFAULT_XLSX.exists():
        return DEFAULT_XLSX
    candidates = sorted(SCRIPT_DIR.parent.glob("*Gantt*hart*.xlsx"))
    if len(candidates) == 1:
        print(f"[!] Default file not found, using: {candidates[0].name}")
        return candidates[0]
    if not candidates:
        sys.exit(f"[X] Could not find a Gantt chart .xlsx in {SCRIPT_DIR.parent}. Pass --xlsx <path>.")
    sys.exit(
        "[X] Multiple candidate Gantt .xlsx files found, pass --xlsx to pick one:\n"
        + "\n".join(f"    {c.name}" for c in candidates)
    )


def load_schedule(xlsx_path):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        wb = openpyxl.load_workbook(xlsx_path, data_only=True)
    if SHEET_NAME not in wb.sheetnames:
        sys.exit(f"[X] Sheet '{SHEET_NAME}' not found in {xlsx_path.name}. Sheets present: {wb.sheetnames}")
    ws = wb[SHEET_NAME]

    header = [ws.cell(row=HEADER_ROW, column=c).value for c in range(2, 7)]
    expected = ["TASK", "ASSIGNED TO", "PROGRESS", "START", "END"]
    if header != expected:
        sys.exit(
            f"[X] Sheet layout changed: row {HEADER_ROW} cols B:F = {header}, expected {expected}. "
            "Update HEADER_ROW/FIRST_DATA_ROW in this script to match the new layout."
        )

    title = ws["B1"].value or "Gantt Chart"

    rows = []
    r = FIRST_DATA_ROW
    while r <= ws.max_row:
        name = ws.cell(row=r, column=2).value
        r += 1
        if name is None:
            continue
        name = str(name).strip()
        if not name:
            continue
        if STOP_MARKER in name.lower():
            break

        assigned = ws.cell(row=r - 1, column=3).value
        progress = ws.cell(row=r - 1, column=4).value
        start = ws.cell(row=r - 1, column=5).value
        end = ws.cell(row=r - 1, column=6).value
        start = start.date() if isinstance(start, datetime) else start
        end = end.date() if isinstance(end, datetime) else end

        if assigned is None and progress is None and start is None and end is None:
            rows.append(ScheduleRow("phase", name))
            continue

        if start and end and end < start:
            print(f"[!] Task '{name}': END ({end}) is before START ({start}) -- skipping its bar.")
            start = end = None

        rows.append(ScheduleRow("task", name, assigned, progress, start, end))

    if not rows:
        sys.exit(f"[X] No task rows found starting at row {FIRST_DATA_ROW}. Check the sheet layout.")
    return title, rows


def compute_page_windows(rows, weeks_per_page, page_size_in):
    dated = [r for r in rows if r.kind == "task" and r.start and r.end]
    if not dated:
        sys.exit("[X] No tasks have both START and END dates -- nothing to plot.")
    min_start = min(r.start for r in dated)
    max_end = max(r.end for r in dated)

    page_start = min_start - timedelta(days=min_start.weekday())  # snap to Monday on/before
    page1_days = weeks_per_page * 7

    fig_w, fig_h = page_size_in
    _, _, page1_chart_w_in = page_layout(fig_w, fig_h, with_label=True)
    _, _, cont_chart_w_in = page_layout(fig_w, fig_h, with_label=False)
    inches_per_day = page1_chart_w_in / page1_days
    cont_days = max(1, int(cont_chart_w_in / inches_per_day))

    win_start = page_start
    win_end = win_start + timedelta(days=page1_days - 1)
    windows = [(win_start, win_end)]
    while win_end < max_end:
        win_start = win_end + timedelta(days=1)
        win_end = win_start + timedelta(days=cont_days - 1)
        windows.append((win_start, win_end))
    return windows, min_start, max_end


def next_revision(out_dir):
    pattern = re.compile(r"^gantt_chart_rev(\d+)_")
    found = []
    for f in out_dir.glob("gantt_chart_rev*_*.pdf"):
        m = pattern.match(f.name)
        if m:
            found.append(int(m.group(1)))
    return (max(found) + 1) if found else 0


def render_page(rows, win_start, win_end, page_num, total_pages, title, rev, pdf, page_size_in):
    n_rows = len(rows)
    fig_w, fig_h = page_size_in
    with_label = page_num == 1
    chart_rect, label_rect, _ = page_layout(fig_w, fig_h, with_label)

    fig = plt.figure(figsize=(fig_w, fig_h))
    ax_chart = fig.add_axes(chart_rect)
    ax_labels = fig.add_axes(label_rect, sharey=ax_chart) if with_label else None

    fig.suptitle(f"{title} -- Gantt Chart", fontsize=13, fontweight="bold", x=0.03, ha="left", y=0.97)
    subtitle = (
        f"rev {rev}  |  Page {page_num} of {total_pages}  |  "
        f"{win_start:%b %d, %Y} - {win_end:%b %d, %Y}  |  "
        f"exported {datetime.now():%m/%d/%Y %H:00}"
    )
    if not with_label:
        subtitle += "  |  continued -- task list on page 1"
    fig.text(0.03, 0.925, subtitle, fontsize=8.5, color="#444444", ha="left")

    win_s = mdates.date2num(win_start)
    win_e = mdates.date2num(win_end) + 1

    task_idx = 0
    for i, row in enumerate(rows):
        y = -i
        if row.kind == "phase":
            if ax_labels is not None:
                ax_labels.axhspan(y - 0.5, y + 0.5, color=COLOR_PHASE_BAND, zorder=0)
                ax_labels.text(0.02, y, row.name, fontsize=8, fontweight="bold", va="center", ha="left")
            ax_chart.axhspan(y - 0.5, y + 0.5, color=COLOR_PHASE_BAND, zorder=0)
            continue

        if task_idx % 2 == 1:
            if ax_labels is not None:
                ax_labels.axhspan(y - 0.5, y + 0.5, color=COLOR_ROW_ALT, zorder=0)
            ax_chart.axhspan(y - 0.5, y + 0.5, color=COLOR_ROW_ALT, zorder=0)
        task_idx += 1

        if ax_labels is not None:
            label = row.name
            if not (row.start and row.end):
                label += "  (unscheduled)"
            ax_labels.text(0.05, y, label, fontsize=7, va="center", ha="left")

        if not (row.start and row.end):
            continue

        s = mdates.date2num(row.start)
        e = mdates.date2num(row.end) + 1
        vis_s, vis_e = max(s, win_s), min(e, win_e)
        if vis_e <= vis_s:
            continue

        ax_chart.barh(y, vis_e - vis_s, left=vis_s, height=0.62, color=COLOR_BAR_REMAINING, zorder=2)

        progress = row.progress if isinstance(row.progress, (int, float)) else 0
        progress = max(0.0, min(1.0, progress))
        fill_e = s + (e - s) * progress
        fill_vis_e = min(fill_e, vis_e)
        if fill_vis_e > vis_s:
            ax_chart.barh(y, fill_vis_e - vis_s, left=vis_s, height=0.62, color=COLOR_BAR_DONE, zorder=3)

    if ax_labels is not None:
        for spine in ax_labels.spines.values():
            spine.set_visible(False)
        ax_labels.set_xticks([])
        ax_labels.set_xlim(0, 1)
    ax_chart.set_ylim(-(n_rows - 0.5), 0.5)

    day = win_start
    while day <= win_end:
        if day.weekday() >= 5:
            ax_chart.axvspan(mdates.date2num(day), mdates.date2num(day) + 1, color=COLOR_WEEKEND, zorder=1)
        day += timedelta(days=1)

    ax_chart.set_xlim(win_s, win_e)
    ax_chart.xaxis_date()
    ax_chart.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.MO))
    ax_chart.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax_chart.xaxis.set_minor_locator(mdates.DayLocator())
    ax_chart.grid(which="major", axis="x", color=COLOR_GRID_MAJOR, linewidth=0.8, zorder=0)
    ax_chart.grid(which="minor", axis="x", color=COLOR_GRID_MINOR, linewidth=0.4, zorder=0)
    ax_chart.tick_params(axis="x", labelsize=7.5, top=True, labeltop=True, bottom=True, labelbottom=True)
    ax_chart.set_yticks([])
    for spine in ["left", "right", "top"]:
        ax_chart.spines[spine].set_visible(False)

    pdf.savefig(fig)
    plt.close(fig)


def write_manifest(out_path, xlsx_path, rev, weeks_per_page, page_size_name, windows, pdf_name, min_start, max_end):
    lines = []
    lines.append("GANTT CHART EXPORT MANIFEST")
    lines.append("=" * 72)
    lines.append(f"Source        : {xlsx_path.name}")
    lines.append(f"Revision      : rev{rev}")
    lines.append(f"Exported      : {datetime.now():%m/%d/%Y %H:00}")
    lines.append(f"Timeline      : {min_start:%b %d, %Y} - {max_end:%b %d, %Y}")
    lines.append(f"Page size     : {page_size_name}")
    lines.append(f"Weeks on pg 1 : {weeks_per_page}  (task list eats width; later pages fit more days at the same scale)")
    lines.append(f"Pages         : {len(windows)}")
    lines.append(f"File          : {pdf_name}")
    lines.append("")
    lines.append("Pages are in order left to right -- print and lay them out to read the full timeline.")
    lines.append("Trim each page's blank side margin before taping for a seamless join.")
    lines.append("")
    lines.append(f"{'PAGE':<6}{'DAYS':<6}{'DATE RANGE'}")
    lines.append("-" * 72)
    for i, (ws_, we_) in enumerate(windows, start=1):
        days = (we_ - ws_).days + 1
        lines.append(f"{i:<6}{days:<6}{ws_:%b %d, %Y} - {we_:%b %d, %Y}")
    out_path.write_text("\n".join(lines), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Export the JEA Gantt chart to a tiled, multi-page landscape PDF.")
    parser.add_argument("--xlsx", help="Path to the Gantt chart .xlsx (default: auto-detect next to this folder).")
    parser.add_argument("--weeks-per-page", type=int, default=3, help="Calendar weeks covered by each PDF page (default: 3).")
    parser.add_argument("--page-size", choices=sorted(PAGE_SIZES_IN), default="letter", help="Landscape page size (default: letter).")
    args = parser.parse_args()

    xlsx_path = resolve_xlsx_path(args.xlsx)
    title, rows = load_schedule(xlsx_path)
    page_size_in = PAGE_SIZES_IN[args.page_size]
    windows, min_start, max_end = compute_page_windows(rows, args.weeks_per_page, page_size_in)

    out_dir = SCRIPT_DIR
    rev = next_revision(out_dir)
    now = datetime.now()
    date_str = f"{now.month}.{now.day}.{now.strftime('%y')}"
    hour_str = f"{now.hour:02d}"
    base = f"gantt_chart_rev{rev}_{date_str}_{hour_str}"

    total = len(windows)
    pdf_name = f"{base}.pdf"
    with PdfPages(out_dir / pdf_name) as pdf:
        for i, (win_start, win_end) in enumerate(windows, start=1):
            render_page(rows, win_start, win_end, i, total, title, rev, pdf, page_size_in)
            print(f"[OK] page {i} of {total}  ({win_start:%b %d} - {win_end:%b %d})")
    print(f"[OK] {pdf_name}")

    manifest_name = f"{base}_manifest.txt"
    write_manifest(out_dir / manifest_name, xlsx_path, rev, args.weeks_per_page, args.page_size, windows, pdf_name, min_start, max_end)
    print(f"[OK] {manifest_name}")
    print(f"\nDone: {total}-page PDF written to {out_dir / pdf_name} as revision {rev}.")


if __name__ == "__main__":
    main()
