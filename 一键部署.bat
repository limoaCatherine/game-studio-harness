@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
where powershell >nul 2>nul
if errorlevel 1 (
  echo 需要 PowerShell。也可以直接运行: python install\install.py --workspace 你的业务根
  exit /b 2
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0一键部署.ps1" %*
exit /b %ERRORLEVEL%
