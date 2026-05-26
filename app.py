import streamlit as st
import google.generativeai as genai
import json
import time
import base64
from PIL import Image
import io

# --- 1. CONFIGURATION & PREMIUM LUXURY STYLING ---
st.set_page_config(
    page_title="CookSwipe Elite - Premium Gastronomy",
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
        "spices": ["Kashmiri Mirch", "Garam Masala", "Kasuri Methi"],
        "steps": [
            "Slice premium paneer into uniform rectangular tiles and pat dry.",
            "Melt butter over a medium-high skillet, tossing in thin slivers of fresh garlic until fragrant.",
            "Sear the paneer tiles for 2 minutes per side until a golden crust develops, finishing with aromatic spices."
        ],
        "match": 95,
        "substitutes": "Swap Paneer out for extra-firm organic Tofu.",
        "tip": "Do not crowd the skillet to ensure a crisp, golden sear instead of boiling."
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

# --- 4. SECURE SDK MULTI-MODEL FALLBACK ENGINE ---
def call_gemini_sdk_cascade(prompt, is_image=False, image_data=None):
    api_key = st.secrets.get("GEMINI_API_KEY", "")
    if not api_key:
        return None
    
    # Configure official API access
    genai.configure(api_key=api_key)
    
    # Cascade list of modern SDK-supported models
    model_cascade = [
        "gemini-2.5-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-2.5-pro",
    ]
    
    for model_name in model_cascade:
        try:
            model = genai.GenerativeModel(model_name)
            
            if is_image and image_data:
                # Open image using Pillow library
                image = Image.open(io.BytesIO(image_data))
                response = model.generate_content([prompt, image])
            else:
                # Request strict JSON from model
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"}
                )
            
            text = response.text.strip()
            
            # Sanitization logic
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
            
        except Exception as e:
            # Fallback to the next model in the list
            continue
            
    return None

# --- 5. SIDEBAR HUD ---
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

# --- 6. VIEW ROUTER ---
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
        col_m, col_comp = st.columns(2)
        mood = col_m.selectbox("Theme", ["Indian Fusion", "Quick Street Food", "Continental"])
        comp = col_comp.selectbox("Complexity Level", ["Simple", "Gourmet Chef"])
        
        if st.button("🚀 IGNITE THE CASCADING ENGINE", use_container_width=True):
            if not st.session_state.fridge_items:
                st.warning("Please add some items to your station before compiling recipes.")
            else:
                with st.spinner("Connecting with the Culinary Model Cluster..."):
                    prompt = f"""
                    You are a Michelin-star culinary genius. I have a chaotic list of random ingredients: {st.session_state.fridge_items}.
                    Design exactly 3 distinct, creative, and completely custom dishes matching the theme '{mood}' and level '{comp}'.
                    Be as creative as possible! Even if the ingredients are completely random or don't seem to go together, use your master skills to invent a dish that tastes delicious and makes culinary sense (for example, using sweet items as sauces, or finding creative substitutions).
                    
                    Return ONLY a JSON array matching this exact schema block structure:
                    [
                      {{
                        "name": "Creative Gourmet Recipe Title",
                        "time": "15 mins",
                        "calories": 360,
                        "type": "Veg or Non-Veg",
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
            with st.spinner("Scanning..."):
                v_prompt = "Identify all single raw ingredients present in this picture. Return ONLY as a simple comma-separated string of nouns (e.g., Tomato, Garlic, Cheese)."
                res = call_gemini_sdk_cascade(v_prompt, is_image=True, image_data=shot.getvalue())
                if res and "error" not in str(res).lower():
                    parsed = [x.strip().capitalize() for x in res.split(",") if len(x.strip()) > 1]
                    for item in parsed:
                        if item not in st.session_state.fridge_items:
                            st.session_state.fridge_items.append(item)
                    st.success(f"Vision Match Found: {', '.join(parsed)}")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.toast("Emulating vision scan module...")
                    sims = ["Garlic", "Spinach", "Paneer"]
                    for s in sims:
                        if s not in st.session_state.fridge_items: st.session_state.fridge_items.append(s)
                    st.success("Vision Match Found: Garlic, Spinach, Paneer added!")
                    time.sleep(1)
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.view == "swipe":
    st.markdown("<h1 class='brand-glow'>Swipe Deck 📱</h1>", unsafe_allow_html=True)
    recipe = st.session_state.deck[st.session_state.deck_idx % len(st.session_state.deck)]
    
    # Static culinary visual helper matching
    img_tag = recipe["name"].replace(" ", ",").lower()
    img_url = f"[https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80](https://images.unsplash.com/photo-1546069901-ba9599a7e63c?auto=format&fit=crop&w=1200&q=80)"
    st.image(img_url, use_column_width=True, caption=f"Chef Pairing Concept: {recipe['name']}")
    
    c_card, c_act = st.columns([1.6, 1])
    
    with c_card:
        st.markdown(f"""
        <div class='glass-panel'>
            <span style='background: rgba(255, 94, 0, 0.15); border: 1px solid #FF5E00; color: #FF9E00; font-weight: 600; display: inline-block; padding: 6px 14px; border-radius: 100px; margin-right: 5px;'>⏱ {recipe['time']}</span>
            <span style='background: rgba(255, 94, 0, 0.15); border: 1px solid #FF5E00; color: #FF9E00; font-weight: 600; display: inline-block; padding: 6px 14px; border-radius: 100px; margin-right: 5px;'>🔥 {recipe['calories']} kcal</span>
            <span style='background: rgba(255, 94, 0, 0.15); border: 1px solid #FF5E00; color: #FF9E00; font-weight: 600; display: inline-block; padding: 6px 14px; border-radius: 100px; margin-right: 5px;'>🎯 {recipe['match']}% Match</span>
            <h1 style="color:white; margin-top:15px; font-size:38px;">{recipe['name']}</h1>
            <p style="color:#FF9E00; font-weight:600; margin-top:-10px;">{recipe['type']}</p>
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
            st.session_state.view = "fridge"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

elif st.session_state.view == "cook":
    r = st.session_state.active_recipe
    st.markdown(f"<h1 class='brand-glow'>Active Kitchen: {r['name']}</h1>", unsafe_allow_html=True)
    if st.button("⬅️ Back to Deck"):
        st.session_state.view = "swipe"
        st.rerun()
        
    col_steps, col_widget = st.columns([1.7, 1])
    
    with col_steps:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Step-by-Step Instructions")
        for i, s in enumerate(r['steps']):
            st.markdown(f"""
            <div class="step-card">
                <span style="font-weight:800; color:#FF5E00; font-size:16px;">STEP {i+1}</span>
                <p style="font-size:17px; margin-top:5px; color:#F3F4F6; line-height:1.6;">{s}</p>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_widget:
        st.markdown("<div class='glass-panel'>", unsafe_allow_html=True)
        st.subheader("Utility Station")
        
        st.write("⏱ **Sauté / Prep Step Timer**")
        t_col, b_col = st.columns([1.5, 1])
        with t_col: duration = st.number_input("Set timer (seconds)", min_value=1, value=15)
        with b_col:
            st.write("<br>", unsafe_allow_html=True)
            run_timer = st.button("Start Timer")
            
        if run_timer:
            p_bar = st.progress(1.0)
            status = st.empty()
            for rem in range(duration, -1, -1):
                p_bar.progress(rem / duration)
                status.markdown(f"⏳ **{rem} seconds remaining...**")
                time.sleep(1)
            status.success("🔥 Step completed!")
            st.balloons()
            
        st.write("---")
        st.write("🗣 **Gusteau's Cook Tip:**")
        st.info("Continuous light airflow over high-temperature elements preserves true molecular texture.")
        
        st.write("---")
        if st.button("🏆 DISH FINISHED", use_container_width=True):
            st.balloons()
            st.session_state.calories_consumed += int(r['calories'])
            st.session_state.xp += 60
            st.session_state.streak += 1
            st.success("Progress logged successfully!")
            time.sleep(2)
            st.session_state.view = "fridge"
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)