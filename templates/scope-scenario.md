# Scope: <Scope name> (<SCOPE>)

- App map: ../app-map.md
- Module: <module name>

## Flows

| ID | Flow | Status | Notes |
| -- | ---- | ------ | ----- |
| <SCOPE-FLOW> | <flow name> | Proposed \| Approved \| Rejected | <reason for rejection, else -> |

## Scenarios

| ID | Title | Type | Suite | Priority | Persona | Readiness | Status | Exec Time |
| -- | ----- | ---- | ----- | -------- | ------- | --------- | ------ | --------- |
| <SCOPE-FLOW-001> | <title> | positive \| negative \| edge | smoke \| sanity \| regression | P0 \| P1 \| P2 \| P3 | <persona \| any \| n/a> | Ready \| Needs-Setup <PREP-ID> | Not Run \| In Progress \| Passed \| Failed \| Blocked \| Skipped | <duration or -> |

## Gherkin

### <SCOPE-FLOW-001>: <title>

```gherkin
@<SCOPE-FLOW-001> @<suite>
Scenario: <title>
  Given <precondition>
  When <action>
  Then <observable expectation>
```
