# ============================================================
# register_task.ps1
# RUN THIS ONCE (as Administrator) to schedule the job.
#
# Creates ONE Windows Task Scheduler task ("DailyAIGovernanceReadme")
# with THREE daily triggers (06:00, 12:00 local time), and
# configures it to be genuinely "set and forget":
#   - Wakes the computer from sleep to run, if needed
#   - If the PC was asleep/off at the scheduled time, runs the
#     missed task as soon as you're next logged in
#   - Runs whenever you're logged in, even with the screen locked
#   - Verifies the task actually registered (no silent failures)
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


# Settings: wake the PC, catch up missed runs, don't require being logged in interactively
$settings = New-ScheduledTaskSettingsSet `
    -WakeToRun `
    -StartWhenAvailable `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10) `
    -MultipleInstances IgnoreNew

# Principal: run using the current user account, when the user is logged on
# (screen can be locked - that's fine). This is more reliable than S4U,
# which can silently fail to register on Microsoft-account-linked Windows logins.
$principal = New-ScheduledTaskPrincipal `
    -UserId "$env:USERDOMAIN\$env:USERNAME" `
    -LogonType Interactive `
    -RunLevel Highest

try {
    Register-ScheduledTask `
        -TaskName $taskName `
        -Action $action `
        -Trigger @($trigger1, $trigger2, $trigger3) `
        -Settings $settings `
        -Principal $principal `
        -Description "Runs daily_governance_update.bat 3x/day: adds 1 sentence/day to governance/Readme.md and commits+pushes." `
        -ErrorAction Stop | Out-Null
} catch {
    Write-Output ""
    Write-Output "REGISTRATION FAILED: $($_.Exception.Message)"
    Write-Output "The task was NOT created. Do not assume it's scheduled - fix the error above and re-run this script."
    exit 1
}

# Verify it actually stuck (Register-ScheduledTask can occasionally report
# success but not persist the task - so we double check here).
$verify = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if (-not $verify) {
    Write-Output ""
    Write-Output "WARNING: Registration command completed, but the task was NOT found"
    Write-Output "when checked afterward. Something silently failed. Do not assume this"
    Write-Output "worked - open Task Scheduler manually and check, or re-run this script"
    Write-Output "as Administrator."
    exit 1
}

Write-Output ""
Write-Output "CONFIRMED: Task '$taskName' is registered and visible in Task Scheduler,"
Write-Output "with 2 daily triggers: 06:00, 12:00."
Write-Output "It runs whenever you are logged in (screen locked is fine) and will"
Write-Output "wake the PC from sleep and catch up any missed run automatically."
Write-Output "It will NOT run if the PC is fully signed out or shut down at the"
Write-Output "scheduled time - it will run as soon as you next log in that day instead."
Write-Output ""
Write-Output "Verify any time with:  Get-ScheduledTask -TaskName $taskName"
Write-Output "Or open Task Scheduler and look under Task Scheduler Library."
