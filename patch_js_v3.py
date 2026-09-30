with open('static/new_script.js', 'r', encoding='utf-8') as f:
    js_code = f.read()

# 1. ADD t() helper
t_helper = """
function t(key, args) {
   let str = (UI_TRANSLATIONS[currentLanguage] || UI_TRANSLATIONS['en'])[key] || UI_TRANSLATIONS['en'][key] || key;
   if (args) {
      for (const [k, v] of Object.entries(args)) {
         str = str.replace(`{${k}}`, v);
      }
   }
   return str;
}
"""
js_code = js_code.replace("function updateUI() {", t_helper + "\nfunction updateUI() {")

# 2. Modify renderField
render_field_old = """
  const v = provenance.satellite_badge;
  $('f-badge-mode').className = `badge ${v==='LIVE'?'badge-live':v==='MODEL'?'badge-model':v==='DEMO'?'badge-demo':'badge-err'}`;
  
  if (provenance.data_status === 'DEMO' && provenance.scenario_date) {
    $('f-badge-mode').textContent = `${t.demoBadge || 'DEMO'} SCENARIO · Historical snapshot · ${provenance.scenario_date}`;
  } else {
    // Basic translation for string matches
    if(v==='DEMO') $('f-badge-mode').textContent = t.demoBadge || 'DEMO';
    else $('f-badge-mode').textContent = v;
  }
  
  $('f-geohash').textContent = `${t.geohash} ${fs.field.geohash}`;
  $('f-location').textContent = `${fs.field.lat.toFixed(4)}, ${fs.field.lon.toFixed(4)}`;
  $('f-crop').textContent = fs.field.crop ? `${t.declaredCrop} ${esc(fs.field.crop)}` : t.unknownCrop;

  const h = fs.health;
  const ring = $('f-health-ring');
  if(h.score !== null) {
    ring.dataset.status = h.status;
    $('f-health-score').textContent = h.score;
    // Do not translate health status fully, or if you do, map it.
    $('f-health-status').textContent = h.status.toUpperCase();
    $('f-health-status').style.color = ring.dataset.status === 'healthy' ? 'var(--health-good)' : ring.dataset.status === 'watch' ? 'var(--health-watch)' : 'var(--health-poor)';
    
    $('f-health-comps').innerHTML = Object.entries(h.components).map(([k,v]) => `
      <div class="data-point">
        <span class="dp-label" style="text-transform:capitalize">${k}</span>
        <span class="dp-val">${v ?? '--'}</span>
      </div>
    `).join('');
  } else {
    $('f-health-score').textContent = '--';
    $('f-health-status').textContent = 'UNAVAILABLE';
    $('f-health-comps').innerHTML = '';
  }

  $('f-evidence-list').innerHTML = evidence.map(e => {
    const bClass = e.badge==='LIVE'?'badge-live':e.badge==='MODEL'?'badge-model':e.badge==='DEMO'?'badge-demo':'badge-pre';
    let localBadge = e.badge;
    if (e.badge === 'DEMO') localBadge = t.demoBadge || 'DEMO';
    return `
    <div style="padding: 12px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; margin-bottom: 8px;">
      <div style="display:flex; justify-content:space-between; margin-bottom: 4px;">
        <code style="font-size:11px; color:var(--text-muted);">${e.id}</code>
        <span class="badge ${bClass}">${localBadge}</span>
      </div>
      <div style="font-weight:600; font-size:14px;">${esc(e.indicator)}: ${esc(e.value)} ${esc(e.unit)}</div>
      <div style="font-size:13px; color:var(--text-muted); margin-top:2px;">${esc(e.interpretation)}</div>
      <div style="font-size:11px; color:var(--text-light); margin-top:4px;">${t.source} ${esc(e.source)}</div>
    </div>
  `}).join('');
"""

render_field_new = """
  const v = provenance.satellite_badge;
  let bClass = v==='LIVE'?'badge-live':v==='MODEL'?'badge-model':v==='DEMO'?'badge-demo':'badge-err';
  $('f-badge-mode').className = `badge ${bClass}`;
  
  if (provenance.data_status === 'DEMO' && provenance.scenario_date) {
    $('f-badge-mode').textContent = `${t('demoBadge')} · Historical snapshot · ${provenance.scenario_date}`;
  } else {
    $('f-badge-mode').textContent = String(v).toLowerCase() === 'precomputed' ? t('precomputedBadge') : t(String(v).toLowerCase() + 'Badge');
  }
  
  $('f-geohash').textContent = `${t('geohash')} ${fs.field.geohash}`;
  $('f-location').textContent = `${fs.field.lat.toFixed(4)}, ${fs.field.lon.toFixed(4)}`;
  $('f-crop').textContent = fs.field.crop ? `${t('declaredCrop')} ${esc(fs.field.crop)}` : t('unknownCrop');

  const h = fs.health;
  const ring = $('f-health-ring');
  if(h.score !== null) {
    ring.dataset.status = h.status;
    $('f-health-score').textContent = h.score;
    $('f-health-status').textContent = t('status_' + h.status) || h.status.toUpperCase();
    $('f-health-status').style.color = ring.dataset.status === 'healthy' ? 'var(--health-good)' : ring.dataset.status === 'watch' ? 'var(--health-watch)' : 'var(--health-poor)';
    
    $('f-health-comps').innerHTML = Object.entries(h.components).map(([k,val]) => `
      <div class="data-point">
        <span class="dp-label" style="text-transform:capitalize">${t('health_' + k) || k}</span>
        <span class="dp-val">${val ?? '--'}</span>
      </div>
    `).join('');
  } else {
    $('f-health-score').textContent = '--';
    $('f-health-status').textContent = t('status_unknown') || 'UNAVAILABLE';
    $('f-health-comps').innerHTML = '';
  }

  $('f-evidence-list').innerHTML = evidence.map(e => {
    const ebadge = e.badge || 'UNAVAILABLE';
    const bClass = ebadge==='LIVE'?'badge-live':ebadge==='MODEL'?'badge-model':ebadge==='DEMO'?'badge-demo':'badge-pre';
    let localBadge = String(ebadge).toLowerCase() === 'precomputed' ? t('precomputedBadge') : t(String(ebadge).toLowerCase() + 'Badge');
    
    let localIndicator = t(e.indicator_key) || e.indicator;
    let localInterpretation = e.interpretation_key ? t(e.interpretation_key, {val: String(e.value)}) : e.interpretation;
    
    return `
    <div style="padding: 12px; background: var(--bg); border: 1px solid var(--border); border-radius: 6px; margin-bottom: 8px;">
      <div style="display:flex; justify-content:space-between; margin-bottom: 4px;">
        <code style="font-size:11px; color:var(--text-muted);">${e.id}</code>
        <span class="badge ${bClass}">${localBadge}</span>
      </div>
      <div style="font-weight:600; font-size:14px;">${esc(localIndicator)}: ${esc(e.value)} ${esc(e.unit)}</div>
      <div style="font-size:13px; color:var(--text-muted); margin-top:2px;">${esc(localInterpretation)}</div>
      <div style="font-size:11px; color:var(--text-light); margin-top:4px;">${t('source')} ${esc(e.source)}</div>
    </div>
  `}).join('');
"""

if render_field_old in js_code:
    js_code = js_code.replace(render_field_old, render_field_new)
else:
    print("Warning: render_field_old block not found perfectly.")

# 3. Modify renderAdvisory
render_advisory_old_start = "function renderAdvisory(a) {"
render_advisory_old_end = "  $('adv-note').textContent = a.confidence_note || '';\n}"

# We will cut out the slice
idx1 = js_code.find(render_advisory_old_start)
idx2 = js_code.find(render_advisory_old_end) + len(render_advisory_old_end)

render_advisory_new = """function renderAdvisory(a) {
  $('adv-content').style.display = 'block';
  $('btn-speak').disabled = false;
  
  const buildSec = (titleKey, contentHtml, isCollapsible=false) => {
      if(!contentHtml) return '';
      const title = esc(t(titleKey));
      if(isCollapsible) {
         return `<details style="margin-bottom:12px; padding:12px; background:#f9fafb; border: 1px solid var(--border); border-radius:6px; cursor:pointer;">
           <summary style="font-weight:600; color:var(--primary); font-size:14px;">${title}</summary>
           <div style="margin-top:12px; font-size:14px;">${contentHtml}</div>
         </details>`;
      }
      return `<div style="margin-bottom:24px;">
         <h3 class="card-title" style="margin-bottom:12px; font-size:16px;">${title}</h3>
         ${contentHtml}
      </div>`;
  };

  const safeMap = (arr, fn) => {
      if(!arr || !arr.length) return `<p class="dp-label">${t('adv_no_data')}</p>`;
      return arr.map(fn).join('');
  };

  const evidMap = (arr) => arr?.length ? `<div style="margin-top:6px;">${arr.map(id => `<span class="evidence-tag" style="font-size:11px; margin-right:4px;">${id}</span>`).join('')}</div>` : '';

  let html = '';
  
  // Field Status
  html += buildSec('sec_field_status', `
     <p style="font-weight:600; margin-bottom:4px; font-size: 16px;">${esc(a.field_status?.status || '')}</p>
     <p>${esc(a.field_status?.explanation || '')}</p>
  `, false);
  
  // What Data Shows
  html += buildSec('sec_what_data_shows', safeMap(a.what_the_data_shows, r => `
    <div style="padding:12px; border-bottom:1px solid #eee;">
      <div style="font-weight:500;">${esc(r.observation)}</div>
      <div style="font-size:13px; color:#666; margin-top:2px;">${esc(r.importance)}</div>
      ${r.evidence_id ? evidMap([r.evidence_id]) : ''}
    </div>
  `));
  
  // Risks
  html += buildSec('sec_priority_risks', safeMap(a.priority_risks, r => `
    <div style="padding:12px; background:#fef2f2; border:1px solid #fecaca; border-radius:6px; margin-bottom:8px;">
      <div style="font-weight:600; color:#991b1b; font-size:14px;">${esc(r.risk)} <span class="badge badge-err" style="float:right">${esc(r.severity)}</span></div>
      <p style="margin-top:4px;">${esc(r.why_it_matters)}</p>
      ${evidMap(r.evidence_ids)}
    </div>
  `));
  
  // Immediate Actions
  html += buildSec('sec_immediate_actions', safeMap(a.immediate_actions, r => `
    <div style="padding:12px; background:var(--bg); border:1px solid var(--border); border-radius:6px; margin-bottom:8px; border-left: 4px solid var(--primary);">
       <div style="font-weight:600; font-size:14px;">${esc(r.action)} <span class="badge badge-live" style="float:right">${esc(r.timing)}</span></div>
       <p style="margin-top:8px;">${esc(r.reason)}</p>
    </div>
  `));
  
  // Weather Responses
  html += buildSec('sec_weather_response', safeMap(a.weather_response, r => `
    <div style="margin-bottom:8px; border-bottom:1px solid #eee; padding-bottom:8px;">
       <div style="font-weight:600;">${esc(r.condition)}</div>
       <div>${esc(r.action)} <span style="font-size:12px; color:#666;">(${esc(r.timing)})</span></div>
    </div>
  `), true);
  
  // Soil Management
  html += buildSec('sec_soil_management', safeMap(a.soil_management, r => `
    <div style="margin-bottom:8px; border-bottom:1px solid #eee; padding-bottom:8px;">
       <div style="font-weight:600;">${esc(r.action)}</div>
       <div>${esc(r.reason)} <span style="font-size:12px; color:#666;">(${esc(r.timing)})</span></div>
    </div>
  `), true);
  
  // Crop Management
  html += buildSec('sec_crop_management', safeMap(a.crop_management, r => `
    <div style="margin-bottom:8px; border-bottom:1px solid #eee; padding-bottom:8px;">
       <div style="font-weight:600;">${esc(r.action)}</div>
       <div>${esc(r.reason)}</div>
    </div>
  `), true);

  // Regen Actions
  html += buildSec('sec_regen_actions', safeMap(a.regenerative_actions, r => `
    <div style="margin-bottom:8px; padding-bottom:8px; border-bottom:1px solid #eee;">
       <div style="font-weight:600;">🌱 ${esc(r.practice)}</div>
       <p style="font-size: 13px; margin-top:2px;">${esc(r.how_to_apply)}</p>
       <div style="font-size:12px; color:#666; margin-top:2px;">Benefit: ${esc(r.benefit)} | Timing: ${esc(r.timing)}</div>
    </div>
  `), true);

  // Crop Options
  html += buildSec('sec_crop_options', safeMap(a.crop_options, r => `
    <div style="margin-bottom:8px; border-bottom:1px solid #eee; padding-bottom:8px;">
       <div style="font-weight:600;">${esc(r.crop)} <span class="badge ${r.suitability==='high'?'badge-live':'badge-model'}">${esc(r.suitability)}</span></div>
       <div style="margin-top:2px; font-size:13px;">${esc(r.reason)}</div>
       <div style="font-size:12px; color:#666; margin-top:2px;">Conditions: ${esc(r.conditions)}</div>
    </div>
  `), true);
  
  // Monitoring Plan
  html += buildSec('sec_monitoring_plan', safeMap(a.monitoring_plan, r => `
    <div style="margin-bottom:8px; padding-bottom:8px;">
       <div><strong style="color:var(--text-main)">${esc(r.indicator)}</strong>: ${esc(r.what_to_watch)}</div>
       <div style="font-size:12px; color:#666; margin-top:2px;">Check: ${esc(r.when_to_check)}</div>
       <div style="font-size:13px; color:#991b1b; margin-top:2px;">If occurs: ${esc(r.action_if_condition_occurs)}</div>
    </div>
  `), true);
  
  // Why this advice matches
  html += buildSec('sec_why_advice', safeMap(a.why_this_advice, r => `
    <div style="margin-bottom:8px; padding:12px; background:#f0f9ff; border:1px solid #bae6fd; border-radius:6px;">
       <div style="font-weight:500;">${esc(r.recommendation)}</div>
       <p style="margin-top:4px; font-size:13px;">${esc(r.reasoning)}</p>
       ${evidMap(r.evidence_ids)}
    </div>
  `), true);

  const container = $('adv-content');
  container.innerHTML = `<div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom: 24px;">
        <h2 class="card-title" style="font-size: 22px; color: var(--primary);">${esc(t('localizedAdvisory'))}</h2>
        <button class="btn btn-secondary" id="btn-speak">🔊 ${esc(t('listen'))}</button>
      </div>`;
  
  container.innerHTML += `<p style="font-size:16px; margin-bottom: 24px;">${esc(a.summary || '')}</p>`;
  
  const dynBox = document.createElement('div');
  dynBox.innerHTML = html;
  
  // Meta block
  const meta = document.createElement('div');
  meta.style.marginTop = '24px';
  meta.style.padding = '12px';
  meta.style.background = '#f3f4f6';
  meta.style.borderRadius = 'var(--radius-sm)';
  meta.style.fontSize = '13px';
  meta.innerHTML = `<strong style="color:#b45309;"><span data-i18n="sec_when_expert">${esc(t('sec_when_expert'))}</span>:</strong> <span>${esc(a.when_to_seek_expert_help || '')}</span><br>
  <strong style="color:var(--text-main); margin-top:8px; display:inline-block;"><span data-i18n="sec_confidence">${esc(t('sec_confidence'))}</span>:</strong> <span>${esc(a.confidence_note || '')}</span>`;
  
  dynBox.appendChild(meta);
  container.appendChild(dynBox);

  // Restore Voice feature handler bind since we rewrote innerHTML
  $('btn-speak').onclick = () => {
    if(!currentAdvisory) return;
    speechSynthesis.cancel();
    const actionsText = (a.immediate_actions||[]).map(c=>`${c.action}.`).join(' ');
    const txt = `${a.summary || ''} ${actionsText}`;
    const u = new SpeechSynthesisUtterance(txt);
    u.lang = VOICE[currentLanguage] || 'en-IN';
    speechSynthesis.speak(u);
  };
}"""

if idx1 != -1 and idx2 != -1:
    js_code = js_code[:idx1] + render_advisory_new + js_code[idx2:]
else:
    print("Warning: render_advisory_old block not found")

with open('static/new_script.js', 'w', encoding='utf-8') as f:
    f.write(js_code)
    
print("Updated static/new_script.js")
