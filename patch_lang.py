import re

with open('static/lang.js', 'r', encoding='utf-8') as f:
    js = f.read()

# I will replace the English words for all language sections.
# But instead of finding all of them, I can use a simple python dict to find and replace per language.

transl = {
    "hi": {"liveBadge": "लाइव", "demoBadge": "डेमो", "modelBadge": "मॉडल", "precomputedBadge": "पूर्व-परिकलित", "source": "स्रोत:"},
    "ta": {"liveBadge": "நேரலை", "demoBadge": "டெமோ", "modelBadge": "மாதிரி", "precomputedBadge": "முன்கூட்டியே கணக்கிடப்பட்டது", "source": "மூலம்:"},
    "te": {"liveBadge": "ప్రత్యక్షం", "demoBadge": "డెమో", "modelBadge": "నమూనా", "precomputedBadge": "ముందుగా లెక్కించబడింది", "source": "మూలం:"},
    "bn": {"liveBadge": "সরাসরি", "demoBadge": "ডেমো", "modelBadge": "মডেল", "precomputedBadge": "আগে থেকে হিসাবকৃত", "source": "উৎস:"},
    "mr": {"liveBadge": "थेट", "demoBadge": "डेमो", "modelBadge": "मॉडेल", "precomputedBadge": "पूर्वनिर्धारित", "source": "स्रोत:"},
    "pa": {"liveBadge": "ਲਾਈਵ", "demoBadge": "ਡੈਮੋ", "modelBadge": "ਮਾਡਲ", "precomputedBadge": "ਪਹਿਲਾਂ ਤੋਂ ਗਿਣਿਆ ਹੋਇਆ", "source": "ਸਰੋਤ:"},
    "gu": {"liveBadge": "લાઇવ", "demoBadge": "ડેમો", "modelBadge": "મોડેલ", "precomputedBadge": "અગાઉથી ગણતરી કરેલ", "source": "સ્ત્રોત:"},
    "kn": {"liveBadge": "ಲೈವ್", "demoBadge": "ಡೆಮೊ", "modelBadge": "ಮಾದರಿ", "precomputedBadge": "ಮೊದಲೇ ಲೆಕ್ಕಹಾಕಿದ", "source": "ಮೂಲ:"},
    "ml": {"liveBadge": "തത്സമയം", "demoBadge": "ഡെമോ", "modelBadge": "മാതൃക", "precomputedBadge": "നേരത്തെ കണക്കാക്കിയത്", "source": "ഉറവിടം:"},
}

for lang, vals in transl.items():
    # Because lang.js has 
    # "ta": { ... }
    # I can capture the block of the language.
    pattern = r'("' + lang + r'":\s*\{)(.*?)(\},?\n\s*"[a-z]{2}":|\}\s*$;)'
    idx_start = js.find('"' + lang + '": {')
    if idx_start == -1: continue
    
    # Simple regex to replace just inside this block is tricky. Let's do a substring replace for specific keys.
    # We find the boundary of the language block
    idx_end = js.find('},', idx_start)
    if idx_end == -1: idx_end = len(js)
    
    block = js[idx_start:idx_end]
    for key, val in vals.items():
        # Match `"key": "..."`
        block = re.sub(rf'"{key}":\s*"[^"]*"', f'"{key}": "{val}"', block)
    
    js = js[:idx_start] + block + js[idx_end:]

with open('static/lang.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Patched lang.js successfully.")
