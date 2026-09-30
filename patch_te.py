import json

def patch_telugu():
    with open('static/lang.js', 'r', encoding='utf-8') as f:
        js = f.read()

    te = {
        "appDesc": "ఆధార-కృతంగా వ్యవసాయ మేధస్సు పొర",
        "navDashboard": "డాష్‌బోర్డ్",
        "navField": "క్షేత్ర పరిశీలన",
        "navAdvisory": "AI సలహా",
        "navDoctor": "పంట డాక్టర్",
        "cropInput": "పంట (ఉదా. గోధుమ)",
        "analyzeBtn": "విశ్లేషించండి",
        "tapMap": "మ్యాప్‌ను నొక్కి పిన్ ఉంచండి.",
        "scenariosTitle": "ఇంటర్‌ఆపెరబిలిటీ పైలట్",
        "scenariosDesc": "రాష్ట్ర నెట్‌వర్క్ మూల్యాంకనం కోసం ప్రదర్శన క్షేత్రాలు.",
        "fieldEmpty": "ఆధారాలు చూడటానికి డాష్‌బోర్డ్‌లో క్షేత్రాన్ని ఎంచుకోండి.",
        "declaredCrop": "పంట గుర్తింపు:",
        "unknownCrop": "తెలియని పంట",
        "advEmpty": "క్షేత్రం నుండి మీ సలహాను సృష్టించండి."
    }

    modified = js
    idx = modified.find('"te": {')
    if idx != -1:
        injection = ""
        for k, v in te.items():
            injection += f'    "{k}": "{v}",\n'
        modified = modified[:idx + len('"te": {') + 1] + injection + modified[idx + len('"te": {') + 1:]

    with open('static/lang.js', 'w', encoding='utf-8') as f:
        f.write(modified)
    print("lang.js patched for Telugu (te)")

if __name__ == '__main__':
    patch_telugu()
