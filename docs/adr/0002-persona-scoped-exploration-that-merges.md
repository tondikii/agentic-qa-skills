# Persona-scoped exploration that merges

A single exploration run cannot see modules hidden by role, feature flag, or data conditions. So each `qa-explore` run binds to one persona, re-runs merge (adding modules and annotating `visible-to`, never deleting), and completeness is claimed per-persona only until every known persona is covered.

## Consequences

`qa-to-scenario` inherits `visible-to` as the default persona filter, `qa-execute` preflights per-persona credentials, and the registry carries an explicit persona-coverage table plus a suspected-gaps section instead of ever claiming to be globally complete.
