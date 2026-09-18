---
name: qa-to-sheets
description: "Convert a scope folder's markdown artifacts into one local tabbed .xlsx workbook, one tab per file."
---

# qa-to-sheets

Convert a scope folder's markdown artifacts into one local tabbed workbook.

## Inputs

- `scope` (required): scope code matching `qa/<scope>/`.
- `--output` (optional): workbook path. Default `qa/<scope>/<scope>.xlsx`.

## Process

1. Verify the scope folder holds its scenario file, preparation file, and report.
2. Run the bundled converter (`scripts/md2xlsx.py qa/<scope> -o <output>`). Requires `openpyxl` (`pip install openpyxl`).
3. Open the workbook and confirm: one tab per markdown file, tables as real cells, Gherkin sections as readable blocks.
4. Report the workbook path to the user.

## Outputs

- `<scope>.xlsx` with one tab per markdown file.

## Rules

- Repeat runs over unchanged inputs produce an identical workbook (cell-identical; file bytes may differ by embedded metadata).
- The workbook lands inside `qa/<scope>/` by default, next to its sources.
- English prompts and artifacts.
