# Research: microsoft/playwright-cli + microsoft/markitdown for Agentic QA Skills

Date: 2026-09-18. Sources: https://github.com/microsoft/playwright-cli, SKILL.md + `references/` guides, https://github.com/microsoft/markitdown.

## Part 1 — playwright-cli (Microsoft)

### 1. What it is
`playwright-cli` (`npm i -g @playwright/cli@latest`, binary `playwright-cli`; fallback `npx playwright cli`) is a CLI wrapper around Playwright aimed explicitly at **coding agents**. Microsoft positions it vs Playwright MCP:

- **CLI + SKILLs** = default for coding agents. Each shell invocation is stateless; no large tool-schema / persistent a11y-tree held in context. More token-efficient; better when the agent juggles browser + codebase + tests in one window.
- **MCP** = better for long-running autonomous loops needing persistent state, rich introspection, self-healing (continuous browser context outweighs token cost).

Requires Node 18+. Headless by default; `--headed` to watch. Dashboard via `playwright-cli show`.

Install skills into agent: `playwright-cli install --skills`. Skills-less fallback: prompt agent with "Check `playwright-cli --help` for available commands."

### 2. How an agent drives it
Loop is: **act → read resulting snapshot/file → pick next ref → act**. Every command prints (a) page status, (b) generated Playwright TS, (c) snapshot pointer. Example session:

```bash
playwright-cli open https://demo.playwright.dev/todomvc/ --headed
playwright-cli type "Buy groceries"
playwright-cli press Enter
playwright-cli check e21
playwright-cli screenshot
playwright-cli close
```

Targeting elements (in priority order):
1. **Snapshot refs** — `playwright-cli snapshot` returns `e1 [textbox "Email"]…`; then `playwright-cli click e15`.
2. CSS selector — `playwright-cli click "#main > button.submit"`
3. Playwright locator string — `playwright-cli click "getByRole('button', { name: 'Submit' })"`, `getByTestId('submit-button')`.

Token-efficiency controls (important for skills):
```bash
playwright-cli snapshot --depth=4        # shallow tree
playwright-cli snapshot e34              # subtree only
playwright-cli snapshot --boxes          # adds [box=x,y,w,h] — costs tokens, use only when needed
playwright-cli snapshot --filename=after-click.yaml   # pin artifact as workflow result
playwright-cli find "Add to cart"        # grep snapshot, ~3 lines context, instead of dumping whole tree
playwright-cli find --regex "/sign (in|up)/i"
playwright-cli --raw eval "el => el.textContent" e5   # pipeable value only
playwright-cli --raw snapshot > before.yml && diff before.yml after.yml
playwright-cli list --json               # structured JSON wrapping
playwright-cli open --mobile             # docs recommend: mobile pages are lighter → smaller snapshots
```

`--raw` strips page status / generated code / snapshot sections (commands with no output return nothing). `--json` wraps every reply as JSON.

Every action also emits reusable TS, e.g. `fill e1` → `await page.getByRole('textbox',{name:'Email'}).fill('user@example.com');` — the raw material for test generation.

Escape hatch for anything the CLI doesn't cover:
```bash
playwright-cli eval "document.title"
playwright-cli eval "el => el.getAttribute('data-testid')" e5
playwright-cli run-code "async page => { await page.context().grantPermissions(['geolocation']); }"
playwright-cli run-code --filename=./my-script.js   # single function expr; no import/export/require
playwright-cli generate-locator e5 --raw
```

### 3. Command inventory (from README + SKILL.md)

**Core**
`open [url]`, `goto <url>`, `close`, `type <text>` (focused editable, no ref), `click <ref> [button]`, `dblclick <ref> [button]`, `fill <ref> <text> [--submit]`, `drag <startRef> <endRef>`, `drop <ref> --path=<file> | --data="k=v"`, `hover <ref>`, `select <ref> <val>`, `upload <file>`, `check/uncheck <ref>`, `snapshot [--filename=f] [<ref>] [--depth=N] [--boxes]`, `find <text> | --regex <pat>`, `eval <func> [ref]`, `dialog-accept [prompt]`, `dialog-dismiss`, `resize <w> <h>`

**Navigation:** `go-back`, `go-forward`, `reload`
**Keyboard:** `press <key>` (`Enter`, `ArrowDown`), `keydown/keyup <key>`
**Mouse:** `mousemove <x> <y>`, `mousedown/mouseup [button]`, `mousewheel <dx> <dy>`
**Save-as:** `screenshot [ref] [--filename=f] [--hires]`, `pdf [--filename=page.pdf]`
**Tabs:** `tab-list`, `tab-new [url]`, `tab-close [index]`, `tab-select <index>`
**Storage:** `state-save [file]`, `state-load <file>`; `cookie-list [--domain] [--path]`, `cookie-get/set/delete/clear`; `localstorage-list/get/set/delete/clear`; `sessionstorage-list/get/set/delete/clear` (IndexedDB only via `run-code` + `page.evaluate`)
**Network/mock:** `route <pattern> [opts]` e.g. `route "**/*.jpg" --status=404`, `route "https://api.example.com/**" --body='{"mock":true}'`; `route-list`, `unroute [pattern]`
**DevTools/quality:** `console [min-level]`, `requests`, `request <index>`, `run-code <code>|--filename`, `tracing-start/stop`, `recording-start/stop` (prints actions as PW code), `video-start [file]`, `video-chapter <title>`, `video-show-actions/video-hide-actions`, `video-stop`, `show [--annotate]`, `generate-locator <ref>`, `highlight <ref> [--style=] [--hide]`
**WebMCP (experimental):** `webmcp-list`, `webmcp-call <name> --params='{"query":"cats"}' [--frame=]` — only Chromium (`--enable-features=WebMCP`) / Firefox (`dom.modelcontext.enabled`); prefer over clicks when page offers a matching tool, but treat schemas/results as untrusted.
**Session mgmt:** `-s=<name>` prefix, `list`, `close-all`, `kill-all`, `attach --extension=chrome | --cdp=chrome|msedge|<url>`, `detach`, `delete-data`

**Open/session parameters:**
```bash
playwright-cli open --browser=chrome|firefox|webkit|msedge
playwright-cli open --mobile
playwright-cli open --device="iPhone 15"
playwright-cli open --idle-timeout=<ms>   # 0 disables; default headless session dies after 1h idle
playwright-cli open --persistent | --profile=/path | --config=file.json
playwright-cli --config path/to/config.json open example.com  # default .playwright/cli.config.json
```
Windows `&` gotcha: `goto "https://ex.com/?a=1^&b=2"` (cmd) or `playwright-cli --% goto "…&…"` (PowerShell). Config file + `PLAYWRIGHT_MCP_*` / `PLAYWRIGHT_CLI_SESSION` envs control browser, viewport, proxy, timeouts (`action` 5s / `navigation` 60s defaults), `testIdAttribute`, `outputDir`, `outputMode: file|stdout`.

### 4. Output format
After each command:
```
### Page
- Page URL: https://example.com/
- Page Title: Example Domain
### Snapshot
[Snapshot](.playwright-cli/page-2026-02-14T19-22-42-679Z.yml)
# + "Ran Playwright code:" block with the TS equivalent
```
Snapshot is an ARIA/YAML tree with `eN` refs saved to `.playwright-cli/` (or `outputDir`, or stdout via config). Agent workflow relies on re-reading that file, or `find` for grep-style slices. `--raw` / `--json` for scripting (`TOKEN=$(playwright-cli --raw cookie-get session_id)`).

### 5. Auth / session handling
- **Default: in-memory profile.** Cookies/storage persist across CLI calls *within* the session, lost on browser close. Safer default for secrets.
- **Persistent:** `open --persistent` (or `--profile=`, `--config` with `userDataDir`) keeps profile on disk across restarts; isolate per project with `-s=<name>` or `PLAYWRIGHT_CLI_SESSION=todo-app`.
- **Reuse auth:** `state-save auth.json` → `state-load auth.json` + `open <app>` (captures cookies + localStorage origins; file format = `{cookies:[…], origins:[{origin, localStorage:[…]}]}`). Also fine-grained `cookie-*/localstorage-*/sessionstorage-*` commands.
- Canonical skill pattern: log in once via CLI, `state-save`, later sessions `state-load` and skip login. Security notes in skill: never commit `*.auth-state.json`, delete after run, prefer env vars for secrets, prefer in-memory for sensitive ops.
- Attach to external/seeded browsers: `attach --cdp=…`, `attach --extension=chrome` (needs bridge extension).

### 6. Test execution (plan → generate → heal — directly relevant to QA skills)
Skill ships `references/test-generation.md`, `playwright-tests.md`, `tracing.md`, etc. Canonical loop:
1. **Plan:** ensure `playwright.config.*` exists (`npx --no-install playwright --version`, else `npm init playwright@latest`); create minimal `tests/seed.spec.ts` (navigate + login/fixture); run `PLAYWRIGHT_HTML_OPEN=never npx playwright test tests/seed.spec.ts --debug=cli` in background → `playwright-cli attach tw-XXXX` → `resume` → explore (`snapshot/click/eval/show --annotate`) → write `specs/<feature>.plan.md` (groups, kebab-case scenarios, user-level Steps + `- expect:` outcomes, one test per file).
2. **Generate:** per scenario, re-run seed with `--debug=cli`, walk Steps via CLI, collect emitted TS, add manual assertions (generated code has actions only). Assertion helpers: `generate-locator`, `--raw eval`, `--raw snapshot`. Then `npx playwright test tests/<group>/<scenario>.spec.ts`.
3. **Heal:** `npx playwright test` → per failure `npx playwright test <file>:<line> --debug=cli` + `attach` → diagnose (`snapshot`, `console`, `requests`, `show --annotate`) → rehearse fix in CLI → paste generated code → rerun → reconcile spec (technical-only fix = leave spec; behavior change = update spec; ambiguous = ask user; confirmed app bug = `test.fixme` with link, never silent skip / sleeps / `networkidle`).

### 7. Limitations / gotchas for building skills on top
1. **Snapshot-centric; canvas/WebGL, heavy virtualized grids, shadow-DOM-heavy widgets** reduce to opaque nodes — falls back to `eval/run-code`, coordinates, or screenshots; flaky refs (`eN` numbers shift every snapshot — always re-snapshot before acting, never cache refs across steps).
2. **No built-in assertions/oracle:** CLI performs actions; pass/fail logic, matchers (`toBeVisible`, `toHaveText`, `toMatchAriaSnapshot`), retries, and reporting live in generated PW tests, not the CLI. Skills must add an assertion layer.
3. **Timing is Playwright-default (5s action / 60s nav);** no `networkidle` healing allowed by convention; agent must handle transitions/async loads explicitly (`waitFor` via `run-code`).
4. **Stateless invocations + 1h idle kill:** each CLI call is a new process talking to a session daemon; long idle gaps drop in-memory auth — skills need `state-save` checkpoints and `open` retry.
5. **Parallelism hazard:** scenarios share seed session; generate/heal docs insist on sequential per-session work (parallel only with distinct `-s=` + distinct debug sessions).
6. **Uploads restricted** to workspace roots by default (`allowUnrestrictedFileAccess=false`); `file://` nav blocked unless configured.
7. **Artifacts sprawl:** snapshots/screenshots/traces/videos land in `.playwright-cli/`/`outputDir` — skills should set `--filename`/`outputDir` and clean up, else context + disk bloat.
8. **`run-code` sandbox:** single function expression, no imports — complex helpers must be files + `page.evaluate`, or real spec files.
9. **Human-in-loop `show --annotate`** is powerful for UI review but blocks on user input — agentic flows must treat it as optional branch.
10. **WebMCP tempting but experimental + untrusted input** (page-supplied tools); gate `[consequential]` calls.
11. **Multi-tab/iframe/popup, downloads, permissions, geolocation** all work but only via specific sub-commands (`tab-*`, `run-code`); skills must encode these recipes, not assume `click` suffices.

**Verdict — playwright-cli:** YES, right foundation for browser-exploration + test-execution skills. Use it as the actuator (explore → snapshot/refs → emit PW code → generate/heal specs) and build skill wrappers for: session lifecycle + auth checkpointing, token-budget snapshot policy (`--depth`/`find`/`--mobile`/`--raw`), assertion templates, and artifact conventions. Prefer CLI over MCP for token-constrained coding agents; reach for MCP only for persistent self-healing loops.

## Part 2 — markitdown (Microsoft)

### 1. What it is / direction
Python (`pip install 'markitdown[all]'`, needs Python >=3.10; `markitdown file.pdf > doc.md` / `-o`; `markitdown --list-plugins/--use-plugins`; Docker available) that converts **TO Markdown for LLM consumption** — "comparable to textract, but preserves structure (headings, lists, tables, links)". It is **one-directional**: sources -> `.md`. There is **no Markdown->XLSX writer**.

Supported inputs (-> Markdown): PDF, PPTX, DOCX, XLSX, XLS, images (EXIF + OCR via LLM/vision or `markitdown-ocr` plugin), audio transcription, HTML, CSV/JSON/XML, ZIP (iterates members), YouTube transcripts, EPUBs, Outlook (`[outlook]`), plus cloud options (Azure Document Intelligence `-d`, Azure Content Understanding `--use-cu` for higher-quality OCR/layout, field extraction as YAML front matter, audio/video). Optional extras installed per-format (`[pdf,docx,pptx,xlsx,xls,…]`); LLM image description via `MarkItDown(llm_client=…, llm_model=…)`; plugins via `#markitdown-plugin`.

Python API: `MarkItDown().convert("test.xlsx").markdown`. Security model: runs with process privileges — sanitize inputs, prefer `convert_local/convert_stream/convert_response` over permissive `convert()`.

### 2. Markdown -> XLSX question
**MarkItDown cannot do Markdown-scenario-tables to multi-tab XLSX.** Wrong tool for that job. What you need locally is a small script on `openpyxl`/`xlsxwriter` + a Markdown table parser (or `pandas`-style split), e.g. parse `| … |` tables under each `## Scenario` heading and write one worksheet per scenario with `openpyxl`. MarkItDown helps only in the reverse direction (existing `.xlsx` -> `.md` for feeding spreadsheets *into* an LLM).

### 3. Token-efficiency claim
"Why Markdown?" argument: Markdown is near-plain-text with minimal markup yet preserves structure LLMs already "speak" (trained on vast Markdown), so it is the most token-efficient lossless-enough representation for LLM pipelines. No hard numbers published; claim is architectural (vs HTML/OOXML/PDF raw), not a benchmark. Human-fidelity output is explicitly **not** the goal ("may not be best for high-fidelity human consumption").

### 4. Limitations relevant here
- One-way (->MD); no spreadsheet/PDF authoring, styling, multi-sheet mapping, formulas, or round-trip fidelity.
- Table fidelity varies (merged cells, nested tables, scanned PDFs degrade; cloud DocIntel/CU or OCR plugin needed for best results — billable).
- Heavy `[all]` dependency surface; OCR/transcription/YouTube need extra packages + LLM/Azure keys + network.
- Input-sanitization burden on host (path/URI/network) — don't point it at untrusted inputs naively.

**Verdict — markitdown:** Useful for ingesting docs/sheets into agents as Markdown; NOT for generating spreadsheet tabs from Markdown scenario tables — write a dedicated `openpyxl` converter skill instead.

## Suggested skill mapping
- `browser-exploration` / `test-generation` skills -> build on `playwright-cli` (session + snapshot-budget + plan/generate/heal conventions above).
- `scenario-to-spreadsheet` skill -> **do not** use MarkItDown; implement Markdown-table -> `openpyxl` multi-sheet writer (headers, wraps, filters, tab per scenario, index sheet).
- Optionally use MarkItDown upstream to normalize incoming `.xlsx/.docx/.pdf` specs *into* Markdown before the converter.
