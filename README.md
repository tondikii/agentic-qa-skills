# agentic-qa-skills

Harness-agnostic skill suite for agentic browser testing: from persona-scoped exploration to executable scenarios, reports, and spreadsheets.

## What this repo builds

Five installable skills (`qa-explore`, `qa-to-flows`, `qa-to-scenario`, `qa-execute`, `qa-to-sheets`) that carry a web-testing effort from a URL to living markdown artifacts under `qa/`, plus a deferred sixth skill (`to-code`, Playwright BDD generation) whose inputs are guaranteed convertible.

## Where things live

- `CONTEXT.md` — domain glossary (source of truth for terms like app-map, flow, scenario, persona).
- `docs/adr/` — architecture decisions (e.g. persona-scoped exploration, markitdown rejection).
- `docs/research/` — background research (playwright-cli API, BDD metadata).
- `docs/agents/` — agent skill configuration (issue tracker, domain doc rules).
- `qa/` — test artifacts produced by the skills (created during implementation).

## Plan and tickets

- Spec: [#1](https://github.com/tondikii/agentic-qa-skills/issues/1)
- Foundation: [#2](https://github.com/tondikii/agentic-qa-skills/issues/2)
- Skills: [#3](https://github.com/tondikii/agentic-qa-skills/issues/3) (qa-explore), [#4](https://github.com/tondikii/agentic-qa-skills/issues/4) (qa-to-flows), [#5](https://github.com/tondikii/agentic-qa-skills/issues/5) (qa-to-scenario), [#6](https://github.com/tondikii/agentic-qa-skills/issues/6) (qa-execute), [#7](https://github.com/tondikii/agentic-qa-skills/issues/7) (qa-to-sheets)
