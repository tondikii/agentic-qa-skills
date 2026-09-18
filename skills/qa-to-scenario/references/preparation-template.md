# Preparation: <Scope name>

## Test data

| ID | Item | Owner | Done |
| -- | ---- | ----- | ---- |
| PREP-<MOD>-001 | <what data must exist> | agent \| human | [ ] |

## Credentials

| ID | Item | Owner | Done |
| -- | ---- | ----- | ---- |
| PREP-<MOD>-002 | <ENV_VAR_NAME> available in `.env` | human | [ ] |

Credential items name the environment variable only, never the value.

## Environment

| ID | Item | Owner | Done |
| -- | ---- | ----- | ---- |
| PREP-<MOD>-003 | <URL, browser, seed command> | agent \| human | [ ] |

## Seed and reset

| ID | Item | Owner | Done |
| -- | ---- | ----- | ---- |
| PREP-<MOD>-004 | <how to reach a clean state> | agent \| human | [ ] |

Agent-owned items are attempted automatically at execution preflight. Human-owned items block with instructions.
