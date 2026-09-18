"""Convert a QA scope folder (scenario, preparation, report markdown) into a tabbed .xlsx workbook.

Usage:
    python md2xlsx.py <scope-dir> [-o <workbook.xlsx>]

Each markdown file becomes one tab: the table lands as real cells,
per-scenario Gherkin sections as readable text blocks.
"""

import argparse
import re
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font

TABLE_SEPARATOR = re.compile(r"^\|[\s\-\|:]+\|$")
GHERKIN_HEADING = re.compile(r"^###\s+(.+)$")
FAILURE_HEADING = re.compile(r"^###\s+(.+)$")
FENCE = "```"


def parse_table(lines):
    """Parse the first markdown table found in lines. Returns (header, rows)."""
    header, rows = [], []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and i + 1 < len(lines) and TABLE_SEPARATOR.match(lines[i + 1].strip()):
            header = [c.strip() for c in line.strip("|").split("|")]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            break
        i += 1
    return header, rows


def parse_sections(lines, heading_pattern, fenced=True):
    """Collect ### sections as (title, body). Fenced blocks kept verbatim."""
    sections, title, buf, in_fence = [], None, [], False
    for line in lines:
        stripped = line.strip()
        if fenced and stripped.startswith(FENCE):
            in_fence = not in_fence
            buf.append(line.rstrip("\n"))
            continue
        match = heading_pattern.match(stripped) if not in_fence else None
        if match:
            if title is not None:
                sections.append((title, "\n".join(buf).strip()))
            title, buf = match.group(1), []
        elif title is not None:
            buf.append(line.rstrip("\n"))
    if title is not None:
        sections.append((title, "\n".join(buf).strip()))
    return sections


def write_table(ws, header, rows, start_row=1):
    bold = Font(bold=True)
    for col, value in enumerate(header, start=1):
        cell = ws.cell(row=start_row, column=col, value=value)
        cell.font = bold
    for r, row in enumerate(rows, start=start_row + 1):
        for col, value in enumerate(row, start=1):
            ws.cell(row=r, column=col, value=value)
    for col in ws.columns:
        width = max((len(str(c.value)) for c in col if c.value), default=10)
        ws.column_dimensions[col[0].column_letter].width = min(width + 2, 60)
    return start_row + len(rows) + 2


def convert_scope(scope_dir, output):
    scope_dir = Path(scope_dir)
    files = sorted(scope_dir.glob("*.md"))
    if not files:
        raise SystemExit(f"No markdown files in {scope_dir}")

    wb = Workbook()
    wb.remove(wb.active)
    for path in files:
        ws = wb.create_sheet(path.stem[:31])
        lines = path.read_text(encoding="utf-8").splitlines()
        row = 1
        for table_start in find_tables(lines):
            header, rows = table_start
            row = write_table(ws, header, rows, start_row=row)
        if path.name.endswith(".scenario.md"):
            for title, body in parse_sections(lines, GHERKIN_HEADING):
                ws.cell(row=row, column=1, value=title).font = Font(bold=True)
                row += 1
                ws.cell(row=row, column=1, value=body)
                row += 2
        elif path.name == "report.md":
            for title, body in parse_sections(lines, FAILURE_HEADING):
                ws.cell(row=row, column=1, value=title).font = Font(bold=True)
                row += 1
                ws.cell(row=row, column=1, value=body)
                row += 2
    wb.save(output)
    print(f"Wrote {output} ({len(files)} tabs)")


def find_tables(lines):
    """Yield (header, rows) for every markdown table in lines."""
    tables = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("|") and i + 1 < len(lines) and TABLE_SEPARATOR.match(lines[i + 1].strip()):
            header = [c.strip() for c in line.strip("|").split("|")]
            rows, i = [], i + 2
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            tables.append((header, rows))
            continue
        i += 1
    return tables


def main(argv=None):
    parser = argparse.ArgumentParser(description="Convert a QA scope folder to a tabbed workbook.")
    parser.add_argument("scope_dir", help="Folder holding the scope markdown files")
    parser.add_argument("-o", "--output", default=None, help="Workbook path (default: <scope-dir>/<scope>.xlsx)")
    args = parser.parse_args(argv)
    scope_dir = Path(args.scope_dir)
    output = args.output or str(scope_dir / f"{scope_dir.name}.xlsx")
    convert_scope(scope_dir, output)


if __name__ == "__main__":
    main()
