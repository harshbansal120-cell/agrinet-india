import re

def patch_script():
    with open('static/new_script.js', 'r', encoding='utf-8') as f:
        js = f.read()

    # dx-badge HEALTHY / ISSUE DETECTED
    old_badge = "$('dx-badge').textContent = d.healthy ? 'HEALTHY' : 'ISSUE DETECTED';"
    new_badge = "$('dx-badge').textContent = d.healthy ? (window.t('status_healthy') || 'HEALTHY') : (window.t('status_issue') || 'ISSUE DETECTED');"
    js = js.replace(old_badge, new_badge)

    # dx-conf
    old_conf = "$('dx-conf').textContent = `Conf: ${d.confidence.toUpperCase()}`;"
    new_conf = "$('dx-conf').textContent = `${window.t('dx_conf') || 'Conf:'} ${window.localizeEnum(d.confidence, 'confidence').toUpperCase()}`;"
    js = js.replace(old_conf, new_conf)

    # dx-exp
    old_exp = "$('dx-exp').textContent = d.expert_escalation || 'Monitor closely.';"
    new_exp = "$('dx-exp').textContent = d.expert_escalation || (window.t('dx_monitor') || 'Monitor closely.');"
    js = js.replace(old_exp, new_exp)

    # suitability badge check string literal issue
    old_suit = "r.suitability==='high'?'badge-live':'badge-model'"
    new_suit = "String(r.suitability).toLowerCase()==='high'?'badge-live':'badge-model'"
    js = js.replace(old_suit, new_suit)
    
    with open('static/new_script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
    print("new_script.js diagnosis section patched.")

def patch_lang():
    with open('static/lang.js', 'r', encoding='utf-8') as f:
        js = f.read()

    vocab = {
        'en': {"status_issue": "ISSUE DETECTED", "dx_conf": "Conf:", "dx_monitor": "Monitor closely."},
        'hi': {"status_issue": "समस्या मिली", "dx_conf": "विश्वसनीयता:", "dx_monitor": "करीब से निगरानी करें।"},
        'ta': {"status_issue": "பிரச்சினை கண்டறியப்பட்டது", "dx_conf": "நம்பகத்தன்மை:", "dx_monitor": "கூர்ந்து கண்காணிக்கவும்."}
    }
    
    all_langs = ['en', 'hi', 'ta', 'te', 'bn', 'mr', 'pa', 'gu', 'kn', 'ml']
    
    for lang in all_langs:
        idx = js.find(f'"{lang}": {{')
        if idx == -1: continue
        
        subset = vocab.get(lang, vocab['en'])
        injection = ""
        for k, v in subset.items():
            injection += f'    "{k}": "{v}",\n'
        
        # inject immediately after lang: {
        js = js[:idx + len(f'"{lang}": {{') + 1] + injection + js[idx + len(f'"{lang}": {{') + 1:]

    with open('static/lang.js', 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("lang.js diagnosis patched.")

if __name__ == '__main__':
    patch_script()
    patch_lang()
