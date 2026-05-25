import streamlit as st
import json
import requests
import time
import base64
from PIL import Image
import io

# --- 1. CONFIGURATION & PREMIUM STYLING ---
st.set_page_config(
    page_title="CookSwipe Elite - Premium Gastronomy Engine",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Luxury Glassmorphism Injector
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #050505;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F3F4F6;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(5, 5, 5, 0.5);
        backdrop-filter: blur(12px);
    }
    
    .brand-glow {
        font-size: 50px;
        font-weight: 800;
        background: linear-gradient(135deg, #FF5E00 0%, #FF9E00 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -2px;
        margin-bottom: 5px;
    }
    
    .glass-panel {
        background: rgba(255, 255, 255, 0.02);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.06);
        border-radius: 25px;
        padding: 30px;
        margin-bottom: 25px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
    }
    
    .mascot-bubble {
        background: rgba(255, 94, 0, 0.07);
        border: 1px solid rgba(255, 94, 0, 0.2);
        border-radius: 20px;
        padding: 15px;
        color: #FFE6D5;
        font-style: italic;
        margin-bottom: 20px;
        font-size: 14px;
    }
    
    .step-card {
        background: rgba(255, 255, 255, 0.01);
        border-left: 4px solid #FF5E00;
        padding: 18px 20px;
        margin-bottom: 15px;
        border-radius: 0 15px 15px 0;
    }
    
    .stButton>button {
        border-radius: 14px !important;
        font-weight: 700 !important;
        transition: all 0.2s ease-in-out !important;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. FAILSAFE LOCAL DATABASE ---
LOCAL_RECIPES = [
    {
        "name": "Artisanal Pan-Seared Garlic Paneer",
        "time": "12 mins",
        "calories": 340,
        "type": "Veg",
        "spices": ["Kashmiri Mirch", "Garam Masala", "Kasuri Methi"],
        "steps": [
            "Slice premium paneer into uniform rectangular tiles and pat dry.",
            "Melt butter over a medium-high skillet, tossing in thin slivers of fresh garlic until fragrant.",
            "Sear the paneer tiles for 2 minutes per side until a golden crust develops."
        ],
        "match": 95,
        "substitutes": "Swap Paneer out for extra-firm organic Tofu.",
        "tip": "Do not crowd the skillet to ensure a crisp sear."
    }
]

# --- 3. SESSION STATE ENGINE ---
if 'view' not in st.session_state: st.session_state.view = "fridge"
if 'fridge_items' not in st.session_state: st.session_state.fridge_items = ["Paneer", "Garlic", "Onion"]
if 'deck' not in st.session_state: st.session_state.deck = []
if 'deck_idx' not in st.session_state: st.session_state.deck_idx = 0
if 'active_recipe' not in st.session_state: st.session_state.active_recipe = None
if 'xp' not in st.session_state: st.session_state.xp = 120
if 'streak' not in st.session_state: st.session_state.streak = 2
if 'calories_consumed' not in st.session_state: st.session_state.calories_consumed = 410
if 'favorites' not in st.session_state: st.session_state.favorites = []

# --- 4. HARDENED API CLIENT ---
def call_gemini(prompt, is_image=False, image_bytes=None):
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
        
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}
    
    if is_image and image_bytes:
        base64_img = base64.b64encode(image_bytes).decode("utf-8")
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inlineData": {"mimeType": "image/jpeg", "data": base64_img}}
                ]
            }]
        }
    else:
        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"responseMimeType": "application/json"}
        }

    try:
        res = requests.post(url, headers=headers, json=payload, timeout=15)
        if res.status_code == 200:
            text = res.json()['candidates'][0]['content']['parts'][0]['text'].strip()
            
            # FIXED: Sanitization logic to clean markdown strings
            if text.startswith("```"):
                parts = text.split("```")
                if len(parts) > 1:
                    text = parts[1]
                if text.startswith("json"):
                    text = text[4:]
            
            text = text.replace("```", "").strip()
            return text if is_image else json.loads(text)
    except Exception:
        pass
    return None

# --- 5. SIDEBAR HUD ---
with st.sidebar:
    st.markdown("<h2 style='color:#FF5E00; margin-bottom:0;'>Chef Gusteau 👨‍🍳</h2>", unsafe_allow_html=True)
    msg = "Gusteau says: 'Show me your ingredients, my friend!'"
    if st.session_state.view == "swipe": msg = "Gusteau says: 'Swipe for culinary magic!'"
    st.markdown(f'<div class="mascot-bubble">{msg}</div>', unsafe_allow_html=True)
    
    st.markdown("### 🏆 Kitchen Mastery")
    lvl = int(st.session_state.xp / 100) + 1
    st.write(f"Level {lvl} Cuisinier")
    st.progress((st.session_state.xp % 100) / 100)
    st.write(f"✨ {st.session_state.xp} XP | 🔥 {st.session_state.streak}-Day Streak")
    
    st.markdown("### 📊 Today's Calories")
    st.write(f"Logged: **{st.session_state.calories_consumed}** / 2000")
    st.progress(min(st.session_state.calories_consumed / 2000, 1.0))

# --- 6. VIEW ROUTER ---
if st.session_state.view == "fridge":
    st.markdown("<h1 class='brand-glow'>CookSwipe Elite</h1>", unsafe_allow_html=True)
    
    tab_f, tab_c = st.tabs(["🧊 Fridge Station", "📷 AI Scanner"])
    
    with tab_f:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        with st.form("ing_form", clear_on_submit=True):
            col_in, col_bt = st.columns([3, 1])
            with col_in:
                raw = st.text_input("Enter ingredient:")
            with col_bt:
                st.write("<br>", unsafe_allow_html=True)
                if st.form_submit_button("Add", use_container_width=True) and raw:
                    st.session_state.fridge_items.append(raw.capitalize())
                    st.rerun()

        st.write("#### Station Inventory:")
        if st.session_state.fridge_items:
            itms = ", ".join(st.session_state.fridge_items)
            st.info(f"Active: {itms}")
            if st.button("🗑️ Reset"):
                st.session_state.fridge_items = []
                st.rerun()
            
        col_m, col_comp = st.columns(2)
        mood = col_m.selectbox("Theme", ["Indian Fusion", "Quick Street Food", "Continental"])
        comp = col_comp.selectbox("Level", ["Easy", "Gourmet"])
        
        if st.button("🚀 IGNITE ENGINE", use_container_width=True):
            with st.spinner("Thinking..."):
                prompt = f"Ingredients: {st.session_state.fridge_items}. Theme: {mood}. Level: {comp}. Return JSON array with name, time, calories (int), type, spices (list), steps (list), match (int), substitutes, tip."
                data = call_gemini(prompt)
                st.session_state.deck = data if data else LOCAL_RECIPES
                st.session_state.view = "swipe"
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with tab_c:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        shot = st.camera_input("Scan ingredients")
        if shot:
            with st.spinner("Scanning..."):
                v_prompt = "List only raw ingredients in this image as a comma-separated string."
                res = call_gemini(v_prompt, is_image=True, image_bytes=shot.getvalue())
                if res:
                    for i in res.split(","):
                        st.session_state.fridge_items.append(i.strip().capitalize())
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.view == "swipe":
    st.markdown("<h1 class='brand-glow'>Swipe Deck 📱</h1>", unsafe_allow_html=True)
    recipe = st.session_state.deck[st.session_state.deck_idx % len(st.session_state.deck)]
    
    st.markdown(f"""
    <div class='glass-panel'>
        <h2>{recipe['name']}</h2>
        <p>⏱ {recipe['time']} | 🔥 {recipe['calories']} kcal | 🎯 {recipe['match']}% Match</p>
        <hr>
        <p><b>Chef's Tip:</b> {recipe['tip']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    if c1.button("❌ Next"):
        st.session_state.deck_idx += 1
        st.rerun()
    if c2.button("🍳 Cook"):
        st.session_state.active_recipe = recipe
        st.session_state.view = "cook"
        st.rerun()
    if c3.button("❤️ Save"):
        st.session_state.favorites.append(recipe['name'])
        st.session_state.xp += 15
        st.rerun()

elif st.session_state.view == "cook":
    r = st.session_state.active_recipe
    st.markdown(f"<h1 class='brand-glow'>Cooking: {r['name']}</h1>", unsafe_allow_html=True)
    
    st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
    for i, s in enumerate(r['steps']):
        st.markdown(f"<div class='step-card'><b>Step {i+1}:</b> {s}</div>", unsafe_allow_html=True)
    
    if st.button("🏆 FINISHED", use_container_width=True):
        st.session_state.calories_consumed += int(r['calories'])
        st.session_state.xp += 60
        st.session_state.view = "fridge"
        st.balloons()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)