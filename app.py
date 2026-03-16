import streamlit as st
import os
import urllib.parse
import json
import itertools
from PIL import Image
from dotenv import load_dotenv
from google import genai

# --- 1. CONFIG & SETUP ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="dripCHECK | Style Intelligence",
    page_icon="👕",
    layout="centered"
)

# Initialize Session State for the Closet & Combos
if "closet" not in st.session_state:
    st.session_state.closet = []
if "combos" not in st.session_state:
    st.session_state.combos = []

# --- UNIFIED BRAND STYLESHEET ---
# Google Fonts (separate call so Streamlit does not render CSS as text)
st.markdown("""
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fredoka:wght@400;500;700&family=MuseoModerno:wght@700;800&family=Public+Sans:wght@400;600;700;800&family=Space+Grotesk:wght@400;600;700;800&display=swap" rel="stylesheet">
""", unsafe_allow_html=True)

st.markdown("""
<style>
/* ============================================================
   dripCHECK — Unified Stylesheet (Streamlit Overrides)
   Brand: Teal (#008080) on Warm Sand (#F4E1C1)
   ============================================================ */

/* --- Design Tokens --- */
:root {
  --clr-teal:        #008080;
  --clr-teal-dark:   #2D4F4F;
  --clr-teal-light:  rgba(0, 128, 128, 0.12);
  --clr-sand:        #F4E1C1;
  --clr-sand-light:  #fdfbf7;
  --clr-dark:        #1A1A1A;
  --clr-warm-gray:   #78716C;
  --clr-white:       #ffffff;

  --font-body:    'Public Sans', sans-serif;
  --font-display: 'Space Grotesk', sans-serif;
  --font-splash:  'MuseoModerno', sans-serif;
  --font-tag:     'Fredoka', sans-serif;

  --radius-sm:   0.5rem;
  --radius-md:   1rem;
  --radius-lg:   1.5rem;
  --radius-xl:   2rem;
  --radius-full: 9999px;

  --shadow-sm:    0 1px 3px rgba(0,0,0,0.08);
  --shadow-md:    0 4px 16px rgba(0,128,128,0.10);
  --shadow-lg:    0 8px 32px rgba(0,128,128,0.15);
  --shadow-glow:  0 0 40px rgba(0,128,128,0.18);

  --transition-fast:   150ms ease;
  --transition-base:   250ms ease;
}

/* --- Streamlit Global Overrides --- */
.stApp, [data-testid="stAppViewContainer"] {
    background-color: var(--clr-sand) !important;
    font-family: var(--font-body) !important;
    color: var(--clr-dark) !important;
}
header[data-testid="stHeader"] {
    background: rgba(244, 225, 193, 0.82) !important;
    backdrop-filter: blur(14px) !important;
    -webkit-backdrop-filter: blur(14px) !important;
    border-bottom: 1px solid rgba(0,0,0,0.05) !important;
}
[data-testid="stSidebar"] {
    background: var(--clr-sand-light) !important;
    border-right: 1px solid rgba(0,128,128,0.08) !important;
    font-family: var(--font-body) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--clr-teal-dark) !important;
    font-family: var(--font-display) !important;
}

/* --- Buttons --- */
.stButton > button {
    width: 100%;
    border-radius: var(--radius-md) !important;
    height: 3.2em;
    background-color: var(--clr-teal) !important;
    color: var(--clr-white) !important;
    font-weight: 700 !important;
    font-family: var(--font-body) !important;
    border: none !important;
    box-shadow: var(--shadow-md) !important;
    transition: opacity var(--transition-fast), box-shadow var(--transition-base), transform var(--transition-fast) !important;
    letter-spacing: 0.02em;
}
.stButton > button:hover {
    opacity: 0.88 !important;
    box-shadow: var(--shadow-glow) !important;
    transform: scale(0.98);
}
.stButton > button:active {
    transform: scale(0.96) !important;
}
.stDownloadButton > button {
    width: 100%;
    border-radius: var(--radius-md) !important;
    background: transparent !important;
    color: var(--clr-teal) !important;
    border: 2px solid var(--clr-teal) !important;
    font-weight: 700 !important;
}
.stDownloadButton > button:hover {
    background: var(--clr-teal) !important;
    color: var(--clr-white) !important;
}
.stLinkButton > a {
    border-radius: var(--radius-md) !important;
    background: transparent !important;
    color: var(--clr-teal) !important;
    border: 2px solid var(--clr-teal) !important;
    font-weight: 700 !important;
    transition: background var(--transition-fast), color var(--transition-fast) !important;
}
.stLinkButton > a:hover {
    background: var(--clr-teal) !important;
    color: var(--clr-white) !important;
}

/* --- File Uploader (Upload Zone) --- */
[data-testid="stFileUploader"] {
    border: 2px dashed rgba(0, 128, 128, 0.3) !important;
    border-radius: var(--radius-lg) !important;
    padding: 1.5rem !important;
    background: rgba(244,225,193,0.15) !important;
    transition: border-color var(--transition-base), background var(--transition-base) !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: var(--clr-teal) !important;
    background: rgba(0,128,128,0.05) !important;
}
[data-testid="stFileUploader"] button {
    background-color: var(--clr-teal) !important;
    color: var(--clr-white) !important;
    border-radius: var(--radius-md) !important;
    font-weight: 700 !important;
}

/* --- Glass Cards (Closet Items) --- */
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255, 255, 255, 0.40) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid rgba(0, 128, 128, 0.12) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: var(--shadow-sm) !important;
    transition: box-shadow var(--transition-base), transform var(--transition-base) !important;
    overflow: hidden;
}
div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: var(--shadow-lg) !important;
    transform: translateY(-3px);
}

/* --- Expanders (The Roast) --- */
div[data-testid="stExpander"] {
    border: 1px solid rgba(0,128,128,0.15) !important;
    border-radius: var(--radius-md) !important;
    background: rgba(244,225,193,0.25) !important;
}
div[data-testid="stExpander"] summary {
    font-weight: 700 !important;
    color: var(--clr-teal-dark) !important;
    font-family: var(--font-body) !important;
}

/* --- Divider --- */
hr {
    border-color: rgba(0,128,128,0.1) !important;
}

/* --- Success / Error / Info alerts --- */
div[data-testid="stAlert"] {
    border-radius: var(--radius-md) !important;
    font-family: var(--font-body) !important;
}

/* --- Custom Brand Elements --- */
.drip-hero-title {
    font-family: 'MuseoModerno', sans-serif;
    font-size: clamp(2.5rem, 7vw, 4.5rem);
    font-weight: 800;
    color: var(--clr-teal);
    letter-spacing: -0.04em;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.drip-hero-sub {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(1rem, 2.5vw, 1.35rem);
    font-weight: 600;
    color: var(--clr-teal-dark);
    letter-spacing: -0.01em;
    margin-bottom: 0.25rem;
}
.drip-hero-tagline {
    font-family: 'Public Sans', sans-serif;
    font-size: 0.85rem;
    color: var(--clr-warm-gray);
    font-weight: 400;
}
.drip-section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--clr-teal-dark);
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.drip-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.25rem;
    padding: 0.2rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.625rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    background: var(--clr-teal);
    color: var(--clr-white);
}
.drip-footer {
    text-align: center;
    padding: 1.5rem 0;
    font-size: 0.8rem;
    color: var(--clr-warm-gray);
    font-family: 'Public Sans', sans-serif;
    border-top: 1px solid rgba(0,128,128,0.08);
    margin-top: 2rem;
}
.drip-footer a {
    color: var(--clr-teal);
    font-weight: 600;
    text-decoration: none;
}
.drip-footer a:hover {
    text-decoration: underline;
}
.drip-empty-closet {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--clr-warm-gray);
    font-family: 'Public Sans', sans-serif;
}
.drip-empty-closet .icon {
    font-size: 3rem;
    margin-bottom: 0.75rem;
    opacity: 0.5;
}
.drip-empty-closet p {
    font-size: 0.95rem;
}

/* --- Reveal Animation --- */
@keyframes slideUp {
  from { opacity: 0; transform: translateY(20px); }
  to   { opacity: 1; transform: translateY(0); }
}
.reveal {
  opacity: 0;
  animation: slideUp 0.6s cubic-bezier(0.16, 1, 0.3, 1) forwards;
}
.reveal-1 { animation-delay: 0.1s; }
.reveal-2 { animation-delay: 0.22s; }
.reveal-3 { animation-delay: 0.34s; }

/* --- Sidebar Brand Accent --- */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #b91c1c !important;
    border: 2px solid #b91c1c !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #b91c1c !important;
    color: var(--clr-white) !important;
}

</style>
""", unsafe_allow_html=True)

# --- 2. HELPER FUNCTIONS ---
def get_pinterest_link(tags):
    """Turns Gemini tags into a Pinterest search URL"""
    base_url = "https://www.pinterest.com/search/pins/?q="
    clean_query = urllib.parse.quote(f"{tags} outfit ideas")
    return base_url + clean_query

def clear_closet():
    """Wipes the session state closet and combos"""
    st.session_state.closet = []
    st.session_state.combos = []

# --- 3. UI SIDEBAR ---
with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png")
    else:
        st.markdown("""
        <div style="padding: 0.5rem 0;">
            <span style="font-family: 'MuseoModerno', sans-serif; font-weight: 800; font-size: 1.8rem; letter-spacing: -0.04em; font-style: italic; color: #2D4F4F;">
                drip<span style="color: #008080;">CHECK</span>
            </span>
            <span class="drip-badge" style="margin-left: 0.5rem; vertical-align: middle;">AI</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.markdown("### ⚙️ Closet Management")
    if st.button("🗑️ Clear My Closet", on_click=clear_closet):
        st.toast("Closet wiped clean!")

    st.divider()
    st.caption("AIML Student Project · Hackophobia 2026")

# --- 4. MAIN UI & UPLOADER (Multi-File) ---
st.markdown("""
<div class="reveal">
    <p class="drip-hero-title">👕 dripCHECK</p>
    <p class="drip-hero-sub">Turn your laundry pile into <em style="color:#008080;">Certified Drip.</em></p>
    <p class="drip-hero-tagline">Upload up to 6 clothing items · Get AI analysis for each · Generate outfit combinations</p>
</div>
""", unsafe_allow_html=True)

st.write("")  # spacer

uploaded_files = st.file_uploader(
    "Upload your clothing items (up to 6)...",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

if uploaded_files:
    # Cap at 6
    if len(uploaded_files) > 6:
        st.warning("⚠️ Maximum 6 items allowed. Only the first 6 will be processed.")
        uploaded_files = uploaded_files[:6]

    # Show thumbnails of selected files
    st.markdown(f"**{len(uploaded_files)} item(s) selected:**")
    preview_cols = st.columns(min(len(uploaded_files), 6))
    images = []
    for i, uf in enumerate(uploaded_files):
        img = Image.open(uf)
        images.append(img)
        with preview_cols[i]:
            st.image(img, caption=uf.name[:15], use_container_width=True)

    if st.button("🔍 Analyze All & Add to Closet"):
        if not api_key:
            st.error("Missing Gemini API Key! Check your .env file.")
        else:
            progress_bar = st.progress(0, text="Starting analysis...")
            client = genai.Client(api_key=api_key)
            success_count = 0

            for i, img in enumerate(images):
                progress_bar.progress(
                    (i) / len(images),
                    text=f"🤖 Analyzing item {i + 1} of {len(images)}..."
                )
                try:
                    prompt = """
                    Analyze the clothing in the image. Return ONLY a JSON object with these keys:
                    {
                        "item": "specific name of clothing",
                        "color": "dominant color",
                        "style": "fashion aesthetic",
                        "tags": "3-word search keywords",
                        "roast": "a lighthearted snarky comment about this item",
                        "score": "style rating 1-10"
                    }
                    Do not include markdown formatting or extra text.
                    """

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[prompt, img]
                    )

                    raw_text = response.text.strip().replace("```json", "").replace("```", "")
                    data = json.loads(raw_text)

                    st.session_state.closet.append({
                        "image": img,
                        "details": data
                    })
                    success_count += 1

                except Exception as e:
                    st.error(f"Failed on item {i + 1}: {e}")

            progress_bar.progress(1.0, text="✅ Analysis complete!")
            if success_count > 0:
                st.success(f"✅ Added **{success_count}** item(s) to your closet!")
                st.balloons()

# --- 5. THE VIRTUAL CLOSET (Grid View) ---
st.write("")  # spacer
st.markdown('<div class="drip-section-header reveal reveal-1">🛒 Your Virtual Closet</div>', unsafe_allow_html=True)
st.write("")  # spacer

if not st.session_state.closet:
    st.markdown("""
    <div class="drip-empty-closet reveal reveal-2">
        <div class="icon">👗</div>
        <p>Your closet is empty.<br>Upload images above to start your collection!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    cols = st.columns(3)
    for idx, entry in enumerate(st.session_state.closet):
        with cols[idx % 3]:
            with st.container(border=True):
                st.image(entry["image"], use_container_width=True)
                info = entry["details"]
                st.markdown(f"**{info['item']}**")
                st.caption(f"{info['color']} · {info['style']}")

                p_url = get_pinterest_link(info['tags'])
                st.link_button("🔥 Find Inspo", p_url)

                with st.expander("💀 The Roast"):
                    st.write(info['roast'])
                    st.markdown(f"**Drip Score: {info['score']}/10**")

# --- 6. OUTFIT COMBINATIONS ---
st.write("")  # spacer
st.markdown('<div class="drip-section-header reveal reveal-2">🔀 Outfit Combinations</div>', unsafe_allow_html=True)
st.write("")  # spacer

if len(st.session_state.closet) < 2:
    st.markdown("""
    <div class="drip-empty-closet reveal reveal-2">
        <div class="icon">✨</div>
        <p>Add at least 2 items to your closet<br>to unlock outfit combinations!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    max_combo = min(len(st.session_state.closet), 6)
    if max_combo > 2:
        combo_size = st.slider(
            "Items per outfit",
            min_value=2,
            max_value=max_combo,
            value=2,
            help="How many items to combine into one outfit"
        )
    else:
        combo_size = 2

    closet_items = st.session_state.closet
    possible_combos = list(itertools.combinations(range(len(closet_items)), combo_size))
    st.caption(f"🧮 {len(possible_combos)} possible combination(s) with {combo_size} items")

    if st.button("✨ Generate Outfit Combos"):
        if not api_key:
            st.error("Missing Gemini API Key! Check your .env file.")
        else:
            st.session_state.combos = []  # reset
            client = genai.Client(api_key=api_key)

            # Limit to 10 combos max to avoid API overuse
            combos_to_process = possible_combos[:10]
            if len(possible_combos) > 10:
                st.info(f"Showing the first 10 of {len(possible_combos)} combinations.")

            progress = st.progress(0, text="Mixing outfits...")

            for ci, combo_indices in enumerate(combos_to_process):
                progress.progress(ci / len(combos_to_process), text=f"🧵 Rating combo {ci + 1}...")
                items_in_combo = [closet_items[i] for i in combo_indices]
                item_descriptions = [
                    f"- {it['details']['item']} ({it['details']['color']}, {it['details']['style']})"
                    for it in items_in_combo
                ]
                desc_text = "\n".join(item_descriptions)

                try:
                    combo_prompt = f"""
You are a fashion stylist. I have selected these clothing items for an outfit:
{desc_text}

Rate this outfit combination. Return ONLY a JSON object:
{{
    "combo_name": "a creative 2-3 word outfit name",
    "vibe": "the overall aesthetic/vibe of the combo",
    "rating": "1-10 rating for how well these pieces go together",
    "verdict": "one sentence on why this works or doesn't",
    "tip": "one actionable improvement suggestion"
}}
Do not include markdown formatting or extra text.
"""
                    # Send images along for visual context
                    combo_images = [it["image"] for it in items_in_combo]
                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=[combo_prompt] + combo_images
                    )

                    raw = response.text.strip().replace("```json", "").replace("```", "")
                    combo_data = json.loads(raw)

                    st.session_state.combos.append({
                        "indices": combo_indices,
                        "details": combo_data
                    })
                except Exception as e:
                    st.warning(f"Combo {ci + 1} failed: {e}")

            progress.progress(1.0, text="✅ All combos rated!")

    # Display generated combos
    if st.session_state.combos:
        st.write("")
        for ci, combo in enumerate(st.session_state.combos):
            cdata = combo["details"]
            items_in_combo = [closet_items[i] for i in combo["indices"]]

            with st.container(border=True):
                # Combo header
                header_cols = st.columns([3, 1])
                with header_cols[0]:
                    st.markdown(f"### {cdata.get('combo_name', 'Outfit')}")
                    st.caption(f"🎨 {cdata.get('vibe', 'N/A')}")
                with header_cols[1]:
                    st.markdown(f"<p style='font-size:2.5rem; font-weight:900; color:#008080; text-align:right; line-height:1;'>{cdata.get('rating', '?')}<span style='font-size:1rem; color:#78716C;'>/10</span></p>", unsafe_allow_html=True)

                # Item thumbnails in a row
                thumb_cols = st.columns(len(items_in_combo))
                for ti, it in enumerate(items_in_combo):
                    with thumb_cols[ti]:
                        st.image(it["image"], use_container_width=True)
                        st.caption(it["details"]["item"])

                # Verdict & Tip
                st.markdown(f"**Verdict:** {cdata.get('verdict', '')}")
                st.markdown(f"💡 **Tip:** {cdata.get('tip', '')}")

                # Pinterest link for the whole combo
                combo_tags = " ".join([it["details"]["tags"] for it in items_in_combo])
                st.link_button("🔥 Find Combo Inspo", get_pinterest_link(combo_tags))

# --- 7. FOOTER ---
st.markdown("""
<div class="drip-footer reveal reveal-3">
    Powered by <a href="https://deepmind.google/technologies/gemini/" target="_blank">Gemini 2.5 Flash</a>
    · Vibe Coded with Antigravity
</div>
""", unsafe_allow_html=True)