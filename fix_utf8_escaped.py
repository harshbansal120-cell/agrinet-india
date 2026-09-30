import os
import sys

replacements = {
    "\u00e2\u2020\u2019": "\u2192", # â†’ to →
    "\u00e2\u20ac\u201d": "\u2014", # â€” to — (em dash)
    "\u00e2\u20ac\u201c": "\u2013", # â€“ to – (en dash)
    "\u00c3\u0082\u00b0C": "\u00b0C", # Â°C to °C
    "0\u00e21": "0-1" # 0â1 to 0-1
}

count = 0
for root, _, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "venv" in root or ".git" in root: continue
    for f in files:
        if f.endswith(".py") or f.endswith(".html"):
            path = os.path.join(root, f)
            if path == os.path.abspath(__file__): continue
            
            with open(path, "r", encoding="utf-8") as file:
                try:
                    content = file.read()
                except UnicodeDecodeError:
                    continue
            
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
