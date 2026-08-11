# Kind Designs — Biodiversity Monitoring Concept Demo

Speculative pitch demo for Kind Designs (3D-printed Living Seawalls™, Miami).
Not commissioned, not affiliated — built to show the idea ahead of an intro
from Masa Crowe.

Two distinct pieces:
1. **Real**: a YOLO fish detector (`leodorf/fishvision-detector`) running on
   public South Florida reef footage. Proves the pipeline works — not a claim
   that it's their wall.
2. **Illustrative**: a Folium map + per-site dashboard using real Kind Designs
   site names/locations (Pine Tree Dr, North Bay Road, Venetian Island, Palm
   Island, Star Island, Sunset Islands, Bayfront Park, Bryan Place) with
   placeholder species/diversity numbers. Shows what the dashboard becomes
   once real GoPro footage is available. Labeled as illustrative everywhere
   it appears.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Regenerate the detection video

Needs the model weights (not committed — see `.gitignore`):

```bash
# models/best_v1.08.pt — copy from ARC-CV-App/models/ or pull from the
# leodorf/fishvision-detector HF repo (gated, needs HF_TOKEN)
python render_detection.py
```

## Deploy

Push to GitHub, then share.streamlit.io → New app → point to `app.py`.
`kinddesigns_boxes_web.mp4` (~26MB) is committed directly since it's under
GitHub's 100MB limit — no external hosting needed.

## Status

Demo built, not yet sent. Waiting on:
- Masa's contact intro
- Outreach email draft (short, name-drop Masa, reference the FIU/Harborne
  monitoring program by name, link this demo, ask for a 20-min call)
