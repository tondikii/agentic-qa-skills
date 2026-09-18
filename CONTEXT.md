# Agentic QA Skills

Glossary for the harness-agnostic browser-testing skill suite built in this repo: persona-scoped exploration down to executable scenarios, with preparation lists and reports.

## Language

**app-map**:
The registry of an application's modules, submenus, and routes, written by `qa-explore` and scoped per persona.
_Avoid_: sitemap, inventory

**module**:
A top-level area of the application under test (e.g. user-management).
_Avoid_: domain, bounded context

**submenu**:
A section within a module (e.g. user list), carrying which personas can see it.
_Avoid_: child menu, tab

**scope**:
One module or submenu under test, mapping to one folder under `qa/` holding its scenario, preparation, and report files.
_Avoid_: target, subject

**flow**:
One user journey through a scope that becomes testable scenarios once approved.
_Avoid_: journey, use case

**scenario**:
One testable behavior of a flow, written as Gherkin with its expectation in `Then`, carrying a stable ID.
_Avoid_: test case

**persona**:
A credential set used during exploration and execution (e.g. `admin`); scenarios declare which persona they run as, or `any`.
_Avoid_: actor, profile

**preparation**:
The per-scope list of what must exist before scenarios can run: test data, credentials, environment, seed and reset steps.
_Avoid_: prerequisites, fixtures

**readiness**:
Whether a scenario may run yet: `Ready`, or `Needs-Setup` linked to its blocking preparation items.
_Avoid_: preparedness

**status**:
The last execution outcome of a scenario: `Not Run`, `In Progress`, `Passed`, `Failed`, `Blocked`, or `Skipped`.
_Avoid_: state, result

**report**:
The per-scope record of execution outcomes: summary counts, per-scenario results, and failure details.
_Avoid_: test report, results
