import re

with open('static/new_script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Replace hardcoded "Historical snapshot"
js = js.replace("`${window.t('demoBadge')} · Historical snapshot · ${provenance.scenario_date}`", 
                "`${window.t('demoBadge')} · ${window.t('historicalSnapshot') || 'Historical snapshot'} · ${provenance.scenario_date}`")

with open('static/new_script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Patched Historical snapshot")
