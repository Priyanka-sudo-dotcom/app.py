import streamlit as st
import google.generativeai as genai
import json
import requests
from streamlit_lottie import st_lottie

# --- 1. SETTINGS & LUXURY GLASS UI ---
st.set_page_config(page_title="CookSwipe Ultra", page_icon="💎", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at top right, #1a1a1a, #000000);
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: white;
    }
    
    /* Glassmorphism Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 40px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
        animation: fadeIn 1.2s ease-in-out;
    }

    @keyframes fadeIn { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }

    .stat-pill {
        background: linear-gradient(90deg, #FF6B00, #FF3D00);
        padding: 6px 18px;
        border-radius: 100px;
        font-weight: 700;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .stButton>button {
        background: white !important;
        color: black !important;
        border-radius: 50px !important;
        font-weight: 800 !important;
        border: none !important;
        height: 60px !important;
        transition: all 0.4s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 30px rgba(255,255,255,0.2);
    }
</style>
""", unsafe_allow_html=True)

# --- 2. ASSETS & AI TOOLS ---
def load_lottie(url):
    r = requests.get(url)
    return r.json() if r.status_code == 200 else None

cook_lottie = load_lottie("https://assets10.lottiefiles.com/packages/lf20_m6cuL6.json")

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("🔑 API Key Missing in Secrets!")

# --- 3. THE SIDEBAR (ADVANCED OPTIONS) ---
with st.sidebar:
    st.markdown("### 🎚️ Culinary Controls")
    flavor = st.selectbox("Cuisine Style", ["Authentic Indian", "Modern Fusion", "Minimalist", "High-Protein", "Street Food"])
    servings = st.slider("Servings", 1, 6, 2)
    complexity = st.select_slider("Technique", ["Fast", "Standard", "Chef Mode"])

# --- 4. THE MAIN INTERFACE ---
st.markdown("<h1 style='font-size: 60px; font-weight: 800; margin-bottom: 0;'>CookSwipe <span style='color:#FF6B00;'>Ultra</span></h1>", unsafe_allow_html=True)
st.write("### Infinite variations. Michelin-star AI logic.")

col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    st.write("#### 📥 What's in your station?")
    ingredients = st.text_area("List ingredients...", "Paneer, Spinach, Garlic, Cream", height=150)
    
    if st.button("✨ GENERATE VARIATIONS"):
        if ingredients:
            with st.spinner("🎨 Curating flavor profiles..."):
                # The "Infinite Variation" Prompt
                prompt = f"""
                Create a {flavor} {complexity} recipe using: {ingredients}.
                For {servings} servings. Use professional culinary language.
                Return ONLY a JSON:
                {{"name": "...", "time": "...", "calories": "...", "spices": [], "steps": [], "vibe": "..."}}
                """
                try:
                    # Using the latest 2026 free model
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                    res_text = response.text.replace('```json', '').replace('```', '').strip()
                    st.session_state.recipe = json.loads(res_text)
                except Exception as e:
                    st.error("Connection hiccup. Try again!")

# --- 5. THE OUTPUT (LUXURY DISPLAY) ---
if 'recipe' in st.session_state:
    res = st.session_state.recipe
    with col_out:
        # Stable HD Image from Pexels/Unsplash API
        image_query = res['name'].replace(" ", "+")
        st.markdown(f"""
            <img src="https://images.unsplash.com/photo-1504674900247-0877df9cc836?q=80&w=2070&auto=format&fit=crop" 
            style="width:100%; border-radius:40px; margin-bottom:20px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                <span class="stat-pill">⏱ {res['time']}</span>
                <span class="stat-pill">🥗 {res['calories']} KCAL</span>
                <span class="stat-pill">✨ {res['vibe']}</span>
            </div>
            <h1 style="font-size: 45px; margin-bottom: 10px;">{res['name']}</h1>
            <p style="color: #aaa; font-size: 18px;">Expertly tailored for {servings} people using {flavor} techniques.</p>
            <hr style="border: 0.1px solid rgba(255,255,255,0.1); margin: 30px 0;">
            
            <h3 style="color:#FF6B00;">The Spice Palette</h3>
            <p style="font-size: 18px;">{", ".join(res['spices'])}</p>
            
            <h3 style="color:#FF6B00; margin-top:30px;">Execution Steps</h3>
            {"".join([f"<div style='margin-bottom:15px; font-size:18px;'><b style='color:#FF6B00;'>{i+1}.</b> {s}</div>" for i, s in enumerate(res['steps'])])}
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
else:
    with col_out:
        st_lottie(cook_lottie, height=400, key="initial")
        st.markdown("<p style='text-align:center; color:#555;'>Ready to transform your ingredients into art.</p>", unsafe_allow_html=True)
