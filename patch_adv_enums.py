import re
import json

def patch_lang():
    with open('static/lang.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # The new keys to add for each language. Just fallback to English for others, but exact for en, hi, ta.
    vocab = {
        'en': {
            "enum_status_good": "Good", "enum_status_monitor": "Monitor", "enum_status_critical": "Critical",
            "enum_severity_low": "Low", "enum_severity_medium": "Medium", "enum_severity_high": "High",
            "enum_priority_now": "Now", "enum_priority_this_week": "This week", "enum_priority_monitor": "Monitor",
            "enum_suitability_high": "High", "enum_suitability_moderate": "Moderate", "enum_suitability_conditional": "Conditional",
            "enum_bool_true": "Yes", "enum_bool_false": "No",
            "enum_health_healthy": "Healthy", "enum_health_unhealthy": "Unhealthy"
        },
        'hi': {
            "enum_status_good": "अच्छा", "enum_status_monitor": "निगरानी आवश्यक", "enum_status_critical": "गंभीर",
            "enum_severity_low": "कम", "enum_severity_medium": "मध्यम", "enum_severity_high": "उच्च",
            "enum_priority_now": "अभी", "enum_priority_this_week": "इस सप्ताह", "enum_priority_monitor": "निगरानी करें",
            "enum_suitability_high": "उच्च", "enum_suitability_moderate": "मध्यम", "enum_suitability_conditional": "शर्तों के साथ",
            "enum_bool_true": "हाँ", "enum_bool_false": "नहीं",
            "enum_health_healthy": "स्वस्थ", "enum_health_unhealthy": "अस्वस्थ"
        },
        'ta': {
            "enum_status_good": "நன்று", "enum_status_monitor": "கண்காணிக்கவும்", "enum_status_critical": "சிக்கலானது",
            "enum_severity_low": "குறைவு", "enum_severity_medium": "நடுத்தரம்", "enum_severity_high": "அதிகம்",
            "enum_priority_now": "இப்போது", "enum_priority_this_week": "இந்த வாரம்", "enum_priority_monitor": "கண்காணிக்கவும்",
            "enum_suitability_high": "அதிகம்", "enum_suitability_moderate": "நடுத்தரம்", "enum_suitability_conditional": "நிபந்தனைக்கு உட்பட்டது",
            "enum_bool_true": "ஆம்", "enum_bool_false": "இல்லை",
            "enum_health_healthy": "ஆரோக்கியமானது", "enum_health_unhealthy": "ஆரோக்கியமற்றது"
        }
    }

    modified = js
    all_langs = ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'pa', 'gu', 'kn', 'ml']
    
    for lang in all_langs:
        idx = modified.find(f'"{lang}": {{')
        if idx == -1: continue
        
        subset = vocab.get(lang, vocab['en'])
        injection = ""
        for k, v in subset.items():
            injection += f'    "{k}": "{v}",\n'
        
        # inject immediately after lang: {
        modified = modified[:idx + len(f'"{lang}": {{') + 1] + injection + modified[idx + len(f'"{lang}": {{') + 1:]

    with open('static/lang.js', 'w', encoding='utf-8') as f:
        f.write(modified)
    print("lang.js patched.")

def patch_script():
    with open('static/new_script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # Add localizeEnum globally, near window.t
    if "window.localizeEnum = function" not in js:
        helper = """window.localizeEnum = function(val, category) {
    if (val === undefined || val === null) return '';
    if (typeof val === 'boolean') return window.t('enum_bool_' + String(val)) || String(val);
    const key = `enum_${category}_${String(val).toLowerCase()}`;
    const result = window.t(key);
    return result !== key ? result : String(val);
};

"""
        idx = js.find('window.t = ')
        if idx != -1:
            js = js[:idx] + helper + js[idx:]
        else:
            print("Failed to inject localizeEnum")

    # Replace enum values in renderAdvisory
    # 1. field_status -> status
    js = js.replace("${esc(a.field_status?.status || '')}", "${esc(window.localizeEnum(a.field_status?.status, 'status') || '')}")
    # 2. severity
    js = js.replace("${esc(r.severity)}", "${esc(window.localizeEnum(r.severity, 'severity'))}")
    # 3. priority/timing for immediate actions
    js = js.replace('float:right">${esc(r.timing)}</span></div>', 'float:right">${esc(window.localizeEnum(r.timing, "priority"))}</span></div>')
    # 4. crop suitability
    js = js.replace('float:right">${esc(r.suitability)}</span></div>', 'float:right">${esc(window.localizeEnum(r.suitability, "suitability"))}</span></div>')

    # Update updateUI to renderAdvisory
    updateui_patch = """
  renderScenarios();
  if (currentFieldState && currentAdvisory) {
      renderAdvisory(currentAdvisory);
  }
}"""
    
    if "if (currentFieldState && currentAdvisory)" not in js:
        # replace end of updateUI
        old_end = """
  renderScenarios();
}"""
        new_end = updateui_patch
        js = js.replace(old_end, new_end)

    with open('static/new_script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    print("new_script.js patched.")

if __name__ == '__main__':
    patch_lang()
    patch_script()
