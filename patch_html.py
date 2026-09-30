import re

def main():
    with open('static/index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Inject lang.js
    if '<script src="/static/lang.js"></script>' not in html:
        html = html.replace('</head>', '  <script src="/static/lang.js"></script>\n</head>')

    # 1. HTML Replacements (adding data-i18n tags where needed, or just finding the exact text)
    replacements = {
        '<p>Evidence-grounded agricultural intelligence layer</p>': '<p data-i18n="appDesc">Evidence-grounded agricultural intelligence layer</p>',
        '<button class="nav-btn active" data-target="view-dashboard">Dashboard</button>': '<button class="nav-btn active" data-target="view-dashboard" data-i18n="navDashboard">Dashboard</button>',
        '<button class="nav-btn" data-target="view-field">Field Intelligence</button>': '<button class="nav-btn" data-target="view-field" data-i18n="navField">Field Intelligence</button>',
        '<button class="nav-btn" data-target="view-advisory">AI Advisory</button>': '<button class="nav-btn" data-target="view-advisory" data-i18n="navAdvisory">AI Advisory</button>',
        '<button class="nav-btn" data-target="view-doctor">Crop Doctor</button>': '<button class="nav-btn" data-target="view-doctor" data-i18n="navDoctor">Crop Doctor</button>',
        '<button class="nav-btn" data-target="view-network">Network / API</button>': '<button class="nav-btn" data-target="view-network" data-i18n="navNetwork">Network / API</button>',
        
        'Connecting to AgriNet...': '<span data-i18n="connecting">Connecting to AgriNet...</span>',
        '<h2 class="card-title">Select a Field</h2>': '<h2 class="card-title" data-i18n="selectField">Select a Field</h2>',
        '<p class="card-subtitle">Pin a location or run a deterministic demo scenario.</p>': '<p class="card-subtitle" data-i18n="pinDesc">Pin a location or run a deterministic demo scenario.</p>',
        'placeholder="Crop (optional, e.g. Wheat)"': 'placeholder="Crop (optional, e.g. Wheat)" data-i18n-placeholder="cropInput"',
        '<button class="btn" id="btn-analyze">Analyze Pinned Field</button>': '<button class="btn" id="btn-analyze" data-i18n="analyzeBtn">Analyze Pinned Field</button>',
        '<p id="pin-coords" style="font-size: 13px; color: var(--text-muted); margin-top: 8px;">Tap map to place pin.</p>': '<p id="pin-coords" style="font-size: 13px; color: var(--text-muted); margin-top: 8px;" data-i18n="tapMap">Tap map to place pin.</p>',
        
        '<h2 class="card-title">Interoperability Pilot Scenarios</h2>': '<h2 class="card-title" data-i18n="scenariosTitle">Interoperability Pilot Scenarios</h2>',
        '<p class="card-subtitle">Pre-configured demonstrator fields for state network evaluation.</p>': '<p class="card-subtitle" data-i18n="scenariosDesc">Pre-configured demonstrator fields for state network evaluation.</p>',
        '<p class="dp-label">Loading scenarios...</p>': '<p class="dp-label" data-i18n="loadingScenarios">Loading scenarios...</p>',
        
        'Select a field on the Dashboard to view intelligence.': '<span data-i18n="fieldEmpty">Select a field on the Dashboard to view intelligence.</span>',
        '<button class="btn" id="btn-gen-adv">Generate AI Advisory</button>': '<button class="btn" id="btn-gen-adv" data-i18n="genAdvisoryBtn">Generate AI Advisory</button>',
        '<h3 class="card-title" style="text-align: center;">Deterministic Field Health</h3>': '<h3 class="card-title" style="text-align: center;" data-i18n="healthTitle">Deterministic Field Health</h3>',
        '<h3 class="card-title">Evidence Bundle</h3>': '<h3 class="card-title" data-i18n="evidenceTitle">Evidence Bundle</h3>',
        '<p class="card-subtitle">Structured deterministic observations.</p>': '<p class="card-subtitle" data-i18n="evidenceDesc">Structured deterministic observations.</p>',
        
        'Generate an advisory from the Field Intelligence tab.': '<span data-i18n="advEmpty">Generate an advisory from the Field Intelligence tab.</span>',
        '<h3 style="font-family:var(--font-display);">Gemini Reasoning Engine</h3>': '<h3 style="font-family:var(--font-display);" data-i18n="advLoadingTitle">Gemini Reasoning Engine</h3>',
        '<p style="color:var(--text-muted); margin-top:8px;">Synthesizing structured evidence into localized action...</p>': '<p style="color:var(--text-muted); margin-top:8px;" data-i18n="advLoadingDesc">Synthesizing structured evidence into localized action...</p>',
        
        '<h2 class="card-title" style="font-size: 22px; color: var(--primary);">Localized Advisory</h2>': '<h2 class="card-title" style="font-size: 22px; color: var(--primary);" data-i18n="localizedAdvisory">Localized Advisory</h2>',
        '<button class="btn btn-secondary" id="btn-speak">🔊 Listen</button>': '<button class="btn btn-secondary" id="btn-speak" data-i18n="listen">🔊 Listen</button>',
        '<h3 class="card-title" style="margin-bottom: 16px;">Priority Actions</h3>': '<h3 class="card-title" style="margin-bottom: 16px;" data-i18n="priorityActions">Priority Actions</h3>',
        '<h3 class="card-title" style="margin: 24px 0 16px; color:#9a3412;">Known Risks</h3>': '<h3 class="card-title" style="margin: 24px 0 16px; color:#9a3412;" data-i18n="knownRisks">Known Risks</h3>',
        '<h3 class="card-title" style="margin-bottom: 16px; color:var(--primary);">Regenerative Practices</h3>': '<h3 class="card-title" style="margin-bottom: 16px; color:var(--primary);" data-i18n="regenPractices">Regenerative Practices</h3>',
        '<h3 class="card-title" style="font-size: 16px;">Climate-Resilient Crop Options</h3>': '<h3 class="card-title" style="font-size: 16px;" data-i18n="cropOptions">Climate-Resilient Crop Options</h3>',
        '<strong style="color:var(--text-main);">AI Confidence Note:</strong>': '<strong style="color:var(--text-main);" data-i18n="aiConfidence">AI Confidence Note:</strong>',
        
        '<h2 class="card-title">Multimodal Assessment</h2>': '<h2 class="card-title" data-i18n="dxTitle">Multimodal Assessment</h2>',
        '<p class="card-subtitle">Upload a crop image for Gemini analysis.</p>': '<p class="card-subtitle" data-i18n="dxDesc">Upload a crop image for Gemini analysis.</p>',
        '<p style="font-weight: 500;">Click or drop image here</p>': '<p style="font-weight: 500;" data-i18n="dropImage">Click or drop image here</p>',
        'placeholder="Crop (optional)"': 'placeholder="Crop (optional)" data-i18n-placeholder="dxCropInput"',
        '<button class="btn" id="btn-dx" style="width:100%;">Run AI Diagnosis</button>': '<button class="btn" id="btn-dx" style="width:100%;" data-i18n="runDxBtn">Run AI Diagnosis</button>',
        '<h2 class="card-title">Assessment Results</h2>': '<h2 class="card-title" data-i18n="dxResTitle">Assessment Results</h2>',
        'Awaiting image upload.': '<span data-i18n="dxEmpty">Awaiting image upload.</span>',
        '<p style="margin-top:12px;">Analyzing image...</p>': '<p style="margin-top:12px;" data-i18n="dxLoading">Analyzing image...</p>',
        '<span class="dp-label">Symptoms</span>': '<span class="dp-label" data-i18n="symptoms">Symptoms</span>',
        '<span class="dp-label">Action</span>': '<span class="dp-label" data-i18n="action">Action</span>',
        '<strong style="color:#b45309;">Expert Escalation:</strong>': '<strong style="color:#b45309;" data-i18n="expertEscalation">Expert Escalation:</strong>',
        
        '<h2 class="card-title">AgriNet Interoperability Pilot</h2>': '<h2 class="card-title" data-i18n="netTitle">AgriNet Interoperability Pilot</h2>',
        '<p class="card-subtitle">One intelligence schema. Configurable state adapters.</p>': '<p class="card-subtitle" data-i18n="netDesc">One intelligence schema. Configurable state adapters.</p>',
        '<h2 class="card-title">DPG API Contract (v1)</h2>': '<h2 class="card-title" data-i18n="apiTitle">DPG API Contract (v1)</h2>',
        '<p class="card-subtitle">Exposed endpoints for state-level integration.</p>': '<p class="card-subtitle" data-i18n="apiDesc">Exposed endpoints for state-level integration.</p>'
    }

    for Old, New in replacements.items():
        html = html.replace(Old, New)

    with open('static/index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
main()
