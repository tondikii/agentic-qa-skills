# Skill convention

Every skill in this suite lives in its own folder at the repo root and follows the same shape so skills install cleanly on any harness.

## Folder shape

```
qa-<name>/
├── SKILL.md            ← the skill prompt (entry point)
└── references/         ← supporting files the prompt points at
    ├── <topic>.md      ← templates, schemas, checklists
    └── ...
```

Shared tooling lives in `tools/` at the repo root. Worked examples live in `examples/`.

## SKILL.md structure

1. Name and one-line purpose.
2. Inputs (required and optional, with defaults).
3. Process (numbered steps the agent follows in order).
4. Outputs (which files are written or updated, and how).
5. Rules (hard constraints: verification over guessing, no secrets in markdown, refusal conditions).

## Rules for all skills

- All prompts, templates, and artifacts in English.
- Skill names use the `qa-` prefix to avoid collision with generic skills.
- Skills communicate only through the `qa/` file schemas, never through private state.
- Credentials are referenced by environment variable name only, never stored in markdown.
- Each skill is validated by dogfooding it on a real demo site before its ticket closes.
