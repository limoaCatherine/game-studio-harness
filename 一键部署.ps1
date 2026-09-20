# 一键把 Game Studio Harness 部署到本机多套 AI 编程工具与业务根。不装 DCC，不写密钥。
[CmdletBinding()]
param(
    [string]$Workspace = "",
    [string]$Tools = "all",
    [switch]$CursorOnly,
    [switch]$WriteMcp,
    [switch]$DryRun
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

if (-not $CursorOnly -and -not $Workspace) {
    $default = Join-Path (Split-Path $Root -Parent) "studio-root"
    $inputWs = Read-Host "业务根绝对路径（将创建 .harness，回车默认 $default）"
    if ([string]::IsNullOrWhiteSpace($inputWs)) {
        $Workspace = $default
    } else {
        $Workspace = $inputWs.Trim().Trim('"')
    }
}

$install = @($py) + $pyArgs + @((Join-Path $Root "install\install.py"))
$verify = @($py) + $pyArgs + @((Join-Path $Root "install\verify_install.py"))
if ($CursorOnly) {
    $install += "--cursor-only"
    $verify += "--cursor-only"
} else {
    New-Item -ItemType Directory -Force -Path $Workspace | Out-Null
    $install += @("--workspace", $Workspace)
    $verify += @("--workspace", $Workspace)
}
$install += @("--tools", $Tools)
$verify += @("--tools", $Tools)
if ($WriteMcp) { $install += "--write-mcp" }
if ($DryRun) { $install += "--dry-run" }

Write-Host "部署架构文件..." -ForegroundColor Cyan
& $install[0] $install[1..($install.Length - 1)]
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if (-not $DryRun) {
    Write-Host "验收架构是否落地..." -ForegroundColor Cyan
    & $verify[0] $verify[1..($verify.Length - 1)]
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}

Write-Host ""
Write-Host "部署完成。" -ForegroundColor Green
if (-not $CursorOnly) {
    Write-Host "用 Cursor / Claude Code / Codex / Grok / DeepSeek Harness 打开 $Workspace"
}
exit 0
