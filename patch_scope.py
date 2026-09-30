import json
import re

with open('static/new_script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Remove global existing t() if any
js = re.sub(r'function t\(key, args\) \{\n   let str =[\s\S]*?return str;\n\}', '', js)

# 2. Add window.t and window.localizePlace at the top
helpers = """
window.t = function(key, params = {}) {
    const lang = window.currentLanguage || 'en';
    const dictionary = UI_TRANSLATIONS[lang] || UI_TRANSLATIONS.en;
    let value = dictionary[key] ?? UI_TRANSLATIONS.en[key] ?? key;

    if (typeof value !== 'string') {
        value = String(value);
    }

    for (const [param, replacement] of Object.entries(params)) {
        value = value.replaceAll(`{${param}}`, String(replacement));
    }

    return value;
};

const LOCATION_TRANSLATIONS = {
    "Sambalpur": { "en": "Sambalpur", "hi": "संबलपुर", "ta": "சம்பல்பூர்", "te": "సంబల్పూర్", "bn": "সম্বলপুর", "mr": "संबलपूर", "pa": "ਸੰਬਲਪੁਰ", "gu": "સંબલપુર", "kn": "ಸಂಬಲ್ಪುರ", "ml": "സംബൽപൂർ" },
    "Odisha": { "en": "Odisha", "hi": "ओडिशा", "ta": "ஒடிசா", "te": "ఒడిశా", "bn": "ওড়িশা", "mr": "ओडिशा", "pa": "ਓਡੀਸ਼ਾ", "gu": "ઓડિશા", "kn": "ಒಡಿಶಾ", "ml": "ഒഡീഷ" },
    "Agra": { "en": "Agra", "hi": "आगरा", "ta": "ஆக்ரா", "te": "ఆగ్రా", "bn": "আগ্রা", "mr": "आग्रा", "pa": "ਆਗਰਾ", "gu": "આગરા", "kn": "ಆಗ್ರಾ", "ml": "ആഗ്ര" },
    "Uttar Pradesh": { "en": "Uttar Pradesh", "hi": "उत्तर प्रदेश", "ta": "உத்தரப் பிரதேசம்", "te": "ఉత్తర ప్రదేశ్", "bn": "উত্তরপ্রদেশ", "mr": "उत्तर प्रदेश", "pa": "ਉੱਤਰ ਪ੍ਰਦੇਸ਼", "gu": "ઉત્તર પ્રદેશ", "kn": "ಉತ್ತರ ಪ್ರದೇಶ", "ml": "ഉത്തർപ്രദേശ്" },
    "Ludhiana": { "en": "Ludhiana", "hi": "लुधियाना", "ta": "லுதியானா", "te": "లుధియానా", "bn": "লুধিয়ানা", "mr": "लुधियाना", "pa": "ਲੁਧਿਆਣਾ", "gu": "લુધિયાણા", "kn": "ಲುಧಿಯಾನಾ", "ml": "ലുധിയാന" },
    "Punjab": { "en": "Punjab", "hi": "पंजाब", "ta": "பஞ்சாப்", "te": "పంజాబ్", "bn": "পাঞ্জাব", "mr": "पंजाब", "pa": "ਪੰਜਾਬ", "gu": "પંજાબ", "kn": "ಪಂಜಾಬ್", "ml": "പഞ്ചാബ്" },
    "Nashik": { "en": "Nashik", "hi": "नाशिक", "ta": "நாசிக்", "te": "నాసిక్", "bn": "নাশিক", "mr": "नाशिक", "pa": "ਨਾਸਿਕ", "gu": "નાશિક", "kn": "ನಾಸಿಕ್", "ml": "നാസിക്" },
    "Maharashtra": { "en": "Maharashtra", "hi": "महाराष्ट्र", "ta": "மகாராஷ்டிரா", "te": "మహారాష్ట్ర", "bn": "মহারাষ্ট্র", "mr": "महाराष्ट्र", "pa": "ਮਹਾਰਾਸ਼ਟਰ", "gu": "મહારાષ્ટ્ર", "kn": "ಮಹಾರಾಷ್ಟ್ರ", "ml": "മഹാരാഷ്ട്ര" },
    "Guntur": { "en": "Guntur", "hi": "गुंटूर", "ta": "குண்டூர்", "te": "గుంటూరు", "bn": "গুন্টুর", "mr": "गुंटूर", "pa": "ਗੁੰਟੂਰ", "gu": "ગુંટુર", "kn": "ಗುಂಟೂರು", "ml": "ഗുണ്ടൂർ" },
    "Andhra Pradesh": { "en": "Andhra Pradesh", "hi": "आंध्र प्रदेश", "ta": "ஆந்திரப் பிரதேசம்", "te": "ఆంధ్రప్రదేశ్", "bn": "অন্ধ্রপ্রদেশ", "mr": "आंध्र प्रदेश", "pa": "ਆਂਧરા ਪ੍ਰਦੇਸ਼", "gu": "આંધ્ર પ્રદેશ", "kn": "ಆಂಧ್ರ ಪ್ರದೇಶ", "ml": "ആന്ധ്രാപ്രദേശ്" },
    "Villupuram": { "en": "Villupuram", "hi": "विल्लुपुरम", "ta": "விழுப்புரம்", "te": "విళ్ళుపురం", "bn": "ভিন্নুপুরম", "mr": "विल्लुपुरम", "pa": "ਵਿਲੁਪੁਰਮ", "gu": "વિલ્લુપુરમ", "kn": "ವಿழுப்புರಂ", "ml": "വിഴുപ്പുറം" },
    "Tamil Nadu": { "en": "Tamil Nadu", "hi": "तमिलनाडु", "ta": "தமிழ்நாடு", "te": "తమిళనాడు", "bn": "তামিলনাড়ু", "mr": "तमिळनाडू", "pa": "ਤਮਿਲਨਾਡੂ", "gu": "તમિલનાડુ", "kn": "ತಮಿಳುನಾಡು", "ml": "തമിഴ്നാട്" },
    "Wheat": { "en": "Wheat", "hi": "गेहूँ", "ta": "கோதுமை", "te": "గోధుమ", "bn": "গম", "mr": "गहू", "pa": "ਕਣਕ", "gu": "ઘઉં", "kn": "ಗೋಧಿ", "ml": "ഗോതമ്പ്" },
    "Rice": { "en": "Rice", "hi": "चावल", "ta": "அரிசி", "te": "వరి", "bn": "চাল", "mr": "तांदूळ", "pa": "ਚੌਲ", "gu": "ચોખા", "kn": "ಅಕ್ಕಿ", "ml": "അരി" },
    "Cotton": { "en": "Cotton", "hi": "कपास", "ta": "பருத்தி", "te": "పత్తి", "bn": "তুলা", "mr": "कापूस", "pa": "ਕਪਾਹ", "gu": "કપાસ", "kn": "ಹತ್ತಿ", "ml": "പരുത്തി" },
    "Groundnut": { "en": "Groundnut", "hi": "मूंगफली", "ta": "நிலக்கடலை", "te": "వేరుశెనగ", "bn": "চিনাবাদাম", "mr": "भुईमूग", "pa": "ਮੂੰਗਫਲੀ", "gu": "મગફળી", "kn": "ಕಡಲೆಕಾಯಿ", "ml": "നിലക്കടല" },
    "Sorghum": { "en": "Sorghum", "hi": "ज्वार", "ta": "சோளம்", "te": "జొన్న", "bn": "জোয়ার", "mr": "ज्वारी", "pa": "ਜਵਾਰ", "gu": "જુવાર", "kn": "ಜೋಳ", "ml": "ചോളം" }
};

window.localizePlace = function(name, language = window.currentLanguage) {
    if(!name) return "";
    return LOCATION_TRANSLATIONS[name]?.[language]
        || LOCATION_TRANSLATIONS[name]?.en
        || name;
};

// Also redefine localizeLocation to handle structured "City, State"
window.localizeLocation = function(locStr) {
    if(!locStr) return "";
    let parts = locStr.split(',').map(s => s.trim());
    if (parts.length === 2) {
         return `${window.localizePlace(parts[0])}, ${window.localizePlace(parts[1])}`;
    }
    return window.localizePlace(locStr);
};
"""

js = js.replace('let lastDxResult = null; // store to know if dx exists', 'let lastDxResult = null; // store to know if dx exists\n' + helpers)


# 3. Strip out `const t = UI_TRANSLATIONS...` everywhere
js = re.sub(r'const t = UI_TRANSLATIONS\[currentLanguage\]\s*\|\|\s*UI_TRANSLATIONS\[\'en\'\];\n?', '', js)
# Also might be written as UI_TRANSLATIONS[window.currentLanguage]
js = re.sub(r'const t = UI_TRANSLATIONS\[window.currentLanguage\]\s*\|\|\s*UI_TRANSLATIONS\[\'en\'\];\n?', '', js)

# 4. Replace `t.key` with `window.t('key')` where applicable. 
# Look for t.sysError, t.apiOnline, t.analyzeBtn, etc.
js = re.sub(r'(?<!window\.)t\.([a-zA-Z0-9_]+)', r"window.t('\1')", js)
# Replace existing `t(` with `window.t(` to force using the global
js = re.sub(r'(?<!window\.)\bt\(', 'window.t(', js)

# 5. Interoperability scenarios need localized location and crop
old_scen = '<div class="sb-title">${esc(s.name)}</div>\\n        <div class="sb-sub">${esc(s.crop)}</div>'
new_scen = '<div class="sb-title">${esc(window.localizeLocation(s.name))}</div>\\n        <div class="sb-sub">${esc(window.localizePlace(s.crop))}</div>'
js = js.replace('<div class="sb-title">${esc(s.name)}</div>', '<div class="sb-title">${esc(window.localizeLocation(s.name))}</div>')
js = js.replace('<div class="sb-sub">${esc(s.crop)}</div>', '<div class="sb-sub">${esc(window.localizePlace(s.crop))}</div>')


# 6. We also need to localize field state name (which shows Sambalpur, Odisha).
# Where does it show Sambalpur? Let's check `static/index.html` or `static/new_script.js`
# wait, you'll find `<h2 id="f-name">...</h2>` in index.html? If we look at updateUI() or renderField(), is there code that updates `f-name` or `f-location-name`?
js = js.replace("${fs.field.crop}", "${window.localizePlace(fs.field.crop)}")

with open('static/new_script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Scope and location patches applied.")
