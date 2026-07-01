from pathlib import Path
from datetime import datetime
import random

BASE = Path(__file__).parent
README = BASE / "README.md"

# -----------------------------
# TIME-AWARE GOVERNANCE MODES
# -----------------------------

INSIGHT_THEMES = [
    "transparency", "accountability", "risk detection",
    "policy evaluation", "public trust", "decision intelligence"
]

POLICY_THEMES = [
    "resource allocation", "strategic planning", "public service delivery",
    "institutional efficiency", "data governance", "policy design"
]

REFLECTION_THEMES = [
    "ethical governance", "system resilience", "long-term impact",
    "fairness in decisions", "AI responsibility", "public good"
]

def generate_sentence(mode: str) -> str:
    if mode == "morning":
        theme = random.choice(INSIGHT_THEMES)
        templates = [
            f"AI improves {theme} in governance systems.",
            f"AI strengthens {theme} using real-time data.",
            f"AI enhances {theme} for better public decisions.",
            f"AI supports {theme} through evidence-based insights."
        ]

    elif mode == "afternoon":
        theme = random.choice(POLICY_THEMES)
        templates = [
            f"AI optimizes {theme} in public institutions.",
            f"AI supports better {theme} through analytics.",
            f"AI improves {theme} for government effectiveness.",
            f"AI enables adaptive {theme} in governance."
        ]

    else:  # evening
        theme = random.choice(REFLECTION_THEMES)
        templates = [
            f"AI raises questions about {theme} in governance.",
            f"AI ensures {theme} is considered in decisions.",
            f"AI highlights the importance of {theme}.",
            f"AI supports responsible {theme} in public systems."
        ]

    sentence = random.choice(templates)

    # enforce max 80 characters
    return sentence[:80].strip()


# -----------------------------
# DETERMINE MODE FROM TIME
# -----------------------------

hour = datetime.utcnow().hour

# CEST schedule mapped to UTC:
# 06:00 CEST → 04 UTC → morning
# 13:00 CEST → 11 UTC → afternoon
# 18:00 CEST → 16 UTC → evening

if hour in [4]:
    mode = "morning"
elif hour in [11]:
    mode = "afternoon"
elif hour in [16]:
    mode = "evening"
else:
    mode = "morning"

# -----------------------------
# WRITE TO README
# -----------------------------

if not README.exists():
    README.write_text("# AI Governance Knowledge Base\n\n", encoding="utf-8")

today = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

sentence = generate_sentence(mode)

with open(README, "a", encoding="utf-8") as f:
    f.write(f"## {today} ({mode})\n")
    f.write(f"- {sentence}\n\n")

print(f"Generated {mode} governance insight.")