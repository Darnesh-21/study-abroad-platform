import os
import re

root = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
emoji_pattern = re.compile(r"[\U0001F300-\U0001F6FF]")
matches = {}
for dirpath, dirnames, filenames in os.walk(root):
    dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "venv"}]
    for filename in filenames:
        path = os.path.join(dirpath, filename)
        rel = os.path.relpath(path, root)
        try:
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
        except Exception:
            continue
        if emoji_pattern.search(text):
            matches.setdefault(rel, []).extend(emoji_pattern.findall(text))

for path, found in matches.items():
    print(f"{path}: {sorted(set(found))}")
