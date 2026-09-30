import os
import sys

replacements = {
    "→": "→",
    "—": "—",
    "–": "–",
    "Â°C": "°C",
    "0-1": "0-1"
}

count = 0
for root, _, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "venv" in root or ".git" in root: continue
    for f in files:
        if f.endswith(".py") or f.endswith(".html"):
            path = os.path.join(root, f)
            if path == os.path.abspath(__file__): continue
            
            with open(path, "rb") as file:
                raw = file.read()
            
            try:
                content = raw.decode("utf-8")
            except UnicodeDecodeError:
                content = raw.decode("cp1252")
            
            orig = content
            for k, v in replacements.items():
                content = content.replace(k, v)
                
            if content != orig:
                with open(path, "w", encoding="utf-8") as out:
                    out.write(content)
                print(f"Fixed {path}")
                count += 1
                sys.stdout.flush()

print(f"Total files fixed via string replacement: {count}")
