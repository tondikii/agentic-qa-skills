# Skill convention

Every skill in this suite lives in its own folder under `skills/` and follows the same shape so skills install cleanly on any harness.

## Folder shape

```
skills/qa-<name>/
├── SKILL.md            ← the skill prompt (entry point, with name/description frontmatter)
├── references/         ← supporting files the prompt points at (templates, checklists)
└── scripts/            ← helper scripts the skill runs (validators, converters)
```

Shared tooling also lives in `tools/` at the repo root, and worked examples in `examples/`. Skills never depend on repo-root paths: every template and script a skill needs is bundled inside its own folder so installer copies stay self-contained.

## SKILL.md structure

1. YAML frontmatter with `name` and `description` (required by the Agent Skills spec and the `skills` installer).
2. Name and one-line purpose.
3. Inputs (required and optional, with defaults).
4. Process (numbered steps the agent follows in order).
5. Outputs (which files are written or updated, and how).
6. Rules (hard constraints: verification over guessing, no secrets in markdown, refusal conditions).

## Rules for all skills

- All prompts, templates, and artifacts in English.
- Skill names use the `qa-` prefix to avoid collision with generic skills.
- Skills communicate only through the `qa/` file schemas, never through private state.
- Credentials are referenced by environment variable name only, never stored in markdown.
- Each skill is validated by dogfooding it on a real demo site before its ticket closes.
