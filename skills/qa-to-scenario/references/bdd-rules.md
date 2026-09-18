# qa-to-scenario: BDD rules checklist

Apply to every scenario before finishing:

- [ ] Title is unique within the scope file.
- [ ] Steps are declarative (`When I submit the form`), never click-type chains.
- [ ] No secrets, credentials, or absolute URLs inside Gherkin steps.
- [ ] No markdown formatting (bold, links, line breaks) inside steps.
- [ ] ID rendered as `@TAG` directly above the `Scenario:` line, plus `@<suite>`.
- [ ] `Then` states an observable expectation.

Run the bundled validator (`scripts/bddcheck.py <scope>.scenario.md`) to verify mechanically.
