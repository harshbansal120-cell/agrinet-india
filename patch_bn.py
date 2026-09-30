import json

def patch_bangla():
    with open('static/lang.js', 'r', encoding='utf-8') as f:
        js = f.read()

    bn = {
        "appDesc": "প্রমাণ-ভিত্তিক কৃষি বুদ্ধিমত্তা",
        "navDashboard": "ড্যাশবোর্ড",
        "navField": "ক্ষেত্রের বুদ্ধিমত্তা",
        "navAdvisory": "এআই পরামর্শ",
        "navDoctor": "ফসল ডাক্তার",
        "health_weather": "আবহাওয়া",
        "health_soil": "মাটি",
        "health_eo_confidence": "ইও আত্মবিশ্বাস",
        "evidenceTitle": "প্রমাণ বান্ডিল",
        "evidenceDesc": "কাঠামোগত নির্ণায়ক পর্যবেক্ষণ।",
        "ind_rain_past": "বৃষ্টিপাত (গত ৭ দিন)",
        "ind_rain_next": "বৃষ্টিপাত (আগামী ৭ দিন)",
        "ind_temp": "গড় সর্বোচ্চ তাপমাত্রা (সাম্প্রতিক)",
        "rain_mod_past": "মাঝারি বৃষ্টিপাত (গত ৭ দিন) → পর্যাপ্ত।",
        "rain_very_low_next": "খুব কম বৃষ্টিপাত (আগামী ৭ দিন) → খরা ঝুঁকি।",
        "temp_favorable": "অধিকাংশ ফসলের জন্য অনুকূল তাপমাত্রা।",
        "analyzeBtn": "বিশ্লেষণ করুন",
        "tapMap": "পিন রাখতে মানচিত্রে আলতো চাপুন।",
        "cropInput": "ফসল (যেমন গম)",
        "scenariosTitle": "ইন্টারঅপারেবিলিটি পাইলট পরিস্থিতি",
        "scenariosDesc": "নেটওয়ার্ক মূল্যায়নের জন্য প্রাক-কনফিগার করা ক্ষেত্র।"
    }

    modified = js
    idx = modified.find('"bn": {')
    if idx != -1:
        injection = ""
        for k, v in bn.items():
            injection += f'    "{k}": "{v}",\n'
        modified = modified[:idx + len('"bn": {') + 1] + injection + modified[idx + len('"bn": {') + 1:]

    with open('static/lang.js', 'w', encoding='utf-8') as f:
        f.write(modified)
    print("lang.js patched for Bangla (bn)")

if __name__ == '__main__':
    patch_bangla()
