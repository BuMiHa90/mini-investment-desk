$ErrorActionPreference = "Stop"

try {
    [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    $OutputEncoding = [System.Text.UTF8Encoding]::new($false)
    $PSStyle.OutputRendering = "PlainText"
}
catch {
    # Keep running even if the host does not expose console encoding controls.
}

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

$Claude = "C:\Users\ADMIN\.local\bin\claude.exe"
if (-not (Test-Path -LiteralPath $Claude)) {
    $Claude = "claude"
}

$Prompt = @'
Read CLAUDE.md first and follow all instructions there to run the daily Mini Investment Desk automation from this repository root.
'@

try {
    Write-TaskLog "Starting scheduled Claude daily runner."
    Write-TaskLog "Project root: $ProjectRoot"
    Write-TaskLog "Claude executable: $Claude"
    Write-TaskLog "Model: claude-sonnet-4-6"
    Write-TaskLog "Log file: $LogFile"
    Write-TaskLog "Launching Claude. Long-running pipeline steps can be quiet while Claude or nested agents work."

    & $Claude -p $Prompt --model "claude-sonnet-4-6" --dangerously-skip-permissions 2>&1 |
        ForEach-Object {
            $Text = ($_ | Out-String).TrimEnd()
            if ($Text) {
                Write-TaskLog $Text
            }
        }
    $ExitCode = $LASTEXITCODE
    Write-TaskLog "Claude exited with code $ExitCode."
    exit $ExitCode
}
catch {
    Write-TaskLog "ERROR: $($_.Exception.Message)"
    exit 1
}
