# ============================================================
# register_task.ps1
# RUN THIS ONCE (as Administrator) to schedule the job.
#
# Creates ONE Windows Task Scheduler task ("DailyAIGovernanceReadme")
# with THREE daily triggers (06:00, 12:00, 18:00 local time), and
# configures it to be genuinely "set and forget":
#   - Wakes the computer from sleep to run, if needed
#   - If the PC was off/asleep at the scheduled time, runs the
#     missed task as soon as the PC is back on
#   - Runs even if you're not logged in (background)
#   - Doesn't require you to touch anything ever again
# ============================================================

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$batPath   = Join-Path $scriptDir "daily_governance_update.bat"
$taskName  = "DailyAIGovernanceReadme"

# Remove any old version of the task first (safe if it doesn't exist)
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# Action: run the .bat file
$action = New-ScheduledTaskAction -Execute $batPath

# Three triggers, one per run-time
$trigger1 = New-ScheduledTaskTrigger -Daily -At "06:00"
$trigger2 = New-ScheduledTaskTrigger -Daily -At "12:00"
$trigger3 = New-ScheduledTaskTrigger -Daily -At "18:00"

# Settings: wake the PC, catch up missed runs, don't require being logged in interactively
$settings = New-ScheduledTaskSettingsSet `
    -WakeToRun `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -MultipleInstances IgnoreNew

# Principal: run whether user is logged on or not, using the current user account.
# NOTE: this prompts you once for your Windows password so Windows can store it.
$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType S4U `
    -RunLevel Highest

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger @($trigger1, $trigger2, $trigger3) `
    -Settings $settings `
    -Principal $principal `
    -Description "Runs daily_governance_update.bat 3x/day: adds 1 sentence/day to governance/Readme.md and commits+pushes." | Out-Null

Write-Output ""
Write-Output "Task '$taskName' registered with 3 daily triggers: 06:00, 12:00, 18:00."
Write-Output "It will wake the PC if asleep, and catch up any missed run automatically."
Write-Output "You do not need to click anything else, ever, unless you move/rename these files."
Write-Output ""
Write-Output "Verify any time with:  schtasks /query /tn $taskName /v /fo LIST"
