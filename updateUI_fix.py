import re

with open('static/new_script.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix updateUI data-i18n parsing
bad_updateui = """function updateUI() {
    
  // Update all data-i18n simple tags
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    if (t[key]) {
      // Retain HTML for complex elements if necessary, but we only replaced simple text nodes
      if (el.children.length === 0) {
         el.textContent = t[key];
      } else {
         // for tags that contain children, we only want to set inner text if safe, currently we kept it clean for span/p
         el.innerHTML = t[key];
      }
    }
  });
  
  // Placeholders
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    if (t[key]) el.placeholder = t[key];
  });"""

good_updateui = """let currentScenarios = null;

function renderScenarios() {
  if (!currentScenarios) return;
  $('scenario-list').innerHTML = currentScenarios.scenarios.map(s => `
      <div class="scenario-btn" onclick="runScenario('${s.key}', ${s.lat}, ${s.lon})">
        <span class="badge badge-demo" style="margin-bottom:8px">${window.t('demoBadge') || 'DEMO'}</span>
        <div class="sb-title">${esc(window.localizeLocation(s.name))}</div>
        <div class="sb-sub">${esc(window.localizePlace(s.crop))}</div>
      </div>
    `).join('');
}

function updateUI() {
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    let translated = window.t(key);
    if (translated !== key) {
      if (el.children.length === 0) {
         el.textContent = translated;
      } else {
         el.innerHTML = translated;
      }
    }
  });
  
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    let translated = window.t(key);
    if (translated !== key) el.placeholder = translated;
  });

  renderScenarios();
"""

if bad_updateui in js:
    js = js.replace(bad_updateui, good_updateui)
else:
    print("Warning: could not find bad_updateui")

# Replace init
bad_init = """    const scen = await apiGet('/api/scenarios');
    $('scenario-list').innerHTML = scen.scenarios.map(s => `
      <div class="scenario-btn" onclick="runScenario('${s.key}', ${s.lat}, ${s.lon})">
        <span class="badge badge-demo" style="margin-bottom:8px">${window.t('demoBadge') || 'DEMO'}</span>
        <div class="sb-title">${esc(window.localizeLocation(s.name))}</div>
        <div class="sb-sub">${esc(window.localizePlace(s.crop))}</div>
      </div>
    `).join('');"""

good_init = """    currentScenarios = await apiGet('/api/scenarios');
    renderScenarios();"""

if bad_init in js:
    js = js.replace(bad_init, good_init)
else:
    print("Warning: could not find bad_init")
    
with open('static/new_script.js', 'w', encoding='utf-8') as f:
    f.write(js)

print("Updated script.")
