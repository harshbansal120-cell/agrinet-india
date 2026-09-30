import json

def patch_marathi():
    with open('static/lang.js', 'r', encoding='utf-8') as f:
        js = f.read()

    mr = {
        "appDesc": "पुरावा-आधारित कृषी बुद्धिमत्ता",
        "navDashboard": "डॅशबोर्ड",
        "navField": "क्षेत्र बुद्धिमत्ता",
        "navAdvisory": "AI सल्ला",
        "navDoctor": "पीक डॉक्टर",
        "health_weather": "हवामान",
        "health_soil": "माती",
        "health_eo_confidence": "EO आत्मविश्वास",
        "evidenceTitle": "पुरावा बंडल",
        "evidenceDesc": "संरचित निश्चित निरीक्षणे.",
        "ind_rain_past": "पाऊस (गेले ७ दिवस)",
        "ind_rain_next": "पाऊस (पुढील ७ दिवस)",
        "ind_temp": "सरासरी कमाल तापमान (अलीकडील)",
        "rain_mod_past": "मध्यम पाऊस (गेले ७ दिवस) → पुरेसा.",
        "rain_very_low_next": "अतिशय कमी पाऊस (पुढील ७ दिवस) → दुष्काळाचा धोका.",
        "temp_favorable": "बहुतेक पिकांसाठी अनुकूल तापमान.",
        "analyzeBtn": "विश्लेषण करा",
        "tapMap": "पिन ठेवण्यासाठी नकाशावर टॅप करा.",
        "cropInput": "पीक (उदा. गहू)",
        "scenariosTitle": "इंटरऑपरेबिलिटी पायलट",
        "scenariosDesc": "राज्य नेटवर्क मूल्यांकनासाठी डेमो फील्ड.",
        "fieldEmpty": "पुरावे पाहण्यासाठी डॅशबोर्डवर एक क्षेत्र निवडा.",
        "declaredCrop": "नोंदवलेले पीक:",
        "unknownCrop": "अज्ञात पीक",
        "advEmpty": "क्षेत्रामधून तुमचा सल्ला तयार करा."
    }

    modified = js
    idx = modified.find('"mr": {')
    if idx != -1:
        injection = ""
        for k, v in mr.items():
            injection += f'    "{k}": "{v}",\n'
        modified = modified[:idx + len('"mr": {') + 1] + injection + modified[idx + len('"mr": {') + 1:]

    with open('static/lang.js', 'w', encoding='utf-8') as f:
        f.write(modified)
    print("lang.js patched for Marathi (mr)")

if __name__ == '__main__':
    patch_marathi()
