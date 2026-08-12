"""
Kind Designs pitch demo — biodiversity monitoring dashboard concept.

Two distinct pieces, deliberately not blurred together:
  1. Detection video: REAL YOLO inference (leodorf/fishvision-detector) on
     public South Florida reef footage. Not their wall — proof the pipeline
     actually detects fish in this kind of environment.
  2. Map + per-site data: ILLUSTRATIVE. Real site names/locations (from
     kinddesigns.com + press), placeholder species/diversity numbers. Shows
     what the dashboard looks like once real GoPro footage feeds it — not
     a claim that this survey has been run.
Every section that shows illustrative data labels it as such.
"""
import sys
from pathlib import Path

BASE = Path(__file__).parent
sys.path.insert(0, str(BASE))

import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

from sites import SITES

st.set_page_config(page_title="Kind Designs × Biodiversity Monitoring — Concept Demo",
                    layout="wide", initial_sidebar_state="collapsed")

ACCENT = "#2dd4bf"

CSS = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
html, body, .stApp, [data-testid="stAppViewContainer"] {{
    background: #07161a !important;
    color: #cbd5e1;
    font-family: 'Inter', sans-serif;
}}
[data-testid="stHeader"], [data-testid="stToolbar"] {{ display: none !important; }}
section[data-testid="stSidebar"] {{ display: none; }}
.block-container {{ padding: 2rem 2.5rem 4rem !important; max-width: 1180px !important; }}

.badge {{ display:inline-block;background:{ACCENT}1f;color:{ACCENT};font-size:0.68rem;
    font-weight:700;letter-spacing:.12em;text-transform:uppercase;padding:5px 14px;
    border-radius:999px;border:1px solid #1e6f66;margin-bottom:16px; }}
.illustrative-badge {{ display:inline-block;background:rgba(245,158,11,0.12);color:#f59e0b;
    font-size:0.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
    padding:4px 12px;border-radius:999px;border:1px solid rgba(245,158,11,0.35);margin-bottom:14px; }}
.real-badge {{ display:inline-block;background:rgba(34,197,94,0.12);color:#22c55e;
    font-size:0.62rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;
    padding:4px 12px;border-radius:999px;border:1px solid rgba(34,197,94,0.35);margin-bottom:14px; }}

.sec {{ font-size: 0.65rem; text-transform: uppercase; letter-spacing: .18em;
       color: #2a6058; font-weight: 700; margin: 40px 0 6px; }}
.sec-sub {{ font-size: 0.82rem; color: #6b8f89; margin-bottom: 18px; line-height: 1.6; }}

.vid-card {{ border-radius: 12px; overflow: hidden; border: 1px solid #123a34;
            box-shadow: 0 8px 32px rgba(0,0,0,0.35); }}

.glass-card {{ background: #0d1f1c; border: 1px solid #123a34; border-radius: 12px;
              padding: 18px 20px; margin-bottom: 14px; position: relative; }}
.glass-card .title {{ color: {ACCENT}; font-size: 0.85rem; font-weight: 700; margin-bottom: 6px;
                      padding-right: 78px; }}
.glass-card .body {{ color: #6b8f89; font-size: 0.78rem; line-height: 1.75; }}
.card-tag {{ position: absolute; top: 18px; right: 20px; font-size: 0.58rem; font-weight: 800;
            letter-spacing: .08em; padding: 3px 9px; border-radius: 999px; text-transform: uppercase; }}
.card-tag.live {{ background: rgba(34,197,94,0.12); color: #22c55e; border: 1px solid rgba(34,197,94,0.35); }}
.card-tag.roadmap {{ background: rgba(148,163,184,0.10); color: #6b8f89; border: 1px solid rgba(100,139,132,0.35); }}

.site-table td, .site-table th {{ font-size: 0.8rem; }}

.cta-card {{ background: linear-gradient(135deg, {ACCENT}1a, rgba(13,31,28,0.4));
            border: 1px solid {ACCENT}4d; border-radius: 14px;
            padding: 2rem; text-align: center; margin-top: 8px; }}
.cta-card .h {{ color: #f1f5f9; font-size: 1.1rem; font-weight: 800; margin-bottom: 8px; }}
.cta-card .b {{ color: #6b8f89; font-size: 0.82rem; line-height: 1.7; margin-bottom: 4px; }}
.cta-card .e {{ color: {ACCENT}; font-size: 0.9rem; font-weight: 700; margin-top: 10px; }}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding:36px 36px 32px;background:linear-gradient(160deg,#0e2b26,#0a1e1a 65%);
            border:1px solid #1e6f66;border-radius:18px;margin-bottom:16px">
  <div class="badge">\U0001F41F Concept Demo · Not Affiliated With Kind Designs</div>
  <div style="font-size:2.1rem;font-weight:800;color:#f8fafc;letter-spacing:-0.04em;line-height:1.15;max-width:720px">
    What your GoPro monitoring program could look like running through automated detection
  </div>
  <div style="font-size:0.95rem;color:#9dc4bd;margin-top:14px;line-height:1.6;max-width:680px">
    A rough sketch of a biodiversity dashboard for the Living Seawall™ program — built to show
    the idea, not to present real results. One piece of this is real (the detection video below);
    everything else is a mockup of what it could become with real footage from your walls.
  </div>
</div>
""", unsafe_allow_html=True)

# ── Real detection video ────────────────────────────────────────────────────
st.markdown("<div class='sec'>The Real Part</div>", unsafe_allow_html=True)
st.markdown('<span class="real-badge">✓ Real inference, real footage</span>', unsafe_allow_html=True)
st.markdown("""
<div class="sec-sub">
This is a live YOLO species detector (6 species, trained + tracked) running on public
South Florida reef footage — <b>not</b> footage from an actual Living Seawall™. It's here
to show the pipeline genuinely identifies and tracks fish against rocky, colonized
structure, the same kind of scene a GoPro on your wall would see.
</div>
""", unsafe_allow_html=True)

col_v, col_stat = st.columns([2, 1], gap="medium")
with col_v:
    st.markdown("<div class='vid-card'>", unsafe_allow_html=True)
    st.video(str(BASE / "kinddesigns_boxes_web.mp4"), loop=True, autoplay=True, muted=True)
    st.markdown("</div>", unsafe_allow_html=True)
with col_stat:
    st.markdown(f"""
    <div class="glass-card" style="height:100%">
      <div class="title">\U0001F3AF What's live here</div>
      <div class="body">
        Real-time <b>species-level</b> detection with tracking — Sergeant Major, White Grunt,
        French Grunt, Porkfish, Bluehead Wrasse, Parrotfish — plus per-frame count.<br><br>
        Model: custom YOLO26 detector trained on hand-labeled frames from this clip,
        with ByteTrack so detections persist across frames instead of flickering.<br><br>
        <b>Honest caveat:</b> trained on ~120 frames from one clip, not a general-purpose
        classifier yet. Sergeant Major and White Grunt (the two most common species here)
        are reliable; Porkfish and Parrotfish had very few training examples and will miss
        or misfire more often. More labeled footage fixes that.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Illustrative map ─────────────────────────────────────────────────────────
st.markdown("<div class='sec'>Product Vision — Per-Site Dashboard</div>", unsafe_allow_html=True)
st.markdown('<span class="illustrative-badge">⚠ Illustrative data, not a real survey</span>', unsafe_allow_html=True)
st.markdown("""
<div class="sec-sub">
Site names and general locations below are real (pulled from kinddesigns.com and
press coverage). Species lists, counts, and diversity numbers are placeholder
values — nobody has run this analysis on your actual GoPro footage yet. This is
what the dashboard would populate with once that footage is available.
</div>
""", unsafe_allow_html=True)

m = folium.Map(
    location=[25.87, -80.155], zoom_start=11,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri World Imagery",
)
all_lats = [s["lat"] for s in SITES]
all_lons = [s["lon"] for s in SITES]
m.fit_bounds([[min(all_lats) - 0.02, min(all_lons) - 0.02],
              [max(all_lats) + 0.02, max(all_lons) + 0.02]])

for s in SITES:
    popup_html = f"""
    <div style="font-family:Inter,sans-serif;min-width:220px;padding:4px">
      <div style="font-size:14px;font-weight:700;color:#0e7490;margin-bottom:4px">{s['name']}</div>
      <div style="font-size:11px;color:#aaa;margin-bottom:8px">{s['area']} · Installed {s['installed']}</div>
      <div style="font-size:12px;margin-bottom:2px"><b>Diversity index:</b> {s['diversity_index']}</div>
      <div style="font-size:12px;margin-bottom:2px"><b>Avg fish/session:</b> {s['fish_count_avg']}</div>
      <div style="font-size:12px;margin-bottom:2px"><b>Species:</b> {', '.join(s['species'])}</div>
      <div style="font-size:12px;margin-bottom:6px"><b>Inverts:</b> {', '.join(s['invertebrates'])}</div>
      <div style="font-size:10px;color:#f59e0b">⚠ Illustrative data</div>
    </div>
    """
    folium.CircleMarker(
        location=[s["lat"], s["lon"]],
        radius=10 + s["diversity_index"] * 12,
        color="#ffffff", weight=2,
        fill=True, fill_color=ACCENT, fill_opacity=0.75,
        popup=folium.Popup(popup_html, max_width=290),
        tooltip=f"{s['name']} — diversity {s['diversity_index']}",
    ).add_to(m)
st_folium(m, width=1130, height=460, returned_objects=[])

df = pd.DataFrame(SITES)
col_a, col_b = st.columns(2, gap="medium")
with col_a:
    fig1 = px.bar(df.sort_values("diversity_index", ascending=True),
                   x="diversity_index", y="name", orientation="h",
                   color="diversity_index", color_continuous_scale=["#123a34", ACCENT],
                   labels={"diversity_index": "Diversity Index", "name": ""},
                   title="Biodiversity Index by Site (illustrative)")
    fig1.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
                        margin=dict(l=10, r=10, t=40, b=10), height=340)
    st.plotly_chart(fig1, use_container_width=True)
with col_b:
    fig2 = px.scatter(df, x="months_monitored", y="diversity_index", size="fish_count_avg",
                       color="diversity_index", color_continuous_scale=["#123a34", ACCENT],
                       hover_name="name",
                       labels={"months_monitored": "Months Monitored", "diversity_index": "Diversity Index"},
                       title="Colonization Over Time (illustrative)")
    fig2.update_layout(template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)",
                        paper_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
                        margin=dict(l=10, r=10, t=40, b=10), height=340)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<div class='sec'>Per-Site Detail</div>", unsafe_allow_html=True)
display_df = df[["name", "area", "installed", "months_monitored", "diversity_index", "fish_count_avg"]].rename(
    columns={"name": "Site", "area": "Area", "installed": "Installed", "months_monitored": "Months Monitored",
             "diversity_index": "Diversity Index", "fish_count_avg": "Avg Fish/Session"})
st.dataframe(display_df, use_container_width=True, hide_index=True)

# ── Capability cards ─────────────────────────────────────────────────────────
st.markdown("<div class='sec'>Pipeline Capabilities</div>", unsafe_allow_html=True)
cards = [
    ("\U0001F41F", "Fish detection & tracking", "live",
     "Runs on real footage right now — the video above. Per-frame counts, confidence scores, "
     "ByteTrack so individual fish are tracked across frames instead of re-detected from scratch."),
    ("\U0001F3F7️", "Species-level classification", "live",
     "6 species trained from ~120 hand-labeled frames of this clip: Sergeant Major, White Grunt, "
     "French Grunt, Porkfish, Bluehead Wrasse, Parrotfish. The two dominant species are reliable; "
     "the thin-data ones need more labeled footage to firm up — same process, just more frames."),
    ("\U0001F5FA️", "Cross-site GIS dashboard", "roadmap",
     "Aggregate biodiversity view across every wall — shown above as a mockup. Once real "
     "per-site data exists, this becomes live and could be shown to city planners and property "
     "owners as evidence the walls are working ecologically."),
    ("\U0001F9F1", "Structural defect / crack detection", "roadmap",
     "Phase 2 idea: flag cracks or degradation in the 3D-printed tiles from the same GoPro "
     "footage. Harder build — needs labeled crack data — but a strong second pitch."),
    ("\U0001F41A", "Benthic cover classification", "roadmap",
     "Could accelerate or replace manual Coral Point Count analysis — automatic classification "
     "of coral, algae, and invertebrate cover from the same footage."),
]
col_a, col_b = st.columns(2, gap="medium")
cols = [col_a, col_b]
for i, (icon, title, tag, body) in enumerate(cards):
    with cols[i % 2]:
        tag_label = "Live In This Demo" if tag == "live" else "Roadmap"
        st.markdown(
            f"<div class='glass-card'><span class='card-tag {tag}'>{tag_label}</span>"
            f"<div class='title'>{icon} &nbsp;{title}</div>"
            f"<div class='body'>{body}</div></div>",
            unsafe_allow_html=True,
        )

# ── CTA ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="cta-card">
  <div class="h">Want to see this running on real Living Seawall™ footage?</div>
  <div class="b">This whole thing took a weekend to sketch out with public footage.
  Give me a clip from your GoPro monitoring program and I'll show you what it looks
  like with your actual data — no cost to find out.</div>
  <div class="e">leodorfman1@gmail.com</div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#123a34;font-size:0.72rem;
            margin-top:40px;padding-top:20px;border-top:1px solid #0d1f1c">
  Concept demo built by Leo Dorfman — not affiliated with or endorsed by Kind Designs
</div>
""", unsafe_allow_html=True)
