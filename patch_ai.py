ADVISORY_SCHEMA_V2 = """Return ONLY valid JSON matching this exact schema:
{
  "summary": "str (2-3 sentences, plain language overview of field condition)",
  "field_status": {
    "status": "str (good|monitor|critical)",
    "explanation": "str"
  },
  "what_the_data_shows": [
    {
      "observation": "str (what we see)",
      "evidence_id": "str (MUST be from supplied list)",
      "importance": "str"
    }
  ],
  "priority_risks": [
    {
      "risk": "str",
      "severity": "low|medium|high",
      "evidence": "str",
      "evidence_ids": ["str"],
      "why_it_matters": "str"
    }
  ],
  "immediate_actions": [
    {
      "action": "str",
      "timing": "str",
      "reason": "str",
      "priority": "now|this_week|monitor"
    }
  ],
  "soil_management": [
    {
      "action": "str",
      "reason": "str",
      "timing": "str"
    }
  ],
  "water_management": [
    {
      "action": "str",
      "reason": "str",
      "timing": "str"
    }
  ],
  "weather_response": [
    {
      "condition": "str",
      "action": "str",
      "timing": "str"
    }
  ],
  "crop_management": [
    {
      "action": "str",
      "reason": "str"
    }
  ],
  "regenerative_actions": [
    {
      "practice": "str",
      "how_to_apply": "str",
      "benefit": "str",
      "timing": "str"
    }
  ],
  "crop_options": [
    {
      "crop": "str",
      "suitability": "high|moderate|conditional",
      "reason": "str",
      "conditions": "str"
    }
  ],
  "monitoring_plan": [
    {
      "indicator": "str",
      "what_to_watch": "str",
      "when_to_check": "str",
      "action_if_condition_occurs": "str"
    }
  ],
  "why_this_advice": [
    {
      "recommendation": "str",
      "evidence_ids": ["str"],
      "reasoning": "str"
    }
  ],
  "when_to_seek_expert_help": "str",
  "confidence_note": "str"
}

If any section has no relevant evidence, return an empty list [] for it. Do NOT fabricate missing measurements.
"""

def extract_evidence_ids(evidence):
    return [e.get("id") for e in evidence if e.get("id")]

def validate_evidence(json_obj, valid_ids):
    if isinstance(json_obj, dict):
        # We need to filter any list of strings that is associated with evidence_ids
        for k in list(json_obj.keys()):
            if k == "evidence_ids":
                # Filter invalid IDs out
                valid_list = [eid for eid in json_obj[k] if eid in valid_ids]
                json_obj[k] = valid_list
            elif k == "evidence_id":
                if json_obj[k] not in valid_ids:
                    json_obj[k] = ""
            else:
                validate_evidence(json_obj[k], valid_ids)
    elif isinstance(json_obj, list):
        for item in json_obj:
            validate_evidence(item, valid_ids)

import re
with open('app/ai.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Replace the schema string
schema_start = code.find('ADVISORY_SCHEMA_V2 = """Return ONLY valid JSON matching this exact schema:')
schema_end = code.find('"""\n\ndef advisory(ctx:', schema_start) + 3

if schema_start != -1 and schema_end != 2:
    code = code[:schema_start] + ADVISORY_SCHEMA_V2 + code[schema_end:]

# Now replace advisory_v2 logic
v2_start = code.find('def advisory_v2(field_state_compact:')
if v2_start != -1:
    v2_end = code.find('def diagnose(', v2_start)
    if v2_end != -1:
        # We need to find the `# ──────────────────────────────────────────────` before it
        v2_end = code.rfind('#', v2_start, v2_end)
        
        replacement = '''def advisory_v2(field_state_compact: dict, evidence: list, lang: str):
    """Enhanced advisory: structured evidence-grounded reasoning.

    Args:
        field_state_compact: compact field state from field_state.field_state_for_gemini()
        evidence: list of evidence items
        lang: language code
    """
    L = LANGS.get(lang, "English")
    evidence_text = json.dumps(evidence, ensure_ascii=False, default=str)
    field_text = json.dumps(field_state_compact, ensure_ascii=False, default=str)
    valid_evidence_ids_str = ", ".join([e.get("id", "") for e in evidence if "id" in e])

    prompt = f"""You are an agronomy advisor for small and marginal farmers in India.

TASK: Analyze the FIELD STATE and EVIDENCE BUNDLE below. Produce a structured advisory.

RULES:
1. Use ONLY the data provided. Do NOT invent measurements or statistics.
2. Reference evidence IDs from the bundle when explaining risks and recommendations.
3. Use only evidence IDs from the supplied evidence list [{valid_evidence_ids_str}]. Never invent, modify, or fabricate an evidence ID.
4. If data is missing or uncertain, acknowledge it. Do NOT fabricate missing measurements.
5. Recommend regenerative, low-cost, locally practical options.
6. If the land is not cropland, say so and advise accordingly.
7. Write all text values in {L} (simple words, no jargon).
8. Keep all JSON keys in English.
9. The Field Health Score is deterministic (computed by the system). You may explain it but do NOT recalculate it.
10. Each recommendation must have a clear WHY linked to specific evidence.
11. Give specific timing: now, next 24-48 hours, next 3-7 days, monitor over the coming weeks. Only use timing when justified by the supplied evidence.
12. Never create fake precision (do not invent fertilizer quantities, irrigation quantities, yield predictions).

FIELD STATE:
{field_text}

EVIDENCE BUNDLE:
{evidence_text}

{ADVISORY_SCHEMA_V2}"""

    r = _generate(contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0.3))
    
    parsed = _safe_parse(r)
    
    # Enforce evidence safety validation in Python post-processing
    valid_ids = set([e.get("id") for e in evidence if "id" in e])
    
    def validate_ids(obj):
        if isinstance(obj, dict):
            for k in list(obj.keys()):
                if k == "evidence_ids" and isinstance(obj[k], list):
                    obj[k] = [eid for eid in obj[k] if eid in valid_ids]
                elif k == "evidence_id" and isinstance(obj[k], str):
                    if obj[k] not in valid_ids:
                        obj[k] = ""
                else:
                    validate_ids(obj[k])
        elif isinstance(obj, list):
            for item in obj:
                validate_ids(item)

    validate_ids(parsed)
    return parsed

'''
        code = code[:v2_start] + replacement + code[v2_end:]

with open('app/ai.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Updated ai.py successfully.")
