# agentic-qa-skills

Harness-agnostic skills for agentic browser testing: from persona-scoped exploration to executable scenarios, reports, and spreadsheets.

## Installation

Requires `playwright-cli` (`npm install -g @playwright/cli`) on the machine running the agent, and `openpyxl` (`pip install openpyxl`) for spreadsheet output.

**Any agent (recommended):**

```sh
npx skills@latest add tondikii/agentic-qa-skills
```

Pick the skills you want and which agents to install them on.

**Claude Code (managed bundle):**

```sh
/plugin install agentic-qa-skills@tondikii/agentic-qa-skills
```

**Manual:** copy any folder under `skills/` into your project's skill directory. Each skill is self-contained (templates, checklists, and scripts bundled inside).

## Skills

| Skill | What it does |
| ----- | ------------ |
| `qa-explore` | Register modules, submenus, and routes into a persona-scoped `qa/app-map.md` |
| `qa-to-flows` | Turn one registry scope into an approved flow list |
| `qa-to-scenario` | Turn approved flows into Gherkin scenarios, preparation items, and a report |
| `qa-execute` | Run scenarios live via `playwright-cli`, write results back |
| `qa-to-sheets` | Convert scope markdown into a tabbed `.xlsx` workbook |

Run them in order: explore → flows → scenario → execute → sheets. A sixth skill (`to-code`, Playwright BDD generation) is planned; every scenario written now is already convertible.

## Where things live

- `skills/` — the installable skills (each self-contained).
- `tools/` — shared copies of the helper scripts (`md2xlsx.py`, `bddcheck.py`).
- `templates/` — shared copies of the file schemas.
- `examples/todomvc/` — worked example to copy from.
- `CONTEXT.md` — domain glossary.
- `docs/adr/`, `docs/research/`, `docs/agents/` — decisions, research, agent config.

## Plan and tickets

- Spec: [#1](https://github.com/tondikii/agentic-qa-skills/issues/1)
- Foundation: [#2](https://github.com/tondikii/agentic-qa-skills/issues/2) (closed)
- Skills: [#3](https://github.com/tondikii/agentic-qa-skills/issues/3) (closed), [#4](https://github.com/tondikii/agentic-qa-skills/issues/4) (closed), [#5](https://github.com/tondikii/agentic-qa-skills/issues/5) (closed), [#6](https://github.com/tondikii/agentic-qa-skills/issues/6) (closed), [#7](https://github.com/tondikii/agentic-qa-skills/issues/7) (closed)
