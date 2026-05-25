import streamlit as st
import google.generativeai as genai
import json
import requests
import time
from streamlit_lottie import st_lottie

# --- 1. SETTINGS & LUXURY GLASS UI ---
st.set_page_config(page_title="CookSwipe Ultra", page_icon="💎", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background: #000000;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: white;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 40px;
        padding: 40px;
        box-shadow: 0 25px 50px rgba(0,0,0,0.5);
    }

    .stat-pill {
        background: #FF6B00;
        padding: 6px 18px;
        border-radius: 100px;
        font-weight: 700;
        font-size: 12px;
        text-transform: uppercase;
        margin-right: 10px;
    }

    .stButton>button {
        background: white !important;
        color: black !important;
        border-radius: 50px !important;
        font-weight: 800 !important;
        height: 60px !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. THE SELF-HEALING AI BRAIN ---
def call_ai_with_retry(prompt, retries=3):
    model = genai.GenerativeModel('gemini-1.5-flash')
    for i in range(retries):
        try:
            response = model.generate_content(prompt)
            # Robust JSON cleaning
            res_text = response.text.strip()
            if "```json" in res_text:
                res_text = res_text.split("```json")[1].split("```")[0]
            elif "```" in res_text:
                res_text = res_text.split("```")[1].split("```")[0]
            return json.loads(res_text.strip())
        except Exception as e:
            if i < retries - 1:
                time.sleep(2) # Wait 2 seconds before retrying
                continue
            else:
                return f"Error: {str(e)}"

try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("🔑 API Key Missing in Secrets!")

# --- 3. THE UI LAYOUT ---
st.markdown("<h1 style='font-size: 50px; font-weight: 800;'>CookSwipe <span style='color:#FF6B00;'>Ultra</span></h1>", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.8], gap="large")

with col_in:
    st.write("#### 📥 Kitchen Inventory")
    ingredients = st.text_area("What are we working with?", "Chicken, Garlic, Lemon, Honey", height=150)
    style = st.selectbox("Cuisine Vibe", ["Modern European", "Bold Asian", "Traditional Desi", "Quick & Healthy"])
    
    if st.button("✨ CREATE MASTERPIECE"):
        if ingredients:
            with st.spinner("🎨 Orchestrating flavors..."):
                prompt = f"""
                Create a {style} recipe using: {ingredients}.
                Strictly return ONLY JSON format:
                {{"name": "...", "time": "...", "calories": "...", "spices": [], "steps": [], "fact": "..."}}
                """
                result = call_ai_with_retry(prompt)
                if isinstance(result, dict):
                    st.session_state.recipe = result
                else:
                    st.error("The Chef is overwhelmed. Please wait 10 seconds and try again.")

# --- 4. THE DISPLAY ---
if 'recipe' in st.session_state:
    res = st.session_state.recipe
    with col_out:
        # Dynamic HD Image Generator
        img_keyword = res['name'].replace(" ", ",")
        img_url = f"https://loremflickr.com/1200/600/food,{img_keyword}/all"
        
        st.markdown(f'<img src="{img_url}" style="width:100%; border-radius:40px; margin-bottom:25px; box-shadow: 0 20px 40px rgba(0,0,0,0.5);">', unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="glass-card">
            <div style="margin-bottom: 25px;">
                <span class="stat-pill">⏱ {res['time']}</span>
                <span class="stat-pill">🥗 {res['calories']} KCAL</span>
            </div>
            <h1 style="font-size: 45px; margin-bottom: 15px;">{res['name']}</h1>
            <hr style="border: 0.1px solid rgba(255,255,255,0.1); margin: 30px 0;">
            
            <h3 style="color:#FF6B00;">Spice Palette</h3>
            <p style="font-size: 18px; margin-bottom:30px;">{", ".join(res['spices'])}</p>
            
            <h3 style="color:#FF6B00;">Chef's Technique</h3>
            {"".join([f"<p style='font-size:18px; margin-bottom:12px;'><b style='color:#FF6B00;'>{i+1}.</b> {s}</p>" for i, s in enumerate(res['steps'])])}
            
            <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 20px; margin-top: 30px; border-left: 5px solid #FF6B00;">
                <p style="margin:0; color:#00FF88; font-weight:bold;">✨ Pro Tip</p>
                <p style="margin:0; color:#ccc;">{res['fact']}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.balloons()
