@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
where powershell >nul 2>nul
if errorlevel 1 (
  echo Need PowerShell, or run: python -m gsh setup --workspace YOUR_STUDIO_ROOT
  exit /b 2
)
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0一键部署.ps1" %*
exit /b %ERRORLEVEL%
