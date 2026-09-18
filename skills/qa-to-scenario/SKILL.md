---
name: qa-to-scenario
description: "Turn approved flows into a scenario table with Gherkin sections, preparation items, and an empty report, enforcing BDD convertibility rules."
---

# qa-to-scenario

Turn approved flows into scenarios, preparation items, and an empty report.

## Inputs

- `scope` (required): scope code matching `qa/<scope>/<scope>.scenario.md` (e.g. `elm-txt`).
- `--persona` (optional): limit generation to these personas (e.g. `admin,staff`). When omitted, inherit the scope's `visible-to` personas from `qa/app-map.md`. When the registry implies more than one persona, ask the user which ones apply before generating.

## Process

1. Read the scope file. Refuse when any flow the user asked about is not Approved: name the unapproved flows and stop.
2. Assign IDs in `<MOD>-<FLOW>-###` form: MOD 2-4 uppercase letters from the registry, FLOW 3-6 uppercase letters (first-word slug of the flow), `###` zero-padded sequence restarting per flow. IDs are never reused after delete.
3. Write the scenario table in fixed column order: ID, Title, Type (positive/negative/edge), Suite (smoke/sanity/regression), Priority (P0-P3), Persona (role, `any`, or `n/a`), Readiness (Ready, or Needs-Setup with PREP link), Status (default Not Run), Exec Time (default `-`).
4. Write one Gherkin section per scenario below the table, each tagged `@<ID> @<suite>`, declarative Given/When/Then with the expectation in Then.
5. Write `preparation.md` from the bundled template in `references/preparation-template.md`: one PREP-ID item per setup need across test-data, credentials (env var names only), environment, and seed/reset, each with agent/human owner.
6. Write the empty `report.md` from the bundled template in `references/report-template.md`.
7. Enforce the five BDD rules on every scenario: unique titles; declarative steps (no click-type chains); no secrets or URLs in Gherkin; no markdown formatting inside steps; ID as `@TAG` above the Scenario. Fix violations before finishing.

## Outputs

- `qa/<scope>/<scope>.scenario.md` enriched with the scenario table and Gherkin sections.
- `qa/<scope>/preparation.md` with PREP-ID items.
- `qa/<scope>/report.md` empty, in the report shape.

## Rules

- Refuse unapproved flows with a clear message naming them.
- Boundary cases map to Type `edge`; access-control cases map to Type `negative` plus Persona.
- No secret values in any file, only environment variable names.
- English prompts and artifacts.
