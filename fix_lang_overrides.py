import json

def fix_lang():
    mr = {
        "health_weather": "हवामान",
        "health_soil": "माती",
        "health_eo_confidence": "EO आत्मविश्वास",
        "evidenceTitle": "पुरावा बंडल",
        "evidenceDesc": "संरचित निश्चित निरीक्षणे.",
        
        "ind_rain_past": "पाऊस (गेले ७ दिवस)",
        "ind_rain_next": "पाऊस (पुढील ७ दिवस)",
        "ind_temp": "सरासरी कमाल तापमान (अलीकडील)",
        "ind_ph": "मातीचा सामू (pH)",
        "ind_soc": "सेंद्रिय कर्ब",
        "ind_ndvi": "वनस्पती (NDVI)",
        "ind_ndwi": "नमी (NDWI)",

        "rain_very_heavy_past": "अतिवृष्टी (गेले ७ दिवस) → पुराचा धोका.",
        "rain_heavy_past": "मुसळधार पाऊस (गेले ७ दिवस) → पाणी साचण्याचा धोका.",
        "rain_mod_past": "मध्यम पाऊस (गेले ७ दिवस) → पुरेसा.",
        "rain_low_past": "कमी पाऊस (गेले ७ दिवस) → ओलाव्यावर लक्ष ठेवा.",
        "rain_very_low_past": "अतिशय कमी पाऊस (गेले ७ दिवस) → दुष्काळाचा धोका.",
        "rain_no_data_past": "पावसाची माहिती उपलब्ध नाही.",
        
        "rain_very_heavy_next": "अतिवृष्टी (पुढील ७ दिवस) → पुराचा धोका.",
        "rain_heavy_next": "मुसळधार पाऊस (पुढील ७ दिवस) → पाणी साचण्याचा धोका.",
        "rain_mod_next": "मध्यम पाऊस (पुढील ७ दिवस) → पुरेसा.",
        "rain_low_next": "कमी पाऊस (पुढील ७ दिवस) → ओलाव्यावर लक्ष ठेवा.",
        "rain_very_low_next": "अतिशय कमी पाऊस (पुढील ७ दिवस) → दुष्काळाचा धोका.",
        "rain_no_data_next": "पावसाचा अंदाज उपलब्ध नाही.",
        
        "temp_extreme": "अत्यंत उष्णता → पिकांवर गंभीर ताण येण्याची शक्यता.",
        "temp_high": "उच्च तापमान → उष्णतेचा ताण शक्य.",
        "temp_warm": "उबदार परिस्थिती → उष्णता-संवेदनशील पिकांचे निरीक्षण करा.",
        "temp_favorable": "बहुतेक पिकांसाठी अनुकूल तापमान श्रेणी.",
        "temp_cool": "थंड परिस्थिती → रब्बी पिकांसाठी अनुकूल.",
        "temp_cold": "अति थंडी → दंव पडण्याचा धोका.",
        "temp_no_data": "तापमान माहिती उपलब्ध नाही."
    }

    bn = {
        "health_weather": "আবহাওয়া",
        "health_soil": "মাটি",
        "health_eo_confidence": "ইও আত্মবিশ্বাস",
        "evidenceTitle": "প্রমাণ বান্ডিল",
        "evidenceDesc": "কাঠামোগত নির্ণায়ক পর্যবেক্ষণ।",

        "ind_rain_past": "বৃষ্টিপাত (গত ৭ দিন)",
        "ind_rain_next": "বৃষ্টিপাত (আগামী ৭ দিন)",
        "ind_temp": "গড় সর্বোচ্চ তাপমাত্রা (সাম্প্রতিক)",
        "ind_ph": "মাটির পিএইচ (pH)",
        "ind_soc": "জৈব কার্বন",
        "ind_ndvi": "উদ্ভিদ (NDVI)",
        "ind_ndwi": "আর্দ্রতা (NDWI)",

        "rain_very_heavy_past": "অতি ভারী বৃষ্টিপাত (গত ৭ দিন) → বন্যার ঝুঁকি।",
        "rain_heavy_past": "ভারী বৃষ্টিপাত (গত ৭ দিন) → জল জমে যাওয়ার ঝুঁকি।",
        "rain_mod_past": "মাঝারি বৃষ্টিপাত (গত ৭ দিন) → পর্যাপ্ত।",
        "rain_low_past": "কম বৃষ্টিপাত (গত ৭ দিন) → আর্দ্রতা পর্যবেক্ষণ করুন।",
        "rain_very_low_past": "খুব কম বৃষ্টিপাত (গত ৭ দিন) → খরা ঝুঁকি।",
        "rain_no_data_past": "বৃষ্টিপাতের তথ্য উপলব্ধ নেই।",
        
        "rain_very_heavy_next": "অতি ভারী বৃষ্টিপাত (আগামী ৭ দিন) → বন্যার ঝুঁকি।",
        "rain_heavy_next": "ভারী বৃষ্টিপাত (আগামী ৭ দিন) → জল জমে যাওয়ার ঝুঁকি।",
        "rain_mod_next": "মাঝারি বৃষ্টিপাত (আগামী ৭ দিন) → পর্যাপ্ত।",
        "rain_low_next": "কম বৃষ্টিপাত (আগামী ৭ দিন) → আর্দ্রতা পর্যবেক্ষণ করুন।",
        "rain_very_low_next": "খুব কম বৃষ্টিপাত (আগামী ৭ দিন) → খরা ঝুঁকি।",
        "rain_no_data_next": "বৃষ্টিপাতের পূর্বাভাস উপলব্ধ নেই।",

        "temp_extreme": "চরম তাপ → ফসলের ব্যাপক চাপের সম্ভাবনা।",
        "temp_high": "উচ্চ তাপমাত্রা → তাপের চাপ সম্ভব।",
        "temp_warm": "উষ্ণ পরিস্থিতি → তাপ-সংবেদনশীল ফসল পর্যবেক্ষণ করুন।",
        "temp_favorable": "অধিকাংশ ফসলের জন্য অনুকূল তাপমাত্রা।",
        "temp_cool": "ঠান্ডা পরিস্থিতি → রবি ফসলের জন্য উপযুক্ত।",
        "temp_cold": "শীতল পরিস্থিতি → তুষারপাতের ঝুঁকি।",
        "temp_no_data": "তাপমাত্রার তথ্য উপলব্ধ নেই।"
    }

    te = {
        "health_weather": "వాతావరణం",
        "health_soil": "నేల",
        "health_eo_confidence": "ఈఓ విశ్వాసం",
        "evidenceTitle": "ఆధారాల కట్ట",
        "evidenceDesc": "నిర్మాణాత్మక ముందస్తు పరిశీలనలు.",

        "ind_rain_past": "వర్షపాతం (గత 7 రోజులు)",
        "ind_rain_next": "వర్షపాతం (రాబోయే 7 రోజులు)",
        "ind_temp": "సగటు గరిష్ట ఉష్ణోగ్రత (ఇటీవలి)",
        "ind_ph": "నేల pH",
        "ind_soc": "సేంద్రీయ కార్బన్",
        "ind_ndvi": "వృక్షసంపద (NDVI)",
        "ind_ndwi": "తేమ (NDWI)",

        "rain_very_heavy_past": "అతి భారీ వర్షపాతం (గత 7 రోజులు) → వరద ముప్పు.",
        "rain_heavy_past": "భారీ వర్షపాతం (గత 7 రోజులు) → నీరు నిలిచిపోయే ముప్పు.",
        "rain_mod_past": "మోస్తరు వర్షం (గత 7 రోజులు) → తగినంత.",
        "rain_low_past": "తక్కువ వర్షపాతం (గత 7 రోజులు) → తేమను గమనించండి.",
        "rain_very_low_past": "చాలా తక్కువ వర్షం (గత 7 రోజులు) → కరువు ప్రమాదం.",
        "rain_no_data_past": "వర్షపాతం డేటా అందుబాటులో లేదు.",
        
        "rain_very_heavy_next": "అతి భారీ వర్షపాతం (రాబోయే 7 రోజులు) → వరద ముప్పు.",
        "rain_heavy_next": "భారీ వర్షపాతం (రాబోయే 7 రోజులు) → నీరు నిలిచిపోయే ముప్పు.",
        "rain_mod_next": "మోస్తరు వర్షం (రాబోయే 7 రోజులు) → తగినంత.",
        "rain_low_next": "తక్కువ వర్షపాతం (రాబోయే 7 రోజులు) → తేమను గమనించండి.",
        "rain_very_low_next": "చాలా తక్కువ వర్షం (రాబోయే 7 రోజులు) → కరువు ప్రమాదం.",
        "rain_no_data_next": "వర్షపాతం అంచనా అందుబాటులో లేదు.",

        "temp_extreme": "తీవ్ర వేడి → పంటలకు తీవ్రమైన ఒత్తిడి ఉండే అవకాశం.",
        "temp_high": "అధిక ఉష్ణోగ్రతలు → వేడి ఒత్తిడి అవకాశం.",
        "temp_warm": "వెచ్చని పరిస్థితులు → వేడి సున్నితమైన పంటలను గమనించండి.",
        "temp_favorable": "చాలా పంటలకు అనుకూలమైన ఉష్ణోగ్రత.",
        "temp_cool": "చల్లని పరిస్థితులు → రబీ పంటలకు అనుకూలం.",
        "temp_cold": "చలి పరిస్థితులు → మంచు ముప్పు.",
        "temp_no_data": "ఉష్ణోగ్రత డేటా అందుబాటులో లేదు."
    }

    override_script = f"""
// INJECTED OVERRIDES
Object.assign(UI_TRANSLATIONS.mr || {{}}, {json.dumps(mr, ensure_ascii=False)});
Object.assign(UI_TRANSLATIONS.bn || {{}}, {json.dumps(bn, ensure_ascii=False)});
Object.assign(UI_TRANSLATIONS.te || {{}}, {json.dumps(te, ensure_ascii=False)});
"""

    with open('static/lang.js', 'r', encoding='utf-8') as f:
        js = f.read()
    
    js = js + "\n" + override_script

    with open('static/lang.js', 'w', encoding='utf-8') as f:
        f.write(js)
        
    print("lang.js Object.assign overrides applied successfully.")

if __name__ == '__main__':
    fix_lang()
