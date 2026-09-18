# qa-execute: selector reference

Selection resolves in this order:

1. Start with every scenario in the scope file.
2. Apply the selector:
   - `file` → keep all.
   - `ids: <PREFIX>*` → keep IDs starting with `<PREFIX>`.
   - `filter: <column>=<value>` → keep matching rows. Columns: suite, type, status, persona. Repeatable; all filters must match.
3. Apply `--persona` when given.
4. Apply `rerun` (default on): drop Passed scenarios.

Examples:

- Whole file: `file`
- One flow: `ids: ELM-TXT-SUB-*`
- Smoke gate: `filter: suite=smoke`
- Retry failures: `filter: status=Failed` (or rely on default rerun)
- Admin only: `--persona admin` with `filter: suite=regression`
