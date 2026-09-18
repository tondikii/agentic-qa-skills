# Reject markitdown for sheets output

`qa-to-sheets` needs markdown tables converted into a multi-tab `.xlsx` workbook. Research verified `markitdown` is ingest-only (many formats to Markdown for LLM consumption) and cannot write spreadsheets, so we ship a small `openpyxl`-based converter script instead.

## Considered Options

- `markitdown`: rejected, wrong direction (reads spreadsheets, never writes them).
- CSV per file: rejected, loses the one-workbook-one-tab-per-file shape stakeholders were promised.
