#!/usr/bin/env python3
"""
daily_governance_update.py
Appends one sentence/day (<=80 chars) to governance/Readme.md about
"AI as a Governance Information System for Decision-Making".

Runs 3x/day via GitHub Actions (see .github/workflows/daily-governance.yml):
- The FIRST run of the day adds the day's sentence to Readme.md.
- EVERY run also stamps governance/.run-log.txt with a timestamp,
  so there are 3 commits/day even though there's only 1 new sentence/day.
"""

import os
import re
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUBFOLDER = "governance"
README_PATH = os.path.join(REPO_ROOT, SUBFOLDER, "Readme.md")
LOG_PATH = os.path.join(REPO_ROOT, SUBFOLDER, ".run-log.txt")

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

"""

DAY_LINE_RE = re.compile(r"^\- \*\*(\d{4}-\d{2}-\d{2})\*\*:", re.MULTILINE)


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

    existing_days = DAY_LINE_RE.findall(content)

    if today not in existing_days:
        index = len(existing_days) % len(SENTENCES)
        sentence = SENTENCES[index]
        line = f"- **{today}**: {sentence}\n"
        with open(README_PATH, "a", encoding="utf-8") as f:
            f.write(line)
        print(f"Added sentence for {today}: {sentence}")
    else:
        print(f"Sentence for {today} already present, not adding another.")

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"Run at {now_str}\n")
    print(f"Stamped run log at {now_str}")


if __name__ == "__main__":
    main()
