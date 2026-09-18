---
name: qa-explore
description: "Register a web application's modules, submenus, and routes into a persona-scoped registry (qa/app-map.md) using snapshot-verified browser exploration."
---

# qa-explore

Register an application's modules, submenus, and routes into a persona-scoped registry (`qa/app-map.md`).

## Inputs

- `url` (required): base URL of the application.
- `persona` (required): one role or credential set for this run (e.g. `admin`, `guest`). Each run covers exactly one persona.
- `credentials` (required unless the persona needs no login): environment variable names holding the login secrets, e.g. `E2E_ADMIN_EMAIL`. Values never enter markdown.
- `module` (optional): one module or submenu to narrow the scope.
- `routes` (optional): known routes to seed exploration.

## Process

1. Open `url` in a fresh `playwright-cli` session for this persona. If login is needed, sign in using the credential env vars.
2. Capture snapshots (`snapshot`, `find` for menus and navigation) to discover modules, submenus, and routes. Verify every entry from an observed snapshot: never infer a module from a URL pattern.
3. If `qa/app-map.md` exists, merge: add new modules and submenus, annotate `visible-to` with this persona, update the coverage table. Never delete another persona's findings.
4. If it does not exist, create it from the bundled template in `references/app-map-template.md`.
5. Record anything the user mentioned but you could not observe in Suspected gaps, with persona and reason.
6. Update Completeness: list this persona as covered. Claim global completeness only when every known persona is covered.

## Outputs

- `qa/app-map.md` created or merged.

## Rules

- Snapshot-verified only: every registry entry traces to an observed snapshot.
- Completeness is claimed per-persona, never globally from one run.
- No secret values in markdown, only environment variable names.
- English prompts and artifacts.
