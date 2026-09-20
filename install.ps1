# Game Studio Harness — Windows 入口。不装 DCC，不写密钥。
[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [string]$Command = "setup",
    [string]$Workspace = "",
    [string]$Tools = "legacy",
    [ValidateSet("minimal", "core", "full")]
    [string]$Profile = "full",
    [string]$IsolateRoot = "",
    [switch]$CursorOnly,
    [switch]$WriteMcp,
    [switch]$DryRun,
    [switch]$Guided,
    [switch]$Yes
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Find-Python {
    foreach ($name in @("python", "py")) {
        $cmd = Get-Command $name -ErrorAction SilentlyContinue
        if ($cmd) {
            $ver = & $cmd --version 2>$null
            if ($ver -match "Python 3\.(1[1-9]|[2-9]\d)") {
                return $cmd.Source
            }
            if ($name -eq "py") {
                $probe = & $cmd -3 --version 2>$null
                if ($probe -match "Python 3\.(1[1-9]|[2-9]\d)") {
                    return @($cmd.Source, "-3")
                }
            }
        }
    }
    return $null
}

$py = Find-Python
if (-not $py) {
    Write-Host "未找到 Python 3.11+。请先安装并勾选 Add to PATH，然后重开终端。" -ForegroundColor Red
    Write-Host "https://www.python.org/downloads/"
    exit 2
}

$pyArgs = @()
if ($py -is [array]) {
    $pyArgs = $py[1..($py.Length - 1)]
    $py = $py[0]
}

$invoke = @($py) + $pyArgs + @("-m", "gsh")
if ($Command -notin @("setup", "sync", "verify", "doctor", "uninstall")) {
    $invoke += "setup"
} else {
    $invoke += $Command
}
if ($CursorOnly) { $invoke += "--cursor-only" }
elseif ($Workspace) { $invoke += @("--workspace", $Workspace) }
$invoke += @("--tools", $Tools)
$invoke += @("--profile", $Profile)
if ($IsolateRoot) { $invoke += @("--isolate-root", $IsolateRoot) }
if ($WriteMcp) { $invoke += "--write-mcp" }
if ($DryRun) { $invoke += "--dry-run" }
if ($Guided) { $invoke += "--guided" }
if ($Yes) { $invoke += "--yes" }

& $invoke[0] $invoke[1..($invoke.Length - 1)]
exit $LASTEXITCODE
