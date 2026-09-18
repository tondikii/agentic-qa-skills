---
name: qa-execute
description: "Run selected scenarios live through playwright-cli and write status, execution time, and report updates back into the markdown."
---

# qa-execute

Run selected scenarios live through `playwright-cli` and write results back into the markdown.

## Inputs

- `scope` (required): scope code matching `qa/<scope>/<scope>.scenario.md`.
- Selector, one of (default: everything):
  - `file`: run the whole scope file.
  - `ids`: one ID pattern, e.g. `USR-CRT-*` (prefix match on scenario IDs).
  - `filter`: tag-style selection over suite, type, status, or persona (e.g. `suite=smoke`, `status=Failed`, `persona=admin`). Repeatable.
- `rerun` (optional): when true, keep Passed results and rerun Failed, Blocked, and Not Run only. On by default.
- `--persona` (optional): run only this persona's scenarios.

## Process

1. Load the scope's scenario table, preparation file, and report.
2. Resolve the selection: apply file/ids/filter plus persona. With `rerun` on, drop Passed scenarios from the set.
3. Preflight: for every persona in the selection, check its credential env vars exist and agent-owned preparation items are done. On any gap, stop before the first scenario and print setup instructions naming the missing var or PREP item. Never print secret values.
4. For each scenario: replay its Gherkin steps live in a `playwright-cli` session, one scenario at a time. Mark In Progress, then Passed or Failed with the observed error. Time each run.
5. Record the emitted Playwright steps per scenario for the future code skill.
6. Write Status and Exec Time back into the scenario table.
7. Rewrite the report: header (scope, date, env, persona), summary counts with pass rate and total duration, per-scenario rows, failures with the exact rerun command, and an appended dated history entry.
8. Skipped scenarios (outside the selection) keep their prior status; scenarios never selected stay Not Run.

## Outputs

- `qa/<scope>/<scope>.scenario.md` with fresh Status and Exec Time.
- `qa/<scope>/report.md` rewritten with this run's results and history.

## Rules

- Missing credentials or preparation stop the run before any scenario, with setup instructions.
- A Blocked scenario names its blocking PREP item; it is never force-run.
- No secret values in markdown, only environment variable names.
- English prompts and artifacts.
