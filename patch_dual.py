import re

def update_script():
    with open('static/new_script.js', 'r', encoding='utf-8') as f:
        js = f.read()
        
    t_func = """window.t = function(key, params = {}) {
    const lang = currentLanguage || 'en';
    const dictionary = UI_TRANSLATIONS[lang] || UI_TRANSLATIONS.en;
    let enVal = UI_TRANSLATIONS.en[key] ?? key;
    let localVal = dictionary[key] ?? enVal;

    if (typeof enVal !== 'string') enVal = String(enVal);
    if (typeof localVal !== 'string') localVal = String(localVal);

    for (const [param, replacement] of Object.entries(params)) {
        enVal = enVal.replaceAll(`{${param}}`, String(replacement));
        localVal = localVal.replaceAll(`{${param}}`, String(replacement));
    }

    if (lang === 'en') return enVal;
    
    // Some keys might return identical in English (untranslated). If it's untranslated, just return English.
    if (localVal === enVal || localVal === key) return enVal;
    
    return `${enVal} / ${localVal}`;
};"""

    # find and replace window.t in file
    start_idx = js.find('window.t = function(key, params')
    end_idx = js.find('};', start_idx) + 2
    if start_idx != -1:
        js = js[:start_idx] + t_func + js[end_idx:]

    loc_func = """window.localizePlace = function(name, language = currentLanguage) {
    if(!name) return "";
    const enStr = LOCATION_TRANSLATIONS[name]?.en || name;
    if (language === 'en') return enStr;
    const localStr = LOCATION_TRANSLATIONS[name]?.[language] || enStr;
    if (localStr === enStr) return enStr;
    return `${enStr} / ${localStr}`;
};"""
    
    start_idx2 = js.find('window.localizePlace = function(name')
    end_idx2 = js.find('};', start_idx2) + 2
    if start_idx2 != -1:
        js = js[:start_idx2] + loc_func + js[end_idx2:]

    with open('static/new_script.js', 'w', encoding='utf-8') as f:
        f.write(js)
    
if __name__ == '__main__':
    update_script()
    print("Dual language patched in script.")
