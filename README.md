# AgriNet India — interoperable agro-advisory network (prototype)

Satellite + soil + weather + crop-disease AI, delivered in 10 Indian languages, exposed as an open geohash-keyed API so any state can plug in data and models.

## Flow
Pin a field → **land routing** → soil (SoilGrids) + weather (Open-Meteo) → **Gemini** regenerative advisory in the farmer's language → optional **Gemini vision** crop-disease diagnosis → voice read-out.

**Land routing:** if a stored PlanetScope pixel lies within `PLANET_RADIUS_M` (300 m) → stored Dynamic World label for that cell as the reference answer, plus a second opinion from our SPEAR PlanetScope MAE encoder + land-cover head, with confidence and agreement flag (source = `planet_highres`); otherwise → Google Earth Engine Dynamic World + Sentinel-2 NDVI (source = `earth_engine_live`). The UI always shows which path answered.

## Google AI / Cloud used
Gemini (advisory, multimodal disease diagnosis, multilingual output) · Earth Engine · Cloud Run · (optional) Vertex AI, BigQuery, Firebase.

## What was built before vs. during the hackathon (Rule 02)
Before: SPEAR PlanetScope MAE pretraining (github.com/udaiveersingh/SPEAR, MIT — WACV 2026 CV4EO Workshop), the labelled parquet data. During: everything in this repo (API, routing, classifier head, Gemini integration, UI, deployment).

## Run locally
```
pip install -r requirements.txt
python scripts/prep_lookup.py /path/to/PlanetScope      # -> data/lookup.parquet
python scripts/train_embed_classifier.py /path/to/PlanetScope # -> data/classifier_emb.joblib (SPEAR embedding head)
python scripts/verify_encoder.py /path/to/PlanetScope        # checks the torch-free encoder port
cp .env.example .env  # set GEMINI_API_KEY; run `earthengine authenticate` for EE
uvicorn app.main:app --reload
```
Deploy: `PROJECT=<gcp-project> GEMINI_API_KEY=<key> ./deploy.sh`

## TODO before submission
1. Enable Earth Engine for your GCP project; test the fallback path.
2. Set `GEMINI_API_KEY`; test advisory + diagnosis.

## Known limits (be upfront with judges)
Planet data is 2023-24 and sparse; the pixel-level head reaches only ~45% accuracy / 0.39 macro-F1 on the imbalanced test set and SPEAR embeddings did not beat raw bands on this single-date data, so it is shown as a second opinion with confidence, not as the answer; advisories are AI-generated and should be checked by local extension officers.
