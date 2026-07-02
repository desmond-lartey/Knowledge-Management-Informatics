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
   It will briefly ask for your Windows password (this lets the
   task run even when you're logged out — it's stored securely by
   Windows itself, not by this script). This registers ONE task,
   `DailyAIGovernanceReadme`, with 3 daily triggers: 06:00, 12:00, 18:00.

**That's it. From here on, nothing needs to be double-clicked, ever,
on any future day** — Windows itself wakes the task up automatically.

## How "fully automatic" is enforced
- `-WakeToRun`: if the PC is asleep at the scheduled time, Windows
  wakes it up just enough to run the task.
- `-StartWhenAvailable`: if the PC was fully off (not just asleep)
  at 06:00, the task runs as soon as the PC is next turned on,
  instead of being skipped.
- The task runs whether or not you're logged in (locked screen is fine).
- The only things that stop it: the PC being completely powered off
  for the entire day, or you removing/renaming the files.

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
