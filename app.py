import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from PIL import Image

# Load environment variables
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

# Initialize Gemini Client
if API_KEY:
    client = genai.Client(api_key=API_KEY)
else:
    st.error("Missing GEMINI_API_KEY in .env file!")
    st.stop()

st.set_page_config(page_title="DripCheck AI", page_icon="👕", layout="centered")

# --- UI Header ---
st.title("👕 DripCheck")
st.markdown("*Your AI Stylist for the Broke & Busy*")

# --- Sidebar / Settings ---
with st.sidebar:
    st.header("Vibe Settings")
    mood = st.selectbox("What's the vibe today?", ["Casual", "Exam/Library", "Presentation", "Date Night", "Gym"])
    roast_mode = st.toggle("Enable Roast Mode 🔥", value=False)

# --- Main App Logic ---
uploaded_file = st.file_uploader("Upload your fit...", type=['jpg', 'jpeg', 'png'])

if uploaded_file:
    img = Image.open(uploaded_file)
    st.image(img, caption="Current Selection", use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✨ Style Me"):
            with st.spinner("Analyzing drip..."):
                prompt = f"Analyze this clothing item. Context: {mood} vibe. Suggest 3 combinations and explain why they work."
                response = client.models.generate_content(model="gemini-1.5-flash", contents=[prompt, img])
                st.subheader("Style Intelligence")
                st.write(response.text)
                
                # Dynamic Pinterest Link
                search_query = f"{mood}+style+outfit+inspiration"
                st.link_button("See Inspo on Pinterest", f"https://www.pinterest.com/search/pins/?q={search_query}")

    with col2:
        if roast_mode and st.button("🔥 Roast Me"):
            with st.spinner("Preparing the burn..."):
                roast_prompt = "Be a brutal fashion critic. Roast this outfit using Gen-Z slang. Keep it funny but mean."
                roast_resp = client.models.generate_content(model="gemini-2.0-flash", contents=[roast_prompt, img])
                st.error(roast_resp.text)