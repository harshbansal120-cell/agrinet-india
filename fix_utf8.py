import os
import sys

replacements = {
    "→".encode("utf-8"): "→".encode("utf-8"),
    "—".encode("utf-8"): "—".encode("utf-8"),
    "–".encode("utf-8"): "–".encode("utf-8"),
    "°C".encode("utf-8"): "°C".encode("utf-8"),
    "0-1".encode("utf-8"): "0-1".encode("utf-8")
}

count = 0
for root, _, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
    if "venv" in root or ".git" in root: continue
    for f in files:
        if f.endswith(".py") or f.endswith(".html"):
            path = os.path.join(root, f)
            with open(path, "rb") as file:
                content = file.read()
            
            orig = content
            for k, v in replacements.items():
                content = content.replace(k, v)
                
            if content != orig:
                with open(path, "wb") as out:
                    out.write(content)
                print(f"Fixed {path}")
                count += 1
                sys.stdout.flush()

print(f"Total files fixed via byte replacement: {count}")
