import streamlit as st
import json
import google.generativeai as genai
import requests
import time
from PIL import Image
import io
import streamlit.components.v1 as components
from streamlit_lottie import st_lottie

# --- 1. CONFIGURATION & PREMIUM LUXURY STYLING ---
st.set_page_config(
    page_title="CookSwipe Elite - AI Gastronomy",
    page_icon="🥘",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Dark Luxury Glassmorphism CSS Injector
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        background-color: #030303;
        font-family: 'Plus Jakarta Sans', sans-serif;
        color: #F3F4F6;
    }
    
    [data-testid="stHeader"] {
        background-color: rgba(3, 3, 3, 0.5);
        backdrop-filter: blur(12px);
    }
    
    .brand-glow {
        font-size: 52px;
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

# --- 2. FAILSAFE COMPREHENSIVE LOCAL DATABASE ---
LOCAL_RECIPES = [
    {
        "name": "Artisanal Pan-Seared Shahi Paneer",
        "time": "12 mins",
        "calories": 340,
        "type": "Veg",
        "category": "Chatpata",
        "spices": ["Kashmiri Mirch", "Garam Masala", "Kasuri Methi"],
        "steps": [
            "Slice premium paneer into uniform rectangular tiles and pat dry.",
            "Melt butter over a medium-high skillet, tossing in thin slivers of fresh garlic until fragrant.",
            "Sear the paneer tiles for 2 minutes per side until a golden crust develops, finishing with aromatic spices."
        ],
        "match": 95,
        "substitutes": "Swap Paneer out for extra-firm organic Tofu.",
        "tip": "Do not crowd the skillet to ensure a crisp, golden sear instead of boiling."
    },
    {
        "name": "Velvet Garlic Spinach Sauté",
        "time": "8 mins",
        "calories": 180,
        "type": "Veg",
        "category": "Healthy",
        "spices": ["Black Pepper", "Crushed Cumin", "Sea Salt"],
        "steps": [
            "Wash and thoroughly dry fresh spinach leaves to prevent soggy water pockets.",
            "Heat cold-pressed oil in a deep wok and gently brown minced garlic and sliced onions.",
            "Fold in the spinach in batches, allowing it to wilt gently over medium heat while maintaining vibrant green color."
        ],
        "match": 90,
        "substitutes": "Kale or Swiss chard can replace spinach perfectly.",
        "tip": "Finish with a squeeze of fresh lemon juice right at the end to unlock natural iron absorption."
    },
    {
        "name": "Emerald Paneer & Spiced Spinach Stir-Fry",
        "time": "15 mins",
        "calories": 310,
        "type": "Veg",
        "category": "Healthy",
        "spices": ["Garam Masala", "Turmeric", "Cumin Seeds"],
        "steps": [
            "Blanch the fresh spinach leaves and puree them into a silky smooth base with a touch of green chili.",
            "Sauté cumin seeds and finely chopped onions in warm oil until sweet and caramelized.",
            "Stir-fry the paneer cubes lightly, then fold them into the spiced green spinach gravy and simmer for 5 minutes."
        ],
        "match": 98,
        "substitutes": "Substitute Paneer with pressed Tofu cubes or roasted Mushrooms.",
        "tip": "Adding a splash of cold water to the spinach puree helps preserve its gorgeous vivid emerald color."
    }
]

# --- 3. SESSION STATE ENGINE ---
if 'view' not in st.session_state: st.session_state.view = "fridge"
if 'fridge_items' not in st.session_state: st.session_state.fridge_items = ["Paneer", "Spinach", "Garlic", "Onion"]
if 'deck' not in st.session_state: st.session_state.deck = []
if 'deck_idx' not in st.session_state: st.session_state.deck_idx = 0
if 'active_recipe' not in st.session_state: st.session_state.active_recipe = None
if 'xp' not in st.session_state: st.session_state.xp = 120
if 'streak' not in st.session_state: st.session_state.streak = 2
if 'calories_consumed' not in st.session_state: st.session_state.calories_consumed = 410
if 'favorites' not in st.session_state: st.session_state.favorites = []

# --- 4. ULTIMATE CASCADING 12-MODEL OFFICIAL SDK ENGINE ---
def call_gemini_sdk_cascade(prompt, is_image=False, img_bytes=None):
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    
    genai.configure(api_key=api_key)
    model_cascade = ["gemini-2.5-flash", "gemini-1.5-flash", "gemini-1.5-pro", "gemini-2.5-pro", "gemini-2.0-flash-exp", "gemini-1.0-pro"]
    
    for model_name in model_cascade:
        try:
            model = genai.GenerativeModel(model_name)
            if is_image and img_bytes:
                image = Image.open(io.BytesIO(img_bytes))
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            text = response.text.replace("```json", "").replace("```", "").strip()
            return json.loads(text)
        except Exception:
            continue
    return None

# --- 5. LOTTIE ANIMATION LOADER ---
def load_lottie_url(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200: return r.json()
    except Exception: pass
    return None

lottie_cooking = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_m6cuL6.json")

# --- 6. UNBREAKABLE CLIENT-SIDE GRAPHICS (HTML/SVG ENGINE) ---
def render_dish_svg_html(recipe_name, tag, category):
    name_lower = recipe_name.lower()
    if "soup" in name_lower or "stew" in name_lower or "shahi" in name_lower or "gravy" in name_lower:
        food_graphic = """<path d="M 330,140 C 330,195 470,195 470,140 Z" fill="#D84315" stroke="#FF5E00" stroke-width="3" />"""
    elif "salad" in name_lower or "spinach" in name_lower or "sauté" in name_lower or "fry" in name_lower:
        food_graphic = """<path d="M 330,175 Q 400,105 470,175 Z" fill="#2E7D32" opacity="0.8" />"""
    else:
        food_graphic = """<path d="M 330,165 C 330,105 470,105 470,165 Z" fill="#ECEFF1" />"""
    return f"""<svg viewBox="0 0 800 320" style="width: 100%; height: auto;">{food_graphic}</svg>"""

# --- 7. VOICE NARRATOR ---
def execute_voice_synthesis(text_to_speak):
    tts_html = f"<script>var u = new SpeechSynthesisUtterance('{text_to_speak.replace('\'', '')}'); window.speechSynthesis.speak(u);</script>"
    components.html(tts_html, height=0, width=0)

# --- 8. VIEW ROUTER ---
if st.session_state.view == "fridge":
    st.markdown("<h1 class='brand-glow'>CookSwipe Elite</h1>", unsafe_allow_html=True)
    if st.button("🚀 IGNITE ENGINE"):
        st.session_state.deck = LOCAL_RECIPES
        st.session_state.view = "swipe"
        st.rerun()

elif st.session_state.view == "swipe":
    recipe = st.session_state.deck[st.session_state.deck_idx % len(st.session_state.deck)]
    st.markdown(render_dish_svg_html(recipe['name'], recipe.get('type', 'Veg'), recipe.get('category', 'Healthy')), unsafe_allow_html=True)
    if st.button("🍳 Cook"):
        st.session_state.active_recipe = recipe
        st.session_state.view = "cook"
        st.rerun()

elif st.session_state.view == "cook":
    r = st.session_state.active_recipe
    for i, s in enumerate(r['steps']):
        st.markdown(f"**Step {i+1}:** {s}")
        if st.button(f"🔊 Speak {i+1}", key=f"speak_{i}"): execute_voice_synthesis(s)
        
    duration = st.number_input("Timer (s)", value=15)
    if st.button("Start Timer"):
        status = st.empty()
        for rem in range(duration, -1, -1):
            status.markdown(f"⏳ **{rem}s**")
            time.sleep(1)
        status.success("🔥 Done!")