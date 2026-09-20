# 一键把 Game Studio Harness 部署到本机 AI 编程工具与业务根。不装 DCC，不写密钥。
[CmdletBinding()]
param(
    [string]$Workspace = "",
    [string]$Tools = "legacy",
    [ValidateSet("minimal", "core", "full")]
    [string]$Profile = "full",
    [switch]$CursorOnly,
    [switch]$WriteMcp,
    [switch]$DryRun,
    [switch]$Guided
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$extra = @()
if ($Workspace) { $extra += @("-Workspace", $Workspace) }
if ($CursorOnly) { $extra += "-CursorOnly" }
if ($WriteMcp) { $extra += "-WriteMcp" }
if ($DryRun) { $extra += "-DryRun" }
if ($Guided) { $extra += "-Guided" }
& (Join-Path $Root "install.ps1") -Command setup -Tools $Tools -Profile $Profile -Yes @extra
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
if (-not $DryRun) {
    $vextra = @()
    if ($Workspace) { $vextra += @("-Workspace", $Workspace) }
    if ($CursorOnly) { $vextra += "-CursorOnly" }
    & (Join-Path $Root "install.ps1") -Command verify -Tools $Tools -Profile $Profile -Yes @vextra
    if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
}
Write-Host "部署完成。" -ForegroundColor Green
exit 0
