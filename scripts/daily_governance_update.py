#!/usr/bin/env python3
"""
daily_governance_update.py
Appends one sentence/day (<=80 chars) to governance/Readme.md about
"AI as a Governance Information System for Decision-Making".

Runs via GitHub Actions (see .github/workflows/daily-governance.yml):
- The FIRST run of the day adds the day's sentence to Readme.md.
- EVERY run also stamps governance/.run-log.txt with a timestamp.
- Readme.md is pruned to only show the most recent KEEP_DAYS daily
  entries, so it doesn't grow forever - older entries are dropped
  from the display (full history still lives in git commit log /
  .run-log.txt, nothing is "lost", it's just not shown in the file).
"""

import os
import re
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBFOLDER = "governance"
README_PATH = os.path.join(REPO_ROOT, SUBFOLDER, "Readme.md")
LOG_PATH = os.path.join(REPO_ROOT, SUBFOLDER, ".run-log.txt")

# How many most-recent daily entries to keep visible in Readme.md.
# 7 = today + the previous 6 days, matching "last 6 days" + today.
KEEP_DAYS = 7

SENTENCES = [
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
    "AI strengthens accountability by logging every decision step.",
]

HEADER = """# AI as a Governance Information System for Decision-Making

A daily log of short reflections (auto-generated, 6:00 AM CEST).
Showing the most recent {keep_days} days.

""".format(keep_days=KEEP_DAYS)

HEADER_RE = re.compile(r"^.*?(?=^\- \*\*\d{4}-\d{2}-\d{2}\*\*:)", re.DOTALL | re.MULTILINE)
DAY_LINE_RE = re.compile(r"^\- \*\*(\d{4}-\d{2}-\d{2})\*\*:.*$", re.MULTILINE)


def main():
    os.makedirs(os.path.dirname(README_PATH), exist_ok=True)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    now_str = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")

    if not os.path.exists(README_PATH):
        with open(README_PATH, "w", encoding="utf-8") as f:
            f.write(HEADER)
        print("Created new Readme.md with header.")

    with open(README_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    # Pull out existing daily lines (date, full_line) in file order (oldest first).
    existing_lines = DAY_LINE_RE.findall(content)  # list of dates only
    all_day_lines = DAY_LINE_RE.finditer(content)
    day_entries = [(m.group(1), m.group(0)) for m in DAY_LINE_RE.finditer(content)]

    # Track how many total daily entries have EVER been written, for sentence
    # rotation - count from .run-log.txt history if present, else fall back
    # to what's currently visible in the file. This way the rotation keeps
    # advancing correctly even after old entries get pruned from Readme.md.
    total_days_seen = count_total_days_from_log()
    if total_days_seen is None:
        total_days_seen = len(day_entries)

    if today not in existing_lines:
        index = total_days_seen % len(SENTENCES)
        sentence = SENTENCES[index]
        day_entries.append((today, f"- **{today}**: {sentence}"))
        print(f"Added sentence for {today}: {sentence}")
    else:
        print(f"Sentence for {today} already present, not adding another.")

    # Keep only the most recent KEEP_DAYS entries by date.
    day_entries.sort(key=lambda pair: pair[0])
    trimmed = day_entries[-KEEP_DAYS:]

    new_body = "\n".join(line for _, line in trimmed) + "\n"
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(HEADER + new_body)

    # Record today's date permanently in the log so sentence rotation and
    # "already posted today" checks stay correct even after Readme.md pruning.
    record_day_in_log(today)

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"Run at {now_str}\n")
    print(f"Stamped run log at {now_str}")


def count_total_days_from_log():
    """Counts how many distinct DAY: lines have ever been recorded, using a
    permanent record kept at the top of .run-log.txt (separate from the
    per-run timestamp lines). Returns None if no such record exists yet."""
    if not os.path.exists(LOG_PATH):
        return None
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    days = set(re.findall(r"^DAY: (\d{4}-\d{2}-\d{2})$", content, re.MULTILINE))
    if not days:
        return None
    return len(days)


def record_day_in_log(today):
    """Appends a permanent 'DAY: YYYY-MM-DD' marker line (once per day) so
    sentence rotation keeps advancing correctly even after old Readme.md
    entries are pruned away."""
    existing = ""
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            existing = f.read()
    marker = f"DAY: {today}"
    if marker not in existing:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(marker + "\n")


if __name__ == "__main__":
    main()
