# Scope: Todo list (TDL)

- App map: ../app-map.md
- Module: Todo list

## Flows

| ID | Flow | Status | Notes |
| -- | ---- | ------ | ----- |
| TDL-ADD | Add todo | Approved | verified via snapshot textbox e8 |
| TDL-TOG | Toggle todo | Approved | verified via snapshot checkbox e21 |
| TDL-DEL | Delete todo | Proposed | delete control not visible until hover; needs confirmation |

## Scenarios

| ID | Title | Type | Suite | Priority | Persona | Readiness | Status | Exec Time |
| -- | ----- | ---- | ----- | -------- | ------- | --------- | ------ | --------- |
| TDL-ADD-001 | Add a todo item | positive | smoke | P0 | guest | Ready | Passed | 4s |
| TDL-ADD-002 | Add todo with empty text | negative | regression | P2 | guest | Ready | Not Run | - |
| TDL-TOG-001 | Mark todo complete | positive | smoke | P1 | guest | Ready | Not Run | - |

## Gherkin

### TDL-ADD-001: Add a todo item

```gherkin
@TDL-ADD-001 @smoke
Scenario: Add a todo item
  Given the todo list is empty
  When I add "Buy milk"
  Then "Buy milk" appears in the list
```

### TDL-ADD-002: Add todo with empty text

```gherkin
@TDL-ADD-002 @regression
Scenario: Add todo with empty text
  Given the todo list is empty
  When I submit an empty todo
  Then no item is added to the list
```

### TDL-TOG-001: Mark todo complete

```gherkin
@TDL-TOG-001 @smoke
Scenario: Mark todo complete
  Given "Buy milk" is in the list
  When I toggle "Buy milk"
  Then "Buy milk" is marked complete
```
