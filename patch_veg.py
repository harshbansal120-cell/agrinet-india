import json

def patch_vegetation_status():
    extra_dict = {
        "hi": {
            "health_vegetation": "वनस्पति",
            "status_healthy": "स्वस्थ",
            "status_watch": "ध्यान दें",
            "status_poor": "ख़राब",
            "status_unknown": "अज्ञात"
        },
        "ta": {
            "health_vegetation": "தாவரங்கள்",
            "status_healthy": "ஆரோக்கியமான",
            "status_watch": "கவனிக்கவும்",
            "status_poor": "மோசமான",
            "status_unknown": "தெரியவில்லை"
        },
        "mr": {
            "health_vegetation": "वनस्पती",
            "status_healthy": "निरोगी",
            "status_watch": "लक्ष ठेवा",
            "status_poor": "खराब",
            "status_unknown": "अज्ञात"
        },
        "bn": {
            "health_vegetation": "উদ্ভিদ",
            "status_healthy": "সুস্থ",
            "status_watch": "নজর রাখুন",
            "status_poor": "খারাপ",
            "status_unknown": "অজানা"
        },
        "te": {
            "health_vegetation": "వృక్షసంపద",
            "status_healthy": "ఆరోగ్యంగా",
            "status_watch": "గమనించండి",
            "status_poor": "బలహీన",
            "status_unknown": "తెలియదు"
        },
        "pa": {
            "health_vegetation": "ਬਨਸਪਤੀ",
            "status_healthy": "ਸਿਹਤਮੰਦ",
            "status_watch": "ਨਿਗਰਾਨੀ ਰੱਖੋ",
            "status_poor": "ਖਰਾਬ",
            "status_unknown": "ਅਣਜਾਣ"
        },
        "gu": {
            "health_vegetation": "વનસ્પતિ",
            "status_healthy": "સ્વસ્થ",
            "status_watch": "ધ્યાન રાખો",
            "status_poor": "નબળું",
            "status_unknown": "અજાણ્યું"
        },
        "kn": {
            "health_vegetation": "ಸಸ್ಯವರ್ಗ",
            "status_healthy": "ಆರೋಗ್ಯಕರ",
            "status_watch": "ಗಮನಿಸಿ",
            "status_poor": "ಕಳಪೆ",
            "status_unknown": "ತಿಳಿದಿಲ್ಲ"
        },
        "ml": {
            "health_vegetation": "സസ്യജാലങ്ങൾ",
            "status_healthy": "ആരോഗ്യമുള്ള",
            "status_watch": "നിരീക്ഷിക്കുക",
            "status_poor": "മോശം",
            "status_unknown": "അജ്ഞാതം"
        }
    }

    override_script = "\n// TERTIARY OVERRIDES: Vegetation & Status\n"
    for lang, translations in extra_dict.items():
        override_script += f"Object.assign(UI_TRANSLATIONS.{lang} || {{}}, {json.dumps(translations, ensure_ascii=False)});\n"

    with open('static/lang.js', 'r', encoding='utf-8') as f:
        js = f.read()
    
    js = js + override_script

    with open('static/lang.js', 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("lang.js vegetation and status overrides applied successfully.")

if __name__ == '__main__':
    patch_vegetation_status()
