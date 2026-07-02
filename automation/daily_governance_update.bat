@echo off
REM ============================================================
REM daily_governance_update.bat
REM Wrapper that runs daily_governance_update.ps1
REM This .bat is what Windows Task Scheduler will call at 6:00 AM.
REM ============================================================

REM %~dp0 = the folder this .bat file lives in, so it works
REM regardless of where you place/move the folder.
set SCRIPT_DIR=%~dp0

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%daily_governance_update.ps1" >> "%SCRIPT_DIR%run_log.txt" 2>&1

exit /b 0
