@echo off
REM ============================================================
REM register_task.bat
REM RUN THIS ONCE (right-click -> Run as administrator).
REM This is the ONLY manual step, ever. It calls register_task.ps1,
REM which sets up a Task Scheduler job that runs completely on its
REM own from now on - 3x/day, forever, with no further clicking.
REM ============================================================

set SCRIPT_DIR=%~dp0

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%register_task.ps1"

pause
