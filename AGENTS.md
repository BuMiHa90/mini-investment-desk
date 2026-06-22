# Daily Operations — Mini Investment Desk

This repository is run automatically by Windows Task Scheduler through Codex CLI. When the scheduled prompt says to follow `AGENTS.md`, run the daily desk workflow below exactly.

## Non-Negotiable Runtime Paths

Use these exact executables:

- PowerShell 7: `C:\Users\ADMIN\AppData\Local\Microsoft\WindowsApps\pwsh.exe`
- Global Python: `C:\Users\ADMIN\AppData\Local\Programs\Python\Python311\python.exe`
- Project root: `F:\Hai BUi\Mini_Investment_Desk_Agent_System_v1`

Before running the pipeline, verify both runtime paths exist and report the versions. Do not continue if either path is missing.

Never run commands through Windows PowerShell 5.1. Never run Python as `python`, `py`, or any other discovered interpreter. All shell commands for the daily workflow must be launched via the PowerShell 7 path above, and all Python calls inside that workflow must use the global Python path above.

Reason: using Windows PowerShell 5.1 can cause UTF-8/Unicode issues in Vietnamese report text; using an inferred Python can hit sandbox/path restrictions or missing dependencies.

## Daily Workflow

1. Start in the project root.
2. Check the working tree. Do not overwrite unrelated user changes. Only the expected daily report outputs under `docs/` and `data/` should be committed automatically.
3. Run the runtime preflight with the exact paths:

```powershell
& "C:\Users\ADMIN\AppData\Local\Microsoft\WindowsApps\pwsh.exe" -NoLogo -NoProfile -ExecutionPolicy Bypass -WorkingDirectory "F:\Hai BUi\Mini_Investment_Desk_Agent_System_v1" -Command @'
$ErrorActionPreference = "Stop"
$Pwsh = "C:\Users\ADMIN\AppData\Local\Microsoft\WindowsApps\pwsh.exe"
$Python = "C:\Users\ADMIN\AppData\Local\Programs\Python\Python311\python.exe"
if (-not (Test-Path -LiteralPath $Pwsh)) { throw "PowerShell 7 path missing: $Pwsh" }
if (-not (Test-Path -LiteralPath $Python)) { throw "Global Python path missing: $Python" }
& $Pwsh --version
& $Python --version
'@
```

4. Run the daily pipeline through PowerShell 7 and global Python only:

```powershell
& "C:\Users\ADMIN\AppData\Local\Microsoft\WindowsApps\pwsh.exe" -NoLogo -NoProfile -ExecutionPolicy Bypass -WorkingDirectory "F:\Hai BUi\Mini_Investment_Desk_Agent_System_v1" -Command @'
$ErrorActionPreference = "Stop"
$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$Python = "C:\Users\ADMIN\AppData\Local\Programs\Python\Python311\python.exe"
& $Python -m pipeline.run_pipeline --cli
'@
```

5. Verify expected outputs:
   - `docs/index.html`
   - `docs/archive/<report-date>.html`
   - `data/reports/<report-date>/01.md`
   - `data/reports/<report-date>/02.md`
   - `data/reports/<report-date>/03.md`

6. Commit and push only expected daily report changes:

```powershell
& "C:\Users\ADMIN\AppData\Local\Microsoft\WindowsApps\pwsh.exe" -NoLogo -NoProfile -ExecutionPolicy Bypass -WorkingDirectory "F:\Hai BUi\Mini_Investment_Desk_Agent_System_v1" -Command @'
$ErrorActionPreference = "Stop"
git status --short
git add docs data
if (git diff --cached --quiet) {
    Write-Host "No daily report changes to commit."
    exit 0
}
git commit -m "Daily desk report $(Get-Date -Format yyyy-MM-dd)"
git push
'@
```

## Failure Handling

If any step fails, stop. Do not invent fallback reports unless the existing pipeline itself enters its documented fallback path. Leave a concise summary with:

- the exact command that failed
- the exit code or exception
- whether `docs/` or `data/` were changed
- the next manual action needed

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **mini-investment-desk** (365 symbols, 387 relationships, 4 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash → `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/mini-investment-desk/context` | Codebase overview, check index freshness |
| `gitnexus://repo/mini-investment-desk/clusters` | All functional areas |
| `gitnexus://repo/mini-investment-desk/processes` | All execution flows |
| `gitnexus://repo/mini-investment-desk/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
