---
name: qa-to-flows
description: "Turn one registry scope into an approved flow list inside its scope file, with an approval gate before scenario work begins."
---

# qa-to-flows

Turn one registry scope into an approved flow list inside its scope file.

## Inputs

- `scope` (required): one module or submenu code from `qa/app-map.md` (e.g. `ELM` or `ELM-TXT`).
- `--deep` (optional): for tiny sites, register modules and generate flows in one pass without forcing two approval gates.

## Process

1. Read `qa/app-map.md` and resolve the scope: its routes, visible-to personas, and confidence.
2. Walk the scope's routes with `playwright-cli` snapshots to discover user journeys (one flow per goal: create, list, update, delete, filter, and so on).
3. Create `qa/<scope>/<scope>.scenario.md` from the bundled template in `references/scope-scenario-template.md` with every flow at status Proposed.
4. Present the flow list to the user for approval. Record each verdict in the file: Approved, or Rejected with a reason. Rejected flows stay visible.
5. With `--deep`: also write any missing registry entries into `qa/app-map.md` in the same run, then continue at step 2.

## Outputs

- `qa/<scope>/<scope>.scenario.md` with flows carrying Proposed, Approved, or Rejected status.

## Rules

- One scope per run; never generate flows for two modules at once.
- Approval is recorded in the markdown before any scenario work begins.
- Snapshot-verified flows only; no guessing from URLs.
- English prompts and artifacts.
