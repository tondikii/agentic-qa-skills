# Gherkin/BDD Scenario Metadata — Best Practices for Agentic Browser Testing (playwright-bdd compatible)

Research date: 2026-09-18. Target: `vitalets/playwright-bdd` (BDD on Playwright Test runner; `.feature` → generated Playwright tests via `bddgen`).

## 1. Required Gherkin structure

One `.feature` file = exactly one `Feature:` header. playwright-bdd supports all standard Gherkin keywords (incl. `Rule`, `Doc String`, `Data Table`, i18n).

```gherkin
@suite:checkout
Feature: Shopping Cart
  In order to purchase items
  As a registered customer
  I want to manage my cart before checkout
  # ^ free-text description lines under Feature: are parsed but NOT executed. Use for "why".

  Background:
    Given the database has been seeded with test products
    And I am logged in as a verified buyer
  # Rules:
  # - max ONE Background per file, placed after Feature description, before first Scenario
  # - keep to 3-4 steps; it runs before EVERY scenario in the file
  # - if only some scenarios need setup, use tagged hooks or split files instead

  @TC-001 @smoke @positive
  Scenario: Add a single item to an empty cart
    Given the cart is empty
    When I add "Wireless Headphones" to the cart
    Then the cart should contain 1 item
    And the total should be "$79.99"

  @TC-002 @regression
  Scenario Outline: User registration with various email domains
    Given the registration form is open
    When I register with email "<email>" and password "Str0ngP@ss99"
    Then a confirmation email is sent to "<email>"
    # NOTE: recommended playwright-bdd pattern — put a <column> placeholder
    # in the Outline name so each generated test gets a unique, stable title
    # e.g. `Scenario Outline: Registration with <email>` (see section 5).

    Examples:
      | email                 |
      | alice@gmail.com       |
      | bob.smith@company.org |
```

Key structural rules (Cucumber + playwright-bdd enforced):

| Construct | Rule |
|---|---|
| `Feature:` | Exactly one per file, first non-comment/non-tag line. File must be `*.feature`. |
| `Scenario:` | One behavior per scenario. Independent (no cross-scenario state). Needs at least one `Given/When/Then` step. Title appears in Playwright report — make it precise (`Login fails when account is locked`, not `Error case 2`). Titles must be **unique within a file** or Playwright throws. |
| `Background:` | 0 or 1 per file. No tags, no `Examples`. |
| `Scenario Outline:` + `Examples:` | Every `<placeholder>` in steps must have a matching `Examples` column header, and vice versa. Can have **multiple named `Examples:` blocks** per outline, each individually taggable (see section 5). |
| `Rule:` (Cucumber 6+) | Optional grouping of scenarios under one business rule. Supported by parser; rarely needed — prefer splitting large files. |
| `Given/When/Then/And/But` | `And`/`But` inherit the previous keyword's type (parser treats them identically); choice is readability only. Convention: `Given` = preconditions, `When` = user action, `Then` = observable outcome. |
| `Data Table` / `Doc String` | For structured/multi-line step args (see section 4). |
| `"""` / `\| table \|` | Must immediately follow the step line. |

Agentic-browser style guidance (from Cucumber "better Gherkin" + Gherkin guides): declarative, not imperative. Prefer `When I update my profile name to "Alice Smith"` over five click/type steps. Step definitions own selectors; feature text owns intent. This is what keeps agent-generated features maintainable.

## 2. How tags work

### 2.1 Syntax and scope

```gherkin
@authentication @smoke
Feature: User Login

  @happy-path @TC-010
  Scenario: Successful login
    ...

  @error-handling @regression @TC-011
  Scenario: Login with wrong password
    ...
```

- Tags are `@no-spaces` tokens on lines directly above `Feature:`, `Scenario:`, `Scenario Outline:`, or `Examples:`.
- Feature-level tags apply to **all** scenarios in the file (inheritance).
- `Examples:`-level tags apply only to that block's rows — the standard way to split fast/slow data sets:

```gherkin
  Scenario Outline: Payment processing
    When I pay with "<method>"
    Then the order status should be "<status>"

    @fast
    Examples: Card payments
      | method     | status    |
      | Visa       | confirmed |
      | Mastercard | confirmed |

    @slow
    Examples: Bank transfers
      | method        | status  |
      | Bank transfer | pending |
```

### 2.2 Conventional tag vocabulary

| Category | Examples | Use |
|---|---|---|
| Suite / gate | `@smoke`, `@regression`, `@sanity`, `@e2e`, `@acceptance` | CI selection: fast `@smoke` gate vs full `@regression` |
| Quality/type | `@positive`, `@negative`, `@edge`, `@happy-path`, `@error-handling` | Maps to markdown-table "type" column |
| Priority | `@P0`, `@P1`, `@P2`, `@P3` or `@priority:high`, `@critical` | Maps to "priority" column; keep to one scheme |
| Area | `@auth`, `@checkout`, `@search`, `@desktop`, `@mobile` | Filtering + step scoping |
| Lifecycle | `@wip`, `@draft`, `@deprecated`, `@requires-database`, `@flaky` | Exclude from CI (`not @wip`) |
| Traceability | `@TC-042`, `@C123`, `@TEST-123`, `@jira:PROJ-123` | Scenario ID (see section 3) |
| Execution control (playwright-bdd **special**) | see section 2.3 | Change runner behavior — do NOT reuse casually |

### 2.3 playwright-bdd special tags (behavior-changing — reserved!)

From `docs/writing-features/special-tags.md` (verified against repo source):

| Tag | Effect | Scope |
|---|---|---|
| `@only` | Run only tagged tests (like `test.only`) | Feature, Scenario |
| `@skip` / `@fixme` | Skip (`test.skip`) | Feature, Scenario |
| `@fail` | Expect failure (`test.fail`) | Feature, Scenario |
| `@slow` | Timeout x3 (`test.slow`) | Feature, Scenario |
| `@timeout:5000` | Explicit timeout ms (on Feature = per-scenario) | Feature, Scenario |
| `@retries:2` | Retries; on a single scenario wraps it in an anonymous describe | Feature, Scenario |
| `@mode:parallel` / `@mode:serial` / `@mode:default` | Playwright execution mode | Feature, Scenario Outline (**not** a single `Scenario`) |

Consequences:

1. Since Playwright 1.42, Gherkin tags are mapped to Playwright tags and visible in HTML reports; accessible inside steps via the `$tags`/`$test` fixtures.
2. Filtering uses Cucumber-style tag expressions via config or CLI: `npx bddgen --tags "@smoke and not @slow" && npx playwright test`. Supports `and` / `or` / `not` / parentheses.
3. **Tags-from-path**: any `@`-prefixed directory or filename auto-tags its features AND scopes co-located `steps.ts` to them. `features/@checkout/checkout.feature` is equivalent to an `@checkout` tag. Useful for agent scaffolding (suite = folder), but renaming a folder retags tests.
4. Never use a special-tag name as plain metadata: tagging a scenario `@slow` because "the page loads slowly" triples its timeout whether you meant that or not. Same for `@only` (reduces a CI run to one test) and `@fail`.

## 3. Scenario IDs: tag vs comment (convention)

**Convention: put the stable scenario ID in a tag, not a comment.**

```gherkin
  @TC-042 @smoke
  Scenario: Login succeeds with valid credentials
    ...
  # BAD (invisible to tooling):
  # id: TC-042
  # Scenario: Login succeeds ...
```

Why tags win:

| Aspect | `@TC-042` tag | `# TC-042` comment |
|---|---|---|
| Runner visibility | Yes — mapped to Playwright tag, shown in report, filterable (`--tags "@TC-042"`), readable via `$tags` fixture | No — stripped before execution/reporting |
| Traceability integrations | Standard for Xray/AssertThat/TestRail-CLI/Jira sync (scenarios tagged `@TEST-123`, `@C123`, `@JIRA-456` auto-link on upload) | Requires custom comment parsing per tool |
| Uniqueness enforcement | Greppable/lintable | Easy to duplicate silently |
| playwright-bdd conflicts | None (any `@X-NNN` is a plain tag) | `# title-format:` above `Examples:` is **reserved** for example-title templates — an ID comment there breaks titles |

Recommended scheme:

- Format: `@TC-<NNN>` (or `@<SUITE>-<NNN>`, e.g. `@AUTH-012`) — one ID per `Scenario`/`Scenario Outline`. For outlines, the ID tags the outline; individual rows are distinguished by unique example titles (section 5).
- Also acceptable where a tracker dictates it: `@C123` (TestRail case), `@T123` (Qase), `@jira:PROJ-123` (playwright-bdd docs use `@jira:123` in their own example). Pick ONE scheme per repo.
- Keep the human slug in the Scenario title; keep the machine ID in the tag. Never encode the ID only in the title text (`Scenario: TC-042 login...`) — titles get reworded, tags stay stable.
- Comments are for prose context (`# Covers PROJ-123 AC2; seeded user fixture`), never for the canonical ID.

## 4. Test-data / credentials parametrization patterns

### 4.1 `Scenario Outline` + `Examples` (primary pattern)

```gherkin
  Scenario Outline: Login with <role> succeeds
    Given I am on the login page
    When I log in as "<role>"
    Then I land on the dashboard

    Examples:
      | role  |
      | admin |
      | buyer |
```

- One row = one Playwright test. Keep rows to same-behavior variations; different behaviors become separate scenarios (outline overuse obscures intent).
- Empty cells, unquoted numbers, and dates are strings unless the step definition converts them — document expected types in step defs, not features.

### 4.2 Credentials: NEVER hardcode secrets in `.feature`

Features are business-readable specs committed to git. Pattern:

```gherkin
  # feature file — role names only
  When I log in as "admin"
```

```ts
// steps.ts — fixture/env resolves the secret
When('I log in as {string}', async ({ page }, role: string) => {
  const creds = {
    admin: { user: process.env.ADMIN_USER!, pass: process.env.ADMIN_PASS! },
  } as const;
  await login(page, creds[role]);
});
```

If a table needs user shapes, use role + email, not passwords:

```gherkin
  Given the following users exist:
    | name  | email             | role  |
    | Alice | alice@example.com | admin |
```

Seed via API/fixture in `Before` hooks, not via UI clicks in every scenario.

### 4.3 `Data Table` vs `Doc String` vs `Examples`

| Need | Construct | Example |
|---|---|---|
| Same scenario x N data sets | `Scenario Outline` + `Examples:` table with `<col>` placeholders | Login x roles, search x queries |
| One step needs a record set | Inline `Data Table` under the step | `Given the following users exist:` + 3-col table |
| One step needs a blob (JSON/XML/long text) | `Doc String` (`"""json ... """`) | POST body, rich text assertion |
| Environment-specific values (URLs, secrets, browsers) | Playwright fixtures / `process.env` / project config — NOT Gherkin | `BASE_URL`, `ADMIN_PASS` |

## 5. Metadata columns in agentic-testing scenario tables

Markdown inventory tables (TestRail/Qase/Xray-style) commonly carry these columns; mapping to Gherkin below:

| Markdown column | Typical values | Gherkin equivalent in playwright-bdd |
|---|---|---|
| `ID` | `TC-001`, `AUTH-012`, `C123` | **Tag** `@TC-001` (see section 3) |
| `Title / Scenario` | `Login succeeds with valid credentials` | `Scenario:` title (must be unique per file) |
| `Suite / Feature` | `Auth`, `Checkout` | `Feature:` name and/or containing folder (`features/@auth/...`) and/or `@auth` tag |
| `Priority` (+ `Severity`) | `P0–P3` / `Critical/High/Medium/Low` | Tag: `@P0` or `@priority:high`. Keep ONE scheme; `Severity` (impact) vs `Priority` (run order) are distinct in TestRail/Qase — don't merge them into one tag |
| `Type` | `positive / negative / edge`, `smoke / regression`, `happy-path / error-handling` | Tags `@positive`, `@negative`, `@edge`, `@smoke` |
| `Status` | `draft / ready / automated / deprecated` | `draft` maps to `@wip` or `@skip` (excluded from CI); `deprecated` maps to delete or `@skip` with reason; `automated` is implicit (it has a scenario). Do NOT invent `@draft` and expect the runner to filter it unless you add the expression |
| `Preconditions` | `Seeded buyer account` | `Background:` steps or leading `Given` steps |
| `Steps / Expected` | `Click login -> dashboard` | `When`/`Then` steps (declarative) |
| `Test data` | `admin / buyer roles` | `Examples:` rows / `Data Table` / fixtures (section 4) |
| `Timeout / Estimate` | `30s`, `@slow` | `@timeout:N` / `@slow` special tags (caution section 2.3) |
| `Execution time (last run)` | `1.2s` | **Nowhere in the feature** — runtime output (Playwright HTML/Cucumber JSON reports), not authoring metadata |
| `Owner / Author` | `@alice` | Nowhere in the feature (use git blame / CODEOWNERS). An `@owner:alice` tag pollutes `--tags` filtering |
| `Requirement` | `PROJ-123` | Tag `@jira:PROJ-123` or description line; linkable by upload tooling |

Minimal convertible core: `ID` to tag, `Title` to `Scenario:`, `Suite` to `Feature:`/folder, `Type`/`Priority` to tags, `Data` to `Examples:`, `Steps` to `Given`/`When`/`Then`. Everything else (`Status`, `Owner`, `Execution time`, estimates) lives in the tracker/CI, not the `.feature`.

playwright-bdd example-title note (from `customize-examples-title.md`): default generated title per outline row is `Example #<index>`, which shifts when rows are inserted. Four stabilization mechanisms, in priority order: (1) `<column>` placeholder in the `Examples:` block name, (2) `<column>` placeholder in the `Scenario Outline:` name, (3) `# title-format: ... <column> ...` comment directly above `Examples:`, (4) global `examplesTitleFormat` config option. Generated titles must be unique per outline or Playwright throws.

## 6. What makes a markdown scenario table NOT convertible to playwright-bdd

Concrete blockers / silent-corruption risks when converting markdown rows to `.feature` files:

1. **No `Feature:` home.** Every file needs exactly one `Feature:` header. A table of 50 orphan scenarios with no suite grouping cannot be emitted — assign each row a `Feature` (new or existing file) first.
2. **Non-unique or empty scenario titles.** Playwright errors on duplicate test titles in a file. Tables with `Test login`, `Error case`, blank cells, or two rows mapping to the same outline+row values fail generation. Fix: precise titles + `<column>` in outline/`Examples:` names + `# title-format:` (four mechanisms above; global fallback `examplesTitleFormat` config). Generated titles must be unique **per outline**.
3. **Rogue special tags.** Metadata like `slow`, `only`, `fail`, `fixme`, `mode:serial` in a `Tags` column becomes `@slow`/`@only`/`@fail`/… and silently changes timeouts/retries/selection. Sanitize: allowlist plain tags; map timing intent explicitly to `@timeout:N`.
4. **Invalid tag characters.** Tags cannot contain spaces; `@P0 High` parses as two tags (`@P0`, `@High` — the second likely unintended). Normalize to `@P0`, `@priority:high`, `@suite:order-history`. Colons are legal (`@jira:123`, `@timeout:5000`) but `@timeout:X`/`@retries:X`/`@mode:X` with bad values break generation.
5. **Markdown formatting inside cells.** Bold, code spans, links, `<br>`, merged cells, multi-line cells have no Gherkin meaning and leak into step text, producing unmatched step definitions. Strip to plain text; quote string args `"..."`; use `<placeholders>` only for `Examples` columns.
6. **`Examples` to placeholder mismatch.** Every `<name>` in steps needs an `Examples` column and vice versa. Tables that list data columns never referenced (or reference `<cols>` with no table) fail at generation.
7. **Multiple backgrounds / misplaced blocks.** Only one `Background:` per file, before scenarios; `Examples:` only under outlines; `Rule:` cannot nest arbitrarily. A markdown "Preconditions" column that differs per row must become per-scenario `Given`s, not a shared `Background:`.
8. **Secrets and env-specific data inline.** Passwords, tokens, absolute URLs, user-specific IDs in table cells get baked into committed features. Replace with role names + fixtures/env (section 4.2).
9. **Steps that aren't automatable as written.** `Verify backend eventually consistent`, `Check email arrives within 5 min`, purely visual `Looks premium` — no deterministic step definition exists. Rewrite to observable assertions or mark `@skip`/`@manual` and exclude from `bddgen` runs.
10. **Reserved comment syntax collision.** `# title-format: ...` directly above `Examples:` is consumed as the title template. ID/prose comments placed there hijack example titles — keep ID in tags, prose elsewhere.
11. **One-row-per-assertion explosion.** Tables that split a single behavior into 20 rows differing only in asserted text usually want one scenario with a `Data Table`/`Doc String`, not a 20-row outline (unreadable reports, slow runs).
12. **Step-definition gap (process, not syntax).** Even a perfect `.feature` fails without matching `Given`/`When`/`Then` definitions in `steps.ts` with compatible fixtures. Conversion must also emit/verify step stubs (`npx bddgen` reports missing steps) — otherwise generated specs are red on arrival.

### Quick pre-conversion checklist for an agent

- [ ] Every row has: stable `ID`, precise unique `Title`, `Suite` to `Feature`, at least one `When` + one `Then`.
- [ ] `Type`/`Priority` values map to an agreed tag allowlist (no free-text tags, no special-tag collisions).
- [ ] Parametrized rows share one behavior → one `Scenario Outline` with `<cols>` in title; else separate `Scenario`s.
- [ ] No secrets/URLs in cells; roles + env/fixtures instead.
- [ ] Titles unique per file; example titles unique per outline (use `<column>` templates).

## Sources

- [playwright-bdd repo](https://github.com/vitalets/playwright-bdd)
- [playwright-bdd — Writing features (tags example, `--tags` expressions, Playwright tag mapping)](https://raw.githubusercontent.com/vitalets/playwright-bdd/main/docs/writing-features/index.md)
- [playwright-bdd — Special tags (`@only/@skip/@fixme/@fail/@slow/@timeout/@retries/@mode`)](https://raw.githubusercontent.com/vitalets/playwright-bdd/main/docs/writing-features/special-tags.md)
- [playwright-bdd — Tags from path (`@`-dirs/files)](https://raw.githubusercontent.com/vitalets/playwright-bdd/main/docs/writing-features/tags-from-path.md)
- [playwright-bdd — Customize examples title (4 title-template mechanisms, uniqueness requirement)](https://raw.githubusercontent.com/vitalets/playwright-bdd/main/docs/writing-features/customize-examples-title.md)
- [playwright-bdd — Tags and Filtering (DeepWiki summary)](https://deepwiki.com/vitalets/playwright-bdd/4.4-tags-and-filtering)
- [Gherkin Syntax Guide: Writing Good Feature Files (2026)](https://helpmetest.com/blog/gherkin-syntax-guide/)
- [TestRail — Behaviour-Driven Development (BDD)](https://support.testrail.com/hc/en-us/articles/7827238336916-Behavior-Driven-Development-BDD)
- [TestRail — BDD commands reference](https://support.testrail.com/hc/en-us/articles/45582376878100-Behaviour-Driven-Development-BDD-commands-reference)
- [TestRail — Test case fields (Priority/Type taxonomy)](https://support.testrail.com/hc/en-us/articles/14940939006740-Test-case-fields)
