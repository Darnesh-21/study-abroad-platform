import os
import re

ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
EXCLUDE_DIRS = {".git", "node_modules", "venv", ".next"}

# Covers most emoji ranges used in the project
EMOJI_RE = re.compile(
    "["
    "\U0001F1E6-\U0001F1FF"  # flags
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F700-\U0001F77F"  # alchemical
    "\U0001F780-\U0001F7FF"  # geometric extended
    "\U0001F800-\U0001F8FF"  # arrows C
    "\U0001F900-\U0001F9FF"  # supplemental symbols
    "\U0001FA00-\U0001FAFF"  # symbols & pictographs extended-A
    "\u2600-\u27BF"          # misc symbols
    "]"
)

changed = []

for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        rel = os.path.relpath(path, ROOT)
        try:
            with open(path, "r", encoding="utf-8") as f:
                original = f.read()
        except Exception:
            continue

        updated = EMOJI_RE.sub("", original)
        if updated != original:
            with open(path, "w", encoding="utf-8", newline="") as f:
                f.write(updated)
            changed.append(rel)

for rel in sorted(changed):
    print(rel)
