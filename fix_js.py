import json
import re

with open('static/new_script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the broken window.t('...') logic
# First, fix `documenwindow.t(...)` back to `document....`
js = re.sub(r'([a-zA-Z0-9_]+)window\.t\(\'([a-zA-Z0-9_]+)\'\)', r'\1t.\2', js)
# Wait, let me be very careful.
# `documenwindow.t('getElementById')` was `document.getElementById`.
# `documen` + `window.t('` + `getElementById` + `')`
# This transforms `documenwindow.t('getElementById')` back to `document.getElementById`
def fix_match(m):
    prefix = m.group(1)
    field = m.group(2)
    # the original text before the dot was prefix + 't'
    return f"{prefix}t.{field}"

js = re.sub(r'([a-zA-Z_]+)window\.t\(\'([a-zA-Z0-9_]+)\'\)', fix_match, js)

with open('static/new_script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Fixed broken JS references.")
