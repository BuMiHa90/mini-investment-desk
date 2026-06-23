# Bao cao desk hang ngay — CHAY THANG PIPELINE (khong qua Claude agent dieu phoi).
# Pipeline tu goi Claude CLI cho tung agent qua pipeline/run_agents_cli.py.
# Task Scheduler "Mini Investment Desk Claude Daily" tro toi file nay (8h/15:45/20:30 T2-T6).
# Log: %LOCALAPPDATA%\MiniInvestmentDesk\claude_daily_task.log

$ErrorActionPreference = "Stop"

try {
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    $OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    $PSStyle.OutputRendering = "PlainText"
}
catch {
    # Keep running even if the host does not expose console encoding controls.
}

$env:PYTHONUTF8 = "1"
$env:PYTHONIOENCODING = "utf-8"
$env:PYTHONUNBUFFERED = "1"   # output flush theo dong -> log hien tien do realtime

$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location -LiteralPath $ProjectRoot

$LogDir = Join-Path $env:LOCALAPPDATA "MiniInvestmentDesk"
New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
$LogFile = Join-Path $LogDir "claude_daily_task.log"

function Write-TaskLog {
    param([Parameter(Mandatory = $true)][string]$Message)
    $Line = "[{0:yyyy-MM-dd HH:mm:ss}] {1}" -f (Get-Date), $Message
    Write-Host $Line
    Add-Content -LiteralPath $LogFile -Value $Line -Encoding utf8
}

# --- Runtime paths (tuyet doi, theo CLAUDE.md) ---
$Python = "C:\Users\ADMIN\AppData\Local\Programs\Python\Python311\python.exe"
if (-not (Test-Path -LiteralPath $Python)) { $Python = "python" }

# bao dam claude.exe va git nam trong PATH cho tien trinh con
$env:PATH = "$env:USERPROFILE\.local\bin;C:\Program Files\Git\cmd;$env:PATH"

try {
    Write-TaskLog "=== Bat dau pipeline truc tiep (khong qua Claude agent) ==="
    Write-TaskLog "Project root: $ProjectRoot"
    Write-TaskLog "Python: $Python"

    # 1) Chay pipeline: fetch -> agent 01/02/03 (qua claude CLI) -> render HTML
    Write-TaskLog "Dang chay: python -u -m pipeline.run_pipeline --cli"
    & $Python -u -m pipeline.run_pipeline --cli 2>&1 | ForEach-Object {
        $t = ($_ | Out-String).TrimEnd()
        if ($t) { Write-TaskLog $t }
    }
    if ($LASTEXITCODE -ne 0) {
        Write-TaskLog "PIPELINE THAT BAI (exit $LASTEXITCODE) — khong commit."
        exit 1
    }

    # 2) Commit chi 2 thu muc bao cao (khong dung thay doi khac)
    & git add docs data 2>&1 | ForEach-Object { Write-TaskLog $_ }
    & git diff --cached --quiet
    if ($LASTEXITCODE -eq 0) {
        Write-TaskLog "Khong co thay doi bao cao moi — bo qua commit."
        exit 0
    }
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm"
    & git commit -m "Daily desk report $stamp" 2>&1 | ForEach-Object { Write-TaskLog $_ }

    # 3) Day len main (du dang o nhanh nao) de GitHub Pages cap nhat
    & git push origin HEAD:main 2>&1 | ForEach-Object { Write-TaskLog $_ }
    if ($LASTEXITCODE -ne 0) {
        Write-TaskLog "Push main that bai — thu push nhanh hien tai."
        & git push 2>&1 | ForEach-Object { Write-TaskLog $_ }
    }

    Write-TaskLog "=== HOAN TAT ==="
    exit 0
}
catch {
    Write-TaskLog "ERROR: $($_.Exception.Message)"
    exit 1
}
