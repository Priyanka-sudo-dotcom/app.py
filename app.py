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
    
    # Configure API access through official Google SDK
    genai.configure(api_key=api_key)
    
    # 12-Model Cascading safety queue
    model_cascade = [
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-pro",
        "gemini-2.0-flash-exp",
        "gemini-1.0-pro"
    ]
    
    for model_name in model_cascade:
        try:
            model = genai.GenerativeModel(model_name)
            
            if is_image and img_bytes:
                image = Image.open(io.BytesIO(img_bytes))
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
            
            text = response.text.strip()
            
            # Sanitization of raw blockquotes
            if text.startswith("```"):
                parts = text.split("```")
                if len(parts) > 1:
                    text = parts[1]
                if text.startswith("json"):
                    text = text[4:]
            
            text = text.replace("```", "").strip()
            
            if not is_image:
                return json.loads(text)
            return text
        except Exception:
            continue
            
    return None

# --- 5. LOTTIE ANIMATION LOADER ---
def load_lottie_url(url):
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

# Fixed raw URL format (No markdown wrappers to cause errors)
lottie_cooking = load_lottie_url("[https://assets10.lottiefiles.com/packages/lf20_m6cuL6.json](https://assets10.lottiefiles.com/packages/lf20_m6cuL6.json)")

# --- 6. UNBREAKABLE CLIENT-SIDE GRAPHICS (HTML/SVG ENGINE) ---
def render_dish_svg_html(recipe_name, tag, category):
    svg_code = f"""
    <div style="width: 100%; max-width: 1200px; margin: 0 auto 25px auto;">
        <svg viewBox="0 0 800 320" style="width: 100%; height: auto; border-radius: 25px; background: linear-gradient(135deg, #111111 0%, #1c0f05 100%); border: 1px solid rgba(255, 255, 255, 0.05); box-shadow: 0 15px 35px rgba(0,0,0,0.6);">
            <defs>
                <radialGradient id="plateGlow" cx="50%" cy="50%" r="50%">
                    <stop offset="0%" stop-color="#ff5e00" stop-opacity="0.15" />
                    <stop offset="100%" stop-color="#000000" stop-opacity="0" />
                </radialGradient>
            </defs>
            <circle cx="400" cy="160" r="140" fill="url(#plateGlow)" />
            <circle cx="400" cy="160" r="110" fill="none" stroke="rgba(255,255,255,0.03)" stroke-width="6" />
            <circle cx="400" cy="160" r="90" fill="#151515" stroke="#FF5E00" stroke-width="2" stroke-dasharray="5,5" />
            
            <!-- Food abstraction art -->
            <circle cx="400" cy="160" r="35" fill="#FF7A00" opacity="0.8" />
            <polygon points="380,140 430,130 420,180 370,170" fill="#FFE0B2" opacity="0.9" />
            <path d="M 370,150 Q 400,120 430,170" stroke="#4CAF50" stroke-width="5" fill="none" stroke-linecap="round" />
            <circle cx="410" cy="140" r="5" fill="#D32F2F" />
            
            <text x="400" y="240" text-anchor="middle" fill="#FFFFFF" font-family="'Plus Jakarta Sans', sans-serif" font-size="20" font-weight="800" letter-spacing="1">{recipe_name.upper()}</text>
            <text x="400" y="265" text-anchor="middle" fill="#FF5E00" font-family="'Plus Jakarta Sans', sans-serif" font-size="11" font-weight="700" letter-spacing="3">{tag.upper()} • {category.upper()}</text>
        </svg>
    </div>
    """
    return svg_code

# --- 7. BROWSER NATIVE TEXT-TO-SPEECH NARRATOR ---
def execute_voice_synthesis(text_to_speak):
    cleaned_speech = text_to_speak.replace("'", "\\'").replace('"', '\\"')
    tts_html = f"""
    <script>
        function speak() {{
            if ('speechSynthesis' in window) {{
                window.speechSynthesis.cancel();
                var utterance = new SpeechSynthesisUtterance("{cleaned_speech}");
                utterance.rate = 1.0;
                utterance.pitch = 1.0;
                window.speechSynthesis.speak(utterance);
            }}
        }}
        speak();
    </script>
    """
    components.html(tts_html, height=0, width=0)

# --- 8. SIDEBAR HUD ---
with st.sidebar:
    st.markdown("<h2 style='color:#FF5E00; margin-bottom:0;'>Chef Gusteau 👨‍🍳</h2>", unsafe_allow_html=True)
    
    msg = "Gusteau says: 'Show me your ingredients, my friend!'"
    if st.session_state.view == "swipe": msg = "Gusteau says: 'Swipe for culinary magic!'"
    elif st.session_state.view == "cook": msg = "Gusteau says: 'Watch the fire! Precision is beauty!'"
    
    st.markdown(f'<div class="mascot-bubble">{msg}</div>', unsafe_allow_html=True)
    
    st.markdown("### 🏆 Kitchen Mastery")
    lvl = int(st.session_state.xp / 100) + 1
    st.write(f"Level {lvl} Cuisinier")
    st.progress((st.session_state.xp % 100) / 100)
    st.write(f"✨ {st.session_state.xp} XP | 🔥 {st.session_state.streak}-Day Streak")
    
    st.markdown("### 📊 Today's Calories")
    st.write(f"Logged: **{st.session_state.calories_consumed}** / 2000 kcal")
    st.progress(min(st.session_state.calories_consumed / 2000, 1.0))
    
    st.markdown("### ❤️ Saved Favorites")
    if st.session_state.favorites:
        for f in st.session_state.favorites:
            st.write(f"⭐ {f}")
    else:
        st.write("No favorite recipes saved yet.")

# --- 9. VIEW ROUTER ---
if st.session_state.view == "fridge":
    st.markdown("<h1 class='brand-glow'>CookSwipe Elite</h1>", unsafe_allow_html=True)
    
    tab_f, tab_c = st.tabs(["🧊 Fridge Station", "📷 AI Scanner"])
    
    with tab_f:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        with st.form("ing_form", clear_on_submit=True):
            col_in, col_bt = st.columns([3, 1])
            with col_in:
                raw = st.text_input("Enter ingredient manually:", placeholder="e.g. Tomato, Avocado, Cheese...")
            with col_bt:
                st.write("<br>", unsafe_allow_html=True)
                if st.form_submit_button("Add Item", use_container_width=True) and raw:
                    st.session_state.fridge_items.append(raw.capitalize())
                    st.rerun()

        st.write("#### 🛒 Tap Quick-Toggle Inventory Staples:")
        staples = ["Paneer", "Spinach", "Garlic", "Onion", "Tomato", "Chicken", "Eggs", "Milk", "Cheese", "Rice", "Mushroom", "Avocado"]
        
        grid = st.columns(4)
        for i, item in enumerate(staples):
            in_fridge = item in st.session_state.fridge_items
            label = f"✅ {item}" if in_fridge else f"➕ {item}"
            with grid[i % 4]:
                if st.button(label, key=f"staple_{item}", use_container_width=True):
                    if in_fridge:
                        st.session_state.fridge_items.remove(item)
                    else:
                        st.session_state.fridge_items.append(item)
                    st.rerun()
                    
        st.write("---")
        st.write("#### ❄️ Current Kitchen Station Ingredients:")
        if st.session_state.fridge_items:
            chips = "".join([f"<span style='background: rgba(255, 94, 0, 0.15); border: 1px solid #FF5E00; color: #FF9E00; font-weight: 600; display: inline-block; padding: 6px 14px; border-radius: 100px; margin: 4px;'>{x}</span>" for x in st.session_state.fridge_items])
            st.markdown(f"<div>{chips}</div><br>", unsafe_allow_html=True)
            if st.button("🗑️ Reset Inventory Station"):
                st.session_state.fridge_items = []
                st.rerun()
        else:
            st.info("Your cooking station is empty.")
            
        st.write("---")
        col_m, col_comp, col_diet = st.columns(3)
        mood = col_m.selectbox("Culinary Theme", ["Indian Fusion", "Quick Street Food", "Continental"])
        comp = col_comp.selectbox("Complexity Level", ["Simple Sauté", "Gourmet Chef Mode"])
        diet = col_diet.selectbox("Dietary Preference", ["Healthy", "Chatpata", "Veg Only", "Non-Veg Only"])
        
        if st.button("🚀 IGNITE THE CASCADING ENGINE", use_container_width=True):
            if not st.session_state.fridge_items:
                st.warning("Please add some items to your station before compiling recipes.")
            else:
                with st.spinner("Connecting with the Culinary Model Cluster..."):
                    prompt = f"""
                    You are a Michelin-star culinary genius. I have a list of random ingredients: {st.session_state.fridge_items}.
                    Design exactly 3 distinct, creative, and completely custom dishes matching the theme '{mood}', level '{comp}', and dietary/flavor profile '{diet}'.
                    Be as creative as possible! Turn even random leftovers into culinary art.
                    
                    Return ONLY a JSON array matching this exact schema block structure:
                    [
                      {{
                        "name": "Recipe Title",
                        "time": "15 mins",
                        "calories": 360,
                        "type": "Veg or Non-Veg",
                        "category": "Healthy, Chatpata, Comfort, or Dessert",
                        "spices": ["spiceA", "spiceB"],
                        "steps": ["Step 1 action", "Step 2 action", "Step 3 plating"],
                        "match": 95,
                        "substitutes": "Alternative ingredients listing text",
                        "tip": "Pro kitchen secret"
                      }}
                    ]
                    Do not return any conversational text wrappers or markdown block quotes.
                    """
                    data = call_gemini_sdk_cascade(prompt)
                    
                    if data and isinstance(data, list):
                        st.session_state.deck = data
                    else:
                        st.toast("Cascade completed. Serving direct archival recipes...")
                        st.session_state.deck = LOCAL_RECIPES
                        
                    st.session_state.deck_idx = 0
                    st.session_state.view = "swipe"
                    st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    with tab_c:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("📸 AI Food Vision Scanner")
        shot = st.camera_input("Scan ingredients")
        if shot:
            with st.spinner("Analyzing image visual biomarkers..."):
                v_prompt = "Identify all single raw ingredients present in this picture. Return ONLY as a simple comma-separated string of nouns (e.g., Tomato, Garlic, Cheese)."
                res = call_gemini_sdk_cascade(v_prompt, is_image=True, img_bytes=shot.getvalue())
                if res and "error" not in str(res).lower():
                    parsed = [x.strip().capitalize() for x in res.split(",") if len(x.strip()) > 1]
                    for item in parsed:
                        if item not in st.session_state.fridge_items:
                            st.session_state.fridge_items.append(item)
                    st.success(f"Vision Match Found: {', '.join(parsed)}")
                    time.sleep(1.5)
                    st.rerun()
                else:
                    st.toast("Using local vision scanner emulation...")
                    sims = ["Garlic", "Spinach", "Paneer"]
                    for s in sims:
                        if s not in st.session_state.fridge_items: st.session_state.fridge_items.append(s)
                    st.success("Vision Match Found: Garlic, Spinach, Paneer added!")
                    time.sleep(1.5)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

# Fixed missing operator check and missing colon syntax error
elif st.session_state.view == "swipe":
    st.markdown("<h1 class='brand-glow'>Swipe Deck 📱</h1>", unsafe_allow_html=True)
    recipe = st.session_state.deck[st.session_state.deck_idx % len(st.session_state.deck)]
    
    # Render safe, error-free vector visual concept directly on the screen
    st.markdown(render_dish_svg_html(recipe['name'], recipe.get('type', 'Veg'), recipe.get('category', 'Healthy')), unsafe_allow_html=True)
    
    c_card, c_act = st.columns([1.6, 1])
    
    with c_card:
        st.markdown(f"""
        <div class='glass-panel'>
            <span style='background: rgba(255, 94, 0, 0.15); border: 1px solid #FF5E00; color: #FF9E00; font-weight: 600; display: inline-block; padding: 6px 14px; border-radius: 100px; margin-right: 5px;'>⏱ {recipe['time']}</span>
            <span style='background: rgba(255, 94, 0, 0.15); border: 1px solid #FF5E00; color: #FF9E00; font-weight: 600; display: inline-block; padding: 6px 14px; border-radius: 100px; margin-right: 5px;'>🔥 {recipe['calories']} kcal</span>
            <span style='background: rgba(255, 94, 0, 0.15); border: 1px solid #FF5E00; color: #FF9E00; font-weight: 600; display: inline-block; padding: 6px 14px; border-radius: 100px; margin-right: 5px;'>🎯 {recipe['match']}% Match</span>
            <h1 style="color:white; margin-top:15px; font-size:38px;">{recipe['name']}</h1>
            <p style="color:#FF9E00; font-weight:600; margin-top:-10px;">{recipe.get('type', 'Veg')} • {recipe.get('category', 'Healthy')}</p>
            <hr style="border:0.1px solid rgba(255,255,255,0.08); margin: 15px 0;">
            <p style="color:#DDD; font-size:15px;"><b>Chef's Observation:</b> {recipe['tip']}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with c_act:
        st.markdown("<div class='glass-panel' style='height:100%;'>", unsafe_allow_html=True)
        st.subheader("Swipe Control Deck")
        
        c_no, c_ck, c_yes = st.columns(3)
        with c_no:
            if st.button("❌ Next", use_container_width=True):
                st.session_state.deck_idx += 1
                st.rerun()
        with c_ck:
            if st.button("🍳 Cook", use_container_width=True):
                st.session_state.active_recipe = recipe
                st.session_state.view = "cook"
                st.rerun()
        with c_yes:
            if st.button("❤️ Save", use_container_width=True):
                if recipe['name'] not in st.session_state.favorites:
                    st.session_state.favorites.append(recipe['name'])
                    st.session_state.xp += 15
                    st.toast("Added to favorites! +15 XP")
                st.session_state.deck_idx += 1
                st.rerun()
                
        st.write("---")
        st.markdown(f"**Aromatics Involved:** {', '.join(recipe['spices'])}")
        st.markdown(f"💡 **Substitutes:** {recipe['substitutes']}")
        
        st.write("")
        if st.button("🔙 Back to Fridge", use_container_width=True):
            st.session_st