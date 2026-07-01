from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
README = BASE / "README.md"
INSIGHTS = BASE / "insights.txt"

# Read all insights
with open(INSIGHTS, "r", encoding="utf-8") as f:
    ideas = [line.strip() for line in f if line.strip()]

# Create README if it doesn't exist
if not README.exists():
    with open(README, "w", encoding="utf-8") as f:
        f.write("# AI Governance Knowledge Base\n\n")
        f.write("Daily insights on using Artificial Intelligence for\n")
        f.write("governance information systems and decision making.\n\n")

# Read current README
with open(README, "r", encoding="utf-8") as f:
    content = f.read()

# Count how many insights have already been added
count = content.count("- ")

# Start over after reaching the end of the list
insight = ideas[count % len(ideas)]

today = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

# Append the next insight
with open(README, "a", encoding="utf-8") as f:
    f.write(f"## {today}\n")
    f.write(f"- {insight}\n\n")

print("README updated successfully.")