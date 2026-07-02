# ============================================================
# daily_governance_update.ps1
# Appends one sentence/day (<=80 chars) to governance\Readme.md
# about "AI as a Governance Information System for Decision-Making".
#
# This script is meant to run 3x/day (via 3 Task Scheduler triggers).
# - The FIRST run of the day adds the day's sentence to Readme.md.
# - EVERY run (all 3) also stamps governance\.run-log.txt with a
#   timestamp and commits that, so you get 3 commits/day even though
#   there's only 1 new sentence/day.
#
# EDIT the two variables below before first use.
# ============================================================

# --- 1. EDIT THIS if it's ever different: full path to your local clone ---
$repoPath = "C:\Users\Gebruiker\Downloads\Knowledge-Management-Informatics"

# --- 2. EDIT THIS if your branch/folder names differ ---
$branch    = "Fires"
$subfolder = "governance"
$fileName  = "Readme.md"

# ============================================================
# 40 rotating sentences (each already verified <= 80 characters)
# ============================================================
$sentences = @(
"AI turns raw data into real-time insight for policy decisions.",
"Governance AI systems flag emerging risks before they escalate.",
"Algorithms can simulate policy outcomes before laws are passed.",
"AI dashboards let officials track KPIs across departments live.",
"Predictive AI helps governments allocate budgets more wisely.",
"AI summarizes citizen feedback to inform government leaders.",
"AI detects fraud patterns hidden in public spending records.",
"Machine learning forecasts demand for essential public services.",
"AI-driven risk scores guide where regulators inspect first.",
"AI chatbots answer citizen queries around the clock reliably.",
"AI models help decision-makers weigh trade-offs objectively.",
"Governance AI reduces bias by standardizing decision criteria.",
"AI systems track policy impact metrics in near real time.",
"AI supports evidence-based lawmaking through data synthesis.",
"Smart AI alerts warn officials of anomalies in public data.",
"AI helps prioritize infrastructure repairs using sensor data.",
"AI-assisted audits catch irregularities faster than manual review.",
"Governance platforms use AI to route decisions to right teams.",
"AI clusters public comments to reveal common citizen concerns.",
"AI forecasting improves disaster response planning accuracy.",
"AI systems help match resources to areas of greatest need.",
"Natural language AI drafts policy summaries for quick review.",
"AI-powered scenario planning strengthens strategic governance.",
"AI helps detect corruption risks in procurement processes.",
"Governance AI enables transparent, auditable decision trails.",
"AI models rank policy options by projected social impact.",
"AI supports participatory governance via sentiment analysis.",
"Real-time AI analytics improve crisis decision-making speed.",
"AI helps regulators monitor compliance across many sectors.",
"Governance information systems use AI to reduce paperwork.",
"AI enables predictive maintenance for public infrastructure.",
"AI systems help balance competing stakeholder interests fairly.",
"AI-driven forecasts guide long-term urban planning choices.",
"Governance AI flags outlier decisions for human review.",
"AI helps translate complex data into clear policy briefs.",
"AI tools support faster, more consistent public decisions.",
"Machine learning improves accuracy of public health forecasts.",
"AI systems help track progress toward sustainable development.",
"Governance AI can personalize public services at scale.",
"AI strengthens accountability by logging every decision step."
)

# ============================================================
# Script logic - you shouldn't need to edit below this line
# ============================================================
try {
    Set-Location -Path $repoPath -ErrorAction Stop
} catch {
    Write-Error "Could not find repo path: $repoPath . Edit `$repoPath at the top of this script."
    exit 1
}

git checkout $branch
git pull origin $branch

$targetDir  = Join-Path $repoPath $subfolder
$targetFile = Join-Path $targetDir $fileName

if (-not (Test-Path $targetDir)) {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
}

$today = Get-Date -Format "yyyy-MM-dd"
$now   = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$logFile = Join-Path $targetDir ".run-log.txt"

# Create the Readme ONE TIME with a header, if it doesn't exist yet
if (-not (Test-Path $targetFile)) {
@"
# AI as a Governance Information System for Decision-Making

A daily log of short reflections (auto-generated, 6:00 AM CEST).

"@ | Set-Content -Path $targetFile -Encoding UTF8
}

# --- Part 1: add today's sentence to Readme.md, but only once/day ---
$existingContent = Get-Content -Path $targetFile -Raw
$addedSentenceToday = $existingContent -match [regex]::Escape($today)

if (-not $addedSentenceToday) {
    $existingLines = Select-String -Path $targetFile -Pattern "^\- \*\*\d{4}-\d{2}-\d{2}\*\*:" -AllMatches
    $dayCount = if ($existingLines) { $existingLines.Count } else { 0 }
    $index = $dayCount % $sentences.Count
    $sentence = $sentences[$index]

    $line = "- **$today**: $sentence"
    Add-Content -Path $targetFile -Value $line -Encoding UTF8
    Write-Output "Added new sentence for $today."
} else {
    Write-Output "Sentence for $today already present, not adding another."
}

# --- Part 2: stamp a run-log file EVERY run, so every run = a commit ---
Add-Content -Path $logFile -Value "Run at $now" -Encoding UTF8

# --- Commit + push whatever changed this run ---
git add "$subfolder/$fileName" "$subfolder/.run-log.txt"
git commit -m "Governance update run - $now"
git push origin $branch

Write-Output "Done: commit created for run at $now."
