# Setup Instructions

## Files
- `daily_governance_update.ps1` — does the actual work (writes the sentence, commits, pushes)
- `daily_governance_update.bat` — thin wrapper that Task Scheduler calls (you never click this yourself)
- `register_task.ps1` — the real scheduling logic
- `register_task.bat` — **the ONE thing you click, ONE time, ever**
- `run_log.txt` — created automatically; check it if something doesn't run

## One-time setup (after this, you never touch anything again)

1. Confirm the repo is where you said:
   `C:\Users\Gebruiker\Downloads\Knowledge-Management-Informatics`
   and that it's on the `Fires` branch. If not:
   ```
   cd C:\Users\Gebruiker\Downloads\Knowledge-Management-Informatics
   git checkout Fires
   ```
   Make sure `git push origin Fires` already works **without** a
   username/password prompt (SSH key, or a saved token via Git
   Credential Manager). This is critical — Task Scheduler runs
   unattended in the background and can't type a password for you.

2. Put these 4-5 files in their own folder — **not inside** the
   `governance` subfolder, and not required to be inside the repo
   at all. E.g. `C:\Scripts\gov-readme\`.

3. Open `daily_governance_update.ps1` and confirm the top matches
   your setup:
   ```powershell
   $repoPath = "C:\Users\Gebruiker\Downloads\Knowledge-Management-Informatics"
   $branch    = "Fires"
   $subfolder = "governance"
   ```

4. Check your Windows time zone is set to a Central European zone
   (Settings → Time & language → Date & time) so "local time" lines
   up with CEST/CET automatically.

5. Right-click `register_task.bat` → **Run as administrator**.
   This registers ONE task, `DailyAIGovernanceReadme`, with 3 daily
   triggers: 06:00, 12:00, 18:00. The script prints a **CONFIRMED**
   message with the task name if it worked, or a clear **FAILED /
   WARNING** message if it didn't — read that output before assuming
   it worked.

6. Immediately verify it actually registered by running, in any
   PowerShell window:
   ```
   Get-ScheduledTask -TaskName DailyAIGovernanceReadme
   ```
   This should print the task's details. If it errors saying the task
   can't be found, registration silently failed — re-run step 5 as
   Administrator and check the printed output for the reason.

**That's it. From here on, nothing needs to be double-clicked, ever,
on any future day** — Windows itself wakes the task up automatically.

## How "fully automatic" is enforced
- `-WakeToRun`: if the PC is asleep at the scheduled time, Windows
  wakes it up just enough to run the task.
- `-StartWhenAvailable`: if the PC was fully off, or you weren't
  logged in, at 06:00, the task runs as soon as you next log in that
  day, instead of being skipped entirely.
- The task runs whenever you're logged in, even with the screen locked.
- It will **not** run if the PC is fully signed out or shut down for
  the entire day — that's the one real limitation. If you regularly
  shut down overnight, expect the 06:00 run to happen right after you
  log in each morning instead of exactly at 6:00.
- The only other things that stop it: you removing/renaming the files,
  or Windows Update resetting task state (rare, but check occasionally).

## If it stops running again
This has happened once before (task silently failed to register).
To check health at any time:
```powershell
Get-ScheduledTask -TaskName DailyAIGovernanceReadme
Get-ScheduledTaskInfo -TaskName DailyAIGovernanceReadme
```
The second command shows `LastRunTime`, `LastTaskResult` (0 = success,
anything else = an error), and `NextRunTime`. If the task is missing
entirely, just re-run `register_task.bat` as administrator — it's
safe to re-run any time, it replaces the old version first.

## What happens each day (3 runs → 3 commits)
- The script creates `governance/Readme.md` the *first* time it ever runs
  (with a title header).
- **Only the first run of the day** appends a new sentence line, e.g.:
  ```
  - **2026-07-01**: AI turns raw data into real-time insight for policy decisions.
  ```
  It cycles through 40 pre-written sentences (all ≤ 80 characters), then
  loops back to the first one after day 40 — still just 1 new sentence
  per day, not 3.
- **Every run** (all 3 times a day) also appends a timestamp line to
  `governance/.run-log.txt` and commits that. This gives you 3 commits/day
  even though only 1 sentence is added.
- Each run commits and pushes to the `Fires` branch automatically.

## Testing before you trust the schedule
Double-click `daily_governance_update.bat` once, manually, right after
setup. Check:
- `governance\Readme.md` got created/updated in your local repo
- The commit shows up on GitHub after a push
- `run_log.txt` has no errors

## To check, change, or remove the schedule later
- View: `schtasks /query /tn DailyAIGovernanceReadme /v /fo LIST`
- Delete: `schtasks /delete /tn DailyAIGovernanceReadme /f`
- To change run times, edit the `-At "HH:MM"` values in
  `register_task.ps1` and re-run `register_task.bat` as administrator
  (it removes the old version of the task first, so it's safe to re-run).
